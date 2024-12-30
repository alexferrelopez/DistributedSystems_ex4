import os

from tkinter import *


def get_last_id(f):
    try:  # catch OSError in case of a one line file
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
    except OSError:
        f.seek(0)
    last_line = f.readline().decode().split("-")[0]
    if last_line:
        num = int(last_line)
    else:
        num = -1

    return num


def _get_lines(self, fp, _from):
    return [x.strip().split("-", 1)[1] for i, x in enumerate(fp) if i >= _from]




if __name__ == '__main__':
    pass