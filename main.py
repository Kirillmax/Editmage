from Utils.Constants import Position, DEBUG
from Window import Window
from Canvas import Canvas
from Text import Text

if __name__ == "__main__":

    text = Text("Hello, wo\nljg k/jlk\nrhjk ghkl\ndjhjkhjk!", (0, 0), 20, (255, 255, 255, 255), render = 5)

    text.retext("Hello, world!\nHello, world!\nHello, world!")
    panel = Window((0, 0), text.size, (30, 30, 30, 255), radius = (0, 0, 12, 12), padding=(20, 20, 20, 20), position=(Position.CENTER, Position.LOWER), origin=(Position.CENTER, Position.LOWER), render = 5)

    top_panel = Window((0, 0), (panel.indented_size[0], 20), (30, 30, 30, 220), radius = (12, 12, 0, 0), position=(Position.CENTER, Position.UPPER), origin=(Position.CENTER, Position.UPPER), render = 5)

    shadow = Window((0, 0), (panel.indented_size[0], panel.indented_size[1] + 20), (0, 0, 0, 255), radius = (15, 15, 15, 15), blur=20, render = 5)
    shadow.remargin((50, 50, 50, 50))
    shadow.repadding((10, 10, 10, 10))

    circle1 = Window((24, 0), (12, 12), (128, 128, 128, 230), radius = (6, 6, 6, 6), padding=(0, 0, 0, 0), position=(Position.LEFT, Position.CENTER), render = 5)
    circle2 = Window((48, 0), (12, 12), (128, 128, 128, 230), radius = (6, 6, 6, 6), padding=(0, 0, 0, 0), position=(Position.LEFT, Position.CENTER), render = 5)
    circle3 = Window((72, 0), (12, 12), (128, 128, 128, 230), radius = (6, 6, 6, 6), padding=(0, 0, 0, 0), position=(Position.LEFT, Position.CENTER), render = 5)
    top_panel.add(circle1)
    top_panel.add(circle2)
    top_panel.add(circle3)

    panel.add(text)

    canvas = Canvas((0, 0), (panel._indented_size[0], panel._indented_size[1] + 20), (255, 255, 255), padding=(100, 100, 100, 100), render = 5)

    canvas.add(shadow)
    canvas.add(panel)
    canvas.add(top_panel)

    canvas.show()

    # canvas.image.convert("RGB").save("test.png")
    