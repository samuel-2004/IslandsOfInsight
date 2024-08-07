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
    def __init__(self, grid: list[list[str]]):
        self.g = grid
        self.width = len(grid[0])
        self.height = len(grid)
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

            # Undo move
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
    `N_CELLS_PER_REGION` = n cells (as specified) per colour region (as specified)
    `LETTER_SORTED` = each letter are in the same region
    """
    MATCH_PATTERN = 0
    MATCH_NOT_PATTERN = 1
    AREA_NUMBER = 2
    AREA_NUMBERS_ARE_ONE_OFF = 3
    CONNECT_CELLS = 4
    N_SYMBOL_PER_COLOUR = 5
    N_CELLS_PER_REGION = 6
    LETTER_SORTED = 7

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
        if 'pattern' in self.rule_values:
            self.compute_patterns()

    def __str__(self):
        out = f"Rule({RuleEnum(self.rule_type)}," + '{'
        for key, val in self.rule_values.items():
            out += f'({key}: {val})'
        out += '}'
        return out

    def compute_patterns(self) -> None:
        """
        Computes the patterns of the rule
        """
        if not self.rule_values['pattern']:
            return

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

        pattern = self.rule_values['pattern']
        # Create pattern variants
        list_of_patterns = []
        list_of_patterns.append(pattern)
        list_of_patterns.append(transpose(pattern))
        for _ in range(3):
            pattern = rot90(pattern)
            list_of_patterns.append(pattern)
            list_of_patterns.append(transpose(pattern))

        # Remove duplicates
        list_of_patterns.sort()
        list_of_patterns = list(k for k,_ in groupby(list_of_patterns))

        # Add to rule values
        self.rule_values['patterns'] = list_of_patterns

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
        out = "('"
        if self.col == Colour.BLACK:
            out += "B"
        elif self.col == Colour.NA:
            out += "#"
        elif self.col == Colour.WHITE:
            out += "W"
        else:
            out += " "
        out += "',"
        for i, j in self.inf:
            out += i + ":" + j
        out = out[:-1] + ")"
        return out

    def __repr__(self):
        return f'LogicGridCell({Colour(self.col)},{self.inf})'

    def __lt__(self, obj):
        return self.col < obj.col

    def __eq__(self, obj):
        return self.col == obj.col

    def set_info(self, info):
        """
        Sets info
        """
        self.inf = info

    def set_colour(self, colour: Colour):
        """
        Sets info
        """
        self.col = colour

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
    def __init__(self, grid: list[list[LogicGridCell]], rules: list[Rule] = [], \
                 linked_cells: list[list[(int, int)]] = []):
        self.g = grid
        self.width = len(self.g[0])
        self.height = len(self.g)
        self.attempts = 0

        self.rules = rules
        self.linked_cells = linked_cells
        if len(linked_cells) > 0:
            self.sort_linked_cells()

    def __str__(self) -> str:
        out = ""
        for row in self.g:
            out += "[" + ",".join([str(l) for l in row]) + "]\n"
            print(out)
            return out
        return out[:-1]

    def __repr__(self) -> str:
        out = str(self.g)
        out += "\nRules:"
        for i, rule in enumerate(self.rules):
            out += f'{i}. {rule}\n'
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

    def sort_linked_cells(self):
        """
        Sorts each list of linked cells, so that we don't 
        have to look through every cell when scanning the grid
        """
        for ls in self.linked_cells:
            ls.sort()

    def add_linked_cells(self, ls: list[(int,int)]):
        """
        Adds the linked cell to the list
        """
        self.linked_cells.append(ls)
        self.sort_linked_cells()

    def _is_pattern_found(self, pattern: list[list[LogicGridCell]] = None, \
                          patterns: list[list[list[LogicGridCell]]] = None) -> bool:
        if pattern:
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
            patterns = []
            patterns.append(pattern)
            patterns.append(transpose(pattern))
            for i in range(3):
                pattern = rot90(pattern)
                patterns.append(pattern)
                patterns.append(transpose(pattern))

            # Remove duplicates
            patterns.sort()
            patterns = list(k for k,_ in groupby(patterns))

        for p in patterns:
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
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        def dfs(x, y, visited):
            if x < 0 or y < 0 or x >= self.height or y >= self.width:
                return
            if self.g[x][y].col not in (colour, Colour.EMPTY) or visited[x][y]:
                return
            visited[x][y] = True
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
                        #print(f'{e[0]},{e[1]}')
                        return False

                # Add orthogonal cells to stack
                if e[0] - 1 >= 0: # cell above
                    if self.g[e[0] - 1][e[1]].col == colour:
                        stack.append((e[0] - 1, e[1]))
                if e[0] + 1 < self.height: # Cell below
                    if self.g[e[0] + 1][e[1]].col == colour:
                        stack.append((e[0] + 1, e[1]))
                if e[1] - 1 >= 0: # cell to the left
                    if self.g[e[0]][e[1] - 1].col == colour:
                        stack.append((e[0], e[1] - 1))
                if e[1] + 1 < self.width: # cell to the right
                    if self.g[e[0]][e[1] + 1].col == colour:
                        stack.append((e[0], e[1] + 1))
            return True

        for i in range(self.height):
            for j in range(self.width):
                if self.g[i][j].inf is not None and self.g[i][j].col == col:
                    if not dfs(i, j, number_of_symbols):
                        return False
        return True

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

    def _are_letters_sorted(self) -> bool:
        true_visited = []
        def dfs(x: int, y: int, letter: str):
            stack = [(x, y)]
            visited = []
            colour = self.g[x][y].col

            while stack:
                e = stack.pop(0)
                if e in visited:
                    continue
                visited.append(e)
                if self.g[e[0]][e[1]].col != colour:
                    continue
                true_visited.append(e)
                if "letter" in self.g[e[0]][e[1]].inf:
                    if self.g[e[0]][e[1]]["letter"] != letter:
                        return False

                # Add orthogonal cells to stack
                if e[0] - 1 >= 0: # cell above
                    new_e = (e[0] - 1, e[1])
                    if new_e not in visited:
                        stack.append(new_e)
                if e[0] + 1 < self.height: # Cell below
                    new_e = (e[0] + 1, e[1])
                    if new_e not in visited:
                        stack.append(new_e)
                if e[1] - 1 >= 0: # cell to the left
                    new_e = (e[0], e[1] - 1)
                    if new_e not in visited:
                        stack.append(new_e)
                if e[1] + 1 < self.width: # cell to the right
                    new_e = (e[0], e[1] + 1)
                    if new_e not in visited:
                        stack.append(new_e)

            return True

        letters_searched = []
        for i in range(self.height):
            for j in range(self.width):
                if "letter" in self.g[i][j].inf:
                    # If the letter has been searched already
                    if self.g[i][j]["letter"] in letters_searched:
                        if (i, j) not in true_visited:
                            return False
                        continue
                    # Now need to do a dfs from here
                    res = dfs(i, j, self.g[i][j]["letter"])
                    if not res:
                        return False
                    letters_searched.append(self.g[i][j]["letter"])
        return True

    def _test_rules(self) -> bool:
        for rule in self.rules:
            if rule.rule_type in [RuleEnum.MATCH_PATTERN, RuleEnum.MATCH_NOT_PATTERN]:
                if rule.rule_values['patterns'] is not None:
                    is_pattern_found = self._is_pattern_found( \
                        patterns = rule.rule_values["patterns"])
                else:
                    is_pattern_found = self._is_pattern_found( \
                        pattern = rule.rule_values["pattern"])
                if (rule.rule_type == RuleEnum.MATCH_PATTERN and not is_pattern_found) or \
                   (rule.rule_type == RuleEnum.MATCH_NOT_PATTERN and is_pattern_found):
                    return False
            elif rule.rule_type in [RuleEnum.AREA_NUMBER, RuleEnum.AREA_NUMBERS_ARE_ONE_OFF]:
                if not self._check_area_numbers(rule.rule_type != RuleEnum.AREA_NUMBER):
                    return False
            elif rule.rule_type == RuleEnum.CONNECT_CELLS:
                if not self._do_all_of_colour_connect(rule.rule_values["colour"]):
                    return False
            elif rule.rule_type == RuleEnum.N_CELLS_PER_REGION:
                num = rule.rule_values["number"]
                col = rule.rule_values["colour"]
                if not self._n_cells_per_region(num, col):
                    return False
            elif rule.rule_type == RuleEnum.N_SYMBOL_PER_COLOUR:
                if not self._n_symbols_per_colour_area(rule.rule_values["number"], \
                                rule.rule_values["colour"]):
                    return False
            elif rule.rule_type == RuleEnum.LETTER_SORTED:
                if not self._are_letters_sorted():
                    return False
        return True

    def _set_linked_cell(self, index: int, colour: Colour):
        pass

    def _solve(self, _cell_x = 0, _cell_y = 0, depth = 0) -> bool:
        """
        Provides a solution to the puzzle
        If returns True, all checks passed
        If returns False, invalid solution
        """
        self.attempts += 1
        if depth == 42:
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
            cells = []
            for ls in self.linked_cells:
                if ls[0] == (_cell_x,_cell_y):
                    cells = ls[1:]
            for colour in (Colour.WHITE,Colour.BLACK):
                self.g[_cell_x][_cell_y].col = colour
                if len(cells) > 0:
                    for c in cells:
                        self.g[c[0]][c[1]].col = colour
                if not self._test_rules():
                    continue
                if self._solve(new_cell_x, new_cell_y, depth + 1): # If a solution is found
                    return True
            self.g[_cell_x][_cell_y].col = Colour.EMPTY
        else:
            if self._solve(new_cell_x, new_cell_y, depth): # If a solution is found
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
    for r in logic_grid:
        print(r)
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

def your_function():
    print("hello world")
    return "hello world"
