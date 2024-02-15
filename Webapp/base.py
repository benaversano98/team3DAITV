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
    'database': 'Libreria_Gruppo3'}


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
    flag = True
    list_books = api_books()
    modificato = False
    rimosso = False
    aggiunto = False

    if request.method == 'POST':

        "modifica utenti"
        mod_id_utente = request.form.get('mod_id_utente')
        new_nome_utente = request.form.get('new_nome_utente')
        new_nascita_anno_utente = request.form.get('new_nascita_anno_utente')
        new_nascita_mese_utente = request.form.get('new_nascita_mese_utente')
        new_nascita_giorno_utente = request.form.get('new_nascita_giorno_utente')
        if (mod_id_utente and isinstance(int(mod_id_utente), int)) and (
                new_nome_utente and new_nascita_anno_utente and new_nascita_mese_utente and new_nascita_giorno_utente):
            isValidDate = True  # check if date is valid
            try:
                datetime.datetime(int(new_nascita_anno_utente), int(new_nascita_mese_utente),
                                  int(new_nascita_giorno_utente))
            except ValueError:
                isValidDate = False

            if isinstance(new_nome_utente, str) and (
                    1900 < int(new_nascita_anno_utente) < datetime.datetime.now().year) and isValidDate:
                ex_query(
                    f"UPDATE users SET name='{new_nome_utente}',date_of_birth='{new_nascita_anno_utente}-{new_nascita_mese_utente}-{new_nascita_giorno_utente}' WHERE id = {mod_id_utente}")
                modificato = True

        "rimuovi utente"
        del_id_utente = request.form.get('del_id_utente')
        if del_id_utente and isinstance(int(del_id_utente), int):
            ex_query(f"DELETE FROM users WHERE id = {del_id_utente}")
            rimosso = True

        "aggiungi utenti"
        nome_utente = request.form.get('nome_utente')
        nascita_anno_utente = request.form.get('nascita_anno_utente')
        nascita_mese_utente = request.form.get('nascita_mese_utente')
        nascita_giorno_utente = request.form.get('nascita_giorno_utente')

        if (nome_utente and nascita_anno_utente and nascita_mese_utente and nascita_giorno_utente):
            isValidDate = True  # check if date is valid
            try:
                datetime.datetime(int(nascita_anno_utente), int(nascita_mese_utente), int(nascita_giorno_utente))
            except ValueError:
                isValidDate = False

            if isinstance(nome_utente, str) and (
                    1900 < int(nascita_anno_utente) < datetime.datetime.now().year) and isValidDate:
                ex_query(
                    f"INSERT INTO `users`(`name`, `date_of_birth`) VALUES ('{nome_utente}','{nascita_anno_utente}-{nascita_mese_utente}-{nascita_giorno_utente}')")
                aggiunto = True
    codice = request.form.get('Search')
    if codice:
        list_books = execute_query(
            f"SELECT * FROM books WHERE title LIKE '%{codice}%' OR author LIKE '%{codice}%'")
    image, frase = "https://img00.deviantart.net/9088/i/2007/223/7/d/no_books_by_applejoan.jpg", "Non ci sono libri a questa ricerca."
    return render_template("home.html", image=image, frase=frase, list_books=list_books, len=len, flag=flag, modificato=modificato, aggiunto=aggiunto, rimosso=rimosso)


@app.route("/api/books")
def api_books():
    query_lg = f'SELECT * FROM books'
    list_books = execute_query(query_lg)
    return list_books


@app.route("/api/users")
def api_users():
    query_lg = 'SELECT * FROM users'
    list_users = execute_query(query_lg)
    return jsonify(list_users)


@app.route("/api/loan")
def api_loan():
    query_lg = 'SELECT * FROM loan'
    list_loan = execute_query(query_lg)
    return jsonify(list_loan)


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
