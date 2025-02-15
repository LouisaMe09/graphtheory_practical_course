import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# CSV-Datei einlesen
input_csv = 'clustering_results.csv'
data = pd.read_csv(input_csv)

# Anpassung der x-Achsen-Beschriftung basierend auf Task
def create_task_label(row):
    # if row['task'] == 'wp03':
    #     return f"{row['task']} ({row['algorithm']})"
    # elif row['task'] == 'wp04b':
    #     return f"{row['task']} (Depth {row['depth']})"
    # else:  # Für wp02 und wp04a nur den Task
    #     return row['task']
    return f"alg:{row['algorithm']}-d:{row['depth']}-it{row['iteration']}"

# Neue Spalte für die angepasste x-Achsen-Beschriftung
data['task_label'] = data.apply(create_task_label, axis=1)

# Farbpalette für Iterationen
palette = sns.color_palette("husl", len(data['iteration'].unique()))

# Plot vorbereiten
plt.figure(figsize=(14, 8))

# Balkendiagramm erstellen
sns.barplot(
    x='task_label',
    y='time',
    hue='iteration',
    data=data,
    palette=palette,
    edgecolor='black'
)

# Achsentitel und Legende
plt.xlabel("Task (Algorithm / Depth)", fontsize=12)
plt.ylabel("Time (seconds)", fontsize=12)
plt.title("Clustering Time by Task, Algorithm, Iteration, and Depth", fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.legend(title='Iteration', fontsize=10, title_fontsize=12)

# Layout anpassen und anzeigen
plt.tight_layout()
plt.show()
