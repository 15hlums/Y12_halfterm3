import pygame

pygame.init()

DISPLAY = pygame.display.set_mode([800, 600])

FPS = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)
left = 50
top = 50
width = 10
height = 40

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            quit()


    DISPLAY.fill((black))

    pygame.draw.rect(DISPLAY, (white), (left, top, width, height))

    left += 5

    pygame.display.update()

    FPS.tick(30)