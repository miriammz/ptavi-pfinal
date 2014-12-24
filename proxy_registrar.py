#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import SocketServer
import sys
import os
import time
import socket


class ServerHandler(ContentHandler):
	
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

if __name__ == "__main__":
	if len(sys.argv) != 2:
        print("Usage: python proxy_registrar.py config")
		sys.exit()
	# parseamos el archivo ua2.xml
	parser = make_parser()
    cHandler = ServerHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open(sys.argv[1]))
