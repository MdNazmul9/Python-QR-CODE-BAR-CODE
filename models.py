
from re import S
from django.db import models
from datetime import datetime
from models.models import Color
from django.contrib.postgres.fields import ArrayField

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
# from django.contrib.postgres.fields import ArrayField
import treepoem




class Company(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    class Meta:
        ordering= ("-id",)

class Category(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    class Meta:
        ordering= ("-id",)

class Product(models.Model):
    product_choice = (
        ('serial_No', 'serial_no'),
        ('Bar_Code', 'bar_code'),
        ('No_Bar_Code', 'no_bar_code'),
    )
    year_month_day_choice = (
        ('YEAR', 'Year'),
        ('MONTH', 'Month'),
        ('WEEK', 'Week'),
        ('DAY', 'Day'),
    )
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=250)
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)

    picture_path = models.ImageField(upload_to='product/', blank=True, null=True)
    pack_size = models.CharField(max_length=250, null=True, blank=True)
    warning_qty = models.PositiveIntegerField()
    model_no = models.CharField(max_length=250, null=True, blank=True)
    unit_type = models.CharField(max_length=250, blank=True, null=True)
    short_qty = models.PositiveIntegerField(default=0)
    # Photo_path = models.ImageField(upload_to='product/')
    box_qty = models.PositiveIntegerField(default=1)
    product_type = models.CharField(max_length=20, choices=product_choice)

    extra_field = models.JSONField(blank=True, null=True, default=dict)

    # extra_field = ArrayField(models.JSONField(null=True, blank=True, default=dict))
    # extra_field = ArrayField(ArrayField(models.CharField(max_length=100, blank=True, null=True)))
    compressor_warrenty = models.PositiveIntegerField(default=0)
    compressor_warrenty_duration = models.CharField(max_length=20, choices=year_month_day_choice, null=True, blank=True)

    panel_warrenty = models.PositiveIntegerField(default=0)
    panel_warrenty_duration = models.CharField(max_length=20, choices=year_month_day_choice, null=True, blank=True)

    motor_warrenty = models.PositiveIntegerField(default=0)
    motor_warrenty_duration = models.CharField(max_length=20, choices=year_month_day_choice, null=True, blank=True)

    spare_parts_warrenty = models.PositiveIntegerField(default=0)
    spare_warrenty_duration = models.CharField(max_length=20, choices=year_month_day_choice,  null=True, blank=True)

    service_warrenty = models.PositiveIntegerField(default=0)
    service_warrenty_duration = models.CharField(max_length=20, choices=year_month_day_choice, null=True, blank=True)

    extra_warrenty = models.JSONField(blank=True, null=True, default=dict)

    qrcode_image = models.ImageField(blank=True, null=True, upload_to='qrcode/')
    barcode_image = models.ImageField(blank=True, null=True, upload_to='barcode/')

    
    def __str__(self):
        return self.name


    class Meta:
        ordering = ('name',)

    def save(self, *args, **kwargs):
        #------------QR CODE---------------
        qrcode_img = treepoem.generate_barcode(
            barcode_type="qrcode",
            data= self.code,
            options= {"includetext": True},
            # Options= "includetext textfont=Times-Roman textsize=9",
        ) 
        # canvas = Image.new('RGB', (102, 102), 'white')
        canvas = Image.new('RGB', qrcode_img.size, 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.code}' + '.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qrcode_image.save(fname, File(buffer), save=False)
        canvas.close()

        #------------------ BAR CODE ---------
        barcode_img = treepoem.generate_barcode(
            barcode_type="code128",
            data= self.code,
            options= {"includetext": True, "height":0.2, "showborder":True, "borderwidth":1, "borderbottom":8},
            # options= {"includetext": True,  "width":0.1, "height":0.1, "showborder":True, "borderwidth":1},
            )
        canvas_img = Image.new('RGB',barcode_img.size, 'white')
        # canvas_img = Image.new('RGB',(242,44), 'white')
        draw_img = ImageDraw.Draw(canvas_img)
        canvas_img.paste(barcode_img)
        fname_path = f'bar_code-{self.code}' + '.png'
        buffer_img = BytesIO()
        canvas_img.save(buffer_img, 'PNG')
        
        self.barcode_image.save(fname_path, File(buffer_img), save=False)
        canvas_img.close()
        super().save(*args, **kwargs)