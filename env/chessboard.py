import pygame

WIDTH = 500
GRID_SIZE = 50
GRID_WIDTH = WIDTH // GRID_SIZE

# Color define
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)

# Global dictionary to store the scores
score_data = {
    "f_score": {},
    "g_score": {},
    "h_score": {}
}

'''
Node Class:

we define several builtin methods inside node class. 

attrs: x, y, color, neighbors.

methods: 

get_pos: return x, y

is_barrier: judge if node is a barrier

reset: init / reset node (let color be white)

make_*: make the node as *, the explicit option is setting the color to correspond color. 
colors params are defined globally.

draw: visualize the node block and draw f, h, g score respectively. 

update_neighbors: update a node
'''


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = WHITE
        self.neighbors = []

    def get_pos(self):
        return self.x, self.y

    def is_barrier(self):
        return self.color == BLACK

    def reset(self):
        self.color = WHITE

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = RED

    def make_end(self):
        self.color = BLUE

    def make_path(self):
        self.color = GREEN

    def make_open(self):
        self.color = YELLOW

    def make_closed(self):
        self.color = GREY

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        f_score = score_data["f_score"].get(self)
        g_score = score_data["g_score"].get(self)
        h_score = score_data["h_score"].get(self)

        if f_score is not None and g_score is not None and h_score is not None:
            font = pygame.font.Font(None, 16)
            f_text = font.render(f"f{f_score:.1f}", True, BLACK)
            g_text = font.render(f"g{g_score:.1f}", True, BLACK)
            h_text = font.render(f"h{h_score:.1f}", True, BLACK)
            win.blit(f_text, (self.x * GRID_SIZE + 2, self.y * GRID_SIZE + 2))  # top-left
            win.blit(g_text, (self.x * GRID_SIZE + 2, self.y * GRID_SIZE + GRID_SIZE - 14))  # bottom-left
            win.blit(h_text, (self.x * GRID_SIZE + GRID_SIZE - 23, self.y * GRID_SIZE + GRID_SIZE - 14))  # bottom-right

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.y > 0 and not grid[self.x][self.y - 1].is_barrier():  # 上
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.y < GRID_WIDTH - 1 and not grid[self.x][self.y + 1].is_barrier():  # 下
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.x > 0 and not grid[self.x - 1][self.y].is_barrier():  # 左
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.x < GRID_WIDTH - 1 and not grid[self.x + 1][self.y].is_barrier():  # 右
            self.neighbors.append(grid[self.x + 1][self.y])

        if self.x > 0 and self.y > 0 and not grid[self.x - 1][self.y - 1].is_barrier():  # 左上
            self.neighbors.append(grid[self.x - 1][self.y - 1])
        if self.x > 0 and self.y < GRID_WIDTH - 1 and not grid[self.x - 1][self.y + 1].is_barrier():  # 左下
            self.neighbors.append(grid[self.x - 1][self.y + 1])
        if self.x < GRID_WIDTH - 1 and self.y > 0 and not grid[self.x + 1][self.y - 1].is_barrier():  # 右上
            self.neighbors.append(grid[self.x + 1][self.y - 1])
        if self.x < GRID_WIDTH - 1 and self.y < GRID_WIDTH - 1 and not grid[self.x + 1][self.y + 1].is_barrier():  # 右下
            self.neighbors.append(grid[self.x + 1][self.y + 1])
