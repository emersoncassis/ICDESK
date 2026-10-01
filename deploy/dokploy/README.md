# Servidor ICDESK na VPS (Dokploy)

O servidor é o que faz os computadores se encontrarem pelo ID. Há dois caminhos:

| | Arquivo | O que é |
|---|---|---|
| **Pro (escolhido)** | `docker-compose.pro.yml` | Console web, API, gerador de cliente personalizado (nome, logo e ícone próprios, já com o seu servidor). Exige licença paga. |
| OSS (alternativa) | `docker-compose.oss.yml` | Só ID e relay, gratuito, sem console. |

## Servidor Pro

### 1. Licença

A licença é comprada em [rustdesk.com/pricing.html](https://rustdesk.com/pricing.html) e ativada no console web (passo 5). Confira lá qual plano inclui o **gerador de cliente personalizado**.

### 2. DNS e firewall

- Registro **A** `desk.seudominio.com` apontando para o IP da VPS. Se usar Cloudflare, deixe **somente DNS** (nuvem cinza).
- Portas de entrada: **TCP 21114-21119** e **UDP 21116**.
- Até trocar a senha padrão (passo 5), restrinja a **21114** ao seu IP: o console sobe com usuário e senha conhecidos.

### 3. Dokploy

1. Projeto > serviço do tipo **Compose** > cole `docker-compose.pro.yml`.
2. **Deploy**. Não configure domínio/Traefik: a rede é a do próprio servidor (`network_mode: host`, obrigatório no Pro).

O volume `icdesk-data` guarda as chaves, o banco e a licença. **Não apague**, e faça backup dele.

### 4. Chave pública

No terminal do contêiner `icdesk-hbbs` (ou SSH na VPS):

```sh
cat /root/id_ed25519.pub
```

(no host: `sudo docker exec icdesk-hbbs cat /root/id_ed25519.pub`). Guarde esse texto: é a chave pública, pode ser compartilhada.

### 5. Console web

1. Abra `http://IP-da-VPS:21114` e entre com o usuário e a senha padrão do guia oficial.
2. **Troque a senha de admin imediatamente.**
3. Ative a licença.

### 6. Gerar o cliente ICDESK

No console, abra o gerador de **Custom Client** e informe:

- nome do app: `ICDESK`
- logo e ícone: `res/icon.png` (1024 px) e `res/logo-header.svg`/`flutter/assets/logo_light.png` deste repositório
- servidor de ID: `desk.seudominio.com`, chave: a do passo 4, servidor de API: `http://desk.seudominio.com:21114`

Plataformas atuais do gerador segundo o guia oficial: Windows x64, macOS (Arm64/X64), Linux e Android Arm64. Baixe os instaladores gerados e distribua.

> Os clientes do gerador saem da base oficial, **não** deste repositório. O que está aqui (tema preto/dourado, português por padrão, textos) só vale para builds feitos a partir deste fork.

## Servidor OSS (alternativa)

`docker-compose.oss.yml`, com `ICDESK_DOMAIN=desk.seudominio.com` na aba Environment. Portas: TCP 21115, TCP/UDP 21116, TCP 21117. Chave: `cat /root/id_ed25519.pub` no contêiner `icdesk-hbbs`. Para gerar apps deste fork apontando para ele, crie no GitHub (Settings > Secrets and variables > Actions) os secrets `ICDESK_SERVER` e `ICDESK_KEY` e rode **Actions > Flutter Nightly Build**.

## Teste rápido

Instale em dois computadores, anote o ID de um e conecte pelo outro. Se ficar em "Conectando..." para sempre, quase sempre é a porta UDP 21116 ou TCP 21117 fechada.
