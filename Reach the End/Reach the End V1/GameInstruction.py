from pathlib import Path
import random
import msvcrt
import shutil
import time
import json
import sys
import os

def create_game(configurations, map_id = [], view_distance = ()):
    gamedata = configurations
    world_data = map_id
    GameWorld = World(len(world_data[0]), len(world_data), view_distance)
    GameWorld.data = gamedata
    firing_groups = {}
    conditions = {}
    y = 0
    for layer in world_data :
        x = 0 
        for cell in layer :
            if cell == "empty" :
                x += 1
                continue
            properties = gamedata[cell]
            if "turret" in cell :
                GameWorld.place_turret(x, y, cell, white_space_remove(properties["turret_sprite"]), properties["direction_to_fire"], properties["firing_mode"], properties["bullet_direction"], properties["bullet_damage"], white_space_remove(properties["bullet_sprite"]), properties["fire_every_tick"], properties["rotation"], properties["direction_of_rotation"], properties["has_condition"])
            elif "end" in cell :
                GameWorld.place("end", x, y, white_space_remove(properties["sprite"]), name_of = cell)
            elif "wall" in cell :
                GameWorld.place("wall", x, y, white_space_remove(properties["sprite"]), name_of = cell, has_condition = properties["has_condition"])
            elif "player" in cell :
                GameWorld.place("player", x, y, white_space_remove(properties["sprite"]), properties["health"], properties["health_sprite"], properties["consumed_health_sprite"])
            elif "condition" in cell :
                GameWorld.place("condition", x, y, white_space_remove(properties["sprite"]), name_of = cell, has_condition = properties["has_condition"], view_distance_n = properties["view_distance_n"])
            x += 1
        y += 1
    #firing groups
    for key, value in gamedata.items() :
        if "turret" in key :
            if value["firing_groups"] in firing_groups :
                firing_groups[value["firing_groups"]].append(key)
            elif not value["firing_groups"] in firing_groups :
                firing_groups[value["firing_groups"]] = [key]
    for key, value in firing_groups.items() :
        if key == 0 :
            continue
        else :
            for turret in firing_groups.get(0, []) :
                firing_groups[key].append(turret)
    del firing_groups[0]
    GameWorld.firing_groups = [value for value in firing_groups.values()]
    #for conditions
    for key, value in gamedata.items() :
        if "turret" in key or "wall" in key :
            if value["has_condition"] in conditions :
                conditions[value["has_condition"]].append(key)
            elif not value["has_condition"] in conditions :
                conditions[value["has_condition"]] = [key]
    del conditions[False]
    for key, value in conditions.items() :
        for cell in value :
            for layer in map_id :
                if cell in layer :
                    GameWorld.conditions_in_map.append(key)
    GameWorld.conditions = conditions
    return GameWorld
        
def time_format (second) :
    time_taken = f"{second} seconds"
    if second > 60 :
        minute = round(second % 60, 2)
        time_taken += f", {minute} minute"
        if minute > 60 :
            hour = round(minute % 60, 2) 
            time_taken += f", {hour} hour"
    return time_taken

def non_blocking_input() :
    if msvcrt.kbhit():
        return msvcrt.getch().decode("utf-8")
    return None

def cordinates_to_advance (direction_to_fire, x, y) :
    #takes in direction turret will be firing x y and return appropiate cordinates
    if direction_to_fire == "up" :
        new_x = x
        new_y = y - 1
    elif direction_to_fire == "down" :
        new_x = x
        new_y = y + 1
    elif direction_to_fire == "left" :
        new_x = x - 1
        new_y = y
    elif direction_to_fire == "right" :
        new_x = x + 1
        new_y = y
    elif direction_to_fire == "random" :
        return cordinates_to_advance(random.choice(["up", "down", "left", "right"]), x, y)
    try :
        if not (new_x < 0 or new_y < 0) :
            return new_x, new_y
    except :
        pass

def move_procedure (World, firing_mode = "simple") :
    #function that takes in object of world and returns world with bullet only moving once by making copy of list removing bullets from it and copying movment fom orignal to copy
    temp_world = [[cell.type for cell in layer] for layer in World.world]
    y = 0
    for layer in temp_world :
        x = 0
        for cell in layer :
            if cell == "bullet" :
                if World.world[y][x].firing_mode == firing_mode or World.world[y][x].direction == "random" :
                    World = World.world[y][x].move(World)
                    if World.world[y][x].type == "empty" :
                        temp_world[y][x] = "empty"
            x += 1
        y += 1
    return World

def shoot_procedure (World, tick) :
    for layer in World.world :
        for cell in layer :
            if "turret" == cell.type and cell.name in World.firing_groups[0] :
                if not cell.has_condition :
                    World = cell.shoot(World)
    World.firing_groups.insert(0, World.firing_groups.pop())
    return World

def white_space_remove (string) :
    result = ""
    whitespaces = [" ", "\n", "\t", "\r"] 
    for char in string :
        if not char in whitespaces :
            result += char
    return result

class World :
    def __init__ (self, width, height, view_distance) :
        self.width = width
        self.height = height
        self.world = [[EmptyCell(x, y, "  ") for x in range(width)] for y in range(height)]
        self.end_cord = []
        self.player = None
        self.data = {}
        self.results = "Won"
        self.view_distance = view_distance
        self.firing_groups = []
        self.conditions = set()
        self.stage_completion_times = {}
        self.conditions_in_map = []
    def display(self):
        if self.view_distance :
            x_start = self.player.x - self.view_distance[0]
            x_end = self.player.x + self.view_distance[0]
            y_start = self.player.y - self.view_distance[1]
            y_end = self.player.y + self.view_distance[1]
            if x_start < 0 :
                x_start = 0
            if x_end > self.width - 1 :
                x_end = self.width - 1
            if y_start < 0 :
                y_start = 0
            if y_end > self.height - 1 :
                y_end = self.height - 1
            world_to_output = [[cell for cell in layer[x_start : x_end + 1]] for layer in self.world[y_start : y_end + 1]]
        else :
            world_to_output = self.world
        output = ""
        output += ("💗" * self.player.health) + ("🤍" * (self.player.max_health - self.player.health)) + "\n"
        terminal_width = shutil.get_terminal_size()[0] 
        for layer in world_to_output:
            row = ""
            for cell in layer:
                if cell.type == "turret":
                    row += self.data[cell.name]["turret_sprite"].strip()
                elif cell.type == "wall":
                    row += self.data[cell.name]["sprite"].strip()
                elif cell.type == "empty":
                    row += "  "
                elif cell.type == "player":
                    row += self.data["player"]["sprite"].strip()
                elif cell.type == "bullet":
                    row += self.data[cell.name]["bullet_sprite"].strip()
                elif cell.type == "end":
                    row += self.data[cell.name]["sprite"].strip()
                elif cell.type == "condition" :
                    row += self.data[cell.name]["sprite"].strip()
            output += row[:terminal_width] + "\n"
        sys.stdout.write("\033[H\033[J" + output)
        sys.stdout.flush()
    def place (self, name, x, y, sprite, health = 0, name_of = "", health_sprite = "", consumed_health_consumed = "", has_condition = None, view_distance_n = None):
        if name == "player" :
            self.world[y][x] = Player(x, y, sprite, health, health_sprite, consumed_health_consumed)
            self.player = self.world[y][x]
        elif name == "end" :
            self.world[y][x] = EndCell(x, y, name_of, sprite)
            self.end_cord.append((x, y))
        elif name == "wall" :
            self.world[y][x] = Wall(x, y, name_of, sprite, has_condition = None)
        elif name == "condition" :
            if not view_distance_n :
                view_distance_n = self.view_distance
            self.world[y][x] = ConditionCell(x, y, name_of, sprite, has_condition, view_distance_n)
    def place_turret (self, x, y, name, turret_sprite, direction_to_fire, firing_mode, bullet_direction, bullet_damage, bullet_sprite, fire_every_tick = 1, rotation = ["up","left","down","right"], direction_of_rotation = False, has_condition = None) :
        if not rotation :
            rotation = ["up", "left", "down", "right"]
        self.world[y][x] = Turret(x, y, name, turret_sprite, direction_to_fire, firing_mode, bullet_direction, bullet_damage, bullet_sprite, fire_every_tick, rotation, has_condition, direction_of_rotation)
    def is_active (self) :
        if self.player.health <= 0 :
            self.results = "Lost"
            return False
        elif self.player.reached_end :
            self.results = "Won"
            return False
        else :
            return True

class EmptyCell :
    def __init__(self, x, y, sprite):
        self.type = "empty"
        self.name = "empty"
        self.sprite = sprite
        self.is_over_writeable = True
        self.is_walkable = True
        self.can_damage = False
        self.x = x
        self.y = y
        self.cordinates = (x, y)
    def revert(self) :
        self.sprite = "  "

class EndCell :
    def __init__(self, x, y, name, sprite):
        self.type = "end"
        self.sprite = sprite
        self.is_over_writeable = False
        self.is_walkable = True
        self.can_damage = False
        self.x = x
        self.y = y
        self.name = name
        self.cordinates = (x, y)

class ConditionCell :
    def __init__(self, x, y, name, sprite, has_condition, view_distance_n):
        self.type = "condition"
        self.sprite = sprite
        self.is_over_writeable = False
        self.is_walkable = True
        self.can_damage = False
        self.x = x
        self.y = y
        self.name = name
        self.cordinates = (x, y)
        self.has_condition = has_condition
        self.view_distance_n = view_distance_n
    
class Bullet :
    def __init__(self, name , firing_mode, direction, bullet_damage, sprite, x = None, y = None):
        self.type = "bullet"
        self.sprite = sprite
        self.is_over_writeable = True
        self.is_walkable = True
        self.can_damage = True
        self.x = x
        self.y = y
        self.name = name
        self.cordinates = (x, y)
        self.firing_mode = firing_mode
        self.direction = direction
        self.bullet_damage = bullet_damage
    def move (self, World) :
        world = World.world
    #takes in 2D List of objects that have attribute is_over_writeable to see wether they bullet can movet and its type an type to see wetther they are player or not
        if self.firing_mode == "laser" and (not self.direction == "random"): 
            world = self.revert(world)
            World.world = world
            return World
        else :
            cordinates_to_move = cordinates_to_advance(self.direction, self.x, self.y)
            try :
                cell_to_move = world[cordinates_to_move[1]][cordinates_to_move[0]]
            except :
                return World
            else :
                try :
                    if cell_to_move.type == "player" :
                        World.player.health -= self.bullet_damage
                        world[self.y][self.x] = EmptyCell(self.x, self.y, sprite = "💥")
                    elif cell_to_move.type == "wall" or cell_to_move.type == "turret" :
                        world[self.y][self.x] = EmptyCell(self.x, self.y, sprite = "  ")
                    elif cell_to_move.type == "bullet" :
                        if random.random() < 0.20 : #chance that if bullet collides with othe it explode
                            world[self.y][self.x] = EmptyCell(self.x, self.y, sprite = "  ")
                    elif cell_to_move.type == "empty" :
                            world[cordinates_to_move[1]][cordinates_to_move[0]] = Bullet(self.name, self.firing_mode, self.direction, self.bullet_damage, self.sprite, cordinates_to_move[0], cordinates_to_move[1])
                            world[self.y][self.x] = EmptyCell(self.x, self.y, sprite = "  ")
                    elif cell_to_move.type == "end" or cell_to_move.type == "condition" :
                        world[self.y][self.x] = EmptyCell(self.x, self.y, sprite = "  ")
                    World.world = world
                    return World
                except :
                    World.world = world
                    return World
    def revert (self, world) :
        if self.firing_mode == "laser" :
            world[self.y][self.x] = EmptyCell(self.x, self.y, sprite = "  ")
        return world
            
class Turret :
    def __init__ (self, x, y, name, turret_sprite, direction_to_fire, firing_mode, bullet_direction, bullet_damage, bullet_sprite, fire_every_tick, rotation, has_condition, direction_of_rotation = False) :
        self.type = "turret"
        self.x = x
        self.y = y
        self.name =  name
        self.cordinates = (x, y)
        self.sprite = turret_sprite
        self.bullet = Bullet(name, firing_mode, bullet_direction, bullet_damage, bullet_sprite)#create object of bullet to determine how it fires and damage it deals that also hasa sprite
        self.is_over_writeable = False
        self.is_walkable = False
        self.can_damage = False
        self.fire_every_tick = fire_every_tick
        self.direction_to_fire = direction_to_fire
        self.direction_of_rotation = direction_of_rotation
        self.rotation = rotation
        self.has_condition = has_condition
    def shoot (self, World) :
        world = World.world
    #takes in 2D List of objects that have attribute is_over_writeable to see wether they bullet can be placed or not and its type an type to see wetther they are player or not
        try : 
            if not self.bullet.firing_mode == "laser" :
                if self.direction_of_rotation :
                    self.direction_to_fire = self.rotation[0]
                    if not self.bullet.direction == "random" :
                        self.bullet.direction = self.rotation[0]
                    self.rotation.append(self.rotation.pop(0))
                    cordinates_to_fire = cordinates_to_advance(self.direction_to_fire, self.x, self.y)
                else :
                    cordinates_to_fire = cordinates_to_advance(self.direction_to_fire, self.x, self.y)
                if world[cordinates_to_fire[1]][cordinates_to_fire[0]].is_over_writeable == True :
                    if not world[cordinates_to_fire[1]][cordinates_to_fire[0]].type == "player" :
                        world[cordinates_to_fire[1]][cordinates_to_fire[0]] = Bullet(self.bullet.name, self.bullet.firing_mode, self.bullet.direction, self.bullet.bullet_damage, self.bullet.sprite, x = cordinates_to_fire[0], y= cordinates_to_fire[1])
                    elif world[cordinates_to_fire[1]][cordinates_to_fire[0]].type == "player" :
                        #player should have attribute health that should be reduced
                        World.player.health -= self.bullet.bullet_damage
                return World
            else :
                if self.direction_of_rotation :
                    self.direction_to_fire = self.rotation[0]
                    if not self.bullet.direction == "random" :
                        self.bullet.direction = self.rotation[0]
                    self.rotation.append(self.rotation.pop(0))
                x = self.x
                y = self.y
                while True :
                    x, y = cordinates_to_advance(self.direction_to_fire, x, y)
                    if world[y][x].type == "player" :
                        World.player.health -= self.bullet.bullet_damage
                    elif world[y][x].type == "empty" or world[y][x].type == "bullet" :
                        world[y][x] =  Bullet(self.bullet.name, self.bullet.firing_mode, self.bullet.direction, self.bullet.bullet_damage, self.bullet.sprite, x , y)
                    else :
                        break
                return World
        except :
            return World

class Wall :
    def __init__(self, x, y, name, sprite, has_condition):
        self.type = "wall"
        self.sprite = sprite
        self.is_over_writeable = False
        self.is_walkable = False
        self.can_damage = False
        self.x = x
        self.y = y
        self.name = name
        self.cordinates = (x, y)
        self.has_condition = has_condition

class Player :
    def __init__(self, x, y, sprite, health, health_sprite, consumed_health_sprite):
        self.type = "player"
        self.sprite = sprite
        self.is_over_writeable = False
        self.is_walkable = False
        self.can_damage = False
        self.x = x
        self.y = y
        self.cordinates = (x, y)
        self.max_health = health
        self.health = health
        self.health_sprite = health_sprite
        self.consumed_health_consumed = consumed_health_sprite
        self.reached_end = False
        self.name = "player"
    def move (self, World, direction, stage_start_time) :
        world = World.world
        cordinates_to_move = cordinates_to_advance(direction, self.x, self.y)
        try :
            cell_to_move = world[cordinates_to_move[1]][cordinates_to_move[0]]
        except :
            pass
        else :
            if cell_to_move.type == "empty" :
                world[cordinates_to_move[1]][cordinates_to_move[0]] = Player(cordinates_to_move[0], cordinates_to_move[1], self.sprite, self.health, self.health_sprite, self.consumed_health_consumed)
                world[self.y][self.x] = EmptyCell(self.x, self.y, sprite = "  ")
                self.x , self.y = cordinates_to_move
            elif cell_to_move.type == "bullet" :
                world[cordinates_to_move[1]][cordinates_to_move[0]] = Player(cordinates_to_move[0], cordinates_to_move[1], self.sprite, self.health, self.health_sprite, self.consumed_health_consumed)
                world[self.y][self.x] = EmptyCell(self.x, self.y, sprite = "  ")
                self.x , self.y = cordinates_to_move
                self.health -= cell_to_move.bullet_damage
            elif cell_to_move.type == "end" :
                world[cordinates_to_move[1]][cordinates_to_move[0]] = Player(cordinates_to_move[0], cordinates_to_move[1], self.sprite, self.health, self.health_sprite, self.consumed_health_consumed)
                world[self.y][self.x] = EmptyCell(self.x, self.y, sprite = "  ")
                self.x , self.y = cordinates_to_move
                self.reached_end = True
            elif cell_to_move.type == "condition" :
                for layer in World.world :
                    for cell in layer :
                        if cell.name in World.conditions[cell_to_move.has_condition] :
                            cell.has_condition = None
                            if cell.type == "wall" :
                                World.world[cell.y][cell.x] = EmptyCell(cell.x, cell.y, "  ")
                World.world[cell_to_move.y][cell_to_move.x] = EmptyCell(cell_to_move.x, cell_to_move.y, "  ")
                World.conditions[cell_to_move.has_condition] = []
                World.stage_completion_times[cell_to_move.has_condition] = time.time() - stage_start_time
                World.view_distance = cell_to_move.view_distance_n
                return World, time.time()
            return World, stage_start_time
        return World, stage_start_time

def start_game (configurations, map_id = "", view_distance = ()) :
    start_time = time.time()
    os.system("echo \033[?25l")
    ticks = 1
    frame_rate = 30
    GameWorld = create_game(configurations, map_id, view_distance)
    GameWorld.display()
    last_time = time.time()
    stage_start_time = time.time()
    while GameWorld.is_active() :
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time
        time.sleep(max(1 / frame_rate - delta_time, 0))
        direction = non_blocking_input()
        if direction == None :
            direction = ""
        else :
            direction = direction.lower()
            if direction == "a" :
                direction = "left"
            elif direction == "s" :
                direction = "down"
            elif direction == "d" :
                direction = "right"
            elif direction == "w" :
                direction = "up"
            GameWorld, stage_start_time = GameWorld.player.move(GameWorld, direction, stage_start_time)
        if ticks % 18 == 0 :
            GameWorld = move_procedure(GameWorld, "simple")
            GameWorld = move_procedure(GameWorld, "laser")
        if ticks % 36 == 0 :
            GameWorld = shoot_procedure(GameWorld, ticks)
        GameWorld.display()
        ticks += 1
    os.system("echo \033[?25h")
    seconds = round(time.time() - start_time, 2)
    time_taken = time_format(seconds)
    string = f"You {GameWorld.results} in {time_taken}."
    for condition in GameWorld.conditions :
        if condition in GameWorld.conditions_in_map :
            if condition in GameWorld.stage_completion_times :
                string += f"\n\n   Stage {condition} : Completed\nTime Taken : {time_format(round(GameWorld.stage_completion_times[condition], 2))}"
            else :
                string += f"\n\n Stage {condition} : Not Completed"
    while True :
        os.system("cls")
        print(string)
        restart_menu = input("       Restart : R\n        Back : B\n    Enter Choice : ").lower()
        if restart_menu == "r" :
            start_game(configurations, map_id, view_distance)
        elif restart_menu == "b" :
            break