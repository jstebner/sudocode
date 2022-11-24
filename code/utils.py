from random import shuffle
from copy import deepcopy

def valid(grid: list[list[int]]) -> bool:
    if not filled(grid):
        return False

    n = int(len(grid)**0.5)
    symbols = set(range(1, 1+n**2))
    for i in range(n**2):
        if any([
            {grid[i][j] for j in range(n**2)} != symbols,
            {grid[j][i] for j in range(n**2)} != symbols,
            {grid[n*(i//n)+j//n][n*(i%n)+(j%n)] for j in range(n**2)} != symbols
        ]):
            return False
    return True


def filled(grid: list[list[int]]) -> bool:
    return not any(
        ele == 0 or type(ele) == set for row in grid for ele in row
    )
    
def make_puzzle(n: int, k: int) -> tuple[str, str]:
    range_n_sqr = range(n**2)
    
    def is_possible(r: int, c: int, val: int) -> bool:
        grp_idx = n*(r//n) + c//n
        return not any([
            val in solution[r],
            val in [solution[i][c] for i in range_n_sqr],
            val in [solution[n*(grp_idx//n)+(i//n)][n*(grp_idx%n)+(i%n)] for i in range_n_sqr] # TODO: this dude slow as hell
        ])

    def solve(grid: list[list[int]]) -> list[list[int]]:
        nonlocal rec_calls
        # if rec_calls > 1000000:
        #     return
        for r in range(n**2):
            for c in range(n**2):
                if grid[r][c] != 0:
                    continue
                for num in range(1,1+n**2):
                    if is_possible(r, c, num):
                        grid[r][c] = num
                        rec_calls += 1
                        solve(grid)
                        if not filled(grid):
                            grid[r][c] = 0
                return
            

    # create n**2 x n**2 grid of 0s
    solution = [[0 for _ in range(n**2)] for _ in range(n**2)]
    while not valid(solution):
        # fill in n groups along diagonal
        for group in range(n):
            subgrid = list(range(1, 1+n**2))
            shuffle(subgrid)
            for i, val in enumerate(subgrid):
                solution[group*n + i//n][group*n + i%n] = val
        # pretty_print((solution))
        rec_calls = 0
        solve(solution)
    print(rec_calls)

    # remove k symbols randomly
    puzzle = deepcopy(solution)
    rmv_idxs = list(range(0, n**4))
    shuffle(rmv_idxs)
    rmv_idxs = [(idx//n**2, idx%n**2) for idx in rmv_idxs[:k]]
    for x, y in rmv_idxs:
        puzzle[x][y] = 0

    return stringify(puzzle), stringify(solution)


def pretty_print(grid: list[list[int]]) -> None:
    matrix = deepcopy(grid)
    n_sqr = len(matrix)
    max_len = 0
    for r in range(n_sqr):
        for c in range(n_sqr):
            matrix[r][c] = str(matrix[r][c])
            max_len = max(len(matrix[r][c]), max_len)
    print("\n".join(" ".join([val.rjust(max_len) if val != '0' else ' '*max_len for val in row]) for row in matrix))


def stringify(grid: list[list[int]]) -> str:
    return " ".join([" ".join(list(map(str, row))) for row in grid])


def matrixify(flat: str) -> list[list[int]]:
    flat = list(map(int, flat.split()))
    n = int(len(flat)**(1/4))
    return [[flat[i*n**2 + j] for j in range(n**2)] for i in range(n**2)]


if __name__ == '__main__':
    pzl, sln = make_puzzle(3, 64)
    # print(pzl)
    # print(sln)
    # pretty_print(matrixify(sln))
    # print(pzl)
    pretty_print(matrixify(pzl))