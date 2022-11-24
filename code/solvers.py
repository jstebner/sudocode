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

def get_row(n, r, c):
    return [(r,y) for y in range(n**2) if y != c]

def get_col(n, r, c):
    return [(x,c) for x in range(n**2) if x != r]

def get_grp(n, r, c):
    grp_idx = n*(r//n) + c//n
    idcs = [(n*(grp_idx//n)+(i//n),n*(grp_idx%n)+(i%n)) for i in range(n**2)]
    idcs.remove((r,c))
    return idcs

def get_adj(n,r,c):
    return list(set(
        get_row(n,r,c) + get_col(n,r,c) + get_grp(n,r,c)
    ))


# TODO: this guy
def solve_CP(grid: list[list[int]], n: int) -> list[list[int]]:
    if any([0 in row for row in grid]):
        for r in range(n**2):
            for c in range(n**2):
                if grid[r][c] != 0:
                    continue
                states = set()
                for sym in range(1, 1+n**2):
                    if is_possible(grid, n, r, c, sym):
                        states.add(sym)
                grid[r][c] = states
    updates = 1
    while updates > 0:
        updates = 0
        for r in range(n**2):
            for c in range(n**2):
                if type(grid[r][c]) != set:
                    continue
                if len(grid[r][c]) == 0:
                    return
                
                match len(grid[r][c]):
                    case 1: # singleton collapse
                        grid[r][c] = grid[r][c].pop()
                        for y,x in get_adj(n,r,c):
                            if type(grid[y][x]) == set:
                                grid[y][x] -= grid[r][c]
                                updates += 1
                        continue
                    
                    case 2 | 3: # polyzygotic propagation (can be >3)
                        size = len(grid[r][c])
                        for get_subset in [get_row, get_col, get_grp]:
                            subset = get_subset(n,r,c)
                            count = 1
                            for y,x in subset: # check for polyzygotes
                                if grid[r][c] == grid[y][x]:
                                    count += 1
                            if count < size: # not enough for implication
                                continue
                            elif count > size: # invalid assumption
                                return
                            
                            for y,x in subset:
                                if grid[y][x] != grid[r][c]:
                                    grid[y][x] -= grid[r][c]
                                    updates += 1
                    # more propagation checks can be added in series here
                
                # elimination collapse
                    
                
                    
    
if __name__ =='__main__':
    n = 4
    k = 64
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