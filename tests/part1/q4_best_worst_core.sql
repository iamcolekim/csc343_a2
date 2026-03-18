-- Focused test data for q4: zero-sales months and ties.
--
-- Key checks:
-- January 2024 -> Book highest 20, Toy lowest 5.
-- March 2024 -> Book and Toy tie at 10, so 4 rows for March.
-- Months with no sales -> both categories are both highest and lowest,
-- so 4 rows per such month.

SET SEARCH_PATH TO Recommender;

INSERT INTO Item VALUES
(1, 'Book', 'Novel', 10.0),
(2, 'Toy', 'Blocks', 5.0);

INSERT INTO Customer VALUES
(1, 'pat@example.com', 'Parker', 'Pat', 'Mx');

INSERT INTO Purchase VALUES
(201, 1, '2024-01-15 10:00:00', '1111', 'visa'),
(202, 1, '2024-03-03 10:00:00', '1111', 'visa');

INSERT INTO LineItem VALUES
(201, 1, 2),
(201, 2, 1),
(202, 1, 1),
(202, 2, 2);
