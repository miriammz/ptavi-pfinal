#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import sys
import SocketServer
import os
import time
import socket


def MensajesLog(mensaje):
    mensaje = mensaje.split("")
    fich = open(cHandler.log, "a")
    for cont in mensaje:
        msg = str(time.time()) + " " + str(cont) + " " + "\n"
    fich.write(msg)
    fich.close()


class ServerHandler(ContentHandler):

    def __init__(self):
        self.etiquetas = {
            "account": ["username", "passwd"],
            "uaserver": ["ip", "puerto"],
            "rtpaudio": ["puerto"],
            "regproxy": ["ip", "puerto"],
            "log": ["path"],
            "audio": ["path"]}
        self.lista = []

    def startElement(self, etiqueta, atributo):
        if etiqueta in self.etiquetas:
            dic = {}
            for attr in self.etiquetas[etiqueta]:
                dic[attr] = (atributo.get(attr, ""))
            self.lista.append([etiqueta, dic])


class EchoHandler(SocketServer.DatagramRequestHandler):

	def handle(self):
		# Escribe dirección y puerto del cliente (de tupla client_address)
        line = self.rfile.read()
        line2 = line.split(" ")
		IP = cHandler.regproxy_ip
		PORT = str(cHandler.regproxy_puerto)
        print "El cliente nos manda " + line
        if line2[0] == "INVITE":
			recibido = "Received from " + IP + ":" + PORT + ": INVITE" 
			MensajesLog(recibido)
            self.wfile.write("SIP/2.0 100 Trying" + '\r\n\r\n' +
                             "SIP/2.0 180 Ringing" + '\r\n\r\n' +
                             "SIP/2.0 200 OK" + '\r\n\r\n')
        elif line2[0] == "BYE":
			recibido = "Received from " + IP + ":" + PORT + ": BYE"
			MensajesLog(recibido)
            self.wfile.write("SIP/2.0 200 OK" + '\r\n\r\n')
        elif line2[0] == "ACK":
			recibido = "Received from " + IP + ":" + PORT + ": ACK"
			MensajesLog(recibido)
            self.wfile.write("SIP/2.0 200 OK" + '\r\n\r\n')
            encontrado = "./mp32rtp -i " + IP + " -p 23032 < " + FICH_AUDIO
            print "Enviando audio..."
            os.system(encontrado)
            print "Envío completado"
        elif line2[0] != "INVITE" and line2[0] != "BYE" and line2[0] != "ACK":
            self.wfile.write("SIP/2.0 405 Method Not Allowed")
        else:
            self.wfile.write("SIP/2.0 400 Bad Request")
        while 1:
            # Si no hay más líneas salimos del bucle infinito
            if not line or line2:
                break

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python uaserver.py config")
		error = "Usage: python uaserver.py config"
        MensajesLog(error)
        sys.exit()
	else:
		print "Listening..."
		comienzo = "Listening..."
		MensajesLog(comienzo)

    # parseamos el archivo ua2.xml
    parser = make_parser()
    cHandler = ServerHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open(sys.argv[1]))

	serv = SocketServer.UDPServer((cHandler.uaserver_ip,
	cHandler.uaserver_puerto), EchoHandler)
    serv.serve_forever()
