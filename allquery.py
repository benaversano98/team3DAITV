from createdb import *


def query1(connection):
    query1 = "SELECT year, COUNT(*) as numero_film FROM `movies` GROUP BY year;"
    result = read_query(connection, query1)
    # return result
    print(result)


def query2(connection):
    query2 = """
    SELECT genres.genre, COUNT(*) as numero_film 
    FROM `movies` JOIN `genres_movies` JOIN `genres` 
    ON movies.movie_id = genres_movies.movie_id AND genres_movies.genre_id = genres.genre_id
    GROUP BY genres.genre;
    """
    result = read_query(connection, query2)
    print(result)

def query3(connection):
    query = "SELECT movie_id FROM movies WHERE media_rating < 3;"
    id_movie = read_query(connection, query)
    

def query4(connection):
    fasciaeta = read_query(connection, "SELECT DISTINCT fasciaeta FROM users")
    sesso = read_query(connection, "SELECT DISTINCT gender FROM users")
    query = """
    SELECT users.fasciaeta, movies.title, movies.media_rating
    FROM movies JOIN ratings JOIN users
    ON movies.movie_id=ratings.movie_id AND ratings.user_id=users.user_id
    WHERE users.fasciaeta = %s
    GROUP BY movies.movie_id
    ORDER BY movies.media_rating DESC
    LIMIT 10;
    """
    result1 = readmany_query(connection, query, fasciaeta)
    print(result1)
    query = """
        SELECT users.gender, movies.title, movies.media_rating
        FROM movies JOIN ratings JOIN users
        ON movies.movie_id=ratings.movie_id AND ratings.user_id=users.user_id
        WHERE users.gender = %s
        GROUP BY movies.movie_id
        ORDER BY movies.media_rating DESC
        LIMIT 10;
        """
    result2 = readmany_query(connection, query, sesso)
    print(result2)

def query5(connection):
    fasciaeta = read_query(connection, "SELECT DISTINCT fasciaeta FROM users")
    query = """
       SELECT movies.title, movies.media_rating, users.gender
       FROM movies JOIN ratings JOIN users
       ON movies.movie_id=ratings.movie_id AND ratings.user_id=users.user_id
       WHERE users.gender = %s
       GROUP BY movies.movie_id
       ORDER BY movies.media_rating;
       """
    result1 = readmany_query(connection, query, fasciaeta)
    print(result1)


