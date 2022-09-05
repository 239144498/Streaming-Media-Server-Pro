# !/usr/bin python3
# -*- coding: utf-8 -*-
from app.settings import PATH


def return_diyepg():
    filename = PATH / "assets/diychannel.txt"
    if filename.is_file():
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    return ""


if __name__ == '__main__':
    a = return_diyepg()
    print(a)
