"""갈톤 보드: 공이 핀을 지나 칸에 쌓이며 종 모양 분포를 만든다.

실행: python -m manim -pql galton.py GaltonBoard
"""
import random
from math import comb

from manim import (
    BLUE, DOWN, LEFT, RIGHT, UP, WHITE, Dot, FadeIn, Rectangle, Scene, Succession, VGroup,
)

ROWS = 7
DX, DY = 0.7, 0.5
BALLS = 24


class GaltonBoard(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        random.seed(3)
        top = 3.4

        def pin_pos(r, j):
            return RIGHT * (j - r / 2) * DX + UP * (top - r * DY)

        pins = VGroup(*[Dot(pin_pos(r, j), radius=0.05, color="#6B7A90")
                        for r in range(ROWS) for j in range(r + 1)])
        self.add(pins)

        floor = -3.4  # 칸의 바닥: 쌓인 공이 핀과 겹치지 않도록 아래에 둔다
        counts = [0] * (ROWS + 1)
        bars = [None] * (ROWS + 1)

        for _ in range(BALLS):
            k = 0
            path = [UP * (top + 0.5)]
            for r in range(ROWS):
                path.append(pin_pos(r, k))
                k += random.randint(0, 1)
            x_bin = RIGHT * (k - ROWS / 2) * DX
            counts[k] += 1
            path.append(x_bin + UP * (floor + counts[k] * 0.18))

            ball = Dot(path[0], radius=0.09, color=BLUE)
            self.add(ball)
            self.play(Succession(*[ball.animate(run_time=0.07, rate_func=lambda t: t).move_to(p)
                                   for p in path[1:]]), run_time=0.07 * (len(path) - 1))

        self.wait(1)
        theory = [comb(ROWS, k) / 2**ROWS * BALLS for k in range(ROWS + 1)]
        self.play(FadeIn(VGroup(*[
            Rectangle(width=DX * 0.9, height=0.02 + t * 0.18, color="#0B2E5C", stroke_width=3, fill_opacity=0)
            .move_to(RIGHT * (k - ROWS / 2) * DX + UP * (floor + (0.02 + t * 0.18) / 2))
            for k, t in enumerate(theory)
        ])))
        self.wait(1)
