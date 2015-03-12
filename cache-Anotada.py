
#!/usr/bin/python
# -*- coding: utf-8 -*-
import webapp
import socket
import urllib

memoriaCache = {}

class cacheAnotada(webapp.webApp):

    def introducirEnlaces(self, fichero, url, enlaces):
        fichero = urllib.urlopen(url)
        html = fichero.read()
        memoriaCache[url] = html
        indice = html.find('<body')
        indice = html.find('>', indice)
        html = (html[:indice + 1] + enlaces +
                "</br></br>" + html[(indice + 1):])        
        return html

    def cabecera(self,recurso,fichero,cabeceras,url,enlaces):
        if recurso == "recurso1":
            html = ("<html><body>" + enlaces +
            "<p>Cabeceras procedentes del navegador del navegador:</p>" +
            cabeceras + "<body text='red'>" +
            "<body bgcolor='#000000'>"
            "</html></body>")
        elif recurso == "recurso2":
            html = ("<html><body>" + enlaces +
            "<p>Cabeceras con destino al servidor " + url + ":</p>" +
            "<body text='red'>" +
            "<body bgcolor='#000000'>"
            "</html></body>")
        elif recurso == "recurso3":
            infoRecurso3 = str(fichero.info())
            print infoRecurso3
            html = ("<html><body>" + enlaces +
                    "<p>Cabeceras procedentes del servidor " + url + ":</p>" +
                    infoRecurso3 + "<body text='red'>" +
                    "<body bgcolor='#000000'>"
                    "</html></body>")
        elif recurso == "recurso4":
            html = ("<html><body>" + enlaces +
            "<p>Ninguna cabecera para el navegador:" +
            "<body text='red'>" +
            "<body bgcolor='#000000'>"
            "</p></html></body>")
        elif recurso == "memoriaCache":
            try:
                html = memoriaCache[url]
                print html
            except KeyError:
                html = ("<html><body><p>Pagina no encontrada</p>" +
                        "</html></body>")
                return ("400 Not Found", hmtl)
        else:
            html = self.introducirEnlaces(fichero,url,enlaces)
        return html    

    def parse(self, request):
        lista = request.split()
        direccionURL = lista[1][1:].split('/')[0]
        cabeceras = request.split('\r\n', 1)[1]
        try:
            recurso = lista[1][1:].split('/')[1]
        except IndexError:
            recurso = None
        print direccionURL
        print recurso
        print cabeceras
        
        return (direccionURL, recurso, cabeceras)

    def process(self, parsedRequest):
        (direccionURL, recurso, cabeceras) = parsedRequest
        miDireccionURL = "http://" + socket.gethostname() + ":1234/" + direccionURL
        url = "http://" + direccionURL
        enlaces = ("<a href= '" + miDireccionURL + "/recurso1'>Recurso1</a></br>" +
                   "<a href= '" + miDireccionURL + "/recurso2'>Recurso2</a></br>" +
                   "<a href= '" + miDireccionURL + "/recurso3'>Recurso3</a></br>" +
                   "<a href= '" + miDireccionURL + "/recurso4'>Recurso4</a></br>" +
                   "<a href= '" + url + "'>Ir a pagina original</a></br>" +
                   "<a href= '" + miDireccionURL + "'>Recargar pagina</a></br>" +
                   "<a href= '" + miDireccionURL + "/memoriaCache'>Cache</a></br>")
        try:
            fichero = urllib.urlopen(url)
        except IOError:
            html = ("<html><body><p>Pagina no encontrada</p></html></body>")
            return ("400 Not Found", hmtl)
        formulario = self.cabecera(recurso,fichero,cabeceras,url,enlaces)
        
        return ("200 OK", formulario)
if __name__ == "__main__":
    servidor = cacheAnotada(socket.gethostname(), 1234)
