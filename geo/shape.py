class Shape:
    def __init__(self, canvas):
        self._depended = []
        self._c = canvas

    def __del__(self):
        self._c.delete(self._id)

    def redraw(self):
        pass

    def update(self):
        self.redraw()
        for d in self._depended:
            d.update()

    def add_dependency(self, shape):
        self._depended.append(shape)