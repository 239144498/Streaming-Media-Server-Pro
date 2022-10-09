# -*- coding: utf-8 -*-
# @Time    : 2022/10/9
# @Author  : Naihe
# @Email   : 239144498@qq.com
# @File    : basic.py
# @Software: PyCharm
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class CodeEnum(int, Enum):
    """业务状态码"""
    SUCCESS = 200
    FAIL = 404


class ResponseBasic(BaseModel):
    code: CodeEnum = Field(default=CodeEnum.SUCCESS, description="业务状态码 200 是成功, 404 是失败")
    data: Any = Field(default=None, description="数据结果")
    msg: str = Field(default="请求成功", description="提示")


class Response200(ResponseBasic):
    pass


class Response404(ResponseBasic):
    code: CodeEnum = CodeEnum.FAIL
    msg: str = "请求失败"
