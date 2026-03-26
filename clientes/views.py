from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from .models import Cliente
from .forms import ClienteForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.utils.timezone import now
from django.db.models.functions import ExtractMonth, ExtractDay
from django.db.models import Count
from django.db.models.functions import TruncMonth

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        senha = request.POST.get('password')
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            login(request, user)
            return redirect('cliente_list')
        else:
            error_message = 'Usuário ou senha inválidos.'
            return render(request, 'contas/login.html', {'error': error_message})
    return render(request, 'contas/login.html')

def registrar_view(request):
    if request.method == "POST":
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            user = form.save()
            print("Usuário criado:", user.username)
            login(request, user)
            return redirect('pagina_inicial')
        else:
             print("Formulário inválido:", form.errors)
    else:
        form = FormularioRegistro()
    return render(request, 'contas/registro.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def pagina_inicial(request):
    return render(request, 'clientes/pagina_inicial.html')

@login_required
def cliente_list(request):
    clientes = Cliente.objects.filter(usuario=request.user)
    hoje = now().date()
    proximos_dias = hoje + timedelta(days=7)

    aniversariantes = []
    for cliente in clientes:
        if cliente.aniversario:
            try:
                dia, mes = map(int, cliente.aniversario.split('/'))
                aniversario_date = date(hoje.year, mes, dia)

                if hoje <= aniversario_date <= proximos_dias:
                    aniversariantes.append(cliente)

            except ValueError:
                pass

    mostrar_apenas_aniversariantes = request.GET.get('aniversariantes') == '1'
    if mostrar_apenas_aniversariantes:
        clientes = aniversariantes

    return render(request, 'clientes/cliente_list.html', {
        'clientes': clientes,
        'aniversariantes': aniversariantes, 
        'mostrar_filtro': mostrar_apenas_aniversariantes 
    })

@login_required
def criar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario = request.user  
            cliente.save() 
            return redirect('cliente_list') 
    else:
        form = ClienteForm()
    return render(request, 'clientes/cliente_form.html', {'form': form})

def atualizar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/cliente_form.html', {'form': form})

def excluir_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk, usuario=request.user)
    if request.method == 'POST':
        cliente.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'mensagem': 'Cliente excluído com sucesso!'})
        return redirect('cliente_list')
    return render(request, 'clientes/cliente_confirm_delete.html', {'cliente': cliente})

@login_required
def dashboard(request):
    clientes = Cliente.objects.filter(usuario=request.user)

    # Total
    total_clientes = clientes.count()

    # Crescimento por mês
    clientes_por_mes = (
        clientes
        .annotate(mes=TruncMonth('data_criacao'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )

    labels = []
    dados = []

    for item in clientes_por_mes:
        labels.append(item['mes'].strftime('%b/%Y'))
        dados.append(item['total'])
    
    pagamentos = (
    clientes
    .exclude(pagamento__isnull=True)
    .exclude(pagamento__exact='')
    .values('pagamento')
    .annotate(total=Count('id'))
    )
    labels_pagamento = []
    dados_pagamento = []
    
    for p in pagamentos:
        if p['pagamento']:
            labels_pagamento.append(p['pagamento'])
            dados_pagamento.append(p['total'])
    if not labels_pagamento:
        labels_pagamento = ['Sem dados']
        dados_pagamento = [1]
    pagamento_mais_usado = None

    if dados_pagamento:
        max_index = dados_pagamento.index(max(dados_pagamento))
        pagamento_mais_usado = labels_pagamento[max_index]

    context = {
        'total_clientes': total_clientes,
        'labels': labels,
        'dados': dados,
        'labels_pagamento': labels_pagamento,
        'dados_pagamento': dados_pagamento,
        'pagamento_mais_usado': pagamento_mais_usado,
    }

    return render(request, 'clientes/dashboard.html', context)