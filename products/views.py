from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Category, Comment, Product
from .forms import NewCommentForm


def products_list_view(request):
    category = request.GET.get('category')

    if category is not None:
        products = Product.objects.filter(category__name=category)
    else:
        products = Product.objects.all().order_by('-datetime_created')

    paginator = Paginator(products, 2)
    page_num = request.GET.get('page')

    try:
        products = paginator.page(page_num)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    categories = Category.objects.all()

    return render(request, 'products/products_list.html', {
        'products': products,
        'categories': categories,
    })


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['comment_form'] = NewCommentForm()
        return contex


class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = NewCommentForm

    def form_valid(self, form):
        comment_obj = form.save(commit=False)
        comment_obj.author = self.request.user

        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)
        comment_obj.product = product

        return super().form_valid(form)
