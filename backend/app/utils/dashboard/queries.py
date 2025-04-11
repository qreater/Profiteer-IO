"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from app.utils.settings.config import settings

DASHBOARD_SUMMARY_QUERY = f"""
WITH
  base_data AS (
    SELECT
      DATE(timestamp) AS sale_date,
      SUM(current_price * purchases) AS revenue,
      SUM(purchases) AS items_sold,
      SUM(views) AS total_views,
      SUM(purchases)::numeric / NULLIF(SUM(views), 0) AS conversion_rate
    FROM public."{settings.TABLE_NAME}"
    GROUP BY sale_date
  ),
  
  day1 AS (
    SELECT * FROM base_data ORDER BY sale_date ASC LIMIT 1
  ),

  day2 AS (
    SELECT * FROM base_data ORDER BY sale_date DESC LIMIT 1
  ),

  top_category_day2 AS (
    SELECT
      category,
      SUM(current_price * purchases) AS total_revenue
    FROM public."{settings.TABLE_NAME}"
    WHERE DATE(timestamp) = (SELECT sale_date FROM day2)
    GROUP BY category
    ORDER BY total_revenue DESC
    LIMIT 1
  )

SELECT
  d2.sale_date AS day_2_date,

  -- Revenue
  d2.revenue AS revenue_day_2,
  d1.revenue AS revenue_day_1,
  ROUND((d2.revenue - d1.revenue) / NULLIF(d1.revenue, 0) * 100, 2) AS revenue_percent_change,

  -- Items sold
  d2.items_sold AS items_day_2,
  d1.items_sold AS items_day_1,
  ROUND((d2.items_sold - d1.items_sold) / NULLIF(d1.items_sold, 0) * 100, 2) AS items_percent_change,

  -- Conversion rate
  ROUND(d2.conversion_rate * 100, 2) AS conversion_rate_day_2,
  ROUND(d1.conversion_rate * 100, 2) AS conversion_rate_day_1,
  ROUND((d2.conversion_rate - d1.conversion_rate) / NULLIF(d1.conversion_rate, 0) * 100, 2) AS conversion_rate_percent_change,

  -- Top category
  top.category AS top_category_day_2,
  top.total_revenue AS top_category_revenue_day_2

FROM day1 d1
JOIN day2 d2 ON TRUE
LEFT JOIN top_category_day2 top ON TRUE;
"""

DASHBOARD_GRAPH_QUERY = f"""
SELECT
  timestamp,
  SUM(views) AS total_views,
  SUM(cart_adds) AS total_cart_adds,
  SUM(purchases) AS total_purchases
FROM public."{settings.TABLE_NAME}"
WHERE DATE(timestamp) = (
    SELECT sale_date FROM (
        SELECT DATE(timestamp) AS sale_date
        FROM public."{settings.TABLE_NAME}"
        GROUP BY sale_date
        ORDER BY sale_date DESC
        LIMIT 1
    ) AS latest
)
GROUP BY timestamp
ORDER BY timestamp;
"""

DASHBOARD_CATEGORY_QUERY = f"""
WITH base_data AS (
  SELECT
    DATE(timestamp) AS sale_date,
    category,
    SUM(current_price * purchases) AS revenue
  FROM public."{settings.TABLE_NAME}"
  GROUP BY sale_date, category
),

day1 AS (
  SELECT * FROM base_data
  WHERE sale_date = (
    SELECT sale_date FROM base_data
    GROUP BY sale_date
    ORDER BY sale_date ASC
    LIMIT 1
  )
),

day2 AS (
  SELECT * FROM base_data
  WHERE sale_date = (
    SELECT sale_date FROM base_data
    GROUP BY sale_date
    ORDER BY sale_date DESC
    LIMIT 1
  )
),

combined AS (
  SELECT
    d2.category,
    COALESCE(d1.revenue, 0) AS revenue_day_1,
    d2.revenue AS revenue_day_2,
    (d2.revenue > COALESCE(d1.revenue, 0)) AS has_increased
  FROM day2 d2
  LEFT JOIN day1 d1 ON d2.category = d1.category
)

SELECT *
FROM combined
ORDER BY revenue_day_2 DESC
LIMIT 3;
"""

DASHBOARD_HOT_PRODUCTS_QUERY = f"""
WITH latest_day AS (
  SELECT DATE(timestamp) AS sale_date
  FROM public."{settings.TABLE_NAME}"
  GROUP BY sale_date
  ORDER BY sale_date DESC
  LIMIT 1
),

hot_products_day2 AS (
  SELECT
    product_id,
    product_name,
    product_image,
    category,
    SUM(purchases) AS total_purchases,
    SUM(current_price * purchases) AS total_revenue
  FROM public."{settings.TABLE_NAME}"
  WHERE DATE(timestamp) = (SELECT sale_date FROM latest_day)
  GROUP BY product_id, product_name, product_image, category
  ORDER BY total_purchases DESC
  LIMIT 3
)

SELECT *
FROM hot_products_day2;
"""
