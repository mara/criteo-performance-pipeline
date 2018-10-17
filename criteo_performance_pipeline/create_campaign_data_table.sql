DROP TABLE IF EXISTS cr_data.campaign;

CREATE TABLE cr_data.campaign (
  campaign_id     INTEGER NOT NULL PRIMARY KEY,
  campaign_name   TEXT    NOT NULL,
  platform        TEXT    NOT NULL,
  channel         TEXT    NOT NULL,
  partner         TEXT    NOT NULL,
  advertiser_name TEXT    NOT NULL,
  currency        TEXT    NOT NULL
);
