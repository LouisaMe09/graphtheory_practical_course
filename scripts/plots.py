
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from matplotlib.patches import Patch

# # CSV-Datei einlesen
# input_csv = 'measurements/clustering_results.csv'
# data = pd.read_csv(input_csv)

# # Anpassung der x-Achsen-Beschriftung basierend auf Task
# def create_task_label(row):
#     return f"alg:{row['algorithm']}-d:{row['depth']}-it{row['iteration']}"

# # Neue Spalte für die angepasste x-Achsen-Beschriftung
# data['task_label'] = data.apply(create_task_label, axis=1)

# # Daten nach 'time' sortieren und die 10 kleinsten Einträge auswählen
# data = data.nsmallest(10, 'time')

# # Farbpalette für Iterationen
# palette = sns.color_palette("husl", len(data['iteration'].unique()))

# # Balkenstile basierend auf Depth festlegen
# def get_hatch(depth):
#     return '' if depth == 0 else '//'

# data['hatch'] = data['depth'].apply(get_hatch)

# # Plot vorbereiten
# plt.figure(figsize=(14, 8))

# # Balkendiagramm erstellen
# bars = sns.barplot(
#     x='task_label',
#     y='time',
#     hue='iteration',
#     data=data,
#     palette=palette,
#     edgecolor='black'
# )

# # Hatching (Streifen) basierend auf Depth anwenden
# for bar, (_, row) in zip(bars.patches, data.iterrows()):
#     bar.set_hatch(row['hatch'])

# # Legende für Depth ergänzen
# handles = [
#     Patch(facecolor='white', edgecolor='black', hatch='', label='Depth = 0'),
#     Patch(facecolor='white', edgecolor='black', hatch='//', label='Depth = 1')
# ]
# plt.legend(handles=handles, title='Depth', loc='upper right', fontsize=10, title_fontsize=12)

# # Achsentitel und andere Anpassungen
# plt.xlabel("Task (Algorithm / Depth)", fontsize=12)
# plt.ylabel("Time (seconds)", fontsize=12)
# plt.title("Clustering Time by Task, Algorithm, Iteration, and Depth (Top 10)", fontsize=14)
# plt.xticks(rotation=45, ha='right', fontsize=10)

# # Layout anpassen und anzeigen
# plt.tight_layout()
# plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

# CSV-Datei einlesen
input_csv = 'measurements/clustering_results.csv'
data = pd.read_csv(input_csv)

# Daten filtern: Nur die gewünschten Algorithmen behalten
data['algorithm'] = data['algorithm'].apply(eval)

# Daten filtern: Nur die Zeilen, bei denen 'algorithm' die exakte Kombination ['vertex_count', 'weisfeiler_lehman'] enthält
filtered_data = data[data['algorithm'].apply(lambda x: x == ['vertex_count', 'weisfeiler_lehman'])]


# Anpassung der x-Achsen-Beschriftung basierend auf Task
def create_task_label(row):
    return f"alg:{row['algorithm']}-d:{row['depth']}-it{row['iteration']}"

# Neue Spalte für die angepasste x-Achsen-Beschriftung
filtered_data['task_label'] = filtered_data.apply(create_task_label, axis=1)

# Farbpalette für Iterationen
palette = sns.color_palette("husl", len(filtered_data['iteration'].unique()))

# Balkenstile basierend auf Depth festlegen
def get_hatch(depth):
    if depth == 0:
        return ''  # Keine Streifen
    elif depth == 1:
        return '//'  # Breite Streifen
    elif depth == 2:
        return 'xx'  # Enge Streifen

filtered_data['hatch'] = filtered_data['depth'].apply(get_hatch)

# Plot vorbereiten
plt.figure(figsize=(14, 8))

# Balkendiagramm erstellen
bars = sns.barplot(
    x='task_label',
    y='time',
    hue='iteration',
    data=filtered_data,
    palette=palette,
    edgecolor='black'
)

# Hatching (Streifen) basierend auf Depth anwenden
for bar, (_, row) in zip(bars.patches, filtered_data.iterrows()):
    bar.set_hatch(row['hatch'])

# Legende für Depth ergänzen
handles = [
    Patch(facecolor='white', edgecolor='black', hatch='', label='Depth = 0'),
    Patch(facecolor='white', edgecolor='black', hatch='//', label='Depth = 1'),
    Patch(facecolor='white', edgecolor='black', hatch='xx', label='Depth = 2')
]
plt.legend(handles=handles, title='Depth', loc='upper right', fontsize=10, title_fontsize=12)

# Achsentitel und andere Anpassungen
plt.xlabel("Task (Algorithm / Depth)", fontsize=12)
plt.ylabel("Time (seconds)", fontsize=12)
plt.title("Clustering Time by Task, Algorithm, Iteration, and Depth (Filtered)", fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=10)

# Layout anpassen und anzeigen
print(filtered_data.head())
plt.tight_layout()
plt.show()

