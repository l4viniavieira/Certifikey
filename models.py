from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator

class Curso(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Nome do Curso")
    horas_obrigatorias = models.PositiveIntegerField(
        verbose_name="Horas Obrigatórias Exigidas"
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"


class Estudante(models.Model):
    nome_completo = models.CharField(max_length=150, verbose_name="Nome Completo")
    email = models.EmailField(
        max_length=100, 
        unique=True, 
        verbose_name="E-mail Institucional"
    )  
    matricula = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Matrícula"
    ) 
    senha = models.CharField(max_length=128, verbose_name="Senha")
    ano_ingresso = models.PositiveIntegerField(verbose_name="Ano de Ingresso")
    curso = models.ForeignKey(
        Curso, 
        on_delete=models.CASCADE, 
        verbose_name="Curso Técnico"
    )  

    def __str__(self):
        return f"{self.nome_completo} ({self.matricula})"

    class Meta:
        verbose_name = "Estudante"
        verbose_name_plural = "Estudantes"


class Categoria(models.Model):
    NATUREZA_CHOICES = [
        ('ENSINO', 'Ensino'),
        ('PESQUISA', 'Pesquisa'),
        ('EXTENSAO', 'Extensão'),
    ]

    nome = models.CharField(max_length=100, verbose_name="Nome da Categoria")
    natureza = models.CharField(
        max_length=20, 
        choices=NATUREZA_CHOICES, 
        default='EXTENSAO', 
        verbose_name="Natureza da Atividade"
    )
    teto_maximo_horas = models.PositiveIntegerField(
        verbose_name="Teto Máximo de Horas Permitido"
    ) 

    def __str__(self):
        return f"{self.nome} - {self.get_natureza_display()}"

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Certificado(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente de Análise'),
        ('APROVADO', 'Aprovado'),
        ('RECUSADO', 'Recusado'),
    ]

    titulo_atividade = models.CharField(max_length=200, verbose_name="Título da Atividade")
    carga_horaria = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], 
        verbose_name="Carga Horária (Horas)"
    )
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name="Data de Envio")
    
    arquivo = models.FileField(
        upload_to='certificados/', 
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'jpeg'])],
        verbose_name="Arquivo do Certificado"
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='PENDENTE', 
        verbose_name="Status da Análise"
    )
    justificativa_recusa = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Justificativa de Recusa"
    )

    estudante = models.ForeignKey(
        Estudante, 
        on_delete=models.CASCADE, 
        verbose_name="Estudante"
    )
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.RESTRICT, 
        verbose_name="Categoria da Atividade"
    )

    def __str__(self):
        return f"{self.titulo_atividade} - {self.estudante.nome_completo} [{self.status}]"

    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"


class Notificacao(models.Model):
    mensagem = models.TextField(verbose_name="Mensagem do Alerta")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    lida = models.BooleanField(default=False, verbose_name="Lida?")
    
    estudante = models.ForeignKey(
        Estudante, 
        on_delete=models.CASCADE, 
        verbose_name="Estudante"
    )

    def __str__(self):
        return f"Notificação para {self.estudante.nome_completo} em {self.data_criacao.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"


class Tutorial(models.Model):
    titulo = models.CharField(max_length=150, verbose_name="Título do Passo/Instrução")
    descricao = models.TextField(verbose_name="Descrição Detalhada")
    ordem_exibicao = models.PositiveIntegerField(
        default=1, 
        verbose_name="Ordem de Exibição"
    )

    def __str__(self):
        return f"{self.ordem_exibicao}. {self.titulo}"

    class Meta:
        verbose_name = "Tutorial"
        verbose_name_plural = "Tutoriais"
        ordering = ['ordem_exibicao']