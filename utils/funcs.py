import math
from queue import PriorityQueue

from env import *


'''
There are several functions. 

h is heuristic function, which calc the estimate cost from temp pos to destiny.

reconstruct_path visualize the path node.

a_star search for the path to destiny. note that if there are more than one optimal path, the a_star algorithm will only
give out one of them.

make grid, draw_* draw the env. 

get_clicked_pos get the mouse pos, the pos is a tuple of discrete int, which means the scales of x, y location.
'''

# Heuristic func
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    # return abs(x1 - x2) + abs(y1 - y2)


# reconstruct path
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
        pygame.display.update()


# A*
def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    clock = pygame.time.Clock()
    FPS = 10  # FPS

    while not open_set.empty():
        clock.tick(FPS)  # FPS set
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, current, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if current.x != neighbor.x and current.y != neighbor.y:
                temp_g_score = g_score[current] + math.sqrt(2)
            else:
                temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                    draw()  # Add this line
                    pygame.display.update()
                    score_data["f_score"][neighbor] = f_score[neighbor]
                    score_data["g_score"][neighbor] = g_score[neighbor]
                    score_data["h_score"][neighbor] = h(neighbor.get_pos(), end.get_pos())

        draw()

        if current != start:
            current.make_closed()

    return False


# 宸哥出品，必属精品


# make grid
def make_grid():
    grid = []
    for i in range(GRID_WIDTH):
        grid.append([])
        for j in range(GRID_WIDTH):
            node = Node(i, j)
            grid[i].append(node)
    return grid


# Draw grid
def draw_grid(win):
    for i in range(GRID_WIDTH):
        pygame.draw.line(win, BLACK, (0, i * GRID_SIZE), (WIDTH, i * GRID_SIZE))
        pygame.draw.line(win, BLACK, (i * GRID_SIZE, 0), (i * GRID_SIZE, WIDTH))


# Draw window
def draw_window(win, grid):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win)
    pygame.display.update()


# Set env with mouse click
def get_clicked_pos(pos):
    x, y = pos
    return x // GRID_SIZE, y // GRID_SIZE
