#!/usr/bin env python2
# -*- coding: utf-8 -*-

"""Serveur applicatif
Recoit des requetes POST (user, hashedpass, audioblob) des applications clientes
et renvoie les transcriptions 
"""

import BaseHTTPServer
import cgi

from speechActions import requestHandling
from clientAuth import checkAuth


class SpeechServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        '''Respond to a GET request'''
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("Ça se passe en POST pour les requêtes !")


    def do_POST(self):
        """Respond to a POST request"""
        
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        user = form['user']
        hashedPass = form['hashedPass']
        

        #Check if the user is authorizd
        if checkAuth(user, hashedPass):
            clientDB = form['clientDB']
            
            action = form['action']
            respMessage = speechActions.requestHandling(action, form)
        else:
            respMessage = "You're not authorized to call me !\
                            Register at speech.wumzi.info"
                            
          

        #And respond
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(respMessage)


def run(adress, port):
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
        PORT = 8080
        print("Port set to default : %s" % PORT)

    run('localhost', PORT)
