-- Customer Appreciation Week

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;


-- You may find it convenient to do this for each of the views
-- that define your intermediate steps. (But give them better names!)
-- DROP VIEW IF EXISTS IntermediateStep CASCADE;

-- Define views for your intermediate steps here:
-- CREATE VIEW IntermediateStep AS .

-- For each customer who placed one or more purchases yesterday,
-- keep only their first purchase yesterday (by checkout_time).

-- ################
-- My query below:
-- ################

DROP VIEW IF EXISTS FirstOrdersYesterday CASCADE;

-- Define views for your intermediate steps here:
-- For each customer who placed one or more purchases yesterday,
-- keep only their first purchase yesterday (by checkout_time).
CREATE VIEW FirstOrdersYesterday AS
SELECT DISTINCT ON (p.CID)
       p.PID,
       p.CID
FROM Purchase p
WHERE p.checkout_time >= CURRENT_DATE - INTERVAL '1 day'
  AND p.checkout_time < CURRENT_DATE
ORDER BY p.CID, p.checkout_time ASC, p.PID ASC;

-- 1) Insert the free mug item.
INSERT INTO Item (IID, category, description, price)
SELECT COALESCE(MAX(IID), 0) + 1,
       'Housewares',
       'Company logo mug',
       0
FROM Item;

-- 2) Add one free mug to the first purchase yesterday for each customer.
INSERT INTO LineItem (PID, IID, quantity)
SELECT f.PID,
       i.IID,
       1
FROM FirstOrdersYesterday f
JOIN Item i
  ON i.description = 'Company logo mug';
