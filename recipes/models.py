from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    times_cooked = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, through='RecipeProduct')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeProduct(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.IntegerField()

    class Meta:
        unique_together = ('recipe', 'product')
