import pygame
import asyncio
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Russian Doll Game")
clock = pygame.time.Clock()

pearl = pygame.image.load("pearl.png").convert_alpha()
pearl = pygame.transform.scale(pearl, (40, 40))

palePink = (255, 205, 220)
daret = (68, 0, 18)
lightMauve = (194, 146, 161)
darkMauve = (135, 76, 98)


cupWidth = 100
cupHeight = 150

cup_y = 150
font = pygame.font.Font(None, 48)

class Cup:
    def __init__(self, x, y, index):
        self.rect = pygame.Rect(x, y, cupWidth, cupHeight)
        self.target_x = x
        self.orig_y = y
        self.target_y = y
        self.index = index
        self.speed = 10
        self.vspeed = 24
    
    def draw(self, screen):
        pygame.draw.rect(screen, darkMauve, self.rect, border_radius=10)

    def update(self):
        if self.rect.x < self.target_x:
            self.rect.x = min(self.rect.x + self.speed, self.target_x)
        elif self.rect.x > self.target_x:
            self.rect.x = max(self.rect.x - self.speed, self.target_x)
        # vertical movement toward target_y (for lift/lower)
        if self.rect.y < self.target_y:
            self.rect.y = min(self.rect.y + self.vspeed, self.target_y)
        elif self.rect.y > self.target_y:
            self.rect.y = max(self.rect.y - self.vspeed, self.target_y)

    def isMoving(self):
        return (self.rect.x != self.target_x) or (self.rect.y != self.target_y)

    def lift(self, amount=60):
        # move cup up by amount (positive amount lifts up)
        self.target_y = self.orig_y - amount

    def lower(self):
        self.target_y = self.orig_y
    
positions = [100, 350, 600]
cups = [Cup(positions[i], cup_y, i) for i in range(3)]

pearlOwner = random.choice(cups)
# lift the cup that hides the pearl during the preview so player can see it
pearlOwner.lift(60)

state = "preview"
previewTime = 120
shuffleCount = 0
maxShuffles = 10
shuffling = True
gameOver = False
message = "Remember where the pearl is!"

def shuffleCups():
    global shuffleCount, state, message
    # only shuffle when in shuffling state
    if state != "shuffling":
        return
    if shuffleCount < maxShuffles:
        c1, c2 = random.sample(cups, 2)
        c1.target_x, c2.target_x = c2.target_x, c1.target_x
        shuffleCount += 1
    else:
        state = "picking"
        message = "Where is the pearl? Click a cup to find out!"
        print("[DEBUG] shuffle finished -> state=picking")

#main loop

running = True

async def main_loop():
    global running, state, previewTime, shuffleCount, gameOver, message
    while running:
        screen.fill(palePink)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and state == "picking" and not gameOver:
                mousePOS = event.pos
                print(f"[DEBUG] MOUSEBUTTONDOWN at {mousePOS}, state={state}, gameOver={gameOver}")
                for cup in cups:
                    if cup.rect.collidepoint(mousePOS):
                        print(f"[DEBUG] clicked cup index={cup.index}, pearlOwner index={pearlOwner.index}")
                        gameOver = True
                        state = "gameover"
                        cup.lift(80)
                        if cup is pearlOwner:
                            message = "You found the pearl!"
                        else:
                            message = "Try again!"
                            pearlOwner.lift(80)

        # update positions for all cups
        for cup in cups:
            cup.update()

        # draw pearl once (table position) during preview and after game over
        if state == "preview" or state == "gameover":
            pearl_x = pearlOwner.rect.centerx - pearl.get_width() // 2
            pearl_y = pearlOwner.orig_y + cupHeight - 40
            screen.blit(pearl, (pearl_x, pearl_y))

        # handle preview timer once per frame
        if state == "preview":
            previewTime -= 1
            if previewTime <= 0:
                for c in cups:
                    c.lower()
                state = "shuffling"
                message = "Watch closely"

        # handle shuffling state
        if state == "shuffling":
            moving = any(cup.isMoving() for cup in cups)
            if not moving:
                shuffleCups()

        # draw cups after pearl so cups can cover the pearl when lowered
        for cup in cups:
            cup.draw(screen)

        text = font.render(message, True, daret)
        screen.blit(text, (WIDTH // 2 - text.get_width()//2, 50))

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

asyncio.run(main_loop())