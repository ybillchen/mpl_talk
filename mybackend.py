import numpy as np

from matplotlib._pylab_helpers import Gcf
from matplotlib.backend_bases import (
     FigureCanvasBase, FigureManagerBase, RendererBase)

def matrix_to_string(matrix):
    return '\n'.join([''.join(['##' if cell == 1 else '  ' for cell in row]) for row in matrix])

class RendererMyBackend(RendererBase):

    def __init__(self, bbox):
        super().__init__()
        points = bbox.get_points().astype(int)
        self.mat = np.zeros((points[1,1]-points[0,1]+1, points[1,0]-points[0,0]+1), dtype=int)

    def draw_path(self, gc, path, transform, rgbFace=None):
        vs = transform.transform(path.vertices)
        x0, y0 = vs[0]
        for x1, y1 in vs[1:]:
            if np.abs(y1 - y0) <= np.abs(x1 - x0):
                a = (y1 - y0) / (x1 - x0)
                i0 = min(int(x0), int(x1))
                i1 = max(int(x0), int(x1))
                for i in range(i0, i1+1):
                    j = int(a * (i-x0) + y0)
                    self.mat[-1-j,i] = 1
            else:
                b = (x1 - x0) / (y1 - y0)
                j0 = min(int(y0), int(y1))
                j1 = max(int(y0), int(y1))
                for j in range(j0, j1+1):
                    i = int(b * (j-y0) + x0)
                    self.mat[-1-j,i] = 1
            x0 = x1
            y0 = y1

    def draw_image(self, gc, x, y, im):
        pass

    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        pass

class FigureManagerMyBackend(FigureManagerBase):
    def show(self):
        print(self.canvas.draw())

class FigureCanvasMyBackend(FigureCanvasBase):
    manager_class = FigureManagerMyBackend

    def draw(self):
        renderer = RendererMyBackend(self.figure.figbbox)
        self.figure.draw(renderer)
        return matrix_to_string(renderer.mat)

    filetypes = {**FigureCanvasBase.filetypes, 'txt': 'TXT File Format'}

    def print_txt(self, filename, *args, **kwargs):
        with open(filename, 'w') as f:
            f.write(self.draw())

    def get_default_filetype(self):
        return 'txt'


FigureCanvas = FigureCanvasMyBackend
FigureManager = FigureManagerMyBackend