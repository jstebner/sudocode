from utils import *
from time import process_time_ns


def is_possible(grid: list[list[int]], n:int, r: int, c: int, val: int) -> bool:
    return not any([
        val in grid[r],
        val in [grid[i][c] for i in range(n**2)],
        val in [grid[n*((n*(r//n) + c//n)//n)+i//n][n*(((n*(r//n) + c//n))%n)+(i%n)] for i in range(n**2)]
    ])


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
    
    
def solve(method: str, grid: list[list[int]]):
    def solve_BT(grid: list[list[int]], n: int) -> list[list[int]]:
        nonlocal rec_calls
        for r in range(n**2):
            for c in range(n**2):
                if grid[r][c] != 0:
                    continue
                for num in range(1,1+n**2):
                    if is_possible(grid, n, r, c, num):
                        grid[r][c] = num
                        rec_calls += 1
                        solve_BT(grid, n)
                        if not filled(grid):
                            grid[r][c] = 0
                return

    def solve_CP(grid: list[list[int]], n: int) -> list[list[int]]: # DEBUG: this sometimes doesnt solve pzls
        nonlocal rec_calls
        if any([0 in row for row in grid]): # create state spaces 
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
        while updates > 0: # prune search space
            updates = 0
            for r in range(n**2):
                for c in range(n**2):
                    if type(grid[r][c]) != set:
                        continue
                    if len(grid[r][c]) == 0:
                        return
                    
                    match len(grid[r][c]):
                        case 1: # singleton collapse
                            for y,x in get_adj(n,r,c): # propagate change
                                if type(grid[y][x]) == set:
                                    grid[y][x] -= grid[r][c]
                            updates += 1
                            grid[r][c] = grid[r][c].pop()
                            continue
                        
                        case 2 | 3: # polyzygotic propagation (can be >3 but eh)
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
                                    if type(grid[y][x]) == set and grid[y][x] != grid[r][c] and len(grid[r][c].intersection(grid[y][x])):
                                        grid[y][x] -= grid[r][c]
                                        updates += 1
                    # more propagation checks can be added in series here
                    
                    for symbol in grid[r][c]: # elimination collapse
                        for get_subset in [get_row, get_col, get_grp]:
                            subset = get_subset(n,r,c)
                            for y,x in subset: # check for single instance
                                if type(grid[y][x]) == set and symbol in grid[y][x]:
                                    break
                            else: # only runs if no instance of symbol is found
                                grid[r][c] = {symbol}
                                for y,x in get_adj(n,r,c): # propagate change
                                    if type(grid[y][x]) == set:
                                        grid[y][x] -= grid[r][c]
                                updates += 1
                                grid[r][c] = symbol
                                break
                        else: # antipattern i use way too much for scuffed control flow
                            continue
                        break
            # print()
        # backtrack
        r_min, c_min = None, None
        for r in range(n**2):
            for c in range(n**2):
                if type(grid[r][c]) != set:
                    continue
                if [r_min, c_min] == [None, None]:
                    r_min, c_min = r, c
                elif len(grid[r][c]) < len(grid[r_min][c_min]):
                    r_min, c_min = r, c
        if [r_min, c_min] != [None, None]: # DEBUG: after a reset, the program does a weird thing with pointers and idk why
            backup = deepcopy(grid)
            for symbol in grid[r_min][c_min]:
                print(f'guessing {symbol} for ({r_min},{c_min})')
                for y,x in get_adj(n,r_min,c_min):
                    if type(grid[y][x]) == set:
                        grid[y][x] -= {symbol}
                grid[r_min][c_min] = symbol
                rec_calls += 1
                solve_CP(grid, n)
                print(f'finished guess {symbol} for ({r_min}, {c_min})')
                if not valid(grid):
                    grid = backup
                    print('guess no good, updating board')
                    pretty_print(grid)
                else:
                    print("ebic!")
                    return
        
    n = int(len(grid)**0.5)
    solve_function = {'bt':solve_BT, 'cp':solve_CP}[method.lower()]
    rec_calls = 0
    start = process_time_ns()
    solve_function(grid, n)
    end = process_time_ns()
    
    return end-start, rec_calls
                             
    
if __name__ =='__main__':
    # n = 3
    # k = 60
    # pzl, sln = make_puzzle(n, k)


    # maybe_sln = matrixify(pzl)
    # rec_calls = 0
    # time, recs = solve('cp', maybe_sln)
    
    # pretty_print(maybe_sln)
    
    # print(f"valid: {valid(maybe_sln)}")
    # if not valid(maybe_sln):
    #     print(pzl)


    # for mthd in ['bt', 'cp']:
    #     maybe_sln = matrixify(pzl)
    #     rec_calls = 0
    #     time, recs = solve(mthd, maybe_sln)
        
    #     print(mthd)
    #     print("  valid" if valid(maybe_sln) else "  invalid")
    #     print("  matches sol" if stringify(maybe_sln)==sln else "  dont match sol")
    #     print(f'  {round(time*10e-9, 4)} s, {recs} calls')
    #     if not valid(maybe_sln):
    #         print(pzl)
    #         pretty_print(maybe_sln)
    
    pzl = '0 8 0 0 2 0 0 0 0 0 6 0 0 0 9 0 0 0 9 0 0 0 0 8 3 1 0 2 3 0 0 0 0 0 0 0 4 0 0 0 5 0 0 0 0 0 0 9 0 0 0 5 4 0 0 0 0 0 3 7 1 0 0 0 0 0 0 8 4 0 0 0 0 0 0 6 0 0 0 0 0'
    
    maybe_sln = matrixify(pzl)
    time, recs = solve("cp", maybe_sln)
    
    pretty_print(maybe_sln)
    print(valid(maybe_sln))