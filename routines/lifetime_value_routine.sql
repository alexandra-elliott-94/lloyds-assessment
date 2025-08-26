WITH
  monthly_sum_cte AS (
  SELECT
    cust_id,
    EXTRACT(YEAR
    FROM
      dt) AS year,
    EXTRACT(week
    FROM
      dt) AS week,
    SUM(amount) AS amount_sum
  FROM
    `data_landing.transactions`
  GROUP BY
    cust_id,
    EXTRACT(YEAR FROM dt),
    EXTRACT(week FROM dt) ),
  cumsum_per_week AS (
  SELECT
    cust_id,
    year,
    week,
    SUM(amount_sum) OVER (PARTITION BY cust_id ORDER BY year, week) AS cumulative_sum,
  FROM
    monthly_sum_cte),
  percent_rank_cte AS (
  SELECT
    cust_id,
    year,
    week,
    cumulative_sum,
    PERCENT_RANK() OVER(PARTITION BY year, week ORDER BY cumulative_sum) prnk
  FROM
    cumsum_per_week)
SELECT
  cust_id,
  year,
  week,
  cumulative_sum as lifetime_spend
FROM
  percent_rank_cte
WHERE
  prnk >= 0.95;