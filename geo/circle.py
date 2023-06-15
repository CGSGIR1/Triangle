from vec import Vec
from shape import Shape

class Circle(Shape):
    def __init__(self, canvas, C, P):
        super().__init__(canvas)
        self.C = C
        self.P = P
        for p in C, P:
            p.add_dependency(self)
        self._id = self._c.create_oval(0, 0, 0, 0, width=2)
        self.redraw()

    def redraw(self):
        dist = Vec.len1(self.C - self.P)
        self._c.coords(self._id,
                       self.C.x - dist, self.C.y - dist,
                       self.C.x + dist, self.C.y + dist)