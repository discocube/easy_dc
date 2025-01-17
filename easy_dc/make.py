from collections import defaultdict
from itertools import product, chain, repeat

from easy_dc.defs import *
from easy_dc.utils import uon, save_G, timed
from easy_dc.xyz import Xy


def basis_vectors(unit: int = 2) -> BasisVectors:
    """
    Cube vectors centered at origin (0, 0, 0) with the edgelength of 2 to avoid floats.
    """
    return [Xy([0 if i != idx else 1 * s for i in range(3)]) for idx, x in enumerate('xyz') for s in (unit, -unit)]


def axis_vectors(unit: int = 1) -> AxisVectors:
    """
    Rotation Vectors
    """
    return {x: {f'{x}{s}': Xy([0 if i != idx else 1 * int(f'{s}{unit}') for i in range(3)]) for s in ('+', '-')} for idx, x in enumerate('xyz')}


def make_dcgraph(ORD: int, save: bool = True) -> Graph:
    """
    Make a discocube graph.
    """
    G = {
        'ORD': ORD,
        'V': (V := make_vertices(ORD)),
        'VI': (VI := make_vi_map(V)),
        'E': (E := make_edges(V, VI)),
        'A': (A := make_adjacency(E)),
        'EA': make_edges_adjacency(A, E),
        'W': {n: sum(map(abs, V[n])) for n in A},
        'CC': (cc_oe := make_coloring(A, both=True))[0],
        'OE': cc_oe[1],
        'ZA': stratify_A(A, V)
    }
    if save: save_G(G)
    return G


def make_vertices(ORD: int) -> Verts:
    """
    Vertices from the order.
    """
    OGN: Vector = 0, 0, 0
    BV: BasisVectors = basis_vectors()
    ORD_N = {order: n + 1 for n, order in enumerate(uon(8, 3_000_000))}
    stages = {k: set() if k else {OGN} for k in range(ORD_N[ORD])}
    for lvl in range(1, ORD_N[ORD]):
        stages[lvl] = {(Xy(vec) + xyz).data for vec in stages[lvl - 1] for xyz in BV}
    V = (p for ve in (tuple(tuple(c) for c in make_cube(p)) for p in set((tuple(v) for vc in list(stages.values()) for v in vc))) for p in ve)
    return sorted(set(V), key=lambda x: (edist(x), x[0], x[1], x[2]))


def make_cube(p: Xy = Xy((0, 0, 0))) -> Xy:
    """
    From an origin point, create a cube consisting of 8 corners (vertices).
    """
    AX: AxisRotations = axis_vectors()
    return Xy([s + AX['z'][k] for k in AX['z'] for s in Xy([Xy(j) + AX['y'][k] for j in Xy([Xy(p) + AX['x'][k] for k in AX['x']]) for k in AX['y']])])


def edist(a) -> float:
    """
    Calculate the Euclidean distance between point a and the origin (0, 0, 0).
    """
    return sum([((0, 0, 0)[idx] - a[idx]) ** 2 for idx in range(len(a))]) ** 0.5


def make_vi_map(V: Verts) -> IdxMap:
    """
    Make a mapping of key: data to value: idx_vert to avoid costly index lookups.
    """
    return dict(zip(V, range(len(V))))


def make_edges(V: Verts, VI: IdxMap, unit: int = 2) -> Edges:
    """
    Make edges from verts and vert mapping
    """
    BV: BasisVectors = basis_vectors(unit=unit)
    VS: QuickSet = make_quickset(V)
    return tuple(((i, VI[e]) for i, n in enumerate((((Xy(p) + xz).data for xz in BV if VS.issuperset([(Xy(p) + xz).data])) for p in V)) for e in n))


def make_quickset(to_set: Iterable) -> QuickSet:
    """
    Convert an iterable into a set to perform quick set operations.
    """
    return set(map(tuple, to_set))


def make_adjacency(edges: Edges) -> AdjDict:
    """
    Adjacency list from edges.

    Makes an adjacency dictionary from edges list.
    """
    A = {n: set() for n in {e for edge in edges for e in edge}}
    for edge in edges:
        A[edge[0]].add(edge[1])
        A[edge[1]].add(edge[0])
    return A


def make_edges_adjacency(A: AdjDict, E: Edges) -> EAdj:
    """
    Make an edges adjacency.

    Adjacent edges are those that are parallel to the edge and is one unit length away from the current edge.
    """
    et = set(map(frozenset, E))
    return {frozenset((u, p)): et & {*map(frozenset, product(A[u] - {p}, A[p] - {u}))} for u, p in et}


def make_coloring(A: AdjDict = None, both: bool = False, oddeven: bool = False) -> Union[Mapping, NodesGroup]:
    """
    Returns a dict mapping a node to its chromatic coloring.

    specify output.
    """
    odd_even = {0: {0}, 1: {*A[0]}}
    while set(A.keys()).difference(odd_even[0].union(odd_even[1])):
        for odd in odd_even[0]: odd_even[1].update(A[odd])
        for even in odd_even[1]: odd_even[0].update(A[even])
    colored_nodes = {number: key for key in odd_even.keys() for number in odd_even[key]}
    return odd_even if oddeven else (colored_nodes, odd_even) if both else colored_nodes


def stratify_A(A: AdjDict, V: Verts) -> GLvls:
    """
    Partition the Adjacency according to the z-axis.
    The resulting subgraphs are 2d grid graphs.
    """

    def stratified_nodes() -> AdjDict:
        """
        The adjacency should be partitioned so that the graph consists of planes of x, y,
        starting from the bottom.
        """
        return {z: {ix for ix, v in enumerate(V) if v[-1] == z} for z in sorted({vert[2] for vert in V}) if abs(z) != z}

    def filter_graph(nodes) -> NodesMap:
        """
        Create graph with only the nodes in nodes.
        """
        return {k: v.intersection(nodes) for k, v in A.items() if k in nodes}

    return {level: filter_graph(nodes) for level, nodes in stratified_nodes().items()}


def ae_for_grid(x: int = None, y: int = None, z: int = None, both: bool = False) -> Graph:
    """
    Create adjacency and edges dict/list for 2d/3d regular rectangular grids.

    Not providing z will create a 2d grid. Setting parameter <both> to True returns both 2d/3d versions as a dict.
        x: the width of the grid
    y: the height of the grid
    z: the depth of the grid (for 3D grids)
    both: a boolean flag indicating whether to return both 2D and 3D versions of the adjacency lists and edge lists as a dictionary.

    The function first creates a 2D grid of vertices using the xy_rng range object and the chunked function. It then initializes empty adjacency
    lists and edge lists A and E, respectively. Next, the function loops through the rows and columns of the grid, and for each vertex n, it adds its
    adjacent vertices to the adjacency list A and the corresponding edges to the edge list E. If the vertex is in the middle of the grid, it adds
    edges to all four of its adjacent vertices. If the vertex is on the edge or in a corner of the grid, it only adds edges to the adjacent vertices
    that exist. If the z parameter is not provided (indicating a 2D grid), the function returns the adjacency list A and the edge list E.
    If the z parameter is provided (indicating a 3D grid), the function generates an adjacency list A3 and an edge list E3 for the 3D grid by looping
    through the 2D layers of the grid and adding edges between each layer and the one above and below it.
    Finally, if the both parameter is set to True, the function returns a dictionary containing both the 2D and 3D versions of the adjacency lists and
    edge lists. Otherwise, it returns the appropriate adjacency list and edge list for the specified dimensions of the grid.
    """
    xy_rng = range(_xy := x * y)
    xy_grid = list(chunked(xy_rng, x))  # noqa
    A, E = defaultdict(set), set()
    for iy in range(y):
        for ix in range(x):
            n = xy_grid[iy][ix]
            if all((ix, iy)) and ix < x - 1 and iy < y - 1:
                A[n] = {n + 1, n - 1, n - x, n + x}
                E.update(map(lambda ns: frozenset([n, n + ns]), (1, -1, -x, x)))
            else:
                if ix:
                    A[n].add(n - 1)
                    E.add(frozenset([n, n - 1]))
                if ix < x - 1:
                    A[n].add(n + 1)
                    E.add(frozenset([n, n + 1]))
                if iy:
                    A[n].add(n - x)
                    E.add(frozenset([n, n - x]))
                if iy < y - 1:
                    A[n].add(n + x)
                    E.add(frozenset([n, n + x]))
    if not z:
        return A, E
    A3 = {k: set() for k in range(x * y * z)}
    for m in range(_xy):
        A3[m] = {*A[m], m + _xy}
        for i in range(1, z):
            n = m + (floor := i * _xy)
            A3[n] = {x + floor for x in A[m]}.union({n - _xy} if i == z - 1 else {n - _xy, n + _xy})
    E3 = {*map(frozenset, chain.from_iterable(map(lambda k: zip(repeat(k), A[k]), A)))}
    if not both:
        return A3, E3
    return {2: (A, E), 3: (A3, E3)}


def get_startpos(screen_size, cell_size, xy) -> Verts:
    """
    Calculate the start position based on screen size.

    location on screen to place top-left corner of grid.
    """
    return [(screen_size[i] - (xy[i] * cell_size)) // 2 for i in range(2)]


def make_vertices_grid(x, y, cellsize, offset=(0, 0)) -> Verts:
    """
    Makes vertices based on cell size.

    """
    return [(ix + offset[0], iy + offset[1]) for iy in range(0, y * cellsize, cellsize) for ix in range(0, x * cellsize, cellsize)]


def make_gridgraph(x, y, cell_size, screen_size=(1200, 1200)) -> Graph:
    """
    Make grid graph based on cellsize.
    """
    a, e = ae_for_grid(x, y)
    return {
        'startpos': (pos := get_startpos(screen_size=screen_size, cell_size=cell_size, xy=(x, y))),
        'A': a,
        'E': e,
        'V': make_vertices(x, y, cell_size, offset=pos),
        'V1': make_vertices(x, y, cellsize=2),
        'CC': make_coloring(a)[0],
        'EA': make_edges_adjacency(a, e)
    }
