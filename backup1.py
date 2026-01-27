# w -> UP
# s -> DOWN
# d -> RIGHT
# s -> LEFT 
print ('** Welcome to the SNAKE GAME 🐍🐍**')
user_name: str = input('Enter your User Name:')
print(f'{user_name}! You enter the snake cage')
print (f'you can move around and eat sweet apples by using')
print(f'w(UP), s(DOWN), d(RIGHT), s(LEFT)')

# GAME SETUP
grid_size: int = 20
snake: list[list[int]]=[[10,10],[9,10],[8,10]]
apple_postion: list[int] = [17,17]
obtacle_position: list[int] = [3,9]
direction: list[int] = [0,0]
score: int = 0
game_running: bool = True
border_min_value = 0
border_max_value = 19
star_position: list[int] =[10,10]
while game_running:
#create the Game plan
    for y in range(grid_size):
        row: str = ''
        for x in range(grid_size):
             if [x,y] == snake[0]:
                row = row + '🐍'
             elif [x,y] in snake:
                row = row + '🟩'
             elif [x,y] == apple_postion:
                row = row + '🍎'
             elif x == 0 or x==19 or y==0 or y==19:
                row = row + '🌹'
             elif score > 2 and [x,y] ==star_position:
                 row = row + '⭐'
             elif score > 4 and [x,y] ==obtacle_position:
                 row = row + '🔥'
             else:
                row = row + '⬛'
        print (row)
        

    user_input = input ('MOVE (w/d/s/a) or QUIT (q)')
    if user_input == 'q':
        game_running = False
        break
    elif user_input == 'd':
        direction = [1,0]
    elif user_input == 'w':
        direction = [0,-1]
    elif user_input == 's':
        direction = [0,1]
    elif user_input == 'a':
        direction = [-1,0]
    else:
        direction = [0,0]
        print('that is not a valid option, please try again')
        continue

# calculate the new position of the head snake
    current_snake_head = snake[0]
    new_x = current_snake_head[0] + direction[0]
    new_y = current_snake_head[1] + direction[1]
    new_snake_head = [new_x, new_y]

    
    def head_reach_border(head):
        snake_head_x_reach_min_border = head == border_min_value
        snake_head_x_reach_max_border = head == border_max_value
        return snake_head_x_reach_min_border or snake_head_x_reach_max_border

    snake_head_x_reach_border = head_reach_border(new_snake_head[0])
    snake_head_y_reach_border = head_reach_border(new_snake_head[1])
   
    if new_snake_head in snake or snake_head_x_reach_border or snake_head_y_reach_border:
        print('💥GAME OVER!!💀')
        break
    
    # insert the new head into the snake body
    snake.insert(0,new_snake_head)

    if new_snake_head == apple_postion:
        import random
        print ('YAYYY!!! you ate an apple🥳')
        score = score + 1 
        print (f'score:{score}')
        #apple_postion =[random.randint(0,grid_size-1), random.randint(0,grid_size-1)]
        apple_postion = [random.randint(1, grid_size - 2), random.randint(1, grid_size -2)]
    else:
        #remove the old tail 
        snake.pop()
        if new_snake_head == star_position:
             print ('you have got a speed bonus⚡⚡')
             star_position = [random.randint(1, grid_size - 2), random.randint(1, grid_size -2)]
        elif new_snake_head == obtacle_position:
            print ('you died!!💀💀')
            break
        else:
            continue