import pygame
import sqlite3
import random
import time

# Инициализация Pygame
pygame.init()

# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Моя игра")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Список цветов для бонусов
BONUS_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Класс Игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - 100
        self.speed = 1
        self.name = name
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Ограничение перемещения игрока в пределах экрана
        self.rect.clamp_ip(screen.get_rect())

# Класс Базы Данных
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('scores.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS scores
                         (name TEXT, score INTEGER)''')

    def save_score(self, name, score):
        self.c.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
        self.conn.commit()

    def get_top_scores(self):
        self.c.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 5")
        return self.c.fetchall()

class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.color = random.choice(BONUS_COLORS)
        self.image = pygame.Surface([20, 20])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Основной цикл игры
def main():
    # Создание игрока
    player_name = ""
    player_input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50, 400, 50)
    player_input_active = True
    player = None

    # Создание объекта базы данных
    db = Database()
    bonuses = pygame.sprite.Group()
    for i in range(10):
        bonus = Bonus(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))
        bonuses.add(bonus)

    # Количество собранных бонусов
    collected_bonuses = 0
    total_bonuses = 10

    # Время начала игры
    start_time = time.time()
    time_limit = 30  # 30 секунд

    # Основной игровой цикл
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player_input_rect.collidepoint(event.pos):
                    player_input_active = not player_input_active
            elif event.type == pygame.KEYDOWN:
                if player_input_active:
                    if event.key == pygame.K_RETURN:
                        player_input_active = False
                        player = Player(player_name)
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

        # Обновление позиции игрока
        if player:
            player.update()

        # Обновление бонусов
        bonuses.update()

        # Проверка столкновений игрока с бонусами
        if player:
            collected_bonus_sprites = pygame.sprite.spritecollide(player, bonuses, True)
            for bonus in collected_bonus_sprites:
                player.score += 10
                collected_bonuses += 1

        # Проверка на проигрыш
        if collected_bonuses == total_bonuses:
            running = False
            font = pygame.font.Font(None, 48)
            text = font.render("Вы выиграли!", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25))
            # Сохранение результата в базе данных
            db.save_score(player.name, player.score)
            # Вывод топ-5 игроков
            font = pygame.font.Font(None, 36)
            top_scores = db.get_top_scores()
            for i, (name, score) in enumerate(top_scores):
                text = font.render(f"{i+1}. {name}: {score}", True, WHITE)
                screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 25 + i * 30))
            pygame.display.flip()
            pygame.time.wait(5000)  # Пауза 5 секунд
            running = False
        elif time.time() - start_time > time_limit:
            running = False
            font = pygame.font.Font(None, 48)
            text = font.render("Вы проиграли.", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25))
            # Сохранение результата в базе данных
            db.save_score(player.name, player.score)
            # Вывод топ-5 игроков
            font = pygame.font.Font(None, 36)
            top_scores = db.get_top_scores()
            for i, (name, score) in enumerate(top_scores):
                text = font.render(f"{i+1}. {name}: {score}", True, WHITE)
                screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 25 + i * 30))
            pygame.display.flip()
            pygame.time.wait(5000)  # Пауза 5 секунд
            running = False

        # Отрисовка игровых объектов
        screen.fill(BLACK)
        if player:
            screen.blit(player.image, player.rect)
        bonuses.draw(screen)

        # Отображение информации об игроке
        if player_input_active:
            pygame.draw.rect(screen, GRAY, player_input_rect, 2)
            font = pygame.font.Font(None, 36)
            text = font.render(f"Введите ваше имя: {player_name}", True, WHITE)
            screen.blit(text, (player_input_rect.x + 10, player_input_rect.y + 10))
        elif player:
            font = pygame.font.Font(None, 36)
            text = font.render(f"Имя: {player.name}, Счёт: {player.score}", True, WHITE)
            screen.blit(text, (10, 10))

            # Отображение оставшегося времени
            time_remaining = time_limit - (time.time() - start_time)
            if time_remaining > 0:
                text = font.render(f"Время: {int(time_remaining)} секунд", True, WHITE)
                screen.blit(text, (10, 50))
            else:
                text = font.render(f"Время вышло", True, WHITE)
                screen.blit(text, (10, 50))

        # Обновление экрана
        pygame.display.flip()

    # Завершение Pygame
    pygame.quit()

if __name__ == "__main__":
    main()

