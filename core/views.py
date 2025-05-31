from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
import MySQLdb
from django.db.models import Prefetch
from .models import Product,User,Admin,Cart,P_order,Order
from datetime import date
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import random
 


def a_admin_home(request):
    if  'admin_id' in request.session: 
        new_order=Order.objects.filter(p_status="dispatched")
        order_history=Order.objects.filter(p_status="Delivered")
        return render(request, 'a_admin_home.html',{'new_order':new_order,'order_history':order_history})        
    else:
        return redirect('../login/')

def a_users(request):
    if  'admin_id' in request.session:   
        users=User.objects.all()
        return render(request, 'a_users.html',{'users':users})    
    else:
        return redirect('../login/')


def a_product(request):
    if  'admin_id' in request.session:
        data1=Product.objects.filter(p_cat='Fashion')
        data2=Product.objects.filter(p_cat='Electronic')
        data3=Product.objects.filter(p_cat='Jewellery')
        return render(request, 'a_product.html',{'data1':data1,'data2':data2,'data3':data3})         
    else:
        return redirect('../login/')

def a_add_product(request):
    if  'admin_id' in request.session:
        if request.method == "POST":
            image = request.FILES.get('image')
            p_name = request.POST['pname']
            p_price = request.POST.get('pprice') 
            p_rating = round(random.uniform(2, 5))
            p_details = request.POST.get('p_details')
            p_cat = request.POST.get('pcat')             
            lines = p_details.split('\n')
            processed_lines = [f'&#x2022; {line.strip()}' for line in lines if line.strip()]
            p_det = '<br>'.join(processed_lines)
            # Save user
            Product.objects.create(
                p_name=p_name,
                p_price=p_price,
                p_rating=p_rating,
                p_det=p_det,
                p_cat=p_cat,
                image=image
            )
            return redirect('../a_product/') 
        return render(request, 'a_add_product.html')        
    else:
        return redirect('../login/')

def a_edit_product(request):
    if  'admin_id' in request.session:
        id_value = request.GET.get('id')
        prod = Product.objects.filter(id=id_value).first()
        if prod:
          
            prod.p_det = prod.p_det.replace('<br>', '\n').replace('<br/>', '\n').replace('&#x2022; ', '')

        product = get_object_or_404(Product, id=id_value)

        if request.method == 'POST':
           
            product.p_name = request.POST.get('pname')
            product.p_price = request.POST.get('pprice')
            product.p_rating = request.POST.get('prating')   
            p_details= request.POST.get('p_details')
            lines = p_details.split('\n')
            processed_lines = [f'&#x2022; {line.strip()}' for line in lines if line.strip()]
            p_det = '<br>'.join(processed_lines)
            product.p_det = p_det
            product.p_cat = request.POST.get('pcat')

            if request.FILES.get('image'):
                product.image = request.FILES['image']

            product.save()
            return redirect('../a_product/') 
        return render(request, 'a_edit_product.html', {'id_value': id_value,'data': [prod] if prod else [],})
        
    else:
        return redirect('../login/')

def a_delete_product(request):
    if  'admin_id' in request.session:
        print("hi")
        id_value = request.GET.get('id')
        product = get_object_or_404(Product, id=id_value)
        product.delete()
        return redirect('../a_product/')
        
    else:
        return redirect('../login/')

def a_order_details(request):
    if  'admin_id' in request.session:
        order_id = request.GET.get('id')         
        order_det=P_order.objects.filter(o_id_id=order_id)
        order=Order.objects.filter(id=order_id)

        if request.method == "POST":
            e_otp = request.POST.get('otp') 
            order_otp=request.session.get(f'otp_{order_id}')
            print('2')
            print(order_otp)
            print(e_otp)
            
            if int(e_otp)==int(order_otp):
                del request.session[f'otp_{order_id}']
                order = get_object_or_404(Order, id=order_id)
                order.d_date = date.today()
                order.p_status = "Delivered"
                order.save()
                print('1')
                return redirect('../a_admin_home/')
            
                 

        return render(request, 'a_order_details.html', {'order': order_det,'order1':order})       
    else:
        return redirect('../login/')


def home(request):
    image_list = [f"{i}.png" for i in range(1, 13)]
    if 'user_id' in request.session:          
        return render(request, 'home.html',{"login":"login",'image_list': image_list})
    return render(request, 'home.html',{'image_list': image_list})


def product(request):
    id_value = request.GET.get('id')
    if id_value=="1":
        products = Product.objects.filter(p_cat="Fashion")
    if id_value=="2":
        products = Product.objects.filter(p_cat="Electronic")
    if id_value=="3":
        products = Product.objects.filter(p_cat="Jewellery")
    
    if 'user_id' in request.session:
        u_id=int(request.session['user_id'])
        added = Cart.objects.filter(u_id_id=u_id).values_list('p_id_id', flat=True)
        if added:
            return render(request, 'product.html', {'products': products,'added':added,"login":"login"})
        else:
            return render(request, 'product.html', {'products': products,"login":"login"})

    return render(request, 'product.html', {'products': products})

def product_det(request):
    id_value = request.GET.get('id')
    item=Product.objects.filter(id=id_value)
    if 'user_id' in request.session:
        u_id=int(request.session['user_id'])
        added = Cart.objects.filter(u_id_id=u_id).values_list('p_id_id', flat=True)
        if added:
            return render(request, 'product_det.html', {'item': item,'added':added,"login":"login"})
        else:
            return render(request, 'product_det.html', {'item': item,"login":"login"})

    return render(request, 'product_det.html', {'item': item})

@csrf_exempt
def checkout(request):
    if 'user_id' in request.session: 
        if request.method == "POST": 
            user_id = request.session.get('user_id')
            cart_items = Cart.objects.filter(u_id=user_id)
            user=User.objects.filter(id=user_id)
            total = 0
            cart_data = []

            for item in cart_items:
                qty = int(request.POST.get(f'quantity_{item.id}', 1))
                price = item.p_id.p_price  
                subtotal = price * qty
                total += subtotal

                cart_data.append({
                    'name': item.p_id.p_name, 
                    'p_id': item.p_id_id,
                    'price': price,
                    'quantity': qty,
                    'subtotal': subtotal
                })
                print(cart_data)
            return render(request, 'checkout.html', {
                'total': total,
                'cart_data': cart_data,
                'user':user ,
                'login':'login'
            })
    else:
        return redirect('../login/')


def order(request):
    if 'user_id' not in request.session:
        return redirect('../login/')
    user_id = request.session.get('user_id')

    if request.method == "POST":
        
        user_name = request.POST.get('name')
        d_add = request.POST.get('add')
        location = request.POST.get('location')
        total_a = request.POST.get('total')

        user = User.objects.get(id=user_id) 
        order_obj = Order.objects.create(
            o_date=date.today(),
            d_name=user_name,
            d_add=d_add,
            d_location=location,
            total_amout=total_a,
            p_status="dispatched",
            u_id_id=user_id
        )
        otp = random.randint(1000, 9999) 
        request.session[f'otp_{order_obj.id}'] = otp

        p_ids = request.POST.getlist('p_id[]')
        quantities = request.POST.getlist('quantity[]')
        subtotals = request.POST.getlist('subtotal[]')

        print(p_ids)
        print(quantities)
       

        for p_id, quantity ,subtotal  in zip(p_ids, quantities,subtotals):
            try:
                product = Product.objects.get(id=p_id)
                P_order.objects.create(
                    o_id_id=order_obj.id,
                    p_id_id=product.id,
                    p_name=product.p_name,
                    p_image=product.image,
                    p_quantity=quantity,
                    p_subtital=subtotal,
                    p_price=product.p_price
                )
            except Product.DoesNotExist:
                continue
        product = get_object_or_404(Cart, u_id=user_id)
        product.delete()
           
    orders = Order.objects.filter(u_id_id=user_id, p_status="dispatched")
    order_history = Order.objects.filter(u_id_id=user_id, p_status="Delivered")
    order_history_product = P_order.objects.filter(o_id__in=order_history)

    for order in orders:
        order.otp = request.session.get(f'otp_{order.id}')

    return render(request, 'order.html', {
        "orders": orders,
        "order_history": order_history,
        "order_history_product": order_history_product,
        "login": "login"
    })

     


    return redirect('../cart/')

def order_details(request):
    if 'user_id' in request.session: 
        order_id = request.GET.get('id')         
        order_det=P_order.objects.filter(o_id_id=order_id)
        order=Order.objects.filter(id=order_id)
        return render(request, 'order_details.html', {'order': order_det,'order1':order,'login':'login'})   
    else:
        return redirect('../login/')
 
def create_account(request): 
    if request.method == "POST":
        name = request.POST['u_name']
        phone = request.POST['u_phone']
        address = request.POST['u_add']
        gender = request.POST['u_gender']
        email = request.POST['u_email']
        pwd = request.POST['u_pwd']
 
        User.objects.create(
            u_name=name,
            u_phone=phone,
            u_add=address,
            u_gender=gender,
            u_email=email,
            u_pwd=pwd
        )
        if 'user_id' in request.session:
            return render(request, 'create_account.html', {'msg': 'User registered successfully',"login":"login"})
        return render(request, 'create_account.html', {'msg': 'User registered successfully'})
    return render(request,'create_account.html')

def user_home(request):
    if 'user_id' in request.session:
        return render(request, 'user_home.html',{"login":"login"})

    return render(request, 'user_home.html')

def cart(request):
    if 'user_id' in request.session:
        u_id=int(request.session['user_id'])
  
        query = """
        SELECT product.*, cart.* 
        FROM product, cart 
        WHERE product.id = cart.p_id_id 
        AND product.id IN (
            SELECT p_id_id FROM cart WHERE u_id_id = %s
        );
        """

        with connection.cursor() as c:
            c.execute(query, [u_id])
            items = c.fetchall()
            columns = [col[0] for col in c.description]   
 
        results = [dict(zip(columns, row)) for row in items]

        return render(request, 'cart.html', {'items': results,'login':'login'})
    else:
        return redirect('../login/')


def add_to_cart(request):
    if 'user_id' in request.session:            
        u_id=int(request.session['user_id'])
        product_id = request.GET.get('id')  
        product = Product.objects.get(id=product_id)
        user = User.objects.get(id=u_id) 
        if not Cart.objects.filter(u_id=user, p_id=product).exists():
            Cart.objects.create(
                u_id=user,
                p_id=product,
                c_date=date.today(),
                p_status='Avilable'
            )
            return redirect('../cart/')
    else:
        return redirect('../login/')

def delete_from_cart(request):
    if 'user_id' in request.session:            
      
        cart_id = request.GET.get('id')   
 
        product = get_object_or_404(Cart, id=cart_id)
        product.delete()

        return redirect('../cart/') 
    else:
        return redirect('../login/')


def login(request):
    if 'user_id' in request.session:
        return redirect('/')
    if  'admin_id' in request.session:
        return redirect('../a_admin_home/')
    else:   
        if(request.POST):
            email = request.POST['email']
            pwd = request.POST['pass']

           
            user = User.objects.filter(u_email=email, u_pwd=pwd).first()
            if user:
                request.session['user_id'] = user.id
                return redirect('../cart/')
            
             
            admin = Admin.objects.filter(a_email=email, a_pwd=pwd).first()
            if admin:
                request.session['admin_id'] = admin.id
                return redirect('../a_admin_home')

            messages.error(request, "Invalid credentials") 
    
            return render(request, 'login.html')
    
    return render(request, 'login.html')

def log_out(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    elif 'admin_id' in request.session:
        del request.session['admin_id']
    return redirect('../login') 
