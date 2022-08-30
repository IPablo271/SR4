import struct
def chart(c):
    #Ocupa 1 byte.
    #=c es para que sea un caracter. El encode es para convertir el caracter a bits. El =c es para convertir esos bits a bytes.
    return struct.pack("=c", c.encode('ascii'))

#Recibe un número como parámetro.
def word(w):
    #Ocupa 2 bytes.
    #El formato para un word es 'h'. Este gasta 2 bytes, que es lo que se quiere.
    return struct.pack("=h", w)

#Recibe un número como parámetro.
def dword(d): #Double word.
    #Ocupa 4 bytes. El l es para un num de 4 bytes.
    return struct.pack("=l", d)

def color(r, g, b): #Función que crea el color.
    #3 bytes. Retorna el color en bytes.
    return bytes([b, g, r])
