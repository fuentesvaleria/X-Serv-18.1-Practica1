#!/usr/bin/python3

import webapp
import csv

def Formulario():
    formu = """
    <form action="" method="POST">url:<br><input type="text" name="url" placeholder="URL a acortar"><br><input type="submit" value="Enviar"></form> 
    """
    return formu
    
class Url_Acortar (webapp.webApp):

	#asigno las variales list_url y url_reducida para poder luego tenerlas en los respectivos diccionarios
	#por otra parte asigno num = 0 porque es el numero donde voy a empezar a acortar
	
	list_url = ""
	url_reducida = ""
	num = 0
	diccionario = {}
	simplificado_dicc = {}
	
	def parse(self,request):
		metodo = request.split()[0] #nos devuelve o get o post
		recurso = request.split()[1][1:] #nos quedamos con la url
		if metodo == "POST" :
			cuerpo = request.split('\r\n\r\n', 1)[1].split('=')[1]
			if len(cuerpo.split("%3A%2F%2F")) == 1:
				url = "http://" + cuerpo.split('%', 1)[0]
			else:
				url = "http://" + cuerpo.split("%3A%2F%2F", 1)[1].split('%', 1)[0]
		else:
			cuerpo = ""
			url = cuerpo
		print (url)
		return (metodo, recurso, url)
	
	def process(self,parsedRequest):
		metodo, resource, url = parsedRequest
		formu = Formulario()
		if metodo == "GET":
			if resource == "":
				codigo = "200 OK"
				#creamos una tabla de html usando table tb td 
				cuerpo = "<html>url<br>" + formu + "<table><tr><td>URL</td><td>short_url</td></tr><tr><td>" + self.list_url + "</td><td>" + self.url_reducida + "</td></tr></table>" + "</html>"
			elif resource == "favicon.ico":
				codigo = "404 Not Found"
				cuerpo = "<html><body>favicon</html>"
			else:
			# en este caso nos va a redirigir la pagina se refrescara en el caso de que yo pido "nº" y eso es menor que el contador
				if int(resource) < self.num :
					codigo = "307 Temporary Redirect"
					cuerpo = "<html><body><h1>Redirigir</h1><meta http-equiv='Refresh' content='0; url= " + str(self.simplificado_dicc[int(resource)]) +"'></body></html>"
				else:
					codigo = "400 Not Found"
					cuerpo = "<html><body><h1>error </h1></body></html>"
		if metodo == "POST" :
			if url == "":
				codigo = "400 Not Found"
				cuerpo = "<html><body><h1>error </h1></body></html>"
			if url not in self.diccionario.keys(): #dict.keys() se usa mucho en los diccionarios
				self.diccionario[self.num] = url
				self.diccionario[url] = self.num
				self.list_url = self.list_url + "<p>" + str(url) + "</p>"
				self.url_reducida = self.url_reducida + "<p>http://localhost:1234/" + str(self.num) + "</p>"
				self.num = self.num + 1
			#el diccionario en un fichero
			#buscado en google
			with open('listurl.csv', 'a', newline = '') as mifichero:
				ficheroUrl = csv.writer(mifichero)
				ficheroUrl.writerow([self.num,url])
			codigo = "200 OK"
			cuerpo = '<html><body>' + "<p><h4>url_orig<a href=" + url + ">" + str(url) + "</a></h4></p><p><h4>url_short<a href=" + "http://localhost:1234/" + str(self.num - 1) + ">" + str("http://localhost:1234/" + str(self.num - 1)) + "</a></h4></p>" + "<p><a href='http://localhost:1234/'>formulario</a></p>" + "</body></html>"
		
		return(codigo,cuerpo)
	
	def __init__(self, hostname, port):
		archi = open('listurl.csv', 'a')
		archi.close()
		super().__init__(hostname,port)

if __name__ == "__main__":
    testWebApp = Url_Acortar("localhost", 1234)