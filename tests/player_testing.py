### Player Testing ###

# LIBRARIES
import pygame, time, random, math
from boid_school import BoidController, Player, utilities
pygame.init()

# CONSTANTS
windowSize = (800,800)
bgCol = "light gray"

boid_controller = BoidController(num_init_boids=150, spawn_range=pygame.Rect(0,0,*windowSize))
player = Player(pygame.Vector2(windowSize[0]/2, windowSize[1]/2))

# LOOP SET-UP
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption("Player Testing")
screen.fill(bgCol)

debug_view = False
mousePos = None
running = True
tick = 0
dt = 0

# MAINLOOP
while running:

    # Time
    lastTime = time.time()

    # Pygame Events
    for event in pygame.event.get():
        
        # Quit Event
        if event.type == pygame.QUIT:
            running = False
            break

        # Key Events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break
            elif event.key == pygame.K_SPACE:
                debug_view = not debug_view

        # Mouse Events
        elif event.type == pygame.MOUSEMOTION:
            mousePos = event.pos

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.dash()

    # All the Good Stuff
    if running:

        boid_controller.update(dt, player)
        player.update(dt, mousePos)

        # Display and Time
        pygame.display.update()
        screen.fill(bgCol)

        boid_controller.draw(screen, debug_view)
        player.draw(screen)

        tick += 1
        dt = time.time()-lastTime

# PROGRAM END
pygame.quit()
print("PROGRAM END")
