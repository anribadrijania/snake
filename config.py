import random
import pygame

class GameConfig:
    def __init__(self, grid_size, time_limit, difficulty, seed):
        self.grid_size = grid_size
        self.time_limit = time_limit
        self.difficulty = difficulty
        self.seed = seed

def show_menu():
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Snake vs AI - Menu")
    font = pygame.font.SysFont(None, 36)

    grid_sizes = {"Small": (10, 10), "Medium": (20, 20), "Big": (30, 30)}
    grid_keys = list(grid_sizes.keys())
    grid_index = 1

    time_limits = ["1:00", "2:00", "5:00", "No Limit"]
    time_index = 1

    difficulties = ["Easy", "Hard", "Impossible"]
    difficulty_index = 1

    selected = False
    while not selected:
        screen.fill((40, 40, 40))

        def draw_option(label, options, index, y_pos):
            text = f"{label}: {options[index]}"
            txt_surface = font.render(text, True, (255, 255, 255))
            screen.blit(txt_surface, (100, y_pos))
            return pygame.Rect(100, y_pos, 400, 40)

        grid_rect = draw_option("Grid Size", grid_keys, grid_index, 80)
        time_rect = draw_option("Time Limit", time_limits, time_index, 140)
        diff_rect = draw_option("Difficulty", difficulties, difficulty_index, 200)

        start_button = pygame.Rect(200, 280, 200, 50)
        pygame.draw.rect(screen, (0, 150, 0), start_button)
        start_text = font.render("Start Game", True, (255, 255, 255))
        screen.blit(start_text, (start_button.x + 30, start_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if grid_rect.collidepoint(event.pos):
                    grid_index = (grid_index + 1) % len(grid_keys)
                elif time_rect.collidepoint(event.pos):
                    time_index = (time_index + 1) % len(time_limits)
                elif diff_rect.collidepoint(event.pos):
                    difficulty_index = (difficulty_index + 1) % len(difficulties)
                elif start_button.collidepoint(event.pos):
                    if difficulties[difficulty_index].lower() == "impossible":
                        # Show the "Coming Soon" message
                        coming_soon_text = font.render("Impossible Mode: Coming Soon!", True, (255, 100, 100))
                        screen.blit(coming_soon_text, (100, 340))
                        pygame.display.flip()
                        pygame.time.delay(2000)
                    else:
                        selected = True

    # Parse time
    time_limit = None
    if time_limits[time_index] != "No Limit":
        minutes, seconds = map(int, time_limits[time_index].split(":"))
        time_limit = (minutes, seconds)

    return GameConfig(
        grid_size=grid_sizes[grid_keys[grid_index]],
        time_limit=time_limit,
        difficulty=difficulties[difficulty_index].lower(),
        seed=random.randint(0, 1000000)
    )
