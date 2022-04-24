from Canvas import Canvas
from PIL import Image, ImageDraw
from Utils.Constants import Position

class Window(Canvas):
    def __init__(self, xy = (0, 0), size = (1, 1), color = (255, 255, 255, 255), radius = 20, blur = 0, margin = (0, 0, 0, 0), padding = (0, 0, 0, 0), position = (Position.CENTER, Position.CENTER), auto_update = True):
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
        
        if self._radius < 0: self._radius = 0
        if self._radius > 0:
            w, h = im.size

            alpha = Image.new('L', (w, h), 255)

            circle = Image.new('L', (self._radius * 4, self._radius * 4), 0)
            ImageDraw.Draw(circle).ellipse((0, 0, self._radius * 4, self._radius * 4), 255)
            circle = circle.resize((self._radius * 2, self._radius * 2), Image.LANCZOS)

            # обрезаем круг на четверть его размера и помещаем его в нужный угол окна
            alpha.paste(circle.crop((0, 0, self._radius, self._radius)), (0, 0))#top left
            alpha.paste(circle.crop((self._radius, 0, self._radius * 2, self._radius)), (w - self._radius, 0))#top right
            alpha.paste(circle.crop((0, self._radius, self._radius, self._radius * 2)), (0, h - self._radius))#bottom left
            alpha.paste(circle.crop((self._radius, self._radius, self._radius * 2, self._radius * 2)), (w - self._radius, h - self._radius))#bottom rigth

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
    
    def reradius(self, radius):
        self._radius = radius
        if self.auto_update: self._redraw()

