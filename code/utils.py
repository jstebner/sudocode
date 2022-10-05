import random

# TODO: this one
def is_valid(grid: list[list[int]]) -> bool:
    """
    Checks if the input solution to a sudoku is valid

    :param grid:    2D matrix of completed sudoku solution
    :type grid:     list[list[int]]
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
    :type n:    int
    :param k:   number of removed symbols
    :type k:    int
    :rtype:     tuple[string, string]
    :return:    tuple of puzzle and solution of space-separated row-wise 
                repr of sudoku puzzle
    """

    # create n**2 x n**2 grid of 0s
    solution = [[0 for _ in range(n**2)] for _ in range(n**2)]
    
    # fill in n groups along diagonal
    for group in range(n):
        subgrid = list(range(1, 1+n**2))
        random.shuffle(subgrid)
        for i, val in enumerate(subgrid):
            solution[group*n + i//n][group*n + i%n] = val
    
    # backtrack fill remaining 0s
    
    puzzle = solution.copy()

    # remove k symbols randomly

    return stringify(puzzle), stringify(solution)


def pretty_print(matrix: list[list[int]]) -> None:
    """
    Prints a matrix but pretty

    :param matrix:  2D array of integers
    :type matrix:   list[list[int]]
    :rtype:         void
    :return:        None
    """

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
    :type grid:     list[list[int]]
    :rtype:         string
    :return:        space-separated row-wise repr of input puzzle
    """
    
    return " ".join([" ".join(list(map(str, row))) for row in grid])


def matrixify(flat: str) -> list[list[int]]:
    """
    Converts a space-separated row-wise repr of a square sudoku puzzle 
    to a 2D grid of ints repring the same puzzle

    :param flat:    space-separated row-wise repr of sudoku
    :type flat:     string
    :rtype:         list[list[int]]
    :return:        2D grid of ints repring input puzzle
    """
    flat = list(map(int, flat.split()))
    n = int(len(flat)**(1/4))
    return [[flat[i*n**2 + j] for j in range(n**2)] for i in range(n**2)]


if __name__ == '__main__':
    pzl, sln = make_puzzle(3, 0)
    # print(pzl)
    pretty_print(matrixify(sln))