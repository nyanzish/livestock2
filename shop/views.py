from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import Uploadform, Farmerform
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from .models import Item, Order, OrderItem
# Create your views here.

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
def post_product(request):

    form = Uploadform()
    if request.method == 'POST':
        form = Uploadform(request.POST, request.FILES)
        if form.is_valid():
            user_pr = form.save(commit=False)
            user_pr.image = request.FILES['image']
            file_type = user_pr.image.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                return render(request, 'shop/error.html')
            user_pr.save()
            return render(request, 'shop/product2.html', {'user_pr': user_pr})
    context = {"form": form,}
    return render(request, 'shop/farmer.html', context)

def reg_farmer(request):

    form = Farmerform()
    if request.method == 'POST':
        form = Farmerform(request.POST)
        if form.is_valid():
            user_pr = form.save(commit=False)
            user_pr.save()
            return render(request, 'shop/product.html', {'user_pr': user_pr})
    context = {"form": form,}
    return render(request, 'shop/farmer_register.html', context)

def index(request):
	context={

	'items':Item.objects.all()
	}

	return render(request,'shop/home.html',context)

def cart(request):
	return render(request,'shop/cart.html')

def pay(request):
	return render(request,'shop/pay.html')

@login_required
def checkout(request):
	return render(request,'shop/checkout.html')

def product(request,slug):
    obj= Item.objects.get(id=slug)
	
    context={
        'object':obj
    }
    return render(request,'shop/product2.html',context)

def mymarket(request):
	return render(request,'shop/mymarket.html')

def product_upload(request):
	return render(request,'shop/product_upload.html')


class HomeView(ListView):
    model = Item
    #paginate_by = 10
    template_name = "home.html"

class MarketView(ListView):
    model = Item
    paginate_by = 2
    template_name = "mymarket.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "product2.html"

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, id=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("shop:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("shop:product",slug=slug)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("shop:product",slug=slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, id=slug)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_qs2 = OrderItem.objects.filter(user=request.user)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item= OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "The product was succefully removed from your cart.")
            return redirect("shop:product",slug=slug)
            
            
        else:
            messages.info(request, "Your order doesnot contain this item.")
            return redirect("shop:product",slug=slug)
            
            

    else:
            messages.info(request, "You donot have an order.")
            return redirect("shop:product",slug=slug)
            

@login_required
def remove_single_item_from_cart2(request, slug):
    item = get_object_or_404(Item, slug= slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.quantity -= 1
            order_item.save()
    
            messages.info(request, "This item quantity was updated.")
            return redirect("shop:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("shop:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("shop:product", slug=slug)
            
            
@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item= OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                messages.info(request, "The product was succefully removed from your cart.")
                return redirect("shop:order-summary")
            
            
        else:
            messages.info(request, "Your order doesnot contain this item.")
            return redirect("shop:product",slug=slug)
            
            

    else:
            messages.info(request, "You donot have an order.")
            return redirect("shop:product",slug=slug)
            
