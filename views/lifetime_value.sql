WITH
  totals AS (
  SELECT
    cust_id,
    SUM(amount) AS lifetime_spend
  FROM
    `data_landing.transactions`
  GROUP BY
    cust_id),
  ranking AS (
  SELECT
    cust_id,
    lifetime_spend,
    PERCENT_RANK() OVER (ORDER BY lifetime_spend) AS pct_rank
  FROM
    totals)
SELECT
  cust_id,
  lifetime_spend
FROM
  ranking
WHERE
  pct_rank >= 0.95;