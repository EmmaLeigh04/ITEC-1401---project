import pygame
import random
import sys

pygame.init()

screen_width = 800
screen_height = 600

pink = (255, 192, 203)
white = (255, 255, 255)
magenta = (255, 0, 255)
orange = (255, 165, 0)
background_color = (188, 184, 138)

#falling items
itemSpeed = 5
itemRadius = 15

#basket
basket_width = 100
basket_height = 20

#timer
startTime = 45

#display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Catch the treasure!")

basketX = screen_width // 2 - basket_width // 2
basketY = screen_height - basket_height - 10
itemX = random.randint(0, screen_width - itemRadius)
itemY = 0
score = 0
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

start_ticks = pygame.time.get_ticks() 
def draw_basket(x, y):
    pygame.draw.rect(screen, magenta, (x, y, basket_width, basket_height))
     # Start the timer

def draw_item(x, y):
    pygame.draw.circle(screen, pink, (x, y), itemRadius)

def display_score(score):
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

def display_timer(seconds):
    timer_text = font.render(f"Time: {seconds}", True, white)
    screen.blit(timer_text, (screen_width - 150, 10))

#main game loop

while True:
    screen.fill(background_color)

    second = startTime - (pygame.time.get_ticks() - start_ticks) // 1000
    if second <= 0:
        print(f"Time's up! Your final score is: {score}")
        pygame.quit()
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basketX > 0:
        basketX -= 10
    if keys[pygame.K_RIGHT] and basketX < screen_width - basket_width:
        basketX += 10

    itemY += itemSpeed

    if score > 5 and score % 5 == 0:
        itemSpeed = min(10, itemSpeed + 1)
        basket_width = max(50, basket_width - 10)
    if score > 10 and score % 10 == 0:
        itemSpeed = min(15, itemSpeed + 1)
        basket_width = max(30, basket_width - 10)
    if score > 15 and score % 15 == 0:
        itemSpeed = min(20, itemSpeed + 1)
        basket_width = max(20, basket_width - 10)
    if score > 20 and score % 20 == 0:
        itemSpeed = min(25, itemSpeed + 1)
        basket_width = max(10, basket_width - 10)

    if itemY >= basketY and basketX < itemX < basketX + basket_width:
        score += 1
        itemX = random.randint(0, screen_width - itemRadius)
        itemY = 0
    elif itemY > screen_height:
        itemX = random.randint(0, screen_width - itemRadius)
        itemY = 0

    draw_basket(basketX, basketY)
    draw_item(itemX, itemY)
    display_score(score)
    display_timer(second)

    pygame.display.flip()
    clock.tick(30)