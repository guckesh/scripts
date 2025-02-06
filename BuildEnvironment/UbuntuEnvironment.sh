#!/bin/bash

# Verifica se o script está sendo executado como root
if [ "$(id -u)" != "0" ]; then
   echo "Este script deve ser executado como root. Use sudo."
   exit 1
fi

echo "Instalando e configurando o Zsh como shell padrão..."

# Instala o Zsh
apt update && apt install -y zsh || {
    echo "Erro ao instalar o Zsh. Saindo..."
    exit 1
}

# Define o Zsh como shell padrão para o usuário atual
chsh -s $(which zsh) || {
    echo "Erro ao definir o Zsh como shell padrão."
    exit 1
}

# Instala o Oh My Zsh
echo "Instalando Oh My Zsh..."
sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" || {
    echo "Erro ao instalar Oh My Zsh. Saindo..."
    exit 1
}

# Configura o tema do Zsh
echo "Configurando tema 'bira' no Oh My Zsh..."
sed -i 's/^ZSH_THEME=".*"/ZSH_THEME="bira"/' ~/.zshrc || {
    echo "Erro ao configurar o tema 'bira'."
}

# Adiciona variáveis de ambiente ao arquivo .zshrc
echo "Configurando variáveis de ambiente no .zshrc..."
cat <<EOF >>~/.zshrc

# Variáveis para compilação Android
export USE_CCACHE=1
export CCACHE_DIR=~/.ccache
export ANDROID_HOME=~/Android/Sdk
export PATH=\$ANDROID_HOME/platform-tools:\$ANDROID_HOME/tools:\$PATH
EOF

echo "Shell Zsh configurado com sucesso. Reinicie o terminal para aplicar as mudanças ao shell."
echo "Continuando com a instalação dos pacotes necessários..."

# Atualização do sistema
echo "Atualizando o sistema..."
apt update && apt upgrade -y || { 
    echo "Erro ao atualizar o sistema. Saindo..."; 
    exit 1; 
}

# Instalação do Python mais recente e pip3
echo "Instalando o Python mais recente e pip3..."
add-apt-repository -y ppa:deadsnakes/ppa || {
    echo "Erro ao adicionar repositório do Python mais recente."
    exit 1
}

apt update || exit 1
apt install -y python3.11 python3.11-venv python3.11-dev python3-pip || {
    echo "Erro ao instalar o Python mais recente e pip3. Saindo..."
    exit 1
}

echo "Verificando versões instaladas:"
python3.11 --version || echo "Erro ao verificar versão do Python."
pip3 --version || echo "Erro ao verificar versão do pip3."

# Instalação de pacotes essenciais
echo "Instalando pacotes necessários..."
apt install -y build-essential git openjdk-11-jdk wget unzip openssh-client neofetch gufw curl software-properties-common || {
    echo "Erro ao instalar pacotes. Saindo..."
    exit 1
}

# Instalação de pacotes adicionais necessários
echo "Instalando pacotes adicionais necessários..."
apt install -y libncurses5 libncurses5-dev zlib1g zlib1g-dev gcc-multilib g++-multilib clang lld ninja-build flex bison || {
    echo "Erro ao instalar pacotes adicionais. Saindo..."
    exit 1
}

# Configuração do Git
echo "Configurando Git..."
git config --global user.email "mezaquegit@gmail.com"
git config --global user.name "Mezaque Silver"
echo "Configuração do Git concluída: email 'mezaquegit@gmail.com', nome 'Mezaque Silver'."

# Configuração da ferramenta repo
echo "Baixando e configurando a ferramenta repo..."
mkdir -p ~/bin
if [ ! -f ~/bin/repo ]; then
    curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo || {
        echo "Erro ao baixar a ferramenta repo. Saindo..."
        exit 1
    }
    chmod a+x ~/bin/repo
    export PATH=~/bin:\$PATH
fi

# Preparação para compilação Android
echo "Preparando diretório para código-fonte Android..."
mkdir -p ~/android15 || {
    echo "Erro ao criar diretório para código-fonte."
    exit 1
}

cd ~/android15

# Configuração da chave SSH
echo "Gerando chave SSH para o Git..."
if [ ! -f ~/.ssh/id_rsa ]; then
    read -p "Digite o email para configurar sua chave SSH: " user_email
    ssh-keygen -t rsa -b 4096 -C "$user_email" -N "" -f ~/.ssh/id_rsa || {
        echo "Erro ao gerar a chave SSH."
        exit 1
    }
    echo "Chave SSH gerada:"
    cat ~/.ssh/id_rsa.pub

    echo "Adicionando a chave SSH ao agente..."
    eval "$(ssh-agent -s)" || echo "Erro ao iniciar o agente SSH."
    ssh-add ~/.ssh/id_rsa || {
        echo "Erro ao adicionar chave ao agente SSH."
    }

    echo "Por favor, adicione a seguinte chave pública ao seu repositório Git (GitHub, GitLab, etc.):"
    echo "--------------------------------------"
    cat ~/.ssh/id_rsa.pub
    echo "--------------------------------------"

    echo "Abrindo a página de configuração de chaves SSH do GitHub..."
    xdg-open "https://github.com/settings/keys" 2>/dev/null || echo "Abra https://github.com/settings/keys manualmente."
else
    echo "Chave SSH já existe. Pule esta etapa."
fi

echo "Script concluído com sucesso. Reinicie o terminal para aplicar as mudanças."
