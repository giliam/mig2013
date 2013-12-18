#!/usr/bin env python2
# -*- coding: utf-8 -*-

"""Serveur applicatif
Recoit des requetes POST (user, hashedpass, audioblob) des applications clientes
et renvoie les transcriptions 
"""

import BaseHTTPServer
from cgi import FieldStorage
from xml.etree import ElementTree as ET

from speechserver.speechActions import requestHandling
from speechserver.clientAuth import AuthUser

from core.utils import db



class SpeechServerHandler( BaseHTTPServer.BaseHTTPRequestHandler ):
    def do_GET(self):
        """ Respond to a GET request """
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("Ca se passe en POST pour les requetes !")


    def do_POST(self):
        """Respond to a POST request"""
        
        form = FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        user = form.getvalue('user')
        hashedPass = form.getvalue('hashedPass')
        clientDB = ''#form.getvalue('clientDB')
        
        #form = dict(form)
        #print(form)

        #Check if the user is authorized and he has access to clientDb
        authUser = AuthUser()
        if True or authUser.checkAuth(user, authUser.hashPass(hashedPass), clientDB):
            action = form.getvalue('action')
            requestHandler = requestHandling()
            respData = requestHandler.handle(clientDB, action, form)
            respXML = self.buildXMLResponse(respData)
        else:
            respXML = "You're not authorized to call me !\
                            Register at speech.wumzi.info"

        #respXML = self.buildXMLResponse({'respWord' : user})
          

        #And respond
        self.send_response(200)
        self.send_header('Content-type', 'text/xml')
        self.end_headers()
        self.wfile.write(respXML)

    @classmethod
    def buildXMLResponse(cls, data):
        """Build the XML doc response from the data dictionnary"""
        root = ET.Element('root')
        for key, value in data.items():
            elem = ET.SubElement(root, key)
            elem.text = value

        return ET.tostring(root, encoding="utf-8")


    @classmethod
    def parseXMLRequest(cls, XMLString):
        """Build a dict from an XML doc"""
        data = {}
        root = ET.fromstring(XMLString)
        for child in root:
            data[child.tag] = child.text
        return data



def run(port, adress="localhost"):
    server =  BaseHTTPServer.HTTPServer((adress, port), SpeechServerHandler)
    server.serve_forever()


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2:
        try:
            PORT = int(sys.argv[1])
        except TypeError:
            print("Please provide an int !")
    else:
        PORT = 8010
        print("Port set to default : %s" % PORT)

    run('localhost', PORT)
