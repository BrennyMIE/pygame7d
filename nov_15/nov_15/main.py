import pygame # This imports the pygame library into the script, so that it's functions are available to be used.
from noise import pnoise1, pnoise2
import math
import random
# In Python, when you want to use a function from a library you've imported, you connect them with a dot (.). This is often called dot notation.

pygame.init() # This tells python: "Inside the pygame library, find the function called init, and run it; the parentheses are how you tell the program to run the specified function."

screen_width = 1920 # Create the variable screen_width. Default = 1280
screen_height = 1080 # Create the variable screen_height. Default = 720

screen = pygame.display.set_mode((screen_width, screen_height)) # this creates a variable 'screen' and assigns the value of the created surface using pygame.display.set_mode()

running = True # create the variable 'running' and set it's value to 'True'
clock = pygame.time.Clock() # Create the variable 'clock', and assigns the value returned from the function pygame.time.Clock()?
debug_font = pygame.font.Font(None, 30) # create the variable debug_font, and set it's font to None(default font), with size 30

# Define Tile Size
tile_width = 64  # create the variable tile_width, which specifies the height of the floor. Default = 100
tile_height = 64 # create the variable tile_height, which specifies the height of the floor. Default = 100
total_noise_scale = 2
noise_factor_x = 0.002 / total_noise_scale
noise_factor_y = 0.01 / total_noise_scale
# Load textures:
background_texture_src = pygame.image.load('world_background.png')
bg_texture = pygame.transform.scale(background_texture_src, (screen_width, screen_height))

ground_texture_biome1_botleft_src = pygame.image.load('ground_texture_plains_botleft.png')
ground_texture_biome1_botmid_src = pygame.image.load('ground_texture_plains_botmid.png')
ground_texture_biome1_botright_src = pygame.image.load('ground_texture_plains_botright.png')
ground_texture_biome1_midright_src = pygame.image.load('ground_texture_plains_midright.png')
ground_texture_biome1_mid_src = pygame.image.load('ground_texture_plains_mid.png')
ground_texture_biome1_midleft_src = pygame.image.load('ground_texture_plains_midleft.png')
ground_texture_biome1_topleft_src = pygame.image.load('ground_texture_plains_topleft.png')
ground_texture_biome1_topmid_src = pygame.image.load('ground_texture_plains_topmid.png')
ground_texture_biome1_topright_src = pygame.image.load('ground_texture_plains_topright.png')



ground_texture_biome2_src = pygame.image.load('ground_texture_jungle.png')
ground_texture_biome3_src = pygame.image.load('ground_texture_desert.png')
ground_texture_biome4_src = pygame.image.load('ground_texture_mountains.png')
ground_texture_biome5_src = pygame.image.load('ground_texture_tundra.png')

ground_texture = pygame.transform.scale(ground_texture_biome2_src, (tile_width, tile_height))

world_tiles = {}

player_sprite_src = pygame.image.load('player_sprite.png')
player_sprite_scaled = pygame.transform.scale(player_sprite_src, (tile_width, tile_height * 2))

enemy_sprite_src = pygame.image.load('enemy_sprite.png')
enemy_sprite = pygame.transform.scale(enemy_sprite_src, (tile_width, tile_height*2))
class enemyClass:
    def __init__(self, x, y, width, height):
        #Create a rect for position and collision
        self.rect = pygame.Rect(x, y, width, height)

        # Give each enemy it's own physics variables
        self.current_speed_x = 0
        self.current_speed_y = 0
        self.on_ground = False

# Define the zone where things must be rendered
renderzone_right = screen_width + tile_width # add a buffer of 1 tile (!!!!!!!!currently negative 1 tile just so I can see what's going on!!!!!!!)
renderzone_left = 0 - tile_width # also add the 1 tile buffer (bllarrghhhh inverted for testing!!!!!!)
renderzone_top = 0 - tile_height # probably not needed
renderzone_bottom = screen_height + tile_height # also probably not needed
ground_level = screen_height - tile_height
new_ground_y_max = ground_level
new_ground_y_min = 0

#define the random seed for the world generation
seed_x = random.randint(0, 1000000)
seed_y = random.randint(0, 1000000)
print({seed_x, seed_y})

world_scroll = 0 # initialise the world_scroll variable, which defines how far the world has currently scrolled.
world_speed = 0 # initialise the speed that the world is currently scrolling. Default = 0

# generate a list of ground rectangles and initilise it with a single rectangle.
ground_rects = [pygame.Rect(0, screen_height - tile_height, tile_width, tile_height)] # Create the list ground_rects, which will contain a list of rectangles used for drawing the ground. Initialise it with a single rectangle that is the height of the floor, and the width of the screen.
generated_world_edge_x = tile_width
world_tiles = {}

#create a new, empty list to store enemies that are currently in the world:
world_enemies = []
enemy_spawn_chance = 0

player_width = tile_width # create the variable for the player_width. Default = 50
player_height = tile_height*2 # create the variable for the player_height. Default = 50

gravity = 2 # initialise the speed of gravity. DEFAULT 2 
jump_force = gravity * 14 # set the force with which the player jumps

player_x = 0#screen_width / 2 - player_width / 2 # create the variable player_x, which initialises the player's x position. Default value = screen_width/2 - player_width/2 - which is the middle of the screen.
player_y = 0#screen_height - tile_height - player_height # create the variable player_y, which initialises the player's y position. Default value = screen_height - tile_height - player_height - which is standing on the ground
player_acceleration = 0.4 # define the player's acceleration speed. Default = 0.2
player_sliding_friction = 0.1
score = 0 # initialise the score as 0

player_current_speed_x = 0 # Initialise the player's current x speed. Default = 0
player_current_speed_y = 0 # Initialise the player's current y speed. Default = 0
player_max_speed_x = 7 # Define the player's maximum speed, in pixels per cycle. DEFAULT 7
player_max_speed_y = 50 # Define the player's maximum y speed, in pixels per cycle.
player_min_x = 0 # Define the minimum allowed x coordinate of the player
player_max_x = world_scroll + screen_width / 2 - player_width / 2 + player_width # define the maximum allowed x value for the player, when accounting for the size of the window.

biome_size = 20000 # Define how many pixels wide each biome / level is to be Default = 20000
biome_1 = 'Mountains'
biome_2 = 'Desert'
biome_3 = 'Jungle'
biome_4 = 'Tundra'
biome_5 = 'Plains'
current_biome = biome_1

# --- Begin Game Loop ---

while running: # everything below this will happen as long as 'running' is 'True'
    # if the player's x coordinate is less than the maximum allowed x coordinate, then set the current world scrolling speed to zero.
    if player_x < player_max_x:
        world_speed = 0

    # if the current world scrolling speed is less than the speed of acceleration per cycle (which is also the minimum possible speed the player can be moving), then set it to zero, to avoid any weirdness that might cause the world to scroll very slowly unintentionally
    if world_speed < player_acceleration:
        world_speed = 0

    # if the player's x coordinate is greater than or equal to the maximum allowed x coordinate and the world is not currently scrolling, and the player is moving, then transfer the player speed into world scrolling speed (which will provide the illusion that the player is moving 'forward' in the game world)
    if player_x >= player_max_x and world_speed == 0 and player_current_speed_x > 0:
        world_speed = player_current_speed_x
    
    # If the players x positions is less than or equal to the minimum allowed x position (he's not allowed here!) then move him to his minimum allowed x position, and set his speed to zero.
    if player_x <= player_min_x:
        player_x = player_min_x
        player_current_speed_x = 0

    # If the players current speed is less than the minimum allowed speed in either direction (one cycle of acceleration), then set his speed to zero (to prevent any weird things happening where he accidentally ends up moving by a fraction of this amount)
    if player_current_speed_x < player_acceleration and player_current_speed_x > -player_acceleration:
        player_current_speed_x = 0

# --- Begin Update Loop ---
    enemy_spawn_chance = world_scroll / 10000

    if player_x > biome_size and player_x < biome_size * 2:
        current_biome = biome_2
    if player_x > biome_size*2 and player_x < biome_size * 3:
        current_biome = biome_3
    if player_x > biome_size*3 and player_x < biome_size * 4:
        current_biome = biome_4
    if player_x > biome_size*4 and player_x < biome_size * 5:
        current_biome = biome_5
    if current_biome == biome_1:
        ground_texture_botleft = pygame.transform.scale(ground_texture_biome1_botleft_src, (tile_width, tile_height))
        ground_texture_botmid = pygame.transform.scale(ground_texture_biome1_botmid_src, (tile_width, tile_height))
        ground_texture_botright = pygame.transform.scale(ground_texture_biome1_botright_src, (tile_width, tile_height))
        ground_texture_midleft = pygame.transform.scale(ground_texture_biome1_midleft_src, (tile_width, tile_height))
        ground_texture_mid = pygame.transform.scale(ground_texture_biome1_mid_src, (tile_width, tile_height))
        ground_texture_midright = pygame.transform.scale(ground_texture_biome1_midright_src, (tile_width, tile_height))
        ground_texture_topleft = pygame.transform.scale(ground_texture_biome1_topleft_src, (tile_width, tile_height))
        ground_texture_topmid = pygame.transform.scale(ground_texture_biome1_topmid_src, (tile_width, tile_height))
        ground_texture_topright = pygame.transform.scale(ground_texture_biome1_topright_src, (tile_width, tile_height))
    if current_biome == biome_2:
        ground_texture = pygame.transform.scale(ground_texture_biome2_src, (tile_width, tile_height))
    if current_biome == biome_3:
        ground_texture = pygame.transform.scale(ground_texture_biome3_src, (tile_width, tile_height))
    if current_biome == biome_4:
        ground_texture = pygame.transform.scale(ground_texture_biome4_src, (tile_width, tile_height))
    if current_biome == biome_5:
        ground_texture = pygame.transform.scale(ground_texture_biome5_src, (tile_width, tile_height))

    # Update the minimum and maximum allowed x position for the player:
    player_max_x = world_scroll + screen_width / 2 - player_width / 2 + player_width
    player_min_x = world_scroll
    # set player on ground to false every frame
    player_on_ground = False
    can_jump = 0

    #Make the player fall according to gravity:
    if player_current_speed_y < player_max_speed_y and not player_on_ground:
        player_current_speed_y += gravity

    # if the right side of the latest piece of ground, minus the world_scroll value, is less than or equal to the width of the screen, then create a new piece of ground, 'new_ground', identical to the previous piece, then append it to the list ground_rects
    if generated_world_edge_x - world_scroll <= renderzone_right:
        for y_pos in range(0, screen_height-tile_height, tile_height):
            noise_value = pnoise2(((generated_world_edge_x * noise_factor_x) + seed_x), ((y_pos * noise_factor_y) + seed_y))
            enemy_spawn_value = random.randint(0, 100)
            if noise_value > 0.15:
                new_ground = pygame.Rect(generated_world_edge_x,y_pos,tile_width, tile_height)
                ground_rects.append(new_ground)
                grid_x = generated_world_edge_x // tile_width
                grid_y = y_pos // tile_height
                world_tiles[(grid_x, grid_y)] = 'ground' # Store this tile in our dictionary
                if enemy_spawn_value < enemy_spawn_chance:
                    new_enemy = enemyClass(generated_world_edge_x, y_pos-tile_height*2, tile_width, tile_height*2)
                    world_enemies.append(new_enemy)
        generated_world_edge_x += tile_width

        enemy_spawn_value = random.randint(0, 100)
        if enemy_spawn_value < enemy_spawn_chance:
                    new_enemy = enemyClass(generated_world_edge_x, y_pos-tile_height, tile_width, tile_height*2)
                    world_enemies.append(new_enemy)
    
    # while the length of ground_rects is greater than zero (which should always be true), then set the variable 'oldest_ground' to the first item in the list 'ground_rects'
    while len(ground_rects) > 0:
        oldest_ground = ground_rects[0]
    
        # if the rightmost coordinate of the oldest piece of ground minus the distance the world has scrolled is less than zero (offscreen), then remove that piece of ground from the list 'ground_rects'
        if oldest_ground.right - world_scroll < renderzone_left:
            ground_rects.pop(0)
            grid_x = oldest_ground.x // tile_width
            grid_y = oldest_ground.y // tile_height
            if (grid_x, grid_y) in world_tiles:
                del world_tiles[(grid_x, grid_y)]
        # if the above is not true, exit the while loop for this frame.
        else:
            break

    while len(world_enemies) > 0:
        oldest_enemy = world_enemies[0]
    
        # if the rightmost coordinate of the oldest piece of ground minus the distance the world has scrolled is less than zero (offscreen), then remove that piece of ground from the list 'ground_rects'
        if oldest_enemy.rect.right - world_scroll < renderzone_left:
            world_enemies.pop(0)
        # if the above is not true, exit the while loop for this frame.
        else:
            break

    # create the variable 'keys' and assign a list of all keys press or not
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d] and sliding == 0: # check if the D key is pressed, then:
        # if the player's current speed is less than his maximum allowed speed, and he has room to move to the right, and the world is not scrolling, then increase his speed by his acceleration amount.
        if player_current_speed_x < player_max_speed_x:
            player_current_speed_x += player_acceleration

        # if the player's current x position is greater than or equal to his maximum allowed x coordinate (which should start the world scrolling), and the world is not yet scrolling at the maximum speed of the player, then add his acceleration to the current world scrolling speed
        # this ensures that the player's momentum transfers to and from the world scrolling smoothly.
        if player_x >= player_max_x and world_speed < player_max_speed_x:
            world_speed += player_acceleration

    if keys[pygame.K_a] and sliding == 0: # check if the A key is pressed (player wannts to move left), then:
        # if the world is currently scrolling, subtract the player's acceleration from the world speed (the world scrolling has to slow to zero before the player should actually start moving left, due to his momentum)
        if world_speed > 0:
            world_speed -= player_acceleration

        # if the world speed is less than the player's acceleration (if this is true, then it should be zero, and never negative), set it to zero just to be safe.
        if world_speed < player_acceleration:
            world_speed = 0

        # if the player's current speed LEFT is less than his maximum allowed speed LEFT (notice the *-1), and there is still room for him to move left, AND the world is not scrolling, then add the player's acceleration to his movement LEFT (by subtacting the player's acceleration from his x speed, so that it goes negative, and he moves left)
        if player_current_speed_x > -player_max_speed_x:
            player_current_speed_x -= player_acceleration

    # if both A and D are pressed or NEITHER are pressed AND the player is moving to the right, then subtract his acceleration value from his current speed, so he slows down.
    if ((keys[pygame.K_a] and keys[pygame.K_d]) or not (keys[pygame.K_a] or keys[pygame.K_d])) and player_current_speed_x > 0:
        player_current_speed_x -= player_acceleration

    # if both A and D are pressed or NEITHER are pressed AND the player is moving to the left, then add his acceleration value from his current speed, so he slows down.
    if ((keys[pygame.K_a] and keys[pygame.K_d]) or not (keys[pygame.K_a] or keys[pygame.K_d])) and player_current_speed_x < 0:
        player_current_speed_x += player_acceleration

    # if both A and D are pressed or NEITHER are pressed AND the world is currently scrolling, then subtract his acceleration value from the current world scrolling speed, so it slows down.
    if ((keys[pygame.K_a] and keys[pygame.K_d]) or not (keys[pygame.K_a] or keys[pygame.K_d])) and world_speed > 0:
        world_speed -= player_acceleration

    if keys[pygame.K_LSHIFT]:
        player_sprite = pygame.transform.rotate(player_sprite_scaled, -90)
        player_rectangle = player_sprite.get_rect(center = (player_x - world_scroll, player_y + tile_height))
        player_width = tile_width*2
        player_height = tile_height
        if sliding == 0 and player_current_speed_x < player_max_speed_x*1.1 and player_current_speed_x > -player_max_speed_x*1.1:
            player_current_speed_x *=2
            player_current_speed_y -= jump_force*0.35
            sliding = 1
        if player_current_speed_x > 0:
            player_current_speed_x -= player_sliding_friction
        else:
            player_current_speed_x += player_sliding_friction

    else:
        player_sprite = pygame.transform.rotate(player_sprite_scaled, 0)
        player_rectangle = player_sprite.get_rect(center = (player_x- world_scroll, player_y + tile_height))
        player_width = tile_width
        player_height = tile_height*2
        sliding = 0

    if player_current_speed_y < 0:
        player_y += player_current_speed_y
        # define the player bounding box just before detecting collision, so that it's value is updated every frame after the player has moved.
        player_bbox = pygame.Rect(player_x+(player_width*0.1), player_y+(player_height*0.2), player_width*0.8, player_height*0.8)
        for ground in ground_rects:
        # Now we're "inside" the loop.
        # The 'ground' variable holds the block we're currently looking at.

        # Move the player upwards if he's inside the ground (because he shouldn't be)
            if player_bbox.colliderect(ground): #detect if the player bounding box is colliding with ANY piece of ground.
                player_y = ground.y + player_height
                player_current_speed_y = 0
                break
    
    if (player_current_speed_y > 0) and not player_on_ground:
        player_y += player_current_speed_y
        # define the player bounding box just before detecting collision, so that it's value is updated every frame after the player has moved.
        player_bbox = pygame.Rect(player_x+(player_width*0.1), player_y+(player_height*0.2), player_width*0.8, player_height*0.8)
        for ground in ground_rects:
        # Now we're "inside" the loop.
        # The 'ground' variable holds the block we're currently looking at.

        # Move the player upwards if he's inside the ground (because he shouldn't be)
            if player_bbox.colliderect(ground): #detect if the player bounding box is colliding with ANY piece of ground.
                player_y = ground.y - player_height
                player_current_speed_y = 0
                player_on_ground = True
                can_jump = 1
                break

    # if the player's current speed is greater than or equal to the player's acceleration value or -1* the acceleration value (the player is moving), then shift the player's x position by the current speed of the player
    if player_current_speed_x >= player_acceleration:
        player_x += player_current_speed_x
        player_bbox = pygame.Rect(player_x+(player_width*0.1), player_y+(player_height*0.2), player_width*0.8, player_height*0.8)
        for ground in ground_rects:
            # Now we're "inside" the loop.
            # The 'ground' variable holds the block we're currently looking at.

            # Move the player upwards if he's inside the ground (because he shouldn't be)
            if player_bbox.colliderect(ground): #detect if the player bounding box is colliding with ANY piece of ground.
                player_x = ground.x - player_width
                player_current_speed_x = 0
                break

    if player_current_speed_x <= -player_acceleration:
        player_x += player_current_speed_x
        player_bbox = pygame.Rect(player_x+(player_width*0.1), player_y+(player_height*0.2), player_width*0.8, player_height*0.8)
        for ground in ground_rects:
            # Now we're "inside" the loop.
            # The 'ground' variable holds the block we're currently looking at.

            # Move the player upwards if he's inside the ground (because he shouldn't be)
            if player_bbox.colliderect(ground): #detect if the player bounding box is colliding with ANY piece of ground.
                player_x = ground.x + player_width
                player_current_speed_x = 0
                break

    for enemy in world_enemies:
        enemy.on_ground = False
        enemy.current_speed_x = -2
        if enemy.current_speed_y < player_max_speed_y and not enemy.on_ground:
            enemy.current_speed_y += gravity
        
        if enemy.current_speed_y < 0:
            enemy.rect.y += enemy.current_speed_y
            for ground in ground_rects:
                if enemy.rect.colliderect(ground): #detect if the player bounding box is colliding with ANY piece of ground.
                    enemy.rect.y = ground.y + enemy.rect.height
                    enemy.current_speed_y = 0
                    break
        
        if (enemy.current_speed_y > 0) and not enemy.on_ground:
            enemy.rect.y += enemy.current_speed_y
            for ground in ground_rects:
                if enemy.rect.colliderect(ground): #detect if the enemy bounding box is colliding with ANY piece of ground.
                    enemy.rect.y = ground.y - enemy.rect.height
                    enemy.current_speed_y = 0
                    enemy.on_ground = True
                    break
        if enemy.current_speed_x > 0:
            enemy.rect.x += enemy.current_speed_x
            for ground in ground_rects:
                    enemy.rect.x = ground.x - enemy.rect.width
                    enemy.current_speed_x = 0
                    break

        if enemy.current_speed_x < 0:
            enemy.rect.x += enemy.current_speed_x
            for ground in ground_rects:
                    enemy.rect.x = ground.x + enemy.rect.width
                    enemy.current_speed_x = 0
                    break

    # if the world scrolling speed is above 0 and the player is at his maximum x position, then scroll the world by the current world scrolling speed.
    if world_speed > 0 and player_x >= player_max_x:
        world_scroll += world_speed
        score += world_speed/100
    
    if keys[pygame.K_SPACE]: # If the spacebar is currently pressed:
        if can_jump == 1 and sliding == 0: # and can jump is 1 (the player is on the ground)
            player_current_speed_y -= jump_force # then jump
        else:
            player_current_speed_y -= jump_force/jump_force  # allow player to jump higher if he holds the jump button

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
        
# --- End Update Loop ---

# --- Begin Draw Loop ---

    # Draw the background texture which is used for the sky
    screen.blit(bg_texture, (0,0))

    # --- Begin Draw All Ground Pieces ---
    for ground in ground_rects:
        # Get the grid position of the tile we are about to draw
        grid_x = ground.x // tile_width
        grid_y = ground.y // tile_height
        
        # check for all 4 cardinal neighbours
        has_above = (grid_x, grid_y - 1) in world_tiles
        has_below = (grid_x, grid_y + 1) in world_tiles
        has_left = (grid_x - 1, grid_y) in world_tiles
        has_right = (grid_x + 1, grid_y) in world_tiles

        # choose the correct texture
        texture_to_draw = ground_texture_mid #default to mid


        #middlemiddle
        if has_above and has_right and has_below and has_left:
            texture_to_draw = ground_texture_mid

        #edges
        if not has_below: # bottom edge
            texture_to_draw = ground_texture_botmid
        if not has_above: # top edge
            texture_to_draw = ground_texture_topmid
        if not has_left: # left edge
            texture_to_draw = ground_texture_midleft
        if not has_right: # right edge
            texture_to_draw = ground_texture_midright

        # check every single edge and corner
        #corners
        if not has_below and not has_left: #botleft
            texture_to_draw = ground_texture_botleft
        if not has_below and not has_right: # botright
            texture_to_draw = ground_texture_botright
        if not has_above and not has_left: # topleft
            texture_to_draw = ground_texture_topleft
        if not has_above and not has_right: #topright
            texture_to_draw = ground_texture_topright

        
        

        # draw the chosen texture
        screen.blit(texture_to_draw, (ground.x - world_scroll, ground.y))

    # --- End Draw All Ground Pieces ---

    # --- Begin Draw All Enemies ---
    for enemy in world_enemies:
        screen.blit(enemy_sprite, (enemy.rect.x - world_scroll, enemy.rect.y))
    # --- End draw all enemies ---

    screen.blit(player_sprite, player_rectangle) # Draw the player sprite
    
    # Score Text variable declaration:
    score_text = debug_font.render(f"Score: {round(score)}", True, (30, 30, 30)) # render the font 'debug font' with the value of the current score, colour off-black.

    # get the rectangle/bounding box of the score element:
    score_text_bbox = score_text.get_rect()

    # Position the score text so that it's located at the top middle of the screen:
    score_text_bbox.topleft = (screen_width / 2 - score_text_bbox.width / 2, 30) #since we're using the left coordinate, we need to subtract half of the width of the score bounding box to ensure it's properly centred. And place it 30px from the top of the screen.

    # blit the text onto the 'screen'
    screen.blit(score_text, score_text_bbox)

    # Debug Text Variable Declaraction
    text_surface = debug_font.render(f"Speed: {round(player_current_speed_x, 1)}", True, (0, 0, 0)) #render the font 'debug font' with the specified value, which is for the player's current speed, rounded to 1 decimal place, colour black.
    text_surface2 = debug_font.render(f"X: {round(player_x, 1)}", True, (0, 0, 0)) #render the font 'debug font' with the specified value, which is for the player's current x coordinate, rounded to 1 decimal place, colour black.
    text_world_scroll = debug_font.render(f"World Scroll: {round(world_scroll, 1)}", True, (0, 0, 0)) #render the font 'debug font' with the specified value, which is for the world_scroll value, rounded to 1 decimal place, colour black.
    text_world_speed = debug_font.render(f"World Speed: {round(world_speed, 1)}", True, (0, 0, 0)) #render the font 'debug font' with the specified value, which is for the worlds's current scrolling speed, rounded to 1 decimal place, colour black.

    # Get the rectangles/bounding box of the debug text elements
    text_rect = text_surface.get_rect()
    text_rect2 = text_surface2.get_rect()
    text_world_scroll_rect = text_world_scroll.get_rect()
    text_world_speed_rect = text_world_speed.get_rect()

    # Dynamically position the debug text so that it's correctly located at the top right
    text_rect.topright = (screen_width - 10, 10) # 10px from the top, 10px from the right
    text_rect2.topright = (screen_width - 10, 40) # 30px below text_rect
    text_world_scroll_rect.topright = (screen_width - 10, 70) # 30px below text_rect2
    text_world_speed_rect.topright = (screen_width - 10, 100) # 30px below text_world_scroll_rect

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