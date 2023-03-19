"""Common pi calculation functions

This file is part of the DrawPi project, Copyright © 2023 JonLiuFYI
SPDX-License-Identifier: Apache-2.0
"""
from math import sqrt

from point import Point


def diameter(pts: list[Point]) -> float:
    """Find the "diameter" of the circle drawing (mean of width and height)"""
    s = sorted(pts)  # sorted by key x implicitly (thanks NamedTuple)

    max_x = s[-1].x
    min_x = s[0].x
    width = max_x - min_x

    s = sorted(pts, key=lambda p: p.y)
    max_y = s[-1].y
    min_y = s[0].y
    height = max_y - min_y

    return (width + height) / 2


def circumference(pts: list[Point]) -> float:
    """Find the "circumference" of the circle drawing (aka perimeter)"""
    out = 0
    for i, this_p in enumerate(pts):
        prev_p = pts[i - 1]
        out += sqrt(
            (this_p.x - prev_p.x) * (this_p.x - prev_p.x)
            + (this_p.y - prev_p.y) * (this_p.y - prev_p.y)
        )
    return out
