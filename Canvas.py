from io import BytesIO
import base64, io
from PIL import Image, ImageFilter, ImageDraw
from matplotlib.animation import ImageMagickBase

from Utils.Constants import Position, DEBUG

"""
Для обновления канваса необходимо вызвать функцию update()
Либо включить параметр auto_update = True
"""


class Canvas:
    def __init__(self, xy=(0, 0), size=(1, 1), color=(255, 255, 255, 255), blur: float = 0, margin=(0, 0, 0, 0), padding=(0, 0, 0, 0), position=(Position.CENTER, Position.CENTER), render = 1, auto_update: bool = True):
        """
        Конструктор класса
        :param xy: позиция элемента (координаты)()
        :param position: позиция элемента относитнльно родителя и отсчет координат (Position.CENTER, Position.UPPER)
         ______            ______
        |      |          |∘ →x  |
        |  ∘ →x|          |↓y    |
        |__↓y__|          |______|
        (CENTER, CENTER) (LEFT, UPPER)
        :param size: размер элемента (width, height)
        :param real_size: размер элемента без учета margin и padding (width, height)
        :param color: цвет элемента
        :param blur: размытие элемента
        :param auto_update: автоматическое обновление канваса
        :param margin: границы элемента (учитывается при xy/position)(left, top, right, bottom)
        :param padding: поля элемента (учитывается при xy/position)(left, top, right, bottom)
        """
        self.auto_update: bool = auto_update
        self._render = render
        self._margin = margin
        self._padding = padding
        self._blur: float = blur
        self._coordinates = xy
        self._position: tuple[Position, Position] = position
        self._real_size = size
        self._size = self._tuple_add(self._tuple_add(self._real_size, self._margin), self._padding)
        self._color = color
        self._image = Image.new("RGBA", (1, 1))
        self._elements: list[Canvas] = []  # type: list[Canvas]
        self._redraw()

        self._dedug()

    @property
    def image(self): return self._image

    @property
    def size(self): return self._size

    @property
    def real_size(self): return self._real_size
   
    @property
    def size_add_padding(self): return self._tuple_add(self._real_size, self._padding)

    @property
    def position(self): return self._position

    @property
    def coordinates(self): return self._coordinates

    def _dedug(self):
        """
        Дебаг
        Рисует границы элементов
        """
        if DEBUG:
            ImageDraw.Draw(self._image).rectangle(
                (0, 0, self._size[0] - 1, self._size[1] - 1), outline=(255, 0, 0, 255))
            ImageDraw.Draw(self._image).rectangle((self._margin[0] + self._padding[0], self._margin[1] + self._padding[1], self._size[0] -
                                                   self._margin[2] - self._padding[2], self._size[1] - self._margin[3] - self._padding[3]), outline=(0, 0, 255, 255))
            ImageDraw.Draw(self._image).rectangle(
                (self._margin[0], self._margin[1], self._size[0] - self._margin[2], self._size[1] - self._margin[3]), outline=(0, 255, 0, 255))

    def _tuple_add(self, t1: tuple[int, int], t2: tuple[int, int, int, int]):
        """Сложение двух кортежей"""
        return (t1[0] + t2[0] + t2[2], t1[1] + t2[1] + t2[3])

    def _redraw(self, render = None):
        """Перерисовывает канвас"""

        if render is None: render = self._render

        w, h = self._size

        self._image = Image.new("RGBA", (int(w * render), int(h * render)), (0, 0, 0, 0))

        self._image = self._draw_im(self._image)

        self._image = self._image.resize(self._size, Image.LANCZOS)

        for element in self._elements:
            image = element.image

            x, y = element.coordinates
            x += self._padding[0] + self._margin[0]
            y += self._padding[1] + self._margin[1]

            for i in range(2):
                xy_pos = self._real_size[i] - element.size[i]
                if element.position[i] == Position.CENTER:
                    x += xy_pos // 2 if i==0 else 0
                    y += xy_pos // 2 if i==1 else 0
                elif element.position[i] in(Position.RIGHT, Position.LOWER):
                    x += xy_pos if i==0 else 0
                    y += xy_pos if i==1 else 0

            if element._blur > 0:
                # чтобы тень не делала изображение полупрозрачным
                image_a = Image.new("RGBA", self._image.size)
                image_a.paste(image, (x, y), image)
                self._image = Image.alpha_composite(self._image, image_a)
            else:
                self._image.paste(image, (x, y), image)


        self._image = self._blur_im(self._image)


        self._dedug()

    def _draw_im(self, image, render = None):
        """Рисует картинку на канвасе"""
        if render is None: render = self._render

        im = image.copy()
        ImageDraw.Draw(im).rectangle(
            (self._margin[0] * render, self._margin[1] * render, (self._size[0] - self._margin[2]) * render, (self._size[1] - self._margin[3]) * render), fill=self._color)
        return im

    def _blur_im(self, image):
        im = image.copy()
        if self._blur > 0:
            return im.filter(ImageFilter.GaussianBlur(self._blur))
        return im

    def recolor(self, color):
        """Изменить цвет элемента"""
        self._color = color
        if self.auto_update:
            self._redraw()

    def repadding(self, padding):
        """Изменить внутренние отстыпы у элемента (учитываются при xy/position)"""
        self._padding = padding
        self._size = self._tuple_add(self._tuple_add(self._real_size, self._margin), self._padding)
        if self.auto_update:
            self._redraw()

    def remargin(self, margin):
        """Изменить внешние отстыпы у элемента (учитываются при xy/position)"""
        self._margin = margin
        self._size = self._tuple_add(self._tuple_add(self._real_size, self._margin), self._padding)
        if self.auto_update:
            self._redraw()

    def reblur(self, blur):
        """
        Изменить размытие элемента
        (Затрагивает также его дочерние элементы)
        :param blur: сила размытие (0 - нет размытия)
        """
        if blur == self._blur:
            return
        if blur > 0:
            self._blur = blur
        else:
            self._blur = 0
            print("Размытие должно быть положительным. 'blur' установлен на 0")
        if self.auto_update:
            self._redraw()

    def resize(self, size):
        """Изменить размер элемента"""
        if size == self._real_size:
            return
        if size[0] > 0:
            self._real_size = (size[0], self._real_size[1])
        else:
            self._real_size = (1, self._real_size[1])
            print("Размер должен быть положительным. 'size' установлен на (1, x)")
        if size[1] > 0:
            self._real_size = (self._real_size[0], size[1])
        else:
            self._real_size = (self._real_size[0], 1)
            print("Размер должен быть положительным. 'size' установлен на (x, 1)")
        self._size = self._tuple_add(self._tuple_add(self._real_size, self._margin), self._padding)
        if self.auto_update:
            self._redraw()

    def reposition(self, position: tuple[Position, Position]):
        """Переместить элемент"""
        self._position = position
        if self.auto_update:
            self._redraw()

    def recoordinates(self, xy):
        """Переместить элемент"""
        self._coordinates = xy
        if self.auto_update:
            self._redraw()

    def update(self):
        """Обновляет элемент"""
        self._redraw()

    def get_base64(self):
        im = self._image.copy()

        buffered = BytesIO()
        im.save(buffered, format = "PNG")

        base64_bytes = base64.b64encode(buffered.getvalue())
        base64_str = ("data:image/png;base64," + base64_bytes.decode('utf-8'))
        return base64_str

    def swap_elements(self, element1, element2):
        """
        Поменять местами элементы
        :param element1: первый элемент
        :param element2: второй элемент
        """
        if element1 in self._elements and element2 in self._elements:
            self._elements[self._elements.index(element1)] = element2
            self._elements[self._elements.index(element2)] = element1
            if self.auto_update:
                self._redraw()

    def move_element(self, element, index):
        """
        Переместить элемент в новую позицию
        :param element: элемент
        :param index: новая позиция
        """
        if element in self._elements:
            self._elements.remove(element)
            self._elements.insert(index, element)
            if self.auto_update:
                self._redraw()

    def add(self, element, index: int = -1):
        """
        Добавляет элемент как дочерний для текущего элементу
        :param element: элемент для добавления (Canvas)
        :param index: индекс в который добавляется элемент (по умолчанию (-1) - в конец)
        """
        if index == -1:
            self._elements.append(element)
        else:
            try:
                self._elements.insert(index, element)
            except IndexError:
                raise IndexError(
                    f"Индекс(index = {index}) вне допустимого диапазона!")
        if self.auto_update:
            self._redraw()

    def remove(self, element):
        """
        Удаляет элемент из дочерних элементов
        :param element: элемент для удаления (Canvas)
        """
        if element in self._elements:
            self._elements.remove(element)
            if self.auto_update:
                self._redraw()

    def remove_index(self, index: int):
        """
        Удаляет элемент по индексу
        :param index: индекс элемента для удаления
        """
        try:
            self._elements.pop(index)
        except IndexError:
            raise IndexError(
                f"Индекс(index = {index}) вне допустимого диапазона!")
        if self.auto_update:
            self._redraw()

    def clear_elements(self):
        """Очистить элемент от всех дочерних элементов"""
        self._elements.clear()
        if self.auto_update:
            self._redraw()

    def render(self, render: int):
        
        # for element in self._elements:
        #     self._image = element.render(render)
        if self.auto_update:
            self._redraw()
        return self._image

    def show(self):
        """Показать изображение. Вызывать после обновления(если автоматическое обновление НЕ включено)"""
        if self.auto_update:
            self._redraw()
        self._image.show()
