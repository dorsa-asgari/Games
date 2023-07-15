import random
import tkinter as tk


class Player:
    def __init__(self, marker="X", is_human=True, color="red"):
        self.marker = marker
        self.is_human = is_human
        self.color = color
        self.opponentMarker = "O" if marker == "X" else "X"

    def get_computer_move(self, board):
        # use AI to get computer move
        win_cell = self.canIWin(board)
        block_cell = self.canOpponentWin(board)

        if win_cell:
            return win_cell
        elif block_cell:
            return block_cell
        elif board[0][0] == 0 or board[0][2] == 0 or board[2][0] == 0 or board[2][2] == 0:    # select random between 4 corners if empty
            empty_pos = []
            for i, j in [[0, 0], [0, 2], [2, 0], [2, 2]]:
                if board[i][j] == 0:
                    empty_pos.append([i, j])
            return random.choice(empty_pos)
        elif board[1][1] == 0:             # if central cell is empty return that
            return [1, 1]
        else:
            empty_pos = []
            for i, j in [[0, 1], [1, 0], [1, 2], [2, 1]]:
                if board[i][j] == 0:
                    empty_pos.append([i, j])
            return random.choice(empty_pos)

    def canIWin(self, board):
        # if computer can do a move and win the position will return unless return false
        for i in range(3):
            result = self.check3CellForWin(board, [[i, 0], [i, 1], [i, 2]], self.marker)     # check rows
            if result:
                return result
            result = self.check3CellForWin(board, [[0, i], [1, i], [2, i]], self.marker)     # check columns
            if result:
                return result

        result = self.check3CellForWin(board, [[0, 0], [1, 1], [2, 2]], self.marker)         # check diagonal 1
        if result:
            return result
        result = self.check3CellForWin(board, [[0, 2], [1, 1], [2, 0]], self.marker)         # check diagonal 1
        if result:
            return result
        return False

    def canOpponentWin(self, board):
        # if opponent can do a move and win the position to block the move will return unless return false
        for i in range(3):
            result = self.check3CellForWin(board, [[i, 0], [i, 1], [i, 2]], self.opponentMarker)      # check rows
            if result:
                return result
            result = self.check3CellForWin(board, [[0, i], [1, i], [2, i]], self.opponentMarker)      # check columns
            if result:
                return result

        result = self.check3CellForWin(board, [[0, 0], [1, 1], [2, 2]], self.opponentMarker)          # check diagonal 1
        if result:
            return result
        result = self.check3CellForWin(board, [[0, 2], [1, 1], [2, 0]], self.opponentMarker)          # check diagonal 1
        if result:
            return result
        return False

    def check3CellForWin(self, board, cells: list, marker):
        # if with a move in 3 cells can win the position of that will return unless return false
        counter = []
        for i, j in cells:
            if board[i][j] == marker:
                counter.append(1)      # if the cell is my cell
            elif board[i][j] == 0:
                counter.append(0)      # if cell is empty
            else:
                break                  # id cell is for opponent
        if counter.count(1) == 2 and counter.count(0) == 1:
            return cells[counter.index(0)]
        return False


class Board:
    turn = 0

    def __init__(self, root, players):
        self.players = players
        self.game_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.create_board()
        self.turn = random.randrange(0, 2)       # select randomly between player 1 and 2
        current_player = self.players[self.turn]
        self.changeStatusLabel(current_player)
        if not current_player.is_human:          # check if the first player is computer
            # make first move by computer player
            position = current_player.get_computer_move(self.game_board)
            self.make_move(position, current_player)


    def create_board(self):
        # create GUI
        self.createGUI()
        self.buttons = self.createButtons()

    def createButtons(self):
        # create a list of buttons
        buttons = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(3):
            for j in range(3):
                buttons[i][j] = tk.Button(self.root, text="", bd=0, highlightthickness=0, bg="#fff", font=("Arial", 25), disabledforeground="#000", activebackground="#fff", width=4, height=2, command=lambda i=i, j=j: self.pressed([i, j]))
                buttons[i][j].grid(row=i * 2 + 1, column=j * 2)

        # create lines between 9 cells(buttons)
        tk.Frame(self.root, bg="black", width=220).grid(row=2, column=0, columnspan=5)
        tk.Frame(self.root, bg="black", width=220).grid(row=4, column=0, columnspan=5)
        tk.Frame(self.root, bg="black", height=270).grid(row=1, column=1, rowspan=5)
        tk.Frame(self.root, bg="black", height=270).grid(row=1, column=3, rowspan=5)
        return buttons

    def createGUI(self):
        # create and place status label and QUIT button
        self.status = tk.Label(self.root, text="status:")
        self.status.grid(row=0, column=0, columnspan=4, sticky="w")
        tk.Button(self.root, text="QUIT", command=lambda: self.root.destroy()).grid(row=0, column=4, sticky="e")

    def make_move(self, position, player):
        self.game_board[position[0]][position[1]] = player.marker                       # change the game_board list
        self.buttons[position[0]][position[1]].config(disabledforeground=player.color)  # change the button's text color
        self.buttons[position[0]][position[1]].configure(text=player.marker)            # change the button's text
        self.buttons[position[0]][position[1]]['state'] = 'disabled'                    # set the button to disable and can not be clickable any more

        # check if the player won
        if self.is_winner(player):
            self.changeStatusLabel(player, winner=True)
            self.disableGame()
            return

        # check if it is tied
        if self.is_tie():
            self.changeStatusLabel(player, tie=True)
            self.disableGame()
            return

        self.turn = 1 - self.turn                    # assign the class variable "turn" properly toggle between 1 and 0
        self.changeStatusLabel(self.players[self.turn])  # update the status label to declare whose turn is it

    def is_winner(self, player):
        # check if the player has won
        if self.game_board[0][0] == player.marker and self.game_board[0][1] == player.marker and self.game_board[0][2] == player.marker:
            return True
        elif self.game_board[1][0] == player.marker and self.game_board[1][1] == player.marker and self.game_board[1][2] == player.marker:
            return True
        elif self.game_board[2][0] == player.marker and self.game_board[2][1] == player.marker and self.game_board[2][2] == player.marker:
            return True
        elif self.game_board[0][0] == player.marker and self.game_board[1][0] == player.marker and self.game_board[2][0] == player.marker:
            return True
        elif self.game_board[0][1] == player.marker and self.game_board[1][1] == player.marker and self.game_board[2][1] == player.marker:
            return True
        elif self.game_board[0][2] == player.marker and self.game_board[1][2] == player.marker and self.game_board[2][2] == player.marker:
            return True
        elif self.game_board[0][0] == player.marker and self.game_board[1][1] == player.marker and self.game_board[2][2] == player.marker:
            return True
        elif self.game_board[0][2] == player.marker and self.game_board[1][1] == player.marker and self.game_board[2][0] == player.marker:
            return True
        return False

    def is_tie(self):
        # check if game_board has any "empty" slot available
        for i in self.game_board:
            for j in i:
                if j == 0:
                    return False
        return True

    def pressed(self, position):
        # call when a cell(button) clicked
        self.make_move(position, self.players[self.turn])
        current_player = self.players[self.turn]
        if not self.players[self.turn].is_human:  # check if is computer turn or not and make a play if is computer turn
            computer_position = current_player.get_computer_move(self.game_board)
            self.make_move(computer_position, current_player)

    def changeStatusLabel(self, player, winner=False, tie=False):
        # changing status label to a player or set the winner name or set TIE
        if tie:
            self.status.configure(text="TIE", fg="blue")
        elif not winner:
            if player.is_human:
                self.status.configure(text="status: Your Turn", fg="black")
            else:
                self.status.configure(text="status: Computer Turn", fg="black")
        else:
            if player.is_human:
                self.status.configure(text="Winner: YOU", fg="green")
            else:
                self.status.configure(text="Winner: Computer", fg="green")

    def disableGame(self):
        # disable all cells(buttons) when the game end(tie or have winner)
        for i in self.buttons:
            for j in i:
                j['state'] = 'disabled'


root = tk.Tk()
root.resizable(False, False)
player1 = Player("X", True, "red")
player2 = Player("O", False, "blue")
players = [player1, player2]
board = Board(root, players)

root.mainloop()