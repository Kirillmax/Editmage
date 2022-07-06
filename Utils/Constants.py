from distutils.debug import DEBUG
import enum

DEBUG = False
# DEBUG = True

# Перечисление для расположения элемента относительно родителя
class Position(enum.Enum):
    CENTER      =  0 # ● Центр (default)
    UPPER       =  1 # ↑ Верхний
    LEFT        =  2 # ← Левый
    RIGHT       =  3 # → Правый
    LOWER       =  4 # ↓ Нижний


# Размер готового изображения
class Quality(enum.Enum):
    SD  = 480
    HD  = 720
    FHD = 1080
    QHD = 1440
    UHD = 2160

COLOR_DEFOLD    = (224, 224, 224) # white все символы "/.,:;?()[]{}<>+-_=!@#$%^&*|~`"
COLOR_KEY_WORDS = (217,  61,  89) # red ключевые слова var int def class....
COLOR_STRINGS   = (148, 166, 109) # green кавычки и в них - "текст" или 'текст'
COLOR_CLASSES   = ( 87, 199, 159) # ярко green class enum import using....
COLOR_COMMENTS  = ( 57,  77,  89) # gray комментарии
COLOR_NUMBERS   = (127,  99, 166) # violet числа
COLOR_VARIABLES = ( 51, 153, 255) # Blue всё остальное
COLOR_FUNCTIONS = (242, 165,  22) # orange классы (def вот_это(self))

class ColorText(enum.Enum):
    DEFOLD    = 0 # COLOR_DEFOLD
    KEY_WORDS = 1 # COLOR_KEY_WORDS
    STRINGS   = 2 # COLOR_STRINGS
    CLASSES   = 3 # COLOR_CLASSES
    COMMENTS  = 4 # COLOR_COMMENTS
    NUMBERS   = 5 # COLOR_NUMBERS
    VARIABLES = 6 # COLOR_VARIABLES
    FUNCTIONS = 7 # COLOR_FUNCTIONS

color_text = {
    ColorText.DEFOLD: COLOR_DEFOLD,
    ColorText.KEY_WORDS: COLOR_KEY_WORDS,
    ColorText.STRINGS: COLOR_STRINGS,
    ColorText.CLASSES: COLOR_CLASSES,
    ColorText.COMMENTS: COLOR_COMMENTS,
    ColorText.NUMBERS: COLOR_NUMBERS,
    ColorText.VARIABLES: COLOR_VARIABLES,
    ColorText.FUNCTIONS: COLOR_FUNCTIONS
}

# Класс для определения цветовой схемы языка
class Language(enum.Enum):
    NONE        = -1
    PYTHON      =  0 
    KOTLIN      =  1
    C_SHARP     =  2
    JAVA        =  3
    JAVA_SCRIPT =  4
    SWIFT       =  5
    CSS         =  6
    SQL         =  7
    RUBY        =  8
    GO          =  9
    C           = 10
    HTML        = 11
    CPP         = 12
    PHP         = 13
    JSON        = 14
    RUST        = 15