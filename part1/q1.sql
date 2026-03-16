-- Unrated products

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;
DROP TABLE IF exists q1 CASCADE;

CREATE TABLE q1(
    CID INTEGER,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT
);

-- Drop any views we create (safe if re-run).
DROP VIEW IF EXISTS UnratedItems CASCADE;
DROP VIEW IF EXISTS CustomerUnratedItems CASCADE;
DROP VIEW IF EXISTS QualifiedCustomers CASCADE;

-- 1) Items that have NO reviews at all.
CREATE VIEW UnratedItems AS
SELECT i.IID
FROM Item i
WHERE NOT EXISTS (
    SELECT 1
    FROM Review r
    WHERE r.IID = i.IID
);

-- 2) For each customer, which distinct unrated items have they purchased?
CREATE VIEW CustomerUnratedItems AS
SELECT DISTINCT p.CID, li.IID
FROM Purchase p
JOIN LineItem li
  ON li.PID = p.PID
JOIN UnratedItems u
  ON u.IID = li.IID;

-- 3) Customers who bought at least 3 different unrated items.
CREATE VIEW QualifiedCustomers AS
SELECT CID
FROM CustomerUnratedItems
GROUP BY CID
HAVING COUNT(DISTINCT IID) >= 3;

-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q1
SELECT c.CID,
       c.first_name,
       c.last_name,
       c.email
FROM Customer c
JOIN QualifiedCustomers q
  ON q.CID = c.CID;