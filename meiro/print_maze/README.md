# Print_Maze_Py

"Print_Maze_Py" is a routine that draws a maze  from a spannning tree with Python.

# Features

Print_Maze_Py used [NetworkX](https://networkx.github.io) .
 
```python
import networkx
```

# Requirement

* Python 3.7.6
* networkx 2.5

# Installation

Install NetworkX with pip command.

```bash
pip install networkx
```

# Usage

Please create input text file.

```python:input.txt
m,n     # m×n matrix
s,t     # s: source, t: target
N       # Number of branches
a1,b1   # Start and end points of each branches
:
:
aN,bN
```

Run "print_maze.py" .

```bash
python print_maze.py input_file.txt
```

With the '--answer' option, the shortest path from source node to target node is drawn.

```bash
python print_maze.py --answer input_file.txt
```

# Note

Be careful not to put a line break at the end of the file.
You should see the following error message.

```bash
"Error: blank line in the input file"
```

# Author

* Hiroki Yano
* Kwansei Gakuin University, MiwaLab
* yano@kwansei.ac.jp

# License
"Print_Maze_Py" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
 
Let's try drawing a maze using this program in gnp class!
 
Thank you!