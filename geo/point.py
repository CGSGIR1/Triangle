from vec import Vec
from shape import Shape


class Point(Vec, Shape):
    POINT_R = 5

    def __init__(self, canvas, coords, color="red"):
        Vec.__init__(self, *coords)
        Shape.__init__(self, canvas)
        self._id = self._c.create_oval(0, 0, 0, 0, fill=color, tags="point")
        self.redraw()

    def redraw(self):
        x, y = self.x, self.y 
        r = self.POINT_R
        self._c.coords(self._id, x - r, y - r, x + r, y + r)

    def deletePoint(self):
        for d in self._depended:
            self._c.delete(d._id)
        self._c.delete(self._id)

    def deleteLine(self):
        for d in self._depended:
            self._c.delete(d._id)


class MovePoint(Point):
    def __init__(self, canvas, coords):
        super().__init__(canvas, coords)
        canvas.tag_bind(self._id, "<B1-Motion>", self.pressed)
        
    def pressed(self, ev):
        self.x = ev.x
        self.y = ev.y
        self.update()