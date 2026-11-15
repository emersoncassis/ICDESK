---
name: acesso-remoto-4-build
description: Gera os instaladores da sua versão do acesso remoto (Windows, macOS, Linux e Android) pelo GitHub Actions, já com o seu servidor e a sua chave embutidos, e confere o resultado. Use quando a pessoa falar em "build", "gerar os instaladores", "compilar", "segredos do GitHub", "ICDESK_SERVER", "release", ou na etapa 4 do guia acesso-remoto-0-comece-aqui.
---

# Etapa 4: build dos apps

Os apps são compilados de graça pelo GitHub Actions (repositórios públicos não pagam minutos).
O endereço e a chave do servidor entram no app na hora da compilação, como padrão: o usuário
instala e já conecta, sem configurar nada.

Pré-requisitos: etapa 3 concluída (endereço e chave pública em mãos) e Actions habilitado no fork.

## 1. Cadastrar os segredos

Pergunte o endereço (ex.: `desk.empresa.com.br`) e a chave pública da etapa 3. Depois, no GitHub:
**Settings > Secrets and variables > Actions > New repository secret**

| Nome | Valor |
|---|---|
| `ICDESK_SERVER` | o endereço, sem `http://` (ex.: `desk.empresa.com.br`) |
| `ICDESK_KEY` | a chave pública (conteúdo de `id_ed25519.pub`) |

Os nomes dos segredos continuam `ICDESK_*` mesmo com outra marca: são nomes internos do build.
Com o GitHub CLI logado dá para fazer pelo terminal:
```bash
gh secret set ICDESK_SERVER --body "desk.empresa.com.br"
gh secret set ICDESK_KEY --body "CHAVE_PUBLICA"
```

## 2. Rodar o build

Envie as mudanças das etapas anteriores (`git push`) e rode **Actions > Flutter Nightly Build >
Run workflow** (ou `gh workflow run flutter-nightly.yml`). Depois disso ele roda sozinho toda noite.
Leva cerca de 1 h 30. Os arquivos saem na release `nightly` do repositório
(`https://github.com/USUARIO/REPOSITORIO/releases/tag/nightly`).

Alguns jobs podem falhar ou ser cancelados no fork por dependerem de assinaturas e chaves do
projeto original (ex.: assinatura de macOS/Windows). Isso não impede os demais: confira se os
principais instaladores apareceram na release (`*-x86_64.exe`, `*.msi`, `*-universal.apk`,
`*-x86_64.deb`, `*.dmg`).

## 3. Conferir se o servidor foi embutido

Baixe o `.deb` de Linux e procure o endereço dentro da biblioteca:
```bash
dpkg-deb -x rustdesk-*-x86_64.deb x
strings x/usr/share/rustdesk/lib/librustdesk.so | grep -c "desk.empresa.com.br"   # tem que ser ≥ 1
```
No Windows, basta instalar e abrir Configurações > Rede: o servidor de ID já vem preenchido.
Teste real: instale em dois aparelhos e conecte um no outro pelo ID.

## 4. Avisos para passar à pessoa

- Windows e macOS mostram aviso de "editor desconhecido" porque os instaladores não são assinados.
  Assinar exige certificado pago (opcional, pode ficar para depois).
- iPhone/iPad: não há instalador público; publicar na App Store exige conta de desenvolvedor Apple.
- Se o servidor ou a chave mudarem, atualize os segredos e gere os apps de novo.

Siga para `acesso-remoto-5-site`.
