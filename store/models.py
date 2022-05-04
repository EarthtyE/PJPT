from distutils.command.upload import upload
import email
from email.mime import image
from itertools import product
from lib2to3.pgen2 import token
from tabnanny import verbose
from unicodedata import category, name
from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=255,unique=True)
    slug=models.SlugField(max_length=255,unique=True)
        
    def __str__(self):
        return self.name

    class Meta : #ตกแต่งหน้าแอด
        ordering=('name',) # เรียงลำดับตัวอักษร
        verbose_name='หมวดหมู่สินค้า' #เอาไว้เปลี่ยนชื่อต่างๆในแอดมินให้ทำงานง่ายขึ้น
        verbose_name_plural="ข้อมูลประเภทสินค้า"
        
    def get_url(self):
        return reverse('product_by_category',args=[self.slug])

class Product(models.Model):
    name=models.CharField(max_length=255,unique=True)
    slug=models.SlugField(max_length=255,unique=True)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.CASCADE) #on_delete=models.CASCADE ลบทั้งความสัมพันธ์
    images=models.ImageField(upload_to="product",blank=True) #blank=True ใส่รูปตามหลังได้
    stock=models.IntegerField()
    available=models.BooleanField(default=True) #สถานะใช้งานพร้อมไม่พร้อมไรงี้
    created=models.DateTimeField(auto_now_add=True) #วันที่สต๊อก
    updated=models.DateTimeField(auto_now=True) #เมื่อมีการแก้ไขค่อยขึ้นวันที่
    
    def __str__(self):
        return self.name
    
    class Meta : #ตกแต่งหน้าแอด
        ordering=('name',) # เรียงลำดับตัวอักษร
        verbose_name='สินค้า' #เอาไว้เปลี่ยนชื่อต่างๆในแอดมินให้ทำงานง่ายขึ้น
        verbose_name_plural="ข้อมูลสินค้า"
        
    def get_url(self):
        return reverse('productDetils',args=[self.category.slug,self.slug])
    
    
class Cart(models.Model): #ตะกร้าสินค้า
    cart_id=models.CharField(max_length=255,blank=True) #รหัสตะกร้าสินค้า
    date_added=models.DateTimeField(auto_now_add=True) #วันเวลาที่หบิย
        
    def __str__(self):
        return self.cart_id
        
    class Meta:
        db_table='cart' #บันทึกลงดาต้าเบส
        ordering=('date_added',) #เรียงลำดับตามวันเวลา
        verbose_name='ตะกร้าสินค้า' #แปลงชื่อในหน้าแอดมิน
        verbose_name_plural="ข้อมูลตะกร้าสินค้า"
    
class CartItem(models.Model): #รายการสินค้าในตะกร้า
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity=models.IntegerField() #เก็บจำนวนที่เพิ่มลงตะกร้า
    active=models.BooleanField(default=True) #เช็คสถานะว่ารายการสินค้าตัวไหนใช่ได้
        
    class Meta:
        db_table='cartItem'
        verbose_name='รายการสินค้าในตะกร้า' 
        verbose_name_plural="ข้อมูลรายการสินค้าในตะกร้า"
           
    def sub_total(self):#ฟังชั่นหาผลรวมสินค้าแต่ละอย่างรวมกัน
            return self.product.price * self.quantity
        
    def __str__(self):
        return self.product.name
    
class Order(models.Model):
    name=models.CharField(max_length=255,blank=True)
    address=models.CharField(max_length=255,blank=True)
    city=models.CharField(max_length=255,blank=True)
    postcode=models.CharField(max_length=255,blank=True)
    total=models.DecimalField(max_digits=10,decimal_places=2)
    email=models.EmailField(max_length=250,blank=True)
    token=models.CharField(max_length=255,blank=True)
    created=models.DateTimeField(auto_now_add=True) 
    updated=models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='Order'
        ordering=('id',)
    def __str__(self):
        return str(self.id)
    
class OrderItem(models.Model):
    product=models.CharField(max_length=250)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True) 
    updated=models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='OrderItem'
        ordering=('order',)
    def sub_total(self):
        return self.quantity*self.price
    
    def __str__(self):
        return self.product
    