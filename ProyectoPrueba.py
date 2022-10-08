import math
from gl import *
from Obj import *
from Render import *
from vector import *
from texture import *


r = Render(600, 486)
background = Texture('Pokemon.bmp')
r.framebuffer = background.pixels

r.lookAt(V3(0,0,5), V3(0,0,0), V3(0,1,0))
r.active_shader = r.shader

r.texture = Texture('p.bmp')
r.load_model('mimikyu.obj',(0.4,0.4,0.4),  (-0.7,-0.8,0),(0,-(math.pi/2),0))
r.draw('TRIANGLES')

r.texture = Texture('pokemonb.bmp')
r.load_model('Pokemon.obj',(0.3,0.3,0.3),  (0.30,-0.8,0),(0,2,0))
r.draw('TRIANGLES')

r.texture = Texture('Mew.bmp')
r.load_model('Mew.obj',(0.15,0.15,0.15),  (0,0,0),(0,0.8,0))
r.draw('TRIANGLES')

r.light = V3(0,0,1)
r.texture = Texture('rockt.bmp')
r.load_model('Rock2.obj',(0.035,0.035,0.035),  (-0.43,-0.21,0),(0,0.5,0))
r.draw('TRIANGLES')

r.light = V3(1,1,1)
r.active_shader = r.shader2
r.texture = Texture('Apple.bmp')
r.load_model('Apple.obj',(0.08,0.08,0.08),  (-0.2,-1,0),(0,0,0))
r.draw('TRIANGLES')




r.write('Proyecto.bmp')

