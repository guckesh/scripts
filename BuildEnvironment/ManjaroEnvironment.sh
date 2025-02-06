#!/bin/bash

# Função para verificar se um comando existe
command_exists() {
    command -v "$1" &> /dev/null
}

# Atualizar o sistema e instalar dependências básicas
echo "Atualizando o sistema e instalando dependências básicas..."
sudo pacman -Syu --needed --noconfirm base-devel git wget curl unzip zsh

# Verificar se Zsh está instalado
if ! command_exists zsh; then
    echo "Erro: Zsh não foi instalado corretamente."
    exit 1
fi

# Configurar o Zsh como shell padrão para o usuário atual
echo "Configurando o Zsh como shell padrão..."
if [ "$EUID" -eq 0 ]; then
    echo "Nota: Não é possível alterar o shell do usuário root. Faça logout e altere manualmente com 'chsh -s $(which zsh)'."
else
    chsh -s "$(which zsh)"
fi
echo "Shell padrão configurado para Zsh. Faça logout ou reinicie o terminal para aplicar as mudanças."

# Baixar o histórico do Zsh
echo "Baixando o histórico do Zsh do repositório..."
curl -o ~/.zsh_history https://raw.githubusercontent.com/guckesh/guckesh/refs/heads/master/profile/.zsh_history

# Verificar se o download foi bem-sucedido
if [ -f ~/.zsh_history ]; then
    echo "Histórico do Zsh baixado com sucesso."
else
    echo "Erro: Não foi possível baixar o histórico do Zsh."
    exit 1
fi

# Instalar Python e pip
echo "Instalando Python e pip..."
sudo pacman -S --needed --noconfirm python python-pip

# Verificar se Python e pip estão instalados
if ! command_exists python || ! command_exists pip3; then
    echo "Erro: Python ou pip não foram instalados corretamente."
    exit 1
fi

# Configurar ambiente de compilação para AOSP e kernel Android
echo "Configurando ambiente de compilação para AOSP e kernel Android..."

# Dependências do AOSP
echo "Instalando dependências do AOSP..."
sudo pacman -S --needed --noconfirm jdk11-openjdk repo ccache bison gperf libxml2 ninja

# Instalar ncurses5-compat-libs do AUR
if ! command_exists yay; then
    echo "Instalando yay para gerenciar pacotes AUR..."
    git clone https://aur.archlinux.org/yay.git
    cd yay || exit 1
    makepkg -si --noconfirm
    cd .. && rm -rf yay
fi
echo "Instalando ncurses5-compat-libs do AUR..."
yay -S --needed --noconfirm ncurses5-compat-libs

# Configurar variáveis de ambiente
echo "Configurando variáveis de ambiente para o AOSP..."
cat <<EOF >> ~/.zshrc
# Variáveis de ambiente para AOSP
export USE_CCACHE=1
export CCACHE_DIR=~/.ccache
export ANDROID_JAVA_HOME=/usr/lib/jvm/java-11-openjdk
export PATH=\$PATH:\$ANDROID_HOME/tools:\$ANDROID_HOME/platform-tools
EOF

# Baixar a ferramenta repo
echo "Baixando a ferramenta repo..."
mkdir -p ~/bin
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo
export PATH=~/bin:$PATH

# Configurar o cache para compilações mais rápidas
echo "Configurando ccache com 40 GB de espaço..."
ccache -M 40G

# Finalização
echo "Configuração concluída! Certifique-se de reiniciar o terminal para aplicar as mudanças."
