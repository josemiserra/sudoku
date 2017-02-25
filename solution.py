import re
import itertools

assignments = []
is_diagonal = True


def cross(A, B):
    """Cross product of elements in A and elements in B."""
    return [s + t for s in A for t in B]


rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

diagonal_units = [[i + j for i, j in zip(rows, cols)], [i + j for i, j in zip(rows, cols[::-1])]]

unitlist = row_units + column_units + square_units

if (is_diagonal):
    unitlist = unitlist + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values, n=2):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        n : n can be 2,3,4 depending if you want to search pairs, triplets or quads...
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # This constraint implies that all candidates must have 2 digits.
    # The code can be generalized to triplets or Quads by changing then value len(values[box]) to n
    candidate_values = [box for box in values.keys() if len(values[box]) == 2]
    if (not candidate_values):
        return values
    # Now I need to invert the dictionary to find which ones are repeated (have each value more than once)
    rev_values = {}
    for box in candidate_values:
        rev_values.setdefault(values[box], set()).add(box)
    # My candidates are all boxes with two digits that are repeated more than once across my sudoku
    candidate_twins = [list(box) for digits, box in rev_values.items() if len(box) > 1]
    if (not candidate_twins):
        return values
    # The problem here is that I can have repetitions all over my sudoku with 3 or 4 times the same pair of digits
    # That means we have to resolve couples in the same row, column or square, independently
    for twins_list in candidate_twins:
        list_pairs = list(itertools.combinations(twins_list, 2))
        for pair in list_pairs:
            twin_1 = pair[0]
            twin_2 = pair[1]
            # if that is the case, we have to find for which unit
            units_to_check = [units[twin_2][i] for i in range(3) if twin_1 in units[twin_2][i]]
            # If the twin_1 is in the same row, column or square as twin_2
            for digit in list(values[twin_1]):
                for unit in units_to_check:
                    for el in unit:
                        if not (el == twin_1) and not (el == twin_2):
                            assign_value(values, el, values[el].replace(digit, ''))
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    sudoku_re = re.compile(r'^[\d\.]+$')
    if sudoku_re.match(grid):
        assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
        in_dict = dict(zip(boxes, grid))
        for key, value in in_dict.items():
            if (value == '.'):
                in_dict[key] = '123456789'
        return in_dict


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for el in peers[box]:
            assign_value(values, el, values[el].replace(digit, ''))
    return values


def only_choice(values):
    for unit in unitlist:  # For each box, we have 27 boxes and 3 units assigned to each
        counter = dict(zip('123456789', [list() for x in range(9)]))
        for el in unit:
            for digit in list(values[el]):
                counter[digit].append(el)
        for key, dvalues in counter.items():
            if (len(dvalues) == 1):
                assign_value(values, dvalues[0], key)
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        if (stalled):
            # Now we need to apply Naked twins
            values = naked_twins(values)
            values = eliminate(values)
            values = only_choice(values)
            # Check how many boxes have a determined value, to compare
            solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
            stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    values = reduce_puzzle(values)
    if (not values):
        return False
    # Choose one of the unfilled squares with the fewest possibilities
    list_n = [len(value) for _, value in values.items()]
    max_val = max(list_n)
    if (max_val == 1):
        return values
    else:
        list_to_search = [i[0] for i in sorted(zip(values.keys(), list_n), key=lambda x: x[1]) if i[1] > 1]

    box = list_to_search[0]
    to_do = list(values[box])
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for digit in to_do:
        values2 = values.copy()
        assign_value(values2, box, digit)
        values2 = search(values2)
        if (values2):
            return values2
    return False


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # diag_sudoku_grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)
    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
