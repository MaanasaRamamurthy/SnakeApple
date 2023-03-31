import random
import pygame
import time
from pygame.locals import *

SIZE = 40


class Snake:
    # snake is represented as a list of blocks. the size of each block is 40
    def __init__(self, surface):
        self.surface = surface
        # initial length of snake
        self.length = 3
        # the snake image is loaded
        self.block = pygame.image.load("./resources/block.jpg").convert()
        self.position_x = [SIZE] * self.length  # it gives an array of length=self.length and value=40 i.e,[40,40,40]
        self.position_y = [SIZE] * self.length  # same as above. position_y=[40,40,40] initially

    def draw(self):
        # the snake body which is a block is drawn on the screen at the position (120,120) initially
        # the snake will be drawn at a new position everytime with the change in x and y value
        for i in range(self.length):
            self.surface.blit(self.block, (self.position_x[i], self.position_y[i]))

    def increase_length(self):
        # this function is called whenever the snake eats an apple
        # when this happens, the length of the snake is increased by 1
        self.length += 1
        # for this append function, any value can be appended into the x and y list. Eg. -1,0,1 etc
        # but for the move() to work properly, we are appending the below value
        # this will append the position of x and y of the new block
        self.position_x.append((self.position_x[self.length-2]) + SIZE)
        self.position_y.append((self.position_y[self.length-2]) + SIZE)

    def crawl(self, direction):
        # snake is represented as a list of x and y points.
        # so when the snake move in one direction, its head value i.e.,
        # x[0] and y[0] is increased with a size of the block i.e., 40
        # the rest of the values in the list is moved one step backward
        # this will give the illusion as if the snake moving forward
        for i in range(self.length - 1, 0, -1):
            self.position_x[i] = self.position_x[i - 1]
            self.position_y[i] = self.position_y[i - 1]
        if direction == "right":
            self.position_x[0] += 40
        elif direction == "down":
            self.position_y[0] += 40
        elif direction == "left":
            self.position_x[0] -= 40
        elif direction == "up":
            self.position_y[0] -= 40

        # once the list is updated, the snake is drawn on the game window. This process takes place so quickly
        # that the movement looks smooth on the screen
        self.draw()


class Apple:
    # apple is represented as an image. The 4 corners of the image are taken for positioning the apple on the screen.
    def __init__(self, surface):
        self.apple = pygame.image.load("./resources/apple.jpg").convert()
        # the apple is rendered at (120,120) initially
        self.apple_pos_x = 120
        self.apple_pos_y = 120
        self.surface = surface

    def draw(self):
        # the apple is drawn on the surface of the screen at position (120,120) initially
        self.surface.blit(self.apple, (self.apple_pos_x, self.apple_pos_y))

    def move(self, position_x, position_y):
        # this function is called when the snake eats an apple. random function is used to position the new apple
        # at some random position on the screen
        self.apple_pos_x = random.randint(1, 23) * SIZE
        self.apple_pos_y = random.randint(1, 16) * SIZE
        # this is done to make sure that the apple is not rendered on top of snake.
        # the apple image may overlap with the snake list if (x,y) of apple is equal to
        # any block(x,y) of snake list
        for i in position_x:
            for j in position_y:
                if self.apple_pos_x == i and self.apple_pos_y == j:
                    self.move(position_x, position_y)


class Game:
    def __init__(self):
        pygame.init()
        # the game window is initialized with the given dimensions
        self.surface = pygame.display.set_mode([1000, 720])
        self.render_bg()
        # initially the snake is made to move in right direction( not compulsory)
        self.direction = "right"
        # this is done to make sure that when the snake is moving in right or left direction, only possible moves should
        # be up or down(i,e., 90deg turn) and vice versa. this eliminates the possibility of 180deg turn.
        self.key = "rl"     # initially this is set to "rl" coz direction is set to "right" initially
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.score = 0
        self.game_over = False

    def collision(self, x1, y1, x2, y2):
        # this function can be used to detect collision of the snake's head with the apple or with itself
        # this depends on the value that is passed in x2 and y2 arguments,
        # if x2 and y2 contains the value of the x and y position of the apple, it detects if the snake eats the apple
        # or if x2 and y2 contains the value of x[i] and y[i]  of the snake body, it detects if the snake hits itself.
        if x2 <= x1 < x2 + SIZE - 1:
            if y2 <= y1 < y2 + SIZE - 1:
                return True
        return False

    def render_bg(self):
        bg = pygame.image.load("./resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def display_game_over(self):
        self.surface.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 20)
        line1 = font.render(f"GAME OVER! YOUR SCORE: {self.score}", True, (228, 191, 191))
        self.surface.blit(line1, (200, 200))
        pygame.display.flip()

    def display_score(self):
        # this function is used to display the score on top right corner of the screen
        font = pygame.font.SysFont('arial', 20)
        final_score = font.render(f"Score: {self.score}", True, (228, 191, 191))
        self.surface.blit(final_score, (900, 10))

    def play_step(self):
        # render background of pygame
        self.render_bg()

        # get input from user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                # when the snake is moving in left or right direction, only up and down keys work. i.e.,
                # the snake cannot take 180deg turn
                if self.key == "rl":
                    if event.key == K_UP:
                        self.direction = "up"
                        self.key = "ud"

                    elif event.key == K_DOWN:
                        self.direction = "down"
                        self.key = "ud"
                # when the snake is moving in up or down direction, only right and left keys work. i.e.,
                # the snake cannot take 180deg turn
                if self.key == "ud":
                    if event.key == K_RIGHT:
                        self.direction = "right"
                        self.key = "rl"

                    elif event.key == K_LEFT:
                        self.direction = "left"
                        self.key = "rl"

        # move the snake
        self.snake.crawl(self.direction)

        # collision detection
        # hits boundary
        if self.snake.position_x[0] > 1000 - SIZE or self.snake.position_x[0] < 0 or \
                self.snake.position_y[0] > 720 - SIZE or self.snake.position_y[0] < 0:
            self.game_over = True
            return self.score, self.game_over

        # hits itself
        for i in range(3, self.snake.length):
            if self.collision(self.snake.position_x[0], self.snake.position_y[0],
                              self.snake.position_x[i], self.snake.position_y[i]):
                self.game_over = True
                return self.score, self.game_over

        # eat food
        if self.collision(self.snake.position_x[0], self.snake.position_y[0],
                          self.apple.apple_pos_x, self.apple.apple_pos_y):
            self.snake.increase_length()
            self.score += 1
            self.apple.move(self.snake.position_x, self.snake.position_y)

        # update ui
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        return self.score, self.game_over


if __name__ == "__main__":
    game = Game()
    while True:
        score, over = game.play_step()
        if over:
            game.display_game_over()
        time.sleep(0.1)



