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
        self.dicc[cliente] = IP
		cliente = line2[1].split(":")[1]
		PUERTO = str(line2[1].split(":")[2])
		EXPIRES = line3[3]
		tiempo = time.time() + int(EXPIRES)
        hora_actual = time.time()
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
            self.wfile.write("SIP/2.0 100 Trying" + '\r\n\r\n' +
                             "SIP/2.0 180 Ringing" + '\r\n\r\n' +
                             "SIP/2.0 200 OK" + '\r\n\r\n')

        elif line2[0] == "BYE":
            self.wfile.write("SIP/2.0 200 OK" + '\r\n\r\n')
			

        #falta SIP/2.0 404 User Not Found: usuario no registrado
        elif line2[0] != "INVITE" and line2[0] != "BYE" and line2[0] != "ACK":
            self.wfile.write("SIP/2.0 405 Method Not Allowed")

        else:
            self.wfile.write("SIP/2.0 400 Bad Request")

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
# ejecutamos el proxy: python proxy_registrar.py config
# donde config es un fichero xml (pr.xml)
