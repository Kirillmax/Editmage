from Window import Window
from Canvas import Canvas
from Text import Text

if __name__ == "__main__":

    canvas = Canvas((0, 0), (700, 700), (255, 255, 255, 255))

    panel = Window((100, 100), (100, 100), (0, 255, 0, 100))
    canvas.add(panel)

    text = Text("Hello World", (100, 450), size = 32)
    canvas.add(text)

    text.recolor((34, 245, 34, 255))
    panel.reposition((200, 600))

    text_panel = Text("Hello World", (0, 0), size = 20, color= (0, 0, 0, 255))
    panel.add(text_panel)
    panel.reblur(1.3)

    canvas.show()