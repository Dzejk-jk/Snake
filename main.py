import pygame
import random
import time
import sys
from config import config


def update_position(snake, direction, step):
    if direction == "UP":
        snake = [snake[0], snake[1] - step]
    if direction == "DOWN":
        snake = [snake[0], snake[1] + step]
    if direction == "LEFT":
        snake = [snake[0] - step, snake[1]]
    if direction == "RIGHT":
        snake = [snake[0] + step, snake[1]]
    return snake


def update_direction(direction, keys):
    if keys[pygame.K_UP]:
        return "UP" if direction != "DOWN" else direction
    if keys[pygame.K_DOWN]:
        return "DOWN" if direction != "UP" else direction
    if keys[pygame.K_LEFT]:
        return "LEFT" if direction != "RIGHT" else direction
    if keys[pygame.K_RIGHT]:
        return "RIGHT" if direction != "LEFT" else direction
    return direction


def is_out(snake, game_res):
    if snake[0] < 0 or snake[1] < 0 or snake[0] > game_res[0] or snake[1] > game_res[1]:
        return True
    return False


def wall_bonus(snake, game_res):
    if is_out(snake, game_res):
        if snake[0] < 0:
            snake[0] = game_res[0]
        if snake[0] > game_res[0]:
            snake[0] = 0
        if snake[1] > game_res[1]:
            snake[1] = 0
        if snake[1] < 0:
            snake[1] = game_res[1]
    return snake


def end_game(window):
    print("GAME OVER")
    window.fill(config.BACKGROUND_COLOR)
    pygame.quit()
    sys.exit()


def generate_out_of_window():
    x = -100
    y = -100
    return [x, y]


def generate_bonus(game_res, snake_size):
    x = random.choice(range(0, game_res[0] - snake_size + 1, snake_size))
    y = random.choice(range(0, game_res[1] - snake_size + 1, snake_size))
    return [x, y]


def is_collision(snake_head, bonus):
    if snake_head[0] == bonus[0] and snake_head[1] == bonus[1]:
        return True
    return False
                

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode(config.GAME_RES)
    snake = [[config.GAME_RES[0] // 2, config.GAME_RES[1] // 2]]
    apple = generate_bonus(config.GAME_RES, config.SNAKE_SIZE)
    bonus_speed = generate_bonus(config.GAME_RES, config.SNAKE_SIZE)
    bonus_wall = generate_bonus(config.GAME_RES, config.SNAKE_SIZE)
    bonus_duration_remaining = 0
    bonus_duration_remaining_wall = 0
    direction = "LEFT"
    bonus_w = False
    bonus_s = False
    score = 0
    score_font = pygame.font.SysFont("comicsans", config.SCORE_FONT_SIZE)

    while True:
        score_text = score_font.render(f"Score {score}", True, config.SCORE_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()
        direction = update_direction(direction, keys)
        new_position = update_position(snake[0], direction, config.SNAKE_SIZE)
        snake.insert(0, new_position)

        # eating apple 
        if is_collision(snake[0], apple):
            print("Apple")
            apple = generate_bonus(config.GAME_RES, config.SNAKE_SIZE)
            score += 1
        else:
            snake.pop()
        
        # bonus speed 
        if is_collision(snake[0], bonus_speed):
            print("Speed bonus")
            config.GAME_FPS += config.SPEED_BONUS
            bonus_duration_remaining = 5
            bonus_speed = generate_out_of_window()
            bonus_s = True
        if bonus_duration_remaining > 0:
            bonus_duration_remaining -= (time.time() - last_frame_time)
            if bonus_duration_remaining <= 0:
                bonus_s = False
                config.GAME_FPS -= config.SPEED_BONUS
                bonus_duration_remaining = 0 
                bonus_speed = generate_bonus(config.GAME_RES, config.SNAKE_SIZE)
                print("Speed dissapear")

        # bonus wall
        if is_collision(snake[0], bonus_wall):
            print("Wall bonus")
            bonus_wall = generate_out_of_window()
            bonus_duration_remaining_wall = 5
            bonus_w = True
        if bonus_duration_remaining_wall > 0:
            bonus_duration_remaining_wall -= (time.time() - last_frame_time)
            if bonus_duration_remaining_wall <= 0:
                bonus_w = False
                bonus_duration_remaining_wall = 0 
                bonus_wall = generate_bonus(config.GAME_RES, config.SNAKE_SIZE)
                print("Wall bonus dissapear")

        # snake body collision
        if snake[0] in snake[1:]:
            end_game(window)

        # wall collision    
        if bonus_w == True:
            wall_bonus(snake[0], config.GAME_RES)
        else:
            if is_out(snake[0], config.GAME_RES):
                end_game(window)

        for part in snake:
            snake_head_x, snake_head_y = snake[0]
            if bonus_w:
                pygame.draw.rect(window, config.BODY_COLOR, 
                            pygame.Rect(part[0], part[1], config.SNAKE_SIZE, config.SNAKE_SIZE))
                pygame.draw.rect(window, config.WALL_BONUS_COLOR, 
                             pygame.Rect(snake_head_x, snake_head_y, config.SNAKE_SIZE, config.SNAKE_SIZE))
            elif bonus_s:
                pygame.draw.rect(window, config.BODY_COLOR, 
                            pygame.Rect(part[0], part[1], config.SNAKE_SIZE, config.SNAKE_SIZE))
                pygame.draw.rect(window, config.BONUS_SPEED_COLOR, 
                             pygame.Rect(snake_head_x, snake_head_y, config.SNAKE_SIZE, config.SNAKE_SIZE))
            else:  
                pygame.draw.rect(window, config.BODY_COLOR, 
                                pygame.Rect(part[0], part[1], config.SNAKE_SIZE, config.SNAKE_SIZE))
                pygame.draw.rect(window, config.HEAD_COLOR, 
                                pygame.Rect(snake_head_x, snake_head_y, config.SNAKE_SIZE, config.SNAKE_SIZE))
        pygame.draw.rect(window, config.APPLE_COLOR, 
                        pygame.Rect(apple[0], apple[1], config.SNAKE_SIZE, config.SNAKE_SIZE))
        pygame.draw.rect(window, config.BONUS_SPEED_COLOR, 
                        pygame.Rect(bonus_speed[0], bonus_speed[1], config.SNAKE_SIZE, config.SNAKE_SIZE))
        pygame.draw.rect(window, config.WALL_BONUS_COLOR, 
                        pygame.Rect(bonus_wall[0], bonus_wall[1], config.SNAKE_SIZE, config.SNAKE_SIZE))
        window.blit(score_text, (config.GAME_RES[0] - 90, config.GAME_RES[1] - config.GAME_RES[1]))
        last_frame_time = time.time()
        pygame.display.update()
        window.fill(config.BACKGROUND_COLOR)
        clock.tick(config.GAME_FPS)