import tkinter
import random
import time
import keyboard

CANVAS_WIDTH = 420
CANVAS_HEIGHT = 420
WORLD_SPEED = 0.5
GRID = 20
BAR_SIZE = 40
SPEED = 20
ENEMIES = 3


def main():
    # Create level
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, "Bomberman_v1")
    background = canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill = 'green')

    # Create upper bar
    bar_width = CANVAS_WIDTH
    bar_height = 40
    bar = canvas.create_rectangle(0, 0, bar_width, bar_height, fill = 'gray')


    # Set the current lives, score and timer values
    lives = 3
    score = 0
    timer = 200

    # Other variables
    time_bomb = 0
    bombs_in_use = 0
    enemy_list = []
    x_switch_dir = 0
    y_switch_dir = 0
    dir_x = 1
    dir_y = 0

    # Set initial GUI
    text_time_object = canvas.create_text(20, 10, text='')
    text_lives_object = canvas.create_text(20 + CANVAS_WIDTH / 4, 10, text='')
    text_score_object = canvas.create_text(20 + CANVAS_WIDTH / 2, 10, text='')

    # Create walls around
    wall_number_h = CANVAS_WIDTH // GRID
    wall_number_v = CANVAS_HEIGHT // GRID - 4
    x_wall = 0
    y_wall = BAR_SIZE
    wall_list = []
    soft_wall_list = []
    for i in range(wall_number_h):
        wall = canvas.create_rectangle(x_wall, y_wall, x_wall + GRID, y_wall + GRID, fill = 'black')
        wall_list.append(wall)
        wall = canvas.create_rectangle(x_wall + 2, y_wall + 2, x_wall + GRID - 1, y_wall + GRID - 1, fill = 'white')
        wall_list.append(wall)
        x_wall += GRID
    x_wall = 0
    y_wall = CANVAS_HEIGHT - GRID - (CANVAS_HEIGHT % GRID)
    for i in range(wall_number_h):
        wall = canvas.create_rectangle(x_wall, y_wall, x_wall + GRID, y_wall + GRID, fill = 'black')
        wall_list.append(wall)
        wall = canvas.create_rectangle(x_wall + 2, y_wall + 2, x_wall + GRID - 1, y_wall + GRID - 1, fill = 'white')
        wall_list.append(wall)
        x_wall += GRID
    x_wall = 0
    y_wall = BAR_SIZE + GRID
    for i in range(wall_number_v):
        wall = canvas.create_rectangle(x_wall, y_wall, x_wall + GRID, y_wall + GRID, fill = 'black')
        wall_list.append(wall)
        wall = canvas.create_rectangle(x_wall + 2, y_wall + 2, x_wall + GRID - 1, y_wall + GRID - 1, fill = 'white')
        wall_list.append(wall)
        y_wall += GRID
    x_wall = CANVAS_WIDTH - GRID - (CANVAS_WIDTH % GRID)
    y_wall = BAR_SIZE + GRID
    for i in range(wall_number_v):
        wall = canvas.create_rectangle(x_wall, y_wall, x_wall + GRID, y_wall + GRID, fill = 'black')
        wall_list.append(wall)
        wall = canvas.create_rectangle(x_wall + 2, y_wall + 2, x_wall + GRID - 1, y_wall + GRID - 1, fill = 'white')
        wall_list.append(wall)
        y_wall += GRID

    # Create hard walls in a pattern
    hard_wall_number_h = ((CANVAS_WIDTH // GRID) - 2) // 2
    hard_wall_number_v = ((CANVAS_HEIGHT // GRID) - 4) // 2
    x_hard_wall = 2 * GRID
    y_hard_wall = BAR_SIZE + 2 * GRID
    hard_wall_list_x = []
    hard_wall_list_y = []
    for i in range(hard_wall_number_v):
        for i in range(hard_wall_number_h):
            wall = canvas.create_rectangle(x_hard_wall, y_hard_wall, x_hard_wall + GRID, y_hard_wall + GRID, fill = 'black')
            wall_list.append(wall)
            wall = canvas.create_rectangle(x_hard_wall + 2, y_hard_wall + 2, x_hard_wall + GRID - 1,
                                           y_hard_wall + GRID - 1, fill = 'white')
            wall_list.append(wall)
            x_hard_wall += 2 * GRID
            hard_wall_list_x.append(x_hard_wall)
        x_hard_wall = 2 * GRID
        y_hard_wall += 2 * GRID
        hard_wall_list_y.append(y_hard_wall)

    hard_wall_coordinates = {}
    for key in hard_wall_list_x:
        for value in hard_wall_list_y:
            hard_wall_coordinates[key] = value
            #hard_wall_list_y.remove(value)
            break


    # Create random soft walls
    rows = wall_number_v
    col = wall_number_h - 2
    for i in range(1, rows - 1):
        soft_wall_y = BAR_SIZE + GRID * (1 + i)
        for i in range(1, col - 1):
            soft_wall_x = GRID * (1 + i)
            dice = random.randint(1, 4)
            if dice == 1:
                wall_soft = canvas.create_rectangle(soft_wall_x, soft_wall_y, soft_wall_x + GRID,
                                                    soft_wall_y + GRID, fill='yellow')
                if overlap(canvas, wall_soft, background):
                    canvas.delete(wall_soft)


    # Create player
    player_x = GRID
    player_y = BAR_SIZE + GRID
    player_id = canvas.create_oval(player_x, player_y, player_x + GRID, player_y + GRID, fill = 'blue')
    ghost_id = canvas.create_oval(player_x + 1, player_y + 1, player_x - 1 + GRID, player_y + GRID - 1, fill = 'gray')


    # Create enemies

    for i in range(ENEMIES):
        enemy_created = 0
        while enemy_created == 0:
            enemy_x = random.randint(2, col - 1) * GRID
            enemy_y = BAR_SIZE + random.randint(2, rows - 1) * GRID
            enemy = canvas.create_oval(enemy_x, enemy_y, enemy_x + GRID, enemy_y + GRID, fill = 'pink')
            if overlap(canvas, enemy, background):
                canvas.delete(enemy)
            else:
                enemy_created = 1


    # Game mechanics
    while timer >= 0 or lives > 0:

        # Timer mechanics
        canvas.delete(text_time_object)
        text_time = 'TIME ' + str(int(timer))
        text_time_object = canvas.create_text(50, 10, text=str(text_time))
        timer -= WORLD_SPEED

        # Lives mechanics
        canvas.delete(text_lives_object)
        text_lives = 'LIVES ' + str(lives)
        text_lives_object = canvas.create_text(50 + CANVAS_WIDTH / 4, 10, text=str(text_lives))

        # Score mechanics
        canvas.delete(text_score_object)
        text_score = 'SCORE ' + str(score)
        text_score_object = canvas.create_text(50 + CANVAS_WIDTH / 2, 10, text=str(text_score))






        # Player mechanics
        x_player = get_left_x(canvas, player_id)
        y_player = get_top_y(canvas, player_id)


        # Player moves

        x_speed, y_speed = get_speed()
        print(x_speed)
        print(y_speed)


        canvas.move(ghost_id, x_speed, y_speed)
        if overlap(canvas, ghost_id, background):
            canvas.moveto(ghost_id, x_player, y_player)
        else:
            canvas.move(player_id, x_speed, y_speed )




        '''''
        
        objects_top = canvas.find_overlapping(x_player, y_player - 5, x_player + GRID, y_player + GRID)
        objects_bottom = canvas.find_overlapping(x_player, y_player, x_player + GRID, y_player + 5 + GRID)
        objects_left = canvas.find_overlapping(x_player - 5, y_player, x_player + GRID, y_player + GRID)
        objects_right = canvas.find_overlapping(x_player, y_player, x_player + 5 + GRID, y_player + GRID)
        right_check = not (any(item in objects_right for item in wall_list) or any(
            item in objects_right for item in soft_wall_list))
        left_check = not (any(item in objects_left for item in wall_list) or any(
            item in objects_left for item in soft_wall_list))
        up_check = not (any(item in objects_top for item in wall_list) or any(
            item in objects_top for item in soft_wall_list))
        down_check = not (any(item in objects_bottom for item in wall_list) or any(
            item in objects_bottom for item in soft_wall_list))

        
        print("right", right_check, objects_right)
        print("left", left_check, objects_left)
        print("up", up_check, objects_top)
        print("down", down_check, objects_bottom)
        print("playerID", player_id)


        if right_check and keyboard.is_pressed() == 'right':
            x_speed = SPEED
            y_speed = 0
        elif left_check and keyboard.is_pressed() == 'left':
            x_speed = -SPEED
            y_speed = 0
        elif up_check and keyboard.is_pressed() == 'up':
            x_speed = 0
            y_speed = -SPEED
        elif down_check and keyboard.is_pressed() == 'down':
            x_speed = 0
            y_speed = SPEED
        else:
            x_speed = 0
            y_speed = 0


        dx_player = int(x_player) + int(x_speed)
        dy_player = int(y_player) + int(y_speed)
        canvas.moveto(player_id, dx_player, dy_player)
        
        # Player puts a bomb + bomb mechanics
        bomb_destroys_list = []
        bomb_kill = 0
        if key == "Enter" and bombs_in_use == 0:
            bomb = canvas.create_oval(x_player, y_player, x_player + GRID, y_player + GRID, fill = 'black')
            time_bomb = timer - 2.5
            x_bomb = canvas.get_left_x(bomb)
            y_bomb = canvas.get_top_y(bomb)
            bombs_in_use = 1
        if timer == time_bomb:
            canvas.delete(bomb)
            fire_h = canvas.create_oval(x_bomb - GRID, y_bomb + GRID / 4, x_bomb + 2 * GRID, y_bomb + 3 * GRID / 4,
                                        fill = 'red')
            fire_v = canvas.create_oval(x_bomb + GRID / 4, y_bomb - GRID, x_bomb + 3 * GRID / 4, y_bomb + 2 * GRID,
                                        fill = 'red')

            bomb_destroys_list = canvas.find_overlapping(x_bomb - GRID, y_bomb + GRID / 4, x_bomb + 2 * GRID,
                                                         y_bomb + 3 * GRID / 4)
            bomb_destroys_list.remove('shape_0')
            bomb_destroys_list.remove(str(fire_h))
            bomb_destroys_list.remove(str(fire_v))

            if player_id in bomb_destroys_list:
                lives = death(lives)
                bomb_destroys_list.remove(str(player_id))
                bomb_kill = 1

            for item in bomb_destroys_list:
                if item not in wall_list:
                    canvas.delete(item)
            bomb_destroys_list = canvas.find_overlapping(x_bomb + GRID / 4, y_bomb - GRID, x_bomb + 3 * GRID / 4,
                                                         y_bomb + 2 * GRID)
            bomb_destroys_list.remove('shape_0')
            bomb_destroys_list.remove(str(fire_h))
            bomb_destroys_list.remove(str(fire_v))
            if player_id in bomb_destroys_list:
                if bomb_kill == 0:
                    lives = death(lives)
                bomb_destroys_list.remove(str(player_id))

            for item in bomb_destroys_list:
                if item not in wall_list:
                    canvas.delete(item)
                    if item in enemy_list:
                        score += 100
        if timer == time_bomb - 1:
            canvas.delete(fire_h)
            canvas.delete(fire_v)
            bombs_in_use = 0

        # Enemies mechanics

        for item in enemy_list:
            enemy = item
            print(enemy)
            x_enemy = get_left_x(canvas, enemy)
            y_enemy = get_top_y(canvas, enemy)
            moved = 0
            sleep_enemy = 0.5
            while moved == 0:
                if front_is_clear(canvas, x_enemy, y_enemy, dir_x, dir_y, wall_list, soft_wall_list):
                    move(canvas, enemy, dir_x, dir_y)
                    moved = 1
                elif front_is_clear(canvas, x_enemy, y_enemy, dir_x, dir_y, wall_list, soft_wall_list) == None:
                    dir_x = 0
                    dir_y = 0
                    moved = 1
                else:
                    dir_x, dir_y = turn_right(canvas, enemy, dir_x, dir_y)
                    sleep_enemy = 0
                print(front_is_clear(canvas, x_enemy, y_enemy, dir_x, dir_y, wall_list, soft_wall_list))
                time.sleep(sleep_enemy)
        # Game over conditions
                '''
        if timer == 0:
            game_over(canvas)
        elif lives == 0:
            game_over(canvas)
        canvas.update()
        time.sleep(WORLD_SPEED)

def get_speed():
    if keyboard.is_pressed('right'):
        x_speed = SPEED
        y_speed = 0
    elif keyboard.is_pressed('left'):
        x_speed = -SPEED
        y_speed = 0
    elif keyboard.is_pressed('up'):
        x_speed = 0
        y_speed = -SPEED
    elif keyboard.is_pressed('down'):
        x_speed = 0
        y_speed = SPEED
    else:
        x_speed = 0
        y_speed = 0

    return x_speed, y_speed


def overlap(canvas, object, background):
    object_x = get_left_x(canvas, object)
    object_y = get_top_y(canvas, object)
    overlap = list(canvas.find_overlapping(object_x + 1, object_y + 1, object_x + GRID - 1, object_y + GRID - 1))
    overlap.remove(object)
    overlap.remove(background)
    if len(overlap) > 0:
        print("overlap", overlap)
        return True
    else:
        return False

def front_is_clear(canvas, x_enemy, y_enemy, dir_x, dir_y, wall_list, soft_wall_list):
    objects_top_enemy = canvas.find_overlapping(x_enemy, y_enemy - 5, x_enemy + GRID, y_enemy + GRID)
    objects_bottom_enemy = canvas.find_overlapping(x_enemy, y_enemy, x_enemy + GRID, y_enemy + 5 + GRID)
    objects_left_enemy = canvas.find_overlapping(x_enemy - 5, y_enemy, x_enemy + GRID, y_enemy + GRID)
    objects_right_enemy = canvas.find_overlapping(x_enemy, y_enemy, x_enemy + 5 + GRID, y_enemy + GRID)

    right_check_enemy = not (any(item in objects_right_enemy for item in wall_list) or any(
        item in objects_right_enemy for item in soft_wall_list))
    left_check_enemy = not (any(item in objects_left_enemy for item in wall_list) or any(
        item in objects_left_enemy for item in soft_wall_list))
    up_check_enemy = not (any(item in objects_top_enemy for item in wall_list) or any(
        item in objects_top_enemy for item in soft_wall_list))
    down_check_enemy = not (any(item in objects_bottom_enemy for item in wall_list) or any(
        item in objects_bottom_enemy for item in soft_wall_list))

    if dir_x == 1 and dir_y == 0:
        return right_check_enemy
    elif dir_x == 0 and dir_y == 1:
        return down_check_enemy
    elif dir_x == -1 and dir_y == 0:
        return left_check_enemy
    elif dir_x == 0 and dir_y == -1:
        return up_check_enemy

    if not (right_check_enemy and left_check_enemy and down_check_enemy and up_check_enemy):
        return None


def move(canvas, enemy, dir_x, dir_y):
    enemy_speed_x = dir_x * SPEED
    enemy_speed_y = dir_y * SPEED
    canvas.move(enemy, enemy_speed_x, enemy_speed_y)


def turn_right(canvas, enemy, dir_x, dir_y):
    if dir_x == 1 and dir_y == 0:
        dir_x = 0
        dir_y = 1
    elif dir_x == 0 and dir_y == 1:
        dir_x = -1
        dir_y = 0
    elif dir_x == -1 and dir_y == 0:
        dir_x = 0
        dir_y = -1
    elif dir_x == 0 and dir_y == -1:
        dir_x = 1
        dir_y = 0

    return dir_x, dir_y


def random_direction():
    direction = random.randint(-1, 1)
    if direction == 0:
        direction = 1
    return direction


def death(lives):
    lives -= 1
    print('lives:', lives)
    return lives


def game_over(canvas):
    canvas.clear()
    canvas.create_text(CANVAS_WIDTH / 2 - 40, CANVAS_HEIGHT / 2, text='GAME OVER!')

def make_canvas(width, height, title):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    reachange_y for drawing.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas

def get_left_x(canvas, object):
    return canvas.coords(object)[0]

def get_top_y(canvas, object):
    return canvas.coords(object)[1]

def get_right_x(canvas, object):
    return canvas.coords(object)[2]

def get_bottom_y(canvas, object):
    return canvas.coords(object)[3]

if __name__ == '__main__':
    main()