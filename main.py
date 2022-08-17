import asyncio
import curses
import random
import time

TIC_TIMEOUT = 0.1
STAR_TYPES = ['*', '+', '.', ':', '\'']


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(int(2 // TIC_TIMEOUT)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(int(0.3 // TIC_TIMEOUT)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(int(0.5 // TIC_TIMEOUT)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(int(0.3 // TIC_TIMEOUT)):
            await asyncio.sleep(0)

        for _ in range(int(random.randint(0, 10) // TIC_TIMEOUT)):
            await asyncio.sleep(0)


def get_random_star(rows, columns):
    row = random.randint(1, rows - 2)
    column = random.randint(1, columns - 2)

    figure = random.choice(STAR_TYPES)
    return row, column, figure


def draw(canvas):
    rows, columns = canvas.getmaxyx()
    curses.curs_set(False)
    canvas.nodelay(True)
    coros = [blink(canvas, *get_random_star(rows, columns)) for _ in range(100)]
    while True:
        for coro in coros.copy():
            try:
                coro.send(None)
            except StopIteration:
                coros.remove(coro)
        canvas.border()
        canvas.refresh()
        time.sleep(TIC_TIMEOUT * 2)
