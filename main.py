from Utils.Constants import Position
from Window import Window
from Canvas import Canvas
from Text import Text

if __name__ == "__main__":

    canvas = Canvas((0, 0), (700, 700), (255, 255, 255, 255), padding=(10, 10, 10, 10), margin=(20, 20, 20, 20))

    panel2 = Window((0, 0), (300, 300), (108, 123, 247, 255), radius = 100, position=(Position.RIGHT, Position.LOWER), margin=(0, 50, 25, 10))
    canvas.add(panel2)
    panel1 = Window((0, 0), (200, 200), (255, 255, 189, 255), padding=(10, 10, 10, 10), margin=(20, 20, 20, 20))
    canvas.add(panel1)

    panel1.add(Text("Hello, world!", (0, 0), 16, (0, 0, 0, 255)))
    panel1.reradius(50)
    panel1.recolor((255, 0, 0, 255))
    canvas.show()