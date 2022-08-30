from gl import *
from Obj import *
from Render import *
from vector import *
from texture import *



glCreateWindow(1300, 1300)

glColor(0, 0,0)




scale_factor = (500,500,500)
translate_factor = (550,200,0)
rotatefactor = (0,-(pi/3),0)
createtexture('p.bmp')
lmodel('mimikyu.obj',scale_factor, translate_factor,rotatefactor)

glFinish()
