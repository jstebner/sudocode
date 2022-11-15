from utils import *

def is_possible(grid: list[list[int]], n:int, r: int, c: int, val: int) -> bool:
    return not any([
        val in grid[r],
        val in [grid[i][c] for i in range(n**2)],
        val in [grid[n*((n*(r//n) + c//n)//n)+i//n][n*(((n*(r//n) + c//n))%n)+(i%n)] for i in range(n**2)]
    ])
    

def filled(grid: list[list[int]]) -> bool:
    return not any(
        ele == 0 or type(ele) == set for row in grid for ele in row
    )


def solve_BT(grid: list[list[int]], n: int) -> list[list[int]]:
    for r in range(n**2):
        for c in range(n**2):
            if grid[r][c] != 0:
                continue
            for num in range(1,1+n**2):
                if is_possible(grid, n, r, c, num):
                    grid[r][c] = num
                    solve_BT(grid, n)
                    if not filled(grid):
                        grid[r][c] = 0
            return


def solve_CP(grid: list[list[int]], n: int) -> list[list[int]]:
    pass

if __name__ =='__main__':
    n = 6
    k = 200
    pzl, sln = make_puzzle(n, k)
    maybe_sln = matrixify(pzl)
    print('PUZZLE:')
    pretty_print(matrixify(pzl))
    print('SOLUTION:')
    pretty_print(matrixify(sln))

    
    solve_BT(maybe_sln, n)
    
    print("MAYBE?:")
    pretty_print(maybe_sln)
    print()
    
    print("is good tho" if valid(maybe_sln) else "YO WTF")
    print(stringify(maybe_sln))
    print(sln)
    print("POGGERS" if stringify(maybe_sln)==sln else "NOOOOOOOOOO")