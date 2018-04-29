from django.shortcuts import render, get_object_or_404
from django.views.generic.base import RedirectView, TemplateView
from pagina.models import Product,Purchase
from django.urls import reverse
from django.http import HttpResponse
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#Prueba de integrar directamente el paypal.py aqui en vistas
import decimal
import urllib
import sys

from django.conf import settings


######################################

#Agregar una nueva vista de tal forma que cuando se seleccione de la lista de articulos
#disponibles lanze una nueva en la cual se va a seleccionar si esta va a ser una renta o una compra
#Para en seguida sacar otra vista la cual seleccione los datos necesarios que se le soliciten
def error(request):
	return render(request,'pagina/error.html')

def index(request):
	p = Product.objects.all()
	return render(request,'pagina/paypal.html',{'list': Product.objects.all()})

@login_required
def profile(request):
	return render(request,'pagina/profile.html',{'list':Purchase.objects.filter(purchaser=request.user)})

@login_required
def descripcion(request,id):
	resource = get_object_or_404(Product,pk=id)
	return render(request,'pagina/descripcion.html',{'resource':resource})


@login_required
def download(request, id):
	resource = get_object_or_404(Product,pk=id)
	return render(request,'pagina/purchase.html',{'resource':resource,'paypal_url':settings.PAYPAL_URL,'paypal_email':settings.PAYPAL_EMAIL,'paypal_return_url':settings.PAYPAL_RETURN_URL})
#agregar un datediff, para mandar tambien el precio total de la renta
@login_required
def downloadr(request,id):
	resource = get_object_or_404(Product,pk=id)
	return render(request,'pagina/purchaseR.html',{'resource':resource,'paypal_url':settings.PAYPAL_URL,'paypal_email':settings.PAYPAL_EMAIL,'paypal_return_url':settings.PAYPAL_RETURN_URL})

@login_required
def purchased(request,uid,id):

	resource = get_object_or_404(Product,pk=id)
	user = get_object_or_404( User, pk=uid )

	if request.GET.get('tx'):
		tx = request.GET['tx']
		#print(tx)
		amt = request.GET['amt']
	#	print(amt)
		st = request.GET['st']
	#	print(st)
		try:
			existing = Purchase.objects.get(tx=tx)
			return render(request,'pagina/error.html',{'error':"Duplicate transaction"})
		except Purchase.DoesNotExist:
			result = verificar(tx)

			xd = resource.PrecioV

			if result.success() and str(resource.precio) == result.amount(): #valid
				purchase = Purchase(resource=resource,purchaser=user,tx=tx)
				purchase.save()

				return render(request,'pagina/purchased.html',{'resource':resource})
			else:
				return render(request,'pagina/error.html',{'error':"fallo para validar pago"})

	else:
		return render(request,'pagina/error.html',{'error':"No existe transaccion"})


#Pruebas del paypal.py agregado aqui a views

class verificar(object):
	def __init__(self,tx):
		try:
			transaccion = Purchase.objects.get(tx = tx)
			self.result = 'Transaction %s has alredy been processed' %tx
			self.response = self.result
		except Purchase.DoesNotExist:
			post = dict()
			post[ 'cmd' ] = '_notify-synch'
			post[ 'tx' ] = tx
			post[ 'at' ] = settings.PAYPAL_PDT_TOKEN
			self.response = urllib.request.urlopen( settings.PAYPAL_PDT_URL, urllib.parse.urlencode(post).encode("utf-8")).read().decode('utf-8')

			#data = urllib.parse.urlencode(post).encode("utf-8")
			#print(data)

			#req = settings.PAYPAL_PDT_URL
			#print(req)
			#with urllib.request.urlopen(req,data = data ) as f:
			#	self.response = f.read().decode('utf-8')


			lines = self.response.split( '\n' )
			print(lines)

			self.result = lines[0].strip()

			self.results = dict()
			for line in lines[1:]:
				linesplit = line.split( '=',2 )

				if len( linesplit ) == 2:
					self.results[ linesplit[0].strip() ] = urllib.parse.unquote(linesplit[1].strip())
				#print(results)

	def success( self ):
		return self.result == 'SUCCESS' and self.results[ 'payment_status' ] == 'Completed'
	def amount( self ):
		print(type(self.results['mc_gross']))
		print(self.results['payment_gross'])
		return self.results[ 'mc_gross' ]





#############################
