from django.db import models

from core.models import TimeStampedModel


class Category(models.Model):

    """ Product's Category (상품 카테고리) """

    name = models.CharField(max_length=50)
    owner = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(TimeStampedModel):

    """ Product's Information Model (상품 모델)"""

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    price = models.IntegerField(blank=True, default=0)
    qty = models.IntegerField(blank=True, default=0)
    soldPrice = models.IntegerField(blank=True, default=0)
    soldNumber = models.IntegerField(blank=True, default=0)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, null=True)
    owner = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
