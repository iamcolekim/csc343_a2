-- Focused test data for q2: helpfulness categories.
--
-- Expected q2 rows:
-- 1 | Alice Able | very helpful
-- 2 | Bob Baker | somewhat helpful
-- 3 | Cara Cole | not helpful
-- 4 | Dan Drew | not helpful
-- 5 | Evan Elm | not helpful

SET SEARCH_PATH TO Recommender;

INSERT INTO Item VALUES
(1, 'Book', 'Book 1', 10.0),
(2, 'Book', 'Book 2', 12.0),
(3, 'Toy', 'Toy 1', 20.0);

INSERT INTO Customer VALUES
(1, 'alice@example.com', 'Able', 'Alice', 'Ms'),
(2, 'bob@example.com', 'Baker', 'Bob', 'Mr'),
(3, 'cara@example.com', 'Cole', 'Cara', 'Ms'),
(4, 'dan@example.com', 'Drew', 'Dan', 'Mr'),
(5, 'evan@example.com', 'Elm', 'Evan', 'Mr');

INSERT INTO Review VALUES
(1, 1, 5, 'great'),
(2, 1, 4, 'good'),
(2, 2, 4, 'solid'),
(3, 2, 3, 'ok'),
(5, 3, 2, NULL);

INSERT INTO Helpfulness VALUES
(1, 1, 2, TRUE),
(1, 1, 3, TRUE),
(1, 1, 4, TRUE),
(1, 1, 5, TRUE),
(2, 1, 1, TRUE),
(2, 1, 3, TRUE),
(2, 1, 4, FALSE),
(2, 2, 1, TRUE),
(2, 2, 3, FALSE),
(5, 3, 1, FALSE),
(5, 3, 2, FALSE);
