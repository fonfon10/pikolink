from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import PasswordResetForm
from django.utils.crypto import get_random_string

User = get_user_model()


@admin.action(description="Invite selected users (send password reset email)")
def invite_users(modeladmin, request, queryset):
    for user in queryset:
        if not user.email or not user.is_active:
            continue

        # force unknown password
        user.set_password(get_random_string(64))
        user.save()

        form = PasswordResetForm({"email": user.email})
        if form.is_valid():
            form.save(
                request=request,
                use_https=False,  # dev only
                from_email=None,
                email_template_name="registration/password_reset_email.html",
                subject_template_name="registration/password_reset_subject.txt",
            )


class UserAdmin(DjangoUserAdmin):
    actions = [invite_users]


from .models import Customer, Link, Click

admin.site.register(Customer)
admin.site.register(Link)
admin.site.register(Click)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)