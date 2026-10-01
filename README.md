<p align="center">
  <img src="res/logo-header.svg" alt="ICDESK - Remote Access"><br>
  <a href="#como-funciona">Como funciona</a> •
  <a href="#idioma">Idioma</a> •
  <a href="#identidade-visual">Identidade visual</a> •
  <a href="#compilar">Compilar</a> •
  <a href="#licença">Licença</a>
</p>

# ICDESK

Software de acesso e controle remoto do **IC TEAM**. Permite usar, ver ou consertar um computador ou celular à distância pela internet.

> [!Caution]
> **Aviso de uso:** o ICDESK deve ser usado apenas com autorização do dono do dispositivo. Acesso não autorizado, controle indevido ou invasão de privacidade são usos proibidos, e os autores não se responsabilizam por uso indevido.

## Como funciona

- Cada dispositivo recebe um número de identificação único (ID).
- Para acessar outra máquina, digite o ID no programa.
- O dono do outro aparelho precisa aceitar a conexão para liberar o acesso.
- Funciona em Windows, macOS, Linux, Android e iOS.

## Idioma

A interface abre em **português do Brasil** por padrão. Para trocar, vá em Configurações > Idioma; a escolha fica salva.

- Traduções: [`src/lang/pt_BR.rs`](src/lang/pt_BR.rs) (completo, 780 textos).
- O padrão é definido em `translate_locale`, em [`src/lang.rs`](src/lang.rs).
- Português de Portugal continua disponível em `src/lang/pt_PT.rs`.

## Identidade visual

As cores e o logo do ICDESK foram inspirados na paleta oficial do IC TEAM.

## Compilar

- Tenha o ambiente de desenvolvimento Rust e C++ pronto.
- Instale o [vcpkg](https://github.com/microsoft/vcpkg) e defina a variável `VCPKG_ROOT`.
  - Windows: `vcpkg install libvpx:x64-windows-static libyuv:x64-windows-static opus:x64-windows-static aom:x64-windows-static`
  - Linux/macOS: `vcpkg install libvpx libyuv opus aom`
- Clone com os submódulos: `git clone --recurse-submodules https://github.com/emersoncassis/ICDESK`
- Interface Flutter (atual): `python3 build.py --flutter` (ver `flutter/` para as dependências).
- Execução de desenvolvimento: `cargo run`

## Compilar no Linux

### Ubuntu 18 (Debian 10)

```sh
sudo apt install -y zip g++ gcc git curl wget nasm yasm libgtk-3-dev clang libxcb-randr0-dev libxdo-dev \
        libxfixes-dev libxcb-shape0-dev libxcb-xfixes0-dev libasound2-dev libpulse-dev cmake make \
        libclang-dev ninja-build libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
```

### openSUSE Tumbleweed

```sh
sudo zypper install gcc-c++ git curl wget nasm yasm gcc gtk3-devel clang libxcb-devel libXfixes-devel cmake alsa-lib-devel gstreamer-devel gstreamer-plugins-base-devel xdotool-devel
```

### Fedora 28 (CentOS 8)

```sh
sudo yum -y install gcc-c++ git curl wget nasm yasm gcc gtk3-devel clang libxcb-devel libxdo-devel libXfixes-devel pulseaudio-libs-devel cmake alsa-lib-devel gstreamer1-devel gstreamer1-plugins-base-devel
```

### Arch (Manjaro)

```sh
sudo pacman -Syu --needed unzip git cmake gcc curl wget yasm nasm zip make pkg-config clang gtk3 xdotool libxcb libxfixes alsa-lib pipewire
```

### Install vcpkg

```sh
git clone https://github.com/microsoft/vcpkg
cd vcpkg
git checkout 2023.04.15
cd ..
vcpkg/bootstrap-vcpkg.sh
export VCPKG_ROOT=$HOME/vcpkg
vcpkg/vcpkg install libvpx libyuv opus aom
```

### Fix libvpx (For Fedora)

```sh
cd vcpkg/buildtrees/libvpx/src
cd *
./configure
sed -i 's/CFLAGS+=-I/CFLAGS+=-fPIC -I/g' Makefile
sed -i 's/CXXFLAGS+=-I/CXXFLAGS+=-fPIC -I/g' Makefile
make
cp libvpx.a $HOME/vcpkg/installed/x64-linux/lib/
cd
```

### Compilar e executar

```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
git clone --recurse-submodules https://github.com/emersoncassis/ICDESK
cd ICDESK
VCPKG_ROOT=$HOME/vcpkg cargo run
```

## Licença

Este projeto é derivado de software livre distribuído sob a licença AGPL-3.0. O texto da licença e os avisos de copyright originais estão preservados em [LICENCE](LICENCE) e nos cabeçalhos dos arquivos, conforme a licença exige.
