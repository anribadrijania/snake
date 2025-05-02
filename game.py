import pygame
import random
from snake import Snake
from ai import easy_ai_move, hard_ai_move, generate_hamiltonian_cycle
from utils import seeded_random_food, resource_path
import time

pygame.mixer.init()
eat_sound = pygame.mixer.Sound(resource_path("sounds/biting.wav"))
crash_sound = pygame.mixer.Sound(resource_path("sounds/crashing.wav"))
win_sound = pygame.mixer.Sound(resource_path("sounds/win.wav"))
lose_sound = pygame.mixer.Sound(resource_path("sounds/lose.wav"))

CELL_SIZE = 20  # pixels

def run_game(config):
    grid_rows, grid_cols = config.grid_size
    screen_width = grid_cols * CELL_SIZE * 2 + 40  # spacing between grids
    screen_height = grid_rows * CELL_SIZE + 40
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snake vs AI")
    font = pygame.font.SysFont(None, 32)
    large_font = pygame.font.SysFont(None, 60)
    hamilton_cycle = generate_hamiltonian_cycle(grid_rows, grid_cols)

    def draw_hud():
        # Timer
        if time_limit_secs:
            remaining = max(0, int(time_limit_secs - (time.time() - start_time)))
            minutes = remaining // 60
            seconds = remaining % 60
            timer_text = f"Time: {minutes}:{seconds:02d}"
        else:
            timer_text = "Time: ∞"

        score_text = f"Player: {score_player}  |  AI: {score_ai}"

        txt_surface = font.render(timer_text + "    " + score_text, True, (255, 255, 255))
        screen.blit(txt_surface, ((screen_width - txt_surface.get_width()) // 2, 5))

    clock = pygame.time.Clock()

    # Seeded RNG for matching food positions
    random.seed(config.seed)
    food_pos = seeded_random_food(grid_rows, grid_cols, [])

    # Shared starting position
    start_pos = (random.randint(3, grid_rows - 4), random.randint(3, grid_cols - 4))

    player_snake = Snake(start_pos)
    ai_snake = Snake(start_pos)

    score_player = 0
    score_ai = 0

    time_limit_secs = config.time_limit[0] * 60 + config.time_limit[1] if config.time_limit else None
    start_time = time.time()

    running = True
    while running:
        clock.tick(10)  # FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_snake.set_direction((-1, 0))
        elif keys[pygame.K_DOWN]:
            player_snake.set_direction((1, 0))
        elif keys[pygame.K_LEFT]:
            player_snake.set_direction((0, -1))
        elif keys[pygame.K_RIGHT]:
            player_snake.set_direction((0, 1))

        # Move snakes
        player_snake.move(grid_size=(grid_rows, grid_cols))
        ai_snake.direction = {
            "easy": easy_ai_move,
            "hard": lambda snake, food, grid_size:
            hard_ai_move(
                snake,
                food,
                grid_size,
                player_snake_body=player_snake.body,
                hamilton_cycle=hamilton_cycle  # You must generate this at game start
            )
        }[config.difficulty](ai_snake, food_pos, config.grid_size)
        ai_snake.move(grid_size=(grid_rows, grid_cols))

        # Check food collisions
        player_ate = player_snake.body[0] == food_pos
        ai_ate = ai_snake.body[0] == food_pos

        if player_ate:
            eat_sound.play()
            player_snake.grow = True
            score_player += 1

        if ai_ate:
            eat_sound.play()
            ai_snake.grow = True
            score_ai += 1

        if player_ate or ai_ate:
            eat_sound.play()
            food_pos = seeded_random_food(grid_rows, grid_cols, player_snake.body + ai_snake.body)

        # Check end conditions
        player_dead = player_snake.check_self_collision()
        ai_dead = ai_snake.check_self_collision()

        elapsed = time.time() - start_time
        if time_limit_secs and elapsed >= time_limit_secs:
            running = False
            break
        if player_dead or ai_dead:
            crash_sound.play()
            running = False
            break

        # Draw everything
        screen.fill((30, 30, 30))
        draw_hud()

        def draw_grid(snake, offset_x):
            for y in range(grid_rows):
                for x in range(grid_cols):
                    rect = pygame.Rect(offset_x + x * CELL_SIZE, 20 + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, (50, 50, 50), rect, 1)
            for i, segment in enumerate(snake.body):
                color = (0, 180, 255) if i == 0 else (0, 180, 90)
                rect = pygame.Rect(offset_x + segment[1] * CELL_SIZE, 20 + segment[0] * CELL_SIZE, CELL_SIZE * 0.9, CELL_SIZE * 0.9)
                pygame.draw.rect(screen, color, rect)
            food_rect = pygame.Rect(offset_x + food_pos[1] * CELL_SIZE, 20 + food_pos[0] * CELL_SIZE, CELL_SIZE * 0.9, CELL_SIZE * 0.9)
            pygame.draw.rect(screen, (255, 0, 0), food_rect)

        draw_grid(player_snake, 20)
        draw_grid(ai_snake, grid_cols * CELL_SIZE + 40)

        pygame.display.flip()

    pygame.time.delay(1000)
    result = ""
    if player_dead and not ai_dead:
        lose_sound.play()
        result = "AI Wins!"
    elif ai_dead and not player_dead:
        win_sound.play()
        result = "Player Wins!"
    elif time_limit_secs:
        if score_player > score_ai:
            win_sound.play()
            result = "Player Wins by Score!"
        elif score_ai > score_player:
            lose_sound.play()
            result = "AI Wins by Score!"
        else:
            lose_sound.play()
            result = "It's a Tie!"
    elif len(player_snake.body) == grid_rows * grid_cols:
        win_sound.play()
        result = "Player Fills the Map!"
    elif len(ai_snake.body) == grid_rows * grid_cols:
        lose_sound.play()
        result = "AI Fills the Map!"
    else:
        lose_sound.play()
        result = "It's Over!"

    print("\n" + result)

    # Show a result in a window
    result_text = large_font.render(result, True, (255, 255, 0))
    screen.blit(result_text, ((screen_width - result_text.get_width()) // 2, screen_height // 2 - 30))
    pygame.display.flip()
    pygame.time.delay(3000)

