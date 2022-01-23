def board_start(startboard):
    print("This is our game board")
    print(" " + startboard[7] + "  " + '|' + " " + startboard[8] + "  " + '|' + "  " + startboard[9])
    print("--------------")
    print(" " + startboard[4] + "  " + '|' + " " + startboard[5] + "  " + '|' + "  " + startboard[6])
    print("--------------")
    print(" " + startboard[1] + "  " + '|' + " " + startboard[2] + "  " + '|' + "  " + startboard[3])
    time.sleep(1)
    print("Ready?")
    time.sleep(2)
    print("GO!")
    time.sleep(1)
def display_board(board):
    print(" ")
    print(" "+board[7] + "  " +'|'+ " "+ board[8] + "  " +'|'+ "  " +board[9])
    print("--------------")
    print(" "+board[4] + "  " +'|'+ " "+ board[5] + "  " +'|'+ "  " +board[6])
    print("--------------")
    print(" "+board[1] + "  " +'|'+ " "+ board[2] + "  " +'|'+ "  " +board[3])
def player_input():
    marker = ''
    while marker != "X" and marker != "O":
        marker = input("Player 1, choose 'X' or 'O' \n").upper()
        player1_marker = marker

    if marker == "X":
        print("Player 1 is 'X' and Player 2 is 'O'")
        player2_marker = "O"
        return (player1_marker, player2_marker)
    else:
        player2_marker = "X"
        print("Player 1 is 'O' and Player 2 is 'X'")
        return (player1_marker, player2_marker)



def place_marker(board,marker,position):
    board[position] = marker


def win_check(board, marker):

    return ((board[1] == marker and board[2] == marker and board[3] == marker) or
            (board[4] == marker and board[5] == marker and board[6] == marker) or
            (board[7] == marker and board[8] == marker and board[9] == marker) or
            (board[1] == marker and board[4] == marker and board[7] == marker) or
            (board[2] == marker and board[5] == marker and board[8] == marker) or
            (board[3] == marker and board[6] == marker and board[9] == marker) or
            (board[1] == marker and board[5] == marker and board[9] == marker) or
            (board[3] == marker and board[5] == marker and board[7] == marker))


import random

def choose_first():
    gracze=["Player 1 begins","Player 2 begins"]
    zaczyna = random.choice(gracze)
    if zaczyna=="Player 1 begins":
        turn=player1_marker
    else:
        turn=player2_marker
    print(zaczyna)
    return turn



def space_check(board, position):
    if board[position] == "O" or board[position] == "X":
        print("This spot is taken! Choose one that's available!")
        return False
    else:
        print("Free space")
        return board[position] == " "



def full_board_check(board):
    for position in range(1,9):
        if board[1]!=" " and board[2]!=" " and board[3]!=" " and board[4]!=" " and board[5]!=" " and board[6]!=" " and board[7]!=" " and board[8]!=" " and board[9]!=" ":
            return True
        else:
            return False



def player_choice(board):
    position = " "
    while True:
        try:
            position =int(input("Where would you like to put your mark (1-9)? \n"))
            while position not in [1,2,3,4,5,6,7,8,9] or space_check(board, position)==False:
                position = int(input("Where would you like to put your mark (1-9)? \n"))
            else:
                return position
        except ValueError:
            print("Number! Provide an available number from 1 to 9!")

def replay():
    return input("Would you like to play again? (y/n)").lower().startswith('y')

def close():
    print("Game is closing.")
    time.sleep(1)
    print("Game is closing..")
    time.sleep(0.5)
    print("Game closed...")


import time
while True:
    board=[" "," "," "," "," "," "," "," "," "," "]
    startboard=[" ","1","2","3","4","5","6","7","8","9"]
    player1_marker, player2_marker = player_input()
    turn = choose_first()


    play_game=" "
    while play_game.lower()!="y" and play_game.lower()!="n":
        play_game=input("Are you ready to play (y/n)?")
    if play_game.lower() == "y":
        print("Let's go!")
        game_on=True

    if play_game.lower()=="n":
        close()
        game_on = False
        replay()
        break

    print("Welcome to Tic Tac Toe!")
    board_start(startboard)
    while game_on == True:
        if turn==player1_marker:
            print("Player 1 - (",player1_marker, "), your move!")
            display_board(board)
            position = player_choice(board)
            place_marker(board, player1_marker, position)
            if win_check(board,player1_marker):
                display_board(board)
                print("Congratulations Player 1, you won the game!")
                game_on=False
            else:
                if full_board_check(board):
                    display_board(board)
                    print("It's a tie")
                    break
                else:
                    turn=player2_marker

        else:
            turn=player2_marker
            print("Player 2 - (",player2_marker,"), your move!")
            display_board(board)
            position = player_choice(board)
            place_marker(board, player2_marker, position)
            if win_check(board,player2_marker):
                display_board(board)
                print("Congratulations Player 2, you won the game!")
                game_on=False
            else:
                if full_board_check(board):
                    display_board(board)
                    print("It's a tie")
                    break
                else:
                    turn=player1_marker
    if not replay():
        close()
        break
    else:
        game_on=True
