from Utils.Constants import Position
from Window import Window
from Canvas import Canvas
from Text import Text

if __name__ == "__main__":

    canvas = Canvas((0, 0), (700, 700), (255, 255, 255, 255), padding=(10, 10, 10, 10), margin=(20, 20, 20, 20))

    panel = Window((0, 0), (100, 100), (244, 124, 0, 100), margin=(10, 10, 30, 25), padding=(10, 10, 10, 10))
    text = Text("Hello World", (100, 450), size = 32)
    canvas.add(panel)
    canvas.add(Window((0, 0), (100, 100), (190, 123, 180, 255)))

    text = Text("Hello World", (0, 0), size = 32, margin=(10, 10, 20, 10), position=(Position.LEFT, Position.UPPER))
    canvas.add(text)

    text.recolor((34, 245, 34, 255))
    panel.reposition((Position.RIGHT, Position.CENTER))
    panel.recoordinates((200, 600))

    text_panel = Text("987654321123456789", (0, 0), size = 20, color= (0, 0, 0, 255), position = (Position.RIGHT, Position.LOWER), margin = (10, 10, 10, 10))
    panel.add(text_panel)
    text_panel.retext("Hello")
    panel.update()
    panel2 = Window((0, -200), (50, 50), (108, 123, 247, 255), position=(Position.RIGHT, Position.LOWER), margin=(0, 50, 25, 10))
    canvas.add(panel2)
    # panel.add(panel2)
    # panel.reblur(0.1)

    canvas.repadding((40, 30, 39, 130))

    canvas.show()