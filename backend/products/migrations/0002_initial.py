import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shoppingcart",
            name="owner",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_cart",
                to=settings.AUTH_USER_MODEL,
                verbose_name="владелец корзины",
            ),
        ),
        migrations.AddField(
            model_name="review",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_review",
                to="products.product",
                verbose_name="продукт",
            ),
        ),
        migrations.AddField(
            model_name="review",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_review",
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="products.category",
                verbose_name="категория",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="images",
            field=models.ManyToManyField(
                blank=True,
                through="products.ImageProduct",
                to="products.image",
                verbose_name="список изображений",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AddField(
            model_name="orderproductlists",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_in_order",
                to="products.order",
                verbose_name="связанные заказы",
            ),
        ),
        migrations.AddField(
            model_name="orderproductlists",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="order_with_product",
                to="products.product",
                verbose_name="связанные продукты",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="product_list",
            field=models.ManyToManyField(
                related_name="product_in_order",
                through="products.OrderProductLists",
                to="products.product",
                verbose_name="продукт в заказе",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_orders",
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AddField(
            model_name="imageproduct",
            name="image",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="products.image",
            ),
        ),
        migrations.AddField(
            model_name="imageproduct",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="products.product",
            ),
        ),
        migrations.AddField(
            model_name="image",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AddField(
            model_name="favorite",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_favorite",
                to="products.product",
                verbose_name="продукт",
            ),
        ),
        migrations.AddField(
            model_name="favorite",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_favorite",
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AddConstraint(
            model_name="review",
            constraint=models.UniqueConstraint(
                fields=("user", "product"),
                name="rating_allowed_once",
            ),
        ),
        migrations.AddConstraint(
            model_name="orderproductlists",
            constraint=models.UniqueConstraint(
                fields=("order", "product"),
                name="unique_order",
            ),
        ),
        migrations.AddConstraint(
            model_name="favorite",
            constraint=models.UniqueConstraint(
                fields=("user", "product"),
                name="unique favorite",
            ),
        ),
    ]
