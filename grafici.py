import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"dati_query\movies_anno.csv", delimiter=';')
sns.displot(df["Numero film"], kde=True)
plt.xlabel('Anno')
plt.ylabel('Numero di film')
plt.show()


df = pd.read_csv(r"dati_query\movies_genere.csv", delimiter=';')
film_genere = df.groupby("Genere")["Numero film"].sum().reset_index()
sns.barplot(data=film_genere, x="Genere", y="Numero film", color="orange")
plt.xlabel('Genere')
plt.ylabel('Numero di film')
plt.xticks(rotation=45)
plt.show()
