"""
Part3 of csc343 A2: Tests for A2 code.
csc343, Winter 2026
University of Toronto

--------------------------------------------------------------------------------
This file is Copyright (c) 2026 Diane Horton and Marina Tawfik.
All forms of distribution, whether as given or with any changes, are
expressly prohibited.
--------------------------------------------------------------------------------
"""
import pytest
from a2 import *
from psycopg2 import sql
from psycopg2.extras import execute_values



from datetime import datetime




# TODO: Change the values of the following variables to connect to your
#  own database:

DB_NAME = "csc343h-username"
USER = "username"
PASSWORD = ""
# The following uses the relative paths to the schema file and the data file
# we have provided. For your own tests, you will want to make your own data
# files to use for testing.
SCHEMA_FILE = "../schema.ddl"
SAMPLE_DATA = "../data.sql"

def setup_schema_only(schema_path: str) -> None:
    """Reset the database by loading only the schema file."""
    connection, cursor = None, None
    try:
        connection = pg.connect(
            dbname=DB_NAME, user=USER, password=PASSWORD,
            options="-c search_path=recommender"
        )
        cursor = connection.cursor()
        with open(schema_path, "r") as schema_file:
            cursor.execute(schema_file.read())
        connection.commit()
    except Exception as ex:
        if connection:
            connection.rollback()
        raise Exception(f"Couldn't set up schema-only environment:\n{ex}")
    finally:
        if cursor and not cursor.closed:
            cursor.close()
        if connection and not connection.closed:
            connection.close()

def setup(schema_path: str, data_path: str) -> None:
    """Set up the testing environment by importing the schema file
    at <schema_path> and the file containing the data at <data_path>.

    <schema_path> and <data_path> are the relative/absolute paths to the files
    containing the schema and the data respectively.
    """
    connection, cursor, schema_file, data_file = None, None, None, None
    try:
        connection = pg.connect(
            dbname=DB_NAME, user=USER, password=PASSWORD,
            options="-c search_path=recommender"
        )
        cursor = connection.cursor()

        with open(schema_path, "r") as schema_file:
            cursor.execute(schema_file.read())

        with open(data_path, "r") as info_file:
            cursor.execute(info_file.read())

        connection.commit()
    except Exception as ex:
        connection.rollback()
        raise Exception(f"Couldn't set up environment for tests: \n{ex}")
    finally:
        if cursor and not cursor.closed:
            cursor.close()
        if connection and not connection.closed:
            connection.close()


def get_rows(table_name: str) -> Optional[set[tuple]]:
    """Return the contents of the table <table_name> under our recommender
    schema.
    """
    conn, cur = None, None
    try:
        conn = pg.connect(
            dbname=DB_NAME, user=USER, password=PASSWORD,
            options="-c search_path=recommender"
        )
        cur = conn.cursor()
        cur.execute(sql.SQL("SELECT * FROM {}").format(
            sql.Identifier(table_name.lower())))
        return set(elem for elem in cur.fetchall())
    except pg.Error as ex:
        conn.rollback()
        raise Exception(f"Couldn't retrieve data from table {table_name}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def insert_rows(table_name: str, rows: set[tuple]) -> bool:
    """Insert the tuples <rows> in table <table_name> under our recommender
    schema. Return False if an error occurs.
    """
    conn, cur = None, None
    try:
        conn = pg.connect(
            dbname=DB_NAME, user=USER, password=PASSWORD,
            options="-c search_path=recommender"
        )
        cur = conn.cursor()
        insert_query = sql.SQL("INSERT INTO {} VALUES %s").format(
            sql.Identifier(table_name.lower()))
        execute_values(cur, insert_query, list(rows))
    except pg.Error:
        conn.rollback()
        raise Exception(f"Couldn't populate table {table_name}")
    else:
        conn.commit()
        return True
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def test_repopulate_basic() -> None:
    """Test basic aspects of the A2 repopulate method.
    """
    a2 = Recommender()
    try:
        # The following function call will set up the testing environment by
        # loading a fresh copy of the schema and the sample data we have
        # provided into your database. You can create more sample data files
        # and call the same function to load them into your database.
        setup(SCHEMA_FILE, SAMPLE_DATA)

        connected = a2.connect(DB_NAME, USER, PASSWORD)

        # The following is an assert statement. It checks that the value for
        # connected is True. The message after the comma will be printed if
        # that is not the case (that is, if connected is False).
        # Use the same notation throughout your testing.
        assert connected, f"[Connect] Expected True | Got {connected}."

        # TODO: Add more test cases here, or better yet, make more testing
        #   functions, each testing a different aspect of the code.

        # ------------------------ Testing Repopulate ------------------------ #

        # Note: These results assume that the instance has already been
        # populated with the provided data e.g., using the setup function.

        # TEST: The EliteMember table is empty
        repopulated = a2.repopulate()
        assert repopulated, f"[Repopulate] Expected True | Got {repopulated}."

        # You can manually check the contents of your instance to make sure
        # it was updated correctly, or you can use the provided function
        # get_rows.
        actual_popular_items = get_rows("PopularItem")
        # Using sets because the order doesn't matter.
        expected_popular_items = {(2, None), (3, None), (5, None)}
        assert actual_popular_items == expected_popular_items, \
            "[Repopulate] PopularItem content is incorrect."

        actual_elite_ratings = get_rows("EliteRating")
        expected_elite_ratings = set()
        assert actual_elite_ratings == expected_elite_ratings, \
            "[Repopulate] EliteRating content is incorrect."

        # TEST: The EliteMember table includes one member.
        # For your other tests, you can include the contents of the EliteMember
        # as part of your data file. Alternatively, you can use the provided
        # function insert_rows.
        insert_rows("EliteMember", {(1518,)})

        repopulated = a2.repopulate()
        assert repopulated, f"[Repopulate] Expected True | Got {repopulated}."

        # You can manually check the contents of your instance to make sure
        # it was updated correctly, or you can use the provided function
        # get_rows.
        actual_popular_items = get_rows("PopularItem")
        # Using sets because the order doesn't matter.
        expected_popular_items = {(2, None), (3, None), (5, None)}
        assert actual_popular_items == expected_popular_items, \
            "[Repopulate] PopularItem content is incorrect."
        actual_elite_ratings = get_rows("EliteRating")
        expected_elite_ratings = set()
        assert actual_elite_ratings == expected_elite_ratings, \
            "[Repopulate] EliteRating content is incorrect."
    finally:
        a2.disconnect()


def test_recommend_generic_basic() -> None:
    """Test basic aspects of the A2 recommend_generic method.
    """
    a2 = Recommender()
    try:
        # The following function call will set up the testing environment by
        # loading a fresh copy of the schema and the sample data we have
        # provided into your database. You can create more sample data files
        # and call the same function to load them into your database.
        setup(SCHEMA_FILE, SAMPLE_DATA)

        connected = a2.connect(DB_NAME, USER, PASSWORD)

        # The following is an assert statement. It checks that the value for
        # connected is True. The message after the comma will be printed if
        # that is not the case (that is, if connected is False).
        # Use the same notation throughout your testing.
        assert connected, f"[Connect] Expected True | Got {connected}."

        # TODO: Add more test cases here, or better yet, make more testing
        #   functions, each testing a different aspect of the code.

        # --------------------- Testing Recommend Generic -------------------- #

        # Note: These results assume that the instance has already been
        # populated with the provided data e.g., using the setup function.

        # Note: You can call repopulate first. I manually populate the
        # PopularItem table so that you can test this method even if you are not
        # done implementing repopulate.
        # For your other tests, you can include the contents of the PopularItem
        # table as part of your data file. Alternatively, you can use the
        # provided function insert_rows like I do here.

        # TEST: The PopularItem table is empty
        actual_recommended = a2.recommend_generic(3)
        expected_recommended = []
        assert actual_recommended == expected_recommended, \
            f"[Recommend Generic] "\
            f"Expected {expected_recommended} | Got {actual_recommended}."

        # TEST: The PopularItem table is not empty
        insert_rows("PopularItem", {(2, 3.5), (4, 3.5), (3, 2.5)})

        actual_recommended = a2.recommend_generic(2)
        expected_recommended = [2, 4]
        assert actual_recommended == expected_recommended, \
            f"[Recommend Generic] " \
            f"Expected {expected_recommended} | Got {actual_recommended}."
    finally:
        a2.disconnect()


def test_recommend_basic() -> None:
    """Test basic aspects of the A2 recommend method.
    """
    a2 = Recommender()
    try:
        # The following function call will set up the testing environment by
        # loading a fresh copy of the schema and the sample data we have
        # provided into your database. You can create more sample data files
        # and call the same function to load them into your database.
        setup(SCHEMA_FILE, SAMPLE_DATA)

        connected = a2.connect(DB_NAME, USER, PASSWORD)

        # The following is an assert statement. It checks that the value for
        # connected is True. The message after the comma will be printed if
        # that is not the case (that is, if connected is False).
        # Use the same notation throughout your testing.
        assert connected, f"[Connect] Expected True | Got {connected}."

        # TODO: Add more test cases here, or better yet, make more testing
        #   functions, each testing a different aspect of the code.

        # ------------------------ Testing Recommend ------------------------- #

        # Note: These results assume that the instance has already been
        # populated with the provided data e.g., using the setup function.

        # Note: You can call repopulate first. I manually populate the
        # EliteMember, PopularItem and EliteRating tables so that you can test
        # this method even if you are not done implementing repopulate.
        # For your other tests, you can include the contents of these
        # tables as part of your data file. Alternatively, you can use the
        # provided function insert_rows like I do here.

        # TEST: No elite members
        insert_rows("PopularItem", {(2, 3.5), (4, 3.5), (3, 2.5)})

        actual_recommended = a2.recommend(1599, 2)
        expected_recommended = [2, 4]
        assert actual_recommended == expected_recommended, \
            f"[Recommend] "\
            f"Expected {expected_recommended} | Got {actual_recommended}."

    finally:
        a2.disconnect()


def test_repopulate_ties_null_avg_and_popular_only_elite_ratings() -> None:
    """Repopulate should:
    - keep top and second-highest sold items per category (with ties),
    - assign NULL avg_rating to unrated popular items,
    - clear old snapshot rows,
    - and include only elite reviews of popular items in EliteRating.
    """
    a2 = Recommender()
    try:
        setup_schema_only(SCHEMA_FILE)
        connected = a2.connect(DB_NAME, USER, PASSWORD)
        assert connected, f"[Connect] Expected True Got {connected}."

        # Customers
        insert_rows("Customer", {
            (10, "c10@x.ca", "Ten", "Customer", "Customer"),
            (20, "c20@x.ca", "Twenty", "Customer", "Customer"),
            (30, "c30@x.ca", "Thirty", "Customer", "Customer"),
        })

        # Items
        insert_rows("Item", {
            (1, "Books", "Book 1", 10.0),
            (2, "Books", "Book 2", 10.0),
            (3, "Books", "Book 3", 10.0),
            (4, "Games", "Game 1", 20.0),
            (5, "Games", "Game 2", 20.0),
            (6, "Games", "Game 3", 20.0),
        })

        # Purchases
        insert_rows("Purchase", {
            (101, 10, datetime(2025, 1, 1, 10, 0, 0), "1111", "visa"),
            (102, 20, datetime(2025, 1, 1, 11, 0, 0), "2222", "visa"),
            (103, 30, datetime(2025, 1, 1, 12, 0, 0), "3333", "visa"),
            (104, 10, datetime(2025, 1, 2, 10, 0, 0), "1111", "visa"),
            (105, 20, datetime(2025, 1, 2, 11, 0, 0), "2222", "visa"),
            (106, 30, datetime(2025, 1, 2, 12, 0, 0), "3333", "visa"),
        })

        # Sales:
        # Books: item1=10, item2=8, item3=8  -> popular: 1,2,3
        # Games: item4=7,  item5=5, item6=1  -> popular: 4,5
        insert_rows("LineItem", {
            (101, 1, 10),
            (102, 2, 8),
            (103, 3, 8),
            (104, 4, 7),
            (105, 5, 5),
            (106, 6, 1),
        })

        # Reviews:
        # item1 avg = (5 + 1) / 2 = 3.0
        # item2 avg = 3.0
        # item3 avg = NULL (no reviews)
        # item4 avg = (4 + 2) / 2 = 3.0
        # item5 avg = 5.0
        # item6 is non-popular but reviewed by elite customer 10 -> should NOT be in EliteRating
        insert_rows("Review", {
            (10, 1, 5, "great"),
            (20, 1, 1, "bad"),
            (10, 2, 3, "ok"),
            (10, 4, 4, "nice"),
            (20, 4, 2, "meh"),
            (20, 5, 5, "excellent"),
            (10, 6, 2, "not popular"),
        })

        # Elite members
        insert_rows("EliteMember", {(10,), (30,)})

        # Preload stale snapshot rows that should be cleared by repopulate().
        insert_rows("PopularItem", {(6, 1.0)})
        insert_rows("EliteRating", {(10, 6, 2)})

        repopulated = a2.repopulate()
        assert repopulated, f"[Repopulate] Expected True Got {repopulated}."

        actual_popular = get_rows("PopularItem")
        expected_popular = {
            (1, 3.0),
            (2, 3.0),
            (3, None),
            (4, 3.0),
            (5, 5.0),
        }
        assert actual_popular == expected_popular, \
            f"[Repopulate] PopularItem incorrect.\nExpected {expected_popular}\nGot {actual_popular}"

        actual_elite = get_rows("EliteRating")
        expected_elite = {
            (10, 1, 5),
            (10, 2, 3),
            (10, 4, 4),
        }
        assert actual_elite == expected_elite, \
            f"[Repopulate] EliteRating incorrect.\nExpected {expected_elite}\nGot {actual_elite}"

    finally:
        a2.disconnect()

def test_recommend_generic_tie_at_cutoff_and_ignore_nulls() -> None:
    """recommend_generic should:
    - choose highest avg_rating first,
    - break ties by lower IID,
    - and ignore rows with NULL avg_rating in the current implementation.
    """
    a2 = Recommender()
    try:
        setup_schema_only(SCHEMA_FILE)
        connected = a2.connect(DB_NAME, USER, PASSWORD)
        assert connected, f"[Connect] Expected True Got {connected}."

        insert_rows("Item", {
            (1, "Cat", "I1", 1.0),
            (2, "Cat", "I2", 1.0),
            (3, "Cat", "I3", 1.0),
            (5, "Cat", "I5", 1.0),
            (7, "Cat", "I7", 1.0),
            (9, "Cat", "I9", 1.0),
        })

        insert_rows("PopularItem", {
            (5, None),
            (2, 4.5),
            (7, 4.5),
            (3, 4.5),
            (1, 3.0),
            (9, None),
        })

        actual_top2 = a2.recommend_generic(2)
        expected_top2 = [2, 3]
        assert actual_top2 == expected_top2, \
            f"[Recommend Generic] Expected {expected_top2} Got {actual_top2}."

        actual_all_rated = a2.recommend_generic(10)
        expected_all_rated = [2, 3, 7, 1]
        assert actual_all_rated == expected_all_rated, \
            f"[Recommend Generic] Expected {expected_all_rated} Got {actual_all_rated}."

    finally:
        a2.disconnect()

def test_recommend_generic_all_null_returns_empty() -> None:
    """If all popular items have NULL avg_rating, current implementation
    should return an empty list.
    """
    a2 = Recommender()
    try:
        setup_schema_only(SCHEMA_FILE)
        connected = a2.connect(DB_NAME, USER, PASSWORD)
        assert connected, f"[Connect] Expected True Got {connected}."

        insert_rows("Item", {
            (2, "Cat", "I2", 1.0),
            (5, "Cat", "I5", 1.0),
        })

        insert_rows("PopularItem", {
            (2, None),
            (5, None),
        })

        actual = a2.recommend_generic(5)
        expected = []
        assert actual == expected, \
            f"[Recommend Generic] Expected {expected} Got {actual}."

    finally:
        a2.disconnect()



def test_recommend_tie_in_analogous_rater_uses_lower_cid() -> None:
    """If two elite members tie on average rating difference,
    recommend() should use the lower elite CID.
    """
    a2 = Recommender()
    try:
        setup_schema_only(SCHEMA_FILE)
        connected = a2.connect(DB_NAME, USER, PASSWORD)
        assert connected, f"[Connect] Expected True Got {connected}."

        insert_rows("Customer", {
            (1, "cust1@x.ca", "One", "Cust", "Customer"),
            (2, "elite2@x.ca", "Two", "Elite", "Customer"),
            (3, "elite3@x.ca", "Three", "Elite", "Customer"),
        })

        insert_rows("Item", {
            (10, "Pop", "Pop10", 1.0),
            (11, "Pop", "Pop11", 1.0),
            (20, "Rec", "Rec20", 1.0),
            (21, "Rec", "Rec21", 1.0),
            (30, "Rec", "Rec30", 1.0),
        })

        # Customer's ratings on popular items
        insert_rows("Review", {
            (1, 10, 4, "cust"),
            (1, 11, 4, "cust"),

            # Elite 2: diffs are |4-5|=1 and |4-3|=1 => avg 1
            (2, 10, 5, "e2"),
            (2, 11, 3, "e2"),

            # Elite 3: diffs are |4-3|=1 and |4-5|=1 => avg 1
            (3, 10, 3, "e3"),
            (3, 11, 5, "e3"),

            # Additional recommendation candidates
            (2, 20, 5, "e2-high"),
            (2, 21, 5, "e2-high"),
            (3, 30, 5, "e3-high"),
        })

        insert_rows("EliteMember", {(2,), (3,)})

        # Snapshot tables inserted manually so this test does not depend on repopulate().
        insert_rows("PopularItem", {
            (10, 4.0),
            (11, 4.0),
        })
        insert_rows("EliteRating", {
            (2, 10, 5),
            (2, 11, 3),
            (3, 10, 3),
            (3, 11, 5),
        })

        # Customer 1 has bought the overlap items 10 and 11,
        # so they cannot be recommended.
        insert_rows("Purchase", {
            (101, 1, datetime(2025, 1, 1, 10, 0, 0), "1111", "visa"),
        })
        insert_rows("LineItem", {
            (101, 10, 1),
            (101, 11, 1),
        })

        actual = a2.recommend(1, 2)
        expected = [20, 21]
        assert actual == expected, \
            f"[Recommend] Expected {expected} Got {actual}."

    finally:
        a2.disconnect()



def test_recommend_no_overlap_falls_back_to_generic() -> None:
    """If cust has no popular-item ratings in common with any elite member,
    recommend() should fall back to recommend_generic().
    """
    a2 = Recommender()
    try:
        setup_schema_only(SCHEMA_FILE)
        connected = a2.connect(DB_NAME, USER, PASSWORD)
        assert connected, f"[Connect] Expected True Got {connected}."

        insert_rows("Customer", {
            (1, "cust1@x.ca", "One", "Cust", "Customer"),
            (2, "elite2@x.ca", "Two", "Elite", "Customer"),
        })

        insert_rows("Item", {
            (10, "Pop", "Pop10", 1.0),
            (11, "Pop", "Pop11", 1.0),
            (99, "Other", "Other99", 1.0),
        })

        insert_rows("Review", {
            (2, 10, 5, "elite"),
            (2, 11, 3, "elite"),
            (1, 99, 4, "cust-only"),
        })

        insert_rows("EliteMember", {(2,)})
        insert_rows("PopularItem", {
            (10, 4.5),
            (11, 4.0),
        })
        insert_rows("EliteRating", {
            (2, 10, 5),
            (2, 11, 3),
        })

        actual = a2.recommend(1, 2)
        expected = [10, 11]
        assert actual == expected, \
            f"[Recommend] Expected {expected} Got {actual}."

    finally:
        a2.disconnect()


def test_recommend_all_elite_items_already_bought_falls_back_to_generic() -> None:
    """If the analogous elite member has no unseen rated items left,
    recommend() should fall back to recommend_generic().
    """
    a2 = Recommender()
    try:
        setup_schema_only(SCHEMA_FILE)
        connected = a2.connect(DB_NAME, USER, PASSWORD)
        assert connected, f"[Connect] Expected True Got {connected}."

        insert_rows("Customer", {
            (1, "cust1@x.ca", "One", "Cust", "Customer"),
            (2, "elite2@x.ca", "Two", "Elite", "Customer"),
        })

        insert_rows("Item", {
            (10, "Pop", "Pop10", 1.0),
            (11, "Pop", "Pop11", 1.0),
            (20, "Rec", "Rec20", 1.0),
        })

        # Reviews for overlap + elite recommendations.
        # Customer 1 and elite 2 overlap on popular items 10 and 11,
        # so elite 2 is a valid analogous rater.
        # Elite 2 also rated item 20, but customer 1 will already have bought it.
        insert_rows("Review", {
            (1, 10, 4, "cust"),
            (1, 11, 4, "cust"),
            (2, 10, 5, "elite"),
            (2, 11, 3, "elite"),
            (2, 20, 5, "elite-rec"),
        })

        insert_rows("EliteMember", {(2,)})

        # Snapshot tables are inserted manually so this test does not depend on
        # repopulate().
        insert_rows("PopularItem", {
            (10, 4.5),
            (11, 4.0),
        })
        insert_rows("EliteRating", {
            (2, 10, 5),
            (2, 11, 3),
        })

        # Customer 1 has already bought every item elite 2 has rated:
        # 10, 11, and 20.
        insert_rows("Purchase", {
            (101, 1, datetime(2025, 1, 1, 10, 0, 0), "1111", "visa"),
        })
        insert_rows("LineItem", {
            (101, 10, 1),
            (101, 11, 1),
            (101, 20, 1),
        })

        actual = a2.recommend(1, 2)

        # Since elite 2 has no unseen rated items left for customer 1,
        # recommend() should fall back to recommend_generic(2),
        # which should recommend popular items [10, 11].
        expected = [10, 11]
        assert actual == expected, \
            f"[Recommend] Expected {expected} Got {actual}."

    finally:
        a2.disconnect()


def test_recommend_returns_fewer_than_k_when_elite_has_few_unseen_items() -> None:
    """recommend() should return fewer than k items if the analogous elite
    has only a small number of unseen rated items.
    """
    a2 = Recommender()
    try:
        setup_schema_only(SCHEMA_FILE)
        connected = a2.connect(DB_NAME, USER, PASSWORD)
        assert connected, f"[Connect] Expected True Got {connected}."

        insert_rows("Customer", {
            (1, "cust1@x.ca", "One", "Cust", "Customer"),
            (2, "elite2@x.ca", "Two", "Elite", "Customer"),
        })

        insert_rows("Item", {
            (10, "Pop", "Pop10", 1.0),
            (11, "Pop", "Pop11", 1.0),
            (20, "Rec", "Rec20", 1.0),
            (21, "Rec", "Rec21", 1.0),
        })

        # Customer 1 and elite 2 overlap on popular items 10 and 11,
        # so elite 2 is the analogous rater.
        # Elite 2 has also rated items 20 and 21.
        insert_rows("Review", {
            (1, 10, 4, "cust"),
            (1, 11, 4, "cust"),
            (2, 10, 5, "elite"),
            (2, 11, 3, "elite"),
            (2, 20, 5, "elite-rec"),
            (2, 21, 4, "elite-rec"),
        })

        insert_rows("EliteMember", {(2,)})
        insert_rows("PopularItem", {
            (10, 4.5),
            (11, 4.0),
        })
        insert_rows("EliteRating", {
            (2, 10, 5),
            (2, 11, 3),
        })

        # Customer 1 has already bought 10, 11, and 21.
        # That leaves only item 20 as an unseen elite-rated item.
        insert_rows("Purchase", {
            (101, 1, datetime(2025, 1, 1, 10, 0, 0), "1111", "visa"),
        })
        insert_rows("LineItem", {
            (101, 10, 1),
            (101, 11, 1),
            (101, 21, 1),
        })

        actual = a2.recommend(1, 3)
        expected = [20]
        assert actual == expected, \
            f"[Recommend] Expected {expected} Got {actual}."

    finally:
        a2.disconnect()


def test_recommend_generic_ignores_nulls_and_breaks_ties_by_iid() -> None:
    """recommend_generic should ignore NULL avg_rating rows in the current
    implementation, and break rating ties by lower IID.
    """
    a2 = Recommender()
    try:
        setup_schema_only(SCHEMA_FILE)
        connected = a2.connect(DB_NAME, USER, PASSWORD)
        assert connected, f"[Connect] Expected True Got {connected}."

        insert_rows("Item", {
            (1, "Cat", "I1", 1.0),
            (2, "Cat", "I2", 1.0),
            (3, "Cat", "I3", 1.0),
            (5, "Cat", "I5", 1.0),
            (7, "Cat", "I7", 1.0),
            (9, "Cat", "I9", 1.0),
        })

        insert_rows("PopularItem", {
            (5, None),
            (2, 4.5),
            (7, 4.5),
            (3, 4.5),
            (1, 3.0),
            (9, None),
        })

        actual_top2 = a2.recommend_generic(2)
        expected_top2 = [2, 3]
        assert actual_top2 == expected_top2, \
            f"[Recommend Generic] Expected {expected_top2} Got {actual_top2}."

        actual_all_rated = a2.recommend_generic(10)
        expected_all_rated = [2, 3, 7, 1]
        assert actual_all_rated == expected_all_rated, \
            f"[Recommend Generic] Expected {expected_all_rated} Got {actual_all_rated}."

    finally:
        a2.disconnect()


def test_recommend_generic_all_null_returns_empty() -> None:
    """If all PopularItem rows have NULL avg_rating, recommend_generic
    should return [] in the current implementation.
    """
    a2 = Recommender()
    try:
        setup_schema_only(SCHEMA_FILE)
        connected = a2.connect(DB_NAME, USER, PASSWORD)
        assert connected, f"[Connect] Expected True Got {connected}."

        insert_rows("Item", {
            (2, "Cat", "I2", 1.0),
            (5, "Cat", "I5", 1.0),
            (9, "Cat", "I9", 1.0),
        })

        insert_rows("PopularItem", {
            (2, None),
            (5, None),
            (9, None),
        })

        actual = a2.recommend_generic(5)
        expected = []
        assert actual == expected, \
            f"[Recommend Generic] Expected {expected} Got {actual}."

    finally:
        a2.disconnect()


def test_recommend_generic_returns_fewer_than_k_when_few_rated_items() -> None:
    """If there are fewer rated popular items than k, recommend_generic
    should return just the rated ones.
    """
    a2 = Recommender()
    try:
        setup_schema_only(SCHEMA_FILE)
        connected = a2.connect(DB_NAME, USER, PASSWORD)
        assert connected, f"[Connect] Expected True Got {connected}."

        insert_rows("Item", {
            (1, "Cat", "I1", 1.0),
            (2, "Cat", "I2", 1.0),
            (3, "Cat", "I3", 1.0),
            (4, "Cat", "I4", 1.0),
        })

        insert_rows("PopularItem", {
            (1, 4.0),
            (2, None),
            (3, 2.5),
            (4, None),
        })

        actual = a2.recommend_generic(10)
        expected = [1, 3]
        assert actual == expected, \
            f"[Recommend Generic] Expected {expected} Got {actual}."

    finally:
        a2.disconnect()

def test_recommend_uses_best_analogous_rater_and_orders_unseen_items() -> None:
    """recommend() should:
    - choose the elite member with the lowest average rating difference,
    - recommend from all items that elite rated,
    - exclude items the customer already bought,
    - and break ties in recommendation rating by lower IID.
    """
    a2 = Recommender()
    try:
        setup_schema_only(SCHEMA_FILE)
        connected = a2.connect(DB_NAME, USER, PASSWORD)
        assert connected, f"[Connect] Expected True Got {connected}."

        insert_rows("Customer", {
            (1, "cust1@x.ca", "One", "Cust", "Customer"),
            (2, "elite2@x.ca", "Two", "Elite", "Customer"),
            (3, "elite3@x.ca", "Three", "Elite", "Customer"),
        })

        insert_rows("Item", {
            (10, "Pop", "Pop10", 1.0),
            (11, "Pop", "Pop11", 1.0),
            (20, "Rec", "Rec20", 1.0),
            (21, "Rec", "Rec21", 1.0),
            (22, "Rec", "Rec22", 1.0),
            (30, "Rec", "Rec30", 1.0),
        })

        # Customer ratings on popular items
        # Elite 2 is the better match:
        #   cust vs elite2 diffs: |4-4|=0, |5-4|=1 => avg 0.5
        #   cust vs elite3 diffs: |4-1|=3, |5-5|=0 => avg 1.5
        insert_rows("Review", {
            (1, 10, 4, "cust"),
            (1, 11, 5, "cust"),

            (2, 10, 4, "e2"),
            (2, 11, 4, "e2"),
            (3, 10, 1, "e3"),
            (3, 11, 5, "e3"),

            # Elite 2's recommendation candidates
            (2, 20, 5, "e2-rec"),
            (2, 21, 5, "e2-rec"),
            (2, 22, 4, "e2-rec"),

            # Elite 3's recommendation candidate (should not be used)
            (3, 30, 5, "e3-rec"),
        })

        insert_rows("EliteMember", {(2,), (3,)})

        # Manually populate snapshot tables so this test does not depend on repopulate().
        insert_rows("PopularItem", {
            (10, 4.0),
            (11, 4.5),
        })
        insert_rows("EliteRating", {
            (2, 10, 4),
            (2, 11, 4),
            (3, 10, 1),
            (3, 11, 5),
        })

        # Customer has already bought the overlap items (10, 11)
        # and one of elite 2's candidate items (22),
        # so the unseen top-rated items left should be 20 and 21.
        insert_rows("Purchase", {
            (101, 1, datetime(2025, 1, 1, 10, 0, 0), "1111", "visa"),
        })
        insert_rows("LineItem", {
            (101, 10, 1),
            (101, 11, 1),
            (101, 22, 1),
        })

        actual = a2.recommend(1, 2)
        expected = [20, 21]
        assert actual == expected, \
            f"[Recommend] Expected {expected} Got {actual}."

    finally:
        a2.disconnect()


if __name__ == "__main__":
    pytest.main()
