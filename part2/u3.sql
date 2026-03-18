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

WITH inserted_mug AS (
    INSERT INTO Item (IID, category, description, price)
    SELECT COALESCE(MAX(IID), 0) + 1,
           'Housewares',
           'Company logo mug',
           0
    FROM Item
    WHERE NOT EXISTS (
        SELECT 1
        FROM Item
        WHERE description = 'Company logo mug'
    )
    RETURNING IID
),
mug AS (
    SELECT IID
    FROM inserted_mug
    UNION ALL
    SELECT IID
    FROM Item
    WHERE description = 'Company logo mug'
      AND NOT EXISTS (SELECT 1 FROM inserted_mug)
)
INSERT INTO LineItem (PID, IID, quantity)
SELECT f.PID,
       m.IID,
       1
FROM FirstOrdersYesterday f
CROSS JOIN mug m
WHERE NOT EXISTS (
    SELECT 1
    FROM LineItem li
    WHERE li.PID = f.PID
      AND li.IID = m.IID
);
