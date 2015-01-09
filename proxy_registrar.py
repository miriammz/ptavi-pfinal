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
    mensaje = mensaje.split(" ")
    fich = open(cHandler.log, "a")
    msg = str(time.time()) + " " + str(mensaje) + " " + "\n"
    fich.write(msg)
    fich.close()


class ProxyHandler(ContentHandler):

    def __init__(self):
        self.name = ""
        self.ip = ""
        self.puerto = ""
        self.database_path = ""
        self.database_passwdpath = ""
        self.log = ""

    def startElement(self, etiqueta, atributo):
        if etiqueta == "server":
            self.server_name = atributo.get("username", "")
            self.server_ip = atributo.get("ip", "127.0.0.1")
            self.server_puerto = atributo.get("puerto", "")
        elif etiqueta == "database":
            self.database_path = atributo.get("path", "")
            self.passwd_path = atributo.get("passwdpath", "")
        elif etiqueta == "log":
            self.log = atributo.get("path", "")

dicc = {}


class ProxyRegistrar(SocketServer.DatagramRequestHandler):

    dicc = {}

    def register2file(self):
        fich = open(cHandler.database_path, "a")
        fich.write("User\tIP\tPuerto\tExpires\n")
        for cliente, valor in self.dicc.items():
            ip = valor.split(",")[0]
            puerto = valor.split(",")[1]
            hora = time.strftime('%Y-­%m-­%d %H:%M:%S',
                                 time.gmtime(time.time()))
            fich.write(cliente + '\t' + ip + '\t' + puerto + '\t' + hora +
                       '\n')
        fich.close()

    def handle(self):
        line = self.rfile.read()
        line2 = line.split(" ")
        line3 = line.split(":")
        IP = str(self.client_address[0])
        PUERTO_UA = str(self.client_address[1])
        cliente = line2[1].split(":")[1]
        self.dicc[cliente] = IP
        hora_actual = time.time()

        print "El cliente nos manda " + line
        if line2[0] == "REGISTER":
            PUERTO = str(line2[1].split(":")[2])
            EXPIRES = line3[3]
            tiempo = time.time() + int(EXPIRES)
            registrado = "Received from " + IP + ":" + PUERTO + ": REGISTER"
            MensajesLog(registrado)
            self.wfile.write("SIP/2.0 200 OK" + '\r\n\r\n')
            enviado = "Sent to " + IP + ":" + PUERTO + ": 200 OK"
            MensajesLog(enviado)
            if EXPIRES == 0:
                if cliente in self.dicc:
                    # borramos al usuario
                    del self.dicc[cliente]
                    self.register2file()
            else:
                self.dicc[cliente] = IP + ", " + PUERTO + ", " + str(tiempo)
                self.register2file()

            for elemento, valor in self.dicc.items():
                hora = valor.split(",")[-1]
                if hora_actual > hora:
                    del self.dicc[elemento]
                    self.register2file()

        elif line2[0] == "INVITE":
            encontrado = False
            PORT = int(self.dicc[cliente][1])
            for i in self.dicc:
                if cliente == i:
                    encontrado = True

            if encontrado:
                recibido = "Received from " + IP + ":" + str(PORT) + ": INVITE"
                MensajesLog(recibido)
                my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                my_socket.connect((IP, PORT))
                print dicc[cliente]
                my_socket.send(line)
                enviado = "Sent to " + IP + ":" + str(PORT) + ": INVITE"
                MensajesLog(enviado)

                try:
                    data = my_socket.recv(1024)
                    print 'Recibido -- ', data
                except socket.error:
                    error = ("Error: No server listening at " +
                             cHandler.server_ip + " port " +
                             cHandler.server_puerto)
                    sys.exit(error)
                    MensajesLog(error)
                    my_socket.close()
                    fin = "Finishing."
                    MensajesLog(fin)
                    print "Fin."

                print 'Recibido -- ', data
                reenviado = "Resent to " + IP + ":" + str(PORT) + ": " + data
                MensajesLog(reenviado)
                print 'Enviando -- ', data
                self.wfile.write(data)

            else:
                self.wfile.write("SIP/2.0 404 User Not Found" + '\r\n\r\n')

        elif line2[0] == "ACK":
            PORT = int(self.dicc[cliente][1])
            recibido = "Received from " + IP + ":" + str(PORT) + ": ACK"
            MensajesLog(recibido)
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            my_socket.connect((IP, PORT))
            my_socket.send(line)
            enviado = "Sent to " + IP + ":" + str(PORT) + ": ACK"
            MensajesLog(enviado)

        elif line2[0] == "BYE":
            PORT = int(self.dicc[cliente][1])
            recibido = "Received from " + IP + ":" + str(PORT) + ": BYE"
            MensajesLog(recibido)
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            my_socket.connect((IP, PORT))
            my_socket.send(line)
            enviado = "Sent to " + IP + ":" + str(PORT) + ": BYE"
            MensajesLog(enviado)

            try:
                data = my_socket.recv(1024)
                print 'Recibido -- ', data
            except socket.error:
                error = ("Error: No server listening at " +
                         cHandler.server_ip + " port " +
                         cHandler.server_puerto)
                sys.exit(error)
                MensajesLog(error)
                my_socket.close()
                fin = "Finishing."
                MensajesLog(fin)
                print "Fin."

            print 'Recibido -- ', data
            reenviado = "Resent to " + IP + ":" + str(PORT) + ": " + data
            MensajesLog(reenviado)
            print 'Enviando -- ', data
            self.wfile.write(data)

        else:
            try:
                data = my_socket.recv(1024)
                print 'Recibido -- ', data
            except socket.error:
                error = ("Error: No server listening at " +
                         cHandler.server_ip + " port " +
                         cHandler.server_puerto)
                sys.exit(error)
                MensajesLog(error)
                my_socket.close()
                fin = "Finishing."
                MensajesLog(fin)
                print "Fin."

            print 'Recibido -- ', data
            reenviado = "Resent to " + IP_ + ":" + PUERTO_UA + ": " + data
            MensajesLog(reenviado)
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            my_socket.connect((IP, PUERTO_UA))
            my_socket.send(data)
            print 'Enviando -- ', data
            self.wfile.write(data)

        while 1:
            # Si no hay más líneas salimos del bucle infinito
            if not line or line2 or line3:
                break

if __name__ == "__main__":
    # Comprobamos que introducimos el numero correcto de parametros y que
    # existe el fichero de audio
    if len(sys.argv) != 2:
        sys.exit("Usage: python proxy_registrar.py config")

    # parseamos el archivo .xml
    parser = make_parser()
    cHandler = ProxyHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open(sys.argv[1]))
    # Creamos servidor de eco y escuchamos
    proxy = SocketServer.UDPServer((str(cHandler.server_ip),
                                    int(cHandler.server_puerto)),
                                   ProxyRegistrar)
    servidor = ("Server MiServidorBigBang listening at port " +
                cHandler.server_puerto + "...")
    print servidor
    proxy.serve_forever()
    MensajesLog(servidor)
