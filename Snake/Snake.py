import random
import os

class Point :
    def __init__ (self, x, y) :
        self.x = x
        self.y = y
    def cord (self) :
        return self.x, self.y

def game_point_placer (display, snake) :
    game_point = Point(random.randint(0, display.size - 1), random.randint(0, display.size - 1))
    while game_point.cord() in [cell.cord() for cell in snake.occupied_cells] :
        game_point = Point(random.randint(0, display.size - 1), random.randint(0, display.size - 1))
    return game_point

def display_screen (self, points_earned, snake) :
        print("\033[1;0H")
        string = ""
        for i in range(1, 4) :
            if i <= snake.lives :
                string += f"{snake.live_remain_sprite} "
            else :
                string += f"{snake.live_consumed_sprite} "
        print(f" Lives: {string}Points: {points_earned}")
        print(f"+{self.horizontal_border * (self.size * self.cell_width)}+")
        for layer in self.board :
            print(self.vertical_border, end = "")
            for cell in layer :
                print(cell, end = "")
            print(self.vertical_border, end = "\n")
        print(f"+{self.horizontal_border * (self.size * self.cell_width)}+") 

def cord_advance (snake, display, direction) :
    snake_cord = [snake.location.x, snake.location.y]
    if direction.lower() == "up" :
        if snake_cord[1] == 0 :
            snake_cord[1] = display.size - 1
        else :
            snake_cord[1] -= 1
    elif direction.lower() == "down" :
        if snake_cord[1] ==  display.size - 1 :
            snake_cord[1] = 0
        else :
            snake_cord[1] += 1
    elif direction.lower() == "left" :
        if snake_cord[0] == 0 :
            snake_cord[0] = display.size - 1
        else :
            snake_cord[0] -= 1
    elif direction.lower() == "right" :
        if snake_cord[0] ==  display.size - 1 :
            snake_cord[0] = 0
        else :
            snake_cord[0] += 1
    return tuple(snake_cord)

class Snake :
    def __init__ (self, sprite, head_sprite , location = (0,0), live_consumed_sprite = "🖤", live_remain_sprite = "❤", lives = 1) :
        self.head_sprite = head_sprite
        self.sprite = sprite
        self.location = Point(location[0], location[1])
        self.occupied_cells = []
        self.occupied_cells.append(Point(location[0], location[1]))
        self.lives = lives
        self.live_consumed_sprite = live_consumed_sprite
        self.live_remain_sprite = live_remain_sprite
    def place (self, display) :
        if display.board[self.location.y][self.location.x] == display.empty_cell :
            display.board[self.location.y][self.location.x] = self.sprite
        else :
            return 0
    def move (self, display, direction, game_point) :
        if direction.lower() == "up" :
            if not cord_advance(self, display, "up") in [cell.cord() for cell in self.occupied_cells] :
                if self.location.y == 0 :
                    self.location.y = display.size - 1
                else :
                    self.location.y -= 1
            else :
                return 0
        elif direction.lower() == "down" :
            if not cord_advance(self, display, "down") in [cell.cord() for cell in self.occupied_cells] :
                if self.location.y == display.size - 1 :
                    self.location.y = 0
                else :
                    self.location.y += 1
            else :
                return 0
        elif direction.lower() == "left" :
            if not cord_advance(self, display, "left") in [cell.cord() for cell in self.occupied_cells] :
                if self.location.x == 0 :
                    self.location.x = display.size - 1
                else :
                    self.location.x -= 1
            else :
                return 0
        elif direction.lower() == "right" :
            if not cord_advance(self, display, "right") in [cell.cord() for cell in self.occupied_cells] :
                if self.location.x == display.size - 1 :
                    self.location.x = 0
                else :
                    self.location.x += 1
            else :
                return 0
        temp_occupied_cells = []
        for cell_no in range(len(self.occupied_cells)) :
            if cell_no == 0 :
                temp_occupied_cells.append(Point(self.location.x, self.location.y))
            else  :
                temp_occupied_cells.append(self.occupied_cells[cell_no - 1])
        self.occupied_cells = temp_occupied_cells
    def grow (self, display, direction, game_point) :
        tail = self.occupied_cells[-1]
        if self.move(display, direction, game_point) == 0 :
            return 0
        self.occupied_cells.append(tail)

class Display :
    def __init__(self, size, empty_cell):
        self.size = size
        self.empty_cell  = empty_cell
        self.board= []
        self.cell_width = len(empty_cell) + 1
        self.horizontal_border = "-"
        self.vertical_border = "|"
    def create (self) :
        self.board = []
        for i in range (self.size) :
            temp = []
            for j in range (self.size) :
                temp.append(self.empty_cell)
            self.board.append(temp)
    def display (self, points_earned, snake) :
        print("\033[1;0H")
        string = ""
        for i in range(1, 4) :
            if i <= snake.lives :
                string += f"{snake.live_remain_sprite} "
            else :
                string += f"{snake.live_consumed_sprite} "
        print(f" Lives: {string}Points: {points_earned}")
        print(f"+{self.horizontal_border * (self.size * self.cell_width)}+")
        for layer in self.board :
            print(self.vertical_border, end = "")
            for cell in layer :
                print(cell, end = "")
            print(self.vertical_border, end = "\n")
        print(f"+{self.horizontal_border * (self.size * self.cell_width)}+") 
    def update (self, snake, game_point, game_point_sprite) :
        temp_display = Display(self.size, self.empty_cell)
        temp_display.create()
        temp_display.board[game_point.y][game_point.x] = game_point_sprite
        for cell in snake.occupied_cells :
            temp_display.board[cell.y][cell.x] = snake.sprite
        temp_display.board[snake.location.y][snake.location.x] = snake.head_sprite
        display.board = temp_display.board

snake = Snake("⬛ ", "🟩", location = (0,0), lives = 3)
display = Display(20, "⬜ ")
display.create()
snake.place(display)
game_point = game_point_placer(display, snake)
game_point_sprite = "🍓 "
points_earned = 0
is_alive = True
direction = "up"

display.update(snake, game_point, game_point_sprite)
display_screen(display, points_earned, snake)
while is_alive :
    display_screen(display, points_earned, snake)
    user_input = input("Enter direction: ")
    if user_input.lower() == "a" :
        direction = "left"
    elif user_input.lower() == "d" :
        direction = "right"
    elif user_input.lower() == "w" :
        direction = "up"
    elif user_input.lower() == "s" :
        direction = "down"
    if cord_advance(snake, display, direction) in [cell.cord() for cell in snake.occupied_cells] :
        if len(snake.occupied_cells) > 1:
            if cord_advance(snake, display, direction) == snake.occupied_cells[1].cord() :
                continue
            else :
                if snake.lives > 0 :
                    snake.lives -= 1
                if snake.lives == 0 :
                    is_alive = False
    elif cord_advance(snake, display, direction) == game_point.cord() :
        snake.grow(display, direction, game_point)
        display.board[game_point.y][game_point.x] = snake.sprite
        game_point = game_point_placer(display, snake)
        points_earned += 1
        display.update(snake, game_point, game_point_sprite)
        os.system("cls")
    elif not cord_advance(snake, display, direction) in [cell.cord() for cell in snake.occupied_cells] :
        snake.move(display, direction, game_point)
    if points_earned == (display.size * display.size) :
        is_alive = False
    display.update(snake, game_point, game_point_sprite)
    display_screen(display, points_earned, snake)
input()