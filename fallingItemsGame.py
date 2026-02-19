import pygame
import random
import sys

pygame.init()

basket_width = 100
basket_height = 80

screen_width = 800
screen_height = 600

pink = (255, 192, 203)
white = (255, 255, 255)
magenta = (255, 0, 255)
orange = (255, 165, 0)
background_color = (188, 184, 138)

#falling items
itemSpeed = 10
itemRadius = 15



#timer
startTime = 45

#display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Catch the treasure!")

# load images after display initialized so convert/convert_alpha work
basket = pygame.image.load("Basket.jpg").convert_alpha()
background = pygame.image.load("background.jpg").convert()
basket = pygame.transform.scale(basket, (basket_width, basket_height))
background = pygame.transform.scale(background, (screen_width, screen_height))

basketX = screen_width // 2 - basket_width // 2
basketY = screen_height - basket_height - 10
itemX = random.randint(0, screen_width - itemRadius)
itemY = 0
score = 0
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

start_ticks = pygame.time.get_ticks() 

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
        basketX -= 12
    if keys[pygame.K_RIGHT] and basketX < screen_width - basket_width:
        basketX += 12

    itemY += itemSpeed
    item_rect = pygame.Rect(itemX - itemRadius, itemY - itemRadius, itemRadius * 2, itemRadius * 2)
    basket_rect = pygame.Rect(basketX, basketY, basket_width, basket_height)
    
    if basket_rect.colliderect(item_rect):
        score += 1
        itemY = -20
        itemX = random.randint(itemRadius, screen_width - itemRadius)
        if score % 5 == 0:
            itemSpeed += 1

    if itemY > screen_height:
        itemX = random.randint(0, screen_width - itemRadius)
        itemY = -50

    screen.blit(background, (0, 0))
    screen.blit(basket, (basketX, basketY))

    draw_item(itemX, itemY)
    display_score(score)
    display_timer(second)

    pygame.display.flip()
    clock.tick(30)