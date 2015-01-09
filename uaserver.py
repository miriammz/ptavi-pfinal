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
    mensaje = mensaje.split(" ")
    fich = open(cHandler.log, "a")
    msg = str(time.time()) + " " + str(mensaje) + " " + "\n"
    fich.write(msg)
    fich.close()


class ServerHandler(ContentHandler):

    def __init__(self):
        self.username = ""
        self.passwd = ""
        self.uaserver_ip = ""
        self.uaserver_puerto = 0
        self.rtp_puerto = 0
        self.regproxy_ip = ""
        self.regproxy_puerto = 0
        self.log = ""
        self.audio = ""

    def startElement(self, etiqueta, atributo):
        if etiqueta == "account":
            self.account_username = atributo.get("username", "")
            self.account_passwd = atributo.get("passwd", "")
        elif etiqueta == "uaserver":
            self.uaserver_ip = atributo.get("ip", "127.0.0.1")
            self.uaserver_puerto = atributo.get("puerto", "")
        elif etiqueta == "rtpaudio":
            self.rtp_puerto = atributo.get("puerto", "")
        elif etiqueta == "regproxy":
            self.regproxy_ip = atributo.get("ip", "")
            self.regproxy_puerto = atributo.get("puerto", "")
        elif etiqueta == "log":
            self.log = atributo.get("path", "")
        elif etiqueta == "audio":
            self.audio = atributo.get("path", "")


class EchoHandler(SocketServer.DatagramRequestHandler):

    def handle(self):
        line = self.rfile.read()
        line2 = line.split(" ")
        IP = cHandler.regproxy_ip
        PORT = int(cHandler.regproxy_puerto)
        line2[0] = ['INVITE', 'ACK', 'BYE', 'CANCEL', 'OPTIONS', 'REGISTER']
        print "El cliente nos manda " + line

        if line2[0] == "INVITE":
            recibido = "Received from " + IP + ":" + PORT + ": INVITE"
            MensajesLog(recibido)
            envio = "Sent to " + IP + ":" + PORT + ": " + "SIP/2.0 100 Trying"
            MensajesLog(envio)
            envio = "Sent to " + IP + ":" + PORT + ": " + "SIP/2.0 180 Ringing"
            MensajesLog(envio)
            envio = ("Sent to " + IP + ":" + PORT + ": " + "SIP/2.0 200 OK " +
                     "Content-Type: application/sdp" + '\n\n' + "v=0" + '\n' +
                     "o=" + cHandler.account_username + " " + IP + '\n' +
                     "s=misesion" + '\n' + "t=0" + '\n' + "m=audio " +
                     cHandler.rtpaudio_puerto + " RTP")
            MensajesLog(envio)
            SDP = ("Content-Type: application/sdp" + '\r\n' + "v=0" + '\n' +
                   "o=" + cHandler.account_username + " " + IP + '\n' +
                   "s=misesion" + '\n' + "t=0" + '\n' + "m=audio " +
                   cHandler.rtpaudio_puerto + " RTP")
            self.wfile.write("SIP/2.0 100 Trying" + '\r\n\r\n' +
                             "SIP/2.0 180 Ringing" + '\r\n\r\n' +
                             "SIP/2.0 200 OK" + '\r\n\r\n' + SDP)

        elif line2[0] == "BYE":
            recibido = "Received from " + IP + ":" + PORT + ": BYE"
            MensajesLog(recibido)
            envio = "Sent to " + IP + ":" + PORT + ": " + "SIP/2.0 200 OK"
            MensajesLog(envio)
            self.wfile.write("SIP/2.0 200 OK" + '\r\n\r\n')

        elif line2[0] == "ACK":
            recibido = "Received from " + IP + ":" + PORT + ": ACK"
            MensajesLog(recibido)
            encontrado = ("./mp32rtp -i " + cHandler.uaserver_ip + " -p " +
                          cHandler.rtpaudio_puerto + " < " +
                          cHandler.audio_path)
            print "Enviando audio..."
            audio = ("Sent to " + cHandler.uaserver_ip + ":" +
                     cHandler.rtpaudio_puerto + ": enviando audio")
            MensajesLog(audio)
            os.system(encontrado)
            audio = ("Sent to " + cHandler.uaserver_ip + ":" +
                     cHandler.rtpaudio_puerto + ": envío completado")
            print "Envío completado"
            print 'Recibido -- ', data

        elif line2[0] != "INVITE" and line2[0] != "BYE" and line2[0] != "ACK":
            recibido = "Received from " + IP + ":" + PORT + ": " + line2[0]
            MensajesLog(recibido)
            envio = ("Sent to " + IP + ":" + PORT + ": " +
                     "SIP/2.0 405 Method Not Allowed")
            MensajesLog(envio)
            self.wfile.write("SIP/2.0 405 Method Not Allowed" + '\r\n\r\n')

        else:
            recibido = "Received from " + IP + ":" + PORT + ": " + line2[0]
            MensajesLog(recibido)
            envio = ("Sent to " + IP + ":" + PORT + ": " +
                     "SIP/2.0 400 Bad Request")
            MensajesLog(envio)
            self.wfile.write("SIP/2.0 400 Bad Request" + '\r\n\r\n')

        while 1:
            if not line or line2:
                break

if __name__ == "__main__":
    # parseamos el archivo ua2.xml
    parser = make_parser()
    cHandler = ServerHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open(sys.argv[1]))

    if len(sys.argv) != 2:
        sys.exit("Usage: python uaserver.py config")
    else:
        comienzo = "Listening..."
        print comienzo
        MensajesLog(comienzo)

    serv = SocketServer.UDPServer((cHandler.uaserver_ip,
                                   int(cHandler.uaserver_puerto)), EchoHandler)
    serv.serve_forever()
