from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView


from management.forms import CreateTitleForm, CreateClientTitleForm
from management.forms import CreateProductForm, EditProductForm

from management.models import Product
from management.models import Client
from management.models import Title

# Create your views here.
def index(request):
	product_list = Product.objects.all().order_by('due_date')
	context = {'product_list': product_list}
	return render(request, 'management/index.html', context)

def product(request, product_id):
	product = get_object_or_404(Product, pk=product_id)
	return render(request, 'management/product.html', {'product': product})

class ListClientView(ListView):
	model = Client
	template_name = 'client_list.html'

class CreateClientView(CreateView):
	model = Client

	def get_context_data(self, **kwargs):

		context = super(CreateClientView, self).get_context_data(**kwargs)
		context['action'] = reverse('client-new')
		return context

class DetailClientView(DetailView):
	model = Client


class UpdateClientView(UpdateView):
	model = Client

	def get_context_data(self, **kwargs):
		context = super(UpdateClientView, self).get_context_data(**kwargs)
		context['action'] = reverse('client-edit',
									kwargs={'pk': self.get_object().id})
		return context

def createTitle(request): 
	if request.method == 'POST':
		form = CreateTitleForm(request.POST)
		if form.is_valid():
			# create a new item
			title = Title.objects.create(
				client=form.cleaned_data['client'],
				name=form.cleaned_data['name'],
			)
			# Always redirect after a POST
			return HttpResponseRedirect('/management/title/%s/' % title.id)
	else:        
		form = CreateTitleForm()
	context = {'page_title': 'Add Title', 'form': form}
	return render(request, 'management/title_form.html', context)

def createTitleClient(request, client_id):  # from client ID
	client = get_object_or_404(Client, pk=client_id)
	if request.method == 'POST':
		form = CreateClientTitleForm(request.POST)
		if form.is_valid():
			# create a new item
			title = Title.objects.create(
				client=client,
				name=form.cleaned_data['name'],
			)
			# Always redirect after a POST
			return HttpResponseRedirect('/management/title/%s/' % title.id)
	else:        
		form = CreateClientTitleForm()
	context = {'page_title': 'Add Title', 'client': client, 'form': form}
	return render(request, 'management/title_form.html', context)



class DetailTitleView(DetailView):
	model = Title

class UpdateTitleView(UpdateView):
	model = Title
   
	def get_success_url(self):
		return reverse('title-detail', kwargs={'pk': self.get_object().id})

	def get_context_data(self, **kwargs):

		context = super(UpdateTitleView, self).get_context_data(**kwargs)
		context['action'] = reverse('title-edit',
									kwargs={'pk': self.get_object().id})
		return context


def editTitle(request, pk):
	title = Title.objects.get(pk=pk)

	if request.method == 'POST':
		form = CreateClientTitleForm(request.POST, instance=title)
		if form.is_valid():
			# create a new item
			title = form.save(commit=False)
			title.client = title.client
			title.save()
			# Always redirect after a POST
			return HttpResponseRedirect('/management/title/%s/' % title.id)
	else:        
		form = CreateClientTitleForm(instance=title)
	
	context = {'page_title': 'Edit Title', 'instance': title, 'form': form}
	return render(request, 'management/title_form.html', context)

def createProduct(request, title_id):  # requires a title_id
	title = get_object_or_404(Title, pk=title_id)
	if request.method == 'POST':
		form = CreateProductForm(request.POST)
		if form.is_valid():
			# create a new item
			product = Product.objects.create(
				title=title,
				product_type = form.cleaned_data['product_type'],
				name = form.cleaned_data['name'],
				cat_number = form.cleaned_data['cat_number'],
				due_date = form.cleaned_data['due_date'],
				status = form.cleaned_data['status'],
			)
			# Always redirect after a POST
			return HttpResponseRedirect(reverse('product-detail', kwargs={'product_id': product.id}))
	else:        
		form = CreateProductForm(initial={'status': '1'})
	context = {'page_title': 'Add Product', 'title': title, 'form': form, 'instance': title}
	return render(request, 'management/product_form.html', context)


def editProduct(request, product_id): 
	product = get_object_or_404(Product, pk=product_id)
	if request.method == 'POST':
		form = EditProductForm(request.POST, instance=product)
		if form.is_valid():
			# create a new item
			product = form.save(commit=False)
			product.title = product.title
			product_type = product.product_type
			product.save()
			# Always redirect after a POST
			return HttpResponseRedirect(reverse('product-detail', kwargs={'product_id': product.id}))
	else:        
		form = EditProductForm(instance=product)
	context = {'page_title': 'Edit Product', 'title': product.title, 'form': form, 'instance': product}
	return render(request, 'management/product_form.html', context)