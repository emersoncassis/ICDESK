---
name: acesso-remoto-3-servidor
description: Coloca no ar o servidor gratuito e open source (hbbs + hbbr do RustDesk Server OSS) da sua versão do acesso remoto, na AWS, na Hostinger, em outro VPS, no Dokploy ou numa máquina local com IP fixo, e obtém a chave pública. Use quando a pessoa falar em "servidor", "deploy", "VPS", "AWS", "Hostinger", "IP fixo", "chave pública", ou na etapa 3 do guia acesso-remoto-0-comece-aqui.
---

# Etapa 3: servidor

O servidor é o que faz os aparelhos se encontrarem pelo ID e, quando a conexão direta não é
possível, repassa o tráfego (relay). Usamos o **RustDesk Server OSS**: gratuito, open source,
sem licença. Ele é leve: 1 vCPU e 1 GB de RAM atendem bem um uso pequeno ou médio.

Resultado: um endereço (`desk.seudominio.com` ou um IP) e a chave pública do servidor.

## 1. Perguntas

1. Onde vai rodar?
   a) AWS (Lightsail é o mais simples; EC2 se já usa AWS)
   b) Hostinger VPS
   c) Outro VPS (DigitalOcean, Contabo, Oracle Cloud, Hetzner…)
   d) Dokploy (já tem um painel Dokploy num VPS)
   e) Máquina local com IP fixo (um PC ou mini-servidor ligado 24 h)
2. Tem um domínio? Se sim, qual subdomínio usar (ex.: `desk.empresa.com.br`)? Sem domínio,
   dá para usar o IP público, mas trocar de servidor depois obriga a gerar os apps de novo.
3. Você tem acesso SSH ao servidor? (Se a pessoa não souber, guie pelo painel do provedor.)

## 2. Portas (iguais para todos os casos)

| Porta | Protocolo | Uso |
|---|---|---|
| 21115 | TCP | teste de tipo de NAT |
| 21116 | TCP **e** UDP | registro do ID e conexão direta |
| 21117 | TCP | relay |

Mais a 22/TCP (SSH), que **deve ficar aberta antes de ativar qualquer firewall**.
21118 e 21119 só são necessárias para o cliente web; não abra se não for usar.

## 3. Preparar a máquina conforme o lugar

**AWS Lightsail:** crie uma instância Linux (Ubuntu LTS). Na aba **Networking**, em
"IPv4 Firewall", adicione regras para as portas acima (TCP 21115-21117 e UDP 21116).
Crie e anexe um **IP estático** (senão o IP muda ao reiniciar).

**AWS EC2:** instância Ubuntu LTS; no **Security Group** da instância, regras de entrada para as
portas acima; associe um **Elastic IP**.

**Hostinger VPS:** escolha Ubuntu (o modelo com Docker já instalado poupa um passo). No hPanel,
VPS > **Firewall**: crie um grupo, adicione regras "Aceitar" para TCP 22, TCP 21115-21117 e
UDP 21116, e ative. O firewall da Hostinger bloqueia tudo o que não tiver regra.

**Outro VPS:** o mesmo raciocínio: Ubuntu LTS, IP fixo e as portas liberadas no painel do provedor.

**Dokploy:** use `deploy/dokploy/docker-compose.oss.yml` como serviço do tipo Compose,
com `ICDESK_DOMAIN=desk.seudominio.com` na aba Environment, e siga `deploy/dokploy/README.md`
(parte "Servidor OSS"). Pule para o passo 5.

**Máquina local com IP fixo:** confirme com a operadora que o IP é fixo e que não há CGNAT
(o IP que aparece no roteador tem que ser o mesmo de sites como "qual é meu IP").
No roteador, redirecione (port forwarding) TCP 21115-21117 e UDP 21116 para o IP interno da máquina,
e reserve esse IP interno no DHCP. Instale Docker (Linux) ou Docker Desktop (Windows/macOS).
A máquina precisa ficar ligada sempre.

Em qualquer Linux com `ufw` ativo, libere também no sistema:
```bash
sudo ufw allow OpenSSH && sudo ufw allow 21115:21117/tcp && sudo ufw allow 21116/udp
```

## 4. Subir o servidor (Docker)

```bash
curl -fsSL https://get.docker.com | sh          # se o Docker ainda não estiver instalado
mkdir -p ~/acesso-remoto && cd ~/acesso-remoto
# copie para cá o arquivo deploy/dokploy/docker-compose.oss.yml do repositório, com o nome compose.yml
echo "ICDESK_DOMAIN=desk.seudominio.com" > .env      # ou o IP público
docker compose -f compose.yml up -d
docker compose -f compose.yml ps                     # os dois serviços devem estar "running"
```
O `-k _` no arquivo faz o servidor só aceitar apps que tenham a chave dele.

## 5. Chave pública e DNS

```bash
docker exec icdesk-hbbs cat /root/id_ed25519.pub
```
Guarde esse texto: é a **chave pública** (pode compartilhar). Nunca copie `id_ed25519` (sem `.pub`).
Faça backup do volume `icdesk-data`: se ele se perder, a chave muda e todos os apps precisam ser gerados de novo.

DNS: registro **A** do subdomínio apontando para o IP. No Cloudflare, deixe "somente DNS" (nuvem cinza):
o proxy do Cloudflare não repassa essas portas.

## 6. Testar

De um computador fora da rede do servidor:
```bash
nc -zv desk.seudominio.com 21116 && nc -zv desk.seudominio.com 21117
```
Teste final: instale o app oficial do RustDesk em dois aparelhos, coloque em Configurações > Rede
o servidor de ID e a chave, e conecte um no outro. Se ficar em "Conectando…", quase sempre é a
UDP 21116 ou a TCP 21117 fechada.

Anote o endereço e a chave e siga para `acesso-remoto-4-build`.
