  SELECT
    cust_id,
    extract(YEAR from dt) AS year,
    extract(MONTH from dt) AS month,
    SUM(amount) AS amount_sum,
    AVG(amount) AS amount_avg
  FROM `data_landing.transactions`
  GROUP BY
    cust_id,
    extract(YEAR from dt),
    extract(MONTH from dt)