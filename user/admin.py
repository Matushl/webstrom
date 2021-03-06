from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Permission

from competition.models import Profile
from user.forms import UserCreationForm
from user.models import User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password',)

    password = ReadOnlyPasswordHashField()

    def clean_password(self):
        return self.initial['password']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('first_name', 'last_name', 'email', 'is_staff',)
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups',)
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('last_login',)
    inlines = (ProfileInline,)

    fieldsets = (
        ('Prihlásenie', {
            'classes': ('wide',),
            'fields': ('email', 'verified_email', 'password', 'last_login'),
        }),
        ('Oprávnenia', {
            'classes': ('collapse',),
            'fields': (('is_staff', 'is_superuser'), 'groups'),
        }),
        ('Extra oprávnenia', {
            'classes': ('collapse',),
            'fields': ('user_permissions',),
            'description': 'Za normálnych okolností sa neudeľujú a mali by '
                           'vystačiť skupiny oprávnení, avšak pre nejaké '
                           'špeciálne potreby môžu byť využité. Priraďujú '
                           'oprávnenia nad rámec skupín.'
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


admin.site.register(Permission)
