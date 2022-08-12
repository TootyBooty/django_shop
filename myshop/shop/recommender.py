import redis
from django.conf import settings
from .models import Product


#connect to redis
r = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)

class Recommender:

    def get_product_key(self, id):
        return f'product:{id}:purchased_with'

    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # Получаем товары купленные вместе с текущим
                if product_id != with_id:
                    # Увеличиваем их рейтинг
                    # r.zincrby(self.get_product_key(product_id), with_id, amount=1)
                    r.zincrby(self.get_product_key(product_id), 1, with_id)
    
    def suggest_products_for(self, products, max_result=6):
        products_ids = [p.id for p in products]
        if len(products) == 1:
            # Передаг только один товар
            suggestions = r.zrange(
                self.get_product_key(products_ids[0]),
                0, -1, desc=True)[:max_result]
        
        else:
            # Формируем временный ключ хранилища
            flat_ids = ''.join([str(id) for id in products_ids])
            tmp_key = f'tmp_{flat_ids}'
            # Передано несколько товаров, суммируем рейтинги их рекоммендаций
            # Сохраняем суммы во временом ключе
            keys = [self.get_product_key(id) for id in products_ids]
            r.zunionstore(tmp_key, keys)
            # Удаляем ID товаров, которые были переданны в списке
            r.zrem(tmp_key, *products_ids)
            # Получаем товары отсортированные по рейтенгу
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_result]
            # Удаляем временный ключ
            r.delete(tmp_key)

        suggested_products_ids = [int(id) for id in suggestions]

        # Получаем рекомендованные товары и сотрируем их
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
    


            