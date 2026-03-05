<h1 align="center">💬 Commit Creator</h1>
<p align="center">
  Gere mensagens de commit profissionais automaticamente usando IA Gemini.
</p>
<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img alt="Gemini" src="https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white"/>
  <img alt="Git" src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white"/>
  <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>
</p>

---

## 📋 Sobre

O **Commit Creator** é uma ferramenta CLI que analisa o `git diff` e `git status` do seu repositório e usa a IA **Google Gemini** para gerar automaticamente mensagens de commit detalhadas, com prefixo de tipo, descrição e resumo por arquivo. Tudo em português!

## ✨ Funcionalidades

- 🧠 Geração inteligente de mensagens de commit via Gemini
- 📝 Mensagens com prefixo (`feat:`, `fix:`, `docs:`, etc.)
- 📂 Resumo detalhado por arquivo modificado
- ✅ Confirmação interativa antes de commitar
- 🔄 Opção de regenerar o commit se não aprovar
- 🚀 Add + Commit + Push em um único comando

## 📦 Instalação

```bash
git clone https://github.com/LuigiNeto01/Commit_creator.git
cd Commit_creator

pip install -r requirements.txt

cp .env.example .env
# Adicione sua GEMINI_API_KEY no .env
```

## 🔧 Uso

```bash
python main.py /caminho/para/seu/repositorio

# Com modelo específico:
python main.py /caminho/para/seu/repositorio --model gemini-2.5-flash
```

### Fluxo de uso:

1. O script analisa as alterações do repositório
2. A IA gera uma mensagem de commit
3. Você visualiza e aprova (ou pede uma nova)
4. O commit é realizado e enviado automaticamente

## ⚙️ Configuração

```env
GEMINI_API_KEY=sua_chave_api_aqui
```

## 🚀 Tecnologias

- **Python 3.10+**
- **Google Gemini API**
- **GitPython** (via subprocess)

## 📝 Licença

MIT © [LuigiNeto01](https://github.com/LuigiNeto01)

---

<p align="center">Feito com ❤️ por <a href="https://github.com/LuigiNeto01">LuigiNeto01</a></p>
