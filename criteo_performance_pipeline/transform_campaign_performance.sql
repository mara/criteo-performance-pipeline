DROP TABLE IF EXISTS cr_dim_next.campaign_performance CASCADE;

CREATE TABLE cr_dim_next.campaign_performance (
  campaign_fk             INTEGER NOT NULL,
  day_fk                  INTEGER NOT NULL,
  clicks                  INTEGER,
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

INSERT INTO cr_dim_next.campaign_performance
  SELECT
    campaign_performance.campaign_id,
    to_char(campaign_performance.date, 'YYYYMMDD') :: INTEGER AS day_fk,
    click,
    impressions,
    ctr,
    revcpc,
    ecpm,
    cost,
    sales,
    conv_rate,
    order_value,
    sales_post_view,
    conv_rate_post_view,
    order_value_post_view,
    cost_of_sale,
    overall_competition_win / 100.0,
    cost_per_order
  FROM cr_data.campaign_performance
    JOIN cr_dim_next.campaign USING (campaign_id);


SELECT util.add_fk('cr_dim_next', 'campaign_performance', 'cr_dim_next', 'campaign');
SELECT util.add_fk('cr_dim_next', 'campaign_performance', 'time', 'day');
