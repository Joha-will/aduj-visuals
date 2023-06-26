from django.db import models

product_sizes = (

    ('4 x 6 inches', '4 x 6 inches'),
    ('5 x 7 inches', '5 x 7 inches'),
    ('8 x 10 inches', '8 x 10 inches'),
    ('8.5 x 11 inches', '8.5 x 11 inches'),
)


class Category(models.Model):
    """ Category model"""
    category_name = models.CharField(max_length=254)

    class Meta:
        """ Override plural name """
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name


class Product(models.Model):
    """ Product model """
    name = models.CharField(max_length=254,)
    model_name = models.CharField(max_length=254, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 null=True, blank=True,)
    description = models.TextField(blank=True)
    size = models.CharField(max_length=20, choices=product_sizes,
                            default='4 x 6 inches')
    image = models.ImageField(null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    class Meta:
        """ Override plural name """
        verbose_name_plural = "products"

    def __str__(self):
        return self.name
