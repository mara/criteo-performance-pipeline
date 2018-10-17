import pathlib
from criteo_performance_pipeline import config

from data_integration.commands.files import Compression
from data_integration.commands.sql import ExecuteSQL
from data_integration.parallel_tasks.files import ParallelReadFile, ReadMode
from data_integration.pipelines import Pipeline, Task

pipeline = Pipeline(
    id="criteo",
    description="Builds the criteo cube from json files downloaded from the API",
    base_path=pathlib.Path(__file__).parent,
    labels={"Schema": "cr_dim"})

pipeline.add_initial(
    Task(id="initialize_schemas",
         description="Recreates data, tmp and dim_next schemas",
         commands=[
             ExecuteSQL(sql_statement="DROP SCHEMA IF EXISTS cr_dim_next CASCADE; CREATE SCHEMA cr_dim_next;",
                        echo_queries=False),
             ExecuteSQL(sql_statement="DROP SCHEMA IF EXISTS cr_tmp CASCADE; CREATE SCHEMA cr_tmp;",
                        echo_queries=False),
             ExecuteSQL(sql_file_name="create_data_schema.sql", echo_queries=False,
                        file_dependencies=["create_data_schema.sql"])
         ]))

pipeline.add(
    ParallelReadFile(
        id="read_campaign",
        description="Loads a csv file with criteo campaigns for all criteo accounts",
        file_pattern="criteo-account-structure-*{}.json.gz".format(config.input_file_version()),
        read_mode=ReadMode.ALL,
        compression=Compression.GZIP,
        mapper_script_file_name="read_campaign.py",
        target_table="cr_data.campaign",
        delimiter_char="\t",
        commands_before=[
            ExecuteSQL(sql_file_name="create_campaign_data_table.sql", echo_queries=False)
        ]))

pipeline.add(
    ParallelReadFile(
        id="read_campaign_performance",
        description="Loads csv files with criteo campaign performance data on a daily basis",
        file_pattern="*/*/*/criteo/campaign-performance*{}.json.gz".format(config.input_file_version()),
        read_mode=ReadMode.ONLY_CHANGED,
        compression=Compression.GZIP,
        mapper_script_file_name="read_campaign_performance.py",
        target_table="cr_data.campaign_performance_upsert",
        delimiter_char=";",
        date_regex="^(?P<year>\d{4})\/(?P<month>\d{2})\/(?P<day>\d{2})/",
        file_dependencies=['create_campaign_performance_data_table.sql'],
        commands_before=[
            ExecuteSQL(sql_file_name="create_campaign_performance_data_table.sql", echo_queries=False,
                       file_dependencies=['create_campaign_performance_data_table.sql'])
        ],
        commands_after=[
            ExecuteSQL(sql_statement='SELECT cr_data.upsert_campaign_performance()')
        ]))

pipeline.add(
    Task(id="transform_campaign",
         description="Creates dim table for criteo campaigns",
         commands=[
             ExecuteSQL(sql_file_name="transform_campaign.sql")
         ]),
    ["read_campaign"])

pipeline.add(
    Task(id="transform_campaign_performance",
         description="Creates dim table for criteo reports",
         commands=[
             ExecuteSQL(sql_file_name="transform_campaign_performance.sql")
         ]),
    ["read_campaign_performance", "transform_campaign"])

pipeline.add_final(
    Task(
        id="replace_schema",
        description="Replaces the current cr_dim schema with the contents of cr_dim_next",
        commands=[ExecuteSQL(sql_statement="SELECT util.replace_schema('cr_dim', 'cr_dim_next');")]))
