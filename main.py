import pygame # This imports the pygame library into the script, so that it's functions are available to be used.

# In Python, when you want to use a function from a library you've imported, you connect them with a dot (.). This is often called dot notation.

pygame.init() # This tells python: "Inside the pygame library, find the function called init, and run it the parentheses is how you tell the program to run the specified function."

screen = pygame.display.set_mode((800, 600)) # this creates a variable 'screen' and assigns the value of the created surface using pygame.display.set_mode()

# For a game to run properly, it needs a game loop, this is the single most important concept in a game. It's a loop that will run continuously as long as our game is supposed to be open.
# In python, the most common way to do this is with a 'while' loop.

running = True # create the variable 'running' and set it's value to 'True'
clock = pygame.time.Clock()
player_x = 375 # Middle of the screen, when accounting for the width of the player.
player_y = 450 # player should be standing on the ground, if he is 50 pixels high.
player_width = 50 # Player width set to 50 pixels wide
player_height = 50 # Player height set to 50 pixels high
player_acceleration = 0.2 # set the player acceleration to 0.1 speed per cycle
player_current_speed = 0
player_max_speed = 5 # Player max speed set to 1 pixel per cycle

# --- main game loop ---
while running: # everything below this will happen as long as 'running' is 'True'
    #pass is a placeholder that means 'do nothing'
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
        if player_current_speed < player_max_speed:
            player_current_speed += player_acceleration
    if keys[pygame.K_a]: # check if the A key is pressed
        if player_current_speed > player_max_speed*-1:
            player_current_speed -= player_acceleration
    if ((keys[pygame.K_a] and keys[pygame.K_d]) or not (keys[pygame.K_a] or keys[pygame.K_d])) and player_current_speed > 0:
        player_current_speed -= player_acceleration
    if ((keys[pygame.K_a] and keys[pygame.K_d]) or not (keys[pygame.K_a] or keys[pygame.K_d])) and player_current_speed < 0:
        player_current_speed += player_acceleration
    if player_current_speed >= 0.2 or player_current_speed <= -0.2:
        player_x += player_current_speed
    # --- draw ---
    screen.fill((173, 216, 230)) # fill the screen with a light blue colour (for the sky)
    pygame.draw.rect(screen, (0, 128, 0), (0, 500, 800, 100)) # Draw a rectangle at the bottom of the screen, 100 pixels high, 800 pixels wide, with colour green.
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_width, player_height)) # draw a rectangle which is the player    # this wont actually render yet, we need to tell pygame that we're done drawing, and to now show the user.
    pygame.display.flip() # Flip the canvas so that the user can now see what we've drawn.
    # --- end of draw ---
    clock.tick(60)
# --- end of game loop ---

# This code runs *after* the main game loop has finished
pygame.quit() # This is the opposite of pygame.init(), this tells python to exit the app and shut down it's engines properly. It's important for a clean exit.