import pygame # This imports the pygame library into the script, so that it's functions are available to be used.
# In Python, when you want to use a function from a library you've imported, you connect them with a dot (.). This is often called dot notation.

pygame.init() # This tells python: "Inside the pygame library, find the function called init, and run it; the parentheses are how you tell the program to run the specified function."

screen_width = 1280 # Create the variable screen_width. Default = 1280
screen_height = 720 # Create the variable screen_height. Default = 720
screen = pygame.display.set_mode((screen_width, screen_height)) # this creates a variable 'screen' and assigns the value of the created surface using pygame.display.set_mode()

running = True # create the variable 'running' and set it's value to 'True'
clock = pygame.time.Clock() # Create the variable 'clock', and assigns the value returned from the function pygame.time.Clock()?
debug_font = pygame.font.Font(None, 30) # create the variable debug_font, and set it's font to None(default font), with size 30
player_width = 50 # create the variable for the player_width. Default = 50
player_height = 50 # create the variable for the player_height. Default = 50
floor_height = 100 # create the variable floor_height, which specifies the height of the floor. Default = 100
player_x = screen_width / 2 - player_width / 2 # create the variable player_x, which initialises the player's x position. Default value = screen_width/2 - player_width/2 - which is the middle of the screen.
player_y = screen_height - floor_height - player_height # create the variable player_y, which initialises the player's y position. Default value = sscreen_height - floor_height - player_height - which is standing on the ground
player_acceleration = 0.2 # define the player's acceleration speed. Default = 0.2
player_current_speed = 0 # Initialise the player's current speed. Default = 0
player_max_speed = 5 # Define the player's maximum speed, in pixels per cycle.
player_min_x = 0 # Define the minimum allowed x coordinate of the player
player_max_x = screen_width / 2 - player_width / 2 + player_width # define the maximum allowed x value for the player, when accounting for the size of the window.
world_scroll = 0 # initialise the world_scroll variable, which defines how far the world has currently scrolled.
world_speed = 0 # initialise the speed that the world is currently scrolling. Default = 0
ground_rects = [pygame.Rect(0, screen_height - floor_height, screen_width, floor_height)] # Create the list ground_rects, which will contain a list of rectangles used for drawing the ground. Initialise it with a single rectangle that is the height of the floor, and the width of the screen.

# --- Begin Game Loop ---

while running: # everything below this will happen as long as 'running' is 'True'
    # if the player's x coordinate is less than the maximum allowed x coordinate, then set the current world scrolling speed to zero.
    if player_x < player_max_x:
        world_speed = 0

    # if the current world scrolling speed is less than the speed of acceleration per cycle (which is also the minimum possible speed the player can be moving), then set it to zero, to avoid any weirdness that might cause the world to scroll very slowly unintentionally
    if world_speed < player_acceleration:
        world_speed = 0

    # if the player's x coordinate is greater than or equal to the maximum allowed x coordinate and the world is not currently scrolling, and the player is moving, then transfer the player speed into world scrolling speed (which will provide the illusion that the player is moving 'forward' in the game world)
    if player_x >= player_max_x and world_speed == 0 and player_current_speed > 0:
        world_speed = player_current_speed

    # If the player's x position is greater than or equal to the maximum allowed x coordinate, then move the player to his maximum allowed x coordinate (because he's not allowed to go past it!) and set his speed to zero (in a needlessly complex way, it seems?)
    if player_x >= player_max_x:
        player_x = player_max_x
        player_current_speed -= player_current_speed
    
    # If the players x positions is less than or equal to the minimum allowed x position (he's not allowed here!) then move him to his minimum allowed x position, and set his speed to zero (again, needlessly complex way?)
    if player_x <= player_min_x:
        player_x = player_min_x
        player_current_speed += -1*player_current_speed

    # If the players current speed is less than the minimum allowed speed in either direction (one cycle of acceleration), then set his speed to zero (to prevent any weird things happening where he accidentally ends up moving by a fraction of this amount)
    if player_current_speed < 0.2 and player_current_speed > -0.2:
        player_current_speed = 0

    # --- Begin Event Loop ---
    for event in pygame.event.get(): # each item in the list 'pygame.event.get()' is assigned to the 'event'
        # if any key has just been pressed, do nothing.
        if event.type == pygame.KEYDOWN:
            pass

        # if any key has just been released, do nothing.
        if event.type == pygame.KEYUP:
            pass

        # if the user clicks the 'X' button to close the window, then change the variable 'running' to 'False'
        if event.type == pygame.QUIT:
            running = False

# --- End Event Loop ---

# --- Begin Update Loop ---
    # define 'last_ground_rect' during the beginning of the update loop, so that's it's value is always set to the latest piece of ground
    last_ground_rect = ground_rects[-1]

    # if the right side of the latest piece of ground, minus the world_scroll value, is less than or equal to the width of the screen, then create a new piece of ground, 'new_ground', identical to the previous piece, then append it to the list ground_rects
    if last_ground_rect.right - world_scroll <= screen_width:
        new_ground = pygame.Rect(last_ground_rect.right,screen_height-floor_height,screen_width, floor_height)
        ground_rects.append(new_ground)
    
    # if the length of ground_rects is greater than zero (which should always be true), then set the variable 'oldest_ground' to the first item in the list 'ground_rects'
    if len(ground_rects) > 0:
        oldest_ground = ground_rects[0]
    
    # if the rightmost coordinate of the oldest piece of ground is less than zero (offscreen), then remove that piece of ground from the list 'ground_rects'
    if oldest_ground.right < 0:
        ground_rects.pop(0)

    # create the variable 'keys' and assign a list of all keys press or not
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]: # check if the D key is pressed, then:
        # if the player's current speed is less than his maximum allowed speed, and he has room to move to the right, and the world is not scrolling, then increase his speed by his acceleration amount.
        if player_current_speed < player_max_speed and player_x+1 <= player_max_x and world_speed == 0:
            player_current_speed += player_acceleration

        # if the player's current x position is greater than or equal to his maximum allowed x coordinate (which should start the world scrolling), and the world is not yet scrolling at the maximum speed of the player, then add his acceleration to the current world scrolling speed
        # this ensures that the player's momentum transfers to and from the world scrolling smoothly.
        if player_x >= player_max_x and world_speed < player_max_speed:
            world_speed += player_acceleration

    if keys[pygame.K_a]: # check if the A key is pressed (player wannts to move left), then:
        # if the world is currently scrolling, subtract the player's acceleration from the world speed (the world scrolling has to slow to zero before the player should actually start moving left, due to his momentum)
        if world_speed > 0:
            world_speed -= player_acceleration

        # if the world speed is less than the player's acceleration (if this is true, then it should be zero, and never negative), set it to zero just to be safe.
        if world_speed < player_acceleration:
            world_speed = 0

        # if the player's current speed LEFT is less than his maximum allowed speed LEFT (notice the *-1), and there is still room for him to move left, AND the world is not scrolling, then add the player's acceleration to his movement LEFT (by subtacting the player's acceleration from his x speed, so that it goes negative, and he moves left)
        if player_current_speed > player_max_speed*-1 and player_x-1 >= player_min_x and world_speed == 0:
            player_current_speed -= player_acceleration

    # if both A and D are pressed or NEITHER are pressed AND the player is moving to the right, then subtract his acceleration value from his current speed, so he slows down.
    if ((keys[pygame.K_a] and keys[pygame.K_d]) or not (keys[pygame.K_a] or keys[pygame.K_d])) and player_current_speed > 0:
        player_current_speed -= player_acceleration

    # if both A and D are pressed or NEITHER are pressed AND the player is moving to the left, then add his acceleration value from his current speed, so he slows down.
    if ((keys[pygame.K_a] and keys[pygame.K_d]) or not (keys[pygame.K_a] or keys[pygame.K_d])) and player_current_speed < 0:
        player_current_speed += player_acceleration

    # if both A and D are pressed or NEITHER are pressed AND the world is currently scrolling, then subtract his acceleration value from the current world scrolling speed, so it slows down.
    if ((keys[pygame.K_a] and keys[pygame.K_d]) or not (keys[pygame.K_a] or keys[pygame.K_d])) and world_speed > 0:
        world_speed -= player_acceleration

    # if the player's current speed is greater than or equal to the player's acceleration value or -1* the acceleration value (the player is moving), then shift the player's x position by the current speed of the player
    if player_current_speed >= player_acceleration or player_current_speed <= -1*player_acceleration:
        player_x += player_current_speed

    # if the world scrolling speed is above 0 and the player is at his maximum x position, then scroll the world by the current world scrolling speed.
    if world_speed > 0 and player_x >= player_max_x:
        world_scroll += world_speed

# --- End Update Loop ---

# --- Begin Draw Loop ---

    screen.fill((173, 216, 230)) # fill the screen with a light blue colour (for the sky)

    # --- Begin Draw All Ground Pieces ---
    for ground in ground_rects:
        pygame.draw.rect(screen, (0,128,0), (ground.x - world_scroll, ground.y, ground.width, ground.height))
    # --- End Draw All Ground Pieces ---

    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_width, player_height)) # draw a rectangle which is the player
    
    # Debug Text Variable Declaraction
    text_surface = debug_font.render(f"Speed: {round(player_current_speed, 1)}", True, (0, 0, 0)) #render the font 'debug font' with the specified value, which is for the player's current speed, rounded to 1 decimal place, colour black.
    text_surface2 = debug_font.render(f"X: {round(player_x, 1)}", True, (0, 0, 0)) #render the font 'debug font' with the specified value, which is for the player's current x coordinate, rounded to 1 decimal place, colour black.
    text_world_scroll = debug_font.render(f"World Scroll: {round(world_scroll, 1)}", True, (0, 0, 0)) #render the font 'debug font' with the specified value, which is for the world_scroll value, rounded to 1 decimal place, colour black.
    text_world_speed = debug_font.render(f"World Speed: {round(world_speed, 1)}", True, (0, 0, 0)) #render the font 'debug font' with the specified value, which is for the worlds's current scrolling speed, rounded to 1 decimal place, colour black.

    # Get the rectangles/bounding box of the debug text elements
    text_rect = text_surface.get_rect()
    text_rect2 = text_surface2.get_rect()
    text_world_scroll_rect = text_world_scroll.get_rect()
    text_world_speed_rect = text_world_speed.get_rect()

    # Dynamically position the debug text so that it's correctly located at the top right
    text_rect.topright = (screen_height - 10, 10) # 10px from the top, 10px from the right
    text_rect2.topright = (screen_height - 10, 40) # 30px below text_rect
    text_world_scroll_rect.topright = (screen_height - 10, 70) # 30px below text_rect2
    text_world_speed_rect.topright = (screen_height - 10, 100) # 30px below text_world_scroll_rect

    # 'blit' the text onto the 'screen'
    screen.blit(text_surface, text_rect)
    screen.blit(text_surface2, text_rect2)
    screen.blit(text_world_scroll, text_world_scroll_rect)
    screen.blit(text_world_speed, text_world_speed_rect)

    # this wont actually render yet, we need to tell pygame that we're done drawing, and to now show the user.

    pygame.display.flip() # Flip the canvas so that the user can now see what we've drawn.

# --- End Draw Loop ---

    clock.tick(60) # Set the maximum framerate of the game Default = 60

# --- End Game Loop ---

# This code runs *after* the main game loop has finished:

pygame.quit() # This is the opposite of pygame.init(), this tells python to exit the app and shut down it's engines properly. It's important for a clean exit.