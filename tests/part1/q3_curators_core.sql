-- Focused test data for q3: curator logic.
--
-- Expected q3 rows:
-- 1 | Book
-- 1 | Toy
-- 3 | Game

SET SEARCH_PATH TO Recommender;

INSERT INTO Item VALUES
(1, 'Book', 'Novel A', 10.0),
(2, 'Book', 'Novel B', 12.0),
(3, 'Toy', 'Puzzle', 15.0),
(4, 'Game', 'Board Game', 30.0);

INSERT INTO Customer VALUES
(1, 'ann@example.com', 'Archer', 'Ann', 'Ms'),
(2, 'ben@example.com', 'Bishop', 'Ben', 'Mr'),
(3, 'cam@example.com', 'Carter', 'Cam', 'Mx'),
(4, 'dia@example.com', 'Dover', 'Dia', 'Ms');

INSERT INTO Purchase VALUES
(101, 1, '2024-01-10 10:00:00', '1111', 'visa'),
(102, 2, '2024-01-11 10:00:00', '2222', 'visa'),
(103, 3, '2024-01-12 10:00:00', '3333', 'visa'),
(104, 4, '2024-01-13 10:00:00', '4444', 'visa');

INSERT INTO LineItem VALUES
(101, 1, 1),
(101, 2, 1),
(101, 3, 1),
(102, 1, 1),
(102, 2, 1),
(103, 4, 1),
(104, 1, 1);

INSERT INTO Review VALUES
(1, 1, 5, 'loved it'),
(1, 2, 4, 'nice'),
(1, 3, 5, ''),
(2, 1, 5, 'good'),
(2, 2, 3, NULL),
(3, 4, 4, 'fun'),
(4, 1, 4, 'ok'),
(4, 2, 4, 'also ok');
