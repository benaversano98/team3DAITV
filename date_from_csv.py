import csv


def dati_movies(file_csv):
    with open(file_csv, encoding='latin1', newline='') as input:
        lettore = csv.reader(input, delimiter=';')
        next(lettore)
        lettore = list(lettore)
        lista_dati = []
        lista_generi = []
        for e in lettore:
            lista_dati.append([f.strip() for f in e])
    return lista_dati, lista_generi

def dati_users(file_csv):

        lista_utenti = []
        for e in lettore:
            lista_utenti.append(e)


