"""DrawPi entry point

This file is part of the DrawPi project, Copyright © 2023 JonLiuFYI
SPDX-License-Identifier: Apache-2.0
"""
from dataclasses import dataclass
import logging
from statistics import fmean

import pyxel as px

import calc
from point import Point


@dataclass
class Results:
    circ: float
    dia: float
    pi: float


class DrawPi:
    drawing = False
    show_results = False
    result = Results(0, 0, 0)
    pi_msg = ""
    prev_point: Point | None = None
    points: list[Point] = []
    pi_attempts: list[float] = []

    def __init__(self) -> None:
        logging.basicConfig(level=logging.DEBUG)

        px.init(256, 256, title="Draw Pi!", fps=120, capture_scale=3)
        px.run(self.update, self.draw)

    def update(self):

        # when press starts
        if px.btnp(px.MOUSE_BUTTON_LEFT):
            px.cls(0)
            self.points = []
            self.drawing = True
            self.prev_point = None
            logging.debug("Drawing now!")

        # while keeping pressed
        if px.btn(px.MOUSE_BUTTON_LEFT):
            self.points.append(Point(px.mouse_x, px.mouse_y))
            logging.debug(f"{Point(px.mouse_x, px.mouse_y)} - [len {len(self.points)}]")

        # when released
        if px.btnr(px.MOUSE_BUTTON_LEFT):
            self.drawing = False

            px.mouse(True)
            self.show_results = True
            self.result.circ = calc.circumference(self.points)
            self.result.dia = calc.diameter(self.points)
            try:
                self.result.pi = self.result.circ / self.result.dia
                self.pi_attempts.append(self.result.pi)
            except ZeroDivisionError:
                self.pi_msg = "Draw a circle first, silly"
            else:
                self.pi_msg = f"Latest attempt at pi: {self.result.pi}"

            logging.debug("Drawing stopped")

    def draw(self):
        px.mouse(True)

        if self.drawing:
            px.mouse(False)
            if self.prev_point is not None:
                px.line(px.mouse_x, px.mouse_y, *self.prev_point, 9)
            self.prev_point = Point(px.mouse_x, px.mouse_y)
        else:
            px.cls(0)
            instructions = (
                "       Find pi with your mouse!\n"
                "     Draw the best circle you can.\n"
                "Draw more to improve the approximation."
            )
            tip = (
                "  (Tip: for best results, release the\n"
                "  mouse button as close to your start\n"
                "           point as you can)"
            )
            px.text(50, 208, instructions, 9)
            px.text(50, 234, tip, 15)

            self.draw_last_drawing()

            if self.show_results:
                px.text(5, 5, f"Circumference: {self.result.circ}\nDiameter: {self.result.dia}", 9)  # fmt: skip
                px.text(5, 20, self.pi_msg, 15)
                if len(self.pi_attempts) > 0:
                    px.text(5, 35, f"Pi: {fmean(self.pi_attempts)}", 7)

    def draw_last_drawing(self):
        pts = self.points
        for i, this_point in enumerate(pts):
            if i == 0:
                continue
            prev_point = pts[i - 1]
            px.line(*this_point, *prev_point, 9)


DrawPi()
