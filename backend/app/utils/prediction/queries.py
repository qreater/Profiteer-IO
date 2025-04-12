"""

 Copyright 2025 @Qreater
 Licensed under the Apache License, Version 2.0.
 See: http://www.apache.org/licenses/LICENSE-2.0

"""

from app.utils.settings.config import settings

PRODUCT_SCENARIO_METRICS_QUERY = f"""
SELECT
  AVG(views) AS views,
  AVG(cart_adds) AS cart_adds,
  ROUND(AVG(popularity_factor), 2) AS popularity_factor,
  ROUND(AVG((%s::float / NULLIF(base_price, 0))::numeric), 2) AS price_ratio
FROM public."{settings.TABLE_NAME}"
WHERE product_id = %s
  AND time_of_day_bucket = %s;
"""
