'''
Simple snake game using pygame.

'''
import pygame
import random

#              R    G    B
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
RED        = (255,   0,   0)
GREEN      = (  0, 210,   0)
DARK_GREEN = (  0, 155,   0)
DARK_GRAY  = ( 40,  40,  40)
PINK       = (   0,   0,  0)

BG_COLOR = PINK
HEAD_COLOR = GREEN
SNAKE_COLOR = DARK_GREEN

FONT_SIZE = 36

# (dx, dy)
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

key_mapping = { pygame.K_LEFT : LEFT, pygame.K_a : LEFT, 
                pygame.K_RIGHT : RIGHT, pygame.K_d : RIGHT,
                pygame.K_UP : UP, pygame.K_w : UP,
                pygame.K_DOWN : DOWN, pygame.K_s : DOWN }


class Snake():
    """Simple snake game.


    title - game title
    width - window width
    height - window height
    cell_size - size of one tile
        height and width need to be multiples of cell_size
    game_speed - must be >1
    """
    def __init__(self, title="Snake", width=640, height=480, cell_size=20, game_speed=8):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        if height % cell_size != 0 or width % cell_size != 0:
            raise ValueError("height and width need to be multiples of cell_size")
        self.game_speed = game_speed
        if game_speed < 1:
            raise ValueError("game_speed must be bigger than 0")
        pygame.init()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.display.fill(BG_COLOR)

    def loop_games(self):
        """Start new game and keep restarting until player quits."""
        while True:
            self.run_game()


    def run_game(self):
        """Run one game."""
        row_count = self.height/self.cell_size
        col_count = self.width/self.cell_size
        x, y = self.get_starting_point()
        snake = [(x, y), (x - 1, y), (x - 2, y)]
        dx, dy = RIGHT
        apple_x, apple_y = self.generate_apple()
        while True:
            current_dx, current_dy = dx, dy
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_mapping:
                        new_dx, new_dy = key_mapping[event.key]
                        # So you can't go from right to left and eat yourself.
                        # You can't check against new_dx/new_dy because it
                        # could be changed multiple times (eg. going right
                        # and pressing up and left quickly).
                        if new_dx != -current_dx and new_dy != -current_dy:
                            dx, dy = new_dx, new_dy


            # move head
            x += dx;
            y += dy
            snake.insert(0, (x, y))
            if x == apple_x and y == apple_y:
                apple_x, apple_y = self.generate_apple()
            else:
                # remove last part of snake
                snake.pop()


            self.display.fill(BG_COLOR)

            # apple
            apple_rect = pygame.Rect(apple_x * self.cell_size, 
                                    apple_y * self.cell_size, 
                                    self.cell_size, self.cell_size)
            pygame.draw.rect(self.display, RED, apple_rect)
            # body
            game_over = False
            for snake_x, snake_y in snake[1:]:
                body_rect = pygame.Rect(snake_x * self.cell_size, snake_y * self.cell_size, 
                                        self.cell_size, self.cell_size)
                pygame.draw.rect(self.display, SNAKE_COLOR, body_rect)
                # border
                pygame.draw.rect(self.display, DARK_GRAY, body_rect, 1)
                if x == snake_x and y == snake_y:
                    game_over = True
            # head
            head_rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                    self.cell_size, self.cell_size)
            pygame.draw.rect(self.display, HEAD_COLOR, head_rect)

            pygame.display.flip()
            self.clock.tick(self.game_speed)

            if x < 0 or x >= col_count \
                or y < 0 or y >= row_count \
                or game_over:
                self.show_game_over()
                return

    def show_game_over(self):
        """Show "game over" text."""
        text = self.font.render("Game Over", True, WHITE)
        text_rect = text.get_rect()
        text_x = self.width / 2 - text_rect.width / 2
        text_y = self.height / 2 - text_rect.height / 2
        self.display.blit(text, (text_x, text_y))
        pygame.display.flip()
        pygame.time.wait(300)

    def generate_apple(self):
        """Generate new apple coordinates (x, y)."""
        return (random.randrange(0, self.width / self.cell_size), 
                random.randrange(0, self.height / self.cell_size))

    def get_starting_point(self):
        """Return starting location of snake's head (x, y)."""
        return (random.randrange(5, (self.width / self.cell_size) - 5), 
                random.randrange(5, (self.height / self.cell_size) - 5))

if __name__ == '__main__':
    snake = Snake()
    snake.loop_games()
python 