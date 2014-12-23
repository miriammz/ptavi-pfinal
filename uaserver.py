#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import sys
import SocketServer
import os
import time


class ServerHandler(ContentHandler):
	
	def __init__(self):
        self.etiquetas = {
		    "acount": ["username", "passwd"],
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

if __name__ == "__main__":
	if len(sys.argv) != 2:
        print("Usage: python uaserver.py config")
	# parseamos el archivo ua2.xml
	parser = make_parser()
    cHandler = ServerHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open(sys.argv[1]))

