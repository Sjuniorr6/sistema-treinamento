from django.contrib import admin
from django.contrib.auth.models import User
from .models import Video, UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Inline para UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil de Usuário'
    fields = ('empresa',)  # Mostra o campo empresa no formulário de criação de usuário

# Personalização do Admin de User para incluir o UserProfile
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Re-registra o modelo User com o novo UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Registro do modelo Video
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'uploaded_at')
    search_fields = ('title',)
    list_filter = ('uploaded_at',)

