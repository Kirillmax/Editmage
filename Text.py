import re
from Canvas import Canvas
from PIL import Image, ImageDraw, ImageFont

from Utils.Constants import Position, Language, ColorText, color_text

class Text(Canvas):
    def __init__(self, text = "", xy = (0, 0), font_size = 16, color = (255, 255, 255, 255), font = "arial.ttf", blur = 0, position = (Position.CENTER, Position.CENTER), origin = (Position.CENTER, Position.CENTER), render = 1, auto_update = True):
        """
        У Text есть НЕТ параметров:
        margin and padding!!!!
        """
        self._font = font
        self._font_size = font_size
        if text == "": text = " "
        self._text = text.replace('\t', "    ") # '\t' заменятся ВСЕ!!! и \\t, '\t', #\t

        # size text width and height
        font = ImageFont.truetype(self._font, self._font_size)
        size = self._get_size()
        # self._language = Language.NONE
        self._language = Language.PYTHON
        super().__init__(xy, size, color, blur, (0, 0, 0, 0), (0, 0, 0, 0), position, origin, render, auto_update)
        
    def _draw_im(self, image, render = None):
        if render is None: render = self._render

        im = image.copy()

        if self._language != Language.NONE:
            im = self.draw_text(im, render)
        else:
            font = ImageFont.truetype(self._font, self._font_size * render)
            ImageDraw.Draw(im).multiline_text((self._margin[0] * render, self._margin[1] * render), self._text, self._color, font=font, align="left")

        return im
    
    def _get_size(self):
        """
        Вернуть размер текста
        С учетом отступов И абзацев(\n)
        Возвращает размер текста БЕЗ учета render-а!!!!!!!!
        """
        str = self._text.split("\n")
        max_line_str = max(str, key=len)
        w = int(self._get_font_size(max_line_str)[0] + (self._get_font_size(' ')[0] / 2)) # прибавляем половину пустой клетки(иногда дальний символ обрезает)

        h = int((len(str)) * self._get_font_size()[1])
        return (w, h)

    def _get_font_size(self, symbol = "$"):
        font = ImageFont.truetype(self._font, self._font_size)
        return font.getsize(symbol)

    def retext(self, text):
        """Изменить текст"""
        self._text = text.replace('\t', "    ")

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



    def draw_text(self, image, render=None):
        """
        Рисуем текст в определенной цветовой схеме (См. константы(Constants.py))
        для разных языков.\n
        Принимает изображение с уже готовым размером подходящем для текста\n
        Возвращает изображение с текстом.
        """
        if render is None: render = self._render

        im = image.copy()
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(self._font, int(self._font_size * render))
        height_font = self._get_font_size()[1] * render

        # разпиение текста на слова, числа, символы и пробелы
        split_text = re.findall(r"[0-9]+|[\w]+|\${|[ =\+\-\*\_~`%;:@\\|^&<>()}\[\].,!?;#\"\']|\$|\{|//|'|/| |\n|\t", self._text)
        
        if self._language == Language.JAVA:
            key_words  = {'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements', 'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package', 'private', 'protected', 'public', 'return', 'short', 'static', 'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws', 'transient', 'try', 'void', 'volatile', 'while'}
            adds_word  = {'System'} # добавляемые слова (import using class enum)
            class_word = {'class', 'import', 'enum', 'interface'} # слова поселе которых идут слова которые становятся спец словами: class Person(), Person - спец слово
        elif self._language == Language.C_SHARP:
            key_words  = {'var', 'string', 'int', 'float', 'double', 'bool', 'char', 'byte', 'decimal', 'long', 'short', 'const',    'false', 'true', 'abstract', 'as', 'base', 'break', 'break', 'case', 'catch', 'checked', 'class', 'continue', 'default', 'delegate', 'do', 'else', 'enum', 'event', 'explicit', 'extern', 'finally', 'fixed', 'for', 'foreach', 'goto', 'if', 'implicit', 'in', 'interface', 'internal', 'is', 'lock', 'namespace', 'new', 'null', 'object', 'operator', 'out', 'override', 'params', 'private', 'protected', 'public', 'readonly', 'ref', 'return', 'sbyte', 'sealed', 'short', 'sizeof', 'stackalloc', 'static', 'struct', 'switch', 'this', 'throw', 'try', 'typeof', 'uint', 'ulong', 'unchecked', 'unsafe', 'ushort', 'using', 'virtual', 'void', 'volatile', 'while'}
            adds_word  = {'add', 'dynamic', 'from', 'get', 'global', "group", 'into', 'join', "let" , "orderby", "partial", 'remove', 'select', 'set', "value", "where", "yield"} 
            class_word = {'class', 'using', 'enum', 'interface', 'namespace', 'struct', 'delegate'} # слова поселе которых идут слова которые становятся спец словами: class Person(), Person - спец слово
        elif self._language == Language.JAVA_SCRIPT:
            key_words  = {'abstract', 'arguments', 'await', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'continue', 'debugger', 'default', 'delete', 'do', 'double', 'else', 'enum', 'eval', 'export', 'extends', 'false', 'final', 'finally', 'float', 'for', 'function', 'goto', 'if', 'implements', 'import', 'in', 'instanceof', 'int', 'interface', 'let', 'long', 'native', 'new', 'null', 'package', 'private', 'protected', 'public', 'return', 'short', 'static', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws', 'transient', 'true', 'try', 'typeof', 'var', 'void', 'volatile', 'while', 'with', 'yield'}
            adds_word  = {'Array', 'Date', 'eval', 'function', 'hasOwnProperty', 'Infinity', 'isFinite', 'isNaN', 'isPrototypeOf', 'length', 'Math', 'NaN', 'Number', 'Object', 'prototype', 'String', 'toString', 'undefined', 'valueOf'}# добавляемые слова (import using class enum)
            class_word = {'class', 'import'} # слова поселе которых идут слова которые становятся спец словами: class Person(), Person - спец слово
        else: # if self._language == Language.PYTHON:
            key_words  = {'False', 'True', 'None', 'and', 'with', 'catch', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'yield'}
            adds_word  = {'os', 'property', 'self', 'Image', 're', 'range', 'list', 'set', 'int', 'float', 'str', 'map'} # добавляемые слова (import using class enum)
            class_word = {'class', 'import'} # слова поселе которых идут слова которые становятся спец словами: class Person(), Person - спец слово

        symbol = {'${','/', '.', ',', '?', '<', '>', '\'', '\"', '\\', '{', '}', ']', '[', '+', '_', '-', '=', '(', ')', '*', '&', '^', '%', '$', '!', '~', '`', ';', ':', '|'}

        comment = {
            '#' : (Language.PYTHON, Language.RUBY, Language.PHP),
            '//': (Language.JAVA, Language.C_SHARP, Language.JAVA_SCRIPT, Language.PHP, Language.C, Language.CPP, Language.GO, Language.RUST),
        }

        x, y =0, -(height_font - font.getsize(' ')[1])

        is_comment    = False # комментарий
        is_string     = ''    # всё что находится в ковычках считается строкой
        is_not_string = False # если в кавычках появляется "{23}", то оно не считается строкой

        length = len(split_text)
        # map(lambda p: abs(p), )
        for i in range(0, length):
            if set(split_text[i].split()) & class_word and i+2 < len(split_text):
                if split_text[i]=='delegate' and i+4 < len(split_text):
                    adds_word.add(split_text[i+4])
                    continue
                if split_text[i] == 'import':
                    for j in range(i+2, len(split_text)):
                        if split_text[j] == '\n':
                            break
                        adds_word.add(split_text[j])
                    continue
                adds_word.add(split_text[i+2])
            
        for i in range(0, length):
            if split_text[i] == ' ':
                x += self._get_font_size(' ')[0] * render
            else:
                if split_text[i] == '\n':
                    y += height_font
                    x = 0
                    is_comment = False
                    continue


                _is_last_string = is_string
                if split_text[i] in("'", '"') or (self._language == Language.JAVA_SCRIPT and split_text[i] == "`"):
                    is_string = '' if is_string else split_text[i] 

                if is_string and (split_text[i] == '{' and self._language != Language.JAVA_SCRIPT) or (split_text[i] == '${' and self._language == Language.JAVA_SCRIPT):
                    is_not_string = True
                is_comment  = True if self._language in(comment.get(split_text[i], (False, False))) and not is_string else is_comment                  
                
                color_txt = ColorText.VARIABLES
                color_txt = ColorText.DEFOLD    if (set(split_text[i].split()) & symbol) else color_txt
                color_txt = ColorText.NUMBERS   if (split_text[i].isdigit()) else color_txt
                color_txt = ColorText.FUNCTIONS if (split_text[i + 1 if i + 1 < length else i] == '(' and color_txt != ColorText.DEFOLD) else color_txt
                color_txt = ColorText.KEY_WORDS if (set(split_text[i].split()) & key_words) else color_txt
                color_txt = ColorText.CLASSES   if (set(split_text[i].split()) & adds_word) else color_txt
                color_txt = ColorText.STRINGS   if ((is_string or _is_last_string) and is_not_string==False) else color_txt
                color_txt = ColorText.COMMENTS  if (is_comment) else color_txt

                draw.text((x, y), split_text[i], color_text[color_txt], font = font)

                x += self._get_font_size(split_text[i])[0] * render

                if is_string and split_text[i]=='}':
                    is_not_string = False   

        return im