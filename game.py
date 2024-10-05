import pygame
import random

# กำหนดสี
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# กำหนดขนาดหน้าจอ
WIDTH = 400
HEIGHT = 600

# กำหนดความเร็วของวัตถุที่ตก
OBJECT_SPEED = 5

# กำหนดขนาดของผู้เล่น
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40

# กำหนดค่าเริ่มต้น
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Falling Objects")
clock = pygame.time.Clock()

# ฟังก์ชันสร้างวัตถุที่ตกลงมา
def create_object():
    object_width = random.randint(20, 50)
    object_height = object_width
    object_x = random.randint(0, WIDTH - object_width)
    object_y = -object_height
    return [object_x, object_y, object_width, object_height]

# ฟังก์ชันวาดผู้เล่น
def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, [x, y, PLAYER_WIDTH, PLAYER_HEIGHT])

# ฟังก์ชันวาดวัตถุที่ตกลงมา
def draw_object(object_list):
    for obj in object_list:
        pygame.draw.rect(screen, RED, obj)

# ฟังก์ชันหลักของเกม
def game_loop():
    player_x = WIDTH // 2 - PLAYER_WIDTH // 2
    player_y = HEIGHT - PLAYER_HEIGHT - 10
    player_speed = 7
    player_dx = 0

    object_list = []
    object_timer = 0

    score = 0
    game_over = False

    # ลูปเกม
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_dx = -player_speed
                if event.key == pygame.K_RIGHT:
                    player_dx = player_speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_dx = 0

        # เคลื่อนที่ผู้เล่น
        player_x += player_dx
        if player_x < 0:
            player_x = 0
        if player_x + PLAYER_WIDTH > WIDTH:
            player_x = WIDTH - PLAYER_WIDTH

        # สร้างวัตถุใหม่
        if object_timer == 0:
            object_list.append(create_object())
        object_timer = (object_timer + 1) % 30

        # เคลื่อนที่วัตถุ
        for obj in object_list:
            obj[1] += OBJECT_SPEED

        # ตรวจสอบการชนของผู้เล่นกับวัตถุ
        for obj in object_list:
            if (obj[1] + obj[3] > player_y and
                obj[0] < player_x + PLAYER_WIDTH and
                obj[0] + obj[2] > player_x and
                obj[1] < player_y + PLAYER_HEIGHT):
                game_over = True

        # ลบวัตถุที่หลุดออกจากหน้าจอ
        object_list = [obj for obj in object_list if obj[1] < HEIGHT]

        # เพิ่มคะแนนเมื่อผู้เล่นหลบได้
        score += 1

        # วาดหน้าจอใหม่
        screen.fill(WHITE)
        draw_player(player_x, player_y)
        draw_object(object_list)

        # แสดงคะแนน
        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    # แสดงหน้าจอ Game Over
    screen.fill(WHITE)
    game_over_text = font.render(f"Game Over! Score: {score}", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
    pygame.display.flip()
    pygame.time.wait(2000)

    pygame.quit()

# เริ่มเกม
game_loop()
