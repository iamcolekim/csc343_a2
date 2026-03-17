-- Hyperconsumers

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;
DROP TABLE IF EXISTS q5 CASCADE;

CREATE TABLE q5 (
    year VARCHAR(4) NOT NULL,
    name VARCHAR(65) NOT NULL,
    email VARCHAR(300) NOT NULL,
    items INTEGER NOT NULL
);

-- You may find it convenient to do this for each of the views
-- that define your intermediate steps. (But give them better names!)
DROP VIEW IF EXISTS CustomerYearTotals CASCADE;

-- Define views for your intermediate steps here:
-- Total quantity bought by each customer in each year
CREATE VIEW CustomerYearTotals AS
SELECT
    to_char(p.checkout_time, 'YYYY') AS year,
    c.CID,
    c.first_name || ' ' || c.last_name AS name,
    c.email,
    SUM(li.quantity) AS items
FROM Customer c
JOIN Purchase p ON c.CID = p.CID
JOIN LineItem li ON p.PID = li.PID
GROUP BY
    to_char(p.checkout_time, 'YYYY'),
    c.CID,
    c.first_name,
    c.last_name,
    c.email;

-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q5
SELECT
    cyt.year AS year,
    cyt.name AS name,
    cyt.email AS email,
    cyt.items AS items
FROM CustomerYearTotals cyt
WHERE (
    SELECT COUNT(DISTINCT cyt2.items)
    FROM CustomerYearTotals cyt2
    WHERE cyt2.year = cyt.year
      AND cyt2.items > cyt.items
) < 5;
