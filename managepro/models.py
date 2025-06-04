from django.db import models

class Archiveproduct(models.Model):
    archiveid = models.AutoField(primary_key=True)
    productid = models.IntegerField(blank=True, null=True)
    productname = models.CharField(max_length=255, blank=True, null=True)
    categoryid = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    expirydate = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    datereceived = models.DateField(blank=True, null=True)
    warehouseid = models.IntegerField(blank=True, null=True)
    archivedat = models.DateTimeField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'archiveproduct'
        verbose_name = 'Архив продуктов'
        verbose_name_plural = "Архив продуктов"

    def __str__(self):
        return self.productname or f"Archiveproduct {self.archiveid}"


class Category(models.Model):
    categoryid = models.AutoField(primary_key=True)
    categoryname = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'category'
        verbose_name = 'Категории'
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.categoryname


class Discount(models.Model):
    discountid = models.AutoField(primary_key=True)
    discountpercentage = models.DecimalField(max_digits=5, decimal_places=2)
    activationcondition = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discount'
        verbose_name = 'Скидки'
        verbose_name_plural = "Скидки"

    def __str__(self):
        return f"{self.discountpercentage}%"


class Notification(models.Model):
    notificationid = models.AutoField(primary_key=True)
    productid = models.ForeignKey('Product',on_delete=models.CASCADE,db_column='productid',blank=True,null=True)
    warehouseid = models.ForeignKey('Warehouse', models.DO_NOTHING, db_column='warehouseid', blank=True, null=True)
    notificationtype = models.TextField(blank=True, null=True)
    creationdate = models.DateTimeField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notification'
        verbose_name = 'Уведомления'
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return f"Notification {self.notificationid}"


class Product(models.Model):
    productid = models.AutoField(primary_key=True)
    productname = models.CharField(max_length=255)
    categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='categoryid', blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    expirydate = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    datereceived = models.DateTimeField(blank=True, null=True)
    warehouseid = models.ForeignKey('Warehouse', models.DO_NOTHING, db_column='warehouseid', blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'
        verbose_name = 'Продукты'
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.productname


class ProductDiscount(models.Model):
    productid = models.ForeignKey(
        Product,
        models.DO_NOTHING,
        db_column='productid',
        primary_key=True,
        verbose_name="Продукт"
    )
    discountid = models.ForeignKey(
        Discount,
        models.DO_NOTHING,
        db_column='discountid',
        verbose_name="Скидка"
    )

    class Meta:
        managed = False
        db_table = 'product_discount'
        verbose_name = 'Продукт — Скидка'
        verbose_name_plural = 'Продукты — Скидки'
        # Указываем составной ключ (для инфы, Django его не применит на уровне ORM)
        unique_together = (('productid', 'discountid'),)

    def __str__(self):
        return f"{self.productid} — {self.discountid}"


class Report(models.Model):
    reportid = models.AutoField(primary_key=True)
    creationdate = models.DateTimeField(blank=True, null=True)
    reporttype = models.TextField(blank=True, null=True)
    format = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report'
        verbose_name = 'Отчёты'
        verbose_name_plural = "Отчёты"

    def __str__(self):
        return f"Report {self.reportid} ({self.reporttype})"


class ReportProduct(models.Model):
    reportid = models.ForeignKey(Report, models.DO_NOTHING, db_column='reportid')
    productid = models.ForeignKey(Product, models.DO_NOTHING, db_column='productid')

    class Meta:
        managed = False
        db_table = 'report_product'
        unique_together = (('reportid', 'productid'),)
        verbose_name = 'Продукты - отчёты'
        verbose_name_plural = "Продукты - отчёты"

    def __str__(self):
        return f"ReportProduct: Report {self.reportid_id} - Product {self.productid_id}"


class Users(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'users'
        verbose_name = 'Пользователи'
        verbose_name_plural = "Пользователи"



    def __str__(self):
        return self.username


class Warehouse(models.Model):
    warehouseid = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)
    minimumstocklevel = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'warehouse'
        verbose_name = 'Склады'
        verbose_name_plural = "Склады"


    def __str__(self):
        return self.address