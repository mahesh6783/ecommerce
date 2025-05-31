from django.db import models

class User(models.Model):
    u_name=models.CharField(max_length=30)
    u_phone=models.CharField(max_length=15)
    u_add=models.CharField(max_length=15)
    u_gender=models.CharField(max_length=15)
    u_email=models.EmailField()    
    u_pwd=models.CharField(max_length=15)   

    class Meta:
        db_table='user'

class Product(models.Model):
    p_name=models.CharField(max_length=30)
    p_price=models.CharField(max_length=30)
    p_rating=models.IntegerField()
    p_det=models.CharField(max_length=500)
    p_cat=models.CharField(max_length=30)
    image = models.ImageField(upload_to='product_images/')

    class Meta:
        db_table='product'

class Cart(models.Model):
    u_id=models.ForeignKey(User, on_delete=models.CASCADE)
    p_id=models.ForeignKey(Product, on_delete=models.CASCADE)
    c_date=models.DateField()
    p_status=models.CharField(max_length=30)

    class Meta:
        db_table='cart'

class Order(models.Model):
    u_id=models.ForeignKey(User, on_delete=models.CASCADE)
    o_date=models.DateField()
    d_date=models.DateField(null=True, blank=True)
    d_name=models.CharField(max_length=30)
    d_add=models.CharField(max_length=50)
    d_location=models.CharField(max_length=500)
    total_amout=models.CharField(max_length=30)
    p_status=models.CharField(max_length=30)
    class Meta:
        db_table='Order'

class P_order(models.Model):
    o_id=models.ForeignKey(Order, on_delete=models.CASCADE)
    p_id=models.ForeignKey(Product, on_delete=models.CASCADE)
    p_name=models.CharField(max_length=30)
    p_image=models.ImageField(upload_to='product_images/')
    p_quantity=models.IntegerField()
    p_price=models.CharField(max_length=30)
    p_subtital=models.CharField(max_length=30)
    class Meta:
        db_table='P_order'



class Admin(models.Model):
    a_email=models.CharField(max_length=30)
    a_pwd=models.CharField(max_length=15)    
    class Meta:
        db_table='admin'
