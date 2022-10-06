from Utilities import * 
from Obj import *
from vector import *
import random
from texture import *
from matriz import *
import math

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
        self.texture = None
        self.Model = None
        self.View = None
        self.active_shader = None

        self.vertex_array = []
        self.vertex_buffer_object = []

        self.clear() #Limpiar la pantalla.
    def viewport(self,x, y,width,height):
        self.viewportx = x
        self.viewporty = y
        self.viewportwidth = width
        self.viewortheight = height
    
    def loadModelMatrix(self,translatep=(0,0,0), scalep=(1,1,1), rotatep=(0,0,0) ):
        translate = V3(*translatep)
        scale = V3(*scalep)
        rotate = V3(*rotatep)

        translation_matrix = matriz([
            [1, 0, 0, translate.x],
            [0, 1, 0, translate.y],
            [0, 0, 1, translate.z],
            [0, 0, 0,           1]
        ])

        scale_matrix = matriz([
            [scale.x, 0, 0, 0],
            [0, scale.y, 0, 0],
            [0, 0, scale.z, 0],
            [0, 0, 0, 1]
        ])

        a = rotate.x
        rotation_x = matriz([
            [1,      0,       0, 0],
            [0, math.cos(a), -math.sin(a), 0],
            [0, math.sin(a),  math.cos(a), 0],
            [0,      0,       0, 1]
        ])

        a = rotate.y
        rotation_y = matriz([
            [math.cos(a), 0, math.sin(a), 0],
            [0, 1,      0, 0],
            [-math.sin(a), 0, math.cos(a), 0],
            [0, 0,      0, 1]
        ])

        a = rotate.z
        rotation_z = matriz([
            [math.cos(a), -math.sin(a), 0, 0],
            [math.sin(a), math.cos(a), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        rotation_matrix = rotation_x * rotation_y * rotation_z

        self.Model = translation_matrix * rotation_matrix * scale_matrix

    
    def loadViewMatrix(self, x, y, z, center):
        Mi = matriz([
            [x.x, x.y, x.z, 0],
            [y.x, y.y, y.z, 0],
            [z.x, z.y, z.z, 0],
            [0, 0, 0, 1],
        ])
        Op = matriz([
            [1, 0, 0, -center.x],
            [0, 1, 0, -center.y],
            [0, 0, 1, -center.z],
            [0, 0, 0,         1]
        ])

        self.View = Mi * Op
    def loadProjectionMatrix(self, eyes, center):
        coeff = -1/(eyes.length() - center.length())
        self.Projection = matriz([
            [1, 0,      0, 0],
            [0, 1,      0, 0],
            [0, 0,      1, 0],
            [0, 0, coeff, 1]
        ])
    def loadViewportMatrix(self):
        x = 0
        y = 0
        w = self.width/2
        h = self.height/2
        self.Viewportmatrix = matriz([
            [w, 0,   0, x + w],
            [0, h,   0, y + h],
            [0, 0, 128,   128],
            [0, 0,   0,     1]
        ])
    
    
    
    def lookAt(self,eye,center,up):

        z = (eye - center).normalize()
        x = (up * z).normalize()
        y = (z * x).normalize()
        self.loadViewMatrix(x, y, z, center)
        self.loadProjectionMatrix(eye, center)
        self.loadViewportMatrix()


   
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
        f.write(chart('B'))
        f.write(chart('M'))
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

        
        
        for y in range(self.height):
            for x in range(self.width):
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
                self.point(x, y)
                listatemp = []
                listatemp.append(y)
                listatemp.append(x)
                listap.append(listatemp)

            else:
                self.point(y, x)
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
                self.point(x, y)
            else:
                self.point(y, x)

            offset += dy * 2

            if offset >= threshold:
                y += 1 if y0 < y1 else -1

                threshold += dx * 2
    def transform_vertex(self,vertex):
        augmented_vertex = matriz([
            [vertex[0]],
            [vertex[1]],
            [vertex[2]],
            [1]
        ])
        if(self.View and self.Projection):
            transformed_vertex = (self.Viewportmatrix * self.Projection *
                                  self.View * self.Model * augmented_vertex).matriz
        else:
            transformed_vertex = (self.Model * augmented_vertex).matriz

        return V3(
            transformed_vertex[0][0] / transformed_vertex[3][0],
            transformed_vertex[1][0] / transformed_vertex[3][0],
            transformed_vertex[2][0] / transformed_vertex[3][0],
        )

    def load_model(self, model, scale_factorn =(1,1,1), translate_factor=(0,0,0),rotate=(0,0,0)):
        self.loadModelMatrix(translate_factor,scale_factorn,rotate)
        cube = Obj(model)

        for face in cube.faces:

            if len(face) == 4:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                v1 = self.transform_vertex (cube.vertices[f1] )
                v2 = self.transform_vertex (cube.vertices[f2] )
                v3 = self.transform_vertex (cube.vertices[f3] )
                v4 = self.transform_vertex (cube.vertices[f4] )


                self.vertex_buffer_object.append(v1)
                self.vertex_buffer_object.append(v2)
                self.vertex_buffer_object.append(v3)
                self.vertex_buffer_object.append(v4)



                if self.texture and len(cube.tvertices) !=0:
                    ft1 = face[0][1] - 1
                    ft2 = face[1][1] - 1
                    ft3 = face[2][1] - 1
                    ft4 = face[3][1] - 1

                    vt1 = V3(*cube.tvertices[ft1])
                    vt2 = V3(*cube.tvertices[ft2])
                    vt3 = V3(*cube.tvertices[ft3]) 
                    vt4 = V3(*cube.tvertices[ft4])

                    self.vertex_buffer_object.append(vt1)
                    self.vertex_buffer_object.append(vt2)
                    self.vertex_buffer_object.append(vt3)
                    self.vertex_buffer_object.append(vt4)
                
                # f1n = face[0][2] - 1
                # f2n = face[1][2] - 1
                # f3n = face[2][2] - 1
                # f4n = face[3][2] - 1

                # fn1 = V3(*cube.nvertices[f1n])
                # fn2 = V3(*cube.nvertices[f2n])
                # fn3 = V3(*cube.nvertices[f3n])
                # fn4 = V3(*cube.nvertices[f4n])

                # self.vertex_buffer_object.append(fn1)
                # self.vertex_buffer_object.append(fn2)
                # self.vertex_buffer_object.append(fn3)
                # self.vertex_buffer_object.append(fn3)


                
                    

            if len(face) == 3 and len(cube.tvertices) != 0:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                v1 = self.transform_vertex (cube.vertices[f1])
                v2 = self.transform_vertex (cube.vertices[f2])
                v3 = self.transform_vertex (cube.vertices[f3])

                self.vertex_buffer_object.append(v1)
                self.vertex_buffer_object.append(v2)
                self.vertex_buffer_object.append(v3)
    

                if self.texture :
                    ft1 = face[0][1] - 1
                    ft2 = face[1][1] - 1
                    ft3 = face[2][1] - 1

                    vt1 = V3(*cube.tvertices[ft1])
                    vt2 = V3(*cube.tvertices[ft2])
                    vt3 = V3(*cube.tvertices[ft3])

                    self.vertex_buffer_object.append(vt1)
                    self.vertex_buffer_object.append(vt2)
                    self.vertex_buffer_object.append(vt3)

                # f1n = face[0][2] - 1
                # f2n = face[1][2] - 1
                # f3n = face[2][2] - 1
    
                # fn1 = V3(*cube.nvertices[f1n])
                # fn2 = V3(*cube.nvertices[f2n])
                # fn3 = V3(*cube.nvertices[f3n])
    

                # self.vertex_buffer_object.append(fn1)
                # self.vertex_buffer_object.append(fn2)
                # self.vertex_buffer_object.append(fn3)

    def triangle_wireframe(self):
        A = next(self.vertex_array)
        B = next(self.vertex_array)
        C = next(self.vertex_array)

        if self.texture:
            tA = next(self.vertex_array)
            tB = next(self.vertex_array)
            tC = next(self.vertex_array)

        self.linevector(A, B)
        self.linevector(B, C)
        self.linevector(C, A)

                
    def draw(self, polygon):
            self.vertex_array = iter(self.vertex_buffer_object)

            if polygon == 'TRIANGLES':
                try:
                    while True:
                        print("Entro al trianglem")
                        self.trianglem()
                except StopIteration:
                    print('Done.')

            if polygon == 'WIREFRAME':
                try:
                    while True:
                        self.triangle_wireframe()
                except StopIteration:
                    print(" done . ")
        
    
    
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



    def trianglem(self):
        A = next(self.vertex_array)
        B = next(self.vertex_array)
        C = next(self.vertex_array)


        if self.texture:
            tA = next(self.vertex_array)
            tB = next(self.vertex_array)
            tC = next(self.vertex_array)
        

        
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
                if (
                    x >= 0 and
                    y >= 0 and
                    x < len(self.zbuffer) and 
                    y < len(self.zbuffer[0]) and self.zbuffer[x][y] < z):
                    self.zbuffer[x][y] = z
                    self.zcolor[x][y] = color(self.clamping(fact*255), self.clamping(fact*255), self.clamping(fact*255))

                    if(self.active_shader):
                        self.current_color = self.shader(self)

                    else:
                        if self.texture:
                            tx = tA.x * w + tB.x * u + tC.x * v
                            ty = tA.y * w + tB.y * u + tC.y * v
                            self.current_color = self.texture.get_color_with_intensity(tx,ty,i)

                    self.point(y, x)
        
 

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

    def shader():
        return color(255, 0, 0)
       
            #return render.texture.get_color_with_intensity(tx, ty, intensity)



    
    