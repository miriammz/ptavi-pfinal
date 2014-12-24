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


class ClientHandler(ContentHandler):

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


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python uaclient.py config method option")
        sys.exit()
    # parseamos el archivo ua1.xml
    parser = make_parser()
    cHandler = ClientHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open(sys.argv[1]))

	# cogemos los parametros pasados por argumento
	METODO = sys.argv[2]
	OPCION = sys.argv[3]

	# Dirección IP del servidor y métodos
	IP = cHandler.regproxy_ip
	PORT = cHandler.regproxy_puerto
	METODO = ["REGISTER", "INVITE", "BYE"]

	# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
	my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	my_socket.connect((IP, PORT))

	LINE, LINE2 = ""
	#creamos LINE segun el tipo del metodo que pasamos como argumento
	if METODO == "REGISTER":
		LINE = "REGISTER sip:" + cHandler.account_username + " SIP/2.0" + "\r\n"
		LINE2 = "Expires: " + OPCION + "\r\n"
	elif METODO == "INVITE":
		LINE = "INVITE sip:" + OPCION + " SIP/2.0" + '\r\n'
		LINE2 = "v=0" + "\n" + "o=" + cHandler.account_username + " " + IP + 
				"\n" + "s=misesion" + "\n" + "t=0" + "\n" + "m=audio " +
				cHandler.rtpaudio_puerto + " RTP"
	elif METODO == "BYE":
		LINE = "BYE sip:" + OPCION + " SIP/2.0" + '\r\n'

	print "Enviando: " + LINE
	my_socket.send(LINE + '\r\n')

	try:
		data = my_socket.recv(1024)
		print 'Recibido -- ', data
	except socket.error:
		sys.exit("Error: No server listening at " + IP + " port " + str(PORT))

	if METODO == "REGISTER":	
	
	elif METODO == "INVITE":
		datos = data.split(" ")
		if data == ("SIP/2.0 100 Trying" + '\r\n\r\n' + "SIP/2.0 180 Ringing" +
		            '\r\n\r\n' + "SIP/2.0 200 OK" + '\r\n\r\n'):
		    LINE = "ACK sip:" + LOGIN + "@" + IP + " SIP/2.0"
		    print "Enviando: " + LINE
		    my_socket.send(LINE + '\r\n\r\n')
		    data = my_socket.recv(1024)
		    print 'Recibido -- ', data

	elif METODO == "BYE":

	print "Terminando socket..."

	# Cerramos todo
	my_socket.close()
	print "Fin."


