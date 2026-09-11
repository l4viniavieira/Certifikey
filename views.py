from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Certificado, Estudante, Categoria, Curso

@login_required
def index(request):
    # Agregação para contagem eficiente no painel
    stats = Certificado.objects.aggregate(
        total=Count('id'),
        aprovados=Count('id', filter=Q(status='APROVADO')),
        pendentes=Count('id', filter=Q(status='PENDENTE')),
        recusados=Count('id', filter=Q(status='RECUSADO'))
    )

    context = {
        'nome_usuario': request.user.username,
        'total_certificados': stats['total'],
        'certificados_aprovados': stats['aprovados'],
        'certificados_pendentes': stats['pendentes'],
        'certificados_recusados': stats['recusados'],
        
        'total_estudantes': Estudante.objects.count(),
        'total_categorias': Categoria.objects.count(),
        
        'certificados_recentes': Certificado.objects.select_related('estudante', 'categoria').order_by('-data_envio')[:5]
    }

    return render(request, 'index.html', context)


@login_required
def perfil_estudante(request):
    estudante = Estudante.objects.filter(usuario=request.user).first()

    # Se não existir perfil, busca/cria um curso padrão antes de criar o Estudante
    if not estudante:
        curso_padrao, _ = Curso.objects.get_or_create(
            nome="Geral",
            defaults={'horas_obrigatorias': 100}
        )
        estudante = Estudante.objects.create(
            usuario=request.user,
            nome_completo=request.user.get_full_name() or request.user.username,
            matricula=f"MAT-{request.user.id}",
            ano_ingresso=2026,
            curso=curso_padrao
        )

    if request.method == 'POST':
        nome_completo = request.POST.get('nome_completo')
        email = request.POST.get('email')
        curso_id = request.POST.get('curso')
        ano_ingresso = request.POST.get('ano_ingresso')

        if curso_id:
            try:
                estudante.curso = Curso.objects.get(id=curso_id)
            except (Curso.DoesNotExist, ValueError):
                messages.error(request, "Curso selecionado é inválido.")
                return redirect('perfil')

        if nome_completo:
            estudante.nome_completo = nome_completo
        if ano_ingresso and ano_ingresso.isdigit():
            estudante.ano_ingresso = int(ano_ingresso)
            
        estudante.save()

        if email:
            request.user.email = email
            request.user.save()

        messages.success(request, "Perfil e dados acadêmicos atualizados com sucesso!")
        return redirect('perfil')

    cursos_disponiveis = Curso.objects.all()

    context = {
        'estudante': estudante,
        'cursos': cursos_disponiveis
    }
    return render(request, 'perfil.html', context)