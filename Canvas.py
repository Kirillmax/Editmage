from io import BytesIO
import base64
from PIL import Image, ImageFilter, ImageDraw

from Utils.Constants import Position, Quality, DEBUG

"""
Для обновления канваса необходимо вызвать функцию update()
Либо включить параметр auto_update = True
"""

class Canvas:
    def __init__(self, xy=(0, 0), size=(1, 1), color=(255, 255, 255, 255), blur: float = 0, margin=(0, 0, 0, 0), padding=(0, 0, 0, 0), position=(Position.CENTER, Position.CENTER), origin=(Position.CENTER, Position.CENTER), render = 1, auto_update: bool = True):
        """
        Конструктор класса
        :param xy: позиция элемента (координаты)()
        :param origin: отсчет позиции элемента (Position.CENTER, Position.CENTER)
        :param position: позиция элемента относитнльно родителя и отсчет координат (Position.CENTER, Position.UPPER)
        _______           _______          ________
        |      |          |∘ →x  |         |∘  ∘  ∘|
        |  ∘ →x|          |↓y    |         |∘  ○  ∘|
        |__↓y__|          |______|         |∘__∘__∘|
        (CENTER, CENTER) (LEFT, UPPER)
        :param size: размер элемента (width, height)
        :param real_size: размер элемента без учета margin и padding (width, height)
        :param color: цвет элемента
        :param blur: размытие элемента
        :param auto_update: автоматическое обновление канваса
        :param margin: границы элемента (учитывается при xy/position)(left, top, right, bottom)
        :param padding: поля элемента (учитывается при xy/position)(left, top, right, bottom)
        :param render: качество итогового элемента(изображения)
        """
        self.auto_update: bool = auto_update
        self._render = render
        self._margin = margin
        self._padding = padding
        self._blur: float = blur
        self._coordinates = xy

        self._position: tuple[Position, Position] = position

        self._origin: tuple[Position, Position] = origin

        self._size = size
        # Размер элемента с учетом PADDINGS
        self._indented_size = self._tuple_add(self._size, self._padding)
        # Размер элемента с учетом PADDINGS and MARGINS
        self._block_size = self._tuple_add(self._indented_size, self._margin)

        self._color = color
        self._elements: list[Canvas] = []  # type: list[Canvas]
        self._image = self._redraw()

    @property
    def image(self): return self._image

    @property
    def size(self): return self._size

    @property
    def indented_size(self): return self._indented_size

    @property
    def block_size(self): return self._block_size
    
    @property
    def margin(self): return self._margin
    
    @property
    def padding(self): return self._padding

    @property
    def position(self): return self._position
    
    @property
    def origin(self): return self._origin

    @property
    def coordinates(self): return self._coordinates

    def _dedug(self, image):
        """
        Дебаг
        Рисует границы элементов
        """

        im = image.copy()

        if DEBUG:
            RED = (255, 0, 0, 255)
            GREEN = (0, 255, 0, 255)
            BLUE = (0, 0, 255, 255)

            ImageDraw.Draw(im).rectangle(
                (0, 0,
                 self._block_size[0] - 1, self._block_size[1] - 1),
                outline=RED
            )
            ImageDraw.Draw(im).rectangle(
                (self._margin[0] + self._padding[0], self._margin[1] + self._padding[1],
                 self._size[0] + self._margin[0] + self._padding[0], self._size[1] + self._margin[1] + self._padding[1]),
                outline=BLUE
            )
            ImageDraw.Draw(im).rectangle(
                (self._margin[0], self._margin[1],
                 self._indented_size[0] + self._margin[0], self._indented_size[1] + self._margin[1]),
                outline=GREEN
            )
        return im

    def _tuple_add(self, t1: tuple[int, int], t2: tuple[int, int, int, int]):
        """Сложение двух кортежей"""
        return (t1[0] + t2[0] + t2[2], t1[1] + t2[1] + t2[3])

    def _redraw(self, render = None):
        """Перерисовывает канвас"""

        if render is None: render = self._render

        # создаем картинку прозрачной и размером с учетом отступов
        w, h = self._block_size
        # делаем ее больше на render 
        im = Image.new("RGBA", (int(w * render), int(h * render)), (0, 0, 0, 0))
        # Рисует сам элемент
        im = self._draw_im(im, render)
        # меняем размер элемента на заданный(без render)
        im = im.resize((int(w), int(h)), Image.LANCZOS)

        # Рисует дочерние элементы
        for element in self._elements:
            image = element.image

            # Создаем кордиинаты
            x, y = element.coordinates[0], element.coordinates[1]
            # Смещаем координаты на отступы слева и сверху(также и у дочернего элемента)
            x += self._padding[0] + self._margin[0] - element.margin[0]
            y += self._padding[1] + self._margin[1] - element.margin[1]

            # считаем нахождение координат отрисовки дочернего элемента
            for i in range(2):
                def pos_percent(position: Position):
                    if position == Position.CENTER: return .5
                    elif position in (Position.RIGHT, Position.LOWER): return 1
                    return 0
                # position
                coord = self._size[i] * pos_percent(element.position[i])
                # origin
                coord -= element.indented_size[i] * pos_percent(element.origin[i])
                # обновляем координаты
                x += coord if i == 0 else 0
                y += coord if i == 1 else 0

            if element._blur > 0 or element._color[3] > 0:
                # чтобы размытие(blur которые пременен к Дочерним элементам!) или прозрачность картинки не делала изображение(родителя) полупрозрачным
                image_a = Image.new("RGBA", im.size)
                image_a.paste(image, (int(x), int(y)), image)
                im = Image.alpha_composite(im, image_a)
            else:
                im.paste(image, (x, y), image)

        # Размываем картинку
        im = self._blur_im(im)

        im = self._dedug(im)
        
        return im

    def _redraw_rend(self, render = None):
        """Перерисовывает канвас"""

        if render is None: render = self._render
        
        im = Image.new("RGBA", (int(self._block_size[0] * render), int(self._block_size[1] * render)), (0, 0, 0, 0))
        im = self._draw_im(im, render)

        for element in self._elements:
            image = element._redraw_rend(render)

            x, y = element.coordinates[0] * render, element.coordinates[1] * render
            # Смещаем координаты на отступы слева и сверху(также и у дочернего элемента)
            x += (self._padding[0] + self._margin[0] - element.margin[0]) * render
            y += (self._padding[1] + self._margin[1] - element.margin[1]) * render

            # считаем нахождение координат отрисовки дочернего элемента
            for i in range(2):
                def pos_percent(position: Position):
                    if position == Position.CENTER: return .5
                    elif position in (Position.RIGHT, Position.LOWER): return 1
                    return 0
                # position
                coord = self._size[i] * pos_percent(element.position[i])
                # origin
                coord -= element.indented_size[i] * pos_percent(element.origin[i])
                # обновляем координаты
                x += coord * render if i == 0 else 0
                y += coord * render if i == 1 else 0

            if element._blur > 0 or element._color[3] > 0:
                # чтобы размытие(blur которые пременен к Дочерним элементам!) или прозрачность картинки не делала изображение(родителя) полупрозрачным
                image_a = Image.new("RGBA", im.size)
                image_a.paste(image, (int(x), int(y)), image)
                im = Image.alpha_composite(im, image_a)
            else:
                im.paste(image, (x, y), image)

        # Размываем картинку
        if self._blur > 0: return im.filter(ImageFilter.GaussianBlur(int(self._blur * render)))

        im = self._dedug(im)
        
        return im

    def _draw_im(self, image, render=None):
        """Рисует картинку на канвасе"""
        if render is None: render = self._render

        im = image.copy()
        ImageDraw.Draw(im).rectangle(
            (self._margin[0] * render,
             self._margin[1] * render,
             (self._margin[0] + self._indented_size[0]) * render,
             (self._margin[1] + self._indented_size[1]) * render),
            fill = self._color
        )
        return im

    def _blur_im(self, image):
        im = image.copy()
        if self._blur > 0: return im.filter(ImageFilter.GaussianBlur(self._blur))
        return im

    def recolor(self, color):
        """Изменить цвет элемента"""
        self._color = color
        if self.auto_update:
            self._image = self._redraw()

    def repadding(self, padding):
        """Изменить внутренние отстыпы у элемента (учитываются при xy/position)"""
        self._padding = padding
        self._indented_size = self._tuple_add(self._size, self._padding)
        self._block_size = self._tuple_add(self._indented_size, self._margin)

        if self.auto_update: self._image = self._redraw()

    def remargin(self, margin):
        """Изменить внешние отстыпы у элемента (учитываются при xy/position)"""
        self._margin = margin
        self._block_size = self._tuple_add(self._indented_size, self._margin)

        if self.auto_update: self._image = self._redraw()

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
            self._image = self._redraw()

    def resize(self, size):
        """Изменить размер элемента"""
        if size == self._size:
            return
        if size[0] > 0:
            self._size = (size[0], self._size[1])
        else:
            self._size = (1, self._size[1])
            print("Размер должен быть положительным. 'size' установлен на (1, x)")
        if size[1] > 0:
            self._size = (self._size[0], size[1])
        else:
            self._size = (self._size[0], 1)
            print("Размер должен быть положительным. 'size' установлен на (x, 1)")

        self._indented_size = self._tuple_add(self._size, self._padding)
        self._block_size = self._tuple_add(self._indented_size, self._margin)

        if self.auto_update: self._image = self._redraw()

    def reposition(self, position: tuple[Position, Position]):
        """Переместить элемент"""
        self._position = position
        if self.auto_update:
            self._image = self._redraw()
    
    def reorigin(self, origin: tuple[Position, Position]):
        """Центр элемента"""
        self._origin = origin
        if self.auto_update:
            self._image = self._redraw()

    def recoordinates(self, xy):
        """Переместить элемент"""
        self._coordinates = xy
        if self.auto_update:
            self._image = self._redraw()

    def update(self):
        """Обновляет элемент"""
        self._image = self._redraw()

    def get_base64(self):
        im = self._image.copy()

        buffered = BytesIO()
        im.save(buffered, format="PNG")

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
                self._image = self._redraw()

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
                self._image = self._redraw()

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
            self._image = self._redraw()

    def remove(self, element):
        """
        Удаляет элемент из дочерних элементов
        :param element: элемент для удаления (Canvas)
        """
        if element in self._elements:
            self._elements.remove(element)
            if self.auto_update:
                self._image = self._redraw()

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
            self._image = self._redraw()

    def clear_elements(self):
        """Очистить элемент от всех дочерних элементов"""
        self._elements.clear()
        if self.auto_update:
            self._image = self._redraw()

    def render(self, quality: Quality):        
        q = int(quality.value)  / min(self._block_size)
  
        im = self._redraw_rend(self._render + q)
        return im.resize((int(self._block_size[0] * q), int(self._block_size[1] * q)), Image.LANCZOS)

    def copy(self):
        canvas = Canvas(
            self._coordinates,
            self._size,
            self._color,
            self._blur,
            self._margin,
            self._padding,
            self._position,
            self._origin,
            self._render,
            self.auto_update)
        for element in self._elements:
            canvas.add(element.copy())
        return canvas

    def show(self):
        """Показать изображение. Вызывать после обновления(если автоматическое обновление НЕ включено)"""
        if self.auto_update:
            self._image = self._redraw()
        self._image.show()
