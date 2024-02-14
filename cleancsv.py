import csv
import re
from lingua import LanguageDetectorBuilder

def correct_title(string):
    # Regex per trovare gli articoli a fine titolo di un film
    regex = r", [ADEGILT][andehilors']{1,2}$"
    regex = re.compile(regex)
    # Presenza di una O come articolo al posto di Il nel film "Il Convento"
    if 'O)' in string:
        string = string.replace("O", "Il")
    if regex.search(string.strip()):
        obj = regex.findall(string.strip())
        for a in obj:
            if a != ", L'":
                match = regex.search(string.strip())
                titolo_senza_articolo = string[:match.start()]  # Parte del titolo prima dell'articolo
                string = f"{a[2:]} {titolo_senza_articolo}".strip()
            else:
                match = regex.search(string.strip())
                titolo_senza_articolo = string[:match.start()]
                string = f"{a[2:]}{titolo_senza_articolo}".strip()
    # Ulteriore pulizia della stringa
    string = string.replace("³", " 3")
    return string.strip()


# EXTRA (Vecchio approccio)
def diff_title(e):
    list_title = []
    if "(" in e:
        lista = e.split('(')
        if len(lista) == 2:
            lista[1] = lista[1].replace(")", "")
            return lista[0], lista[1]
        else:
            lista[1] = lista[1].replace(")", "")
            lista[2] = lista[2].replace(")", "")
            lista[0] = lista[0] + "/" + lista[1]
            lista[1] = lista[2]
            return lista[0], lista[1]
    else:
        lista = [e, ""]
        return lista[0], lista[1]

def dati_puliti():
    encoding_errors = []
    regex_encoding = r"^[a-zA-Z0-9À-ÿ_ !¡#$%&*()-/|\+=¿?.,:;']+$"
    revisione_titoli = []
    detector = LanguageDetectorBuilder.from_all_languages_with_latin_script().build()
    id_titoli_contrari = ["58", "771", "989"]
    file_csv = r"csv\movies.csv"
    with open(file_csv, encoding='latin1', newline='') as input:
        lettore = csv.reader(input, delimiter=';')
        intestazione = next(lettore)[:3]
        lettore = list(lettore)
        lista_dati = []
        genres = {}
        id_genres = 1
        movie_genres = []

        for e in lettore:
            if e[0] in id_titoli_contrari:
                nome = e[1].strip(" )").split(" (")
                e[1] = f"{nome[1]} ({nome[0]})"
            e[1], new = diff_title(e[1])
            e.insert(2, new)
            e[1] = correct_title(e[1])
            if e[2] != '':
                e[2] = correct_title(e[2])
            if bool(re.fullmatch(regex_encoding, e[1])) is False:
                encoding_errors.append(e)
                # Lista per revisione manuale
            if "(" in e[1]:
                text1 = e[1].split("(")[0].strip()
                if detector.detect_language_of(text1).name != "ENGLISH":
                    revisione_titoli.append(e)

            if len(encoding_errors) > 0:
                print('Ci sono encoding errors:\n', encoding_errors)
            lista_dati.append([f.strip() for f in e[:4]])
            genres_tit = e[4].split(',')
            for g in genres_tit:
                g = g.strip()
                if g not in genres.keys():
                    genres[g] = id_genres
                    id_genres += 1
                movie_genres.append([e[0], str(genres[g])])
            # Divisione della stringa dei generi in più elementi per creare una lista di generi
        genres = list(genres.items())
        genres = [(genres[i][1], genres[i][0]) for i in range(len(genres))]
        
    return intestazione, lista_dati, genres, movie_genres

if __name__ == '__main__':
    intestazione, lista_dati, genres, movie_genres = dati_puliti()
    intestazione.insert(2, "Alternative Title")
    with open(r"csv\movies_pulito.csv", "w", encoding='latin1', newline='') as output:
        scrittore = csv.writer(output, delimiter=";")
        scrittore.writerow(intestazione)
        for e in lista_dati:
            scrittore.writerow(e)
    with open(r"csv\genres.csv", "w", encoding='latin1', newline='') as output:
        scrittore = csv.writer(output, delimiter=";")
        scrittore.writerow(["Genre_Id", "Genres"])
        for e in genres:
            scrittore.writerow(list(e))