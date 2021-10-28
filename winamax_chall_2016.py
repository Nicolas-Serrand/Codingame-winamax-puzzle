import sys
import math

MAX_WIDTH = 1000
MAX_HEIGHT = 1000

#-------------------------------- Classes ---------------------------------------

class Ball:
    '''
    Ball class initialize with the number of strokes and its coordinates.
    '''
    def __init__(self, stroke, x, y):
        self.stroke = stroke
        self.x = x
        self.y = y

    def get_coord(self):
        return self.x, self.y

    def possible_stroke(self):
        '''
        return All the coordinates of the cases reachable in one stroke on the grid.
        The destination cases are on the grid and not water cases.
        '''
        pos = []
        if self.stroke > 0:
            if 0 <= self.x - self.stroke and GRID[self.x - self.stroke][self.y] != 'X':
                pos.append(Ball(self.stroke - 1, self.x - self.stroke, self.y))
            if 0 <= self.y - self.stroke and GRID[self.x][self.y - self.stroke] != 'X':
                pos.append(Ball(self.stroke - 1, self.x, self.y - self.stroke))
            if  self.x + self.stroke < height and GRID[self.x + self.stroke][self.y] != 'X':
                pos.append(Ball(self.stroke - 1, self.x + self.stroke, self.y))
            if  self.y + self.stroke < width and GRID[self.x][self.y + self.stroke] != 'X':
                pos.append(Ball(self.stroke - 1, self.x, self.y + self.stroke))
        return pos

    def inhole(self):
        '''
        Return if the ball is in a hole.
        '''
        return GRID[self.x][self.y] == 'H'

    def path_to(self, ball2):
        '''
        return all the cases between two balls include. The balls have to be in the same line.
        For example (0, 0) (4, 0) -> (0, 0), (1, 0) (2, 0) (3, 0) (4, 0)
        '''
        x2, y2 = ball2.get_coord()
        if self.x == x2:
            if self.y < y2:
                return [(self.x, y) for y in range(self.y, y2+1)]
            elif self.y > y2:
                return [(self.x, y) for y in range(self.y, y2-1, -1)]
        elif self.y == y2:
            if self.x < x2:
                return [(x, self.y) for x in range(self.x, x2+1)]
            elif self.x > x2:
                return [(x, self.y) for x in range(self.x, x2-1, -1)]
        else:
            raise ValueError

#-------------------------------- Functions ---------------------------------------

def find_paths(ball, path):
    """
    Find recursively all the paths which access to a hole with a given ball.
    Return a list of possible paths. So a list of lists of points.
    """
    if ball.inhole():
        return [path]
    else:
        res = []
        for coup in ball.possible_stroke():
            path_to = ball.path_to(coup)
            is_compatible =  True
            if not is_compatible_paths(path_to[1:], path):
                is_compatible = False
            if is_compatible:
                new_path = path + path_to[1:]
                result_paths = find_paths(coup, new_path)
                if result_paths:
                    res.extend(result_paths)
        return res

def is_compatible_paths(path1, path2):
    """
    Return if two paths cross.
    """
    for case1 in path1:
        for case2 in path2:
            if case1 == case2:
                return False
    return True          

def find_solution(balls, list_paths, solution):
    """
    Parameters:
    - balls: list of balls
    - list_paths: a dictionnary ball -> list of paths
    - solution: a dictionnary ball -> path
    Compute recursively a solution dictionnary in which each ball has a path which doesn't overlap with the other paths.
    """
    if len(balls) == 0:
        # We found a solution
        return True, solution
    ball = balls[0]
    for path in list_paths[ball]:
        is_compatible = True
        for ball2, sol in solution.items():
            if not is_compatible_paths(path, sol):
                is_compatible = False
        if is_compatible:
            new_solution = solution.copy()
            new_balls = balls[:]
            new_balls.remove(ball)
            new_solution[ball] = path
            is_ok, next_solution = find_solution(new_balls, list_paths, new_solution)
            if is_ok:
                next_solution[ball] = path
                return True, next_solution
    # The explored combination is not a solution
    return False, None 

#---------------------- Start of the process --------------------------------

width, height = [int(i) for i in input().split()]
GRID = []
balls = []

# Create the grid
for i in range(height):
    GRID.append(input())
    for j in range(width):
        if GRID[i][j].isdigit():
            balls.append(Ball(int(GRID[i][j]), i, j))

# For each ball compute all the possible paths.
list_paths = {ball:find_paths(ball, [ball.get_coord()]) for ball in balls}
# Use the above dictionnary to find a combination of paths which doesn't cross.
solution = find_solution(balls, list_paths, dict())[1]

# Write the solution paths on the grid
GRID = [['.' for _ in range(width)] for _ in range(height)]
for ball, path in solution.items():
    for c1, c2 in zip(path, path[1:]):
        if c1[0] < c2[0]:
            GRID[c1[0]][c1[1]] = 'v'
        elif c1[0] > c2[0]:
            GRID[c1[0]][c1[1]] = '^'
        elif c1[1] < c2[1]:
            GRID[c1[0]][c1[1]] = '>'
        elif c1[1] > c2[1]:
            GRID[c1[0]][c1[1]] = '<'

# Print the solution
for row in GRID:
    print("".join(row))