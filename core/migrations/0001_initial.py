# Generated by Django 4.0.4 on 2022-05-11 11:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContactsGroup",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ],
            options={
                "verbose_name": "Группа контактов",
                "verbose_name_plural": "Группы контактов",
            },
        ),
        migrations.CreateModel(
            name="ContactType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
            ],
            options={
                "verbose_name": "Тип контакта",
                "verbose_name_plural": "Типы контактов",
            },
        ),
        migrations.CreateModel(
            name="Contact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.CharField(max_length=100, verbose_name="Значение")),
                (
                    "contacts_group_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.contactsgroup",
                        verbose_name="Группа контактов",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.contacttype", verbose_name="Тип контакта"
                    ),
                ),
            ],
            options={
                "verbose_name": "Контакт",
                "verbose_name_plural": "Контакты",
            },
        ),
    ]
