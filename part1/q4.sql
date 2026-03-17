-- Best and Worst Categories

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;
DROP TABLE IF EXISTS q4 CASCADE;

CREATE TABLE q4 (
    month TEXT NOT NULL,
    highest_category TEXT NOT NULL,
    highest_sales_val FLOAT NOT NULL,
    lowest_category TEXT NOT NULL,
    lowest_sales_val FLOAT NOT NULL
);

-- You may find it convenient to do this for each of the views
-- that define your intermediate steps. (But give them better names!)
DROP VIEW IF EXISTS Months CASCADE;
DROP VIEW IF EXISTS Categories CASCADE;
DROP VIEW IF EXISTS MonthCategory CASCADE;
DROP VIEW IF EXISTS Sales CASCADE;
DROP VIEW IF EXISTS FullSales CASCADE;
DROP VIEW IF EXISTS MaxSales CASCADE;
DROP VIEW IF EXISTS MinSales CASCADE;

-- Define views for your intermediate steps here:
-- The 12 months
CREATE VIEW Months AS
SELECT to_char(generate_series(1, 12), 'FM09') AS month;

-- All categories
CREATE VIEW Categories AS
SELECT DISTINCT category
FROM Item;

-- All month-category pairs
CREATE VIEW MonthCategory AS
SELECT
    m.month,
    c.category
FROM Months m
CROSS JOIN Categories c;

-- Total sales for each month-category pair
CREATE VIEW Sales AS
SELECT
    to_char(p.checkout_time, 'MM') AS month,
    i.category,
    SUM(li.quantity * i.price) AS sales_val
FROM Purchase p
JOIN LineItem li ON p.PID = li.PID
JOIN Item i ON li.IID = i.IID
WHERE EXTRACT(YEAR FROM p.checkout_time) = 2024
GROUP BY to_char(p.checkout_time, 'MM'), i.category;

-- Combine month-category pairs with sales, filling in 0 for missing pairs
CREATE VIEW FullSales AS
SELECT
    mc.month,
    mc.category,
    COALESCE(s.sales_val, 0) AS sales_val
FROM MonthCategory mc
LEFT JOIN Sales s
    ON mc.month = s.month AND mc.category = s.category;

-- Find max and min sales for each month
CREATE VIEW MaxSales AS
SELECT
    month,
    MAX(sales_val) AS max_val
FROM FullSales
GROUP BY month;

CREATE VIEW MinSales AS
SELECT
    month,
    MIN(sales_val) AS min_val
FROM FullSales
GROUP BY month;

-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q4
SELECT
    f.month,
    f.category AS highest_category,
    f.sales_val AS highest_sales_val,
    f2.category AS lowest_category,
    f2.sales_val AS lowest_sales_val
FROM FullSales f
JOIN MaxSales mx
    ON f.month = mx.month AND f.sales_val = mx.max_val
JOIN FullSales f2
    ON f.month = f2.month
JOIN MinSales mn
    ON f2.month = mn.month AND f2.sales_val = mn.min_val;

