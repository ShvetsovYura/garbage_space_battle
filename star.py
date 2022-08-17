import curses
import random
from abc import ABC

from utils import mysleep

TIC_TIMEOUT = 0.1


class AnimatedObject(ABC):
    async def animate(self):
        pass


STAR_TYPES = ['*', '+', '.', ':', '\'']


class Star(AnimatedObject):
    def __init__(self, canvas, max_rows, max_columns):
        self.row = random.randint(1, max_rows - 2)
        self.column = random.randint(1, max_columns - 2)
        self.symbol = random.choice(STAR_TYPES)
        self.canvas = canvas

    async def animate(self):
        canvas = self.canvas
        while True:
            canvas.addstr(self.row, self.column, self.symbol, curses.A_DIM)
            await mysleep(2)

            canvas.addstr(self.row, self.column, self.symbol)
            await mysleep(0.3)

            canvas.addstr(self.row, self.column, self.symbol, curses.A_BOLD)
            await mysleep(0.5)

            canvas.addstr(self.row, self.column, self.symbol)
            await mysleep(0.3)

            await mysleep(random.randint(0, 5))
