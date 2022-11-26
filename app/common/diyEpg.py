# !/usr/bin python3
# -*- coding: utf-8 -*-
from app.conf import config


def return_diyepg():
    filename = config.ROOT / "assets/diyepg.txt"
    if filename.is_file():
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    return ""

