from distutils.debug import DEBUG
import enum

DEBUG = True

# Перечисление для расположения элемента относительно родителя
class Position(enum.Enum):
    NONE        = -1 # без расположения(считаются координаты пользователя)
    UPPER       =  0 # ↑ Верхний
    LEFT        =  1 # ← Левый
    RIGHT       =  2 # → Правый
    LOWER       =  3 # ↓ Нижний
    CENTER      =  4 # ● Центр