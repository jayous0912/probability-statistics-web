"""정규분포 밀도곡선: 구간 [A, B] 아래 넓이 = 확률.

실행: python -m manim -pql normal_area.py NormalArea
"""
from math import erf, sqrt

import numpy as np
from manim import (
    DOWN, UP, WHITE, Axes, Create, Scene, Text, ValueTracker, always_redraw,
)

MU, SIGMA = 0.0, 1.0
A, B = -1.0, 1.0


def cdf(x):
    return 0.5 * (1 + erf((x - MU) / (SIGMA * sqrt(2))))


class NormalArea(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        ax = Axes(x_range=[-4, 4, 1], y_range=[0, 0.5, 0.1], x_length=11, y_length=4.5,
                  axis_config={"color": "#6B7A90", "include_ticks": False, "include_tip": False}
                  ).shift(DOWN * 0.4)
        pdf = lambda x: np.exp(-((x - MU) ** 2) / (2 * SIGMA**2)) / (SIGMA * np.sqrt(2 * np.pi))
        curve = ax.plot(pdf, x_range=[-4, 4], color="#0B2E5C", stroke_width=6)

        self.play(Create(ax.x_axis), Create(curve), run_time=1.5)

        right = ValueTracker(A + 0.001)
        area = always_redraw(lambda: ax.get_area(curve, x_range=(A, right.get_value()),
                                                 color="#4FA3F7", opacity=0.8))
        label = always_redraw(lambda: Text(
            f"P({A:g} ≤ X ≤ {right.get_value():.1f}) = {cdf(right.get_value()) - cdf(A):.3f}",
            font_size=34, color="#0B2E5C").to_edge(UP))
        self.add(area, label)
        self.play(right.animate.set_value(B), run_time=3)
        self.wait(1)
