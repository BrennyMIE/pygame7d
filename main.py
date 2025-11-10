import pygame # This imports the pygame library into the script, so that it's functions are available to be used.
# In Python, when you want to use a function from a library you've imported, you connect them with a dot (.). This is often called dot notation.

pygame.init() # This tells python: "Inside the pygame library, find the function called init, and run it the parentheses is how you tell the program to run the specified function."

screen = pygame.display.set_mode((800, 600)) # this creates a variable 'screen' and assigns the value of the created surface using pygame.display.set_mode()

# For a game to run properly, it needs a game loop, this is the single most important concept in a game. It's a loop that will run continuously as long as our game is supposed to be open.
# In python, the most common way to do this is with a 'while' loop.

running = True # create the variable 'running' and set it's value to 'True'
clock = pygame.time.Clock()
debug_font = pygame.font.Font(None, 30)
player_x = 375 # Middle of the screen, when accounting for the width of the player.
player_y = 450 # player should be standing on the ground, if he is 50 pixels high.
player_width = 50 # Player width set to 50 pixels wide
player_height = 50 # Player height set to 50 pixels high
player_acceleration = 0.2 # set the player acceleration to 0.2 speed per cycle
player_current_speed = 0
player_max_speed = 5 # Player max speed set to 5 pixel per cycle
player_min_x = 0
player_max_x = 425
world_scroll = 0
world_speed = 0

# --- main game loop ---
while running: # everything below this will happen as long as 'running' is 'True'
    #pass is a placeholder that means 'do nothing'
    if player_x < player_max_x:
        world_speed = 0
    if world_speed < player_acceleration:
        world_speed = 0
    if player_x >= player_max_x and world_speed == 0:
        world_speed = player_current_speed
    if player_x >= player_max_x:
        player_x = player_max_x
        player_current_speed -= player_current_speed
    if player_x <= player_min_x:
        player_x = player_min_x
        player_current_speed += -1*player_current_speed
    if player_current_speed < 0.2 and player_current_speed > -0.2:
        player_current_speed = 0
        # --- Event Loop ---
    for event in pygame.event.get(): # each item in the list 'pygame.event.get()' is an event
        if event.type == pygame.KEYDOWN: #if any key has just been pressed
            pass
        if event.type == pygame.KEYUP: # if any key has just been released
            pass
        if event.type == pygame.QUIT: # if the user clicks the 'X' button to close the window
            running = False # Set the variable 'running' to False
    # --- end of event loop ---
    # --- update ---
    keys = pygame.key.get_pressed() # create the variable 'keys' and assign a list of all keys pressed or not

    if keys[pygame.K_d]: # check if the D key is pressed
        if player_current_speed < player_max_speed and player_x+1 <= player_max_x and world_speed == 0:
            player_current_speed += player_acceleration

        if player_x >= player_max_x and world_speed < player_max_speed:
            world_speed += player_acceleration

    if keys[pygame.K_a]: # check if the A key is pressed;
        if world_speed > 0:
            world_speed -= player_acceleration

        if world_speed < player_acceleration:
            world_speed = 0

        if player_current_speed > player_max_speed*-1 and player_x-1 >= player_min_x and world_speed == 0:
            player_current_speed -= player_acceleration

    if ((keys[pygame.K_a] and keys[pygame.K_d]) or not (keys[pygame.K_a] or keys[pygame.K_d])) and player_current_speed > 0:
        player_current_speed -= player_acceleration

    if ((keys[pygame.K_a] and keys[pygame.K_d]) or not (keys[pygame.K_a] or keys[pygame.K_d])) and player_current_speed < 0:
        player_current_speed += player_acceleration

    if ((keys[pygame.K_a] and keys[pygame.K_d]) or not (keys[pygame.K_a] or keys[pygame.K_d])) and world_speed > 0:
        world_speed -= player_acceleration

    if player_current_speed >= player_acceleration or player_current_speed <= -1*player_acceleration:# and player_x >= player_min_x and player_x <= player_max_x:
        player_x += player_current_speed

    if world_speed > 0 and player_x >= player_max_x:
        world_scroll += world_speed
    # --- draw ---
    screen.fill((173, 216, 230)) # fill the screen with a light blue colour (for the sky)
    pygame.draw.rect(screen, (0, 128, 0), (0-world_scroll, 500, 800, 100)) # Draw a rectangle at the bottom of the screen, 100 pixels high, 800 pixels wide, with colour green.
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_width, player_height)) # draw a rectangle which is the player    # this wont actually render yet, we need to tell pygame that we're done drawing, and to now show the user.
    text_surface = debug_font.render(f"Speed: {round(player_current_speed, 2)}", True, (0, 0, 0))
    text_surface2 = debug_font.render(f"X: {round(player_x, 1)}", True, (0, 0, 0))
    text_world_scroll = debug_font.render(f"World Scroll: {round(world_scroll, 1)}", True, (0, 0, 0))
    text_world_speed = debug_font.render(f"World Speed: {round(world_speed, 1)}", True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect2 = text_surface2.get_rect()
    text_world_scroll_rect = text_world_scroll.get_rect()
    text_world_speed_rect = text_world_speed.get_rect()
    text_rect.topright = (800-10, 10) # 10px from the top, 10px from the right
    text_rect2.topright = (800-10, 40)
    text_world_scroll_rect.topright = (800-10, 70)
    text_world_speed_rect.topright = (800-10, 100)
    screen.blit(text_surface, text_rect)
    screen.blit(text_surface2, text_rect2)
    screen.blit(text_world_scroll, text_world_scroll_rect)
    screen.blit(text_world_speed, text_world_speed_rect)
    pygame.display.flip() # Flip the canvas so that the user can now see what we've drawn.
    # --- end of draw ---
    clock.tick(60)
# --- end of game loop ---

# This code runs *after* the main game loop has finished
pygame.quit() # This is the opposite of pygame.init(), this tells python to exit the app and shut down it's engines properly. It's important for a clean exit.