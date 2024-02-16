from createdb import *
import csv


def query1(connection):
    query1 = "SELECT year, COUNT(*) as numero_film FROM `movies` GROUP BY year;"
    result = read_query(connection, query1)
    return result


def query2(connection):
    query2 = """
    SELECT genres.genre, COUNT(*) as numero_film 
    FROM `movies` JOIN `genres_movies` JOIN `genres` 
    ON movies.movie_id = genres_movies.movie_id AND genres_movies.genre_id = genres.genre_id
    GROUP BY genres.genre;
    """
    result = read_query(connection, query2)
    return result


def query3(connection):
    query = "SELECT movie_id FROM movies WHERE media_rating < 3 AND media_rating > 0;"
    id_movie = read_query(connection, query)
    query = "SELECT movie_id, COUNT(ratings.user_id) FROM ratings WHERE movie_id=%s;"
    id_movie = readmany_query(connection, query, id_movie)
    dati = []
    for e in id_movie:
        if e[1] > 250:
            dati.append(e[0])
    return dati


def query4(connection):
    fasciaeta = read_query(connection, "SELECT DISTINCT fasciaeta FROM users")
    sesso = read_query(connection, "SELECT DISTINCT gender FROM users")
    dati = [(e[0],f[0]) for f in sesso for e in fasciaeta]
    query = """
    SELECT users.fasciaeta, users.gender, movies.title, ROUND(AVG(ratings.rating), 2) AS media
    FROM movies JOIN ratings JOIN users
    ON movies.movie_id=ratings.movie_id AND ratings.user_id=users.user_id
    WHERE users.fasciaeta = %s AND users.gender= %s 
    GROUP BY movies.movie_id
    HAVING COUNT(ratings.rating) > 10
    ORDER BY AVG(ratings.rating) DESC
    LIMIT 10;
    """
    result = readmany_query(connection, query, dati)
    return result



def query5(connection):
    fasciaeta = read_query(connection, "SELECT DISTINCT fasciaeta FROM users")
    query = """
    SELECT movies.title, ROUND(CAST(AVG(ratings.rating) AS FLOAT), 2) as media_rating, users.fasciaeta
    FROM movies 
    JOIN ratings 
    ON movies.movie_id=ratings.movie_id
    JOIN users 
    ON ratings.user_id=users.user_id
    WHERE users.fasciaeta = %s
    GROUP BY movies.movie_id
    HAVING COUNT(ratings.rating) > 10
    ORDER BY AVG(ratings.rating);
    """
    result = readmany_query(connection, query, fasciaeta)
    return result


def query6(connection):
    query = """
    SELECT city, COUNT(city)
    FROM users
    GROUP BY city
    ORDER BY COUNT(city) DESC
    LIMIT 20;
    """
    result = read_query(connection, query)
    return result

def query7(connection):
    query = """
    SELECT work, COUNT(work)
    FROM users
    GROUP BY work;
    """
    result = read_query(connection, query)
    return result

if __name__ == '__main__':
    connection = create_db_connection("localhost", "root", "", "streaming")
    # dati = query1(connection)
    # with open(r"dati_query\movies_anno.csv", "w", encoding='utf-8', newline='') as output:
    #     scrittore = csv.writer(output, delimiter=";")
    #     scrittore.writerow(["Anno", "Numero film"])
    #     for e in dati:
    #         scrittore.writerow([e for e in e])
    # dati = query2(connection)
    # with open(r"dati_query\movies_genere.csv", "w", encoding='utf-8', newline='') as output:
    #     scrittore = csv.writer(output, delimiter=";")
    #     scrittore.writerow(["Genere", "Numero film"])
    #     for e in dati:
    #         scrittore.writerow([e for e in e])
    # dati = query3(connection)
    # with open(r"dati_query\film_delete.csv", "w", encoding='utf-8', newline='') as output:
    #     scrittore = csv.writer(output, delimiter=";")
    #     scrittore.writerow(["Id_film"])
    #     for e in dati:
    #         scrittore.writerow([e])
    # dati = query4(connection)
    # with open(r"dati_query\film_preferiti_fasciaeta.csv", "w", encoding='utf-8', newline='') as output:
    #     scrittore = csv.writer(output, delimiter=";")
    #     scrittore.writerow(["Fascia età", "Genere", "Titolo film", "Media voti"])
    #     for e in dati:
    #         scrittore.writerow(e)
    # dati = query5(connection)
    # with open(r"dati_query\rating_film_fasciaeta.csv", "w", encoding='utf-8', newline='') as output:
    #     scrittore = csv.writer(output, delimiter=";")
    #     scrittore.writerow(["Titolo", "Media voti", "Fascia età"])
    #     for e in dati:
    #         scrittore.writerow(e)
    dati = query6(connection)
    with open(r"dati_query\abbonati_provincia.csv", "w", encoding='utf-8', newline='') as output:
        scrittore = csv.writer(output, delimiter=";")
        scrittore.writerow(["Provincia", "Numero abbonati"])
        for e in dati:
            scrittore.writerow(e)
    # dati = query7(connection)
    # with open(r"dati_query\abbonati_lavoro.csv", "w", encoding='utf-8', newline='') as output:
    #     scrittore = csv.writer(output, delimiter=";")
    #     scrittore.writerow(["Provincia", "Numero abbonati"])
    #     for e in dati:
    #         scrittore.writerow(e)
