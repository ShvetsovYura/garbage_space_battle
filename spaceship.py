import itertools
import logging

import curses_tools
from star import AnimatedObject
from utils import read_spaceship_frames, mysleep

_LOGGER = logging.getLogger(__name__)


class Spaceship(AnimatedObject):
    def __init__(self, canvas, row, column):
        self.canvas = canvas
        self.frames = itertools.cycle(read_spaceship_frames())
        self.row = row
        self.column = column
        self.cur_frame = None
        self.prev_frame = None
        self.max_row, self.max_col = canvas.getmaxyx()
        _LOGGER.debug(f'max_rows:{self.max_row}, max_col:{self.max_col}')

    async def move(self, row, column):
        # очистка предыдущего фрейма
        curses_tools.draw_frame(self.canvas, self.row, self.column, self.prev_frame or self.cur_frame, negative=True)

        # применение новых координат
        _new_column = self.column + column * 5
        _new_row = self.row + row * 5
        _frame_rows, _frame_columns = curses_tools.get_frame_size(self.cur_frame)

        if _new_row < 1:
            _new_row = 1

        if _new_column < 1:
            _new_column = 1

        if _new_column + _frame_columns > self.max_col - 1:
            _new_column = self.max_col - _frame_columns - 1

        if _new_row + _frame_rows + 1 > self.max_row:
            _new_row = self.max_row - _frame_rows - 1

        self.column = _new_column
        self.row = _new_row

        # отображение нового фрейма
        curses_tools.draw_frame(self.canvas, self.row, self.column, self.cur_frame)

        # отображенный фрейм становится предыдущим
        self.prev_frame = self.cur_frame

        # отдача управления внешней (вызвающей) функции
        await mysleep(0)

    async def animate(self):
        for frame in self.frames:
            self.cur_frame = frame
            await mysleep(0)
