from sqlite3 import Error
import mysql
import mysql.connector
from flask import Flask, jsonify, render_template, request
import datetime

app = Flask(__name__)

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
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result

def ex_query( query):
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        #print("Query successful")
    except Error as err:
        print(query, f"Error: '{err}'")


@app.route("/", methods=['GET', 'POST'])
def homepage():
    image_carousel = {356: "https://take2.lancastersu.co.uk/wp-content/uploads/2020/09/forrest-gump.jpg",
                      1214: "https://wallpapercave.com/wp/wp10328274.jpg",
                      3623: "https://prod-ripcut-delivery.disney-plus.net/v1/variant/star"
                            "/B3CDE4F04A841BD5CA81AF1B4637C233EF58A72EB3B85C2781B381F68EE1DAC1/scale?width=1200"
                            "&aspectRatio=1.78&format=jpeg"}
    q_carousel = "SELECT * FROM movies WHERE movie_id IN {}".format(tuple(image_carousel.keys()))
    carousel = execute_query(q_carousel)
    for elem in carousel:
        elem.update({'src': image_carousel[elem["movie_id"]]})

    


    return render_template("Home_daitv.html", carousel=carousel)


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


@app.route("/loan",  methods=['GET', 'POST'])
def loan():
    query = """
    SELECT loan.user_id, users.name, GROUP_CONCAT(books.title SEPARATOR ", ") AS title, 
    GROUP_CONCAT(books.id SEPARATOR ", ") AS book_id, GROUP_CONCAT(loan.date_of_loan SEPARATOR ", ") AS date_loan
    FROM loan JOIN users JOIN books
    ON loan.book_id = books.id AND loan.user_id=users.id
    GROUP BY users.name ORDER BY loan.user_id;
    """
    list_loan = execute_query(query)
    elimina = []
    result = []
    flagaggiunge = False
    flagelimina = False

    if request.method == 'POST':
        codice_elimina = [request.form.get('Eliminabook'), request.form.get('Eliminautente')]
        codice_aggiunge = [request.form.get("Aggiungibook"), request.form.get("Aggiungiutente"), request.form.get("Aggiungidata")]
        codice_ricerca = request.form.get('Search')

        if codice_ricerca:
            q_ricerca = f"""
            SELECT loan.user_id, users.name, GROUP_CONCAT(books.title SEPARATOR ", ") AS title, 
            GROUP_CONCAT(books.id SEPARATOR ", ") AS book_id, GROUP_CONCAT(loan.date_of_loan SEPARATOR ", ") AS date_loan
            FROM loan JOIN users JOIN books
            ON loan.book_id = books.id AND loan.user_id=users.id
            WHERE loan.user_id LIKE '%{codice_ricerca}%' OR users.name LIKE '%{codice_ricerca}%'
            GROUP BY users.name ORDER BY loan.user_id;
            """
            list_loan = execute_query(q_ricerca)

        if codice_elimina[0] is not None and codice_elimina[1] is not None:
            flagelimina = True
            elimina = execute_query(f"SELECT * FROM loan WHERE book_id = {codice_elimina[0]} and user_id = {codice_elimina[1]}")
            execute_query(f"DELETE FROM loan WHERE book_id = {codice_elimina[0]} and user_id = {codice_elimina[1]}")
            list_loan = execute_query(query)


        if codice_aggiunge[0] is not None and codice_aggiunge[1] is not None and codice_aggiunge[2] is not None :
            flagaggiunge = True
            try:
                execute_query(f"INSERT INTO loan (book_id, user_id, date_of_loan) VALUES ('{codice_aggiunge[0]}', '{codice_aggiunge[1]}', '{codice_aggiunge[2]}')")
            except:
                result = ["ERRORE"]
            list_loan = execute_query(query)


    return render_template("prestiti.html", list_loan=list_loan, len=len, elimina=elimina, result=result, flagaggiunge=flagaggiunge, flagelimina=flagelimina)


if __name__ == '__main__':
    app.run(debug=True)
