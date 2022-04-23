from abc import abstractclassmethod
from Canvas import Canvas
from PIL import Image, ImageDraw, ImageFont

class Text(Canvas):
    def __init__(self, text, position = (0, 0), size = 16, color = (255, 255, 255, 255), font = "arial.ttf", blur = 0, auto_update = True):
        self._font = font
        self._size_font = size
        self._text = text
        # size text width and height
        font = ImageFont.truetype(self._font, self._size_font)
        size = font.getsize(text)
        super().__init__(position, size, color, blur, auto_update)
        self._redraw()
    
    def _redraw(self):
        """Перерисовывает текст"""
        font = ImageFont.truetype(self._font, self._size_font)
        self._size = font.getsize(self._text)
        self._image = Image.new("RGBA", self._size, (0, 0, 0, 0))
        ImageDraw.Draw(self._image).text((0, 0), self._text, self._color, font=font)

    def recolor(self, color):
        """Изменить цвет текста"""
        return super().recolor(color)

    def reposition(self, xy):
        """Изменить позицию текста"""
        return super().reposition(xy)      

    def add(self, element):
        """Нельзя добавлять элементы в текстовый объект"""
        raise AttributeError ("Нельзя добавлять элементы в текстовый объект")
    def remove(self, element):
        """Нельзя удалять элементы из текстового объекта"""
        raise AttributeError ("Нельзя удалять элементы из текстового объекта")
    def remove_index(self, index: int):
        """Нельзя удалять элементы из текстового объекта"""
        raise AttributeError ("Нельзя удалять элементы из текстового объекта")
    def clear(self):
        """Нельзя очищать текстовый объект от элементов"""
        raise AttributeError ("Нельзя очищать текстовый объект")