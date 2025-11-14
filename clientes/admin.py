from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Cliente

admin.site.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'cpf', 'aniversario', 'pagamento')
    search_fields = ('nome', 'cpf')