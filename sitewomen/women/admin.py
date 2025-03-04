from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Women, Category


class FilterHusband(admin.SimpleListFilter):
    title = "Статус женщин"
    parameter_name = 'her_status'

    def lookups(self, request, model_admin):
        return [('married', 'Замужем'), ('single', 'Не замужем')]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        if self.value() == 'single':
            return queryset.filter(husband__isnull=True)



@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo', 'picture', 'is_published', 'husband', 'cat', 'my_tags']
    # exclude = ['tags', 'is_published']
    readonly_fields = ['picture']
    # filter_horizontal = ['my_tags']
    filter_vertical = ['my_tags']
    prepopulated_fields = {'slug': ('title', )}
    list_display = ('id', 'title', 'picture', 'time_create', 'is_published', 'cat', 'brief_info', 'slug')
    list_display_links = ('id', )
    ordering=['-time_create']
    list_editable = ['is_published', 'title']
    list_per_page = 40
    actions = ['set_published', 'set_draft']
    search_fields = ['title__endswith', 'cat__name']
    list_filter = ['cat__name', 'is_published', FilterHusband]
    save_on_top = True

    @admin.display(description='Краткое описание', ordering='id')
    def brief_info(self, women: Women):
        return f"Описание содержит {len(women.content)} символов"

    @admin.display(description='Текущее изображение')
    def picture(self, women: Women):
        if women.photo:
            return mark_safe(f'<img src="{women.photo.url}" width=60>')
        return "Без фото"

    @admin.action(description='Сделать опубликованным')
    def set_published(self, request, queryset):
        num = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f'Изменено {num} записей!')

    @admin.action(description='Сделать черновиками')
    def set_draft(self, request, queryset):
        num = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f'В черновик добавлено {num} записей!', messages.WARNING)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')