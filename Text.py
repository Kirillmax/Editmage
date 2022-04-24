from Canvas import Canvas
from PIL import Image, ImageDraw, ImageFont

from Utils.Constants import Position

class Text(Canvas):
    def __init__(self, text, xy = (0, 0), size = 16, color = (255, 255, 255, 255), font = "arial.ttf", blur = 0, margin = (0, 0, 0, 0), padding = (0, 0, 0, 0), position = (Position.CENTER, Position.CENTER), auto_update = True):
        self._font = font
        self._size_font = size
        self._text = text
        # size text width and height
        font = ImageFont.truetype(self._font, self._size_font)
        size = font.getsize(text)
        super().__init__(xy, size, color, blur, margin, padding, position, auto_update)
        
    def _draw_im(self, image):
        im = image.copy()
        font = ImageFont.truetype(self._font, self._size_font)
        ImageDraw.Draw(im).text((self._margin[0], self._margin[1]), self._text, self._color, font=font)

        return im

    def retext(self, text):
        """Изменить текст"""
        self._text = text

        font = ImageFont.truetype(self._font, self._size_font)
        self._real_size = font.getsize(self._text)
        self._size = self._tuple_add(self._real_size, self._margin)

        if self.auto_update: self._redraw()

    def resize(self, size: int):
        """Изменить размер текста(размер Font!!!)"""
        self._size_font = size
        font = ImageFont.truetype(self._font, self._size_font)
        self._real_size = font.getsize(self._text)
        self._size = self._tuple_add(self._real_size, self._margin)

        if self.auto_update: self._redraw()