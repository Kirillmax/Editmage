from distutils.debug import DEBUG
import enum

DEBUG = True

# Перечисление для расположения элемента относительно родителя
class Position(enum.Enum):
    CENTER      =  0 # ● Центр (default)
    UPPER       =  1 # ↑ Верхний
    LEFT        =  2 # ← Левый
    RIGHT       =  3 # → Правый
    LOWER       =  4 # ↓ Нижний