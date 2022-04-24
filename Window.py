from Canvas import Canvas
from PIL import Image, ImageDraw
from Utils.Constants import Position

class Window(Canvas):
    def __init__(self, xy = (0, 0), size = (1, 1), color = (255, 255, 255, 255), radius: tuple[(int, int, int, int)] = (0, 0, 0, 0), blur = 0, margin = (0, 0, 0, 0), padding = (0, 0, 0, 0), position = (Position.CENTER, Position.CENTER), auto_update = True):
        self._radius = radius
        super().__init__(xy, size, color, blur, margin, padding, position, auto_update)


    def _draw_im(self, image: Image):
        back = image.copy()
        im = self._add_radius()
        back.paste(im, (self._margin[0], self._margin[1]), im)
        return back 

    def _add_radius(self):
        """Добавляет радиус элементу"""
        im = self._image = Image.new("RGBA", self._real_size, self._color)
        
        radius = ()
        for i in range(len(self._radius)):
            radius += (0,) if self._radius[i] < 0 else (self._radius[i],)
        self._radius = radius
        if any(self._radius):
            w, h = im.size

            alpha = Image.new('L', (w, h), 255)

            circle = Image.new('L', (max(self._radius) * 8, max(self._radius) * 8), 0)
            ImageDraw.Draw(circle).ellipse((0, 0, max(self._radius) * 8, max(self._radius) * 8), 255)

            # обрезаем круг на четверть его размера и помещаем его в нужный угол окна
            if self._radius[0] > 0:
                circle = circle.resize((self._radius[0] * 2, self._radius[0] * 2), Image.LANCZOS)
                alpha.paste(circle.crop((0, 0, self._radius[0], self._radius[0])), (0, 0))#top left
            if self._radius[1] > 0:
                circle = circle.resize((self._radius[1] * 2, self._radius[1] * 2), Image.LANCZOS)
                alpha.paste(circle.crop((self._radius[1], 0, self._radius[1] * 2, self._radius[1])), (w - self._radius[1], 0))#top right
            if self._radius[2] > 0:
                circle = circle.resize((self._radius[2] * 2, self._radius[2] * 2), Image.LANCZOS)
                alpha.paste(circle.crop((0, self._radius[2], self._radius[2], self._radius[2] * 2)), (0, h - self._radius[2]))#bottom left
            if self._radius[3] > 0:
                circle = circle.resize((self._radius[3] * 2, self._radius[3] * 2), Image.LANCZOS)
                alpha.paste(circle.crop((self._radius[3], self._radius[3], self._radius[3] * 2, self._radius[3] * 2)), (w - self._radius[3], h - self._radius[3]))#bottom rigth

            try:
                if self._color[3] < 255:
                    im2 = Image.new("RGBA", (w, h), 0)
                    im = Image.composite(im, im2, alpha)
                else:
                    im.putalpha(alpha)
            except:
                im.putalpha(alpha)

            im.convert('RGBA')
        
        return im
    
    def reradius(self, radius: tuple[(int, int, int, int)]):
        self._radius = radius
        if self.auto_update: self._redraw()

