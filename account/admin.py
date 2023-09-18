from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import User


# Register your models here.
class UserChangeForm(UserChangeForm):
    class Meta:
        models = User
        fields = '__all__'


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class UserAdmin(UserAdmin):
    readonly_fields = ('created_at', 'updated_at', 'last_login',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('date info'), {'fields': ('created_at', 'updated_at',
                                     'last_login',)}),
    )

    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'last_name', 'first_name',
                       'password1', 'password2'),
        })
    ]

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(User, UserAdmin)
