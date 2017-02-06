assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
box_units = [cross(r,c) for r in ('ABC', 'DEF', 'GHI') for c in ('123', '456', '789')]
diagonal_units = [
    [r+c for r,c in zip(rows,cols)],
    [r+c for r,c in zip(rows,reversed(cols))]]
unitlist = row_units + col_units + box_units + diagonal_units
units = {s: [u for u in unitlist if s in u] for s in boxes} # map box to units
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes) # map box to peers

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        twins = set([box for box in unit if len(values[box]) == 2 and unit.count(values[box]) == 2]) # find all unique twins in a set
        for twin in twins:
            twin_val = values[twin]
            for digit in twin_val: # for each digit in a unique twin, iterate through the current unit and remove the digit from its value
                for u in unit:
                    if values[u] != twin_val:
                        values = assign_value(values, u, values[u].replace(digit, ''))
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
    return {k:(v if v != '.' else '123456789') for k,v in zip(boxes, grid)}

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    solved_boxes = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_boxes:
        val = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(val, ''))
    return values

def only_choice(values):
    for u in unitlist:
        for digit in '123456789':
            dplaces = [box for box in u if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False: return False
    if all(len(values[s]) == 1 for s in boxes): return values # completed

    n, s = min((len(values[s]), s) for s in boxes if len(values[x]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku = assign_value(new_sudoku, s, value)
        attempt = search(new_sudoku)
        if attempt: return attempt

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
    search_value = search(values)
    return search_value if search_value != False else False

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
