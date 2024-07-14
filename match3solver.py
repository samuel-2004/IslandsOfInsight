"""
Islands of Insight puzzle solvers
"""

import copy
from enum import Enum

class Match3():
    """
    Solves Match3 puzzles in Islands of Insight
    '#' or -1 count as rocks (imovable objects)
    0 is empty space
    param `grid` is a 2d array representing the objects
        each unique element can be combined
    func `solution` prints a solution to the Match3 puzzle to console
    """
    def __init__(self, grid):
        self.g = grid
        self.width = len(g[0])
        self.height = len(g)
        while True:
            if not self._check3():
                break

    def __str__(self):
        return str(self.g)

    def __repr__(self):
        out = ""
        for j in range(self.height):
            out += " ".join(str(x) for x in self.g[j]) + "\n"
        return out[:-1]

    def _check3(self, do_stuff = True):
        """
        Checks if 3 in a row exists
        param `do_stuff` default True
            if True, will convert any found 3 in a rows (or longer) to 0s
        """
        cells_to_remove = []
        for i in range(self.height):
            for j in range(self.width):
                cell = self.g[i][j]
                if cell in [0,-1,'#']:
                    continue

                # n in a column :
                if i < self.height - 2: # Two below
                    if cell == self.g[i+1][j] and cell == self.g[i+2][j]:
                        cells_to_remove.append((i,j))
                        continue
                if i > 0 and i < self.height - 1: # One below, One above
                    if cell == self.g[i-1][j] and cell == self.g[i+1][j]:
                        cells_to_remove.append((i,j))
                        continue
                if i > 1: # Two above
                    if cell == self.g[i-2][j] and cell == self.g[i-1][j]:
                        cells_to_remove.append((i,j))
                        continue

                # n in a row:
                if j < self.width - 2: # Two to the right
                    if cell == self.g[i][j+1] and cell == self.g[i][j+2]:
                        cells_to_remove.append((i,j))
                        continue
                if j > 0 and j < self.width - 1: # One left, One right
                    if cell == self.g[i][j-1] and cell == self.g[i][j+1]:
                        cells_to_remove.append((i,j))
                        continue
                if j > 1: # Two to the left
                    if cell == self.g[i][j-2] and cell == self.g[i][j-1]:
                        cells_to_remove.append((i,j))
                        continue
        if do_stuff:
            for cell in cells_to_remove:
                self.g[cell[0]][cell[1]] = 0

            while True:
                if not self._drop():
                    break
        return len(cells_to_remove) > 0

    def _drop(self):
        """
        Drops all tiles to the lowest possible position
        """
        has_dropped = False
        for i in range(self.height - 1):
            for j in range(self.width):
                if self.g[i][j] not in [0,-1,'#'] and self.g[i+1][j] == 0:
                    self.g[i+1][j] = self.g[i][j]
                    self.g[i][j] = 0
                    has_dropped = True
        return has_dropped

    def swap(self, x1, y1, x2, y2, do_stuff = True):
        """
        Swaps two tiles
        (x1,y1) <-> (x2,y2)
        param do_stuff default True
            if True, call _check3
        """
        old1 = self.g[x1][y1]
        self.g[x1][y1] = self.g[x2][y2]
        self.g[x2][y2] = old1
        if do_stuff:
            while True:
                if not self._check3():
                    break

    def _check_if_move_valid(self, x1, y1, x2, y2):
        """
        Checks if swapping (x1,y1) <-> (x2,y2) is a valid move
        """
        # Positions are not directly next to each other
        if abs(x1-x2) != 1 and y1 == y2:
            return False
        if abs(y1-y2) != 1 and x1 == x2:
            return False
        # Either are 0
        if self.g[x1][y1] == 0 or self.g[x2][y2] == 0:
            return False
        # They are the same
        if self.g[x1][y1] == self.g[x2][y2]:
            return False
        # Swapping would not result in anything happening
        self.swap(x1, y1, x2, y2, False)
        result = self._check3(False)
        self.swap(x1, y1, x2, y2, False)
        return result

    def generate_moves(self):
        """
        Generates a list of available moves
        """
        moves = []
        for i in range(self.height):
            for j in range(self.width):
                cell = self.g[i][j]
                if cell == 0:
                    continue
                # Check if swaps with tile orthogonally down
                if i < self.height - 1:
                    if self._check_if_move_valid(i, j, i+1, j):
                        moves.append((i, j, i+1, j))
                # Check if swaps with tile orthogonally right
                if j < self.width - 1:
                    if self._check_if_move_valid(i, j, i, j+1):
                        moves.append((i, j, i, j+1))
        return moves

    def is_solved(self):
        """
        Checks if the grid is solved
        A grid is solved iff the cells only contain 0,-1, or '#'
        """
        for i in range(self.height):
            for j in range(self.width):
                if self.g[i][j] not in [0,-1,'#']:
                    return False
        return True

    def solve(self, _depth = 0):
        """
        Does a DFS to find a solution
        """
        moves = self.generate_moves()
        stored_grid = copy.deepcopy(self.g)
        for move in moves:
            # Make move
            self.swap(*move)

            # If the puzzle is solved, return the move
            if self.is_solved():
                return [move]

            # If a solution is found, return the moves
            solution = self.solve(_depth + 1)
            if solution is not None:
                solution.append(move)
                return solution

            # Delete child
            self.g = copy.deepcopy(stored_grid)
        return None

    def solution(self):
        """
        Prints a solution to the grid to console
        """
        s = self.solve()
        print("Solution:")
        for i in range(len(s)):
            print(i,":",s[-1-i])

class RuleEnum(Enum):
    """
    enum for rules available
    `MATCH_PATTERN` = must match a certain pattern\n
    `MATCH_NOT_PATTERN` = must not match a certain pattern\n
    `NUMBER` = region must be of specified size\n
    `CONNECT_CELLS` = cells of same colour (as specified) must connect\n
    `N_SYMBOL_PER_COLOUR` = n symbols (as specified) per colour (as specified)
    """
    MATCH_PATTERN = 0
    MATCH_NOT_PATTERN = 1
    AREA_NUMBER = 2
    AREA_NUMBERS_ARE_ONE_OFF = 3
    CONNECT_CELLS = 4
    N_SYMBOL_PER_COLOUR = 5

class Rule():
    """
    Pattern Required:\n
    `MATCH_PATTERN` = must match a certain pattern\n
    `MATCH_NOT_PATTERN` = must not match a certain pattern

    Number Value Required:\n
    `AREA_NUMBER` = region must be of specified size\n
    `CONNECT_CELLS` = cells of same colour (as specified) must connect

    Number and Colour Value required:\n
    `N_SYMBOL_PER_COLOUR` = n symbols (as specified) per colour (as specified)
    """
    def __init__(self, rule_type: RuleEnum, **kwargs):
        self.rule_type = rule_type
        self.rule_values = kwargs

    def __str__(self):
        out = f"Rule({RuleEnum(self.rule_type)}," + '{'
        for key, val in self.rule_values.items():
            out += f'({key}: {val})'
        return out

    def __repr__(self):
        out = f"Rule of type {RuleEnum(self.rule_type)} with values"
        for key, val in self.rule_values.items():
            out += f'\n{key} '
            if isinstance(val, list):
                for row in val:
                    out = out[:-1] + '\n'
                    for col in row:
                        out += str(col) + " "
            else:
                out += f'\n({key}, {val})'
        return out

class Colour(Enum):
    """
    Cell colour
    """
    BLACK = -1
    EMPTY = 0
    WHITE = 1

class LogicGridCell():
    """
    Defines a class to contain logic grid cell info
    """
    def __init__(self, colour: Colour, info = None):
        self.col = colour
        self.inf = info

    def __str__(self):
        return f'LogicGridCell({Colour(self.col)},{self.inf})'
    def __repr__(self):
        return str(self)

LGC = LogicGridCell

class LogicGrid():
    """
    Solves LogicGrid puzzles in Islands of Insight

    param `grid` is a 2d array representing the cells
    Each cell is a tuple
    (colour, info)
    colour:
        'B' or -1 is a black coloured square
        'W' or +1 is a white coloured square
        ' ' or 0 is an empty or gray space
    info:
        represents any given info about the cell
        e.g. a number or arrow

    param `rules`: a list of rules provided about the puzzle

    func `solution` prints a solution to the LogicGrid puzzle to console
    """
    def __init__(self, grid: list[list[LogicGridCell]], rules: list[Rule]):
        self.g = grid
        self.width = len(g[0])
        self.height = len(g)

        self.rules = rules

    def __str__(self) -> str:
        return str(self.g)

    def __repr__(self) -> str:
        out = ""
        for i in range(self.height):
            r = ""
            for j in self.g[i]:
                if j.col == Colour.BLACK:
                    r += f'(B, {j.inf})'
                elif j.col == Colour.WHITE:
                    r += f'(W, {j.inf})'
            out += r + '\n'
        return out[:-1]

    def _is_pattern_found(self, pattern: list[list[LogicGridCell]]) -> bool:
        pattern_height = len(pattern)
        pattern_width = len(pattern[0])
        for i in range(self.height - pattern_height + 1):
            for j in range(self.width - pattern_width + 1):
                pattern_matches = True
                for i_1 in range(pattern_height):
                    for j_1 in range(pattern_width):
                        if self.g[i + i_1][j + j_1].col != pattern[i_1][j_1].col:
                            pattern_matches = False
                            break
                    if not pattern_matches:
                        break
                if pattern_matches:
                    return True
        return False

    def _do_all_of_colour_connect(self, colour: int) -> bool:
        # Function to perform DFS and mark visited 1s
        def dfs(x, y, visited):
            if x < 0 or y < 0 or x >= self.height or y >= self.width or self.g[x][y].col != colour or visited[x][y]:
                return
            visited[x][y] = True
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
            for dx, dy in directions:
                dfs(x + dx, y + dy, visited)

        # Find the first '1' to start the DFS
        start = None
        for i in range(self.height):
            for j in range(self.width):
                if self.g[i][j].col == colour:
                    start = (i, j)
                    break
            if start:
                break

        if not start:
            return True  # No '1's in the self.g, considered as connected

        # Initialize visited array and start DFS from the first '1'
        visited = [[False for _ in range(self.height)] for _ in range(self.width)]
        dfs(start[0], start[1], visited)

        # Check if all '1's are visited
        for i in range(self.height):
            for j in range(self.width):
                if self.g[i][j].col == colour and not visited[i][j]:
                    return False
        return True

    def _check_area_numbers(self, one_off = False) -> bool:
        def dfs(x: int, y: int, num: int, one_off: bool):
            stack = [(x, y)]
            visited = []
            cells_in_area = 0
            colour = self.g[x][y].col

            while stack:
                e = stack.pop(0)
                if e in visited:
                    continue
                visited.append(e)
                if self.g[e[0]][e[1]].col != colour:
                    continue
                cells_in_area += 1
                if one_off:
                    if cells_in_area > num + 1:
                        break

                # Add orthogonal cells to stack
                if e[0] - 1 >= 0: # cell above
                    if self.g[e[0] - 1][e[1]].col == colour:
                        new_e = (e[0] - 1, e[1])
                        if new_e not in visited:
                            stack.append(new_e)
                if e[0] + 1 < self.height: # Cell below
                    if self.g[e[0] + 1][e[1]].col == colour:
                        new_e = (e[0] + 1, e[1])
                        if new_e not in visited:
                            stack.append(new_e)
                if e[1] - 1 >= 0: # cell to the left
                    if self.g[e[0]][e[1] - 1].col == colour:
                        new_e = (e[0], e[1] - 1)
                        if new_e not in visited:
                            stack.append(new_e)
                if e[1] + 1 < self.width: # cell to the right
                    if self.g[e[0]][e[1] + 1].col == colour:
                        new_e = (e[0], e[1] + 1)
                        if new_e not in visited:
                            stack.append(new_e)

            if one_off:
                return (cells_in_area == num - 1) or (cells_in_area == num + 1)
            else:
                return cells_in_area == num

        for i in range(self.height):
            for j in range(self.width):
                if "number" in self.g[i][j].inf:
                    # Now need to do a dfs from here
                    res = dfs(i, j, self.g[i][j]["number"], one_off)
                    if not res:
                        return False

    def _test_rules(self) -> bool:
        for rule in self.rules:
            if rule.rule_type in [RuleEnum.MATCH_PATTERN, RuleEnum.MATCH_NOT_PATTERN]:
                is_pattern_found = self._is_pattern_found(rule.rule_values["pattern"])
                if (rule.rule_type == RuleEnum.MATCH_PATTERN and not is_pattern_found) or \
                   (rule.rule_type == RuleEnum.MATCH_NOT_PATTERN and is_pattern_found):
                    return False
            elif rule.rule_type in [RuleEnum.AREA_NUMBER, RuleEnum.AREA_NUMBERS_ARE_ONE_OFF]:
                one_off = rule.rule_type != RuleEnum.AREA_NUMBER
                if not self._check_area_numbers(one_off):
                    return False
            elif rule.rule_type == RuleEnum.CONNECT_CELLS:
                do_cells_connect = self._do_all_of_colour_connect(rule.rule_values["colour"])
                if not do_cells_connect:
                    return False
            elif rule.rule_type == RuleEnum.N_SYMBOL_PER_COLOUR:
                pass
        return True

    def _solve(self, _cell_x = 0, _cell_y = 0) -> bool:
        """
        Provides a solution to the puzzle
        If returns True, all checks passed
        If returns False, invalid solution
        """
        colours_to_test = [self.g[_cell_x][_cell_y][0]]
        # if gray, try black and then white
        if self.g[_cell_x][_cell_y][0] in [0, ' ']:
            colours_to_test = [-1,1]

        if _cell_x == self.height - 1 and _cell_y == self.width - 1:
            # This is the final cell, and we need to check all rules are satisfied
            for colour in colours_to_test:
                self.g[_cell_x][_cell_y][0] = colour
                if self._test_rules():
                    return True
            return False

        # Advance to next cell
        if _cell_y == self.width - 1: # If last cell in row
            new_cell_y = 0
            new_cell_x = _cell_x + 1
        else:
            new_cell_y = _cell_y + 1
            new_cell_x = _cell_x

        for colour in colours_to_test:
            self.g[_cell_x][_cell_y][0] = colour
            res = self._solve(new_cell_x, new_cell_y)
            if res: # If a solution is found
                return True

    def solution(self) -> None:
        """
        Provides a solution to the puzzle
        Prints to console
        """
        if self._solve():
            print("Valid Solution Found:")
            for i in range(self.height):
                r = ""
                for j in self.g[i]:
                    if j[0] in [-1,'B']:
                        r += 'B '
                    elif j[0] in [1,'W']:
                        r += 'W '
                print(r)
        else:
            print("No valid solution found :(")

_ = """g = [
[0,  0,  'P',  0,  0],
[0,  'A','W','A',  0],
['A','W','A','W','A'],
['A','W','A','W','A'],
['W','A','W','A','W'],
['#','#','A','#','#'],
['#','P','W','P','#']
]
G = Match3(g)
print(repr(G))
G.solution()"""

g = [
    [LGC(0),LGC(0)],
    [LGC(0),LGC(0)]
    ]
G = LogicGrid(g, [])
G.solution()
