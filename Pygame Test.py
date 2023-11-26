import pygame

#Pygame setup
pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
running = True

window = pygame.display.set_mode((640,480))

# Game
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    # fill screen with color, wipes past frame away
    screen.fill("orange")

    # RENDER

    pygame.draw.rect(window,(0,0,200),(120,120,400,240))

    pygame.display.flip() # Refresh screen
    clock.tick(60) # limits FPS to 60

pygame.quit()