---
name: acesso-remoto-1-marca
description: Cria a identidade da sua versão do acesso remoto (nome, empresa, cores, logo) e troca nome e ícones em todos os apps. Use quando a pessoa quiser "criar a marca", "trocar o nome do app", "trocar o logo/ícone", "rebranding", ou na etapa 1 do guia acesso-remoto-0-comece-aqui.
---

# Etapa 1: marca

Resultado: `brand/BRAND.md` com as decisões, o nome novo em todos os textos que o usuário vê,
e os ícones de Windows, macOS, Linux, Android e iOS gerados a partir do logo da pessoa.

## 1. Entrevista (pergunte, uma rodada por vez, e espere as respostas)

Rodada A, o negócio:
1. Qual o nome do app? (curto, fácil de falar ao telefone; ex.: "MeuDesk", "SuporteJá")
2. Qual o nome da empresa ou de quem oferece? (aparece no rodapé e nos créditos)
3. Para quem é? (técnicos, empresas, família, clientes de um setor específico)
4. Em uma frase: o que o app promete? (vira o slogan do site)

Rodada B, a cara:
5. Já tem logo? Se sim, peça o arquivo (SVG de preferência; PNG de pelo menos 1024 px).
6. Cores: tem cores da marca (hex ou um site para copiar)? Se não, ofereça 3 paletas prontas
   coerentes com o público, cada uma com: fundo, cor principal, cor de destaque e um acento.
7. Tema do app e do site: escuro ou claro?
8. Fonte de título: tem alguma? Se não, sugira uma do Google Fonts com licença aberta.
9. Personalidade em 3 palavras (ex.: "confiável, direto, moderno").

Se a pessoa não tiver logo, proponha 2 ou 3 conceitos simples (monograma com as iniciais dentro
de um círculo ou quadrado arredondado) e desenhe o escolhido em SVG. Não copie logos de terceiros.

## 2. Registrar as decisões

Crie `brand/BRAND.md` com: nome, empresa, público, slogan, personalidade, paleta (hex e papel de
cada cor), fonte e tema. As próximas etapas leem este arquivo.

## 3. Trocar o nome em todos os textos

```bash
python3 .agents/skills/acesso-remoto-1-marca/scripts/renomear_marca.py "NOME" "EMPRESA"           # simulação
python3 .agents/skills/acesso-remoto-1-marca/scripts/renomear_marca.py "NOME" "EMPRESA" --aplicar
```
(No Claude Code o caminho é `.claude/skills/...`.) Mostre a simulação à pessoa antes de aplicar.
Depois confira `git diff --stat` e abra 2 ou 3 arquivos para ver se ficou natural
(ex.: `src/lang/pt_BR.rs`, `flutter/android/app/src/main/res/values/strings.xml`, `flutter/ios/Runner/Info.plist`).
Atualize também o `README.md` (título, descrição) com o nome novo.

## 4. Gerar os ícones

O exportador `res/icdesk-brand/export.py` lê SVGs da pasta `res/icdesk-brand/svg/` e grava todos
os ícones do app. Crie nessa pasta, a partir do logo da pessoa, estes arquivos (todos com
`viewBox="0 0 1024 1024"`, exceto os wordmarks):

| Arquivo | O que é |
|---|---|
| `badge_full.svg` | Logo completo, para ícones grandes |
| `badge_simple.svg` | Versão com menos detalhe (64–96 px) |
| `badge_tiny.svg` | Versão mínima, legível em 16–48 px (bandeja do sistema) |
| `mac_icon.svg` | Quadrado arredondado no padrão do macOS (margem ~10%) |
| `app_square_full.svg` / `app_square_simple.svg` | Logo em quadrado cheio, para iOS e Android |
| `android_fg.svg` | Só o símbolo, centralizado, ocupando ~60% (o fundo vem da cor) |
| `mono_black.svg` / `mono_white.svg` | Símbolo em uma cor só (bandeja do macOS, notificação Android) |
| `wordmark_light.svg` / `wordmark_dark.svg` | Logo + nome na horizontal, `viewBox="0 0 LARGURA 300"` (altura 300 obrigatória) |

Se o logo veio em PNG, contorne-o em SVG simples (formas e um `<image>` embutido em base64 também
funcionam para os tamanhos grandes; para `badge_tiny` e `mono_*` desenhe formas vetoriais).

Antes de exportar, troque em `export.py` a cor fixa `#0D0D0D` (fundo do ícone adaptativo do Android)
pela cor de fundo da marca. Depois:

```bash
pip install cairosvg fonttools pillow     # e ImageMagick (comando "convert")
cd res/icdesk-brand && python3 export.py
```
A pasta `svg/` não vai para o git (o `.gitignore` ignora `*.svg` ali): guarde os SVGs fonte em `brand/logo/`
(o `.gitignore` também ignora `*.svg` e `*.png` no resto do projeto, então use `git add -f brand/logo`).

## 5. Conferir e salvar

- Abra `res/icon.png`, `res/32x32.png` e `flutter/assets/logo_light.png` e confira se estão legíveis.
- Commit: `git add -A && git commit -m "marca: NOME (nome, ícones e textos)"`.
- Siga para `acesso-remoto-2-design-system`.
