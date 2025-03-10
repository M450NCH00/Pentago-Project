
## PENTAGO GAME PROJECT 
## CREATED BY CHOO ZHEN MING
## DATE CREATED: 31/10/2023
## DATE MODIFIED: 03/11/2023

##############################################################################################
#################################                            #################################
#################################       IMPORT MODULES       #################################
#################################                            #################################
##############################################################################################


import pygame
import sys
from random import *


##############################################################################################
#################################                            #################################
#################################    GAME LOGIC FUNCTIONS    #################################
#################################                            #################################
##############################################################################################


####################                         ####################
####################     BASIC FUNCTIONS     ####################
####################                         ####################


# check if move is valid
# returns True/False
def check_move(board, move):
    if board[move[0]][move[1]] == 0:
        return True
    else:
        return False


# check_move()
# returns list of all valid moves
def valid_moves(board):
    Valid_moves = []
    for i in range(0, 6):
        for j in range(0, 6):
            if check_move(board, (i, j)) == True:
                Valid_moves.append((i, j))
    return Valid_moves
    
    
# place the player's marble on the board
# returns the newboard
def place_move(board, player, move):
    newboard = [i[:] for i in board]
    newboard[move[0]][move[1]] = player
    return newboard
    

# rotate the board clockwise a = 1, 3, 5, 7
# rotate the board counter-clockwise a = 2, 4, 6, 8
# returns the newboard
# 1: top right subgrid      2: top right subgrid
# 3: bottom right subgrid   4: bottom right subgrid
# 5: bottom left subgrid    6: bottom left subgrid
# 7: top left subgrid       8: top left subgrid
def rotate_board(board, a):
    newboard = [i[:] for i in board]
    if a == 1 or a == 2:
        r, c = 0, 3
    elif a == 3 or a == 4:
        r, c = 3, 3
    elif a == 5 or a == 6:
        r, c = 3, 0
    elif a == 7 or a == 8:
        r, c = 0, 0

    if a & 1 == 1:
        newboard[r][c], newboard[r][c+2], newboard[r+2][c+2], newboard[r+2][c] = newboard[r+2][c], newboard[r][c], newboard[r][c+2], newboard[r+2][c+2]
        newboard[r][c+1], newboard[r+1][c+2], newboard[r+2][c+1], newboard[r+1][c] = newboard[r+1][c], newboard[r][c+1], newboard[r+1][c+2], newboard[r+2][c+1]
    else:
        newboard[r+2][c], newboard[r][c], newboard[r][c+2], newboard[r+2][c+2] = newboard[r][c], newboard[r][c+2], newboard[r+2][c+2], newboard[r+2][c]
        newboard[r+1][c], newboard[r][c+1], newboard[r+1][c+2], newboard[r+2][c+1] = newboard[r][c+1], newboard[r+1][c+2], newboard[r+2][c+1], newboard[r+1][c]

    return newboard
                

####################                                ####################
####################     CHECKING GAME RESULTS      ####################
####################                                ####################


# check diagonal victory
# returns (win1, win2) in tuple form
def diag_victory(board, a, b, win1, win2):
    if board[1+a][0+b] == board[2+a][1+b] == board[3+a][2+b] == board[4+a][3+b] == board[5+a][4+b]:
        if board[1+a][0+b] == 1:
            win1 += 1
        elif board[1+a][0+b] == 2:
            win2 += 1

    if board[0-a][4+b] == board[1-a][3+b] == board[2-a][2+b] == board[3-a][1+b] == board[4-a][0+b]:
        if board[0-a][4+b] == 1:
            win1 += 1
        elif board[0-a][4+b] == 2:
            win2 += 1

    return (win1, win2)


# check which player wins or draw when both won (before and after rotation)
# returns 1 --> player 1 wins
# returns 2 --> player 2 wins
# returns 0 --> no one wins or draw
# returns -1 --> draw
def check_victory(board):
    win1 = 0
    win2 = 0
    #check rows
    for i in range(0, 6):
        row_1 = board[i][0:5]
        row_2 = board[i][1:6]
        if row_1.count(1) == 5 or row_2.count(1) == 5:
            win1 += 1
        elif row_1.count(2) == 5 or row_2.count(2) == 5:
            win2 += 1

        if win1 > 0 and win2 > 0:
            return -1

    #check columns
    for j in range(0, 6):
        for k in range(0, 2):
            if board[0+k][j] == board[1+k][j] == board[2+k][j] == board[3+k][j] == board[4+k][j] == 1:
                win1 += 1
            elif board[0+k][j] == board[1+k][j] == board[2+k][j] == board[3+k][j] == board[4+k][j] == 2:
                win2 += 1

            if win1 > 0 and win2 > 0:
                return -1

    #check diagonals victory
    (win1, win2) = diag_victory(board, 0, 0, win1, win2)
    (win1, win2) = diag_victory(board, -1, 0, win1, win2)
    (win1, win2) = diag_victory(board, 0, 1, win1, win2)
    (win1, win2) = diag_victory(board, -1, 1, win1, win2)

    if win1 > 0 and win2 > 0:
        return -1
    elif win1 == win2 == 0:
        return 0
    elif win1 == 0 and win2 > 0:
        return 2
    elif win1 > 0 and win2 == 0:
        return 1
    



###############################################################################################
################################                               ################################
################################    GRADING LOGIC FUNCTIONS    ################################
################################                               ################################
###############################################################################################

    
####################                             ####################
####################     ELEMENTARY GRADING      ####################
####################                             ####################

    
# check the score of diagonal cases
# returns the grade
def diag_grade(board, player, opponent, a, b, your_grade, oppo_grade):
    newdiag = [board[k+1+a][k+b] for k in range(0, 5)]
    opiece = newdiag.count(opponent)
    ppiece = newdiag.count(player)
    if opiece == 5:
        oppo_grade += 180
    elif ppiece == 5:
        your_grade += 180
    elif opiece == 0:
        your_grade += ppiece
    elif ppiece == 0:
        oppo_grade += opiece
        
    newdiag = [board[k-a][4-k+b] for k in range(0, 5)]
    opiece = newdiag.count(opponent)
    ppiece = newdiag.count(player)
    if opiece == 5:
        oppo_grade += 180
    elif ppiece == 5:
        your_grade += 180
    elif opiece == 0:
        your_grade += ppiece
    elif ppiece == 0:
        oppo_grade += opiece
        
    return (your_grade, oppo_grade)


# check the score of the move made by the opponent and returns the score
# Algorithm = Your grade - Your opponent's grade
# If opponent wins, -180
# If you win, +180
# If you and your opponent don't win, but opponent's pieces is present, +0
# Everything else, +(the number of pieces you have present)
def grade_move(board, player, opponent, move):
    your_grade = 0
    oppo_grade = 0
    newboard = place_move(board, player, move[0])
    newboard = rotate_board(newboard, move[1])

    # check rows and grade them
    for i in range(0, 6):
        for j in range(0, 2):
            newrow = newboard[i][0+j:5+j]
            opiece = newrow.count(opponent)
            ppiece = newrow.count(player)
            if opiece == 5:
                oppo_grade += 180
            elif ppiece == 5:
                your_grade += 180
            elif opiece == 0:
                your_grade += ppiece
            elif ppiece == 0:
                oppo_grade += opiece

    # check columns and grade them
    for i in range(0, 6):
        for j in range(0, 2):
            newcol = [newboard[k+j][i] for k in range(0, 5)]
            opiece = newcol.count(opponent)
            ppiece = newcol.count(player)
            if opiece == 5:
                oppo_grade += 180
            elif ppiece == 5:
                your_grade += 180
            elif opiece == 0:
                your_grade += ppiece
            elif ppiece == 0:
                oppo_grade += opiece
    
    # check diagonal \ and grade them
    (your_grade, oppo_grade) = diag_grade(newboard, player, opponent, 0, 0, your_grade, oppo_grade)
    (your_grade, oppo_grade) = diag_grade(newboard, player, opponent, -1, 0, your_grade, oppo_grade)
    (your_grade, oppo_grade) = diag_grade(newboard, player, opponent, 0, 1, your_grade, oppo_grade)
    (your_grade, oppo_grade) = diag_grade(newboard, player, opponent, -1, 1, your_grade, oppo_grade)

    # make sure having 2 5 in a rows only counts as 1 win
    if oppo_grade > 180:
        oppo_grade = 180

    if your_grade > 180:
        your_grade = 180
        
    return your_grade - oppo_grade
    

####################                              ####################
####################       ADVANCED GRADING       ####################
####################                              ####################


# Advanced grading logic for rows of 6 squares
def advanced_grade_logic(newrow, opponent, player, p_grade, o_grade):
    o_mid = newrow[1:5].count(opponent)
    p_mid = newrow[1:5].count(player)
    o_front = newrow[0:5].count(opponent)
    p_front = newrow[0:5].count(player)
    o_end = newrow[1:6].count(opponent)
    p_end = newrow[1:6].count(player)
    
    if p_front == 5 or p_end == 5 or (p_mid  == 4 and newrow[0] != opponent and newrow[-1] != opponent):
        p_grade += 180
    elif o_front == 5 or o_end == 5 or (o_front == 4 and p_front == 0) or (o_end == 4 and p_end == 0) or (o_mid == 3 and p_mid == 0 and newrow[0] == newrow[-1] == 0):
        o_grade += 180
    elif o_front == 0 or o_end == 0:
        if o_front == 0:
            p_grade += p_front
        if o_end == 0:
            p_grade += p_end
    elif p_front == 0 or p_end == 0:
        if p_front == 0:
            o_grade += o_front
        if o_end == 0:
            o_grade += o_end
    return (p_grade, o_grade)


# Advanced grading logic for rows of 5 squares (short diagonals)
def advanced_grade_short(newrow, opponent, player, p_grade, o_grade):
    opiece = newrow.count(opponent)
    ppiece = newrow.count(player)
    if opiece == 5 or (opiece == 4 and ppiece == 0):
        o_grade += 180
    elif ppiece == 5:
        p_grade += 180
    elif opiece == 0:
        p_grade += ppiece
    elif ppiece == 0:
        o_grade += opiece
    return (p_grade, o_grade)


# Similar to grade_move() function but can recognise checkmating threat
def advanced_grade_move(board, player, opponent, move):
    your_grade = 0
    oppo_grade = 0
    newboard = place_move(board, player, move[0])
    newboard = rotate_board(newboard, move[1])
    
    # check rows and grade them (Advanced)
    for i in range(0, 6):
        newrow = newboard[i][0:6]
        (your_grade, oppo_grade) = advanced_grade_logic(newrow, opponent, player, your_grade, oppo_grade)

    # check columns and grade them (Advanced)
    for i in range(0, 6):
        newrow = [newboard[k][i] for k in range(0, 6)]
        (your_grade, oppo_grade) = advanced_grade_logic(newrow, opponent, player, your_grade, oppo_grade)
        
    # check long diagonals (Advanced)
    newrow = [newboard[i][i] for i in range(0, 6)]
    (your_grade, oppo_grade) = advanced_grade_logic(newrow, opponent, player, your_grade, oppo_grade)

    newrow = [newboard[i][5-i] for i in range(0, 6)]
    (your_grade, oppo_grade) = advanced_grade_logic(newrow, opponent, player, your_grade, oppo_grade)

    # check short diagonals (Advanced)
    newrow = [newboard[i+1][i] for i in range(0, 5)]
    (your_grade, oppo_grade) = advanced_grade_short(newrow, opponent, player, your_grade, oppo_grade)

    newrow = [newboard[i][i+1] for i in range(0, 5)]
    (your_grade, oppo_grade) = advanced_grade_short(newrow, opponent, player, your_grade, oppo_grade)

    newrow = [newboard[i][4-i] for i in range(0, 5)]
    (your_grade, oppo_grade) = advanced_grade_short(newrow, opponent, player, your_grade, oppo_grade)

    newrow = [newboard[i][6-i] for i in range(1, 6)]
    (your_grade, oppo_grade) = advanced_grade_short(newrow, opponent, player, your_grade, oppo_grade)

    # make sure having 2 5 in a rows only counts as 1 win
    if oppo_grade >= 180 and your_grade >= 180:
        return 0
    elif oppo_grade >= 180 and your_grade < 180:
        return -180
    elif your_grade >= 180 and oppo_grade < 180:
        return 180
    else:
        return your_grade - oppo_grade


########################################################################################
################################                       #################################
################################    PENTAGO ENGINES    #################################
################################                       #################################
########################################################################################


####################                         ####################
####################   ENGINE GENERATION 1   ####################
####################                         ####################


# makes random moves
# returns ((row, column), rotation)
def engine_1(board):
    possible_moves = valid_moves(board)
    move = choice(possible_moves)
    rotation = choice([1,2,3,4,5,6,7,8])
    return (move, rotation)


####################                         ####################
####################   ENGINE GENERATION 2   ####################
####################                         ####################


# 1. make moves that wins
#    (i)  if wins, return the move
#    (ii) if can't win, search for opponent's move best move
#         (a) if opponent wins, find another move
#         (b) if opponent can't win, set that move as an acceptable move
# 2. return acceptable move, or a random move if no such move exists
def engine_2(board, pc_player, opponent, depth):
    possible_moves = valid_moves(board)
    acceptable_move = []

    for move in possible_moves:
        cur_board = place_move(board, pc_player, move)
        victor = check_victory(cur_board)
        if victor == pc_player:
            return (move, 1)
        elif victor == opponent:
            continue
        else:
            for rot in range(1, 9):
                cur_board2 = rotate_board(cur_board, rot)
                victor = check_victory(cur_board2)
                if victor == pc_player:
                    return (move, rot)
                elif victor == opponent:
                    continue
                elif len(possible_moves) == 1 or depth == 1:
                    acceptable_move.append((move, rot))
                else:
                    oppo_move = engine_2(cur_board2, opponent, pc_player, depth-1)
                    cur_board3 = place_move(cur_board2, opponent, oppo_move[0])
                    if check_victory(cur_board3) != opponent:
                        cur_board3 = rotate_board(cur_board3, oppo_move[1])
                        if check_victory(cur_board3) != opponent:
                            acceptable_move.append((move, rot))

    if acceptable_move == []:
        return (choice(possible_moves), 1)
    else:
        return choice(acceptable_move)
                

####################                         ####################
####################   ENGINE GENERATION 3   ####################
####################                         ####################

    
# 1. make moves that wins
#    (i)  if wins, set the move as acceptable move and set its grade as 180
#    (ii) if can't win, search for opponent's move best move, grade it and set it as acceptable moves
# 2. return move_array 
def engine_3(board, pc_player, opponent, real_depth, cur_depth):
    possible_moves = valid_moves(board)
    acceptable_moves = []
    done = False

    for move in possible_moves:
        cur_board = place_move(board, pc_player, move)
        victor = check_victory(cur_board)
        if victor == pc_player:
            acceptable_moves = [(180, move, 1)]
            break
        elif victor == opponent:
            continue
        else:
            for rot in range(1, 9):
                cur_board2 = rotate_board(cur_board, rot)
                victor = check_victory(cur_board2)
                if victor == pc_player:
                    acceptable_moves = [(180, move, rot)]
                    done = True
                    break
                elif victor == opponent:
                    acceptable_moves.append((-180, move, rot))
                elif len(possible_moves) == 1 or cur_depth == 1:
                    grade = grade_move(cur_board2, pc_player, opponent, (move, rot))
                    acceptable_moves.append((grade, move, rot))
                else:
                    oppo_moves = engine_3(cur_board2, opponent, pc_player, real_depth, cur_depth-1)
                    # sort oppo_moves
                    oppo_moves = sorted(oppo_moves, key=lambda x: x[0], reverse=True)
                    grade = grade_move(cur_board2, pc_player, opponent, (move, rot))
                    acceptable_moves.append((grade-oppo_moves[0][0], move, rot))

            if done:
                break

    if real_depth == cur_depth:
        acceptable_moves = sorted(acceptable_moves, key=lambda x: x[0], reverse=True)
        return (acceptable_moves[0][1], acceptable_moves[0][2])
    else:
        return acceptable_moves


####################                         ####################
####################   ENGINE GENERATION 4   ####################
####################                         ####################

    
# Essentially just engine 3 but with advanced grading system
# Should be able to make greater moves with faster speed
def engine_4(board, pc_player, opponent, real_depth, cur_depth):
    possible_moves = valid_moves(board)
    acceptable_moves = []
    done = False
    highest_grade = -180
    for move in possible_moves:
        cur_board = place_move(board, pc_player, move)
        victor = check_victory(cur_board)
        if victor == pc_player:
            acceptable_moves = [(180, move, 1)]
            break
        elif victor == opponent:
            continue
        else:
            for rot in range(1, 9):
                cur_board2 = rotate_board(cur_board, rot)
                grade = advanced_grade_move(cur_board, pc_player, opponent, (move, rot))
                victor = check_victory(cur_board2)
                if victor == pc_player: #grade == 180: #
                    acceptable_moves = [(180, move, rot)]
                    done = True
                    break
                elif victor == opponent and acceptable_moves == []: #grade == -180 and acceptable_moves == []: #
                    acceptable_moves.append((-180, move, rot))
                elif len(possible_moves) == 1 or cur_depth == 1:
                    if grade > highest_grade:
                        acceptable_moves.append((grade, move, rot))
                        highest_grade = grade
                else:
                    oppo_moves = engine_4(cur_board2, opponent, pc_player, real_depth, cur_depth-1)
                    # sort oppo_moves
##                    if oppo_moves == []:
##                        print()
##                        print(cur_depth, pc_player, grade, (move, rot), possible_moves)
##                        print(acceptable_moves)
##                        for i in range(0, 6):
##                            print(*cur_board2[i])
                    oppo_moves = sorted(oppo_moves, key=lambda x: x[0], reverse=True)
                    acceptable_moves.append((grade-oppo_moves[0][0], move, rot))

            if done:
                break

    if real_depth == cur_depth:
        acceptable_moves = sorted(acceptable_moves, key=lambda x: x[0], reverse=True)
        return (acceptable_moves[0][1], acceptable_moves[0][2])
    else:
        return acceptable_moves




########################################################################################
#################################                      #################################
#################################   PYGAME INTERFACE   #################################
#################################                      #################################
########################################################################################


####################                      ####################
####################   PYGAME VARIABLES   ####################
####################                      ####################

    
# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 6
GRID_WIDTH = 400
GRID_HEIGHT = 400
CELL_SIZE = GRID_WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
Player1 = (80, 200, 120)
Player2 = (250, 128, 114)


# Menu
font = pygame.font.SysFont('Georgia', 40, bold = True)
surf = font.render('Easy', True, 'white')
surf_mid = font.render('Medium', True, 'white')
surf_hard = font.render('Hard', True, 'white')
surf_diff = font.render('Difficult', True, 'white')
surf_p1 = font.render('Player 1', True, 'white')
surf_p2 = font.render('Player 2', True, 'white')

easy_width = 200
easy_height = 60
easy_button = pygame.Rect(100, 65, easy_width, easy_height)
mid_button = pygame.Rect(100, 135, easy_width, easy_height)
hard_button = pygame.Rect(100, 205, easy_width, easy_height)
diff_button = pygame.Rect(100, 275, easy_width, easy_height)

p1_button = pygame.Rect(100, 135, easy_width, easy_height)
p2_button = pygame.Rect(100, 205, easy_width, easy_height)


####################                      ####################
####################   PYGAME FUNCTIONS   ####################
####################                      ####################


# Draw the board
def draw_board(board, screen, x_offset=0, y_offset=0):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 0:
                color = WHITE
            elif board[row][col] == 1:
                color = Player1
            elif board[row][col] == 2:
                color = Player2
            pygame.draw.rect(screen, color, (col * CELL_SIZE + x_offset, row * CELL_SIZE + y_offset, CELL_SIZE, CELL_SIZE))
    for x in range(x_offset, GRID_WIDTH + x_offset, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, y_offset), (x, GRID_HEIGHT + y_offset), 2)
    for y in range(y_offset, GRID_HEIGHT + y_offset, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x_offset, y), (GRID_WIDTH + x_offset, y), 2)


# Decides the winner and whether the game continues
# return running True/False
def announce_progress(board, Player, Bot, run):
    winner = check_victory(board)
    if winner == Player or winner == Bot or winner == -1:
        run = False
    elif winner == 0:
        pass
    else:
        print(winner)
        run = False
    return run


# Result window
# return if you wanna play again
def result_window(board, winner, player):
    win = pygame.display.set_mode((600, 550))  # Create a new window
    pygame.display.set_caption("Results")
    
    win.fill((211, 211, 211))  
    font = pygame.font.SysFont('Georgia', 36, bold = True)
    font2 = pygame.font.SysFont('Georgia', 26, bold = True)
    if winner == player:
        text = font.render("You Win!", True, (80, 200, 120))  # Create the text
        text_rect = text.get_rect(center=(300, 35))  # Center the text
        win.blit(text, text_rect)  # Draw the text on the new window
    elif winner != 0 and winner != -1:
        text = font.render("You Lost!", True, (250, 20, 20))  # Create the text
        text_rect = text.get_rect(center=(300, 35))  # Center the text
        win.blit(text, text_rect)
    else:
        text = font.render("You Tied!", True, (230, 230, 250))  # Create the text
        text_rect = text.get_rect(center=(300, 35))  # Center the text
        win.blit(text, text_rect)

    text2 = font2.render("Press Space to Go back to Menu!", True, (123, 104, 238))  # Create the text
    text_rect2 = text2.get_rect(center=(300, 70))  # Center the text
    win.blit(text2, text_rect2)

    draw_board(board, win, 105, 120)
    pygame.display.update()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    return True




########################################################################################
###############################                          ###############################
###############################   MAIN PYGAME FUNCTION   ###############################
###############################                          ###############################
########################################################################################


####################                        ####################
####################   BOTS STRENGTH TEST   ####################
####################                        ####################

                
# Test the strength of bots
def botvsbot(board, olevel, ylevel, Player):
    screen = pygame.display.set_mode((GRID_WIDTH-2, GRID_HEIGHT-2))
    pygame.display.set_caption("Pentago Game")
    
    running = True
    First = "N"
    Turn = 36

    if Player == 1:
        Bot = 2
    else:
        Bot = 1
        First = "Y"

    while running:
        if First == "Y":
            # Opponent bot place down marble
            if olevel == 1:
                (PC_move, PC_rotate) = engine_1(board)
            elif olevel == 2:
                (PC_move, PC_rotate) = engine_2(board, Bot, Player, 2)
            elif olevel == 3:
                (PC_move, PC_rotate) = engine_3(board, Bot, Player, 2, 2)
            elif olevel == 4:
                (PC_move, PC_rotate) = engine_4(board, Bot, Player, 2, 2)
                
            board[PC_move[0]][PC_move[1]] = Bot

            screen.fill(WHITE)
            draw_board(board, screen)
            pygame.display.flip()
            running = announce_progress(board, Player, Bot, running)

            if running == False:
                break

            # Opponet bot rotate board
            board = rotate_board(board, PC_rotate)

            screen.fill(WHITE)
            draw_board(board, screen)
            pygame.display.flip()
            running = announce_progress(board, Player, Bot, running)
            Turn -= 1

            if Turn == 0:
                running = False
                
            if running == False:
                break

        # Your bot place down marble
        if ylevel == 1:
            (PC_move, PC_rotate) = engine_1(board)
        elif ylevel == 2:
            (PC_move, PC_rotate) = engine_2(board, Player, Bot, 2)
        elif ylevel == 3:
            (PC_move, PC_rotate) = engine_3(board, Player, Bot, 2, 2)
        elif ylevel == 4:
            (PC_move, PC_rotate) = engine_4(board, Player, Bot, 2, 2)
                
        board[PC_move[0]][PC_move[1]] = Player

        screen.fill(WHITE)
        draw_board(board, screen)
        pygame.display.flip()
        running = announce_progress(board, Player, Bot, running)

        if running == False:
            break

        # Your bot rotate board
        board = rotate_board(board, PC_rotate)

        screen.fill(WHITE)
        draw_board(board, screen)
        pygame.display.flip()
        running = announce_progress(board, Player, Bot, running)
        Turn -= 1
        
        if Turn == 0:
            running = False
            
        if running == False:
            break

        if First == "N":
            First = "Y"

    return (check_victory(board), Player, board)


####################                           ####################
####################   MAIN PROGRAM FUNCTION   ####################
####################                           ####################


# Run the main program
def main(board):
    screen = pygame.display.set_mode((GRID_WIDTH-2, GRID_HEIGHT-2))
    pygame.display.set_caption("Pentago Game")
    
    running = True
    menu1 = True
    menu2 = True

    # choose difficulty (menu1)
    while menu1:
        screen.fill(WHITE)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                menu1 = False

            if e.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(e.pos):
                    level = 1
                    menu1 = False
                elif mid_button.collidepoint(e.pos):
                    level = 2
                    menu1 = False
                elif hard_button.collidepoint(e.pos):
                    level = 3
                    menu1 = False
                elif diff_button.collidepoint(e.pos):
                    level = 4
                    menu1 = False

        m_a, m_b = pygame.mouse.get_pos()
        if easy_button.x <= m_a <= easy_button.x + easy_width and easy_button.y <= m_b <= easy_button.y + easy_height:
            pygame.draw.rect(screen, (180, 180, 180), easy_button)
        else:
            pygame.draw.rect(screen, (110, 110, 110), easy_button)
        screen.blit(surf, (easy_button.x + 50, easy_button.y + 5))

        if mid_button.x <= m_a <= mid_button.x + easy_width and mid_button.y <= m_b <= mid_button.y + easy_height:
            pygame.draw.rect(screen, (180, 180, 180), mid_button)
        else:
            pygame.draw.rect(screen, (110, 110, 110), mid_button)
        screen.blit(surf_mid, (mid_button.x + 15, mid_button.y + 6))

        if hard_button.x <= m_a <= hard_button.x + easy_width and hard_button.y <= m_b <= hard_button.y + easy_height:
            pygame.draw.rect(screen, (180, 180, 180), hard_button)
        else:
            pygame.draw.rect(screen, (110, 110, 110), hard_button)
        screen.blit(surf_hard, (hard_button.x + 45, hard_button.y + 6))

        if diff_button.x <= m_a <= diff_button.x + easy_width and diff_button.y <= m_b <= diff_button.y + easy_height:
            pygame.draw.rect(screen, (180, 180, 180), diff_button)
        else:
            pygame.draw.rect(screen, (110, 110, 110), diff_button)
        screen.blit(surf_diff, (diff_button.x + 15, diff_button.y + 6))

        pygame.display.update()

    
    # choose who goes first (menu2)
    while menu2:
        screen.fill(WHITE)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                menu2 = False

            if e.type == pygame.MOUSEBUTTONDOWN:
                if p1_button.collidepoint(e.pos):
                    Player = 1
                    menu2 = False
                elif p2_button.collidepoint(e.pos):
                    Player = 2
                    menu2 = False

        m_a, m_b = pygame.mouse.get_pos()
        if p1_button.x <= m_a <= p1_button.x + easy_width and p1_button.y <= m_b <= p1_button.y + easy_height:
            pygame.draw.rect(screen, (180, 180, 180), p1_button)
        else:
            pygame.draw.rect(screen, (110, 110, 110), p1_button)
        screen.blit(surf_p1, (p1_button.x + 17, p1_button.y + 5))

        if p2_button.x <= m_a <= p2_button.x + easy_width and p2_button.y <= m_b <= p2_button.y + easy_height:
            pygame.draw.rect(screen, (180, 180, 180), p2_button)
        else:
            pygame.draw.rect(screen, (110, 110, 110), p2_button)
        screen.blit(surf_p2, (p2_button.x + 17, p2_button.y + 5))

        pygame.display.update()
    
    First = "N"
    Turn = 36

    if Player == 1:
        Bot = 2
    else:
        Bot = 1
        First = "Y"

    while running:
        screen.fill(WHITE)
        draw_board(board, screen)
        pygame.display.flip()

        for event in pygame.event.get():
            P_move = True
            P_rotate = True
            
            if event.type == pygame.QUIT:
                running = False

            if First == "Y":
                # Computer place down marble
                if level == 1:
                    (PC_move, PC_rotate) = engine_1(board)
                elif level == 2:
                    (PC_move, PC_rotate) = engine_2(board, Bot, Player, 2)
                elif level == 3:
                    (PC_move, PC_rotate) = engine_3(board, Bot, Player, 2, 2)
                elif level == 4:
                    (PC_move, PC_rotate) = engine_4(board, Bot, Player, 2, 2)
                    
                board[PC_move[0]][PC_move[1]] = Bot

                screen.fill(WHITE)
                draw_board(board, screen)
                pygame.display.flip()

                running = announce_progress(board, Player, Bot, running)

                if running == False:
                    break

                # Computer rotate board
                board = rotate_board(board, PC_rotate)

                screen.fill(WHITE)
                draw_board(board, screen)
                pygame.display.flip()

                running = announce_progress(board, Player, Bot, running)
                Turn -= 1

                if Turn == 0:
                    running = False
                    
                if running == False:
                    break

            # You place your marble
            while P_move:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        P_move = False
                        
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button
                            x, y = event.pos
                            col = x // CELL_SIZE
                            row = y // CELL_SIZE
                            if (row, col) in valid_moves(board):
                                board[row][col] = Player
                                P_move = False
                                break
                            else:
                                print("\nMAKE A VALID MOVE!")

            if running == False:
                break
            
            screen.fill(WHITE)
            draw_board(board, screen)
            pygame.display.flip()

            running = announce_progress(board, Player, Bot, running)

            if running == False:
                break

            # You rotate the board
            while P_rotate:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        P_rotate = False
                        
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            board = rotate_board(board, 1)
                            P_rotate = False
                            break
                        elif event.key == pygame.K_2:
                            board = rotate_board(board, 2)
                            P_rotate = False
                            break
                        elif event.key == pygame.K_3:
                            board = rotate_board(board, 3)
                            P_rotate = False
                            break
                        elif event.key == pygame.K_4:
                            board = rotate_board(board, 4)
                            P_rotate = False
                            break
                        elif event.key == pygame.K_5:
                            board = rotate_board(board, 5)
                            P_rotate = False
                            break
                        elif event.key == pygame.K_6:
                            board = rotate_board(board, 6)
                            P_rotate = False
                            break
                        elif event.key == pygame.K_7:
                            board = rotate_board(board, 7)
                            P_rotate = False
                            break
                        elif event.key == pygame.K_8:
                            board = rotate_board(board, 8)
                            P_rotate = False
                            break
                        else:
                            print("\nPRESS A NUMBER BETWEEN 1 TO 8 ONLY!")

            if running == False:
                break
            
            screen.fill(WHITE)
            draw_board(board, screen)
            pygame.display.flip()
            
            running = announce_progress(board, Player, Bot, running)
            Turn -= 1
            
            if Turn == 0:
                running = False
                
            if running == False:
                break

            if First == "N":
                First = "Y"

    return (check_victory(board), Player, board)




########################################################################################
#################################                      #################################
#################################   RUN REAL PROGRAM   #################################
#################################                      #################################
########################################################################################


again = True
while again == True:
    board = [[0 for _ in range(6)] for _ in range(6)]
    (winner, player, board) = main(board)
    again = result_window(board, winner, player)




########################################################################################
#################################                      #################################
#################################      BOT VS BOT      #################################
#################################                      #################################
########################################################################################

        
##again = True
##
##rounds = 50        # Choose how many rounds
##your_bot = 4      # Choose your bot engine level (1, 2, 3, 4)
##oppo_bot = 2      # Choose your opponent's bot engine level (1, 2, 3, 4)
##your_player = 1   # Choose your bot's turn (Go first: 1, Go second: 2)
##
##wins, draws, losts = 0, 0, 0
##
##while again == True:
##    board = [[0 for _ in range(6)] for _ in range(6)]
##    
##    print("\nRound:", rounds)
##    rounds -= 1
##    
##    (winner, player, board) = botvsbot(board, oppo_bot, your_bot, your_player)
##    
##    if winner == player:
##        print("\nYOU WON!")
##        wins += 1
##    elif winner == 0 or winner == -1:
##        print("\nIT'S A TIE!")
##        draws += 1
##    else:
##        print("\nYOU LOST!")
##        losts += 1
##
##    print()
##    for i in board:
##        for j in i:
##            print(j, end = " ")
##        print()
##            
##    if rounds == 0:
##        again = False
##    else:
##        again = True

