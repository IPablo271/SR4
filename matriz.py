from vector import *
class matriz(object):
    def __init__(self, matriz):
        self.matriz = matriz

    def __mul__(self, other):
        try:

            if(type(other) == V3):
                other = matriz([[other.x], [other.y], [other.z], [other.w]])

            matrizf = []
            for x in range(len(self.matriz)):
                matrizf.append([])
                for y in range(len(other.matriz[0])):
                    matrizf[x].append([])
                    temp = 0
                    for k in range(len(other.matriz)):
                        temp += self.matriz[x][k] * other.matriz[k][y]
                    matrizf[x][y] = temp
            return matriz(matrizf)

        except:
            print("No se pudo realizar la multiplicaicon")

    def __repr__(self):
        return "matriz" + self.matriz