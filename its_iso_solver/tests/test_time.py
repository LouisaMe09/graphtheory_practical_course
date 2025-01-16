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
    module = task_module.IsomorphismSolver(data=data, args=args)
    
    start_time = time.time()

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
        "task": ["wpx"],
        "algorithms": [
            ["vertex_count", "weisfeiler_lehman"],
            ["edge_count", "weisfeiler_lehman"],
            ["vertex_degrees", "weisfeiler_lehman"],
            ["rank", "weisfeiler_lehman"],
            ["vertex_count", "edge_count", "weisfeiler_lehman"],
            ["vertex_count", "edge_count", "vertex_degrees", "weisfeiler_lehman"],
            ["vertex_count", "edge_count", "vertex_degrees", "rank", "weisfeiler_lehman"]
            ],
        "iterations": [1, 2, 3],
        "depths": [0, 1, 2]
    }

    data = load_from_pickle(file_path)

    results = []

    task = "wpx"
    algorithms = commands['algorithms']
    iterations = commands['iterations']
    depths = commands['depths']

    # if task == 'wp03':
    #     algorithms = commands['algorithm']

    # if task == 'wp04a':
    #     iterations = commands['iteration']
    #     depths = [0]

    # if task == 'wp04b':
    #     iterations = commands['iteration']
    #     depths = commands['depth']

    for algorithm in algorithms:
        for iteration in iterations:
            for depth in depths:

                args = {
                    'task': task,
                    'algorithms': algorithm,
                    'iterations': iteration,
                    'depth': depth,
                    'l_neighborhood': 1
                }

                clustered_data, t = execute(args, data)

                # Ergebnis speichern
                result = {
                    'task': task,
                    'algorithms': algorithm,
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
