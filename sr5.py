from gl import *
from Obj import *
from Render import *
from vector import *
from texture import *



r = Render(1024, 1024)
t = Texture('p.bmp')
r.framebuffer = t.pixels

cube = Obj('mimikyu.obj')
for face in cube.faces:
    if len(face) == 4:
        f1 = face[0][1] - 1
        f2 = face[1][1] - 1
        f3 = face[2][1] - 1
        f4 = face[3][1] - 1

        vt1 = V3(
            cube.tvertices[f1][0] * t.width,
            cube.tvertices[f1][1] * t.height,

        )
        vt2 = V3(
            cube.tvertices[f2][0] * t.width,
            cube.tvertices[f2][1] * t.height,

        )
        vt3 = V3(
            cube.tvertices[f3][0] * t.width,
            cube.tvertices[f3][1] * t.height,

        )
        vt4 = V3(
            cube.tvertices[f4][0] * t.width,
            cube.tvertices[f4][1] * t.height,
        )
        r.linevector(vt1, vt2)
        r.linevector(vt2, vt3)
        r.linevector(vt3, vt4)
        r.linevector(vt4, vt1)

    
    if len(face) == 3:
        f1 = face[0][1] - 1
        f2 = face[1][1] - 1
        f3 = face[2][1] - 1

        vt1 = V3(
            cube.tvertices[f1][0] * t.width,
            cube.tvertices[f1][1] * t.height,

        )
        vt2 = V3(
            cube.tvertices[f2][0] * t.width,
            cube.tvertices[f2][1] * t.height,

        )
        vt3 = V3(
            cube.tvertices[f3][0] * t.width,
            cube.tvertices[f3][1] * t.height,

        )
        r.linevector(vt1, vt2)
        r.linevector(vt2, vt3)
        r.linevector(vt3, vt1)

r.write('triangulos_textura.bmp')

glCreateWindow(1300, 1300)

glColor(0, 0,0)




scale_factor = (500, 500,500)
translate_factor = (650,200,0)
createtexture('p.bmp')
lmodel('mimikyu.obj',scale_factor, translate_factor)

glFinish()

