from vec import Vec
from shape import Shape

class Triangle(Shape):
    def __init__(self, canvas, P0, P1, P2, color="blue", tag="t"):
        super().__init__(canvas)
        self.P0 = P0
        self.P1 = P1
        self.P2 = P2
        for p in P0, P1, P2:
            p.add_dependency(self)
        dots = [P0.x, P0.y, P1.x, P1.y, P2.x, P2.y]
        self._id = self._c.create_polygon(dots, outline="black",
                         fill=color, width=3, tags=tag)
        self.redraw()

    def redraw(self):
        dots = [self.P0.x, self.P0.y, self.P1.x, self.P1.y, self.P2.x, self.P2.y]
        self._c.coords(self._id, *dots)