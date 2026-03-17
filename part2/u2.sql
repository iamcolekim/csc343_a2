-- Fraud Prevention

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Recommender;


-- You may find it convenient to do this for each of the views
-- that define your intermediate steps. (But give them better names!)
DROP VIEW IF EXISTS ExcessPurchases CASCADE;
DROP VIEW IF EXISTS RecentPurchases CASCADE;

-- Define views for your intermediate steps here:
-- Purchases made within the last 24 hours
CREATE VIEW RecentPurchases AS
SELECT
    PID,
    card_pan,
    checkout_time
FROM Purchase
WHERE checkout_time >= NOW() - INTERVAL '24 hours';

-- Purchases made after the fifth recent purchase on the same card.
CREATE VIEW ExcessPurchases AS
SELECT rp1.PID
FROM RecentPurchases rp1
JOIN RecentPurchases rp2
    ON rp1.card_pan = rp2.card_pan
   AND (
       rp2.checkout_time < rp1.checkout_time
       OR (
           rp2.checkout_time = rp1.checkout_time
           AND rp2.PID <= rp1.PID
       )
   )
GROUP BY rp1.PID
HAVING COUNT(*) > 5;

DELETE FROM LineItem
WHERE PID IN (
    SELECT PID
    FROM ExcessPurchases
);

DELETE FROM Purchase
WHERE PID IN (
    SELECT PID
    FROM ExcessPurchases
);
