---
name: acesso-remoto-0-comece-aqui
description: Ponto de partida para criar o seu próprio sistema de acesso remoto a partir de um fork do ICDESK. Use quando a pessoa disser "quero fazer a minha versão", "criar meu acesso remoto", "comece aqui", "por onde começo", ou quando não estiver claro em qual etapa ela está.
---

# Crie o seu sistema de acesso remoto (comece aqui)

Este repositório é um fork do ICDESK (que por sua vez é um fork do RustDesk, licença AGPL-3.0).
O objetivo é a pessoa sair com: marca própria, apps (Windows, macOS, Linux, Android) já apontando
para o servidor dela, servidor no ar e um site de download no GitHub Pages.

Fale em português do Brasil, em linguagem simples. A pessoa pode não ser programadora.

## As etapas, nesta ordem

| # | Skill | Resultado |
|---|---|---|
| 1 | `acesso-remoto-1-marca` | Nome, cores, logo e todos os ícones do app trocados |
| 2 | `acesso-remoto-2-design-system` | Tokens de cor/fonte aplicados no app e no site |
| 3 | `acesso-remoto-3-servidor` | Servidor de ID e relay no ar (AWS, Hostinger, outro VPS ou máquina local com IP fixo) e a chave pública |
| 4 | `acesso-remoto-4-build` | Segredos no GitHub e instaladores gerados pelo GitHub Actions |
| 5 | `acesso-remoto-5-site` | Landing page com downloads no GitHub Pages |

As etapas 1–2 e a 3 são independentes; a 4 precisa da 3 (endereço e chave do servidor); a 5 precisa da 4.

## O que fazer ao ser acionada

1. Confira o ambiente, sem perguntar o que dá para descobrir sozinho:
   - `git remote -v` — é um fork (origin é da pessoa)? Se for o repositório `emersoncassis/ICDESK`
     original, pare e explique como fazer o fork (passo 0 abaixo).
   - `git config user.name` está preenchido?
   - Existe `brand/BRAND.md`? Se sim, a etapa 1 já foi feita.
   - Os segredos `ICDESK_SERVER`/`ICDESK_KEY` não dá para ler; pergunte se já foram criados.
2. Mostre a tabela acima marcando o que já está feito e pergunte por qual etapa seguir.
3. Siga a skill da etapa escolhida. Ao terminar cada etapa, faça um commit com mensagem clara
   e pergunte se pode seguir para a próxima.

## Passo 0: fork e clone (se ainda não fez)

1. Crie uma conta no GitHub, abra https://github.com/emersoncassis/ICDESK e clique em **Fork**.
   Dê um nome ao repositório (ex.: `meudesk`). Deixe marcado "Copy the master branch only".
2. Clone com submódulos: `git clone --recurse-submodules https://github.com/USUARIO/REPOSITORIO`
3. Abra a pasta no Claude Code, Codex ou Antigravity. As skills ficam em:
   - Claude Code: `.claude/skills/`
   - Codex e Antigravity: `.agents/skills/`
4. No fork, abra **Actions** e clique em "I understand my workflows, go ahead and enable them".

## Regras para todas as etapas

- Pergunte antes de decidir gosto (nome, cores, logo, texto do site). Sugira opções, mas a decisão é da pessoa.
- Nunca grave senhas, chaves privadas (`id_ed25519` sem `.pub`) ou tokens no repositório.
  A chave **pública** (`id_ed25519.pub`) pode ser compartilhada.
- Não mude os nomes internos (pacote Android `com.carriez.flutter_hbb`, binário `rustdesk`,
  variáveis `ICDESK_SERVER`/`ICDESK_KEY`, módulo `src/icdesk.rs`): eles não aparecem para o usuário
  e trocá-los quebra o build. Só trocamos o que a pessoa vê.
- Mantenha o aviso de licença AGPL-3.0 e o crédito ao RustDesk.
- O uso de acesso remoto exige autorização do dono do aparelho; mantenha esse aviso no site.
