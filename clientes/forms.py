from django import forms
from .models import Cliente
from django.contrib.auth.models import User
import datetime
import re

class ClienteForm(forms.ModelForm):
    aniversario = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'dd/mm',
            'class': 'form-control',
            'pattern': '[0-3][0-9]/[0-1][0-9]',
            'title': 'Formato: dd/mm',
            'aria-label': 'Data de aniversário no formato dia barra mês',
        }),
        help_text="Informe o dia e o mês (ex: 03/04)."
    )

    def clean_aniversario(self):
        data = self.cleaned_data['aniversario']
        if not re.match(r'^\d{2}/\d{2}$', data):
            raise forms.ValidationError("Use o formato dd/mm.")
        dia, mes = map(int, data.split('/'))
        try:
            datetime.date(2000, mes, dia)
        except ValueError:
            raise forms.ValidationError("Data inválida.")
        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['pagamento'].choices = [
            ('', 'Selecione um método de pagamento')
        ] + [
            choice for choice in self.fields['pagamento'].choices if choice[0] != ''
        ]

        self.fields['pagamento'].widget.attrs.update({
            'class': 'form-select text-muted',
            'aria-label': 'Selecione o método de pagamento',
            'onchange': "this.classList.remove('text-muted');"
        })

        if self.instance and self.instance.aniversario:
            aniversario = self.instance.aniversario
            if isinstance(aniversario, datetime.date):
                self.initial['aniversario'] = aniversario.strftime('%d/%m')

        self.fields['nome'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite o nome completo',
            'aria-label': 'Campo de nome completo',
            'aria-required': 'true',
        })
        self.fields['cpf'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite o CPF',
            'inputmode': 'numeric',
            'aria-label': 'Campo de CPF',
            'aria-required': 'true',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite o e-mail',
            'aria-label': 'Campo de e-mail',
        })
        self.fields['telefone'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite o telefone',
            'inputmode': 'tel',
            'aria-label': 'Campo de telefone para contato',
        })
        self.fields['cep'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite o CEP',
            'inputmode': 'numeric',
            'aria-describedby': 'ajuda-cep',
        })
        self.fields['endereco'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Endereço será preenchido automaticamente',
            'readonly': True,
            'aria-label': 'Campo de endereço preenchido automaticamente',
            })
        self.fields['observacoes'].widget.attrs.update({
            'class': 'form-control',
            'rows': 3,
            'aria-label': 'Campo para observações adicionais sobre o cliente',
        })

    class Meta:
        model = Cliente
        fields = [
            'nome', 'cpf', 'email', 'telefone',
            'cep', 'endereco', 'aniversario',
            'pagamento', 'observacoes',
        ]