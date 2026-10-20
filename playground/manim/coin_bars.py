"""동전 n개 던지기: 앞면의 수 X의 확률분포(이항분포)를 막대로 그린다.

실행: python -m manim -pql coin_bars.py CoinBars
"""
from math import comb

from manim import (
    BLUE, DOWN, RIGHT, UP, WHITE, Create, FadeIn, GrowFromEdge, LaggedStart, Line,
    Rectangle, Scene, Text, VGroup,
)

N = 4  # 동전 개수: 바꿔서 실행해 보기


class CoinBars(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        probs = [comb(N, k) / 2**N for k in range(N + 1)]
        unit = 5.0 / max(probs)  # 가장 높은 막대를 5로 맞춤

        bars = VGroup(*[
            Rectangle(width=1.0, height=p * unit, fill_opacity=1, color=BLUE, stroke_width=0)
            for p in probs
        ])
        bars.arrange(RIGHT, buff=0.35, aligned_edge=DOWN).move_to([0, -0.5, 0])

        base = Line(bars.get_corner(DOWN + RIGHT) + RIGHT * 0.4, bars.get_corner(DOWN + RIGHT * -1) + RIGHT * -0.4,
                    color="#6B7A90")
        xs = VGroup(*[Text(f"X={k}", font_size=26, color="#1B2A41").next_to(b, DOWN, buff=0.25)
                      for k, b in enumerate(bars)])
        ps = VGroup(*[Text(f"{p:.3f}", font_size=26, color="#0B2E5C").next_to(b, UP, buff=0.15)
                      for p, b in zip(probs, bars)])

        self.play(Create(base), FadeIn(xs))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.25))
        self.play(FadeIn(ps))
        self.wait(1)
