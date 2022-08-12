import struct
from Render import *
class Texture:
    def __init__(self,path):
        self.path = path
        self.pixels = []
    
    def read(self):
        with open(self.path, "rb") as image:
            image.seek(10)
            image.read(4)
            header_size = struct.unpack('=l', image.read(4))[0]
            image.seek(18)
            self.width = struct.unpack('=l', image.read(4))[0]
            self.height = struct.unpack('=l', image.read(4))[0]
            image.seek(header_size)
            

            for y in range(self.heightS):
                self.pixels.append([])
                for x in range(self.width):
                    b = ord(image.read(1))
                    g = ord(image.read(1))
                    r = ord(image.read(1))
                    self.pixels[y].append(
                        color(r, g, b)
                    )
    
    def get_color(self,tx, ty):
        x = round(tx * self.width)
        y = round(ty * self.height)

        return self.pixels[y][x]
    
    def get_color_with_intensity(self, tx, ty, intensity):
        x = round(tx * self.width)
        y = round(ty * self.height)
        
        b = self.pixels[y][x][0] * intensity
        g = self.pixels[y][x][1] * intensity
        r = self.pixels[y][x][2] * intensity

        return color(r, g, b)

r = Render(1024,1024)
t = Texture('model2.obj')

r.framebuffer = t.pixels
r.write('prueba.bmp')



