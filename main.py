from collections import deque
class PathNode:
    def __init__(self, data: tuple, parent: tuple):
        self.data = data
        self.parent = parent

def generate_grid(n=10):
    return [[0 for _ in range(n)] for _ in range(n)]

def place_obstacle(grid: list, x:int, y:int):
    grid[x][y] = -1

def remove_obstacle(grid: list, x:int, y:int):
    grid[x][y] = 0

check = []
def bfs_find_target(grid, source, target):
    visited = set()
    global check
    queue = [PathNode(source, None)]
    
    N = len(grid)
    
    is_out_of_bounds = lambda a,b: (a<0 or b<0 or a>=N or b>=N)

    while queue:
        current = queue.pop(0)

        if current.data in visited:
            continue

        visited.add(current.data)

        x, y = current.data

        if grid[x][y] == -1:
            # It's an obstacle and can't be part of a path
            tup = (x, y)
            check.append(tup)
            continue

        if (x,y) == target:
            return current

        # left, right, bottom and top
        frontier = ((x-1, y),(x+1, y), (x, y+1), (x, y-1))
        # filter out invalid frontiers, that fall out of the grid
        frontier = [PathNode((a,b), current) for (a,b) in frontier if not is_out_of_bounds(a,b)]

        queue += frontier

    return None

def trace_path(path_node: PathNode):
    path = []
    while path_node is not None:
        path.append(path_node.data)
        x,y = path_node.data
        path_node = path_node.parent
    return path[::-1]
grid = [[0]*10]*10

def random_obstacles(grid, src, dest):
    from random import randint
    N = len(grid)

    sample_space = [(x,y) for x in range(N) for y in range(N) if (x,y) not in (src,dest) and grid[x][y]!=-1]
    
    print(len(sample_space))
    n = N-1
    
    for _ in range(20):
        i = randint(0, n)
        x,y = sample_space.pop(i)
        place_obstacle(grid, x, y)
    
def shortestPath(grid: list, k: int):
    row, col = len(grid), len(grid[0])
    # use FIFO queue to store (step, x, y, reminding obstacles ellimination)
    q = deque([(0, 0, 0, k)])
    # use seen to store optimal reminding ellimination at certain place
    seen = {(0, 0): k}
    ans = []
    while q:
        step, x, y, k = q.popleft()
        if (x, y) == (row-1, col-1):
            return step
        for nxt_x, nxt_y in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            if not (0 <= nxt_x < row and 0 <= nxt_y < col):
                continue
            nxt_k = k-grid[nxt_x][nxt_y]
            if nxt_k >= 0 and ((nxt_x, nxt_y) not in seen or nxt_k > seen[(nxt_x, nxt_y)]):
                q.append((step+1, nxt_x, nxt_y, k-grid[nxt_x][nxt_y]))
                seen[(nxt_x, nxt_y)] = nxt_k
    return -1

grid = generate_grid()

for p in ((9,7), (8,7), (6,7), (6,8)):
    place_obstacle(grid, *p)

random_obstacles(grid, (0,0), (9,9))

t = bfs_find_target(grid, (0,0), (9,9))
if t:
	print(len(trace_path(t)))
	print(trace_path(t))
else:
    print("Unable to reach destination")
    print("Remove obstacles:" )
    print(check[::-1])
    print(shortestPath(grid, len(check[::-1])))
