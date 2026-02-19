import pygame
import random
import sys

pygame.init()

basket_width = 100
basket_height = 100

screen_width = 800
screen_height = 600

#falling items
itemSize = 60
itemSpeed = 10
itemRadius = 15

#timer
startTime = 45

palePink = (255, 205, 220)
daret = (68, 0, 18)
lightMauve = (194, 146, 161)
darkMauve = (135, 76, 98)

#display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Catch the treasure!")

basket = pygame.image.load("Basket.png").convert_alpha()
background = pygame.image.load("background.jpg").convert()
basket = pygame.transform.scale(basket, (basket_width, basket_height))
background = pygame.transform.scale(background, (screen_width, screen_height))

treasure1 = pygame.transform.scale(pygame.image.load("fork.png").convert_alpha(), (itemSize, itemSize))
treasure2 = pygame.transform.scale(pygame.image.load("necklace.png").convert_alpha(), (itemSize, itemSize))
treasure3 = pygame.transform.scale(pygame.image.load("silver-box.png").convert_alpha(), (itemSize, itemSize))
junk1 = pygame.transform.scale(pygame.image.load("trash.png").convert_alpha(), (itemSize, itemSize))
junk2 = pygame.transform.scale(pygame.image.load("seaweed.png").convert_alpha(), (itemSize, itemSize))

item_types = [
    (treasure1, 5, "Silver Fork"),
    (treasure2, 10, "Shiny Necklace"),
    (treasure3, 15, "Ancient Silver Box"),
    (junk1, -20, "Bag of Trash"),
    (junk2, -10, "Slimy Seaweed")
]

font = pygame.font.SysFont("Dokdo", 36)
small_font = pygame.font.SysFont("Dokdo", 24)

def show_instructions():
    waiting = True
    while waiting:
        screen.fill(palePink)
        title = font.render("Catch the Treasure!", True, daret)
        screen.blit(title, (screen_width // 2 - 100, 50))

        # items and their values
        y_offset = 120
        for img, val, name in item_types:
            screen.blit(img, (250, y_offset))
            color = lightMauve if val > 0 else darkMauve
            txt = small_font.render(f"{name}: {val} points", True, color)
            screen.blit(txt, (310, y_offset + 5))
            y_offset += 60
            
        instructions = font.render("Collect as many treatures as possible, Avoid the junk! Press SPACE to start!", True, daret)
        screen.blit(instructions, (screen_width // 2 - 140, 480))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

basketX = screen_width // 2 - basket_width // 2
basketY = screen_height - basket_height - 10
score = 0
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
start_ticks = pygame.time.get_ticks() 

items = []

def spawn_item():
    entry = random.choice(item_types)
    # support entries with (img, value) or (img, value, name)
    img = entry[0]
    value = entry[1]
    x = random.randint(0, screen_width - itemSize)
    return {"x": x, "y": -50, "img": img, "value": value}

for _ in range(4):
    items.append(spawn_item())

def display_ui(score, timer):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    timer_text = font.render(f"Time: {timer}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
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
        basketX -= 15
    if keys[pygame.K_RIGHT] and basketX < screen_width - basket_width:
        basketX += 15


    basket_rect = pygame.Rect(basketX, basketY, basket_width, basket_height)

    for item in items[:]:
        item["y"] += itemSpeed
        item_rect = pygame.Rect(item["x"], item["y"], itemSize, itemSize)

        if basket_rect.colliderect(item_rect):
            score += item["value"]
            items.remove(item)
            items.append(spawn_item())

        elif item["y"] > screen_height:
            items.remove(item)
            items.append(spawn_item())

    show_instructions()
    screen.blit(background, (0, 0))
    screen.blit(basket, (basketX, basketY))

    for item in items:
        screen.blit(item["img"], (item["x"], item["y"]))

    display_ui(score, second)
    pygame.display.flip()
    clock.tick(30)
