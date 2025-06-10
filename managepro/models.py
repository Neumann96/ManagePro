from django.db import models

class Archiveproduct(models.Model):
    archiveid = models.AutoField(primary_key=True, verbose_name='Идентификатор архива')
    productid = models.IntegerField(blank=True, null=True, verbose_name='Идентификатор продукта')
    productname = models.CharField(max_length=255, blank=True, null=True, verbose_name='Название продукта')
    categoryid = models.IntegerField(blank=True, null=True, verbose_name='Идентификатор категории')
    quantity = models.IntegerField(blank=True, null=True, verbose_name='Количество')
    expirydate = models.DateField(blank=True, null=True, verbose_name='Срок годности')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    datereceived = models.DateField(blank=True, null=True, verbose_name='Дата получения')
    warehouseid = models.IntegerField(blank=True, null=True, verbose_name='Идентификатор склада')
    archivedat = models.DateTimeField(blank=True, null=True, verbose_name='Дата архивации')
    reason = models.TextField(blank=True, null=True, verbose_name='Причина')

    class Meta:
        managed = False
        db_table = 'archiveproduct'
        verbose_name = 'Архив продуктов'
        verbose_name_plural = "Архив продуктов"

    def __str__(self):
        return self.productname or f"Archiveproduct {self.archiveid}"


class Category(models.Model):
    categoryid = models.AutoField(primary_key=True, verbose_name='Идентификатор категории')
    categoryname = models.CharField(max_length=255, verbose_name='Название категории')

    class Meta:
        managed = False
        db_table = 'category'
        verbose_name = 'Категории'
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.categoryname


class Discount(models.Model):
    discountid = models.AutoField(primary_key=True, verbose_name='Идентификатор скидки')
    discountpercentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Процент скидки')
    activationcondition = models.TextField(blank=True, null=True, verbose_name='Условие активации')
    status = models.TextField(blank=True, null=True, verbose_name='Статус')

    class Meta:
        managed = False
        db_table = 'discount'
        verbose_name = 'Скидки'
        verbose_name_plural = "Скидки"

    def __str__(self):
        return f"{self.discountpercentage}%"


class Notification(models.Model):
    notificationid = models.AutoField(primary_key=True, verbose_name='Идентификатор уведомления')
    productid = models.ForeignKey('Product', on_delete=models.CASCADE, db_column='productid', blank=True, null=True,
                                  verbose_name='Продукт')
    warehouseid = models.ForeignKey('Warehouse', models.DO_NOTHING, db_column='warehouseid', blank=True, null=True,
                                    verbose_name='Склад')
    notificationtype = models.TextField(blank=True, null=True, verbose_name='Тип уведомления')
    creationdate = models.DateTimeField(blank=True, null=True, verbose_name='Дата создания')
    status = models.TextField(blank=True, null=True, verbose_name='Статус')

    class Meta:
        managed = False
        db_table = 'notification'
        verbose_name = 'Уведомления'
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return f"Notification {self.notificationid}"


class Product(models.Model):
    productid = models.AutoField(primary_key=True, verbose_name='Идентификатор продукта')
    productname = models.CharField(max_length=255, verbose_name='Название продукта')
    categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='categoryid', blank=True, null=True,
                                   verbose_name='Категория')
    quantity = models.IntegerField(blank=True, null=True, verbose_name='Количество')
    expirydate = models.DateField(blank=True, null=True, verbose_name='Срок годности')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    datereceived = models.DateTimeField(blank=True, null=True, verbose_name='Дата получения')
    warehouseid = models.ForeignKey('Warehouse', models.DO_NOTHING, db_column='warehouseid', blank=True, null=True,
                                    verbose_name='Склад')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name='Изображение')


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
    reportid = models.AutoField(primary_key=True, verbose_name='Идентификатор отчёта')
    creationdate = models.DateTimeField(blank=True, null=True, verbose_name='Дата создания')
    reporttype = models.TextField(blank=True, null=True, verbose_name='Тип отчёта')
    format = models.TextField(blank=True, null=True, verbose_name='Формат')

    class Meta:
        managed = False
        db_table = 'report'
        verbose_name = 'Отчёты'
        verbose_name_plural = "Отчёты"

    def __str__(self):
        return f"Report {self.reportid} ({self.reporttype})"


class ReportProduct(models.Model):
    reportid = models.ForeignKey(Report, models.DO_NOTHING, db_column='reportid', verbose_name='Отчёт')
    productid = models.ForeignKey(Product, models.DO_NOTHING, db_column='productid', verbose_name='Продукт')


    class Meta:
        managed = False
        db_table = 'report_product'
        unique_together = (('reportid', 'productid'),)
        verbose_name = 'Продукты - отчёты'
        verbose_name_plural = "Продукты - отчёты"

    def __str__(self):
        return f"ReportProduct: Report {self.reportid_id} - Product {self.productid_id}"


class Users(models.Model):
    userid = models.AutoField(primary_key=True, verbose_name='Идентификатор пользователя')
    username = models.CharField(unique=True, max_length=255, verbose_name='Имя пользователя')
    password = models.CharField(max_length=255, verbose_name='Пароль')
    role = models.CharField(max_length=50, verbose_name='Роль')

    class Meta:
        managed = False
        db_table = 'users'
        verbose_name = 'Пользователи'
        verbose_name_plural = "Пользователи"



    def __str__(self):
        return self.username


class Warehouse(models.Model):
    warehouseid = models.AutoField(primary_key=True, verbose_name='Идентификатор склада')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    minimumstocklevel = models.IntegerField(blank=True, null=True, verbose_name='Минимальный уровень запасов')


    class Meta:
        managed = False
        db_table = 'warehouse'
        verbose_name = 'Склады'
        verbose_name_plural = "Склады"

    def __str__(self):
        return self.address