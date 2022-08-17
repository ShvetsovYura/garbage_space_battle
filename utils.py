import asyncio
import os
from pathlib import Path

TIC_TIMEOUT = 0.1


def read_spaceship_frames():
    rocket_dir = Path(__file__).resolve().parent / 'animations/spacesheep'
    frames = []
    with open(os.path.join(rocket_dir, 'frame_1.txt'), 'r') as f:
        frames.append(f.read())

    with open(os.path.join(rocket_dir, 'frame_2.txt'), 'r') as f:
        frames.append(f.read())

    return frames


async def mysleep(seconds):
    if not seconds:
        await asyncio.sleep(0)
    for _ in range(int(seconds // TIC_TIMEOUT)):
        await asyncio.sleep(0)
