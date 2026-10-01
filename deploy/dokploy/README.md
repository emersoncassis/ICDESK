# Servidor ICDESK no Dokploy

O servidor é o que faz os computadores se encontrarem pelo ID. Ele roda em dois contêineres (`hbbs` e `hbbr`) na sua VPS.

## 1. DNS

Crie um registro **A** `desk.seudominio.com` apontando para o IP da VPS. Se usar Cloudflare, deixe **somente DNS** (nuvem cinza): o tráfego não é HTTP e não passa pelo proxy.

## 2. Firewall da VPS

Libere estas portas (entrada):

| Porta | Protocolo | Para quê |
|---|---|---|
| 21115 | TCP | teste de NAT |
| 21116 | TCP **e UDP** | registro e conexão por ID |
| 21117 | TCP | relay |

## 3. Dokploy

1. Crie um projeto e adicione um serviço do tipo **Compose** (Raw ou apontando para este repositório, pasta `deploy/dokploy`).
2. Cole o conteúdo de `docker-compose.yml`.
3. Na aba **Environment**, defina `ICDESK_DOMAIN=desk.seudominio.com`.
4. **Deploy**. Não configure domínio/Traefik: o compose usa a rede do próprio servidor (`network_mode: host`, como no guia oficial), então as portas abrem direto na VPS.

O compose usa `-k _`: o servidor só aceita apps que tenham a chave dele (os apps gerados já a levam). O volume `icdesk-data` guarda o par de chaves do servidor. **Não apague esse volume**: se a chave mudar, todos os apps já instalados deixam de conectar.

## 4. Pegar a chave pública

No Dokploy, abra o terminal do contêiner `icdesk-hbbs` (ou use SSH na VPS) e rode:

```sh
cat /root/id_ed25519.pub
```

Guarde esse texto (uma linha, termina com `=`). É a chave pública (pode ser compartilhada); a `id_ed25519` sem `.pub` é privada e nunca sai do servidor.

## 5. Gerar os apps apontando para o seu servidor

No GitHub, em **Settings > Secrets and variables > Actions**, crie:

| Secret | Valor |
|---|---|
| `ICDESK_SERVER` | `desk.seudominio.com` |
| `ICDESK_KEY` | o conteúdo de `id_ed25519.pub` |

Depois vá em **Actions > Flutter Nightly Build > Run workflow**. Ao terminar, os instaladores ficam nos artefatos da execução. Os apps já saem com o servidor e a chave como padrão (o usuário ainda pode trocar em Configurações > Rede).

Assinatura: o Android precisa do secret `ANDROID_SIGNING_KEY` e o macOS de uma conta de desenvolvedor Apple; o Windows sai sem assinatura (o SmartScreen avisa na primeira execução).

## Teste rápido

Instale em dois computadores, anote o ID de um e conecte pelo outro. Se ficar em "Conectando..." para sempre, quase sempre é porta UDP 21116 ou TCP 21117 fechada no firewall.
