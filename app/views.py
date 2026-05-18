from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
import platform
import sys
import boto3
from django.http import HttpResponse


START_TIME = timezone.now()

def create_admin(request):
    from django.contrib.auth.models import User
    from app.models import UserProfile
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_superuser('admin', 'admin@admin.com', 'Admin@123')
        UserProfile.objects.create(user=user, role='admin')
        return HttpResponse("Admin criado! Login: admin / Admin@123")
    return HttpResponse("Admin já existe!")

def get_role(user):
    try:
        return user.userprofile.role
    except:
        return 'viewer'

# ── LOGIN ──
def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        error = "Credenciais inválidas"
    return render(request, 'app/login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('/login/')

# ── DASHBOARD ──
@login_required(login_url='/login/')
def dashboard(request):
    role = get_role(request.user)
    return render(request, 'app/dashboard.html', {'role': role, 'username': request.user.username})

# ── GERENCIAR USUÁRIOS (só admin) ──
@login_required(login_url='/login/')
def manage_users(request):
    if get_role(request.user) != 'admin':
        return redirect('/')

    error = None
    success = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create':
            username = request.POST.get('username')
            password = request.POST.get('password')
            role = request.POST.get('role', 'viewer')
            if User.objects.filter(username=username).exists():
                error = "Usuário já existe"
            else:
                user = User.objects.create_user(username=username, password=password)
                UserProfile.objects.create(user=user, role=role)
                success = f"Usuário {username} criado com sucesso!"

        elif action == 'delete':
            user_id = request.POST.get('user_id')
            try:
                user = User.objects.get(id=user_id)
                if user != request.user:
                    user.delete()
                    success = "Usuário removido!"
                else:
                    error = "Você não pode remover a si mesmo"
            except:
                error = "Usuário não encontrado"

    users = User.objects.all().select_related('userprofile')
    return render(request, 'app/users.html', {
        'users': users,
        'error': error,
        'success': success,
        'username': request.user.username
    })

# ── API ──
@login_required(login_url='/login/')
def status(request):
    uptime = timezone.now() - START_TIME
    return JsonResponse({
        "status": "online",
        "version": "1.0.0",
        "uptime_seconds": int(uptime.total_seconds()),
        "python_version": sys.version,
        "platform": platform.system(),
        "timestamp": timezone.now().isoformat(),
    })

@login_required(login_url='/login/')
def endpoints(request):
    return JsonResponse({
        "endpoints": [
            {"method": "GET", "path": "/api/status/", "description": "Status da aplicação"},
            {"method": "GET", "path": "/api/endpoints/", "description": "Lista de endpoints"},
            {"method": "GET", "path": "/api/deploys/", "description": "Histórico de deploys"},
            {"method": "POST", "path": "/api/deploy/", "description": "Forçar novo deploy (admin)"},
        ]
    })

@login_required(login_url='/login/')
def deploys(request):
    return JsonResponse({
        "deploys": [
            {"version": "1.0.0", "commit": "feat: initial deploy", "date": "2026-05-17", "status": "success"},
        ]
    })

@login_required(login_url='/login/')
@csrf_exempt
def deploy(request):
    if get_role(request.user) != 'admin':
        return JsonResponse({"status": "error", "message": "Acesso negado — apenas admins podem fazer deploy"}, status=403)

    if request.method == 'POST':
        try:
            client = boto3.client('ecs', region_name='sa-east-1')
            client.update_service(
                cluster='autodeploy-cluster',
                service='autodeploy-service',
                forceNewDeployment=True
            )
            return JsonResponse({"status": "success", "message": "Deploy iniciado com sucesso!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Método não permitido"}, status=405)

