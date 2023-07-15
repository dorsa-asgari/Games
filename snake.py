from tkinter import *
import random


class Snake:
    def __init__(self, canvas: Canvas, color, pixelSize=20, initialLenght=2):
        self.canvas = canvas
        self.color = color
        self.pixelSize = pixelSize
        self.coordinates = []
        self.squares = []
        self.direction = "right"

        for i in range(0, initialLenght):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = self.canvas.create_rectangle(x, y, x + pixelSize, y + pixelSize, fill=self.color, tag="snake")
            self.squares.append(square)

    def move_snake_forward(self):
        # handling the movement of the snake based on its current direction

        x, y = self.coordinates[0]

        if self.direction == "up":
            y -= self.pixelSize
        elif self.direction == "down":
            y += self.pixelSize
        elif self.direction == "left":
            x -= self.pixelSize
        elif self.direction == "right":
            x += self.pixelSize

        self.coordinates.insert(0, (x, y))
        square = self.canvas.create_rectangle(x, y, x + self.pixelSize, y + self.pixelSize, fill=self.color,tag="snake")
        self.squares.insert(0, square)

    def changeDirection(self, newDirection):
        # validating the snake's direction change

        if newDirection == 'left':
            if self.direction != 'right':
                self.direction = newDirection
        elif newDirection == 'right':
            if self.direction != 'left':
                self.direction = newDirection
        elif newDirection == 'up':
            if self.direction != 'down':
                self.direction = newDirection
        elif newDirection == 'down':
            if self.direction != 'up':
                self.direction = newDirection

    def deleteLastSnakeTile(self):
        self.canvas.delete(self.squares[-1])
        del self.coordinates[-1]
        del self.squares[-1]


class Food:
    def __init__(self, canvas: Canvas, pixelSize=20):
        self.canvas = canvas
        self.pixelSize = pixelSize
        self.draw_food_on_canvas()

    def draw_food_on_canvas(self):
        # delete the previous food and draw a new one in a random place

        self.canvas.delete("food")
        self.coordinates = [random.randint(0, (400 / self.pixelSize) - 1) * self.pixelSize,
                            random.randint(0, (400 / self.pixelSize) - 1) * self.pixelSize]

        self.canvas.create_rectangle(self.coordinates[0],
                                     self.coordinates[1],
                                     self.coordinates[0] + self.pixelSize,
                                     self.coordinates[1] + self.pixelSize,
                                     fill="#555555",
                                     tag="food")


class Game():
    def __init__(self, screen: Tk):
        self.screen = screen
        self.score = 0
        self.createGUI()

        # create snake and food
        self.snake = Snake(self.canvas, color="#ff5511")
        self.food = Food(self.canvas)

        # bind the keys to functions
        self.screen.bind('<Left>', lambda event: self.snake.changeDirection('left'))
        self.screen.bind('<Right>', lambda event: self.snake.changeDirection('right'))
        self.screen.bind('<Up>', lambda event: self.snake.changeDirection('up'))
        self.screen.bind('<Down>', lambda event: self.snake.changeDirection('down'))

    def createGUI(self):
        # create the main canvas and the score label

        self.canvas = Canvas(self.screen, bg="#ffffff", height=400, width=400, highlightthickness=0)
        self.scoreLabel = Label(self.screen, text=f"Score: {self.score}")
        self.scoreLabel.pack()
        self.canvas.pack()

    def checkCollosion(self):
        # check if the snake collide with the walls of the border or itself

        if self.snake.coordinates[0][0] < 0 or self.snake.coordinates[0][0] > 400:
            return True
        if self.snake.coordinates[0][1] < 0 or self.snake.coordinates[0][1] > 400:
            return True

        for cord in self.snake.coordinates[1:]:
            if cord[0] == self.snake.coordinates[0][0] and cord[1] == self.snake.coordinates[0][1]:
                return True
        return False

    def checkFoodCollision(self):
        # check if the snake hit the food

        if self.snake.coordinates[0][0] == self.food.coordinates[0] and self.snake.coordinates[0][1] == \
                self.food.coordinates[1]:
            return True
        return False

    def move(self):
        # updating the score label after hitting the food,updating the snake's positions every 300 milliseconds,
        # manage the game over condition

        self.snake.move_snake_forward()
        if self.checkFoodCollision():
            self.score += 1
            self.scoreLabel.config(text=f"Score: {self.score}")
            self.food.draw_food_on_canvas()
        else:
            self.snake.deleteLastSnakeTile()

        if self.checkCollosion():
            self.canvas.delete(ALL)
            self.canvas.create_text(self.canvas.winfo_width() / 2,
                                    self.canvas.winfo_height() / 2,
                                    font=('consolas', 50),
                                    text="GAME OVER", fill="red",
                                    tag="gameover")
        else:
            self.screen.after(300, self.move)


window = Tk()
window.title("Snake game")

game = Game(window)
game.move()

window.mainloop()



