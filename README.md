# easy dc solver

An algorithm for solving the Hamiltonian cycle problem deterministically and in linear time on all instances of the discocube graphs:
3-dimensional grid graphs derived from: a polycube of an octahedron | a Hauy construction of an octahedron using cubes as identical building blocks | the accretion of cubes around a central cube which forms an octahedron at the limit...

![Alt text](imgs/planar_embedding.png?raw=true "runtimes of each order")


I hope to tell the story of the discocube, introduce an undefined graph class *Cubic Accretion Graphs*, some of its properties, and the share insights I've gained by solving this problem having taken an approach similar to sculpting the human body...After thousands of studies, drawings, a little math: this is a tiny glimpse into how moving towards a specific aethetic goal yields results. When a graph becomes an artist's muse, how does the artist go about rendering their vision as a painter paints a portrait?

*to be continued...*

What started as a hack-your-own version of a depth-first-search-with-shortcuts for the discocube graph (solving up to 960 vertices), metastasized into pages of overgrown mixin classes mysteriously coupled to each another like overgrown vines pushing me deeper and deeper into the underbelly of its mutant tentacles. Although it was able to solve instances of over a million vertices, it had the clarity of primordial soup. So, as a sadistic gardener I painstakingly pruned my own unescapable web (all those letters you haven't opened yet?) of thorny vines into presentable tiny bonsai trees. So what is a bonsai if not a tree in intimate scope?

To paraphrase Hauy: 

*When solving problems that involve analyzing how nature progresses, we are led by very rapid methods to results that are not immediately obvious. These results may appear paradoxical and surprising. However, if we take the time to carefully examine the steps we took to reach these results, we will begin to understand the underlying principles that led to these outcomes. By going back over the process step by step, we can better understand the logic behind the final results.*

The result of this creative process is a family of algorithms developed specifically to solve various graph problems on the disocube graph. 
The algorithm presented in this repository is the least complex, also making it the fastest. It does the job, solving the hamiltonian cycle problem for over millions of vertices in reasonable time (seconds vs. years), while others take longer but also have other objectives, like forming an always turning cycle with even edge distribution across all axes. But that's giving too much away... 

Eventually this repository will include other linear time algorithms for solving the hamiltonian cycle problem in 3d grid graphs and also in solid grid graphs, addressing some open issues raised in the graph theory research literature.
Execution time of each order (in millions):

### Running times
As the order of the graph increases the number of function calls for each nodes goes down to less than 1.5 function calls when profiled using a 
deterministic profiler. At around 2 million vertices the function call for each node goes down to almost one.

![Alt text](imgs/8-2million.png?raw=true "runtimes of each order")

## Installation

You can install the package by running: 
```
pip install solve_dc
```

## Usage

You can use the package by running the following command in the command line:
```
solve(order)
```

## Command line usage
To use the package via the command line, navigate to the root directory of the project in your terminal and run the following command:
```
python -m solve_dc solve [ORDER]
```
Where [ORDER] is the order of the graph you want to solve. This command will create the graph if it does not already exist, solve the problem, print the time it took to solve the problem, and plot the solution as a 3D line drawing.

You can also pass multiple orders to solve at once by separating them with a space:
```
python -m solve_dc solve 32 80 160 280
```
You can also use the '--help' flag to see a list of available orders:
```
python -m solve_dc solve --help
```
This will show a list of available orders, which can be used as input when running the solve command.

Note that the first 25 instances, from order 32 to 26208, are already included in the package. If you want to solve higher instances, you will need to create the corresponding graphs first using the make_graphs command (see below).

## Creating graphs
To create new graphs, you can use the 'make_graphs' command:
```
python -m solve_dc make_graphs [ORDER] 
```
Where [ORDER] is the order of the graphs you want to create. The graphs will be saved in the graphs folder within the project directory.
Upon installation, the package will create 25 problem instances from order 32 to 26208 in the graphs folder. You can solve higher instances but the graphs will have to be produced first.

You can also pass multiple orders to create at once by separating them with a space:
```
python -m solve_dc make_graphs 32 80 280 960
```
This command will create 3 graphs of order 32, 80, 280 and 960.

Where order is an integer from the following list of available orders:

```
[32, 80, 160, 280, 448, 672, 960, 1320, 1760, 2288, 2912, 3640, 4480, 5440, 6528, 7752, 9120, 10640, 12320, 14168, 16192, 18400, 20800, 23400, 26208, 29232, 32480, 35960, 39680, 43648, 47872, 52360, 57120, 62160, 67488, 73112, 79040, 85280, 91840, 98728, 105952, 113520, 121440, 129720, 138368, 147392, 156800, 166600, 176800, 187408, 198432, 209880, 221760, 234080, 246848, 260072, 273760, 287920, 302560, 317688, 333312, 349440, 366080, 383240, 400928, 419152, 437920, 457240, 477120, 497568, 518592, 540200, 562400, 585200, 608608, 632632, 657280, 682560, 708480, 735048, 762272, 790160, 818720, 847960, 877888, 908512, 939840, 971880, 1004640, 1038128, 1072352, 1107320, 1143040, 1179520, 1216768, 1254792, 1293600, 1333200, 1373600, 1414808, 1456832, 1499680, 1543360, 1587880, 1633248, 1679472, 1726560, 1774520, 1823360, 1873088, 1923712, 1975240, 2027680, 2081040, 2135328, 2190552, 2246720, 2303840, 2361920, 2420968, 2480992, 2542000, 2604000, 2667000, 2731008, 2796032, 2862080, 2929160, 2997280]
```

The program will then solve the problem instance, display the time it took and plot the solution as a 3D line drawing.

## Additional Options

You can also use the '--output' flag to specify a custom directory to save the output graphs. For example:
```
python -m solve_dc make_graphs 1373600 --output /path/to/custom/directory
```
## Licensing:
This package is licensed under the MIT license.