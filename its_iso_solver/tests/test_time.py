import pytest
import pandas as pd
import os
import time
import importlib
from synutility.SynIO.data_type import load_from_pickle
import sys


def execute(args, data):
    task = args['task']

    task_module = importlib.import_module('tasks.' + task)

    # Measure the time for clustering
    start_time = time.time()

    module = task_module.IsomorphismSolver(data=data, args=args)

    clustered_data = module.its_clustering().get_clustered_data()

    end_time = time.time()

    return clustered_data, (end_time - start_time)

def test_clustering_time():
    # CSV-Datei vorbereiten
    output_csv = 'clustering_results.csv'
    columns = ['task', 'algorithm', 'iteration', 'depth', 'time', 'clusters']
    if not os.path.exists(output_csv):
        pd.DataFrame(columns=columns).to_csv(output_csv, index=False)

    file_path = os.path.join('data', 'ITS_graphs.pkl.gz')
    sys.path.append("its_iso_solver")

    commands = {
        "task": ["wp02", "wp03", "wp04a", "wp04b"],
        "algorithm": ["vertex_count", "edge_count", "vertex_degrees","algebraic_connectivity", "rank"],
        "iteration": [1, 2, 3],
        "depth": [0, 1, 2]
    }

    data = load_from_pickle(file_path)

    results = []

    for task in commands['task']:
        algorithms = ['vertex_count']
        iterations = [1]
        depths = [0]

        if task == 'wp03':
            algorithms = commands['algorithm']

        if task == 'wp04a':
            iterations = commands['iteration']
            depths = [0]

        if task == 'wp04b':
            iterations = commands['iteration']
            depths = commands['depth']

        for algorithm in algorithms:
            for iteration in iterations:
                for depth in depths:
                    if task in ['wp02', 'wp03']:
                        iteration = 1
                        depth = 0
                        if task == 'wp02':
                            algorithm = 'x'

                    if task == 'wp04a':
                        algorithm = 'x'

                    if task == 'wp04b':
                        algorithm = 'x'

                    args = {
                        'task': task,
                        'algorithm': algorithm,
                        'iterations': iteration,
                        'depth': depth
                    }

                    clustered_data, t = execute(args, data)

                    # Ergebnis speichern
                    result = {
                        'task': task,
                        'algorithm': algorithm,
                        'iteration': iteration,
                        'depth': depth,
                        'time': round(t, 4),
                        'clusters': len(clustered_data)  # Anzahl der Cluster hinzufügen
                    }
                    results.append(result)

                    # Debugging-Ausgabe
                    print(f"The following setting with \n"
                          f"Task {task}, \n"
                          f"Algorithm {algorithm}, \n"
                          f"Iteration {iteration}, \n"
                          f"Depth {depth} \n"
                          f"Took {t:.4f} seconds\n"
                          f"and found {len(clustered_data)} clusters.\n")

                    # Assert
                    assert len(clustered_data) > 0, (f"The following setting with \n"
                                                     f"Task {task}, \n"
                                                     f"Algorithm {algorithm}, \n"
                                                     f"Iteration {iteration}, \n"
                                                     f"Depth {depth} \n"
                                                     f"produced no clusters.\n")

    # Ergebnisse in die CSV-Datei schreiben
    df = pd.DataFrame(results)
    df.to_csv(output_csv, mode='a', index=False, header=False)
    print(f"Results written to {output_csv}.")
