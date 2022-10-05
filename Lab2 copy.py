import math
from gl import *
from Obj import *
from Render import *
from vector import *
from texture import *


r = Render(1000,1000)
r.current_color = color(0, 255, 255)

def shader1():
    color(255, 0, 0)

scale_factor = (1,1,1)
translate_factor = (0,-0,0)
rotatefactor = (0,(math.pi/5),0)
r.lookAt(V3(0,0,5), V3(0,0,0), V3(0,1,0))
r.texture = Texture('model.bmp')
r.active_shader = shader1
r.load_model('model.obj',scale_factor, translate_factor,rotatefactor)
r.write('pruebalab2.bmp')