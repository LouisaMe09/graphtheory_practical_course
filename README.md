# ITS_ISO_Solver

_Imaginary Transition State Graph Isomorphism Solver_

## Usage

```txt
usage: python3 its_iso_solver [-h] [-t {wp02,wp03,wp04a,wp04b}] [-g GRAPHS] [-a {vertex_count,edge_count,vertex_degrees,algebraic_connectivity,rank}] [-i ITERATIONS] [-d DEPTH]

options:
  -h, --help            show this help message and exit
  -t {wp02,wp03,wp04a,wp04b}, --task {wp02,wp03,wp04a,wp04b}
                        Specifies the task to be used.
  -g GRAPHS, --graphs GRAPHS
                        Specifies the graphs to be used.
  -a {vertex_count,edge_count,vertex_degrees,algebraic_connectivity,rank}, --algorithm {vertex_count,edge_count,vertex_degrees,algebraic_connectivity,rank}
                        (wp03) Specifies the clustering algorithm to be used.
  -i ITERATIONS, --iterations ITERATIONS
                        (wp04a, wp04b) Specifies the number of Weisfeiler-Lehmann iterations.
  -d DEPTH, --depth DEPTH
                        (wp04b) Specifies the clustering depth.
```

## Setup

```shell
pip install -r requirements.txt
```

## Authors

[Maximilian Hoffmann](https://github.com/maximoffdev)\
[Louisa von Menges](https://github.com/LouisaMe09)\
[Lukas Marche](https://github.com/Lvkelol)
