CREATE TABLE cr_dim_next.campaign (
  campaign_id      INTEGER PRIMARY KEY,
  campaign_name    TEXT    NOT NULL UNIQUE,
  account_id       INTEGER NOT NULL,
  account_name     TEXT    NOT NULL,
  account_currency TEXT    NOT NULL
);

INSERT INTO cr_dim_next.campaign
  SELECT
    campaign_id,
    advertiser_name || ' - ' || campaign_name AS campaign_name,
    dense_rank()
    OVER (
      ORDER BY advertiser_name )              AS account_id,
    advertiser_name                           AS account_name,
    currency                                  AS account_currency
  FROM cr_data.campaign
  ORDER BY account_name;
