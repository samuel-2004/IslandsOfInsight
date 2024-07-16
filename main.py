"""
Main file for this project
"""
from puzzle import *

if __name__ == "__main__":
    _ ="""
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
    """

    LG = interpret_lg([
    "WBEEBEEBB",
    "EEEEBEEEE",
    "EBEBEWEWE",
    "EBBBEWWWE",
    "EEBEEEWEE",
    "EEEEWEEEE",
    "WWEEWEEBB"
    ])

    black2x2 = create_solid_shape("black2x2")
    white2x2 = create_solid_shape("white2x2")

    rules = [
    Rule(RuleEnum.MATCH_NOT_PATTERN, pattern = black2x2),
    Rule(RuleEnum.MATCH_NOT_PATTERN, pattern = white2x2),
    #Rule(RuleEnum.N_SYMBOL_PER_COLOUR, number = 1, colour = Colour.WHITE),
    #Rule(RuleEnum.N_SYMBOL_PER_COLOUR, number = 1, colour = Colour.BLACK),
    Rule(RuleEnum.CONNECT_CELLS, colour = Colour.WHITE),
    Rule(RuleEnum.CONNECT_CELLS, colour = Colour.BLACK)
    ]
    for rule in rules:
        LG.add_rule(rule)
    """
    lc = [
        [(1,4),(1,5),(1,6),(2,6),(3,6)],
        [(2,2),(3,2)],
        [(2,4),(3,4),(4,4),(4,3)],
        [(4,6),(5,6),(6,6),(6,5),(6,4)],
        [(4,1),(5,1),(6,1),(6,2),(6,3)]
    ]
    for l in lc:
        LG.add_linked_cells(l)
    #"""
    emp = LG.num_empty()
    print(emp)
    print(2 ** emp)
    print(LG.height)
    print(LG.width)
    LG.solution()
    print('attempts =', LG.attempts)
