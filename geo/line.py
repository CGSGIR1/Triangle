from shape import Shape
import math

EPS = 1e-9
class Line(Shape):
    def __init__(self, canvas, A, B, colorl="black", tag="l"):
        super().__init__(canvas)
        self.p0 = A
        self.p1 = B
        for p in A, B:
            p.add_dependency(self)

        self._id = self._c.create_line(0, 0, 0, 0, fill=colorl, width=2, tags=tag)
        self.redraw()
        
     # line = Line.from_abc(a, b, c)

    # line = Line.from_points(A, B)
    def from_points(A, B):
        normal = (A - B).left()
        return Line(A, normal)

    def contains(self, point):
        return abs(self.normal * (point - self.p0)) < EPS

    def coof(self):
        a = self.normal.x
        b = self.normal.y
        return a, b, -(a * self.p0.x + b * self.p0.y)

    def parLine(self, R):
        r = self.normal.Dir() * R
        a = Line(self.p0 + r, self.normal)
        b = Line(self.p0 + (r * (-1)), self.normal)
        return a.coof(), b.coof()

    def intersec(self, other):
        a1, b1, c1 = self.coof()
        a2, b2, c2 = other.coof()
        if a1 == 0:
            y = (c1 * a2 - c2 * a1) / (a1 * b2 - a2 * b1)
            x = y
        else:
            y = (c1 * a2 - c2 * a1) / (a1 * b2 - a2 * b1)
            x = -(b1 * y + c1) / a1
        return x, y

    def paralel(self, other):
        g = round(self.normal.angle1(other.normal), 6)
        return g == 0 or g == round(math.pi, 6)

    def position(self, p1, p2):
        norm = self.normal - self.p0
        vec1 = p1 - self.p0
        vec2 = p2 - self.p0
        a = norm.angle1(vec1)
        b = norm.angle1(vec2)
        if a > (math.pi / 2) and b > (math.pi / 2):
            return True
        elif a < (math.pi / 2) and b < (math.pi / 2):
            return True
        else:
            return False
    
    def redraw(self):
        self._c.coords(self._id,
                       self.p0.x, self.p0.y,
                       self.p1.x, self.p1.y)