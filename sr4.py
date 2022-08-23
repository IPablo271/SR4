from gl import *
from Obj import *
from Render import *
from vector import *
from texture import *

glCreateWindow(1300, 1300)

glColor(0, 0,0)




scale_factor = (200, 200,200)
translate_factor = (650,500,0)

lmodel('car.obj',scale_factor, translate_factor,'model.bmp')

glFinish()



