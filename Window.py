from Canvas import Canvas

class Window(Canvas):
    def __init__(self, position = (0, 0), size = (1, 1), color = (255, 255, 255, 255), blur = 0, auto_update = True):
        super().__init__(position, size, color, blur, auto_update)

