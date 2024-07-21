"""
Main file for this project
"""
from puzzle import *

if __name__ == "__main__":
    g = [
        ["G","G","B","G","0","0"],
        ["G","P","B","G","B","B"],
        ["P","G","G","B","#","#"],
        ["G","G","P","B","#","#"],
    ]

    m = Match3(g)
    print(m.generate_moves())
    m.solution()
