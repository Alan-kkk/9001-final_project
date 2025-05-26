import pygame
import sys
import random

pygame.init()

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED_FOOD = (213, 50, 80)
COLOR_BLUE_SNAKE = (0, 0, 255)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20

game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

game_clock = pygame.time.Clock()
GAME_FPS = 10

font_message = pygame.font.SysFont(None, 40)
font_score = pygame.font.SysFont(None, 35)
font_large_message = pygame.font.SysFont(None, 75)

def display_game_score(score_value):
    text_surface = font_score.render("Score: " + str(score_value), True, COLOR_BLACK)
    game_screen.blit(text_surface, [10, 10])

def draw_snake_body(snake_block_pixel_size, current_snake_body):
    for x_pos, y_pos in current_snake_body:
        pygame.draw.rect(game_screen, COLOR_BLUE_SNAKE, [x_pos, y_pos, snake_block_pixel_size, snake_block_pixel_size])

def show_message_on_screen(message_text, text_color, y_displacement=0, font_size_type="small"):
    if font_size_type == "large":
        rendered_text = font_large_message.render(message_text, True, text_color)
    else:
        rendered_text = font_message.render(message_text, True, text_color)
    
    text_rectangle = rendered_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_displacement))
    game_screen.blit(rendered_text, text_rectangle)

def main_game_loop():
    is_game_over = False
    is_game_session_closed = False

    snake_head_x = SCREEN_WIDTH / 2
    snake_head_y = SCREEN_HEIGHT / 2
    snake_x_change = 0
    snake_y_change = 0

    snake_body_list = []
    snake_current_length = 1

    food_x_position = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y_position = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    snake_current_direction = None

    while not is_game_over:

        while is_game_session_closed:
            game_screen.fill(COLOR_WHITE)
            show_message_on_screen("You Lost!", COLOR_RED_FOOD, -50, "large")
            show_message_on_screen("Press C-Play Again or Q-Quit", COLOR_BLACK, 50)
            display_game_score(snake_current_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        is_game_over = True
                        is_game_session_closed = False
                    if event.key == pygame.K_c:
                        main_game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake_current_direction != "RIGHT":
                    snake_x_change = -BLOCK_SIZE
                    snake_y_change = 0
                    snake_current_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake_current_direction != "LEFT":
                    snake_x_change = BLOCK_SIZE
                    snake_y_change = 0
                    snake_current_direction = "RIGHT"
                elif event.key == pygame.K_UP and snake_current_direction != "DOWN":
                    snake_y_change = -BLOCK_SIZE
                    snake_x_change = 0
                    snake_current_direction = "UP"
                elif event.key == pygame.K_DOWN and snake_current_direction != "UP":
                    snake_y_change = BLOCK_SIZE
                    snake_x_change = 0
                    snake_current_direction = "DOWN"
                elif event.key == pygame.K_ESCAPE:
                    is_game_over = True
        
        if snake_head_x >= SCREEN_WIDTH or snake_head_x < 0 or snake_head_y >= SCREEN_HEIGHT or snake_head_y < 0:
            is_game_session_closed = True

        snake_head_x += snake_x_change
        snake_head_y += snake_y_change

        game_screen.fill(COLOR_WHITE)
        pygame.draw.rect(game_screen, COLOR_RED_FOOD, [food_x_position, food_y_position, BLOCK_SIZE, BLOCK_SIZE])

        current_snake_head = []
        current_snake_head.append(snake_head_x)
        current_snake_head.append(snake_head_y)
        snake_body_list.append(current_snake_head)

        if len(snake_body_list) > snake_current_length:
            del snake_body_list[0]

        for segment in snake_body_list[:-1]:
            if segment == current_snake_head:
                is_game_session_closed = True

        draw_snake_body(BLOCK_SIZE, snake_body_list)
        display_game_score(snake_current_length - 1)
        pygame.display.update()

        if snake_head_x == food_x_position and snake_head_y == food_y_position:
            food_x_position = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y_position = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_current_length += 1

        game_clock.tick(GAME_FPS)

    pygame.quit()
    sys.exit()

main_game_loop()