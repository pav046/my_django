from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ë': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 'c', 'т': 't', 'у': 'u', 'ф': 'f', 'x': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 's': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}
    return ''.join(map(lambda x: d[x.lower()] if x.lower() in d else x, s))


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):

    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug")
    photo = models.ImageField(null=True, verbose_name='Фотография', upload_to='photo/%Y/%m/%d', blank=True, default=None)
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    is_published = models.BooleanField(default=Status.DRAFT, choices=list(map(lambda x: (bool(x[0]), x[1]), Status.choices)), verbose_name="Статус")

    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name="Категория")
    my_tags = models.ManyToManyField('TagPost', blank=True, related_name='your_tags', verbose_name="Тэги")
    husband = models.OneToOneField('Husband', null=True, related_name='woman', on_delete=models.SET_NULL, blank=True, verbose_name="Муж")

    author = models.ForeignKey(get_user_model(), null=True, default=None, blank=True, on_delete=models.SET_NULL)

    objects = models.Manager()
    published = PublishedManager()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        ordering = ['time_create']
        verbose_name = "Известные женщины"
        verbose_name_plural = "Известные женщины"

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit_to_eng(self.title))
    #     super().save(args, kwargs)

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     super().save(args, kwargs)



class Category(models.Model):

    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name='slug')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('categories', kwargs={'cat_slug': self.slug})

class TagPost(models.Model):

    tag = models.CharField(max_length=100, db_index=True)
    slug = models.CharField(max_length=255, blank=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=150)
    age = models.IntegerField(null=True, blank=True)
    count_m = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.name


class UploadFiles(models.Model):
    file = models.FileField(upload_to='upload_files/%Y-%m-%d', verbose_name='Файл')
