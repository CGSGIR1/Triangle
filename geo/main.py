import keyboard
import math
import random
import tkinter as tk
import time
import tkinter.ttk as ttk
from math import cos, sin
from vec import Vec
from point import MovePoint
from line import Line
from pointsSort import quick_sort_point
from triangle import Triangle
from circle import Circle
from intersection import Intersection


def point_side(line_start, line_end, point):
    line_vec = line_end - line_start
    point_vec = point - line_start

    # Рассчитываем векторное произведение двух векторов
    cross_product = line_vec.x * point_vec.y - line_vec.y * point_vec.x

    if cross_product > 0:
        return False
    elif cross_product < 0:
        return True
    else:
        return True


def newAngle(line_start, line_end, point):
    # Вычисляем координаты векторов между началом отрезка, его концом и исходной точкой
    line_vector = line_end - point
    point_vector = line_start - point

    # Вычисляем длины векторов
    line_length = math.sqrt(line_vector.x ** 2 + line_vector.y ** 2)
    point_length = math.sqrt(point_vector.x ** 2 + point_vector.y ** 2)

    # Вычисляем скалярное произведение векторов
    dot_product = line_vector.x * point_vector.x + line_vector.y * point_vector.y

    # Вычисляем косинус угла между векторами
    a = line_length * point_length
    if a == 0:
        a = 10 ** 10
    cos_angle = dot_product / a
    if cos_angle - 1 < (10 ** -8):
        cos_angle -= 0.0000001
    if cos_angle + 1 < -(10 ** -8):
        cos_angle += 0.0000001
    try:
        angle_rad = math.acos(cos_angle)
    except:
        print("kapez")
        print(cos_angle)
        return
    angle_deg = math.degrees(angle_rad)
    return angle_deg


def rgb_hack(rgb):
    return "#%02x%02x%02x" % rgb

def ClearTriangl():
    global points
    print(":(")
    for i in range(len(points)):
        points[i].deleteLine()

def _Triangularion(Points):
    global c, polyghons
    if (len(Points) < 2):
        return
    # сортируем точки по координате x
    quick_sort_point(Points)
    print(len(Points))
    delPoints = []
    # ищем одинаковые точки
    for i in range(len(Points)):
        for j in range(i + 1, len(Points)):
            if Points[i].x == Points[j].x:
                if Points[i].y == Points[j].y:
                    delPoints.append(j)
                    i = j
            else:
                i += 1
    newPoints = []
    k = 0
    # создаем новый массив без повторяющихся точек
    if len(delPoints) > 0:
        for i in range(len(Points)):
            if i != delPoints[k]:
                newPoints.append(Points[i])
            else:
                if k < len(delPoints) - 1:
                    k += 1
    else:
        for i in range(len(Points)):
            newPoints.append(Points[i])
    if (len(newPoints) < 2):
        return
    ClearTriangl()

    # ищем самую левую нижнию точку
    lenPoints = len(newPoints)
    print(lenPoints)
    P0 = 0
    for i in range(lenPoints):
        if newPoints[i].x != newPoints[P0].x:
            break
        if newPoints[i].y < newPoints[P0].y:
            P0 = i
    c.itemconfig(newPoints[P0]._id, fill='yellow')

    # ищем вторую точку для первого ребра
    secondPoints = []
    for i in range(lenPoints):
        correct = True
        if i == P0:
            continue
        for j in range(lenPoints):
            if i == j or j == P0:
                continue
            if not point_side(newPoints[P0], newPoints[i], newPoints[j]):
                correct = False
                break
        if correct == True:
            secondPoints.append(i)
    P1 = secondPoints[0]
    dist = newPoints[P0].lenTwoPoints(newPoints[P1])
    print(dist)
    for i in range(len(secondPoints)):
        distNew = newPoints[P0].lenTwoPoints(newPoints[secondPoints[i]])
        if dist > distNew:
            dist = distNew
            P1 = secondPoints[i]

    ActiveEdges = [[P0, P1]]
    itogEdges = [[P0, P1]]
    triangles = []
    # ActiveLines = [Line(c, newPoints[P0], newPoints[P1], "red")]
    # SleepLines = []
    print(ActiveEdges.count([P0, P1]))
    while len(ActiveEdges) != 0:
        # time.sleep(0.1)
        n = len(ActiveEdges) - 1
        angle = 0
        anglem = 0
        P2 = None
        P3 = None
        P0 = ActiveEdges[n][0]
        P1 = ActiveEdges[n][1]
        for i in range(lenPoints):
            if i == ActiveEdges[n][0] or i == ActiveEdges[n][1]:
                continue
            # print(P0, P1, i)
            angle2 = newAngle(newPoints[P0], newPoints[P1], newPoints[i])
            if point_side(newPoints[P0], newPoints[P1], newPoints[i]):
                if angle2 > angle:
                    P2 = i
                    angle = angle2
            else:
                if angle2 > anglem:
                    P3 = i
                    anglem = angle2
        ActiveEdges.pop()
        # del ActiveLines[-1]
        # SleepLines.append(Line(c, newPoints[P0], newPoints[P1], "black"))
        if P2 != None:
            triangles.append([P0, P1, P2])
            if itogEdges.count([P0, P2]) == 0 and itogEdges.count([P2, P0]) == 0:
                ActiveEdges.append([P2, P0])
                # ActiveLines.append(Line(c, newPoints[P2], newPoints[P0], "red"))
                itogEdges.append([P2, P0])
            if itogEdges.count([P1, P2]) == 0 and itogEdges.count([P2, P1]) == 0:
                ActiveEdges.append([P2, P1])
                itogEdges.append([P2, P1])
                # ActiveLines.append(Line(c, newPoints[P2], newPoints[P1], "red"))
        if P3 != None and P2 != P3:
            triangles.append([P0, P1, P3])
            if itogEdges.count([P0, P3]) == 0 and itogEdges.count([P3, P0]) == 0:
                ActiveEdges.append([P3, P0])
                itogEdges.append([P3, P0])
                # ActiveLines.append(Line(c, newPoints[P3], newPoints[P0], "red"))
            if itogEdges.count([P1, P3]) == 0 and itogEdges.count([P3, P1]) == 0:
                ActiveEdges.append([P3, P1])
                itogEdges.append([P3, P1])
                # ActiveLines.append(Line(c, newPoints[P3], newPoints[P1], "red"))
    for i in triangles:
        i.sort()
    temp = []
    print(len(triangles))
    for x in triangles:
        if x not in temp: temp.append(x)
    triangles = temp
    print(len(triangles))
    colors = ["yellow", "blue", "gray", "green", "brown", "red", "orange", "purple", "pink"]
    for i in range(len(triangles)):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        polyghons.append(Triangle(c, newPoints[triangles[i][0]], newPoints[triangles[i][1]], newPoints[triangles[i][2]],
                                  color=rgb_hack((r, g, b))))
    # triangles1 = set(triangles)
    # print(triangles1)
    c.tag_lower("t")
    # c.tag_raise("l")


def Triangularion():
    global points
    _Triangularion(list(points))


def addPoint(ev):
    global c, flag, points
    if flag == True:
        k = MovePoint(c, (ev.x, ev.y))
        points.append(k)


def FlagPoint():
    global flag, points
    if flag == True:
        flag = False
    else:
        flag = True


def DeletePoints():
    global points
    if (len(points) > 0):
        points[-1].deletePoint()
        points.pop()


def ClearPoints():
    global points
    while (len(points) > 0):
        DeletePoints()


def RandomPoints(win):
    global c, points, flag
    if (flag):
        win.update_idletasks()
        s = win.geometry()
        s = s.split('+')
        s = s[0].split('x')
        width_root = int(s[0])
        height_root = int(s[1])
        for i in range(10, width_root - 20, 40):
            for j in range(10, height_root - 20, 40):
                k = MovePoint(c, (i, j))
                points.append(k)
    else:
        win.update_idletasks()
        s = win.geometry()
        s = s.split('+')
        s = s[0].split('x')
        width_root = int(s[0])
        height_root = int(s[1])
        lenp = len(points)
        while (len(points) <= lenp + 100):
            k = MovePoint(c, (random.randint(5, width_root - 10), random.randint(5, height_root - 10)))
            points.append(k)


def painting(ev):
    global c, polyghons
    tag = c.find_closest(ev.x, ev.y)
    c.itemconfig(tag, fill='red')
    # for i in range(len(polyghons)):
    #    if polyghons[i]._id == tag:
    #        pass


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        global c, points, polyghons
        points = []
        polyghons = []
        super().__init__(*args, **kwargs)
        self.title("Geometry visalustion")
        self.geometry("1000x800")

        c = tk.Canvas(self, bg="white", bd=0, highlightthickness=0)
        c.pack(anchor=tk.NW, fill=tk.BOTH, expand=True, padx=5, pady=5)

        keyboard.add_hotkey("z", FlagPoint)
        keyboard.add_hotkey("d", DeletePoints)
        keyboard.add_hotkey("t", Triangularion)
        keyboard.add_hotkey("c", ClearTriangl)
        keyboard.add_hotkey("p", ClearPoints)
        keyboard.add_hotkey("r", lambda x=self: RandomPoints(x))
        c.bind("<Button-3>", addPoint)
        c.bind("<Button-1>", painting)
        # p0 = Point(c, (100, 200))
        # line1 = Line(c, MovePoint(c, (100, 200)),
        #             MovePoint(c, (800, 600)))
        # line2 = Line(c, MovePoint(c, (500, 100)),
        #             MovePoint(c, (100, 400)))
        # circle1 = Circle(c, MovePoint(c, (300, 100)),
        #                 MovePoint(c, (200, 400)))
        # circle2 = Circle(c, MovePoint(c, (400, 500)),
        #                 MovePoint(c, (600, 700)))
        # inter1 = Intersection(c, line1, line2)
        # inter2 = Intersection(c, circle1, line1)
        # inter3 = Intersection(c, circle1, circle2)
        c.tag_raise("point")


if __name__ == '__main__':
    global flag
    flag = False
    win = Window()
    win.mainloop()
