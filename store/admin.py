from csv import list_dialects
from django.contrib import admin
from store.models import Category,Product,Cart,CartItem,Order,OrderItem

class ProductAdmin(admin.ModelAdmin): #จัดตารางแอดมินให้ดูง่าย
    list_display=['name','price','stock','created','updated'] #อันนี้ดึงเรียงตารางทำหน้าเดียวเห็นหมด
    list_editable=['price','stock'] #แก้ไขได้เลยที่หน้าแรกหน้าเดียว
    list_per_page=5 #อันนี้กำหนดจำนวนต่อหน้า
    
class OrderAdmin(admin.ModelAdmin): 
    list_display=['id','name','email','total','token','created','updated']  
    list_per_page=5 
    
class OrderItemAdmin(admin.ModelAdmin): 
    list_display=['order','product','quantity','price','created','updated']  
    list_per_page=5 

admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
