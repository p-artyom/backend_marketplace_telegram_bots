import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import users.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                    "password",
                    models.CharField(max_length=128, verbose_name="password"),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="last login",
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="date joined",
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
                (
                    "email",
                    models.EmailField(
                        max_length=200,
                        unique=True,
                        verbose_name="адрес электронной почты",
                    ),
                ),
                ("username", models.CharField(max_length=30)),
                (
                    "first_name",
                    models.CharField(max_length=50, verbose_name="имя"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=50, verbose_name="фамилия"),
                ),
                (
                    "phone",
                    models.CharField(
                        max_length=20,
                        verbose_name="номер телефона",
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=users.models.user_directory_path,
                        verbose_name="Фотография пользователя",
                    ),
                ),
                ("is_seller", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Seller",
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
                    "inn",
                    models.CharField(
                        max_length=12,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[\\d]{10}$|^[\\d]{12}$",
                                message="ИНН состоит из 10 цифр для юридического лица или 12 цифр для физического лица!",
                            )
                        ],
                        verbose_name="ИНН",
                    ),
                ),
                (
                    "logo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=users.models.seller_directory_path,
                        verbose_name="логотип магазина",
                    ),
                ),
                (
                    "store_name",
                    models.TextField(
                        blank=True,
                        max_length=25,
                        null=True,
                        verbose_name="название магазина",
                    ),
                ),
                (
                    "organization_name",
                    models.TextField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="название организации",
                    ),
                ),
                (
                    "organization_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("ООО", "ООО"),
                            ("ОДО", "ОДО"),
                            ("ОА", "ОА"),
                            ("АО", "АО"),
                            ("ПАО", "ПАО"),
                            ("ПТ", "ПТ"),
                            ("ТНВ", "ТНВ"),
                            ("ПК", "ПК"),
                            ("ИП", "ИП"),
                            ("ОАО", "ОАО"),
                            ("Самозанятый", "Самозанятый"),
                        ],
                        max_length=11,
                        null=True,
                        verbose_name="тип организации",
                    ),
                ),
                (
                    "bank_name",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Сбербанк", "Сбербанк"),
                            ("Тинькофф", "Тинькофф"),
                            ("Альфа-Банк", "Альфа-Банк"),
                            ("ВТБ Банк", "ВТБ Банк"),
                            ("Газпромбанк", "Газпромбанк"),
                            ("Райффайзен Банк", "Райффайзен Банк"),
                        ],
                        max_length=15,
                        null=True,
                        verbose_name="название банка",
                    ),
                ),
                (
                    "ogrn",
                    models.CharField(
                        blank=True,
                        max_length=15,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[\\d]{13}$|^[\\d]{15}$",
                                message="ОГРН состоит из 13 цифр для юридического лица или 15 цифр для ИП!",
                            )
                        ],
                        verbose_name="ОГРН",
                    ),
                ),
                (
                    "kpp",
                    models.CharField(
                        blank=True,
                        max_length=9,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[\\d]{9}$",
                                message="КПП состоит из 9 цифр!",
                            ),
                        ],
                        verbose_name="КПП",
                    ),
                ),
                (
                    "bik",
                    models.CharField(
                        blank=True,
                        max_length=9,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[\\d]{9}$",
                                message="БИК состоит из 9 цифр!",
                            ),
                        ],
                        verbose_name="БИК",
                    ),
                ),
                (
                    "payment_account",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[\\d]{20}$",
                                message="Расчетный счет состоит из 20 цифр!",
                            ),
                        ],
                        verbose_name="расчетный счет",
                    ),
                ),
                (
                    "correspondent_account",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[\\d]{20}$",
                                message="Корреспондентский счет состоит из 20 цифр!",
                            ),
                        ],
                        verbose_name="корреспондентский счет",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "продавец",
                "verbose_name_plural": "продавцы",
                "ordering": ("-created",),
            },
        ),
    ]
