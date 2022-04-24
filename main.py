from Utils.Constants import Position
from Window import Window
from Canvas import Canvas
from Text import Text

if __name__ == "__main__":

    canvas = Canvas((0, 0), (700, 700), (255, 255, 255, 255))

    panel = Window((100, 100), (100, 100), (244, 124, 0, 100), margin=(10, 10, 30, 25))
    text = Text("Hello World", (100, 450), size = 32)
    canvas.add(panel)
    canvas.add(Window((100, 100), (100, 100), (190, 123, 180, 255)))

    text = Text("Hello World", (100, 450), size = 32, margin=(10, 10, 20, 10))
    canvas.add(text)

    text.recolor((34, 245, 34, 255))
    panel.reposition((Position.CENTER, Position.CENTER))
    panel.recoordinates((200, 600))

    print(canvas)

    text_panel = Text("987654321123456789", (0, 0), size = 20, color= (0, 0, 0, 255), position = (Position.CENTER, Position.CENTER), margin = (10, 25, 30, 7))
    panel.add(text_panel)
    panel2 = Window((0, 0), (50, 50), (108, 123, 247, 255), position=(Position.CENTER, Position.CENTER), margin=(0, 50, 25, 10))
    # panel.add(panel2)
    # panel.reblur(1.3)

    canvas.show()