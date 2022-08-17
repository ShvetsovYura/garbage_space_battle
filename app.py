import curses
import itertools
import logging.config
import logging
import time

import curses_tools
from spaceship import Spaceship
from star import Star

TIC_TIMEOUT = 0.1


async def handle_input(canvas, _ship: Spaceship):
    while True:
        rows_direction, columns_direction, space_pressed = curses_tools.read_controls(canvas)
        await _ship.move(rows_direction, columns_direction)


def draw(canvas):
    rows, columns = canvas.getmaxyx()
    curses.curs_set(False)
    canvas.nodelay(True)

    stars_coros = [Star(canvas, rows, columns).animate() for _ in range(100)]

    ship = Spaceship(canvas, rows // 2, columns // 2)
    ship_coros = [ship.animate()]
    handlers_coros = [handle_input(canvas, ship)]
    coros = list(itertools.chain(stars_coros, ship_coros, handlers_coros))

    while True:
        for coro in coros.copy():
            try:
                coro.send(None)
            except StopIteration:
                coros.remove(coro)
        canvas.border()
        canvas.refresh()
        time.sleep(TIC_TIMEOUT * 2)


if __name__ == '__main__':
    logging.basicConfig(filename='log.log', level=logging.DEBUG)
    curses.update_lines_cols()
    curses.wrapper(draw)
