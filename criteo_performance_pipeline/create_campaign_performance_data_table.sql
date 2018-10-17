DROP TABLE IF EXISTS cr_data.campaign_performance CASCADE;

CREATE TABLE cr_data.campaign_performance (
  campaign_id             INTEGER NOT NULL,
  date                    DATE    NOT NULL,
  click                   INTEGER,
  impressions             INTEGER,
  ctr                     DOUBLE PRECISION,
  revcpc                  DOUBLE PRECISION,
  ecpm                    DOUBLE PRECISION,
  cost                    DOUBLE PRECISION,
  sales                   INTEGER,
  conv_rate               DOUBLE PRECISION,
  order_value             DOUBLE PRECISION,
  sales_post_view         INTEGER,
  conv_rate_post_view     DOUBLE PRECISION,
  order_value_post_view   DOUBLE PRECISION,
  cost_of_sale            DOUBLE PRECISION,
  overall_competition_win DOUBLE PRECISION,
  cost_per_order          DOUBLE PRECISION
);

-- needed for upserting
SELECT util.add_index('cr_data', 'campaign_performance', column_names := ARRAY ['date']);

-- create an exact copy of the data table. New data will be copied here
DROP TABLE IF EXISTS cr_data.campaign_performance_upsert;

CREATE TABLE cr_data.campaign_performance_upsert AS
  SELECT *
  FROM cr_data.campaign_performance
  LIMIT 0;


CREATE OR REPLACE FUNCTION cr_data.upsert_campaign_performance()
  RETURNS VOID AS '

-- rather than doing a proper upsert, first data for the dates and campaign_ids in the upsert table
DELETE FROM cr_data.campaign_performance
USING cr_data.campaign_performance_upsert
WHERE campaign_performance_upsert.date = campaign_performance.date
      AND campaign_performance_upsert.campaign_id = campaign_performance.campaign_id;

-- copy new data in
INSERT INTO cr_data.campaign_performance
  SELECT *
  FROM cr_data.campaign_performance_upsert;

-- remove tmp data
TRUNCATE cr_data.campaign_performance_upsert;

'
LANGUAGE SQL;
