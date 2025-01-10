import argparse
import os
#import tasks.wp03 as wp03
import importlib


if __name__ == '__main__':
    file_path = os.path.join('data', 'ITS_graphs.pkl.gz')

    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--task", help="Specifies the task to be used.", required=False, default="wp02", choices=["wp02", "wp03", "wp04a", "wp04b"])
    parser.add_argument("-g", "--graphs", help="Specifies the graphs to be used.", required=False, default=file_path)
    parser.add_argument("-a", "--algorithm", help="(wp03) Specifies the clustering algorithm to be used.", required=False, default="vertex_count", choices=["vertex_count", "edge_count", "vertex_degrees", "algebraic_connectivity", "rank"])
    parser.add_argument("-i", "--interations", help="(wp04a, wp04b) Specifies the number of Weisfeiler-Lehmann iterations.", required=False, default=3)
    parser.add_argument("-d", "--depth", help="(wp04b) Specifies the clustering depth.", required=False, default=0, type=int)

    args = vars(parser.parse_args())

    task = args['task']

    task_module = importlib.import_module('tasks.' + task)

    clustered_data = task_module.IsomorphismSolver(graph_path=args['graphs'], args=args).its_clustering().get_clustered_data()

    print(len(clustered_data))
