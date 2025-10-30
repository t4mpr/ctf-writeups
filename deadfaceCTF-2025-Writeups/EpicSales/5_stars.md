# EpicSales – Highest Average Rating (SQL)

## Challenge

- **Location**: `/epicsales`
- **Prompt**: *EpicSales suspects DEADFACE might have been looking for their most popular products. Identify the product with the highest average rating in the `reviews` table.*
- **Flag format**: `deadface{flag text}`.

## Walkthrough

1. **Connect to MySQL**  
   ```bash
   mysql --ssl=0 -h env01.deadface.io -u epicsales -p'Slighted3-Charting-Valium' epicsales_db
   ```

2. **Inspect the schema**  
   ```sql
   SHOW TABLES;
   DESCRIBE reviews;
   ```
   Confirmed the ratings live in `reviews` and product names in `products`.

3. **Compute average ratings**  
   ```sql
   SELECT
       p.product_name,
       AVG(r.rating) AS avg_rating,
       COUNT(*) AS review_count
   FROM reviews r
   JOIN products p ON r.product_id = p.product_id
   GROUP BY r.product_id
   ORDER BY avg_rating DESC, review_count DESC
   LIMIT 5;
   ```

4. **Result**  
   The highest average rating belonged to **VortexAudio Focus** (≈ 3.24 average across 25 reviews).

## Flag

```
deadface{VortexAudio Focus}
```
