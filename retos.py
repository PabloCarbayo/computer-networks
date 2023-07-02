#!/usr/bin/python3
# -- coding: utf -8; mode:python --
from socket import *
import hashlib, base64,re, struct, sys, array

#RETO 0 - Conectarse al servidor

def Reto0():
    #Creamos el socket y lo conectamos a la dirección adecuada
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(("yinkana",2000))
    #Recibimos el mensaje y lo imprimimos
    print(sock.recv(1024).decode())
    #Enviamos nuestro nombre
    sock.send("dreamy_antonelli".encode())
    #Recibimos el mensaje de respuesta
    mensaje = sock.recv(1024).decode()
    print(mensaje)
    #Cerramos el socket
    sock.close()
    return mensaje

#RETO 1 - UDP

def Reto1(id1): #UDP
    #Creamos el socket para el reto y lo bindeamos al puerto 1000
    sock = socket(AF_INET,SOCK_DGRAM)
    sock.bind(('',1000))
    #Creamos el mensaje concatenando el puerto utilizado por el socket y el id recibido
    puertoElejido = "1000 "
    cadenaParaEnviar = puertoElejido + id1
    #Enviamos el mensaje, recibimos el reto y lo imprimimos
    sock.sendto(cadenaParaEnviar.encode(),("yinkana",4000))
    mensajeRecibido, server = sock.recvfrom(3000)
    print(mensajeRecibido.decode())
    #Enviamos el identificador en mayúsculas
    id0Upper = id1.upper()
    sock.sendto(id0Upper.encode(),server)
    siguienteReto=recibirReto(sock)
    return siguienteReto


# RETO 2 - CONTADOR DE NÚMEROS

def Reto2(id2):
    #Creamos el socket y lo conectamos a la dirección adecuada
    sock=socket(AF_INET,SOCK_STREAM)
    sock.connect(('yinkana',3000))
    #Inicializamos las variables que utilizaremos
    salir=False
    mensaje=bytes()
    mem=''
    codigo=''
    contador=0
    #Bucle para recibir los números
    while salir==False:
        mensaje=sock.recv(2048)
        mem=mensaje.decode()
        aux=mem.split()
        codigo=codigo+mem
        #Recorremos la substring recibida en busca del 0 para dejar de recibir números
        for i in aux:
            if i == '0':
                salir=True
                break
    
    v=codigo.split()
    #Recorremos la cadena que hemos recibido contando los números hasta encontrar el 0
    for x in range(0,len(v)):
        if v[x]=="0":
            break
        else:
            contador+=1
    #Formamos el mensaje y lo enviamos
    enviar=id2+" "+str(contador)
    sock.send(enviar.encode())
    #Recibimos el siguiente reto 
    siguienteReto=recibirReto(sock)
    return siguienteReto
            
    
#RETO 3 - YUMMY!
def Reto3(id3):

    #Creamos el socket y lo conectamos a la dirección adecuada
    sock = socket(AF_INET, SOCK_STREAM) 
    sock.connect(('yinkana', 3060))

    #Inicializamos las variables que utilizaremos
    mensajeRecibido=bytes()
    mem=''
    codigo=''
    mensajeFinal=''
    maxIteracones = 5
    iteracion = 0
    #Bucle para recibir el mensaje que hará como máximo 5 iteraciones
    while (iteracion < maxIteracones):
        mensajeRecibido = sock.recv(1024)   
        mem = mensajeRecibido.decode()
        codigo=codigo+mem
        iteracion = iteracion + 1
    #Separamos la cadena recibida en un vector
    v=codigo.split(" ")
    #Recorremos el vector en busca de la longitud de la cadena a enviar
    for subcadena in v:
        if not ":" in subcadena:
            longitud = int(subcadena)
            break
        
    vAux = [None] * longitud #Vector vacío de longitud "longitud"
    #Recorremos el vector en busca de las palabras y sus posiciones
    for subcadena in v:
        if "[" in subcadena:
            break
        if ":" in subcadena:
            palabra, posicion = subcadena.split(":")
            posicion = int(posicion)
            if posicion <= longitud:
                vAux[posicion-1] = palabra
    #Recorremos el vector para formar el mensaje final
    for palabra in vAux:
        mensajeFinal= mensajeFinal + palabra + " "
        
    # Construimos el mensaje de respuesta
    response = id3 +" "+ mensajeFinal + "--"
    # Enviamos el mensaje de respuesta al servidor
    response = response.encode()
    sock.sendall(response)
    #Recibimos el siguiente reto
    siguienteReto=recibirReto(sock)
    return siguienteReto    

#RETO 4 - MD5

def Reto4(id4):
    
    #Creamos el socket y lo conectamos a la dirección adecuada
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('yinkana',9000))
    
    #Enviamos el identificador
    sock.send(id4.encode())
    
    longitud=''
	#Recibimos la longitud del archivo
    while 1:
        data = sock.recv(1)
        aux=data.decode()
        if(aux==":"):
            break
        longitud=longitud+aux
    
    #Convertimos la longitud a entero
    numero=int(longitud)
    contador = 0
    archivo=bytes()
    
    #Formamos el archivo
    while 1:
        if(contador>=numero):
            break
        data = sock.recv(1024)
        archivo=archivo+data
        contador=contador+len(data)
    
    #Calculamos el hash del archivo y lo enviamos
    h=hashlib.new('md5',archivo)
    envio=h.digest()
    sock.send(envio)
    
    #Recibimos el siguiente reto
    siguienteReto=recibirReto(sock)
    return siguienteReto
    
#RETO 5 - YAP

def Reto5(id5):
    # Creamos el socket UDP
    sock = socket(AF_INET, SOCK_DGRAM)
    
    # Codificamos el identificador en base64
    yap="YAP".encode()

    payload = base64.b64encode(id5.encode())
    cabecera = struct.pack('!3sHBHH', yap, 0, 0, 0, 1)
    checksum = cksum(cabecera + payload)
    cabecera = struct.pack('!3sHBHH', yap, 0, 0, checksum, 1)
    envio=cabecera+payload

    # Enviamos el datagrama
    sock.sendto(envio, ('yinkana', 6001))
    
    #Recibimos el enunciado del siguiente reto
    enunciado,aux = sock.recvfrom(5000)
    enunciadoDecode = (base64.b64decode(enunciado[10:]+b'====')).decode()
    print(enunciadoDecode)
    
    sock.close()
    
    return enunciadoDecode
    


#Método principal
def main():

    r1 = Reto1(identificador(Reto0()))
    r2 = Reto2(identificador(r1))
    r3 = Reto3(identificador(r2))
    r4 = Reto4(identificador(r3))
    r5 = Reto5(identificador(r4))

#Método para extraer el identificador del reto  
def identificador(cadena):
    id =''
    inicio = 0
    for i in cadena:
        if i == ":":
            inicio = 1
        if i=="\n":
            break
        if inicio == 1 and i!=":":
            id = id + i
    return id  

#Método para recibir el siguiente reto
def recibirReto(socket):
    encontrado=False
    #Bucle para recibir el próximo mensaje
    while encontrado==False:
        m=socket.recv(3072)
        aux=m.decode()
        #Si encontramos ">" significa que hemos completado el reto
        if ">" in aux:
            encontrado=True
    #Imprimimos el mensaje y cerramos el socket
    print(aux)
    socket.close()
    return aux   



'''
    Metodo extraido de:
  https://bitbucket.org/DavidVilla/inet-checksum/src/master/inet_checksum.py
    Copyright (C) David Villa Alises
'''    
def cksum(pkt):
    if len(pkt) % 2 == 1:
        pkt += b'\0'
    s = sum(array.array('H',pkt))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16 
    s = ~s
    if sys.byteorder == 'little':
        s = ((s >> 8) & 0xff) | s << 8
    return s & 0xffff

## Ejecución del programa
main()