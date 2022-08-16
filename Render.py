
from Utilities import * 
from Obj import *
from vector import *
import random
BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)
GREEN = color(0, 255 , 0)

class Render(object):
   
    def __init__(self,width, height):
        self.width = width
        self.height = height
        self.current_color = BLACK
        self.clear_color = WHITE
        self.viewportx = 0
        self.viewporty = 0
        self.viewportwidth = 0
        self.viewortheight = 0
        self.viewportcolor = GREEN
        self.clear() #Limpiar la pantalla.
    def viewport(self,x, y,width,height):
        self.viewportx = x
        self.viewporty = y
        self.viewportwidth = width
        self.viewortheight = height
   
    def clear(self):
        #Generador del color.
        self.framebuffer = [
            #Los colores tienen que ir de 0 a 255.
            [BLACK for x in range(self.width)] 
            for y in range(self.height)
        ]
        self.zbuffer = [
            #Los colores tienen que ir de 0 a 255.
            [-9999 for x in range(self.width)] 
            for y in range(self.height)
        ]
        self.zcolor = [
            [BLACK for x in range(self.width)]
            for y in range(self.height)
        ]

    
    def write(self, filename):
        #Esta no necesita recibir ningún nombre de archivo.
        #Abrir en bw: binary write.
        f = open(filename, "bw")
        
        #Pixel header.
        f.write(char('B'))
        f.write(char('M'))
        #Tamaño del archivo en bytes. 
        # El 3 es para los 3 bytes que seguirán. El 14 es el tamaño del infoheader y el 40 es el tamaño del otro header.
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(word(0)) #Algo que no se usará. Este es de 2 bytes, por eso se utiliza el word.
        f.write(word(0)) #Algo que no se usará. Este es de 2 bytes, por eso se utiliza el word.
        f.write(dword(14 + 40)) #Offset a la información de la imagen. 14 bytes para el header, 40 para la información de la imagen. Aquí empieza la data.
        #Lo anterior suma 14 bytes.
        
        #Info header.
        f.write(dword(40)) #Este es el tamaño del header. Esto es de 4 bytes, por eso se utiliza el dword.
        f.write(dword(self.width)) #Ancho de la imagen. Esto es de 4 bytes, por eso se utiliza el dword.
        f.write(dword(self.height)) #Alto de la imagen. Esto es de 4 bytes, por eso se utiliza el dword.
        f.write(word(1)) #Número de planos. Esto es de 2 bytes, por eso se utiliza el word.
        f.write(word(24)) #24 bits por pixel. Esto es porque usa el true color y el RGB.
        f.write(dword(0)) #Esto es la compresión. Esto es de 4 bytes, por eso se utiliza el dword.
        f.write(dword(self.width * self.height * 3)) #Tamaño de la imagen sin el header.
        #Pixels que no se usarán mucho.
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        #Lo anterior suma 40 bytes.

        
        
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[y][x])
        f.close()

    def writez(self, filename):
        #Esta no necesita recibir ningún nombre de archivo.
        #Abrir en bw: binary write.
        f = open(filename, "bw")
        
        #Pixel header.
        f.write(char('B'))
        f.write(char('M'))
        #Tamaño del archivo en bytes. 
        # El 3 es para los 3 bytes que seguirán. El 14 es el tamaño del infoheader y el 40 es el tamaño del otro header.
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(word(0)) #Algo que no se usará. Este es de 2 bytes, por eso se utiliza el word.
        f.write(word(0)) #Algo que no se usará. Este es de 2 bytes, por eso se utiliza el word.
        f.write(dword(14 + 40)) #Offset a la información de la imagen. 14 bytes para el header, 40 para la información de la imagen. Aquí empieza la data.
        #Lo anterior suma 14 bytes.
        
        #Info header.
        f.write(dword(40)) #Este es el tamaño del header. Esto es de 4 bytes, por eso se utiliza el dword.
        f.write(dword(self.width)) #Ancho de la imagen. Esto es de 4 bytes, por eso se utiliza el dword.
        f.write(dword(self.height)) #Alto de la imagen. Esto es de 4 bytes, por eso se utiliza el dword.
        f.write(word(1)) #Número de planos. Esto es de 2 bytes, por eso se utiliza el word.
        f.write(word(24)) #24 bits por pixel. Esto es porque usa el true color y el RGB.
        f.write(dword(0)) #Esto es la compresión. Esto es de 4 bytes, por eso se utiliza el dword.
        f.write(dword(self.width * self.height * 3)) #Tamaño de la imagen sin el header.
        #Pixels que no se usarán mucho.
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        #Lo anterior suma 40 bytes.

        
        
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.zcolor[y][x])
        f.close()
    


    #Función que dibuja un punto en la pantalla. Esta es una función de bajo nivel. 
    def point(self, x, y): 
        if (0 < x < self.width and 0 < y < self.height):
            self.framebuffer[x][y] = self.current_color #El color del punto es el color actual.      
    

    def convertp(self,x,y):
        x_ini = x + 1
        y_ini = y + 1

        # calculada = (Sumada * width) / numero sumado

        calcux = (x_ini * self.viewportwidth) / 2
        calcuy = (y_ini * self.viewortheight) / 2

        #  xfinal = (coordenada inicial del viewport + calculada )
        xfinal = round(self.viewportx + calcux)
        yfinal = round(self.viewporty + calcuy)

        return [xfinal , yfinal]
    
    def line2(self, x0,y0,x1,y1):
        listap = []
        x0 = round(x0)
        y0 = round(y0)
        x1 = round(x1)
        y1 = round(y1)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        # Si es empinado, poco movimiento en x y mucho en y.
        steep = dy > dx

        # Se invierte si es empinado
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # Si la linea tiene direccion contraria, invertir
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 -y0)
        dx = x1 - x0

        offset = 0
        threshold = dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.point(y, x)
                listatemp = []
                listatemp.append(y)
                listatemp.append(x)
                listap.append(listatemp)

            else:
                self.point(x, y)
                listatemp = []
                listatemp.append(x)
                listatemp.append(y)
                listap.append(listatemp)


            offset += dy * 2

            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += dx * 2
        return listap
    def linevector(self, v1,v2):
        x0 = round(v1.x)
        y0 = round(v1.y)
        x1 = round(v2.x)
        y1 = round(v2.y)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        # Si es empinado, poco movimiento en x y mucho en y.
        steep = dy > dx

        # Se invierte si es empinado
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # Si la linea tiene direccion contraria, invertir
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        threshold = dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.point(y, x)
            else:
                self.point(x, y)

            offset += dy * 2

            if offset >= threshold:
                y += 1 if y0 < y1 else -1

                threshold += dx * 2
    def transform_vertex(self,vertex,scale,translate):
        return V3(
            (vertex[0] * scale[0]) + translate[0], 
            (vertex[1] * scale[1]) + translate[1],
            (vertex[2] * scale[2] +  translate[2]) 
        )
    def load_model(self, model, scale_factor, translate_factor):

        cube = Obj(model)

        for face in cube.faces:
            if len(face) == 4:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                v1 = self.transform_vertex (cube.vertices[f1], scale_factor , translate_factor)
                v2 = self.transform_vertex (cube.vertices[f2], scale_factor , translate_factor)
                v3 = self.transform_vertex (cube.vertices[f3], scale_factor , translate_factor)
                v4 = self.transform_vertex (cube.vertices[f4], scale_factor , translate_factor)




                self.trianglem(v1,v2, v3)
                self.trianglem(v1,v3, v4)

            if len(face) == 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                v1 = self.transform_vertex (cube.vertices[f1], scale_factor , translate_factor)
                v2 = self.transform_vertex (cube.vertices[f2], scale_factor , translate_factor)
                v3 = self.transform_vertex (cube.vertices[f3], scale_factor , translate_factor)


                self.trianglem(v1, v2, v3)
    
    def bounding_box(self, A, B, C):
        coords = [(A.x, A.y), (B.x, B.y), (C.x, C.y)]
    
        xmin = float('inf')
        xmax = float('-inf')
        ymin = float('inf')
        ymax = float('-inf')

        for (x,y) in coords:
            if x < xmin:
                xmin = x
            if x > xmax:
                xmax = x
            if y < ymin:
                ymin = y
            if y > ymax:
                ymax = y

        return V3(xmin, ymin), V3(xmax, ymax)

    
    def cross(self,v1,v2):

        return (
                v1.y * v2.z - v1.z * v2.y,
                v1.z * v2.x - v1.x * v2.z,
                v1.x * v2.y - v1.y * v2.x
            )
    def barycentric(self, A, B, C , P):
        cx, cy , cz = self.cross(
            V3(B.x - A.x, C.x - A.x, A.x - P.x),
            V3(B.y - A.y, C.y - A.y, A.y - P.y)
        )
        try:
            u = cx / cz
            v = cy / cz
            w = 1 - (u + v)
            return(w ,v ,u)
        except:
            u = - 1
            v = - 1
            w = 1 - u - v
            return (w, v , u)


        

        

    def trianglem(self, A , B , C):
        

        L = V3(0, 0, -1)
        N = (C - A) * (B - A)
        i = L.normalize() @ N.normalize()

        if i < 0:
            return

        self.current_color = color(
            round(255 * i ), 
            round(255 * i ), 
            round(255 * i )
        )



        Bmin, Bmax = self.bounding_box(A, B, C)
        for x in range(round(Bmin.x), round(Bmax.x + 1)):
            for y in range(round(Bmin.y), round(Bmax.y + 1)):
                w, v, u = self.barycentric(A, B, C, V3(x,y))
                if (w < 0 or v < 0 or u < 0) :
                    continue
                z = A.z * w + B.z * v + C.z * u

                fact = z/self.width
                if (self.zbuffer[x][y] < z):
                    self.zbuffer[x][y] = z
                    self.zcolor[x][y] = color(self.clamping(fact*255), self.clamping(fact*255), self.clamping(fact*255))

                    self.point(x, y)
        
 

    def clamping(self, num):
        return int(max(min(num, 255), 0))

    def triangle(self, A , B , C):
        if A.y > B.y:
            A, B = B, A
        if A.y > C.y:
            A, C = C, A
        if B.y > C.y:
            B, C = C, B
        
        self.current_color = color(
            random.randint(0,255),
            random.randint(0,255),
            random.randint(0,255)
        )

        dx_ac = C.x - A.x
        dy_ac = C.y - A.y

        if dy_ac == 0:
            return 

        mi_ac = dx_ac / dy_ac

        dx_ab = B.x - A.x
        dy_ab = B.y - A.y
        
        if dy_ab != 0:
            mi_ab = dx_ab / dy_ab
            for y in range(round(A.y), round(B.y + 1)):
                xi = round(A.x - mi_ac * (A.y - y))
                xf = round(A.x - mi_ab * (A.y - y))
                if xi > xf:
                    xi, xf = xf, xi
            
                for x in range(xi,xf+1):
                    self.point(x,y)

        dx_bc = C.x - B.x
        dy_bc = C.y - B.y

        if dy_bc != 0:
            mi_bc = dx_bc / dy_bc
            for y in range(round(B.y), round(C.y + 1)):
                xi = round(A.x - mi_ac * (A.y - y))
                xf = round(B.x - mi_bc * (B.y - y))

                if xi > xf:
                    xi, xf = xf, xi

                for x in range(xi,xf+1):
                    self.point(x,y)
    
    