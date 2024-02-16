import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# df = pd.read_csv(r"dati_query\movies_anno.csv", delimiter=';')
# sns.displot(df["Numero film"], kde=True)
# plt.xlabel('Anno')
# plt.ylabel('Numero di film')
# plt.show()
#
#
# df = pd.read_csv(r"dati_query\movies_genere.csv", delimiter=';')
# film_genere = df.groupby("Genere")["Numero film"].sum().reset_index()
# sns.barplot(data=film_genere, x="Genere", y="Numero film", color="orange")
# plt.xlabel('Genere')
# plt.ylabel('Numero di film')
# plt.xticks(rotation=45)
# plt.show()

df = pd.read_csv(r"dati_query\film_preferiti_fasciaeta.csv", delimiter=';')
media_voti_per_fascia_eta_f = df[df['Genere'] == 'F'].groupby("Fascia età")["Media voti"].mean().reset_index()
media_voti_per_fascia_eta_m = df[df['Genere'] == 'M'].groupby("Fascia età")["Media voti"].mean().reset_index()
ordered_df_f = media_voti_per_fascia_eta_f.sort_values(by='Media voti')
ordered_df_m = media_voti_per_fascia_eta_m.sort_values(by='Media voti')
plt.figure(figsize=(10, 6))
plt.hlines(y=ordered_df_f['Fascia età'], xmin=0, xmax=ordered_df_f['Media voti'], color='pink', label='F')
plt.hlines(y=ordered_df_m['Fascia età'], xmin=0, xmax=ordered_df_m['Media voti'], color='lightblue', label='M')
plt.plot(ordered_df_f['Media voti'], ordered_df_f['Fascia età'], "D", color='pink')
plt.plot(ordered_df_m['Media voti'], ordered_df_m['Fascia età'], "D", color='lightblue')
plt.yticks(ordered_df_f['Fascia età'])
plt.xlabel('Media voti')
plt.ylabel('Fascia età')
plt.title('Lollipop Plot della media voti per fascia d\'età e genere')
plt.legend()
plt.tight_layout()
plt.show()
