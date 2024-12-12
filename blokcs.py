import pygame

# Инициализация Pygame
pygame.init()

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Размеры окна
width = 800
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Богомолова Game')

# Часы
clock = pygame.time.Clock()

# Параметры платформы и мяча
platform_width = 50
platform_height = 10
ball_radius = 10

# Параметры блоков
block_width = 75
block_height = 20

# Начальные параметры игры
def reset_game():
    global platform_x, platform_y, ball_x, ball_y, ball_x_change, ball_y_change, blocks, game_over, game_won
    platform_x = (width - platform_width) / 2
    platform_y = height - platform_height - 10
    ball_x = width / 2
    ball_y = height / 2
    ball_x_change = 4
    ball_y_change = -4
    game_over = False
    game_won = False

    # Создание блоков
    blocks = []
    for i in range(9):
        for j in range(5):
            blocks.append(pygame.Rect(i * (block_width + 10) + 25, j * (block_height + 10) + 50, block_width, block_height))

# Основной игровой цикл
def game_loop():
    global platform_x, platform_y, ball_x, ball_y, ball_x_change, ball_y_change, blocks, game_over, game_won
    reset_game()  # Инициализируем игру
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if game_over or game_won:
                        reset_game()  # Перезапускаем игру только при окончании игры

        # Только если игра активна, обновляем состояние
        if not game_over and not game_won:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and platform_x > 0:
                platform_x -= 7
            if keys[pygame.K_RIGHT] and platform_x < width - platform_width:
                platform_x += 7

            # Движение мяча
            ball_x += ball_x_change
            ball_y += ball_y_change

            # Проверка столкновения с границами окна
            if ball_x <= ball_radius or ball_x >= width - ball_radius:
                ball_x_change *= -1
            if ball_y <= ball_radius:
                ball_y_change *= -1

            # Проверка столкновения с платформой
            if (platform_y < ball_y + ball_radius < platform_y + platform_height) and (platform_x < ball_x < platform_x + platform_width):
                ball_y_change *= -1

            # Проверка столкновения с блоками
            for block in blocks[:]:
                if block.collidepoint(ball_x, ball_y):
                    blocks.remove(block)
                    ball_y_change *= -1

            # Если мяч упал ниже платформы
            if ball_y > height:
                game_over = True

            # Проверка на победу (если блоки закончились)
            if not blocks:
                game_won = True

        # Отрисовка элементов игры
        display.fill(blue)

        # Отрисовка блоков
        for block in blocks:
            pygame.draw.rect(display, green, block)

        # Отрисовка платформы и мяча
        pygame.draw.rect(display, white, (platform_x, platform_y, platform_width, platform_height))
        pygame.draw.circle(display, red, (int(ball_x), int(ball_y)), ball_radius)

        # Вывод сообщения при окончании игры
        if game_over:
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over! Нажмите R, чтобы начать заново.", True, white)
            display.blit(text, (width // 2 - text.get_width() // 2, height // 2))
        
        if game_won:
            font = pygame.font.Font(None, 36)
            text = font.render("You Win! Нажмите R, чтобы начать заново.", True, white)
            display.blit(text, (width // 2 - text.get_width() // 2, height // 2))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

game_loop()