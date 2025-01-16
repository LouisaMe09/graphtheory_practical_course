# ITS_ISO_Solver

_Imaginary Transition State Graph Isomorphism Solver_

## Usage

```txt
usage: python3 its_iso_solver [-h] [-t {wp02,wp03,wp04a,wp04b,wpx}] [-g GRAPHS] [-l L_NEIGHBORHOOD] [-a {vertex_count,edge_count,vertex_degrees,algebraic_connectivity,rank}] [-i ITERATIONS] [-d DEPTH]
                      [-x {vertex_count,edge_count,vertex_degrees,algebraic_connectivity,rank,weisfeiler_lehman,weisfeiler_lehman_nx} [{vertex_count,edge_count,vertex_degrees,algebraic_connectivity,rank,weisfeiler_lehman,weisfeiler_lehman_nx} ...]]

options:
  -h, --help            show this help message and exit
  -t {wp02,wp03,wp04a,wp04b,wpx}, --task {wp02,wp03,wp04a,wp04b,wpx}
                        Specifies the task to be used.
  -g GRAPHS, --graphs GRAPHS
                        Specifies the graphs to be used.
  -l L_NEIGHBORHOOD, --l_neighborhood L_NEIGHBORHOOD
                        Specifies the L-neighborhood of the reaction center.
  -a {vertex_count,edge_count,vertex_degrees,algebraic_connectivity,rank}, --algorithm {vertex_count,edge_count,vertex_degrees,algebraic_connectivity,rank}
                        (wp03) Specifies the clustering algorithm to be used.
  -i ITERATIONS, --iterations ITERATIONS
                        (wp04a, wp04b, wpx) Specifies the number of Weisfeiler-Lehmann iterations.
  -d DEPTH, --depth DEPTH
                        (wp04b, wpx) Specifies the clustering depth.
  -x {vertex_count,edge_count,vertex_degrees,algebraic_connectivity,rank,weisfeiler_lehman,weisfeiler_lehman_nx} [{vertex_count,edge_count,vertex_degrees,algebraic_connectivity,rank,weisfeiler_lehman,weisfeiler_lehman_nx} ...], --algorithm-list {vertex_count,edge_count,vertex_degrees,algebraic_connectivity,rank,weisfeiler_lehman,weisfeiler_lehman_nx} [{vertex_count,edge_count,vertex_degrees,algebraic_connectivity,rank,weisfeiler_lehman,weisfeiler_lehman_nx} ...]
                        (wpx) Specifies the clustering algorithms to be used.
```

## Setup

```shell
pip install -r requirements.txt
```

## Authors

[Maximilian Hoffmann](https://github.com/maximoffdev)\
[Louisa von Menges](https://github.com/LouisaMe09)\
[Lukas Marche](https://github.com/Lvkelol)
