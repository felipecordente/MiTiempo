#!/usr/bin/python3

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string
import urllib.request

class CounterHandler(ContentHandler):

    def __init__ (self):
        self.inContent = 0
        self.theContent = ""
        self.inDia = 0
        self.inTemperatura = 0
        self.contador = 0

    def startElement (self, name, attrs):
        if name == 'enlace':
            self.inContent = 1
        if name == 'dia':
            self.inDia = 1
            self.contador += 1
        if self.inDia and self.contador == 2:
            if name == 'prob_precipitacion':
                if attrs.get('periodo') == '00-24':
                    self.inContent = 1
            if name == 'estado_cielo':
                if attrs.get('periodo') == '00-24':
                    self.descripcion = attrs.get('descripcion')
            if name == "temperatura":
                self.inTemperatura = 1
            if self.inTemperatura:
                if name == "maxima":
                    self.inContent = 1
                if name == "minima":
                    self.inContent = 1

    def endElement (self, name):
        if name == 'enlace':
            self.url_html = self.theContent.strip('\n')
            self.theContent=""
            self.inContent = 0
        elif name == 'dia':
            self.theContent=""
            self.inDia = 0
        elif name == 'prob_precipitacion' and self.inContent and self.contador == 2:
            self.prob_precipitacion = self.theContent.strip('\n')
            self.theContent=""
            self.inContent = 0
        elif name == 'estado_cielo' and self.inContent and self.contador == 2:
            self.theContent=""
            self.inContent = 0
        elif name == 'temperatura'and self.contador == 2:
            self.theContent=""
            self.inTemperatura = 0
        elif name == 'maxima' and self.inContent and self.contador == 2:
            self.maxima = self.theContent.strip('\n')
            self.theContent=""
            self.inContent = 0
        elif name == 'minima' and self.inContent and self.contador == 2:
            self.minima = self.theContent.strip('\n')
            self.theContent=""
            self.inContent = 0

        if self.inContent:
            self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

def main(url):
    XmlParser = make_parser()
    XmlHandler = CounterHandler()
    XmlParser.setContentHandler(XmlHandler)

    xmlFile = urllib.request.urlopen(url)
    XmlParser.parse(xmlFile)

    return XmlHandler.url_html, XmlHandler.prob_precipitacion, XmlHandler.descripcion, XmlHandler.maxima, XmlHandler.minima

if __name__ == '__main__':
    main()
