from numpy import size
from Canvas import Canvas
from PIL import Image, ImageDraw
from Utils.Constants import Position
from datetime import datetime


class Line(Canvas):
    def __init__(self, xy=(0, 0), points=(1, 1), color=(255, 255, 255, 255), blur=0, width=40, margin=(0, 0, 0, 0), position=(Position.CENTER, Position.CENTER), origin=(Position.CENTER, Position.CENTER), render=1, auto_update=True):
        self._width = width
        self._points = ((0, 0), (points))
        size = (abs(points[0]), abs(points[1]))
        super().__init__(xy, size, color, blur, margin,
                         (0, 0, 0, 0), position, origin, render, auto_update)

    def _draw_im(self, image, render=None):
        if render is None:render = self._render

        im = image.copy()

        # находим большие значения 
        # модуль всех значений умножаем на render
        zip(*self._points)
        start = tuple((map(lambda p: abs(p) * render, list(map(max, zip(*self._points))))))
        end = tuple((map(lambda p: abs(p) * render, list(map(min, zip(*self._points))))))

        ImageDraw.Draw(im).line((start, end), width=self._width * render, fill=self._color)
        
        return im
