import datetime
from datetime import date, timedelta
from django.conf import settings

from django.contrib.auth.models import User

from django.db import models
from django.urls import reverse


class CustomUser(models.Model):
    user = models.OneToOneField(
        User, max_length=150, unique=True, on_delete=models.CASCADE
    )
    email = models.EmailField('email', unique=True)
    img = models.ImageField('Аватар', upload_to="users/", blank=True)
    birthday = models.DateField('День рождения', null=True)
    discount = models.PositiveSmallIntegerField('Скидка', default=0)
    url = models.SlugField(unique=True, max_length=160)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Tag(models.Model):
    """Облако тэгов"""
    title = models.CharField("Тэг", max_length=25)
    url = models.SlugField(max_length=30, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def get_absolute_url(self):
        return reverse("tag_detail", kwargs={"slug": self.url})


class Procedure(models.Model):
    """Процедура"""
    title = models.CharField("Название", max_length=150)
    about = models.TextField("Описание")
    image = models.ImageField('Картинка', upload_to="procedure/")
    price = models.PositiveSmallIntegerField("Цена")
    url = models.SlugField(max_length=160, unique=True)
    time = models.PositiveSmallIntegerField("Длительность", help_text="Время в минутах")
    tags = models.ManyToManyField(
        Tag, verbose_name="Тэги", related_name="procedure_tags"
    )
    sorting = models.SmallIntegerField("Номер сортировки", blank=True, default=0)
    unpublished = models.BooleanField("Черновик", default=False)
    icon = models.CharField("Иконка", max_length=100, default=" ")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("procedure_detail", kwargs={"slug": self.url})

    def get_questions(self):
        return self.questions_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Процедура"
        verbose_name_plural = "Процедуры"


class ComplexProcedure(models.Model):
    title = models.CharField("Название", max_length=150)
    about = models.TextField("Описание")
    image = models.ImageField('Картинка', upload_to="complex/")
    url = models.SlugField(max_length=160, unique=True)
    price = models.PositiveSmallIntegerField("Цена")
    time = models.PositiveSmallIntegerField("Длительность", help_text="Время в минутах")

    tags = models.ManyToManyField(
        Tag, verbose_name="Тэги", related_name="complex_tags"
    )
    sorting = models.SmallIntegerField("Номер сортировки", blank=True, default=0)
    unpublished = models.BooleanField("Черновик", default=False)
    saving = models.PositiveSmallIntegerField("Экономия", null=True)
    procedures = models.ManyToManyField(Procedure, verbose_name="Процедуры", related_name="complex_procedure")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Комплекс"
        verbose_name_plural = "Комплексы"


class ProcedureImages(models.Model):
    """Дополнительные картинки к процедуре"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="procedure_shots/")
    procedure = models.ForeignKey(Procedure, verbose_name="Процедура", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Картинка к процедуре"
        verbose_name_plural = "Картинки к процедуре"


class ComplexImages(models.Model):
    """Дополнительные картинки к комплексу"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="complex_shots/")
    complex = models.ForeignKey(ComplexProcedure, verbose_name="Процедура", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Картинка к комплексу"
        verbose_name_plural = "Картинки к комплексу"


class OrdersHistory(models.Model):
    """История заказов"""
    user = models.OneToOneField(
        User, verbose_name="Пользователь", on_delete=models.SET_NULL, null=True, related_name="order_user"
    )
    procedure = models.ForeignKey(
        Procedure, verbose_name="Процедура", related_name="order_procedure", on_delete=models.SET_NULL, null=True
    ) #ДОПИСАТЬ
    date = models.DateField("Дата проведения")
    price = models.PositiveSmallIntegerField('Цена')
    url = models.SlugField(unique=True, max_length=150)

    def __str__(self):
        return f'{self.user} / {self.procedure} / {self.date}'

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Action(models.Model):
    """Акция"""
    title = models.CharField("Название", max_length=150)
    about = models.TextField("Описание")
    discount = models.PositiveSmallIntegerField("Скидка")
    date_start = models.DateField("Дата начала", default=date.today)
    # date_end = models.DateField("Дата начала", default=date.today + timedelta(days=7))
    date_end = models.DateField("Дата начала", default=(date.today() + timedelta(days=7)))
    is_active = models.BooleanField('Активна', default=False)
    procedure_in = models.ForeignKey(
        Procedure, verbose_name="Процедура", related_name="action_procedure", on_delete=models.CASCADE
    )
    image = models.ImageField('Картинка', upload_to="actions/")
    url = models.SlugField(max_length=160, unique=True)
    # url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"


class Questions(models.Model):
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=2500)
    date = models.DateTimeField(default=datetime.datetime.now)
    parent = models.ForeignKey(
        "self", verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    procedure = models.ForeignKey(Procedure, verbose_name="Процедура", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} | {self.procedure} | {self.date.strftime('%d.%m.%y-%H:%M')}"

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Day_visit(models.Model):
    date = models.DateField("дата", default=date.today)

    def __str__(self):
        return self.date.strftime("%d.%m")


class Visit(models.Model):
    procedure = models.ForeignKey(
        Procedure, verbose_name="Процедура", on_delete=models.CASCADE, default=None)
    client = models.ForeignKey(
        User, verbose_name="Клиент", on_delete=models.CASCADE)
    day = models.ForeignKey(Day_visit, verbose_name="День приема", default=1, on_delete=models.CASCADE)
    timing = models.PositiveSmallIntegerField("продолжительность", default=0)
    time_start = models.TimeField("Время начала")

    def __str__(self):
        return f'{self.procedure.title} | {self.day.date.strftime("%d.%m")} | {self.client.username}'

    def save(self, *args, **kwargs):
        self.timing = self.procedure.time
        super().save(*args, **kwargs)  # Call the "real" save() method.

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"



















