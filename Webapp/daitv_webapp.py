from sqlite3 import Error
import mysql
import mysql.connector
from flask import Flask, jsonify, render_template, request, redirect, session
import datetime
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configura la connessione al database MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'streaming'}


def create_db_connection():
    return mysql.connector.connect(**db_config)


# Funzione per eseguire query SQL
def execute_query(query, params=None, dictionary=True):
    connection = create_db_connection()
    if dictionary:
        cursor = connection.cursor(dictionary=True)
    else:
        cursor = connection.cursor()
    if params is not None:
        if not isinstance(params, (tuple, list)):
            params = (params,)
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()

    return result

def ex_query(query):
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        # print("Query successful")
    except Error as err:
        print(query, f"Error: '{err}'")


login = False


@app.route("/", methods=['GET', 'POST'])
def homepage():
    ### CAROUSEL ###
    image_carousel = {356: "https://take2.lancastersu.co.uk/wp-content/uploads/2020/09/forrest-gump.jpg",
                      1214: "https://wallpapercave.com/wp/wp10328274.jpg",
                      3623: "https://prod-ripcut-delivery.disney-plus.net/v1/variant/star"
                            "/B3CDE4F04A841BD5CA81AF1B4637C233EF58A72EB3B85C2781B381F68EE1DAC1/scale?width=1200"
                            "&aspectRatio=1.78&format=jpeg"}
    q_carousel = "SELECT * FROM movies WHERE movie_id IN {}".format(tuple(image_carousel.keys()))
    carousel = execute_query(q_carousel)
    for elem in carousel:
        elem.update({'src': image_carousel[elem["movie_id"]]})

    rec_genre = execute_query("SELECT genre FROM `genres` ORDER BY RAND() LIMIT 1;")
    query_rec_genre = f"""
        SELECT title, alternative_title, year, media_rating FROM `movies` 
        JOIN genres_movies JOIN genres ON movies.movie_id = genres_movies.movie_id AND 
        genres_movies.genre_id = genres.genre_id 
        WHERE genres.genre = "{rec_genre[0]['genre']}" ORDER BY RAND() LIMIT 4 ;
        """
    rec_content = execute_query(query_rec_genre)

    rec_rating = execute_query("SELECT * FROM movies ORDER BY media_rating DESC LIMIT 4;")
    rec_random = execute_query("SELECT * FROM movies ORDER BY RAND() LIMIT 4;")

    ### LOG IN ###

    if request.method == 'POST':
        id_login = request.form.get('login_navbar')
        search_term = request.form.get('term')
        if id_login:
            q_tot_ratings_city = """
            SELECT movies.movie_id, movies.title, movies.alternative_title, movies.year, SUM(ratings.rating) as tot_rating
            FROM movies JOIN ratings JOIN users
            ON movies.movie_id = ratings.movie_id AND users.user_id = ratings.user_id
            WHERE users.city = (SELECT users.city FROM users WHERE users.user_id = %s)
            GROUP BY movies.movie_id ORDER BY tot_rating DESC LIMIT 4;
            """ % id_login
            top_ratings_city = execute_query(q_tot_ratings_city)

            q_tot_ratings_age = """
                SELECT movies.movie_id, movies.title, movies.alternative_title, movies.year, SUM(ratings.rating) as tot_rating
                FROM movies JOIN ratings JOIN users
                ON movies.movie_id = ratings.movie_id AND users.user_id = ratings.user_id
                WHERE users.fasciaeta = (SELECT users.fasciaeta FROM users WHERE users.user_id = %s)
                GROUP BY movies.movie_id ORDER BY tot_rating DESC LIMIT 4;
                """ % id_login
            global login
            login = True
            session["client_id"] = id_login

            top_ratings_age = execute_query(q_tot_ratings_age)
            return render_template("Home_login_daitv.html", carousel=carousel, rec_content=rec_content,
                                   rec_genre=rec_genre[0],
                                   rec_rating=rec_rating, rec_random=rec_random,
                                   top_ratings_city=top_ratings_city,
                                   top_ratings_age=top_ratings_age, id_login=id_login)
        elif search_term:
            return redirect("/search/%s" % search_term)

    return render_template("Home_daitv.html", carousel=carousel, rec_content=rec_content, rec_genre=rec_genre[0],
                           rec_rating=rec_rating, rec_random=rec_random)

@app.route("/search/<term>")
def search(term):
    genre_count = (term, 0)
    return redirect("/search/%s/%s" % genre_count)

@app.route("/search/<string:term>/<int:num>", methods=['GET', 'POST'])
def search_term_num(term, num):
    limit = 20
    offset = 0
    counter = num
    if request.method == 'POST':
        search_term = request.form.get('term')
        return redirect("/search/%s" % search_term)
    try:
        id_login = session.get("client_id")
        print(id_login)
    except:
        print("error")
    query_movies = f"SELECT * FROM movies WHERE title LIKE '%{term}%' OR alternative_title LIKE '%{term}%' ORDER BY title LIMIT {limit} OFFSET {offset + (counter*limit)}"
    list_search = execute_query(query_movies)
    return render_template("Search.html", list_search=list_search, login=login)

@app.route("/genres", methods=['GET', 'POST'])
def genres():
    list_genres = execute_query('SELECT genre FROM `genres`', dictionary=False)
    list_mov_genre = []
    for cod in list_genres:
        query_movie_genre = f"""SELECT title, alternative_title, year, media_rating FROM `movies`
                JOIN genres_movies JOIN genres ON movies.movie_id = genres_movies.movie_id AND
                genres_movies.genre_id = genres.genre_id
                WHERE genres.genre = "%s" ORDER BY RAND() LIMIT 4 ;""" % cod
        list_mov_genre.append(execute_query(query_movie_genre))

    if request.method == 'POST':
        search_term = request.form.get('term')
        return redirect("/search/%s" % search_term)

    return render_template("Genres.html", list_genres=list_genres, list_mov_genre=list_mov_genre)


@app.route("/genres/<genre>", methods=['GET', 'POST'])
def genres_genre(genre):
    genre_count = (genre, 0)

    return redirect("/genres/%s/%s" % genre_count)


@app.route("/genres/<string:genre>/<int:num>", methods=['GET', 'POST'])
def genres_genre_num(genre, num):
    limit = 20
    offset = 0
    counter = num

    if request.method == 'POST':
        search_term = request.form.get('term')
        return redirect("/search/%s" % search_term)

    query_genre_genre = f"""SELECT title, alternative_title, year, media_rating FROM `movies`
                        JOIN genres_movies JOIN genres ON movies.movie_id = genres_movies.movie_id AND
                        genres_movies.genre_id = genres.genre_id
                        WHERE genres.genre = "{genre}" ORDER BY movies.movie_id LIMIT {limit} OFFSET {offset + (counter*limit)};"""

    mov_genre_genre = execute_query(query_genre_genre)


    return render_template("Genres_genre.html", list_mov_genre=mov_genre_genre, genre=genre, num=int(num))


# @app.route("/catalogue", methods=['GET'])
# def catalogue():
#     genres = execute_query('SELECT * FROM genres')
#     catalogue = {}
#
#     for genre in genres:
#         genre_name = genre['genre']
#         movies_query = f"""
#             SELECT title, alternative_title, year, media_rating
#             FROM movies
#             JOIN genres_movies JOIN genres
#             ON movies.movie_id = genres_movies.movie_id AND genres_movies.genre_id = genres.genre_id
#             WHERE genres.genre = %s;
#         """
#         movies = execute_query(movies_query, (genre_name,))
#         catalogue[genre_name] = movies
#
#     show_all = request.args.get('show_all')
#     sort_az = request.args.get('sort_az')
#     high_rating = request.args.get('high_rating')
#
#     filtered_movies = filter_movies(catalogue, show_all, sort_az, high_rating)
#     return render_template("catalogue.html", catalogue=filtered_movies)
#
#
# def filter_movies(catalogue, show_all, sort_list, high_rating):
#     filtered_movies = catalogue.copy()
#
#     if not show_all:
#         for genre, movies in filtered_movies.items():
#             filtered_movies[genre] = [movie for movie in movies if movie['media_rating'] > 4]
#
#     if sort_list:
#         for genre, movies in filtered_movies.items():
#             filtered_movies[genre] = sorted(movies, key=lambda x: x['title'])
#
#     if high_rating:
#         for genre, movies in filtered_movies.items():
#             filtered_movies[genre] = [movie for movie in movies if movie['media_rating'] > float(high_rating)]
#
#     return filtered_movies


@app.route("/api/movies")
def api_movies():
    query_movies = """
    SELECT title, alternative_title, year, media_rating, GROUP_CONCAT(genres.genre SEPARATOR ", ") AS genres 
    FROM `movies` JOIN genres_movies JOIN genres ON movies.movie_id = genres_movies.movie_id AND 
    genres_movies.genre_id = genres.genre_id GROUP BY movies.movie_id;
    """
    list_movies = execute_query(query_movies)
    return list_movies


@app.route("/api/genres")
def api_genres():
    query_genres = 'SELECT * FROM `genres`'

    query_genres_genre = """
    SELECT title, alternative_title, year, media_rating, GROUP_CONCAT(genres.genre SEPARATOR ", ") AS genres FROM `movies` 
    JOIN genres_movies JOIN genres ON movies.movie_id = genres_movies.movie_id AND 
    genres_movies.genre_id = genres.genre_id 
    WHERE genres.genre LIKE "%comedy%" GROUP BY movies.movie_id;
    """

    list_genres = execute_query(query_genres)
    return jsonify(list_genres)


@app.route("/api/users")
def api_users():
    query_users = 'SELECT * FROM `users`'
    list_users = execute_query(query_users)
    return jsonify(list_users)


@app.route("/api/data/<string:provincia>")
def api_provincia(provincia):
    query_provincia = 'SELECT user_id, gender, age FROM users WHERE city = %s'
    list_provincia = execute_query(query_provincia, (provincia,))
    return list_provincia


@app.route("/api/data/<int:eta>")
def api_eta(eta):
    query_eta = 'SELECT user_id, gender, age FROM users WHERE age > %s'
    list_users = execute_query(query_eta, (eta,))
    return list_users


@app.route("/api/data/<provincia>/<eta>")
def api_provincia_eta(provincia, eta):
    query = 'SELECT user_id, gender, age FROM users WHERE city = %s AND age > %s'
    list_users = execute_query(query, (provincia, eta))
    return jsonify(list_users)


if __name__ == '__main__':
    app.run(debug=True)
