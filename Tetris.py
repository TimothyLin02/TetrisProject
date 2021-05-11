import pygame, random, sys
size = (450, 550)
screen = pygame.display.set_mode(size)

Black = (0, 0, 0)
Gray = (200,200,200)
White = (255, 255, 255)
Green = (0, 255, 0)
Red = (255, 0, 0)
Blue = (0, 0, 255)
Purple = (128, 0, 128)
Orange = (255, 165, 0)
Yellow = (255, 255, 0)
LightBlue = (0, 255, 255)

width = 10
length = 20
board = None
shape = None
shape_color = None
shape_col = 0
shape_row = 0
shape_rotate = True
level = 1
score = 0
time = 550
counter = 0
shape_counter = 0

EVENT_TIMER = 26    #create timer event

def new_board():    #create board(2D array). The board will consist of colors. Game logic will occur on the board. The screen
    global board    #will display the colors of the board in its corresponding locations
    board = [[White for i in range(width)] for k in range(length)]  #10 by 20 board

#declare shapes: shape consist of coordinates. (0,0) is the center of the shape
Shape_Z = [[-1, 0], [0, 0], [0, 1], [1, 1]]
Shape_S = [[-1, 1], [0, 1], [0, 0], [1, 0]]
Shape_Square = [[0,1], [1,1], [1,0], [0,0]]
Shape_I = [[-1, 0], [0, 0], [1, 0], [2, 0]]
Shape_L = [[-1 ,1], [-1, 0], [0, 0], [1, 0]]
Shape_RevL = [[-1, 0], [0, 0], [1, 0], [1, 1]]
Shape_T = [[ -1, 0], [0, 0], [1, 0], [0, 1]]
shapes = [Shape_Z, Shape_S, Shape_Square, Shape_I, Shape_L, Shape_RevL, Shape_T]    #place all shapes in list shapes
colors = [Red, Green, Yellow, LightBlue, Blue, Orange, Purple]  #colors corresponding to shape
spins = [True, True, False, True, True, True, True ]    #spin all shapes except square shape

def move(row, col):  #change shape coordinates
    global shape_row, shape_col
    shape_row += row
    shape_col += col

def valid_position():   #check if the shape is in a valid position after movement
    for i, k in shape:
        row = shape_row+i
        col = shape_col+k
        if col<0 or col>=width:
            return False
        if row>=length:
            return False
        if board[row][col]!=White:
            return False
    return True

def go_right(): #function to move shape right
    move(0, 1)
    if not valid_position():    #if shape cannot move right, move back
        move(0, -1)
        return False
    return True

def go_left():  #function to move shape left
    move(0, -1)
    if not valid_position():    #if shape cannot move left, move back
        move(0,1)
        return False
    return True

def go_down():  #function to move shape down
    move(1, 0)
    if not valid_position():    #if shape cannot move down, move back
        move(-1, 0)
        return False
    return True

def drop(): #drop shape to the bottom
    t = 0
    while go_down():
        t += 1
    return t

def rotate():   #function to rotate shape
    global shape, shape_rotate
    if shape_rotate:
        shape = [[j, -i] for i, j in shape]     #algorithm to rotate shape: new x becomes old-y, new y becomes old x
        if not valid_position():    #if cannot rotate shape(invalid position), move back
            shape = [[-j, i] for i, j in shape]
            return False
        return True
    return False

def new_game(): #function to begin the game
    global level, counter, time, shape_counter, score
    level = 1
    score = 0
    counter = 0
    shape_counter = 0
    time = 550
    new_shape()
    new_board()
    pygame.time.set_timer(EVENT_TIMER, time)

def start_game():   #function to begin game; click enter to begin game
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:    #if enter/return key is clicked, begin game
                return True
        elif event.type == pygame.QUIT:
            sys.exit()

def menu(): #start game menu
    screen.fill(White)
    font = pygame.font.SysFont('arial', 50, True, False)
    Tetris_title = font.render("TETRIS", True, Blue)
    screen.blit(Tetris_title, [150, 150])
    font = pygame.font.SysFont('arial', 25, True, False)
    Tetris_play = font.render("press ENTER to start the game", True, Black)
    screen.blit(Tetris_play, [75, 200])
    Controls_spacebar = font.render("SPACEBAR = hard drop", True, Black)
    screen.blit(Controls_spacebar, [75, 225])
    Controls_KEYUP = font.render("UP ARROW = rotate clockwise", True, Black)
    screen.blit(Controls_KEYUP, [75, 250])
    Controls_KEYLEFT = font.render("LEFT ARROW = move left", True, Black)
    screen.blit(Controls_KEYLEFT, [75, 275])
    Controls_KEYRIGHT = font.render("RIGHT ARROW = move right", True, Black)
    screen.blit(Controls_KEYRIGHT, [75, 300])
    Controls_KEYDOWN = font.render("DOWN ARROW = soft drop", True, Black)
    screen.blit(Controls_KEYDOWN, [75, 325])
    pygame.display.flip()

def game_over():    #function to check if game is over; cannot drop shape
    global time
    game_over = False
    for i, k in shape:
        row = shape_row + 1 + i
        col = shape_col + k
        if board[row][col] != White and shape_row <= 0:
            game_over = True
    return game_over

def game_end(): #game over menu
    font = pygame.font.SysFont("arial", 50, True, False)
    GAMEOVER = font.render("GAME OVER", True, Black)
    screen.blit(GAMEOVER, [10, 150])
    font = pygame.font.SysFont('arial', 25, True, False)
    Tetris_replay = font.render("press ENTER to play again", True, Black)
    screen.blit(Tetris_replay, [10, 200])
    score_display = font.render(str(score), True, Black)
    screen.blit(score_display, [150, 225])
    Score_title = font.render("Score:", True, Black)
    screen.blit(Score_title, [75, 225])
    Level_title = font.render("Level:", True, Black)
    screen.blit(Level_title, [75, 250])
    Level_display = font.render(str(level), True, Black)
    screen.blit(Level_display, [150, 250])
    pygame.display.flip()

def new_shape():    #obtain new shape
    global shape, shape_color, shape_row, shape_col, shape_rotate, shape_counter
    shape_row = 0
    shape_col = width//2-1
    if shape_counter<3:
        num = random.randrange(2,7)
        shape_counter+=1
    else:
        num = random.randrange(7)   #get num with random module to obtain random shape
    shape = shapes[num]
    shape_color = colors[num]
    shape_rotate = spins[num]

def paint():
    screen.fill(White)
    for i, row in enumerate(board): #index of row in board
        for k, cell in enumerate(row):  #index of cells in row
            pygame.draw.rect(screen, cell, [k * 25, i * 25, 25, 25])    #color of cell in board transferred to screen
            pygame.draw.rect(screen, Gray, [k * 25, i * 25, 25, 25], 1) #grid

    if shape:
        for i, k in shape:
            row = shape_row+i
            col = shape_col+k
            pygame.draw.rect(screen, shape_color, [col * 25, row * 25, 25, 25])
    # ScoreBoard
    pygame.draw.rect(screen, Black, [270, 50, 150, 200], 4)
    font = pygame.font.SysFont('Calibri', 25, True, False)
    Score_title = font.render("Score", True, Black)
    screen.blit(Score_title, [280, 60])
    score_display = font.render(str(score), True, Black)
    screen.blit(score_display, [280, 80])
    level_title = font.render("Level", True, Black)
    screen.blit(level_title, [280, 120])
    level_display = font.render(str(level), True, Black)
    screen.blit(level_display, [280, 140])
    pygame.display.flip()

def check_final():  #checks if shape has reached the bottom/on top of another colored block
    is_final = False
    for i, k in shape:
        row = shape_row + 1 + i
        col = shape_col + k
        if row == length:       #check if shape is at the bottom of the board
            is_final = True
            break;
        if board[row][col] != White:    #check if shape is on top of another colored block
            is_final = True
            break;
    if is_final:                #if the block is at the bottom/on top of another colored block; execute body
        for i, k in shape:
            row = shape_row + i #place shape onto the board
            col = shape_col + k
            board[row][col] = shape_color
        global counter, time, level
        remove_filled() #check for full lines(row of colors != white), remove if there are full lines
        new_shape()     #add new shape
        counter +=1     #counter for shapes placed added by one
        if counter == 15 and time>=100: #dropping speed increases by 50 every 15 blocks placed
            level += 1                  #speed does not go below 100
            counter = 0
            time -=50
            pygame.time.set_timer(EVENT_TIMER, time)

def is_full(row):   #check if row in board is filled with colored blocks (not white)
    for i in range(width):
        if board[row][i] == White:
            return False
    return True

def is_empty(row):  #check if row in board is empty (row of white blocks)
    for i in range(width):
        if board[row][i] != White:  #if block in row is not white, it is not empty; return false
            return False
    return True

def remove_filled():    #check for full lines, remove line if full
    global score
    for i in range(length-1, 0, -1):
        while is_full(i):
            score += 100    #add score by 100 for each line removed
            for j in range(i, 0, -1):
                for n in range(width):
                    if (j==0):
                        board[j][n] = White
                    else:
                        board[j][n] = board[j-1][n]
        if is_empty(i): #if empty row, don't remove lines (break)
            break

def process_event():    #process the events throughout the game; call functions based on events occurred
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                if go_left():
                    check_final()
                    paint()
            elif event.key==pygame.K_RIGHT:
                if go_right():
                    check_final()
                    paint()
            elif event.key==pygame.K_UP:
                if rotate():
                    check_final()
                    paint()
            elif event.key==pygame.K_DOWN:
                if go_down():
                    check_final()
                    paint()
            elif event.key==pygame.K_SPACE:
                if drop():
                    check_final()
                    paint()
        elif event.type == EVENT_TIMER:
            if go_down():
                check_final()
                paint()
        elif event.type == pygame.QUIT:
            sys.exit()
def main():
    pygame.init()
    pygame.display.set_caption("ICSTetrisCPT")
    menu()      #display game menu
    while True:
        if start_game():
            new_game()
            while not game_over():
                process_event()
            else:
                game_end()  #game end display

if __name__ == "__main__":
   main()
