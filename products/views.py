from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from utils.pagination import paginate_queryset  # make sure path is correct
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Product
from .forms import ProductForm

class AdminRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'You must be logged in to access this page.')
            return HttpResponseRedirect(reverse_lazy('login'))
        if not hasattr(request.user, 'role') or request.user.role != 'admin':
            messages.warning(request, 'No permission to access this page.')
            return HttpResponseRedirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)

class ProductListView(AdminRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = None  # Disable built-in pagination since we use custom paginate_queryset

    def get_queryset(self):
        queryset = Product.objects.filter(user=self.request.user)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(name__icontains=search))
        return queryset.order_by('-date_added')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # --- apply your global paginator ---
        page_obj, products = paginate_queryset(self.request, context['object_list'])

        context['products'] = products          # override object_list
        context['page_obj'] = page_obj          # override page object
        context['paginator'] = page_obj.paginator  # ensure template sees paginator
        context['is_paginated'] = True
        # ------------------------------------

        context['search_term'] = self.request.GET.get('search', '')
        return context


class ProductCreateView(AdminRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Product added successfully.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Form error. Please correct the fields.')
        return super().form_invalid(form)

class ProductUpdateView(AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        # Only allow edit if owner or superuser
        return Product.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Product updated successfully.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Form error. Please correct the fields.')
        return super().form_invalid(form)

class ProductDeleteView(AdminRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        # Only allow delete if owner or superuser
        return Product.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Product deleted successfully.')
        return super().delete(request, *args, **kwargs)