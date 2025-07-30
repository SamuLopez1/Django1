from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'pages/home.html'
class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Your Name",
        })
        return context
    
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact - Online Store",
            "subtitle": "Contact Us",
            "email": "support@fakestore.com",
            "address": "123 Fake Street, Medellín, Colombia",
            "phone": "+57 300 123 4567",
        })
        return context

class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 299.99},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 999.00},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 49.99},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 79.00}
    ]
class ProductIndexView(View):
    template_name = 'products/index.html'
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)
class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product = Product.products[int(id) - 1]
        except (IndexError, ValueError):
            return HttpResponseRedirect(reverse('home'))

        viewData = {
            "title": f"{product['name']} - Online Store",
            "subtitle": f"{product['name']} - Product information",
            "product": product
        }

        return render(request, self.template_name, viewData)
    
class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("The price must be greater than 0.")
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'
    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)
    
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            return redirect('product_success')  # 👈 redirige a la nueva vista
        else:
            return render(request, self.template_name, {
                "title": "Create product",
                "form": form
            }) 
        
class ProductSuccessView(TemplateView):
    template_name = 'products/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Product Created"
        context["message"] = "Product created successfully!"
        return context
