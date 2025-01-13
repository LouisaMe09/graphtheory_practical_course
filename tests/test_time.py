import pytest
import os
import time
import importlib
from unittest.mock import MagicMock
import importlib
from synutility.SynIO.data_type import load_from_pickle


def execute(args, data):
    task = args['task']

    task_module = importlib.import_module('its_iso_solver.tasks.' + task)

    # Measure the time for clustering
    start_time = time.time()

    module = task_module.IsomorphismSolver(data=data, args=args)#.its_clustering().get_clustered_data()

    clustered_data = module.its_clustering().get_clustered_data()

    end_time = time.time()

    return clustered_data, (end_time - start_time)


def test_clustering_time():
    file_path = os.path.join('../data', 'ITS_graphs.pkl.gz')

    commands = {
        "task": ["wp02", "wp03", "wp04a", "wp04b"],
        "algorithm": ["vertex_count", "edge_count", "vertex_degrees", "rank"],  # "algebraic_connectivity"
        "iteration": [1, 2, 3],
        "depth": [0, 1, 2]
    }

    data = load_from_pickle(file_path)

    for task in commands['task']:

        algorithms = ['vertex_count']
        iterations = [1]
        depths = [0]

        if task == 'wp03':
            algorithms = commands['algorithm']

        if task == 'wp04a' or task == 'wp04b':
            iterations = commands['iteration']

        if task == 'wp04b':
            depths = commands['depth']


        for algorithm in algorithms:
            for iteration in iterations:
                for depth in depths:

                    args = {
                        'task': task,
                        'algorithm': algorithm,
                        'iterations': iteration,
                        'depth': depth
                    }

                    clustered_data, t = execute(args, data)

                    # Assert that the result is valid
                    assert len(clustered_data) > 0, (f"The following setting with \n"
                                                     f"Task {task}, \n"
                                                     f"Algorithm {algorithm}, \n"
                                                     f"Iteration {iteration}, \n"
                                                     f"Depth {depth} \n"
                                                     f"produced no clusters.\n")

                    # Print the time taken
                    print(f"The following setting with \n"
                          f"Task {task}, \n"
                          f"Algorithm {algorithm}, \n"
                          f"Iteration {iteration}, \n"
                          f"Depth {depth} \n"
                          f"Took {t:.4f} seconds\n"
                          f"and found {len(clustered_data)} clusters.\n")

