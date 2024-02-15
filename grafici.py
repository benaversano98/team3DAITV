import pandas as pd
import matplotlib.pyplot as plt


# df = pd.read_csv(r'dati_query\movies_anno.csv', delimiter=';')
# anni = df['Anno']
# numero_film = df['Numero film']
# plt.bar(anni, numero_film, color='blue', edgecolor='white')
# plt.title('Distribuzione dei film per anno')
# plt.xlabel('Anno')
# plt.ylabel('Numero di film')
# plt.show()


df = pd.read_csv(r'dati_query\movies_genere.csv', delimiter=';')
genere = df['Genere']
numero_film = df['Numero film']

# Creazione del grafico a torta
plt.figure(figsize=(15, 15))
patches, texts, _ = plt.pie(numero_film, autopct='%1.1f%%', pctdistance=1.2, startangle=90, textprops={'fontsize': 15, 'color': 'black'})

# Aggiunge la legenda al lato destro del grafico a torta
plt.legend(patches, genere, loc='center left', bbox_to_anchor=(1, 0.5))

# Aggiunge un titolo al grafico
plt.title('Grafico a Torta')

# Mostra il grafico
plt.show()

