import argparse

from utils import *


# Set window size and grid size

def parse_arguments():
    parser = argparse.ArgumentParser(description="A* Pathfinding Visualization")
    parser.add_argument('-t', '--task', type=int, default=2, help="Task to execute (1 or 2)")
    args = parser.parse_args()
    return args


def main(win, task):
    grid = make_grid()

    start = None
    end = None

    run = True
    clock = pygame.time.Clock()
    FPS = 60  # Set FPS

    while run:
        clock.tick(FPS)  # 每秒最多显示 FPS 次帧
        draw_window(win, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if task == 2:
                start = grid[0][0]
                start.make_start()
                end = grid[8][6]
                end.make_end()
                barrier_positions = [(0, 1), (0, 9), (2, 3), (2, 7), (2, 9), (3, 1), (4, 5), (5, 2), (6, 3), (6, 7),
                                     (8, 1), (8, 3), (8, 9)]
                for x, y in barrier_positions:
                    grid[x][y].make_barrier()

            elif task == 1:
                if pygame.mouse.get_pressed()[0]:  # 左键
                    pos = pygame.mouse.get_pos()
                    x, y = get_clicked_pos(pos)
                    node = grid[x][y]
                    if not start and node != end:
                        start = node
                        start.make_start()

                    elif not end and node != start:
                        end = node
                        end.make_end()

                    elif node != start and node != end:
                        node.make_barrier()

            if event.type == pygame.KEYDOWN:
                # press space to start A star algorithm
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    a_star(lambda: draw_window(win, grid), grid, start, end)

                # press C to clear. C stands for 宸哥
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid()

    pygame.quit()


if __name__ == '__main__':
    args = parse_arguments()
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("A* Pathfinding Visualization")
    main(win, args.task)
