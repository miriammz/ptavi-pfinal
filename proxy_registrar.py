#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import SocketServer
import sys
import os
import time
import socket


def MensajesLog(mensaje):
    mensaje = mensaje.split("")
    fich = open(cHandler.log_path, "a")
    for cont in mensaje:
        msg = str(time.time()) + " " + str(cont) + " " + "\n"
    fich.write(msg)
    fich.close()


class ProxyHandler(ContentHandler):

    def __init__(self):
        self.etiquetas = {
            "server": ["name", "ip", "puerto"],
            "database": ["path", "passwdpath"],
            "log": ["path"],
        self.lista = []

    def startElement(self, etiqueta, atributo):
        if etiqueta in self.etiquetas:
            dic = {}
            for attr in self.etiquetas[etiqueta]:
                dic[attr] = (atributo.get(attr, ""))
            self.lista.append([etiqueta, dic])

    dicc = {}


class ProxyRegistrar(SocketServer.DatagramRequestHandler):

    def register2file(self):
            fich = open(cHandler.database_path, "a")
            fich.write("User\tIP\tPuerto\tExpires\n")
            for cliente in self.dicc.items():
                hora = time.strftime('%Y-­%m-­%d %H:%M:%S',
                             time.gmtime(time.time()))
                fich.write(cliente + '\t' + IP + '\t' +  PUERTO + '\t' + hora)
            fich.close()

    def handle(self):
        line = self.rfile.read()
        line2 = line.split(" ")
        line3 = line2.split(":")
        IP = str(self.client_address[0])
        cliente = line2[1].split(":")[1]
        PUERTO = str(line2[1].split(":")[2])
        EXPIRES = line3[3]
        tiempo = time.time() + int(EXPIRES)
        hora_actual = time.time()
        #IP_server =
        #PUERTO_server =
        self.my_socket.connect((ip_server, puerto_server)
"""
self.my_socket.send(reenviar)

ip_server :  este dato lo obtengo de la información SDP del invite

puerto_server : puedo obtenerlo del mensaje Register

reenviar = mensaje INVITE+SDP recibido por el cliente


2. ip_server y puerto_server los obtienes de un registro anterior del receptor
del INVITE. Si no está registrado, hay que devolver un 404.
"""
        print "El cliente nos manda " + line

        if line2[0] == "REGISTER":
            registrado = "Received from " + IP + ":" + PUERTO + ": REGISTER"
            MensajesLog(registrado)
            self.wfile.write("SIP/2.0 200 OK" + '\r\n\r\n')
            enviado = "Sent to " + IP + ":" + PUERTO ": 200 OK"
            MensajesLog(enviado)
            if EXPIRES == 0:
                if cliente in self.dicc:
                    # borramos al usuario
                    del self.dicc[cliente]
                    self.register2file()
            else:
                self.dicc[cliente] = IP + ", " + str(tiempo)
                register2file(cliente)

            for elemento, valor in self.dicc.items():
                hora = valor.split(",")[-1]
                if hora_actual > hora:
                    del self.dicc[elemento]
                    self.register2file()

        elif line2[0] == "INVITE":
            encontrado = False
            for i in dicc:
                if cliente == i:
                    encontrado = True

            if encontrado:
                recibido = "Received from " + IP + ":" + PUERTO + ": INVITE"
                MensajesLog(recibido)
                my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                my_socket.connect((IP, PUERTO))
                my_socket.send(line)
                enviado = "Sent to " + IP + ":" + PUERTO + ": INVITE"
                MensajesLog(enviado)

                try:
                    data = my_socket.recv(1024)
                    print 'Recibido -- ', data
                except socket.error:
                    print "Error: No server listening at " + IP + " port " +
                        PORT
                    error = sys.exit("Error: No server listening at " + IP +
                                     " port " + PORT)
                    MensajesLog(error)
                    my_socket.close()
                    fin = "Finishing."
                    MensajesLog(fin)
                    print "Fin."

                print 'Recibido -- ', data
                reenviado = "Resent to " + IP + ":" + PORT + ": " + data
                MensajesLog(reenviado)
                print 'Enviando -- ', data
                self.wfile.write(data)

            else:
                self.wfile.write("SIP/2.0 404 User Not Found" + '\r\n\r\n')

        elif line2[0] == "ACK":
            recibido = "Received from " + IP + ":" + PUERTO + ": ACK"
            MensajesLog(recibido)
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            my_socket.connect((IP, PUERTO))
            my_socket.send(line)
            enviado = "Sent to " + IP + ":" + PUERTO + ": ACK"
            MensajesLog(enviado)

        elif line2[0] == "BYE":
            recibido = "Received from " + IP + ":" + PUERTO + ": BYE"
            MensajesLog(recibido)
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            my_socket.connect((IP, PUERTO))
            my_socket.send(line)
            enviado = "Sent to " + IP + ":" + PUERTO + ": BYE"
            MensajesLog(enviado)

            try:
                data = my_socket.recv(1024)
                print 'Recibido -- ', data
            except socket.error:
                print "Error: No server listening at " + IP + " port " + PORT
                error = sys.exit("Error: No server listening at " + IP +
                                 " port " + PORT)
                MensajesLog(error)
                my_socket.close()
                fin = "Finishing."
                MensajesLog(fin)
                print "Fin."

            print 'Recibido -- ', data
            reenviado = "Resent to " + IP + ":" + PORT + ": " + data
            MensajesLog(reenviado)
            print 'Enviando -- ', data
            self.wfile.write(data)

        else:
            try:
                data = my_socket.recv(1024)
                print 'Recibido -- ', data
            except socket.error:
                print "Error: No server listening at " + IP + " port " + PORT
                error = sys.exit("Error: No server listening at " + IP +
                                 " port " + PORT)
                MensajesLog(error)
                my_socket.close()
                fin = "Finishing."
                MensajesLog(fin)
                print "Fin."

            print 'Recibido -- ', data
            reenviado = "Resent to " + IP + ":" + PORT + ": " + data
            MensajesLog(reenviado)
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            my_socket.connect((IP, PUERTO))
            my_socket.send(data)
            print 'Enviando -- ', data
            self.wfile.write(data)

        while 1:
            # Si no hay más líneas salimos del bucle infinito
            if not line or line2:
                break

if __name__ == "__main__":
    # Comprobamos que introducimos el numero correcto de parametros y que
    # existe el fichero de audio
    if len(sys.argv) != 2:
        print("Usage: python proxy_registrar.py config")
        error = "Usage: python proxy_registrar.py config"
        MensajesLog(error)
        sys.exit()

    # parseamos el archivo ua2.xml
    parser = make_parser()
    cHandler = ProxyRegistrar()
    parser.setContentHandler(cHandler)
    parser.parse(open(sys.argv[1]))

    # Creamos servidor de eco y escuchamos
    proxy = SocketServer.UDPServer((str(cHandler.server_ip),
            int(cHandler.server_puerto)), ProxyRegistrar)
    print "Server MiServidorBigBang listening at port " +
            cHandler.server_puerto + "..."
    proxy.serve_forever()
    comienzo = "Server MiServidorBigBang listening at port " +
                cHandler.server_puerto + "..."
    MensajesLog(comienzo)
# ejecutamos el proxy: python proxy_registrar.py pr.xml
