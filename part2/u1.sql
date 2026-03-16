-- SALE!SALE!SALE!

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;

-- You may find it convenient to do this for each of the views
-- that define your intermediate steps. (But give them better names!)
DROP VIEW IF EXISTS ItemsSold10Plus CASCADE;

-- Define views for your intermediate steps here:
-- Items that have sold a total of at least 10 units (across all purchases).
CREATE VIEW ItemsSold10Plus AS
SELECT li.IID
FROM LineItem li
GROUP BY li.IID
HAVING SUM(li.quantity) >= 10;

-- Apply discounts to qualifying items, based on current price:
-- 10–50 inclusive => 20% off
-- >50–100 inclusive => 30% off
-- >100 => 50% off
-- <10 => no discount
UPDATE Item i
SET price = CASE
    WHEN i.price >= 10 AND i.price <= 50 THEN i.price * 0.80
    WHEN i.price > 50  AND i.price <= 100 THEN i.price * 0.70
    WHEN i.price > 100 THEN i.price * 0.50
    ELSE i.price
END
WHERE i.IID IN (SELECT IID FROM ItemsSold10Plus);
