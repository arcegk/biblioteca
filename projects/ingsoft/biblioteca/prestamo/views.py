from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import RegistroPrestamo
from django.views.generic import TemplateView , View
from pazys.models import Estudiante
from libros.models import Libro
from datetime import datetime , timedelta
import json


class GenerarPrestamo(TemplateView):
	template_name = "prestamo.html"

class ConsultarPrestamo(TemplateView):
	template_name = "pc.html"

class AjxGenerarPrestamo(View):

# faltan validaciones de multas y prestamos

	def get(self, request):

		code = request.GET.get('code')
		libro = request.GET.get('libro')
		print code
		diccionario = []
		try:
			obj = RegistroPrestamo()
			obj.estudiante = Estudiante.objects.get(codigo=code)
			obj.libro = Libro.objects.get(codigoasignado=libro)
			obj.fechaInicioPrestamo = datetime.now()
			obj.fechaLimite = datetime.now()+timedelta(days=5)
			obj.save()
			ide = obj.id 
			diccionario.append({
					'id' : ide,
				})

		except ObjectDoesNotExist:
			pass

		return HttpResponse(json.dumps({'data' : diccionario}) ,content_type='application/json')


class AjxConsultaLibro(View):

# faltan validaciones de multas y prestamos

	def get(self, request):

		libro = request.GET.get('libro')
		diccionario = []
		try:
			
			libro = Libro.objects.get(codigoasignado=libro)
			diccionario.append({
					'titulo' : libro.titulo,
					'edicion' : libro.Edicion,
					'volumen' : libro.volumen,
				})

		except ObjectDoesNotExist:
			pass

		return HttpResponse(json.dumps({'data' : diccionario}) ,content_type='application/json')



class AjxConsultaPrestamo(View):

# faltan validaciones de multas y prestamos

	def get(self, request):

		code = request.GET.get('code')
		diccionario = []
		dic = []
		try:
			estu = Estudiante.objects.get(codigo=code)
			obj = RegistroPrestamo.objects.filter(estudiante=estu)
			for item in obj:
				dic.append({

					'titulo' : item.libro.tituloLibro,
					'edicion' : item.libro.edicionLibro,
					'volumen' : item.libro.volumenLibro,
				})

			diccionario.append({"prestamos" : dic  , 'nombre' : estu.nombre })

		except ObjectDoesNotExist:
			pass

		return HttpResponse(json.dumps({'data' : diccionario}) ,content_type='application/json')
