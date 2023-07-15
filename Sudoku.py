from tkinter import Tk, Canvas, Frame, Button, BOTH, LEFT, TOP, BOTTOM, filedialog, messagebox , IntVar, Radiobutton
import random
import copy
import os


class SudokuSolver():
    def __init__(self, board):
        self.solutionCounter = 0
        self.board = board
        self.values = [i for i in range(1, len(self.board)+1)]

    def validate(self, value, row, col):
        for i in self.board[row]:
            if i == value:
                return False
        for i in self.board:
            if i[col] == value:
                return False
        
        for i in range((row//3)*3, ((row//3)*3)+3):
            for j in range((col//3)*3, ((col//3)*3)+3):
                if self.board[i][j] == value:
                    return False
        
        return True

    def solve(self, count=False):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    for value in self.values:
                        if self.validate(value, row, col):
                            self.board[row][col] = value
                            nextSolve = self.solve(count=count)
                            if not nextSolve:
                                self.board[row][col] = 0
                            else:
                                return True
                    else:
                        return False

        if count:
            self.solutionCounter += 1
            return False
        return True

    def countSolutions(self):
        self.solutionCounter = 0
        self.solve(count=True)
        return self.solutionCounter


class sudokuGenerator():
    def __init__(self) :
        self.width = 9
        self.heght = 9
        self.board = [[0,0,0,0,0,0,0,0,0] for i in range(9)]
        self.values = [i for i in range(1, len(self.board)+1)]

    def validate(self, value, row, col):
        for i in self.board[row]:
            if i == value:
                return False
        for i in self.board:
            if i[col] == value:
                return False
        
        for i in range((row//3)*3, ((row//3)*3)+3):
            for j in range((col//3)*3, ((col//3)*3)+3):
                if self.board[i][j] == value:
                    return False
        
        return True

    def isBoardFull(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False
        return True
    
    def generatePuzzle(self):
        for cell in range(81):
            row  = cell//9
            col = cell%9
            if self.board[row][col] == 0:
                random.shuffle(self.values)
                for value in self.values:
                    if self.validate(value, row,col):
                        self.board[row][col] = value
                        if self.isBoardFull():
                            return True
                        elif self.generatePuzzle():
                            return True
                break
        self.board[row][col] = 0

    def removeCells(self, removeCount = 10):
        localValues = [x for  x in range(9)]
        random.shuffle(localValues)
        
        for row in localValues:
            for col in localValues:
                if self.board[row][col] != 0:
                    cell = self.board[row][col]
                    self.board[row][col] = 0
                    solver = SudokuSolver(self.board)
                    numberOfSolutions = solver.countSolutions()
                    if numberOfSolutions == 1:
                        if removeCount == 1:
                            return True
                        if self.removeCells(removeCount-1):
                            return True
                        else:
                            self.board[row][col] = cell
                    else:
                        self.board[row][col] = cell
        
        return False
    
    def readBoardFromFile(self, path):
        with open(path, 'r') as f:
            lines = f.readlines()
        
        board = []
        for line in lines:
            l = []
            for i in line.strip().replace(" ", "").split(","):
                l.append(int(i))
            board.append(l)
        self.board = board
        return board
                        

class SudokuUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.gameOver = False
        self.radioButtonValue = IntVar(value=1)

        self.createNewBoard(refreshUI=False)

        self.row, self.col = -1, -1

        self.__initUI()

    def __initUI(self):
        self.parent.title("SUDOKU GAME")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)

        self.difficultyFrame = Frame(self)
        self.difficultyFrame.pack()
        self.difficultyRadioButton1 = Radiobutton(self.difficultyFrame , text="Easy", value=1, variable=self.radioButtonValue)
        self.difficultyRadioButton2 = Radiobutton(self.difficultyFrame , text="Medium", value=2, variable=self.radioButtonValue)
        self.difficultyRadioButton3 = Radiobutton(self.difficultyFrame , text="Difficult", value=3, variable=self.radioButtonValue)
        self.difficultyRadioButton1.pack(side = LEFT)
        self.difficultyRadioButton2.pack(side = LEFT)
        self.difficultyRadioButton3.pack(side = LEFT)

        creaete_button = Button(self, text="Create", command=self.createNewBoard)
        creaete_button.pack(fill=BOTH, side=BOTTOM)
        check_button = Button(self, text="Check", command=self.checkTheBoard)
        check_button.pack(fill=BOTH, side=BOTTOM)
        solve_button = Button(self, text="Solve", command=self.solveBoard)
        solve_button.pack(fill=BOTH, side=BOTTOM)
        load_button = Button(self, text="Load", command=self.loadABoard)
        load_button.pack(fill=BOTH, side=BOTTOM)

        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __draw_grid(self):
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                x = MARGIN + j * SIDE + SIDE / 2
                y = MARGIN + i * SIDE + SIDE / 2
                if self.board[i][j] != 0:
                    color = "black" if self.board[i][j] == self.originalBoard[i][j] else "blue"
                    self.canvas.create_text(x, y, text=self.board[i][j], tags="numbers", fill=color)

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )

    def __cell_clicked(self, event):
        if self.gameOver:
            return
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            # get row and col numbers from x,y coordinates
            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE

            # if cell was selected already - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.originalBoard[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__draw_cursor()

    def __key_pressed(self, event):
        if self.gameOver:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.board[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()

    def createNewBoard(self, refreshUI=True):
        generator = sudokuGenerator()
        generator.generatePuzzle()
        generator.removeCells(self.radioButtonValue.get()*10+20)
        self.board = copy.deepcopy(generator.board)
        self.originalBoard = copy.deepcopy(generator.board)
        if refreshUI:
            self.__draw_puzzle()
    
    def isAnswersValid(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                value = self.board[row][col]
                if value == 0:
                    return False
                for index, i in enumerate(self.board[row]):
                    if i == value and index != col:
                        return False
                for index, i in enumerate(self.board):
                    if i[col] == value and index != row:

                        return False
                
                for i in range((row//3)*3, ((row//3)*3)+3):
                    for j in range((col//3)*3, ((col//3)*3)+3):
                        if self.board[i][j] == value and i != row and j != col:
                            return False
                
        return True

    def checkTheBoard(self):
        if self.isAnswersValid():
            messagebox.showinfo(title="Result", message="VICTORY")
        else:
            messagebox.showinfo(title="Result", message="LOSER")

    def loadABoard(self):
        filePath=filedialog.askopenfilename(initialdir=os.getcwd(), title="Open Text File",filetypes=(("Text Files", "*.txt"),))
        if filePath:
            generator = sudokuGenerator()
            generator.readBoardFromFile(filePath)
            self.board = copy.deepcopy(generator.board)
            self.originalBoard = copy.deepcopy(generator.board)
            self.__draw_puzzle()

    def solveBoard(self):
        board = copy.deepcopy(self.originalBoard)
        solver = SudokuSolver(board)
        ok = solver.solve()
        if ok:
            self.board = copy.deepcopy(solver.board)
            self.__draw_puzzle()
        else:
            messagebox.showinfo(title="SUDOKU", message="This sudoku is unsolvable!!!")



MARGIN = 20
SIDE = 50
WIDTH = MARGIN * 2 + SIDE * 9
HEIGHT = MARGIN * 2 + SIDE * 9

root = Tk()
root.title("SUDOKU GAME")
root.geometry("%dx%d" % (WIDTH, HEIGHT + 150))
SudokuUI(root)

root.mainloop()
