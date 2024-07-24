"""
Main file for this project
"""
from puzzle import *

if __name__ == "__main__":
    g = interpret_lg([
        "GGGGGBG",
        "WGGGGGG",
        "GGGGGGG",
        "GGGWGGG",
        "GGGGGGG",
        "GGGGGGB",
        "GWGGGGG"
    ])
    print(type(g))
    m = LogicGrid(g)
    print(str(m))
    m.g[0][0].set_info({"letter": "A"})
    m.g[0][6].set_info({"letter": "A"})
    m.g[1][1].set_info({"letter": "B"})
    m.g[1][5].set_info({"letter": "B"})
    m.g[2][2].set_info({"letter": "C"})
    m.g[2][4].set_info({"letter": "C"})
    m.g[4][2].set_info({"letter": "A"})
    m.g[4][4].set_info({"letter": "C"})
    m.g[5][1].set_info({"letter": "B"})
    m.g[5][5].set_info({"letter": "B"})
    m.g[6][0].set_info({"letter": "C"})
    m.g[6][6].set_info({"letter": "A"})
    m.add_rule(Rule(RuleEnum.LETTER_SORTED))
    m.solution()
