import math
from gl import *
from Obj import *
from Render import *
from vector import *
from texture import *




glCreateWindow(600, 486)
glClearColor(0,0,0)
glColor(1, 0,0)
glloadBackground('Pokemon.bmp')


# scale_factor = (0.5,0.5,0.5)
# translate_factor = (-0.7,-0.8,0)
# rotatefactor = (0,-(math.pi/2),0)

glactiveshader()
glLookAt(V3(0,0,5), V3(0,0,0), V3(0,1,0))

createtexture('p.bmp')
lmodel('mimikyu.obj',(0.5,0.5,0.5),  (-0.7,-0.8,0),(0,-(math.pi/2),0))

createtexture('pokemonb.bmp')
lmodel('Pokemon.obj',(0.4,0.4,0.4),  (0.2,-1,0),(0,2,0))



gldraw('TRIANGLES')

glFinish('lab2.bmp')