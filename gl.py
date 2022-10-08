from Render import *
from Utilities import *
from vector import *
import random 
from texture import *

rend = None




def glinit():
    pass

def glCreateWindow(width, height):
    global rend
    if width % 4 == 0:
        rend = Render(width, height)
    else:
        print('No se puede procesar la ventana')

def glViewPort(x, y, height, width):
    global rend 
    # if r.height < height:
    #     print("El height del viewport es mayor a la ventana")
    # elif r.width < width:
    #     print("El width del viewport es mayor a la ventana")
    # elif width + x < r.width:
    #     print("El viewport no se encuentra en la pantalla")
    # elif height + y < r.height:
    #     print("El viewport no se encuentra en la pantalla")
    # else:
    rend.viewport(x, y, width, height)
    for j in range(x,width+x):
        for k in range(y,height+y):
            rend.point(j,k)

    

def  glClear():
    global rend
    rend.clear()
def  glClearColor(r, g, b):
    global rend
    rend.clear_color = color(r, g, b)
    glClear()


def glVertex(x, y):
    global rend
    rend.point(x,y)



def glColor(r, g, b):
    r = round(r * 255)
    g = round(g * 255)
    b = round(b * 255)
    rend.current_color = color(r,g,b)

def createline(x0, y0, x1, y1):
    #Metodo de la linea dentro del viewport
    if x0 >= -1 <= 1 and y0 >= -1 <= 1:
        global rend
        rend.line2(*rend.convertp(x0,y0),*rend.convertp(x1,y1))
    else:
        print("No se puede crear la linea")

def createline2(x0,y0,x1,y1):
    global rend
    rend.line3(x0,y0,x1,y1)



def fillfigure2(puntos):
    listax =[]
    listay =[]
    puntosf = []

    last_point = puntos[-1]
    for point in puntos:
        x = rend.line2(*last_point,*point)
        last_point = point
        puntosf += x
    
    for i in range(len(puntos)):
        listax.append(puntos[i][0])
        listay.append(puntos[i][1])

    maxx = max(listax) + 1
    minx = min(listax)
    maxy = max(listay) + 1
    miny = min(listay)
    disx = maxx - minx
    disy = maxy - miny
    puntomx = minx + round(disx/2)
    puntomy = miny + round(disy/2)


    for i in range(len(puntosf)):
        puntox = puntosf[i][0]
        puntoy = puntosf[i][1]
        rend.line2(puntomx, puntomy, puntox,puntoy)

def lmodel(model,scale_factor , translate_factor,rotatefactor):
    global rend
    rend.load_model(model,scale_factor,translate_factor,rotatefactor)

def createvector(v1,v2):
    global rend
    rend.linevector(v1,v2)

def createtexture(textura):
    global rend
    rend.texture = Texture(textura)

def glLookAt(eye,center,up):
    global rend
    rend.lookAt(eye,center,up)

def glactiveshader():
    global rend
    rend.active_shader = rend.shader


   
def gldraw(Triangles):
    global rend
    rend.draw(Triangles)

def glloadBackground(textura):
    global rend
    backgorund = Texture(textura)
    rend.framebuffer = backgorund.pixels


def glFinish(archivo):
    rend.write(archivo) 




