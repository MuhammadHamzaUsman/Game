import random
import time
import os

enemy_type = {
    1 : {
        "health" : 1,
        "sprite" : "👽"
        },
    2 : {
        "health" : 2,
        "sprite" : "👾"
        },
    3 : {
        "health" : 3,
        "sprite" : "🛸"
        }
}
enemy_config = [2]#order in which enemy should appear
enemy_layer = len(enemy_config) #this actualy does upper thing
enemy_horizontal_tick = 5
enemy_decend_randomness = 5
enemy_decend_tick = 10
enemy_sprites = []
display_width = 11
display_height = 10
display_border = "⬛"
start_end_border = f"{display_border}" * 13
enemy_count = 0
empty_cell = "  "
enemy_bullet_limit = 3
enemy_bullet = "🔶"
enemy_bullet_tick = 3
player = "🚔"
player_bullet = "🔷"
player_life = 3
life_sprite = "❤"
consumed_life_sprite = "🖤"
player_position = int(display_width / 2)
collision = "💥"
display = []
temp_display = []
layer_index = 0
cell_index = 0
points = 0
enemy_healths = []
collision_to_be_replaced = []
enemy_decend_limit = 6
enemy_decend_list = []
all_enemy_decend_chance = 1
empty_cell_list = [empty_cell for x in range(display_width)]
game_tick = 0
is_game_active = True
frame_per_second = 1/30
main_menu_choice = ""
control_menu_choice = ""
game_level = 1
is_random_position = False
random_position = "Off"
game_levels = {
    1 : {
        "enemy_config" : [1],
        "enemy_layer" : len([1]),
        "all_enemy_decend_chance" : 1,
        "enemy_decend_limit" : 6,
        "player_life" : 3,
        "enemy_bullet_limit" : 3,
        "enemy_bullet_tick" : 3,
        "enemy_horizontal_tick" : 5,
        "enemy_decend_randomness" : 5,
        "enemy_decend_tick" : 10
    },
    2 : {
        "enemy_config" : [2,1],
        "enemy_layer" : len([2,1]),
        "all_enemy_decend_chance" : 10,
        "enemy_decend_limit" : 7,
        "player_life" : 2,
        "enemy_bullet_limit" : 4,
        "enemy_bullet_tick" : 2,
        "enemy_horizontal_tick" : 4,
        "enemy_decend_randomness" : 7,
        "enemy_decend_tick" : 7
    },
    3 : {
        "enemy_config" : [3,2,1],
        "enemy_layer" : len([3,2,1]),
        "all_enemy_decend_chance" : 20,
        "enemy_decend_limit" : 8,
        "player_life" : 1,
        "enemy_bullet_limit" : 5,
        "enemy_bullet_tick" : 1,
        "enemy_horizontal_tick" : 2,
        "enemy_decend_randomness" : 10,
        "enemy_decend_tick" : 5
    }
}
game_level_list = [list(i.values()) for i in game_levels.values()]


#for creating display
def create_display(display_height, display_width, display) :
    for i in range(display_height) :
        temp_layer = []
        for j in range(0,display_width) :
            temp_layer.append(empty_cell)
        display.append(temp_layer)

#for displaying lives and points 
def display_lives_points(player_life, life_sprite, points) :
        pass

#for displaying display
def display_screen(display, frame_per_second, player_life, life_sprite, points) :
    os.system("cls")
    #print("\033[0;0H")
    string = ""
    for i in range(1, 4) :
        if i <= player_life :
            string += f"{life_sprite} "
        else :
            string += f"{consumed_life_sprite} "
    print(f"Lives: {string}\nPoints: {points}")
    print(start_end_border)
    for layer in display :
        print(display_border, end = "")
        for cell in layer :
            print(cell, end = "")
        print(display_border)
    print(start_end_border)
    print("\t  ", end = "") 
    time.sleep(frame_per_second)

#for creating list that contains collision to be replaced
def create_collision_to_be_replaced_list(display_height, display_width, empty_cell, collision_to_be_replaced) :
    for layer in range(display_height) :
        temp_layer = []
        for cell in range(display_width) :
            temp_layer.append(empty_cell)
        collision_to_be_replaced.append(temp_layer)

#for placing player
def place_player(player, player_position, display, points, player_life) :
    display[-1][player_position] = player
    display_lives_points(player_life, life_sprite, points)
    display_screen(display, frame_per_second, player_life, life_sprite, points)

#for creating list that contains health of each enemy
def create_enemy_health_list(enemy_type, enemy_config, display_height, display_width, empty_cell, enemy_layer, enemy_healths) :
    #for creating list
    for layer in range(display_height) :
        temp_layer = []
        for cell in range(display_width) :
            temp_layer.append(empty_cell)
        enemy_healths.append(temp_layer)
    #for inserting enemy healths
    layer_index = 0
    cell_index = 0
    for layer in enemy_healths :
        cell_index = 0
        for cell in layer :
            if cell == empty_cell :
                enemy_healths[layer_index][cell_index] = enemy_type[enemy_config[layer_index]]["health"]
            cell_index += 1
        layer_index += 1
        if layer_index >= enemy_layer :
            break
    #end of creating health list

#for inserting enemies 
def place_enemies(enemy_type, enemy_config, empty_cell, enemy_layer, collision, display, enemy_healths, enemy_sprites) :
    layer_index = 0
    cell_index = 0
    for layer in display :
        cell_index = 0
        for cell in layer :
            if cell == empty_cell and (not enemy_healths[layer_index][cell_index] == 0) :
                display[layer_index][cell_index] = enemy_type[enemy_config[layer_index]]["sprite"]
            elif cell in enemy_sprites :
                pass
            else :
                display[layer_index][cell_index] = collision
            cell_index += 1
        layer_index += 1
        if layer_index >= enemy_layer :
            break
    display_lives_points(player_life, life_sprite, points)
    display_screen(display, frame_per_second, player_life, life_sprite, points)
    #end of placing enemies

#for creating enemy sprite list accordiing to order given in table
def create_enemy_sprites_list(enemy_type, enemy_sprites) :
    for info in enemy_type.values() :
        enemy_sprites.append(info["sprite"])

#for insering enemy bullet   
def place_enemy_bullet(empty_cell, enemy_bullet_limit, enemy_bullet, display, enemy_sprites, points, player_life) :
    #eblist = enemy bullet list which stores cell in which bullet will appear
    eblist = []
    while len(eblist) < enemy_bullet_limit :
        eblist_index = random.randint(0,9)
        if (not eblist_index in eblist) :
            eblist.append(eblist_index)
    eblist.sort()
    #end of eblist loop
    #enemy bullet loop for placing bullet in display
    layer_index = 1
    cell_index = 0
    for bullet_spawn_cell in eblist :
        bullet_placed = False
        layer_index = 0
        for layer in display :
            cell_index = 0
            for cell in layer :
                if cell == empty_cell and cell_index == bullet_spawn_cell and display[layer_index - 1][cell_index] in enemy_sprites :
                    display[layer_index][cell_index] = enemy_bullet
                    bullet_placed = True
                cell_index += 1
                if bullet_placed :
                    break
            layer_index += 1
            if bullet_placed :
                    break
    display_lives_points(player_life, life_sprite, points)
    display_screen(display, frame_per_second, player_life, life_sprite, points)
    #end of bullet placing

#for lowering enemy bullet 
#mostly done idea using player position i can re display player after its place was taken by collision same in player movment
def lower_enemy_bullet(empty_cell, enemy_bullet, player, player_bullet, player_life, collision, display, points) :
    #for copying display to temp display
    temp_display = []
    for layer in display :
        temp_layer = layer[:]
        temp_display.append(temp_layer)
    #removing enemy bullet in temp display
    layer_index = 0
    cell_index = 0
    for layer in temp_display :
        cell_index = 0
        for cell in layer :
            if cell == enemy_bullet :
                temp_display[layer_index][cell_index] = empty_cell
            cell_index += 1
        layer_index += 1
    #checking where enemy bullet is, clearing it from display and copying it one layer below on temp display
    layer_index = 9
    cell_index = 0
    for layer in reversed(display) :
        cell_index = 0
        for cell in layer :
            if cell == enemy_bullet :
                bullet_index = layer.index(enemy_bullet)
                display[layer_index][bullet_index] = empty_cell
                if layer_index < 9 :
                    if display[layer_index + 1][cell_index] == player_bullet :
                        temp_display[layer_index + 1][bullet_index] = collision
                    elif display[layer_index + 1][cell_index] == player :
                        player_life -= 1
                        temp_display[layer_index][bullet_index] = collision
                    elif display[layer_index + 1][cell_index] == empty_cell :
                        temp_display[layer_index + 1][cell_index] = enemy_bullet
                    else :
                        temp_display[layer_index][cell_index] = enemy_bullet
                elif layer_index == 10 :
                    temp_display[layer_index][bullet_index] = empty_cell
            cell_index += 1
        layer_index -= 1
    #for copying temp display to display
    display = []
    for layer in temp_display :
        temp_layer = layer[:]
        display.append(temp_layer)
    display_lives_points(player_life, life_sprite, points)
    display_screen(display, frame_per_second, player_life, life_sprite, points)
    return display, player_life
    #end of lowering

#for raising player bullet 
def raise_player_bullet(enemy_sprites, empty_cell, enemy_bullet, player_bullet, collision, display, points, enemy_healths, collision_to_be_replaced, player_life):
    #for copying display to temp display
    temp_display = []
    for layer in display :
        temp_layer = layer[:]
        temp_display.append(temp_layer) 
    #for clearing temp display of all player bullets
    layer_index = 0
    cell_index = 0
    for layer in temp_display :
        cell_index = 0
        for cell in layer :
            if cell == player_bullet :
                temp_display[layer_index][cell_index] = empty_cell
            cell_index += 1
        layer_index += 1
    #checking where player bullet is, clearing it from display and copying it one layer below on temp display
    layer_index = 0
    cell_index = 0
    for layer in display :
        cell_index = 0
        for cell in layer :
            if cell == player_bullet :
                bullet_index = layer.index(player_bullet)
                display[layer_index][bullet_index] = empty_cell
                if layer_index > 0 :
                    if display[layer_index - 1][cell_index] == enemy_bullet :
                        temp_display[layer_index - 1][bullet_index] = collision
                    elif display[layer_index - 1][cell_index] in enemy_sprites :
                        points += 1
                        enemy_healths[layer_index - 1][cell_index] -= 1
                        if not enemy_healths[layer_index - 1][cell_index] == 0 :
                            collision_to_be_replaced[layer_index - 1][cell_index] = display[layer_index - 1][cell_index]
                        temp_display[layer_index - 1][bullet_index] = collision
                    else :
                        temp_display[layer_index - 1][bullet_index] = player_bullet
                elif layer_index == 0 :
                    if display[layer_index][cell_index] in enemy_sprites :
                        temp_display[layer_index][bullet_index] = collision
                        enemy_healths[layer_index][cell_index] -= 1
                        if not enemy_healths[layer_index][cell_index] == 0 :
                            collision_to_be_replaced[layer_index][cell_index] = display[layer_index - 1][cell_index]
                        temp_display[layer_index - 1][bullet_index] = collision
                        points += 1
                    elif display[layer_index][cell_index] == empty_cell :
                        temp_display[layer_index][bullet_index] = empty_cell
            cell_index += 1
        layer_index += 1
    #for copying temp display to display
    display = []
    for layer in temp_display :
        temp_layer = layer[:]
        display.append(temp_layer)
    display_lives_points(player_life, life_sprite, points)
    display_screen(display, frame_per_second, player_life, life_sprite, points)
    return display, points
    #end of raising

#player movment and shoot
def player_control(empty_cell, enemy_bullet, player, player_bullet, player_life, player_position, collision, display, points):
    user_input = input("Enter: ").lower()
    if user_input == "d" :
        if not player_position == 10 :
            if display[-1][player_position + 1] == empty_cell :
                display[-1][player_position] = empty_cell
                player_position += 1
                display[-1][player_position] = player
            elif not display[-1][player_position + 1] == empty_cell :
                display[-1][player_position + 1] = collision
                player_life -= 1
        elif player_position == 10 :
            if display[-1][0] == empty_cell :
                display[-1][player_position] = empty_cell
                player_position = 0
                display[-1][0] = player
            elif not display[-1][0] == empty_cell :
                display[-1][0] = collision
                player_life -= 1
    elif user_input == "a" :
        if not player_position == 0 :
            if display[-1][player_position - 1] == empty_cell :
                display[-1][player_position] = empty_cell
                player_position -= 1
                display[-1][player_position] = player
            elif not display[-1][player_position - 1] == empty_cell :
                display[-1][player_position - 1] = collision
                player_life -= 1
        elif player_position == 0 :
            if display[-1][10] == empty_cell :
                display[-1][player_position] = empty_cell
                player_position = 10
                display[-1][10] = player
            elif not display[-1][10] == empty_cell :
                display[-1][10] = collision
                player_life -= 1
    elif user_input == "s" :
        if display[-2][player_position] == empty_cell :
            display[-2][player_position] = player_bullet
        elif display[-2][player_position] == enemy_bullet :
            display[-2][player_position] = collision
    display_lives_points(player_life, life_sprite, points)
    display_screen(display, frame_per_second, player_life, life_sprite, points)
    return player_life, player_position
    #end of player movment and shoot

#for enemy movment all the way to right then left
def enemy_movment_horizontal(enemy_sprites, empty_cell, collision, display, enemy_healths, points, player_life):
    layer_index = 0
    cell_index = 0
    for layer in display :
        cell_index = 0
        for enemy_sprite in enemy_sprites :
            if enemy_sprite in layer :
                for cell in layer :
                    if cell in enemy_sprites :
                        if cell_index > 0 and cell_index < 10 :
                            if (display[layer_index][cell_index + 1] == empty_cell or display[layer_index][cell_index + 1] == collision) and (enemy_healths[layer_index][cell_index + 1] == 0) and (random.randint(1, 100) < 50 == 0):
                                    display[layer_index][cell_index + 1] = display[layer_index][cell_index]
                                    display[layer_index][cell_index] = empty_cell
                                    enemy_healths[layer_index][cell_index + 1] = enemy_healths[layer_index][cell_index]
                                    enemy_healths[layer_index][cell_index] = 0
                            elif (display[layer_index][cell_index - 1] == empty_cell or display[layer_index][cell_index - 1] == collision) and (enemy_healths[layer_index][cell_index - 1] == 0) :
                                    display[layer_index][cell_index - 1] = display[layer_index][cell_index]
                                    display[layer_index][cell_index] = empty_cell
                                    enemy_healths[layer_index][cell_index - 1] = enemy_healths[layer_index][cell_index]
                                    enemy_healths[layer_index][cell_index] = 0
                        elif cell_index == 0 :
                            if (display[layer_index][cell_index + 1] == empty_cell or display[layer_index][cell_index + 1] == collision) and (enemy_healths[layer_index][cell_index + 1] == 0) :
                                    display[layer_index][cell_index + 1] = display[layer_index][cell_index]
                                    display[layer_index][cell_index] = empty_cell
                                    enemy_healths[layer_index][cell_index + 1] = enemy_healths[layer_index][cell_index]
                                    enemy_healths[layer_index][cell_index] = 0
                        elif cell_index == 10 :
                            if (display[layer_index][cell_index - 1] == empty_cell or display[layer_index][cell_index - 1] == collision) and (enemy_healths[layer_index][cell_index - 1] == 0) :
                                    display[layer_index][cell_index - 1] = display[layer_index][cell_index]
                                    display[layer_index][cell_index] = empty_cell
                                    enemy_healths[layer_index][cell_index - 1] = enemy_healths[layer_index][cell_index]
                                    enemy_healths[layer_index][cell_index] = 0
                    cell_index += 1
        layer_index += 1
    display_lives_points(player_life, life_sprite, points)
    display_screen(display, frame_per_second, player_life, life_sprite, points)
    #end of enemy movment

#for moving collion to be replaced objects to loction on display
def transfer_collision_to_be_replaced(empty_cell, collision, display, collision_to_be_replaced, points, player_life):
    layer_index = 0
    cell_index = 0
    for layer in collision_to_be_replaced :
        cell_index = 0
        for cell in layer :
            if not cell == empty_cell :
                if display[layer_index][cell_index] == empty_cell or display[layer_index][cell_index] == collision :
                    display[layer_index][cell_index] = collision_to_be_replaced[layer_index][cell_index]
                collision_to_be_replaced[layer_index][cell_index] = empty_cell
            cell_index += 1
        layer_index += 1
    display_lives_points(player_life, life_sprite, points)
    display_screen(display, frame_per_second, player_life, life_sprite, points)
    #end of collision to be replaced transfer

#for clearing collision
def clear_collision(empty_cell, collision, display, points, player_life) :
    layer_index = 0
    cell_index = 0
    for layer in display :
        cell_index = 0
        if collision in layer :
            for cell in layer :
                if cell == collision :
                    display[layer_index][cell_index] = empty_cell
                cell_index += 1
        layer_index += 1
    display_lives_points(player_life, life_sprite, points)
    display_screen(display, frame_per_second, player_life, life_sprite, points)
    #end of clearing colllsion

#for enemy moving down every decided game tick or randomly
def move_enemy_down(empty_cell, player_bullet, collision, display, enemy_healths, collision_to_be_replaced, enemy_decend_randomness, enemy_decend_tick, enemy_decend_limit, enemy_decend_list, empty_cell_list, game_tick, points, player_life, enemy_bullet) :
    #for finding in which layer enemy is
    enemy_decend_list = []
    layer_index = 0
    for enemy in enemy_sprites :
        layer_index = 0
        for layer in display[:enemy_decend_limit] :
            if enemy in layer :
                enemy_decend_list.append(layer_index)
            layer_index += 1
    enemy_decend_list.sort()
    #for moving enemy down
    if (game_tick % enemy_decend_tick == 0) or (random.randint(1, 100) <= enemy_decend_randomness) :
        if random.randint(1, 100) == 1 :
            layer_index = 6
            for layer in reversed(display[:enemy_decend_limit]) :
                enemy_contain = 0
                for enemy in enemy_sprites :
                    if enemy in display[layer_index] :
                        enemy_contain += 1
                if (layer_index < enemy_decend_limit - 1) and (enemy_contain == 0) and (not enemy_bullet in layer) :
                    if (player_bullet in layer) and (layer_index - 1 in enemy_decend_list) :
                        bullet_index = layer.index(player_bullet)
                        if not enemy_healths[layer_index - 1][bullet_index] == 0 :
                            enemy_healths[layer_index - 1][bullet_index] -= 1
                            if not enemy_healths[layer_index - 1][bullet_index] == 0 :
                                collision_to_be_replaced[layer_index - 1][bullet_index] = display[layer_index - 1][bullet_index]
                            if enemy_healths[layer_index - 1][bullet_index] == 0 :
                                display[layer_index - 1][bullet_index] = empty_cell
                            display[layer_index - 1][bullet_index] = collision
                            points += 1
                    if layer_index in enemy_decend_list and layer_index < enemy_decend_limit - 1 :
                        display[layer_index + 1] = display[layer_index]
                        display[layer_index] = empty_cell_list
                        enemy_healths[layer_index + 1] = enemy_healths[layer_index]
                        enemy_healths[layer_index] = empty_cell_list
                        collision_to_be_replaced[layer_index + 1] = collision_to_be_replaced[layer_index]
                        collision_to_be_replaced[layer_index] = empty_cell_list
                layer_index -= 1
        elif game_tick % enemy_decend_tick == 0 :
            enemy_contain = 0
            random.shuffle(enemy_decend_list)
            for layer_to_descend in enemy_decend_list :
                layer_index = layer_to_descend + 1
                layer = display[layer_to_descend + 1]
                enemy_contain = 0
                for enemy in enemy_sprites :
                    if enemy in display[layer_index] :
                        enemy_contain += 1
                if (layer_to_descend < enemy_decend_limit - 1) and (enemy_contain == 0) and (not enemy_bullet in layer) :
                    if (player_bullet in layer) and (layer_index - 1 in enemy_decend_list) :
                        bullet_index = layer.index(player_bullet)
                        if not enemy_healths[layer_index - 1][bullet_index] == 0 :
                            enemy_healths[layer_index - 1][bullet_index] -= 1
                            if not enemy_healths[layer_index - 1][bullet_index] == 0 :
                                collision_to_be_replaced[layer_index - 1][bullet_index] = display[layer_index - 1][bullet_index]
                            if enemy_healths[layer_index - 1][bullet_index] == 0 :
                                display[layer_index - 1][bullet_index] = empty_cell
                            display[layer_index - 1][bullet_index] = collision
                            points += 1
                    if layer_index - 1 in enemy_decend_list and layer_index < enemy_decend_limit - 1 :
                        display[layer_index] = display[layer_index - 1]
                        display[layer_index - 1] = empty_cell_list
                        enemy_healths[layer_index] = enemy_healths[layer_index - 1]
                        enemy_healths[layer_index - 1] = empty_cell_list
                        collision_to_be_replaced[layer_index] = collision_to_be_replaced[layer_index - 1]
                        collision_to_be_replaced[layer_index - 1] = empty_cell_list
                    break
    display_lives_points(player_life, life_sprite, points)
    display_screen(display, frame_per_second, player_life, life_sprite, points)
    return points

#for counting how many enemies are in display
def count_enemies(display, enemy_sprites, enemy_count, points, player_life) :
    enemy_count = 0
    for enemy in enemy_sprites :
        for layer in display :
            if enemy in layer :
                for cell in layer :
                    if enemy in cell :
                        enemy_count += 1
    return enemy_count

#for main game loop
def game(enemy_type, enemy_config, enemy_layer, enemy_horizontal_tick, enemy_decend_randomness, enemy_decend_tick, enemy_sprites, display_width, display_height, display_border, start_end_border, enemy_count, empty_cell, enemy_bullet_limit, enemy_bullet, enemy_bullet_tick, player, player_bullet, player_life, life_sprite, consumed_life_sprite, player_position, collision, display, temp_display, layer_index, cell_index, points, enemy_healths, collision_to_be_replaced, enemy_decend_limit, enemy_decend_list, all_enemy_decend_chance, empty_cell_list, game_tick, is_game_active, frame_per_second, create_display, create_collision_to_be_replaced_list, place_player, create_enemy_health_list, place_enemies, create_enemy_sprites_list, place_enemy_bullet, lower_enemy_bullet, raise_player_bullet, player_control, enemy_movment_horizontal, transfer_collision_to_be_replaced, clear_collision, move_enemy_down, count_enemies):
    create_display(display_height, display_width, display)
    create_enemy_health_list(enemy_type, enemy_config, display_height, display_width, empty_cell, enemy_layer, enemy_healths)
    create_enemy_sprites_list(enemy_type, enemy_sprites)
    create_collision_to_be_replaced_list(display_height, display_width, empty_cell, collision_to_be_replaced)
    place_enemies(enemy_type, enemy_config, empty_cell, enemy_layer, collision, display, enemy_healths, enemy_sprites)
    while is_game_active :
        game_tick += 1
        place_player(player, player_position, display, points, player_life)
        if game_tick % enemy_bullet_tick == 0 :
            place_enemy_bullet(empty_cell, enemy_bullet_limit, enemy_bullet, display, enemy_sprites, points, player_life)
        player_life, player_position = player_control(empty_cell, enemy_bullet, player, player_bullet, player_life, player_position, collision, display, points)
        display, player_life = lower_enemy_bullet(empty_cell, enemy_bullet, player, player_bullet, player_life, collision, display, points)
        display, points = raise_player_bullet(enemy_sprites, empty_cell, enemy_bullet, player_bullet, collision, display, points, enemy_healths, collision_to_be_replaced, player_life)
        clear_collision(empty_cell, collision, display, points, player_life)
        if (game_tick % enemy_decend_tick == 0) or (random.randint(1, 100) <= enemy_decend_randomness) :
            points = move_enemy_down(empty_cell, player_bullet, collision, display, enemy_healths, collision_to_be_replaced, enemy_decend_randomness, enemy_decend_tick, enemy_decend_limit, enemy_decend_list, empty_cell_list, game_tick, points, player_life, enemy_bullet)
        if game_tick % enemy_horizontal_tick == 0 :
            enemy_movment_horizontal(enemy_sprites, empty_cell, collision, display, enemy_healths, points, player_life)
        transfer_collision_to_be_replaced(empty_cell, collision, display, collision_to_be_replaced, points, player_life)
        enemy_count = count_enemies(display, enemy_sprites, enemy_count, points, player_life)
        if player_life == 0 :
            is_game_active = False
            input("You Lose")
        if enemy_count == 0 :
            is_game_active - False
            input("You Won")
        os.system("cls")
        display_lives_points(player_life, life_sprite, points)
        display_screen(display, frame_per_second, player_life, life_sprite, points)

while True :
    os.system("cls")
    print(" \"Shoot Up!\"\nStart Game: S\n Controls: C\n   Quit: Q")
    main_menu_choice = input("Enter Choice: ").lower()
    if main_menu_choice == "s" :
        os.system("cls")
        print("  Level 1: 1\n  Level 2: 2\n  Level 3: 3\nRandom Level: R\n   Back: B")
        game_level = input("Enter Level: ").lower()
        if game_level == "r" or game_level in str(enemy_type.keys()) :
            if game_level == "r" :
                game_level = random.randint(1,3)
            game_level = int(game_level)
            if game_level == 1 :
                enemy_config, enemy_layer, all_enemy_decend_chance, enemy_decend_limit, player_life, enemy_bullet_limit, enemy_bullet_tick, enemy_horizontal_tick, enemy_decend_randomness, enemy_decend_tick = game_level_list[game_level - 1]
            elif game_level == 2 :
                enemy_config, enemy_layer, all_enemy_decend_chance, enemy_decend_limit, player_life, enemy_bullet_limit, enemy_bullet_tick, enemy_horizontal_tick, enemy_decend_randomness, enemy_decend_tick = game_level_list[game_level - 1]
            elif game_level == 3 :
                enemy_config, enemy_layer, all_enemy_decend_chance, enemy_decend_limit, player_life, enemy_bullet_limit, enemy_bullet_tick, enemy_horizontal_tick, enemy_decend_randomness, enemy_decend_tick = game_level_list[game_level - 1]
            os.system("cls")
            game(enemy_type, enemy_config, enemy_layer, enemy_horizontal_tick, enemy_decend_randomness, enemy_decend_tick, enemy_sprites, display_width, display_height, display_border, start_end_border, enemy_count, empty_cell, enemy_bullet_limit, enemy_bullet, enemy_bullet_tick, player, player_bullet, player_life, life_sprite, consumed_life_sprite, player_position, collision, display, temp_display, layer_index, cell_index, points, enemy_healths, collision_to_be_replaced, enemy_decend_limit, enemy_decend_list, all_enemy_decend_chance, empty_cell_list, game_tick, is_game_active, frame_per_second, create_display, create_collision_to_be_replaced_list, place_player, create_enemy_health_list, place_enemies, create_enemy_sprites_list, place_enemy_bullet, lower_enemy_bullet, raise_player_bullet, player_control, enemy_movment_horizontal, transfer_collision_to_be_replaced, clear_collision, move_enemy_down, count_enemies)
    elif main_menu_choice == "c" :
        while True :
            os.system("cls")
            print(f"\t Player: {player}\n      Player Bullet: {player_bullet}\n    Random Position: {random_position}\n    To change Player: P\n To change Player Bulet: B\nTo change Random Position: R\n\t  Back: K")
            control_menu_choice = input("      Enter Choice: ").lower()
            if control_menu_choice == "p" :
                while True :
                    os.system("cls")
                    print(f"    Player: {player}")
                    print("Enter to reselect\n     Back: B")
                    if input(" Enter choice: ").lower() == "b" :
                        break
                    player = input("  New Player: ")
            elif control_menu_choice == "b" :
                while True :
                    os.system("cls")
                    print(f"Player Bullet: {player_bullet}")
                    print("Enter to reselect\n     Back: B")
                    if input(" Enter choice: ").lower() == "b" :
                        break
                    player_bullet = input("   New Player Bullet: ")
            elif control_menu_choice == "r" :
                if is_random_position :
                    is_random_position = False
                    random_position = "Off"
                    player_position = 5
                elif is_random_position == False :
                    is_random_position = True
                    random_position = "On"
                    player_position = random.randint(0,10)
            elif control_menu_choice == "k" :
                break
    elif main_menu_choice == "q" :
        os.system("cls")
        print("Thank you for playing")
        break