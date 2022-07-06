from Canvas import Canvas
from PIL import Image, ImageDraw
from Utils.Constants import Position
from datetime import datetime


class Window(Canvas):
    def __init__(self, xy = (0, 0), size = (1, 1), color = (255, 255, 255, 255), radius: tuple[(int, int, int, int)] = (0, 0, 0, 0), blur = 0, margin = (0, 0, 0, 0), padding = (0, 0, 0, 0), position = (Position.CENTER, Position.CENTER) , origin = (Position.CENTER, Position.CENTER), render = 1, auto_update = True):
        self._radius = radius
        self._circle = Image.new('L', (200, 200), 0)
        ImageDraw.Draw(self._circle).ellipse((0, 0, 200, 200), 255)
        super().__init__(xy, size, color, blur, margin, padding, position, origin, render, auto_update)


    def _draw_im(self, image, render = None):
        if render is None: render = self._render

        back = image.copy()
        im = self._add_radius()
        back.paste(im, (int(self._margin[0] * render), int(self._margin[1] * render)), im)
        return back 

    def _add_radius(self, render = None):
        """Добавляет радиус элементу"""
        big_start = datetime.now()
        if render is None: render = self._render

        w, h = self.indented_size
        w, h = (int(w * render), int(h * render))

        im = Image.new("RGBA", (w, h), self._color)
        
        radius = ()
        for i in range(len(self._radius)):
            radius += (0,) if self._radius[i] < 0 else (self._radius[i],)
        self._radius = radius
        radius = (int(radius[0] * render), int(radius[1] * render), int(radius[2] * render), int(radius[3] * render))
        if any(self._radius):

            alpha = Image.new('L', (w, h), 255)

            # обрезаем круг на четверть его размера и помещаем его в нужный угол окна
            if radius[0] > 0:
                circle = self._circle.resize((radius[0] * 2, radius[0] * 2), Image.LANCZOS)
                alpha.paste(circle.crop((0, 0, radius[0], radius[0])), (0, 0))#top left
            if radius[1] > 0:
                circle = self._circle.resize((radius[1] * 2, radius[1] * 2), Image.LANCZOS)
                alpha.paste(circle.crop((radius[1], 0, radius[1] * 2, radius[1])), (w - radius[1], 0))#top right
            if radius[2] > 0:
                circle = self._circle.resize((radius[2] * 2, radius[2] * 2), Image.LANCZOS)
                alpha.paste(circle.crop((0, radius[2], radius[2], radius[2] * 2)), (0, h - radius[2]))#bottom left
            if radius[3] > 0:
                circle = self._circle.resize((radius[3] * 2, radius[3] * 2), Image.LANCZOS)
                alpha.paste(circle.crop((radius[3], radius[3], radius[3] * 2, radius[3] * 2)), (w - radius[3], h - radius[3]))#bottom rigth

            try:
                if self._color[3] < 255:
                    im2 = Image.new("RGBA", (w, h), 0)
                    im = Image.composite(im, im2, alpha)
                else:
                    im.putalpha(alpha)
            except:
                im.putalpha(alpha)

            im.convert('RGBA')
        print("big_start = ", (datetime.now() - big_start))
        return im
    
    def reradius(self, radius: tuple[(int, int, int, int)]):
        self._radius = radius
        if self.auto_update: self._image = self._redraw()
