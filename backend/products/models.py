from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models

from core.models import TimestampedModel
from products.utils import cut_string
from users.models import User

PAY_METHOD_CHOICES = [
    ('card', 'card'),
    ('sbp', 'sbp'),
]


def user_directory_path(instance, filename):
    return f'products/{instance.user.id}/{filename}'


class Category(TimestampedModel):
    name = models.CharField(
        'название',
        max_length=200,
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self) -> str:
        return cut_string(self.name)


class Image(TimestampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
    )
    image = models.ImageField(
        'изображение',
        upload_to=user_directory_path,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'


class Product(TimestampedModel):
    def get_article():
        try:
            return Product.objects.latest('id').article + 1
        except ObjectDoesNotExist:
            return settings.FIRST_ARTICLE

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
    )
    name = models.CharField(
        'название бота',
        max_length=60,
        validators=[MinLengthValidator(20)],
    )
    description = models.TextField(
        'описание бота',
        max_length=1500,
        validators=[MinLengthValidator(50)],
    )
    images = models.ManyToManyField(
        Image,
        verbose_name='список изображений',
        blank=True,
        through='ImageProduct',
    )
    video = models.TextField(
        'ссылка на видео',
        blank=True,
        null=True,
    )
    article = models.PositiveIntegerField(
        'артикул',
        default=get_article,
        editable=False,
        unique=True,
    )
    price = models.PositiveIntegerField(
        'стоимость',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100000000),
        ],
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='категория',
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ('-created',)

    def __str__(self) -> str:
        return cut_string(self.name)


class ImageProduct(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'изображение в товаре'
        verbose_name_plural = 'изображения в товарах'

    def __str__(self) -> str:
        return f'{self.image} {self.product}'


class Review(TimestampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_review',
        verbose_name='пользователь',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_review',
        verbose_name='продукт',
    )
    rating = models.PositiveSmallIntegerField(
        'рейтинг',
        blank=False,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    text = models.TextField(
        'текст отзыва',
        validators=[MinLengthValidator(6)],
        max_length=500,
        blank=False,
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ('-created',)
        constraints = [
            models.UniqueConstraint(
                fields=(
                    'user',
                    'product',
                ),
                name='rating_allowed_once',
            ),
        ]

    def __str__(self):
        return cut_string(self.text)


class Order(TimestampedModel):
    def get_number_order():
        try:
            last_order = Order.objects.latest('number_order')
            return last_order.number_order + 1
        except Exception:
            return settings.FIRST_ORDER_NUMBER

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_orders',
        verbose_name='пользователь',
    )
    product_list = models.ManyToManyField(
        Product,
        through='OrderProductLists',
        related_name='product_in_order',
        verbose_name='продукт в заказе',
    )
    pay_method = models.CharField(
        'метод оплаты',
        max_length=4,
        choices=PAY_METHOD_CHOICES,
        blank=True,
        null=True,
    )
    send_to = models.EmailField('куда прислать', max_length=200, blank=True)
    total_cost = models.IntegerField('итоговая цена', blank=True, null=True)
    is_paid = models.BooleanField('оплачен', default=False)
    sale_status = models.BooleanField('скидка', default=False)
    number_order = models.PositiveIntegerField(
        'номер заказа',
        default=get_number_order,
        editable=False,
        unique=True,
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ('-created',)

    def __str__(self):
        return f'Заказ от пользователя: {self.user}'


class OrderProductLists(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='product_in_order',
        verbose_name='связанные заказы',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name='order_with_product',
        verbose_name='связанные продукты',
        null=True,
    )
    quantity = models.IntegerField(
        'количество продуктов',
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'товар в заказе'
        verbose_name_plural = 'товары в заказах'
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=(
                    'order',
                    'product',
                ),
                name='unique_order',
            ),
        ]

    def __str__(self):
        return f'{self.product} {self.quantity} в заказе {self.order}'


class ShoppingCart(TimestampedModel):
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_cart',
        verbose_name='владелец корзины',
    )
    items = models.ManyToManyField(Product, through='ShoppingCartItems')
    discount = models.PositiveSmallIntegerField(
        null=True,
        verbose_name='процент скидки',
    )

    class Meta:
        verbose_name = 'корзина пользователя'
        verbose_name_plural = 'корзины пользователей'

    def __str__(self):
        return f'Корзина пользователя {self.owner.username}'


class ShoppingCartItems(models.Model):
    item = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='shop_cart',
        verbose_name='продукт',
    )
    cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        verbose_name='корзина',
    )
    quantity = models.PositiveSmallIntegerField(
        'Количество товара',
        default=1,
    )
    is_selected = models.BooleanField('выбран', default=True)

    class Meta:
        verbose_name = 'товар в корзине'
        verbose_name_plural = 'товары в корзине'

    def __str__(self):
        return f'{self.item.name} в корзине пользователя {self.cart.owner}'


class Favorite(TimestampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_favorite',
        verbose_name='пользователь',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_favorite',
        verbose_name='продукт',
    )

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique favorite',
            ),
        ]
