import random
import copy

# TODO: this one
def check_board(grid: list[list[int]]) -> bool:
    """
    Checks if the input solution to a sudoku is valid

    :param grid:    2D matrix of completed sudoku solution
    :rtype:         boolean
    :return:        if the sudoku is valid
    """

    n = int(len(grid)**0.5)
    symbols = {i for i in range(1, 1+n**2)}
    for i in range(n**2):
        if any(
            {grid[i][j] for j in range(n**2)} != symbols,
            {grid[j][i] for j in range(n**2)} != symbols,
            {grid[n*(i//n)+j//n][n*(i%n)+(j%n)] for j in range(n**2)} != symbols
        ):
            return False
    return True
    

# TODO: this one too
def make_puzzle(n: int, k: int) -> tuple[str, str]:
    """
    Returns a tuple of puzzle and solution of space-separated 
    row-wise repr of square sudoku puzzle of order N and K removed symbols.

    :param n:   order of square puzzle
    :param k:   number of removed symbols
    :rtype:     tuple[string, string]
    :return:    tuple of puzzle and solution of space-separated row-wise 
                repr of sudoku puzzle
    """

    
    # backtrack fill remaining 0s
    def is_possible(r: int, c: int, val: int) -> bool:
        return not any([
            val in solution[r],
            val in [solution[i][c] for i in range(n**2)],
            val in [solution[n*((n*(r//n) + c//n)//n)+i//n][n*(((n*(r//n) + c//n))%n)+(i%n)] for i in range(n**2)]
        ])

    count = 0
    # DEBUG: it solves it but at the end it resets all the hints :(
    def solve():
        nonlocal solution
        for r in range(n**2):
            for c in range(n**2):
                if solution[r][c] != 0:
                    continue
                for num in range(1,1+n**2):
                    if is_possible(r, c, num):
                        solution[r][c] = num
                        solve()
                        solution[r][c] = 0
                return

    # create n**2 x n**2 grid of 0s
    solution = [[0 for _ in range(n**2)] for _ in range(n**2)]
    while any([0 in row for row in solution]):
        # fill in n groups along diagonal
        for group in range(n):
            subgrid = list(range(1, 1+n**2))
            random.shuffle(subgrid)
            for i, val in enumerate(subgrid):
                solution[group*n + i//n][group*n + i%n] = val
        solve()

    puzzle = solution.copy()
    # remove k symbols randomly

    return stringify(puzzle), stringify(solution)


def pretty_print(grid: list[list[int]]) -> None:
    """
    Prints a matrix but pretty

    :param matrix:  2D array of integers
    :rtype:         void
    :return:        None
    """
    matrix = copy.deepcopy(grid)
    n_sqr = len(matrix)
    max_len = 0
    for r in range(n_sqr):
        for c in range(n_sqr):
            matrix[r][c] = str(matrix[r][c])
            max_len = max(len(matrix[r][c]), max_len)
    print("\n".join(" ".join([val.rjust(max_len) for val in row]) for row in matrix))


def stringify(grid: list[list[int]]) -> str:
    """
    Converts a 2D grid of a square sudoku puzzle and converts it
    to a space-separated row-wise repr of the same puzzle

    :param grid:    2D grid of ints
    :rtype:         string
    :return:        space-separated row-wise repr of input puzzle
    """
    
    return " ".join([" ".join(list(map(str, row))) for row in grid])


def matrixify(flat: str) -> list[list[int]]:
    """
    Converts a space-separated row-wise repr of a square sudoku puzzle 
    to a 2D grid of ints repring the same puzzle

    :param flat:    space-separated row-wise repr of sudoku
    :rtype:         list[list[int]]
    :return:        2D grid of ints repring input puzzle
    """
    flat = list(map(int, flat.split()))
    n = int(len(flat)**(1/4))
    return [[flat[i*n**2 + j] for j in range(n**2)] for i in range(n**2)]


if __name__ == '__main__':
    pzl, sln = make_puzzle(2, 0)
    # print(pzl)
    pretty_print(matrixify(sln))