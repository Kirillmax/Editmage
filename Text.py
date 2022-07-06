from Canvas import Canvas
from PIL import Image, ImageDraw, ImageFont

from Utils.Constants import Position

class Text(Canvas):
    def __init__(self, text, xy = (0, 0), font_size = 16, color = (255, 255, 255, 255), font = "arial.ttf", blur = 0, position = (Position.CENTER, Position.CENTER), origin = (Position.CENTER, Position.CENTER), render = 1, auto_update = True):
        """
        У Text есть НЕТ параметров:
        margin and padding!!!!
        """
        self._font = font
        self._font_size = font_size
        self._text = text
        # size text width and height
        font = ImageFont.truetype(self._font, self._font_size)
        size = self._get_size()
        super().__init__(xy, size, color, blur, (0, 0, 0, 0), (0, 0, 0, 0), position, origin, render, auto_update)
        
    def _draw_im(self, image, render=None):
        if render is None: render = self._render

        im = image.copy()
        font = ImageFont.truetype(self._font, self._font_size * render)
        ImageDraw.Draw(im).text((self._margin[0] * render, self._margin[1] * render), self._text, self._color, font=font)

        return im
    
    def _get_size(self):
        """
        Вернуть размер текста
        С учетом отступов И абзацев(\n)
        Возвращает размер текста БЕЗ учета render-а!!!!!!!!
        """
        str = self._text.split("\n")
        max_line_str = max(str, key=len)
        # Размер одного Tab-а!!!!!!!!!!!!!!!!!!!!!!!!!!
        tab_size = 3
        # найти количество вхождений сивмола '\t' в строке str
        tab_count = max_line_str.count("\t")
        w = int((len(max_line_str) + (tab_count * tab_size)) * self._get_font_size()[0])

        h = int((len(str)) * self._get_font_size()[1])
        return (w, h)

    def _get_font_size(self):
        font = ImageFont.truetype(self._font, self._font_size)
        return font.getsize("$")






    def retext(self, text):
        """Изменить текст"""
        self._text = text

        self._block_size = self._indented_size = self._size = self._get_size()

        if self.auto_update: self._image = self._redraw()

    def resize(self, size: int):
        """Изменить размер текста(Font size!!!)"""
        if size < 1: size = 1
        self._font_size = size
        
        self._block_size = self._indented_size = self._size = self._get_size()

        if self.auto_update: self._image = self._redraw()

    def copy(self):
        text = Text(
            self._text,
            self._coordinates,
            self._font_size,
            self._color,
            self._font,
            self._blur,
            self._position,
            self._origin,
            self._render,
            self.auto_update)
        for element in self._elements:
            text.add(element.copy())
        return text