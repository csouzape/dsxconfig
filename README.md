<div align="center">

```
   ██████╗ ███████╗██╗  ██╗ ██████╗ ██████╗ ███╗   ██╗███████╗██╗ ██████╗
   ██╔══██╗██╔════╝╚██╗██╔╝██╔════╝██╔═══██╗████╗  ██║██╔════╝██║██╔════╝
   ██║  ██║███████╗ ╚███╔╝ ██║     ██║   ██║██╔██╗ ██║█████╗  ██║██║  ███╗
   ██║  ██║╚════██║ ██╔██╗ ██║     ██║   ██║██║╚██╗██║██╔══╝  ██║██║   ██║
   ██████╔╝███████║██╔╝ ██╗╚██████╗╚██████╔╝██║ ╚████║██║     ██║╚██████╔╝
   ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝
```

# 🔧 DSXConfig — Salve seus programas do Linux em um arquivo

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python)](https://www.python.org)
[![License](https://img.shields.io/github/license/csouzape/dsxconfig)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-blue)](https://github.com/csouzape/dsxconfig/releases)

</div>

---

## 🤔 O que é DSXConfig?

Imagine que você tem um computador com **todos os seus programas favoritos instalados**. Agora você quer:
- Mudar de computador
- Reinstalar o Linux
- Começar tudo do zero

**Sem perder nenhum programa ou configuração!**

**DSXConfig faz exatamente isso:** ele **salva uma lista com todos os seus programas** em um arquivo que pode ser executado em qualquer outro computador Linux para instalar tudo automaticamente.

### 💡 Analogia simples:
Pense como se fosse uma **lista de compras** da sua instalação. Em vez de você lembrar de cada programa que tem, o DSXConfig faz uma lista completa e você pode usar essa lista quantas vezes quiser.

---

## 📦 Quais programas ele salva?

DSXConfig salva **3 tipos de programas**:

| Tipo | O que é? | Exemplo |
|------|----------|---------|
| **Programas nativos** | Programas do gerenciador de pacotes do seu Linux | Firefox, Git, VS Code |
| **AUR** (só Arch) | Programas extras da comunidade Arch Linux | Spotify, Discord |
| **Flatpak** | Programas portáveis que funcionam em qualquer Linux | Blender, OBS |

---

## ✨ O que ele faz de especial?

✅ **Fácil de usar** — interface com menus interativos  
✅ **Rápido** — salva e restaura tudo automaticamente  
✅ **Seguro** — não mexe em arquivos do sistema  
✅ **Portável** — funciona em qualquer distribuição Linux  
✅ **Automático** — você só clica e ele faz o resto  

---

## 🖥️ Quais Linuxes funcionam?

| Linux | Suporta? |
|-------|----------|
| **Arch Linux** | ✅ Funciona |
| **Ubuntu / Debian / Linux Mint** | ✅ Funciona |
| **Fedora / Red Hat / CentOS** | ✅ Funciona |

---

## 📋 Pré-requisitos (O que você precisa ter)

Você só precisa de 2 coisas:

### 1️⃣ Python 3.8 ou superior
A maioria dos Linuxes já vem com Python instalado. Para verificar:
```bash
python3 --version
```

Se não tiver, instale:

**Arch Linux:**
```bash
sudo pacman -S python
```

**Ubuntu/Debian:**
```bash
sudo apt install python3
```

**Fedora:**
```bash
sudo dnf install python3
```

### 2️⃣ FZF (Ferramenta de busca interativa)
É um programinha pequeno que deixa a interface bonita. Instale:

**Arch Linux:**
```bash
sudo pacman -S fzf
```

**Ubuntu/Debian:**
```bash
sudo apt install fzf
```

**Fedora:**
```bash
sudo dnf install fzf
```

---

## 🚀 Como instalar?

### Passo 1: Baixe o programa
```bash
git clone https://github.com/csouzape/dsxconfig.git
cd dsxconfig
```

Se você não tem `git`, instale:
```bash
sudo apt install git    # Ubuntu/Debian
sudo pacman -S git      # Arch
sudo dnf install git    # Fedora
```

### Passo 2: Pronto! Execute quando quiser
```bash
python3 main.py
```

---

## 📖 Como usar — Passo a Passo

### 🎯 Objetivo 1: Salvar seus programas

#### Passo 1: Abra o programa
```bash
python3 main.py
```

Você verá uma tela assim:
```
================================================
  DSXConfig System Restoration
  Target: Ubuntu 22.04 LTS
================================================

DSXConfig >
  1 - Export System (Generate .sh)
  2 - View System Info
  3 - About
  0 - Exit
```

#### Passo 2: Escolha "Export System"
Aperte **1** e depois **Enter**

#### Passo 3: Selecione quais programas quer salvar

O programa vai perguntar:
- "Salvar programas do apt?" → Escolha **Sim** para salvar programas principais
- "Salvar programas AUR?" → Escolha **Sim** se estiver no Arch Linux
- "Salvar Flatpak?" → Escolha **Sim** se tiver Flatpak instalado

#### Passo 4: Salve o arquivo
O programa vai criar um arquivo chamado **`restore_dsx_20260519.sh`**

**Pronto! Você salvou todos os seus programas em um arquivo!**

---

### 🔄 Objetivo 2: Restaurar seus programas em outro computador

#### Passo 1: Copie o arquivo
Copie o arquivo `restore_dsx_*.sh` para um **pendrive** ou **nuvem** e leve para seu novo computador.

#### Passo 2: Dê permissão ao arquivo
Abra um terminal e digite:
```bash
chmod +x restore_dsx_*.sh
```

(Isso permite que o arquivo seja executado)

#### Passo 3: Execute o arquivo
```bash
./restore_dsx_*.sh
```

O programa vai:
1. 🔄 Perguntar se quer atualizar o sistema (você escolhe)
2. 📦 Instalar todos os seus programas automaticamente
3. ✅ Mostrar o progresso da instalação
4. 🎉 Avisar quando tudo estiver pronto

**Pronto! Todos os seus programas foram instalados!**

---

## ❓ Dúvidas Frequentes

### P: Eu perco meus dados?
**R:** Não! DSXConfig só **salva a lista de programas**, não toca em seus arquivos ou documentos.

### P: Preciso ser administrador (root)?
**R:** Sim, quando for **instalar** os programas você vai precisar de permissões de administrador. O programa vai pedir a senha quando necessário.

### P: Posso usar o arquivo em outra distribuição Linux?
**R:** **Sim!** Um arquivo de um Ubuntu pode ser usado em Fedora, Arch, etc. O programa automaticamente adapta os nomes dos programas para cada Linux.

### P: E se um programa não existir em outro Linux?
**R:** O programa avisa e tenta continuar com os outros. Alguns programas podem precisar ser instalados manualmente (mas são raros).

### P: Quanto tempo demora?
**R:** Depende de quantos programas você tem e da sua internet. De 5 minutos até alguns anos 😄

### P: Posso editar o arquivo depois?
**R:** **Sim!** Abra o arquivo `.sh` com qualquer editor de texto e remova linhas dos programas que não quer instalar.

### P: O que é esse "FZF" que preciso instalar?
**R:** É um programa que deixa a interface mais legal com menus interativos. Sem ele, funciona mas fica bem mais chato 😅

### P: Posso usar isso em servidores?
**R:** **Sim!** DSXConfig funciona muito bem em servidores para clonar instalações de múltiplas máquinas.

---

## 🔧 Se algo der errado

### Erro: "fzf not found"
```bash
# Instale fzf:
sudo apt install fzf      # Ubuntu/Debian
sudo pacman -S fzf        # Arch
sudo dnf install fzf      # Fedora
```

### Erro: "No packages found"
Isso significa que nenhum programa foi encontrado. Verifique se:
1. Seu gerenciador de pacotes está funcionando
2. Você tem internet conectada
3. Tente executar: `sudo pacman -Q` (Arch) ou `apt list --installed` (Ubuntu)

### Erro: "Permission denied"
Execute com `sudo`:
```bash
sudo python3 main.py
```

---

## 🎓 Exemplos de uso prático

### Exemplo 1: Mudar de notebook
1. No notebook antigo, execute `python3 main.py` e escolha "Export"
2. Salve o arquivo em um pendrive
3. No notebook novo, execute o arquivo e pronto!

### Exemplo 2: Reinstalar o Linux
1. Antes de reinstalar, rode a exportação
2. Salve o arquivo em um lugar seguro (nuvem, pendrive, email)
3. Depois de reinstalar, rode o arquivo e recupere tudo

### Exemplo 3: Ambiente de desenvolvimento
Se você tem um ambiente de desenvolvimento configurado, pode clonar tudo para outros computadores com um comando.

---

## 📝 Changelog

### v2.0.0 (19/05/2026)
- ✅ Interface melhorada e didática
- ✅ Atualização opcional do sistema
- ✅ Melhor detecção de programas
- ✅ Compatibilidade com mais Linuxes

---

## 📄 Licença

MIT © [csouzape](https://github.com/csouzape)

---

## 🤝 Quer contribuir?

Achou um bug ou tem uma ideia? Abra uma **Issue** ou faça um **Pull Request**!

---

**Dúvidas?** Abra uma [Issue](https://github.com/csouzape/dsxconfig/issues) e vamos ajudar! 😊

