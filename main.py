# Code by Adrien TIMBERT @ github.com/aleolux
import os
import sys
import algorithms
from grid import *
from ui import *
from maze import make_maze


def resource_path(relative_path):
    """
    This function is later used for the .exe build
    https://stackoverflow.com/questions/54210392/how-can-i-convert-pygame-to-exe
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def main():
    """Main program"""
    pygame.init()
    pygame.display.set_caption("Python Path Finder Visualizer")
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # load screen

    # load images
    title = Image(GRID_OFFSET_X, 15, pygame.image.load(resource_path("assets/title.png")).convert_alpha(), 0.4)  # load title
    x_start, y_start, scale, space = GRID_OFFSET_X + 50, WINDOW_HEIGHT - 100, 0.55, 150  # load legend images
    legend_open = Image(x_start, y_start, pygame.image.load(resource_path("assets/open.png")).convert_alpha(), 0.55)
    legend_close = Image(x_start + space, y_start, pygame.image.load(resource_path("assets/visited.png")).convert_alpha(), scale)
    legend_path = Image(x_start + space * 2, y_start, pygame.image.load(resource_path("assets/path.png")).convert_alpha(), scale)
    legend_wall = Image(x_start + space * 3, y_start, pygame.image.load(resource_path("assets/wall.png")).convert_alpha(), scale)
    legend_start = Image(x_start + space * 4, y_start, pygame.image.load(resource_path("assets/start.png")).convert_alpha(), scale)
    legend_end = Image(x_start + space * 5, y_start, pygame.image.load(resource_path("assets/end.png")).convert_alpha(), scale)
    images = [title, legend_open, legend_close, legend_wall, legend_path, legend_start, legend_end]

    # load button images
    start_button = Button(GRID_OFFSET_X + 550, 95, pygame.image.load(resource_path("assets/solve.png")).convert_alpha(), 0.65)
    reset_button = Button(GRID_OFFSET_X + 750, 100, pygame.image.load(resource_path("assets/reset.png")).convert_alpha(), 0.5)
    reset_2_button = Button(GRID_OFFSET_X + 750, 60, pygame.image.load(resource_path("assets/reset_2.png")).convert_alpha(), 0.5)
    clean_button = Button(GRID_OFFSET_X + 750, 140, pygame.image.load(resource_path("assets/clean.png")).convert_alpha(), 0.5)
    walls_button = Button(GRID_OFFSET_X + 200, 100, pygame.image.load(resource_path("assets/walls.png")).convert_alpha(), 0.55)
    clean_walls_button = Button(GRID_OFFSET_X + 400, 100, pygame.image.load(resource_path("assets/clean_walls.png")).convert_alpha(),
                                0.55)
    maze_button = Button(GRID_OFFSET_X + 300, 100, pygame.image.load(resource_path("assets/maze.png")).convert_alpha(), 0.55)
    buttons = [start_button, reset_button, reset_2_button, clean_button, walls_button, clean_walls_button, maze_button]

    # load checkboxes
    boxes = [Checkbox(screen, GRID_OFFSET_X, 80, 0, caption="A* algorithm"),
             Checkbox(screen, GRID_OFFSET_X, 100, 1, caption="Breadth-first search"),
             Checkbox(screen, GRID_OFFSET_X, 120, 2, caption="Depth-first search")]
    boxes[0].checked = True

    # grid generation
    grid = generate_grid()
    start, end = reset_start_end(grid)
    set_start, set_end = False, False

    run = True
    while run:  # main loop
        clock.tick(40)
        event_list = pygame.event.get()

        screen.fill(WHITESMOKE)

        for img in images:
            img.draw(screen)

        for box in boxes:
            box.render_checkbox()

        for button in buttons:
            button.draw(screen)

        if start_button.clicked and not (set_start or set_end):  # on start button click
            clean(grid)
            path = []
            if boxes[0].checked:
                path = algorithms.a_star(start, end, grid, False, lambda: draw(grid, screen))
            elif boxes[1].checked:
                path = algorithms.bfs(start, end, grid, lambda: draw(grid, screen))
            elif boxes[2].checked:
                path = algorithms.dfs_iterative(start, end, grid, lambda: draw(grid, screen))
            if path is None or len(path) <= 0:
                print(">>> NO SOLUTION!")

        if reset_button.clicked:  # on reset button click
            reset_grid(grid)
            start, end = reset_start_end(grid, start, end)

        if clean_button.clicked:  # on clean button click
            clean(grid)

        if reset_2_button.clicked:  # on clean start end button click
            start, end = reset_start_end(grid, start, end)

        if clean_walls_button.clicked:  # on clean walls button click
            clean_walls(grid)

        if walls_button.clicked:  # on random walls button click
            clean(grid)
            clean_walls(grid)
            build_random_walls(grid)

        if maze_button.clicked:  # on build maze button click
            clean(grid)
            clean_walls(grid)
            make_maze(grid, lambda: draw(grid, screen))

        for event in event_list:  # event handler
            if event.type == pygame.QUIT:  # on quit
                run = False

            if pygame.mouse.get_pressed()[0]:  # on left click
                pos = pygame.mouse.get_pos()

                for box in boxes:  # on checkbox click
                    box.update_checkbox(event)
                    if box.checked is True:
                        for b in boxes:
                            if b != box:
                                b.checked = False

                if is_cursor_in_grid_area(pos):  # on spot click
                    x, y = spot_coordinates_from_cursor_position(pos)

                    if set_start and (x, y) != end.get_pos():  # set start
                        start = grid[x][y]
                        start.make_start()
                        set_start = False

                    elif set_end and (x, y) != start.get_pos():  # set end
                        end = grid[x][y]
                        end.make_end()
                        set_end = False

                    else:
                        if (x, y) == start.get_pos():  # del start
                            start.make_blank()
                            set_start = True

                        elif (x, y) == end.get_pos():  # del end
                            end.make_blank()
                            set_end = True

                        else:  # build walls
                            grid[x][y].make_wall()

        draw(grid, screen)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
