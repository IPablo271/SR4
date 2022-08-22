import struct
from Utilities import *
from Render import *
from Obj import *
from vector import *
class Texture:
    def __init__(self, path):
        self.path = path
        self.read()
    
    def read(self):
        with open(self.path, 'rb') as image:
            image.seek(10)
            header_size = struct.unpack('=l', image.read(4))[0]
            image.seek(18)
            self.width = struct.unpack('=l', image.read(4))[0]
            self.height = struct.unpack('=l', image.read(4))[0]
            image.seek(header_size)

            self.pixels = []

            for y in range(self.height):
                self.pixels.append([])
                for x in range(self.width):
                    b = ord(image.read(1))
                    g = ord(image.read(1))
                    r = ord(image.read(1))
                    self.pixels[y].append(
                        color(r,g,b)
                    )

    def get_color_with_intensity(self, tx, ty, intensity):
        x = round(tx * self.width)
        y = round(ty * self.height)

        b = self.pixels[y][x][0] * intensity
        g = self.pixels[y][x][1] * intensity
        r = self.pixels[y][x][2] * intensity
        
        return color(r,g,b)

r = Render(1024, 1024)
t = Texture('model.bmp')
r.framebuffer = t.pixels

cube = Obj('model.obj')
for face in cube.faces:
    if len(face) == 3:
        f1 = face[0][1] - 1
        f2 = face[1][1] - 1
        f3 = face[2][1] - 1

        vt1 = V3(
            cube.vertices[f1][0] * t.width,
            cube.vertices[f1][1] * t.height,

        )
        vt2 = V3(
            cube.vertices[f2][0] * t.width,
            cube.vertices[f2][1] * t.height,

        )
        vt3 = V3(
            cube.vertices[f3][0] * t.width,
            cube.vertices[f3][1] * t.height,

        )
        r.linevector(vt1, vt2)
        r.linevector(vt2, vt3)
        r.linevector(vt3, vt1)

r.write('t.bmp')


