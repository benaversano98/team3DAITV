from createtable import *
from insertdate import *
from allquery import *

connect_server = create_server_connection("localhost", "root", "")
elimina_database(connect_server,'streaming')
crea_database(connect_server,'streaming')
connection = create_db_connection("localhost", "root", "", "streaming")
crea_tabelle(connection)
inserisci_dati(connection)
# query5(connection)
print("Arrivederci")
