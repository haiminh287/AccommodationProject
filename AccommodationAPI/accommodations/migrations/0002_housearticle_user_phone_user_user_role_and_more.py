# Generated by Django 5.1.4 on 2025-01-29 05:17

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accommodations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="HouseArticle",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                ("title", models.CharField(max_length=256)),
                ("content", models.TextField()),
                ("contact", models.CharField(max_length=100)),
                ("number_people", models.IntegerField()),
                ("deposit", models.DecimalField(decimal_places=2, max_digits=10)),
                ("area", models.CharField(max_length=100)),
                ("location", models.CharField(max_length=256)),
                ("longitude", models.DecimalField(decimal_places=14, max_digits=30)),
                ("latitude", models.DecimalField(decimal_places=14, max_digits=30)),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("Chờ Kiểm Duyệt", "PENDING"),
                            ("Đã Duyệt", "DONE"),
                            ("Đã Hủy", "CANCEL"),
                        ],
                        default="PENDING",
                        max_length=100,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="user",
            name="phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                max_length=128, null=True, region=None
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="user_role",
            field=models.CharField(
                choices=[
                    ("Chủ Nhà Trọ", "INKEEPER"),
                    ("Người Tìm Trọ", "TENANT"),
                    ("Quản Trị Viên", "ADMIN"),
                ],
                default="Người Tìm Trọ",
                max_length=100,
            ),
        ),
        migrations.CreateModel(
            name="AcquistionArticle",
            fields=[
                (
                    "housearticle_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="accommodations.housearticle",
                    ),
                ),
                ("stateAcqui", models.BooleanField(default=True)),
                (
                    "typeHouse",
                    models.CharField(
                        choices=[
                            ("Chung Cư", "APARTMENT"),
                            ("Nhà Nguyên Căn", "ORIGIN_HOUSE"),
                            ("Phòng Trọ", "ROOM"),
                        ],
                        default="ROOM",
                        max_length=100,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("accommodations.housearticle",),
        ),
        migrations.CreateModel(
            name="LookingArticle",
            fields=[
                (
                    "housearticle_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="accommodations.housearticle",
                    ),
                ),
                ("stateLook", models.BooleanField(default=True)),
            ],
            options={
                "abstract": False,
            },
            bases=("accommodations.housearticle",),
        ),
        migrations.AddField(
            model_name="housearticle",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.CreateModel(
            name="AddtionallInfomaion",
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
                ("name", models.CharField(max_length=256)),
                ("value", models.CharField(max_length=256)),
                (
                    "house",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accommodations.housearticle",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Conversation",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owned_conversations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="received_conversations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ConversationChat",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                ("content", models.TextField()),
                (
                    "conversation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chats",
                        to="accommodations.conversation",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chats",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ImageHouse",
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
                ("image", models.ImageField(null=True, upload_to="house/%Y/%m/")),
                (
                    "house",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accommodations.housearticle",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Notification",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                ("content", models.TextField()),
                ("is_read", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                ("content", models.TextField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "acquisition",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accommodations.acquistionarticle",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Like",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "acquisition",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accommodations.acquistionarticle",
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "acquisition")},
            },
        ),
    ]
