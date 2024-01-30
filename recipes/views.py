from django.db.models import F
from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Recipe, RecipeProduct


def add_product_to_recipe(request):
    """Функция добавляет к указанному рецепту указанный продукт с указанным
    весом. Если в рецепте уже есть такой продукт, то функция должна поменять
    его вес в этом рецепте на указанный. """
    recipe_id = request.GET.get('recipe_id')
    product_id = request.GET.get('product_id')
    weight = request.GET.get('weight')

    if not all([recipe_id, product_id, weight]):
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    try:
        weight = int(weight)
        recipe = Recipe.objects.get(id=recipe_id)
        product = Product.objects.get(id=product_id)

        obj, created = RecipeProduct.objects.update_or_create(
            recipe=recipe,
            product=product,
            defaults={'weight': weight}
        )

        return JsonResponse({'success': True, 'created': created})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def cook_recipe(request):
    """Функция увеличивает на единицу количество приготовленных блюд для
    каждого продукта, входящего в указанный рецепт. """
    recipe_id = request.GET.get('recipe_id')

    if not recipe_id:
        return JsonResponse(
            {'error': 'Не указан recipe_id в теле запроса'},
            status=400)

    try:
        # Получаем все объекты RecipeProduct, связанные с данным рецептом.
        recipe_products = RecipeProduct.objects.filter(recipe_id=recipe_id)

        if not recipe_products.exists():
            return JsonResponse(
                {'error': 'Не найдены продукты по предоставленному рецепту'},
                status=404)

        # Увеличиваем значение times_cooked для каждого продукта в рецепте.
        for recipe_product in recipe_products:
            Product.objects.filter(
                id=recipe_product.product_id
            ).update(
                times_cooked=F('times_cooked') + 1
            )

        return JsonResponse({
            'success': True,
            'message': 'Продукты этого рецепта приготовлены +1 раз'
        })
    except Recipe.DoesNotExist:
        return JsonResponse({'error': 'Recipe does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def show_recipes_without_product(request):
    """Представление в которых отображены id и названия всех рецептов,
    в которых указанный продукт отсутствует, или присутствует в количестве
    меньше 10 грамм """
    product_id = request.GET.get('product_id')

    if not product_id:
        return JsonResponse({
            'error': 'Не указан product_id в теле запроса'},
            status=400)

    product = Product.objects.get(id=product_id)
    recipes_with_product = RecipeProduct.objects.filter(
        product_id=product_id,
        weight__gte=10).values_list('recipe_id', flat=True)
    recipes = Recipe.objects.exclude(id__in=recipes_with_product)

    context = {
        'recipes': recipes,
        'product': product,
    }

    return render(request, 'recipes_without_product.html', context)
