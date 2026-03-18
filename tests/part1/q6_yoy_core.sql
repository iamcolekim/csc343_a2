-- Focused test data for q6: operational-year gaps, zero averages, Infinity.
--
-- Operational years are 2022, 2023, 2024.
--
-- Item 1:
-- 2022 avg = 1, 2023 avg = 2, 2024 avg = 0
-- Changes: 2022->2023 = 100, 2023->2024 = -100
--
-- Item 2:
-- never purchased
-- Changes: 0, 0
--
-- Item 3:
-- 2022 avg = 0, 2023 avg = 0, 2024 avg = 1
-- Changes: 0, Infinity

SET SEARCH_PATH TO Recommender;

INSERT INTO Item VALUES
(1, 'Book', 'Series A', 10.0),
(2, 'Book', 'Series B', 12.0),
(3, 'Toy', 'Robot', 25.0);

INSERT INTO Customer VALUES
(1, 'yoy@example.com', 'Young', 'Yara', 'Ms');

INSERT INTO Purchase VALUES
(401, 1, '2022-01-10 10:00:00', '1111', 'visa'),
(402, 1, '2023-01-10 10:00:00', '1111', 'visa'),
(403, 1, '2024-01-10 10:00:00', '1111', 'visa');

INSERT INTO LineItem VALUES
(401, 1, 12),
(402, 1, 24),
(403, 3, 12);
