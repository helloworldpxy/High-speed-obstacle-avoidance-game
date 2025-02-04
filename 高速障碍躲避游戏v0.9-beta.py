'''
高速障碍躲避游戏 v0.9-beta
Written by HelloWorld05
2025/02/04
'''
import pygame
import random
import math
import sys

# 初始化 Pygame
pygame.init()

# 屏幕设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("高速障碍躲避游戏")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 玩家属性
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_speed = 10

# 障碍物属性
obstacle_list = []
obstacle_speed = 10  # 初始高速度
obstacle_size = 80   # 体积较大
shapes = ['triangle', 'rectangle', 'circle']
colors = [
    (255, 0, 0),    # 红色
    (0, 255, 0),    # 绿色
    (0, 0, 255),    # 蓝色
    (255, 255, 0),  # 黄色
    (255, 0, 255),  # 紫色
    (0, 255, 255)   # 青色
]

# 分数和关卡
score = 0
high_score = 0
level = 1

# 字体设置
font = pygame.font.SysFont("Arial", 24)

# 游戏状态
game_over = False
pause = False

# 生成障碍物
def create_obstacle():
    shape = random.choice(shapes)
    color = random.choice(colors)
    x_pos = random.randint(0, WIDTH - obstacle_size)
    y_pos = -obstacle_size
    obstacle = {
        'shape': shape,
        'color': color,
        'x': x_pos,
        'y': y_pos,
        'size': obstacle_size
    }
    obstacle_list.append(obstacle)

# 绘制障碍物
def draw_obstacle(obstacle):
    shape = obstacle['shape']
    color = obstacle['color']
    x = obstacle['x']
    y = obstacle['y']
    size = obstacle['size']
    if shape == 'rectangle':
        pygame.draw.rect(screen, color, (x, y, size, size))
    elif shape == 'circle':
        pygame.draw.circle(screen, color, (x + size // 2, y + size // 2), size // 2)
    elif shape == 'triangle':
        points = [
            (x + size / 2, y),
            (x, y + size),
            (x + size, y + size)
        ]
        pygame.draw.polygon(screen, color, points)

# 检测碰撞
def detect_collision(player_pos, obstacle):
    px = player_pos[0]
    py = player_pos[1]
    size = obstacle['size']
    ox = obstacle['x']
    oy = obstacle['y']

    # 玩家和障碍物的矩形
    player_rect = pygame.Rect(px, py, player_size, player_size)
    obstacle_rect = pygame.Rect(ox, oy, size, size)

    # 检测矩形重叠
    if player_rect.colliderect(obstacle_rect):
        return True
    return False

# 显示文本
def draw_text(text, size, color, x, y):
    font_obj = pygame.font.SysFont("Arial", size)
    text_surface = font_obj.render(text, True, color)
    screen.blit(text_surface, (x, y))

# 主游戏循环
clock = pygame.time.Clock()
while True:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 暂停功能
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause = not pause
            # 游戏结束后按 'R' 键重新开始
            if game_over and event.key == pygame.K_r:
                game_over = False
                score = 0
                level = 1
                obstacle_speed = 10
                obstacle_list.clear()
                player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]

    if not pause and not game_over:
        # 玩家移动
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_pos[0] < WIDTH - player_size:
            player_pos[0] += player_speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_pos[1] > 0:
            player_pos[1] -= player_speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_pos[1] < HEIGHT - player_size:
            player_pos[1] += player_speed

        # 鼠标控制
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            player_pos[0] = mx - player_size / 2
            player_pos[1] = my - player_size / 2

        # 创建障碍物
        if random.randint(1, max(1, 30 - level * 2)) == 1:
            create_obstacle()

        # 更新障碍物位置
        for obstacle in obstacle_list[:]:
            obstacle['y'] += obstacle_speed
            if obstacle['y'] > HEIGHT:
                obstacle_list.remove(obstacle)
                score += 10  # 每避开一个障碍物得10分

                # 关卡提升
                if score % 100 == 0:
                    level += 1
                    obstacle_speed += 5  # 提升障碍物速度
            # 碰撞检测
            if detect_collision(player_pos, obstacle):
                game_over = True
                if score > high_score:
                    high_score = score

    # 绘制背景
    screen.fill(BLACK)

    # 绘制玩家
    pygame.draw.rect(screen, WHITE, (player_pos[0], player_pos[1], player_size, player_size))

    # 绘制障碍物
    for obstacle in obstacle_list:
        draw_obstacle(obstacle)

    # 显示得分和关卡信息
    draw_text(f"Score: {score}", 24, WHITE, 10, 10)
    draw_text(f"High Score: {high_score}", 24, WHITE, 10, 40)
    draw_text(f"Level: {level}", 24, WHITE, 10, 70)

    # 暂停提示
    if pause:
        draw_text("Game Paused, Press P to Continue", 36, WHITE, WIDTH / 2 - 150, HEIGHT / 2)

    # 游戏结束界面
    if game_over:
        draw_text("Game Over", 64, WHITE, WIDTH / 2 - 100, HEIGHT / 2 - 100)
        draw_text(f"Your Score: {score}", 36, WHITE, WIDTH / 2 - 80, HEIGHT / 2 - 30)
        draw_text("Press R to Restart", 36, WHITE, WIDTH / 2 - 120, HEIGHT / 2 + 30)

    # 更新屏幕
    pygame.display.flip()
    # 控制帧率
    clock.tick(60)
