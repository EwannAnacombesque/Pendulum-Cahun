import pygame
import physics

# Pygame initialisation stuff
pygame.font.init()
pygame.mixer.init()

screen_width = 1000
screen_height = screen_width*11/16

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Pendulum")

# Path
ground = pygame.Surface((screen_width,screen_height))
ground.fill(physics.COLORS_THEME[3])

g = 2 # gravitation value
dt = 0 # current velocity of the simulation
running = True 
initial_dt = 0.05 # reference velocity of the simulation
is_friction_enabled = False

# Can add pendulums
pendulums = [physics.Pendulum(int(screen_width/2),int(screen_height/2),150,150,3.10,3.20,15,15,81,50,30)]

def handle_events():
   global dt,running,initial_dt,is_friction_enabled
   for event in pygame.event.get():
      # Quit the application
        if event.type == pygame.QUIT:
            running =False
      # Stop / play and enable friction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
              if dt == initial_dt: dt =0
              else: dt = initial_dt
            if event.key==pygame.K_RETURN:
              is_friction_enabled = not is_friction_enabled
      # Slow down or speed up the time
        if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 4:
             initial_dt *= 1.1
             initial_dt = min(initial_dt,3)
             dt = initial_dt
          if event.button == 5:
             initial_dt /= 1.1
             dt = initial_dt
        
# Running loop
while running:
    # Set the background as the path
    screen.blit(ground,(0,0))
    clock.tick(200)

    # Process queries, as are pressed keys or mouse scrolling
    handle_events()
    
    # Each pendulum can be treated asynchronously 
    for pendulum in pendulums:
      pendulum.update_physics(g,dt,is_friction_enabled)
      pendulum.update_graphics(ground,dt)
      pendulum.draw(screen)

    pygame.display.flip()
