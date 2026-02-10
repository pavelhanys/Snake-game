"""Simple Snake game implemented with Python's built-in turtle module."""

from __future__ import annotations

import random
import time
import turtle

WINDOW_SIZE = 600
GRID_SIZE = 20
START_DELAY = 0.12
SPEED_UP_FACTOR = 0.97
MIN_DELAY = 0.05


class SnakeGame:
    def __init__(self) -> None:
        self.screen = turtle.Screen()
        self.screen.title("Snake Game")
        self.screen.bgcolor("black")
        self.screen.setup(width=WINDOW_SIZE, height=WINDOW_SIZE)
        self.screen.tracer(0)

        self.head = turtle.Turtle("square")
        self.head.color("lime")
        self.head.penup()
        self.head.goto(0, 0)
        self.direction = "stop"

        self.food = turtle.Turtle("circle")
        self.food.color("red")
        self.food.penup()
        self.food.speed(0)
        self.move_food()

        self.segments: list[turtle.Turtle] = []
        self.score = 0
        self.high_score = 0
        self.delay = START_DELAY

        self.hud = turtle.Turtle()
        self.hud.hideturtle()
        self.hud.color("white")
        self.hud.penup()
        self.hud.goto(0, WINDOW_SIZE // 2 - 40)
        self.update_hud()

        self.bind_keys()

    def bind_keys(self) -> None:
        self.screen.listen()
        self.screen.onkey(lambda: self.change_direction("up"), "Up")
        self.screen.onkey(lambda: self.change_direction("down"), "Down")
        self.screen.onkey(lambda: self.change_direction("left"), "Left")
        self.screen.onkey(lambda: self.change_direction("right"), "Right")
        self.screen.onkey(self.restart, "r")

    def change_direction(self, new_direction: str) -> None:
        opposite = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left",
        }
        if self.direction != opposite.get(new_direction):
            self.direction = new_direction

    def move_head(self) -> None:
        x, y = self.head.xcor(), self.head.ycor()
        if self.direction == "up":
            self.head.sety(y + GRID_SIZE)
        elif self.direction == "down":
            self.head.sety(y - GRID_SIZE)
        elif self.direction == "left":
            self.head.setx(x - GRID_SIZE)
        elif self.direction == "right":
            self.head.setx(x + GRID_SIZE)

    def hit_wall(self) -> bool:
        half = WINDOW_SIZE // 2 - GRID_SIZE
        return abs(self.head.xcor()) > half or abs(self.head.ycor()) > half

    def hit_self(self) -> bool:
        return any(segment.distance(self.head) < GRID_SIZE / 2 for segment in self.segments)

    def move_food(self) -> None:
        half = WINDOW_SIZE // 2 - GRID_SIZE
        x = random.randrange(-half, half + GRID_SIZE, GRID_SIZE)
        y = random.randrange(-half, half + GRID_SIZE, GRID_SIZE)
        self.food.goto(x, y)

    def add_segment(self) -> None:
        segment = turtle.Turtle("square")
        segment.color("green")
        segment.penup()
        self.segments.append(segment)

    def grow_if_needed(self) -> None:
        if self.head.distance(self.food) < GRID_SIZE:
            self.move_food()
            self.add_segment()
            self.score += 10
            self.high_score = max(self.high_score, self.score)
            self.delay = max(MIN_DELAY, self.delay * SPEED_UP_FACTOR)
            self.update_hud()

    def move_segments(self) -> None:
        for idx in range(len(self.segments) - 1, 0, -1):
            x = self.segments[idx - 1].xcor()
            y = self.segments[idx - 1].ycor()
            self.segments[idx].goto(x, y)

        if self.segments:
            self.segments[0].goto(self.head.xcor(), self.head.ycor())

    def update_hud(self) -> None:
        self.hud.clear()
        self.hud.write(
            f"Score: {self.score}  High Score: {self.high_score}  (R to restart)",
            align="center",
            font=("Courier", 16, "normal"),
        )

    def reset(self) -> None:
        time.sleep(0.4)
        self.head.goto(0, 0)
        self.direction = "stop"

        for segment in self.segments:
            segment.goto(1000, 1000)
        self.segments.clear()

        self.score = 0
        self.delay = START_DELAY
        self.update_hud()
        self.move_food()

    def restart(self) -> None:
        self.reset()

    def run(self) -> None:
        while True:
            self.screen.update()

            if self.hit_wall() or self.hit_self():
                self.reset()

            self.move_segments()
            self.move_head()
            self.grow_if_needed()

            time.sleep(self.delay)


def main() -> None:
    game = SnakeGame()
    game.run()


if __name__ == "__main__":
    main()
