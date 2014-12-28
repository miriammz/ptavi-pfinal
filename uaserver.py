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
    fich = open(cHandler.log_path, "a")
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
        IP = str(self.client_address[0])
        PORT = str(self.client_address[1])
        print line
        IP_server = line2[7]
        PORT_server = line2[11]
        line2[0] = ['INVITE', 'ACK', 'BYE', 'CANCEL', 'OPTIONS', 'REGISTER']
        print "El cliente nos manda " + line

        if line2[0] == "INVITE":
            recibido = "Received from " + IP + ":" + PORT + ": INVITE"
            MensajesLog(recibido)
            envio = "Sent to " + IP + ":" + PORT + ": " + "SIP/2.0 100 Trying"
            MensajesLog(envio)
            envio = "Sent to " + IP + ":" + PORT + ": " + "SIP/2.0 180 Ringing"
            MensajesLog(envio)
            envio = "Sent to " + IP + ":" + PORT + ": " + "SIP/2.0 200 OK " +
            "Content-Type: application/sdp" + '\n\n' + "v=0" + '\n' + "o=" +
            cHandler.account_username + " " + IP + '\n' + "s=misesion" + '\n' +
            "t=0" + '\n' + "m=audio " + cHandler.rtpaudio_puerto + " RTP"
            MensajesLog(envio)
            self.wfile.write("SIP/2.0 100 Trying" + '\r\n\r\n' +
                             "SIP/2.0 180 Ringing" + '\r\n\r\n' +
                             "SIP/2.0 200 OK" + '\r\n\r\n')
            self.wfile.write("Content-Type: application/sdp" + '\r\n' + "v=0" +
            '\n' + "o=" + cHandler.account_username + " " + IP + '\n' +
            "s=misesion" + '\n' + "t=0" + '\n' + "m=audio " +
            cHandler.rtpaudio_puerto + " RTP")

        elif line2[0] == "BYE":
            recibido = "Received from " + IP + ":" + PORT + ": BYE"
            MensajesLog(recibido)
            envio = "Sent to " + IP + ":" + PORT + ": " + "SIP/2.0 200 OK"
            MensajesLog(envio)
            self.wfile.write("SIP/2.0 200 OK" + '\r\n\r\n')

        elif line2[0] == "ACK":
            self.wfile.write("SIP/2.0 200 OK" + '\r\n\r\n')
            recibido = "Received from " + IP_server + ":" + PORT_server +
            ": ACK"
            MensajesLog(recibido)
            encontrado = "./mp32rtp -i " + IP_server + " -p " +
            PORT_server + " < " + cHandler.audio_path
            print "Enviando audio..."
            audio = "Sent to " + cHandler.uaserver_ip + ":" +
            cHandler.rtpaudio_puerto + ": enviando audio"
            MensajesLog(audio)
            os.system(encontrado)
            audio = "Sent to " + cHandler.uaserver_ip + ":" +
            cHandler.rtpaudio_puerto + ": envío completado"
            print "Envío completado"
            print 'Recibido -- ', data

        elif line2[0] != "INVITE" and line2[0] != "BYE" and line2[0] != "ACK":
            recibido = "Received from " + IP + ":" + PORT + ": " + line2[0]
            MensajesLog(recibido)
            envio = "Sent to " + IP + ":" + PORT + ": " +
            "SIP/2.0 405 Method Not Allowed"
            MensajesLog(envio)
            self.wfile.write("SIP/2.0 405 Method Not Allowed" + '\r\n\r\n')

        else:
            recibido = "Received from " + IP + ":" + PORT + ": " + line2[0]
            MensajesLog(recibido)
            envio = "Sent to " + IP + ":" + PORT + ": " +
            "SIP/2.0 400 Bad Request"
            MensajesLog(envio)
            self.wfile.write("SIP/2.0 400 Bad Request" + '\r\n\r\n')

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
