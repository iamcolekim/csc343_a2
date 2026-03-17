-- Focused test data for q5: top 5 distinct totals with ties.
--
-- Expected q5 rows:
-- 2024 -> A One 10
-- 2024 -> B Two 9
-- 2024 -> C Three 9
-- 2024 -> D Four 8
-- 2024 -> E Five 7
-- 2024 -> F Six 6
-- 2024 -> G Seven 6
-- 2025 -> A One 3
-- 2025 -> H Eight 1

SET SEARCH_PATH TO Recommender;

INSERT INTO Item VALUES
(1, 'Book', 'Volume 1', 10.0),
(2, 'Toy', 'Cube', 5.0);

INSERT INTO Customer VALUES
(1, 'a@example.com', 'One', 'A', 'Mx'),
(2, 'b@example.com', 'Two', 'B', 'Mx'),
(3, 'c@example.com', 'Three', 'C', 'Mx'),
(4, 'd@example.com', 'Four', 'D', 'Mx'),
(5, 'e@example.com', 'Five', 'E', 'Mx'),
(6, 'f@example.com', 'Six', 'F', 'Mx'),
(7, 'g@example.com', 'Seven', 'G', 'Mx'),
(8, 'h@example.com', 'Eight', 'H', 'Mx');

INSERT INTO Purchase VALUES
(301, 1, '2024-01-01 09:00:00', '1111', 'visa'),
(302, 2, '2024-01-02 09:00:00', '2222', 'visa'),
(303, 3, '2024-01-03 09:00:00', '3333', 'visa'),
(304, 4, '2024-01-04 09:00:00', '4444', 'visa'),
(305, 5, '2024-01-05 09:00:00', '5555', 'visa'),
(306, 6, '2024-01-06 09:00:00', '6666', 'visa'),
(307, 7, '2024-01-07 09:00:00', '7777', 'visa'),
(308, 8, '2024-01-08 09:00:00', '8888', 'visa'),
(309, 1, '2025-01-01 09:00:00', '1111', 'visa'),
(310, 8, '2025-01-02 09:00:00', '8888', 'visa');

INSERT INTO LineItem VALUES
(301, 1, 10),
(302, 1, 9),
(303, 1, 9),
(304, 1, 8),
(305, 1, 7),
(306, 1, 6),
(307, 1, 6),
(308, 1, 5),
(309, 2, 3),
(310, 2, 1);
