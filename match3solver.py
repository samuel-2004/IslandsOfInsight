"""
Islands of Insight puzzle solvers
"""
from datetime import datetime as dt
import copy
from enum import Enum
from itertools import groupby
from re import findall

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
    N_CELLS_PER_REGION = 6

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
        out += '}'
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
    NA = 1000
    def __lt__(self, obj):
        return self.value < obj.value
    def __eq__(self,obj):
        return self.value == obj.value

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

    def __lt__(self, obj):
        return self.col < obj.col

    def __eq__(self, obj):
        return self.col == obj.col

    def set_info(self, info):
        """
        Sets info
        """
        self.inf = info

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
    def __init__(self, grid: list[list[LogicGridCell]], rules: list[Rule] = []):
        self.g = grid
        self.width = len(self.g[0])
        self.height = len(self.g)
        self.attempts = 0

        self.rules = rules

    def __str__(self) -> str:
        return str(self.g)

    def __repr__(self) -> str:
        out = ""
        for i in range(self.height):
            r = ""
            for j in self.g[i]:
                if j.col == Colour.BLACK:
                    r += 'B'
                elif j.col == Colour.WHITE:
                    r += 'W'
                elif j.col == Colour.EMPTY:
                    r += ' '
                elif j.col == Colour.NA:
                    r += '#'
            out += r + '\n'
        return out[:-1]

    def num_empty(self) -> int:
        """
        Calculates the number of empty cells in grid
        """
        total = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.g[i][j].col == Colour.EMPTY:
                    total += 1
        return total

    def print_rules(self) -> None:
        """
        Prints the logic grid's rules
        """
        for rule in self.rules:
            print(rule)

    def add_rule(self, rule: Rule) -> None:
        """
        Adds a new rule
        """
        self.rules.append(rule)

    def _is_pattern_found(self, pattern: list[list[LogicGridCell]]) -> bool:
        def rot90(l):
            """
            Rotates a 2d array 90* clockwise
            """
            return [list(x) for x in reversed(list(zip(*l)))]

        def transpose(l):
            """
            Transposes a list
            """
            return list(map(list, zip(*l)))

        # Create pattern variants
        list_of_patterns = []
        list_of_patterns.append(pattern)
        list_of_patterns.append(transpose(pattern))
        for i in range(3):
            pattern = rot90(pattern)
            list_of_patterns.append(pattern)
            list_of_patterns.append(transpose(pattern))

        # Remove duplicates
        list_of_patterns.sort()
        list_of_patterns = list(k for k,_ in groupby(list_of_patterns))

        for p in list_of_patterns:
            p_height = len(p)
            p_width = len(p[0])
            for i in range(self.height - p_height + 1):
                for j in range(self.width - p_width + 1):
                    p_matches = True
                    for i_1 in range(p_height):
                        for j_1 in range(p_width):
                            if p[i_1][j_1].col == Colour.EMPTY:
                                continue
                            elif self.g[i + i_1][j + j_1].col != p[i_1][j_1].col:
                                p_matches = False
                                break
                        if not p_matches:
                            break
                    if p_matches:
                        return True
        return False

    def _do_all_of_colour_connect(self, colour: int) -> bool:
        #print("Colour =",colour)
        #print(repr(self))
        # Function to perform DFS and mark visited 1s
        def dfs(x, y, visited):
            if x < 0 or y < 0 or x >= self.height or y >= self.width:
                return
            if self.g[x][y].col not in (colour, Colour.EMPTY) or visited[x][y]:
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
        visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        dfs(start[0], start[1], visited)

        # Check if all '1's are visited
        for i in range(self.height):
            for j in range(self.width):
                if self.g[i][j].col == colour and not visited[i][j]:
                    #print(f"Cell ({i}, {j}) not visited")
                    #print()
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

    def _n_symbols_per_colour_area(self, number_of_symbols: int, col: Colour) -> bool:
        def dfs(x: int, y: int, num_symbols: int) -> bool:
            stack = [(x, y)]
            visited = []
            colour = self.g[x][y].col
            symbols_in_area = 0

            while stack:
                e = stack.pop()
                if e in visited:
                    continue
                visited.append(e)
                # Update values
                if self.g[e[0]][e[1]].inf is not None:
                    symbols_in_area += 1
                    if symbols_in_area > num_symbols:
                        return False

                # Add orthogonal cells to stack
                if e[0] - 1 >= 0: # cell above
                    if self.g[e[0] - 1][e[1]].col == colour:
                        new_e = (e[0] - 1, e[1])
                        stack.append(new_e)
                if e[0] + 1 < self.height: # Cell below
                    if self.g[e[0] + 1][e[1]].col == colour:
                        new_e = (e[0] + 1, e[1])
                        stack.append(new_e)
                if e[1] - 1 >= 0: # cell to the left
                    if self.g[e[0]][e[1] - 1].col == colour:
                        new_e = (e[0], e[1] - 1)
                        stack.append(new_e)
                if e[1] + 1 < self.width: # cell to the right
                    if self.g[e[0]][e[1] + 1].col == colour:
                        new_e = (e[0], e[1] + 1)
                        stack.append(new_e)

        for i in range(self.height):
            for j in range(self.width):
                if self.g[i][j].inf is not None and self.g[i][j].col == col:
                    res = dfs(i, j, number_of_symbols)
                    if not res:
                        return False

    def _n_cells_per_region(self, number: int, col: Colour) -> bool:
        visited = []
        stack = []
        count = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.g[i][j].col != col:
                    continue
                if (i, j) in visited:
                    continue
                # At an unvisited cell, must check all cells around it to see if how big area is
                count = 1
                if j < self.width - 1: # Add cell to right
                    stack.append((i, j + 1))
                if i < self.height - 1: # Add cell below
                    stack.append((i + 1, j))
                while stack:
                    s = stack.pop()
                    visited.append(s)
                    if self.g[s[0]][s[1]].col != col:
                        continue
                    count += 1
                    if count > number: # Too many in region
                        return False
                    # Add surrounding cells to stack
                    if s[1] < self.width - 1: # Add cell to right
                        stack.append((s[0], s[1] + 1))
                    if s[1] > 0: # Add cell to left
                        stack.append((s[0], s[1] - 1))
                    if s[0] < self.height - 1: # Add cell below
                        stack.append((i + 1, j))
                    if s[0] > 0: # Add cell above
                        stack.append((i - 1, j))
                if count < number: # Not enough in region
                    return False
        return True

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
            elif rule.rule_type == RuleEnum.N_CELLS_PER_REGION:
                num = rule.rule_values["number"]
                col = rule.rule_values["colour"]
                if not self._n_cells_per_region(num, col):
                    return False
            elif rule.rule_type == RuleEnum.N_SYMBOL_PER_COLOUR:
                if self.num_empty() == 0:
                    num = rule.rule_values["number"]
                    col = rule.rule_values["colour"]
                    if not self._n_symbols_per_colour_area(num, col):
                        return False
        return True

    def _solve(self, _cell_x = 0, _cell_y = 0, depth = 0) -> bool:
        """
        Provides a solution to the puzzle
        If returns True, all checks passed
        If returns False, invalid solution
        """
        if depth == 2:#12.5%
            print(dt.now())
        # This is the final cell, and we need to check all rules are satisfied
        if _cell_x == self.height - 1 and _cell_y == self.width - 1:
            colours_to_test = [self.g[_cell_x][_cell_y].col]
            if self.g[_cell_x][_cell_y].col == Colour.EMPTY:
                colours_to_test = [Colour.WHITE,Colour.BLACK]
            for colour in colours_to_test:
                self.g[_cell_x][_cell_y].col = colour
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

        # if gray, try black and then white
        if self.g[_cell_x][_cell_y].col == Colour.EMPTY:
            colours_to_test = [Colour.WHITE,Colour.BLACK]
            for colour in colours_to_test:
                self.g[_cell_x][_cell_y].col = colour
                if not self._test_rules():
                    continue
                res = self._solve(new_cell_x, new_cell_y, depth + 1)
                if res: # If a solution is found
                    return True
            self.g[_cell_x][_cell_y].col = Colour.EMPTY
        else:
            res = self._solve(new_cell_x, new_cell_y, depth)
            if res: # If a solution is found
                return True
        return False

    def solution(self) -> None:
        """
        Provides a solution to the puzzle
        Prints to console
        """
        if self._solve():
            print("Valid Solution Found:")
            print(repr(self))
        else:
            #print(self.attempts)
            print("No valid solution found :(")

def interpret_lg(grid: list[str]) -> LogicGrid:
    """
    Creates a logic grid from a given grid
    eg
    [
    'GGGBWBW',
    'GGBWBWG'
    ]
    """
    logic_grid = []
    for row in grid:
        row = row.lower()
        logic_grid.append([])
        for char in row:
            if char == 'w':
                logic_grid[-1].append(LGC(Colour.WHITE))
            elif char == 'b':
                logic_grid[-1].append(LGC(Colour.BLACK))
            elif char == '#':
                logic_grid[-1].append(LGC(Colour.NA))
            else:
                logic_grid[-1].append(LGC(Colour.EMPTY))
    return LogicGrid(logic_grid)

def create_solid_shape(string = None, c: Colour = None, w: int = None, \
        h: int = None) -> list[list[LogicGridCell]]:
    """
    Interprets a string and converts it to create a solid shape
    """
    # Interpret string
    if string is not None:
        string = string.lower()
        # Interpret colour
        if 'black' in string:
            c = Colour.BLACK
        elif 'white' in string:
            c = Colour.WHITE
        # Get widht and height
        l = list(map(int, findall(r'\d+', string)))
        if len(l) == 2:
            w = l[0]
            h = l[1]
        else:
            raise ValueError("String had one number in it")

    out = []
    for _ in range(h):
        out.append([])
        for __ in range(w):
            out[-1].append(LogicGridCell(c))
    return out




LG = interpret_lg([
"EBEBEEWEEE",
"EWEBEWEEEW",
"EEWEBEBWEE",
"WEEEEEWBEB",
"EWEEBWEEBE",
"EBEEWBEEBE",
"BEBWEEEEEW",
"EEWBEWEBEE",
"WEEEBEWEBE",
"EEEWEEBEWE"
    ])
LG.g[0][3].inf = 'A'
LG.g[0][6].inf = 'B'
LG.g[3][0].inf = 'C'
LG.g[3][9].inf = 'D'
LG.g[6][0].inf = 'E'
LG.g[6][9].inf = 'F'
LG.g[9][3].inf = 'G'
LG.g[9][6].inf = 'H'

black2x2 = create_solid_shape("black2x2")
white2x2 = create_solid_shape("white2x2")

rules = [
Rule(RuleEnum.MATCH_NOT_PATTERN, pattern = black2x2),
Rule(RuleEnum.MATCH_NOT_PATTERN, pattern = white2x2),
Rule(RuleEnum.N_SYMBOL_PER_COLOUR, number = 1, colour = Colour.WHITE),
Rule(RuleEnum.N_SYMBOL_PER_COLOUR, number = 1, colour = Colour.BLACK)
]
for rule in rules:
    LG.add_rule(rule)

emp = LG.num_empty()
print(emp)
print(2 ** emp)
print(LG.height)
print(LG.width)
print('\n\n\n')

LG.solution()
