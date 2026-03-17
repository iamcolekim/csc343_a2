-- Helpfulness


-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;
DROP TABLE IF EXISTS q2 CASCADE;

create table q2(
    CID INTEGER,
    name TEXT NOT NULL,
    helpfulness_category TEXT NOT NULL
);

-- You may find it convenient to do this for each of the views
-- that define your intermediate steps. (But give them better names!)
DROP VIEW IF EXISTS ReviewStats CASCADE;
DROP VIEW IF EXISTS CustomerStats CASCADE;

-- Define views for your intermediate steps here:
-- For each review count TRUE and FALSE, and total votes
CREATE VIEW ReviewStats AS
SELECT
    r.CID,
    r.IID,
    COUNT(h.*) AS total_votes,
    COUNT(*) FILTER (WHERE h.helpfulness = TRUE) AS true_votes,
    COUNT(*) FILTER (WHERE h.helpfulness = FALSE) AS false_votes
FROM Review r
LEFT JOIN Helpfulness h
    ON r.CID = h.reviewer
   AND r.IID = h.IID
GROUP BY r.CID, r.IID;

-- For each customer: total reviews + number of helpful reviews
CREATE VIEW CustomerStats AS
SELECT
    c.CID,
    c.first_name || ' ' || c.last_name AS name,
    COUNT(r.IID) AS total_reviews,
    COUNT(
        CASE
            WHEN rs.total_votes > 0 AND rs.true_votes > rs.false_votes THEN 1
            ELSE NULL
        END
    ) AS helpful_reviews
FROM Customer c
LEFT JOIN Review r
    ON c.CID = r.CID
LEFT JOIN ReviewStats rs
    ON r.CID = rs.CID AND r.IID = rs.IID
GROUP BY c.CID, c.first_name, c.last_name;

-- Your query that answers the question goes below the "insert into" line:
INSERT INTO q2
SELECT
    CID,
    name,
    CASE
        WHEN total_reviews = 0 THEN 'not helpful'
        WHEN helpful_reviews * 1.0 / total_reviews >= 0.8 THEN 'very helpful'
        WHEN helpful_reviews * 1.0 / total_reviews >= 0.5 THEN 'somewhat helpful'
        ELSE 'not helpful'
    END AS helpfulness_category
FROM CustomerStats;