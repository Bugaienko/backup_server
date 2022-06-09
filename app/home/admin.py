from django import forms
from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# from django.contrib.gis import forms
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Tag, Procedure, ComplexProcedure, ProcedureImages, ComplexImages, OrdersHistory, Action, CustomUser, \
    Questions, Day_visit, Visit


admin.site.register(Day_visit)
admin.site.register(ComplexProcedure)

admin.site.register(ComplexImages)


class ProcedureAdminForm(forms.ModelForm):
    about = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Procedure
        fields = '__all__'


@admin.register(Visit)
class DayVisitAdmin(admin.ModelAdmin):
    list_display = (
        'procedure',
        'client',
        'day',
        'timing',
        'time_start'
    )
    readonly_fields = ('timing', )


@admin.register(ProcedureImages)
class ProcedureImagesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
        'get_image',
        'procedure'
    )
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100">')

    get_image.short_description = 'Изображение'


class ProcedureImagesInline(admin.TabularInline):
    model = ProcedureImages
    extra = 1
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="120">')

    get_image.short_description = 'Изображение'


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'email',
        'text',
        'date',
        'parent',
        'procedure'
    )
    list_display_links = ('id', 'name',)


class QuestionsInline(admin.TabularInline):
    model = Questions
    extra = 1
    readonly_fields = ('name', 'email')


@admin.register(CustomUser)
class CustomerUserAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'email',
        'img',
        'birthday',
        'discount',
        'url',
        'get_image'
    )
    readonly_fields = ('get_image',)
    prepopulated_fields = {'url': ('user',), }

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.img.url} width="120">')


class CustomerUserInline(admin.StackedInline):
    model = CustomUser
    can_delete = False
    verbose_name = "Мой пользователь"
    verbose_name_plural = "Мои пользователи"


class UserAdmin(BaseUserAdmin):
    inlines = (CustomerUserInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ActionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'about',
        'discount',
        'date_start',
        'date_end',
        'is_active',
        'procedure_in',
        'get_image',
        'url'
    )
    list_display_links = ('title', )
    list_filter = ('procedure_in', 'is_active')
    readonly_fields = ('get_image',)
    prepopulated_fields = {'url': ('title',), }

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="120">')

    get_image.short_description = 'Изображение'


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'about',
        'get_image_pr',
        'price', 'time',
        'sorting', 'url', 'icon',
        'unpublished',
    )
    fields = (
        'title',
        'about',
        ('image', 'get_image'),
        ('price', 'time'),
        ('sorting', 'url', 'icon'),
        'unpublished',

    )
    readonly_fields = ('get_image', )
    list_display_links = ('title', 'get_image_pr', )
    list_filter = ('tags', 'unpublished')
    search_fields = ('title', 'about', 'tags__title')
    readonly_fields = ('get_image', 'get_image_pr')
    inlines = [ProcedureImagesInline, QuestionsInline, ]
    save_on_top = True
    prepopulated_fields = {'url': ('title',), }
    # save_as = True - сохранить как новую запись
    list_editable = ('unpublished', 'sorting')
    actions = ['unpublish', 'publish']
    form = ProcedureAdminForm

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(unpublished=True)
        if row_update == 1:
            message_bit = "1 запись обновлена"
        else:
            message_bit = f'{row_update} записи обновлено'
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(unpublished=False)
        if row_update == 1:
            message_bit = "1 запись обновлена"
        else:
            message_bit = f'{row_update} записи обновлено'
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ("change", )

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ("change",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150">')

    def get_image_pr(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100">')

    get_image.short_description = 'Изображение'
    get_image_pr.short_description = 'Изображение'


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('title',), }


class OrdersHistoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('user', 'procedure', 'date'), }


admin.site.register(Tag, TagAdmin)
admin.site.register(Action, ActionAdmin)

admin.site.register(OrdersHistory, OrdersHistoryAdmin)

admin.site.site_title = "Студия массажа Ирины Бугаенко"
admin.site.site_header = "Студия массажа Ирины Бугаенко"
