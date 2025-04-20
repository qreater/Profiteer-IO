"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from app.utils.settings.config import settings

GET_PRODUCTS_QUERY = f"""
WITH latest_day AS (
  SELECT DATE(timestamp) AS sale_date
  FROM public."{settings.TABLE_NAME}"
  GROUP BY sale_date
  ORDER BY sale_date DESC
  LIMIT 1
),

product_metrics AS (
  SELECT
    category,
    product_id,
    product_name,
    product_image,
    ROUND(AVG(rating), 2) AS average_rating,
    ROUND(SUM(current_price * purchases), 2) AS revenue
  FROM public."{settings.TABLE_NAME}"
  WHERE DATE(timestamp) = (SELECT sale_date FROM latest_day)
  GROUP BY category, product_id, product_name, product_image
),

grouped_by_category AS (
  SELECT
    category,
    json_agg(
      json_build_object(
        'product_id', product_id,
        'product_name', product_name,
        'product_image', product_image,
        'average_rating', average_rating,
        'revenue', revenue
      ) ORDER BY product_id
    ) AS products
  FROM product_metrics
  GROUP BY category
)

SELECT json_object_agg(category, products) AS data
FROM grouped_by_category;
"""


GET_PRODUCT_BY_ID_QUERY = f"""
WITH latest_day AS (
  SELECT DATE(timestamp) AS sale_date
  FROM public."{settings.TABLE_NAME}"
  GROUP BY sale_date
  ORDER BY sale_date DESC
  LIMIT 1
),

product_details AS (
  SELECT
    product_id,
    product_name,
    product_image,
    category,
    base_price,
    ROUND(AVG(rating), 2) AS average_rating,
    SUM(purchases) AS total_purchases,
    SUM(views) AS total_views,
    SUM(cart_adds) AS total_cart_adds,
    ROUND(SUM(current_price * purchases), 2) AS revenue
  FROM public."{settings.TABLE_NAME}"
  WHERE DATE(timestamp) = (SELECT sale_date FROM latest_day)
    AND product_id = %s
  GROUP BY product_id, product_name, product_image, category, base_price
),

product_graph AS (
  SELECT
    timestamp,
    views,
    cart_adds,
    purchases
  FROM public."{settings.TABLE_NAME}"
  WHERE DATE(timestamp) = (SELECT sale_date FROM latest_day)
    AND product_id = %s
  ORDER BY timestamp
),

bucket_averages AS (
  SELECT
    time_of_day_bucket,
    ROUND(AVG(purchases), 2) AS average_purchases
  FROM public."{settings.TABLE_NAME}"
  WHERE DATE(timestamp) = (SELECT sale_date FROM latest_day)
    AND product_id = %s
  GROUP BY time_of_day_bucket
),

bucket_averages_json AS (
  SELECT json_object_agg(time_of_day_bucket, average_purchases) AS average_purchases
  FROM bucket_averages
)

SELECT 
  (SELECT row_to_json(product_details) FROM product_details) AS details,
  (SELECT json_agg(product_graph) FROM product_graph) AS graph,
  (SELECT average_purchases FROM bucket_averages_json) AS average_purchases;
"""
