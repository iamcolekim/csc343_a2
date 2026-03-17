-- Curators

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;
DROP TABLE IF EXISTS q3 CASCADE;

CREATE TABLE q3 (
    CID INT NOT NULL,
    category_name TEXT NOT NULL,
    PRIMARY KEY(CID, category_name)
);

-- You may find it convenient to do this for each of the views
-- that define your intermediate steps. (But give them better names!)
DROP VIEW IF EXISTS CategoryItems CASCADE;

-- Define views for your intermediate steps here:
-- All items in each category
CREATE VIEW CategoryItems AS
SELECT
    IID,
    category
FROM Item;

-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q3
SELECT
    c.CID,
    ci.category AS category_name
FROM Customer c
JOIN CategoryItems ci ON TRUE
GROUP BY c.CID, ci.category
HAVING NOT EXISTS (
    -- there exists an item in this category that the customer
    -- has not both purchased and reviewed with a non-NULL comment
    SELECT *
    FROM CategoryItems ci2
    WHERE ci2.category = ci.category
      AND NOT EXISTS (
          SELECT *
          FROM Purchase p
          JOIN LineItem li ON p.PID = li.PID
          JOIN Review r ON r.CID = p.CID AND r.IID = li.IID
          WHERE p.CID = c.CID
            AND li.IID = ci2.IID
            AND r.comment IS NOT NULL
      )
);