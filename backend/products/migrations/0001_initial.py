import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import products.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "name",
                    models.CharField(max_length=200, verbose_name="название"),
                ),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "категории",
            },
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "избранное",
                "verbose_name_plural": "избранные",
            },
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=products.models.user_directory_path,
                        verbose_name="изображение",
                    ),
                ),
            ],
            options={
                "verbose_name": "изображение",
                "verbose_name_plural": "изображения",
            },
        ),
        migrations.CreateModel(
            name="ImageProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "изображение в товаре",
                "verbose_name_plural": "изображения в товарах",
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "pay_method",
                    models.CharField(
                        blank=True,
                        choices=[("card", "card"), ("sbp", "sbp")],
                        max_length=4,
                        null=True,
                        verbose_name="метод оплаты",
                    ),
                ),
                (
                    "send_to",
                    models.EmailField(
                        blank=True,
                        max_length=200,
                        verbose_name="куда прислать",
                    ),
                ),
                (
                    "total_cost",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        verbose_name="итоговая цена",
                    ),
                ),
                (
                    "is_paid",
                    models.BooleanField(default=False, verbose_name="оплачен"),
                ),
                (
                    "sale_status",
                    models.BooleanField(default=False, verbose_name="скидка"),
                ),
                (
                    "number_order",
                    models.PositiveIntegerField(
                        default=products.models.Order.get_number_order,
                        editable=False,
                        unique=True,
                        verbose_name="номер заказа",
                    ),
                ),
            ],
            options={
                "verbose_name": "заказ",
                "verbose_name_plural": "заказы",
                "ordering": ("-created",),
            },
        ),
        migrations.CreateModel(
            name="OrderProductLists",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                        ],
                        verbose_name="количество продуктов",
                    ),
                ),
            ],
            options={
                "verbose_name": "товар в заказе",
                "verbose_name_plural": "товары в заказах",
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "name",
                    models.CharField(
                        max_length=60,
                        validators=[
                            django.core.validators.MinLengthValidator(20),
                        ],
                        verbose_name="название бота",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        max_length=1500,
                        validators=[
                            django.core.validators.MinLengthValidator(50),
                        ],
                        verbose_name="описание бота",
                    ),
                ),
                (
                    "video",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="ссылка на видео",
                    ),
                ),
                (
                    "article",
                    models.PositiveIntegerField(
                        default=products.models.Product.get_article,
                        editable=False,
                        unique=True,
                        verbose_name="артикул",
                    ),
                ),
                (
                    "price",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(
                                100000000,
                            ),
                        ],
                        verbose_name="стоимость",
                    ),
                ),
            ],
            options={
                "verbose_name": "товар",
                "verbose_name_plural": "товары",
                "ordering": ("-created",),
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ],
                        verbose_name="рейтинг",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        max_length=500,
                        validators=[
                            django.core.validators.MinLengthValidator(6),
                        ],
                        verbose_name="текст отзыва",
                    ),
                ),
            ],
            options={
                "verbose_name": "отзыв",
                "verbose_name_plural": "отзывы",
                "ordering": ("-created",),
            },
        ),
        migrations.CreateModel(
            name="ShoppingCart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "discount",
                    models.PositiveSmallIntegerField(
                        null=True,
                        verbose_name="процент скидки",
                    ),
                ),
            ],
            options={
                "verbose_name": "корзина пользователя",
                "verbose_name_plural": "корзины пользователей",
            },
        ),
        migrations.CreateModel(
            name="ShoppingCartItems",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.PositiveSmallIntegerField(
                        default=1,
                        verbose_name="Количество товара",
                    ),
                ),
                (
                    "is_selected",
                    models.BooleanField(default=True, verbose_name="выбран"),
                ),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.shoppingcart",
                        verbose_name="корзина",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shop_cart",
                        to="products.product",
                        verbose_name="продукт",
                    ),
                ),
            ],
            options={
                "verbose_name": "товар в корзине",
                "verbose_name_plural": "товары в корзине",
            },
        ),
        migrations.AddField(
            model_name="shoppingcart",
            name="items",
            field=models.ManyToManyField(
                through="products.ShoppingCartItems",
                to="products.product",
            ),
        ),
    ]
