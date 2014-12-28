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

class ProxyRegistrar(SocketServer.DatagramRequestHandler):

    def handle(self):

		def register2file():
            fich = open(cHandler.database_path, "a")
            fich.write("User\tIP\tExpires\n")
            expire = time.strftime('%Y-­%m-­%d %H:%M:%S',
                             time.gmtime(time.time()))
            fich.write(cliente + '\t' + IP + '\t' +  expire)

		# Escribe dirección y puerto del cliente (de tupla client_address)
        line = self.rfile.read()
        IP = str(self.client_address[0])
        line2 = line.split(" ")
		usuario = line2[1].split(":")
        print "El cliente nos manda " + line

		if line2[0] == "REGISTER":
        
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
