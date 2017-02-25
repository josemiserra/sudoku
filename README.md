# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The constraint is applied globally on each iteration step, the same like we do with only choice or elimination.
The constraint can be defined as:
    When two boxes are equal in the same unit (row, column or square block), eliminate the digits that are the same in the other
    boxes belonging to the same unit.
It can be applied at each iteration step (it is convenient after we did only choice, to remove redundancy) in the reduction function,
or if we want to reduce computational cost we could apply it only when elimination and only choice strategies stall.
Applying the constraint of naked twins reduces the search space in the recursive tree because it can unblock certain stalled states that require
expansion of the search tree by trial and error.
The technique can be generalized to triplets and quads, reducing even more the expansion of the search tree.
However, this constraint is one rule more, it cannot solve all possible stalled states specially if they are very difficult or
the sudoku disposition allows relaxed solutions (however I must say a real sudoku by definition has a unique solution).
Even though, when applied to difficult sudokus, we can appreciate the improvement in performance during the solution state search.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We need to add diagonals as units. Any geometrical constraint between the boxes can be added as a set of units.
I just need to add the units (combination of boxes) that I want to fulfill the constraint. If the constraint
is not reasonable, that will end up without solution. But if it is possible, the tree search will try to find a solution.
The difference between this constraint and the Naked twins is that this constraint is applied abstractly (without knowing
the values a priori) and the naked twins can only be applied online, when the values in each iteration of the tree
are known.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.