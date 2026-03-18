--Year-over-year sales

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;
DROP TABLE IF EXISTS q6 CASCADE;

CREATE TABLE q6 (
    IID INT NOT NULL,
    year1 INT NOT NULL,
    year1_avg FLOAT NOT NULL,
    year2 INT NOT NULL,
    year2_avg FLOAT NOT NULL,
    yoy_change FLOAT NOT NULL
);

-- You may find it convenient to do this for each of the views
-- that define your intermediate steps. (But give them better names!)
DROP VIEW IF EXISTS YearBounds CASCADE;
DROP VIEW IF EXISTS OperationalYears CASCADE;
DROP VIEW IF EXISTS YearPairs CASCADE;
DROP VIEW IF EXISTS Months CASCADE;
DROP VIEW IF EXISTS ItemYearMonth CASCADE;
DROP VIEW IF EXISTS MonthlySales CASCADE;
DROP VIEW IF EXISTS FullMonthlySales CASCADE;
DROP VIEW IF EXISTS YearAverages CASCADE;

-- Define views for your intermediate steps here:
-- Earliest and latest purchase year
CREATE VIEW YearBounds AS
SELECT
    MIN(EXTRACT(YEAR FROM checkout_time)::INT) AS min_year,
    MAX(EXTRACT(YEAR FROM checkout_time)::INT) AS max_year
FROM Purchase;

-- All operational years
CREATE VIEW OperationalYears AS
SELECT
    generate_series(min_year, max_year) AS year
FROM YearBounds;

-- All consecutive pairs of operational years
CREATE VIEW YearPairs AS
SELECT
    y1.year AS year1,
    y2.year AS year2
FROM OperationalYears y1
JOIN OperationalYears y2
    ON y2.year = y1.year + 1;

-- The 12 months
CREATE VIEW Months AS
SELECT
    generate_series(1, 12) AS month;

-- Every item, operational year, and month combination
CREATE VIEW ItemYearMonth AS
SELECT
    i.IID,
    y.year,
    m.month
FROM Item i
CROSS JOIN OperationalYears y
CROSS JOIN Months m;

-- Monthly unit sales for each item
CREATE VIEW MonthlySales AS
SELECT
    li.IID,
    EXTRACT(YEAR FROM p.checkout_time)::INT AS year,
    EXTRACT(MONTH FROM p.checkout_time)::INT AS month,
    SUM(li.quantity) AS monthly_units
FROM Purchase p
JOIN LineItem li
    ON p.PID = li.PID
GROUP BY
    li.IID,
    EXTRACT(YEAR FROM p.checkout_time)::INT,
    EXTRACT(MONTH FROM p.checkout_time)::INT;

-- Fill missing months with 0 sales
CREATE VIEW FullMonthlySales AS
SELECT
    iym.IID,
    iym.year,
    iym.month,
    COALESCE(ms.monthly_units, 0) AS monthly_units
FROM ItemYearMonth iym
LEFT JOIN MonthlySales ms
    ON iym.IID = ms.IID
   AND iym.year = ms.year
   AND iym.month = ms.month;

-- Average monthly unit sales for each item in each year
CREATE VIEW YearAverages AS
SELECT
    IID,
    year,
    AVG(monthly_units) AS year_avg
FROM FullMonthlySales
GROUP BY IID, year;

-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q6
SELECT
    ya1.IID AS IID,
    yp.year1 AS year1,
    ya1.year_avg AS year1_avg,
    yp.year2 AS year2,
    ya2.year_avg AS year2_avg,
    CASE
        WHEN ya1.year_avg = 0 AND ya2.year_avg = 0 THEN 0
        WHEN ya1.year_avg = 0 THEN 'Infinity'::FLOAT
        ELSE ((ya2.year_avg - ya1.year_avg) / ya1.year_avg) * 100
    END AS yoy_change
FROM YearPairs yp
JOIN YearAverages ya1
    ON yp.year1 = ya1.year
JOIN YearAverages ya2
    ON yp.year2 = ya2.year
   AND ya1.IID = ya2.IID;