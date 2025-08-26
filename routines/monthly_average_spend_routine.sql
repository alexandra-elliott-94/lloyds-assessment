WITH MONTHLYSUM_CTE AS (
  SELECT
    cust_id,
    extract(YEAR from dt) AS year,
    extract(MONTH from dt) AS month,
    SUM(amount) AS amount_sum
  FROM `data_landing.transactions`
  GROUP BY
    cust_id,
    extract(YEAR from dt),
    extract(MONTH from dt)
)
SELECT
  cust_id, year, month,amount_sum,
  avg(amount_sum) OVER (partition by cust_id ORDER BY Year, Month) AS cumulative_average
FROM MONTHLYSUM_CTE;