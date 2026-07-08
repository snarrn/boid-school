### Shark Testing ###

# LIBRARIES
import pygame, time, random, math
from boid_school import BoidController, Player, utilities
pygame.init()

# CONSTANTS
windowSize = (950,950)
bgCol = "light gray"

boid_controller = BoidController(num_init_boids=50, num_init_sharks=1, spawn_range=pygame.Rect(200,200,windowSize[0]-400,windowSize[1]-400))
player = Player(pygame.Vector2(windowSize[0]/2, windowSize[1]/2))

# LOOP SET-UP
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption("Shark Testing")
screen.fill(bgCol)

debug_view = False
mousePos = None
running = True
tick = 0
dt = 0
"""
THINGS TO DO
------------
Fix problem with angles changing based on the frame rate.

"""
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
            elif event.button == 2:
                if (pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]):
                    boid_controller.add_boids(count=5, positions=pygame.Vector2(mousePos))
            elif event.button == 3:
                for _ in range(5 if (pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]) else 1):
                    boid_controller.remove_boid_by_pos(pygame.Vector2(mousePos), max_dist=100)

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
