from Utils.Constants import Position, Quality
from Window import Window
from Canvas import Canvas
from Text import Text

if __name__ == "__main__":

    text = Text()

    text.retext("a = 2\nb = 3\nresult = a + b\n\nprint('a + b = ', result)\n\n# Output:\n# a + b = 5")

    panel = Window((0, 0), text.size, (30, 30, 30, 255), radius = (0, 0, 6, 6), padding=(20, 20, 20, 20), position=(Position.CENTER, Position.LOWER), origin=(Position.CENTER, Position.LOWER), render = 5)

    top_panel = Window((0, 0), (panel.indented_size[0], 20), (30, 30, 30, 220), radius = (6, 6, 0, 0), position=(Position.CENTER, Position.UPPER), origin=(Position.CENTER, Position.UPPER), render = 5)

    shadow = Window((0, 0), (panel.indented_size[0], panel.indented_size[1] + 20), (0, 0, 0, 255), radius = (10, 10, 10, 10), blur=20, render = 5)
    shadow.remargin((50, 50, 50, 50))
    shadow.repadding((10, 10, 10, 10))

    circle1 = Window((24, 0), (10, 10), (255, 45, 85, 240), radius = (5, 5, 5, 5), padding=(0, 0, 0, 0), position=(Position.LEFT, Position.CENTER), render = 5)
    circle2 = circle1.copy()
    circle2.recoordinates((44, 0))
    circle2.recolor((255, 204, 0, 240))
    circle3 = circle1.copy()
    circle3.recoordinates((64, 0))
    circle3.recolor((76, 217, 100, 240))
    
    top_panel.add(circle1)
    top_panel.add(circle2)
    top_panel.add(circle3)

    panel.add(text)

    canvas = Canvas((0, 0), (panel._indented_size[0], panel._indented_size[1] + 20), (255, 255, 255))

    # квадрат:
    difference = (max(canvas.size) - min(canvas.size)) / 2
    if canvas.size[0] > canvas.size[1]:
        canvas.repadding((100, 100 + difference, 100, 100 + difference))
    else:
        canvas.repadding((100 + difference, 100, 100 + difference, 100))

    canvas.add(shadow)
    canvas.add(panel)
    canvas.add(top_panel)

    canvas.show()
    
    canvas.render(Quality.FHD).save("test.png", "PNG")

    