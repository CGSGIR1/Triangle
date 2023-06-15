from shape import Shape
from line import Line
from circle import Circle
from point import Point
from vec import Vec
import random


class Intersection(Shape):
    def __init__(self, canvas, sh1, sh2):
        super().__init__(canvas)
        for s in sh1, sh2:
            s.add_dependency(self)
        self.sh1, self.sh2 = sh1, sh2
        self.redraw()

    def redraw(self):
        if type(self.sh1) is Line and type(self.sh2) is Line:
            self.intersectLL(self.sh1, self.sh2)
        if type(self.sh1) is Circle and type(self.sh2) is Line:
            self.intersectCL(self.sh1, self.sh2)
        if type(self.sh1) is Circle and type(self.sh2) is Circle:
            self.intersectCC(self.sh1, self.sh2)
        for p in self._points:
            p.redraw()
    
    def intersectCL(self, circle1, line1):
        self._points = []
        p = circle1.C
        
        u = (line1.p0 - line1.p1).left()
        v = u.left()
        t2, t1 = (p - line1.p0).to_base(u, -v)
        d = u * t1
        R = (circle1.C - circle1.P).len2()
        if R - d.len2() >= 0:
            dlin = (R - d.len2()) ** 0.5
            b = ((line1.p1 - line1.p0).Dir()) * dlin
            
            point1 = b + p - d
            point2 = p - d - b
            self._points.append(Point(self._c, (point1.x, point1.y), "blue"))
            self._points.append(Point(self._c, (point2.x, point2.y), "blue"))
        else:
            pass

    def intersectCC(self, circle1, circle2):
        self._points = []
        R1 = (circle1.C - circle1.P).len2()
        R2 = (circle2.C - circle2.P).len2()
        d = (circle2.C - circle1.C).len1()
        a = (R1 - R2 + d**2) / (2 * d)
        t = circle1.C + (circle2.C - circle1.C) * (a / d)
        if (R1 - a ** 2) >= 0:
            h = (R1 - a ** 2) ** 0.5
            point1 = Vec(t.x + (circle2.C.y - circle1.C.y) * (h / d), t.y - (circle2.C.x - circle1.C.x) * (h / d))
            point2 = Vec(t.x - (circle2.C.y - circle1.C.y) * (h / d), t.y + (circle2.C.x - circle1.C.x) * (h / d))
            self._points.append(Point(self._c, (point1.x, point1.y), "blue"))
            self._points.append(Point(self._c, (point2.x, point2.y), "blue"))
        else:
            pass

    def intersectLL(self, line1, line2):
        self._points = []
        toch1 = line1.p0
        toch2  = line2.p0
        B1 = line1.p1
        B2 = line2.p1
        k = B1 - toch1 
        m = B2 - toch2
        t1, t2 = (toch2 - toch1).to_base(k, m)
        fin = toch1 + k * t2
        self._points.append(Point(self._c, (fin.x, fin.y), "blue"))