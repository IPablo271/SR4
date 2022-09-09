import math
from gl import *
from Obj import *
from Render import *
from vector import *
from texture import *



glCreateWindow(1000, 1000)
glClearColor(0,0,0)
glColor(1, 0,0)





scale_factor = (1,1,1)
translate_factor = (-0.25,-0.7,0)
rotatefactor = (0,-(math.pi/4),0)
glLookAt(V3(0,0,10), V3(0,0,0.5), V3(0.01,0.02,0))
createtexture('p.bmp')
lmodel('mimikyu.obj',scale_factor, translate_factor,rotatefactor)
glFinish('sr6DutchAngle.bmp')
