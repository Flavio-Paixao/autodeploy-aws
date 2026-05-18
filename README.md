# 🚀 AutoDeploy — Django + Docker + AWS ECS + Terraform + GitHub Actions

> Aplicação Django containerizada com Docker, deployada automaticamente no AWS ECS via pipeline CI/CD com GitHub Actions. Inclui dashboard de monitoramento em tempo real com controle de acesso por roles.

🔗 **[Ver ao Vivo](http://54.207.217.120:8000)**

---

## 🎯 Problema que resolve

Pequenas empresas e startups perdem horas fazendo deploy manual de aplicações. Qualquer atualização vira um processo demorado e arriscado.

**Solução:** Pipeline automatizado que faz o deploy completo em menos de 1 minuto a cada push no GitHub — do código ao container em produção sem intervenção manual.

---

## ✨ Features

- **Dashboard de monitoramento** — status em tempo real, uptime, versão em produção
- **Sistema de autenticação** — login seguro com Django Auth
- **Controle de acesso por roles** — Admin (deploy + monitoramento) e Viewer (só monitoramento)
- **Gerenciamento de usuários** — criar e remover usuários pelo dashboard
- **Botão de deploy manual** — forçar novo deploy pelo dashboard (só admins)
- **Histórico de deploys** — registro de todos os deploys realizados
- **Logs via CloudWatch** — monitoramento de logs em tempo real na AWS
- **Pipeline CI/CD** — deploy automático a cada push na branch main

---

## 🏗️ Arquitetura

```
Push no GitHub
      ↓
GitHub Actions dispara
      ↓
Docker build da imagem
      ↓
Push para AWS ECR
      ↓
ECS Fargate atualiza o serviço
      ↓
Aplicação em produção
```

---

## 🛠️ Stack

| Categoria | Tecnologia |
|---|---|
| Backend | Python, Django |
| Containerização | Docker |
| Repositório de imagens | AWS ECR |
| Orquestração | AWS ECS Fargate |
| Infraestrutura | Terraform |
| CI/CD | GitHub Actions |
| Monitoramento | AWS CloudWatch |
| Rede | VPC, Subnet, Internet Gateway, Security Group |
| IAM | Role + Policy para ECS + CloudWatch |

---

## 📁 Estrutura

```
autodeploy-aws/
├── .github/
│   └── workflows/
│       └── deploy.yml       # Pipeline CI/CD
├── app/
│   ├── templates/app/
│   │   ├── dashboard.html   # Dashboard principal
│   │   ├── login.html       # Página de login
│   │   └── users.html       # Gerenciar usuários
│   ├── models.py            # UserProfile (roles)
│   └── views.py             # Views + API endpoints
├── core/
│   ├── settings.py          # Configurações Django
│   └── urls.py              # Rotas
├── infra/
│   ├── main.tf              # VPC, Subnet, ECS, Security Group
│   ├── iam.tf               # Roles e Policies
│   └── variables.tf         # Variáveis Terraform
├── Dockerfile               # Containerização
├── .dockerignore
└── requirements.txt
```

---

## 🔌 API Endpoints

| Método | Rota | Descrição | Acesso |
|---|---|---|---|
| GET | `/` | Dashboard principal | Autenticado |
| GET | `/login/` | Página de login | Público |
| GET | `/logout/` | Logout | Autenticado |
| GET | `/users/` | Gerenciar usuários | Admin |
| GET | `/api/status/` | Status da aplicação | Autenticado |
| GET | `/api/endpoints/` | Lista de endpoints | Autenticado |
| GET | `/api/deploys/` | Histórico de deploys | Autenticado |
| POST | `/api/deploy/` | Forçar novo deploy | Admin |

---

## 👥 Sistema de Roles

| Role | Dashboard | Deploy | Usuários |
|---|---|---|---|
| **Admin** | ✅ | ✅ | ✅ |
| **Viewer** | ✅ | ❌ | ❌ |

---

## 🚀 Como rodar localmente

```bash
# Clonar o repositório
git clone https://github.com/Flavio-Paixao/autodeploy-aws.git
cd autodeploy-aws

# Ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Migrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Rodar
python manage.py runserver
```

---

## 🐳 Docker

```bash
# Build
docker build -t autodeploy .

# Rodar
docker run -p 8000:8000 autodeploy
```

---

## ☁️ Deploy na AWS com Terraform

```bash
# Inicializar
cd infra
terraform init

# Provisionar infraestrutura
terraform apply -var="ecr_image=SEU_ACCOUNT_ID.dkr.ecr.sa-east-1.amazonaws.com/autodeploy:latest"

# Push da imagem para ECR
aws ecr get-login-password --region sa-east-1 | docker login --username AWS --password-stdin SEU_ACCOUNT_ID.dkr.ecr.sa-east-1.amazonaws.com
docker tag autodeploy:latest SEU_ACCOUNT_ID.dkr.ecr.sa-east-1.amazonaws.com/autodeploy:latest
docker push SEU_ACCOUNT_ID.dkr.ecr.sa-east-1.amazonaws.com/autodeploy:latest
```

---

## 🔄 CI/CD Pipeline

O pipeline roda automaticamente a cada push na branch `main`:

1. **Checkout** — clona o repositório
2. **AWS credentials** — configura acesso via secrets do GitHub
3. **ECR login** — autentica no repositório de imagens
4. **Build & Push** — builda e envia a imagem com tags `sha` e `latest`
5. **Deploy ECS** — força novo deployment no serviço

**Secrets necessários no GitHub:**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

---

## 👤 Autor

**Flávio da Paixão Nunes**
Backend Developer & AWS Cloud Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-flaviopx-blue?style=flat&logo=linkedin)](https://linkedin.com/in/flaviopx)
[![GitHub](https://img.shields.io/badge/GitHub-Flavio--Paixao-black?style=flat&logo=github)](https://github.com/Flavio-Paixao)
[![Portfolio](https://img.shields.io/badge/Portfolio-fpx.dev-orange?style=flat)](https://projeto-aws-681892816208-sa-east-1-an.s3.sa-east-1.amazonaws.com/index.html)
