from abc import abstractclassmethod
from pydoc import classname
from PIL import Image, ImageFilter

"""
Для обновления канваса необходимо вызвать функцию update()
Либо включить параметр auto_update = True
"""
class Canvas:
    def __init__(self, xy=(0, 0), size=(1, 1), color=(255, 255, 255, 255), blur = 0, auto_update=True):
        """
        Конструктор класса
        :param xy: позиция элемента
        :param size: размер элемента
        :param color: цвет элемента
        :param blur: размытие элемента
        :param auto_update: автоматическое обновление канваса
        """
        self._auto_update = auto_update
        self._blur = blur
        self._position = xy
        self._size = size
        self._color = color
        self._image = Image.new("RGBA", self._size, self._color)
        self._elements = []  # type: list[Canvas]

    @property
    def image(self): return self._image

    @property
    def size(self): return self._size

    @property
    def auto_update(self) -> bool: return self._auto_update

    @auto_update.setter
    def auto_update(self, value: bool): self._auto_update = value

    @property
    def position(self): return self._position

    def _redraw(self):
        """Перерисовывает канвас"""

        self._image = Image.new("RGBA", self._size, self._color)
        for element in self._elements:
            print(element)
            image = element.image
            self._image.paste(image, element.position, image)
        
        if self._blur > 0:
            self._image = self._image.filter(ImageFilter.GaussianBlur(self._blur))

    def recolor(self, color):
        """Изменить цвет элемента"""   
        self._color = color
        if self._auto_update: self._redraw()

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
        if self._auto_update: self._redraw()
    
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
        if self._auto_update: self._redraw()
        
    def reposition(self, xy):
        """Переместить элемент"""
        self._position = xy
        if self._auto_update: self._redraw()

    def update(self):
        """Обновляет элемент"""
        self._redraw()

    def swap_elements(self, element1, element2):
        """
        Поменять местами элементы
        :param element1: первый элемент
        :param element2: второй элемент
        """
        if element1 in self._elements and element2 in self._elements:
            self._elements[self._elements.index(element1)] = element2
            self._elements[self._elements.index(element2)] = element1
            if self._auto_update: self._redraw()
        
    def move_element(self, element, index):
        """
        Переместить элемент в новую позицию
        :param element: элемент
        :param index: новая позиция
        """
        if element in self._elements:
            self._elements.remove(element)
            self._elements.insert(index, element)
            if self._auto_update: self._redraw()

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
                raise IndexError(f"Индекс(index = {index}) вне допустимого диапазона!")
        if self._auto_update: self._redraw()
        
    def remove(self, element):
        """
        Удаляет элемент из дочерних элементов
        :param element: элемент для удаления (Canvas)
        """
        if element in self._elements:
            self._elements.remove(element)
            if self._auto_update: self._redraw()
        
    def remove_index(self, index: int):
        """
        Удаляет элемент по индексу
        :param index: индекс элемента для удаления
        """
        try:
            self._elements.pop(index)
        except IndexError:
            raise IndexError(f"Индекс(index = {index}) вне допустимого диапазона!")
        if self._auto_update: self._redraw()
        
    def clear_elements(self):
        """Очистить элемент от всех дочерних элементов"""
        self._elements.clear()
        if self._auto_update: self._redraw()

    def render(self, render: int):
        for element in self._elements:
            self._image = element.render(render)
        return self._image

    def show(self):
        """Показать изображение. Вызывать после обновления(если автоматическое обновление НЕ включено)"""
        if self._auto_update: self._redraw()
        self._image.show()


