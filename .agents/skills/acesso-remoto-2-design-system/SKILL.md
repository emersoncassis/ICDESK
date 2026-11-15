---
name: acesso-remoto-2-design-system
description: Monta o design system da sua versão do acesso remoto (tokens de cor, fonte, superfícies e estados) e aplica no app Flutter, nos instaladores e no template do site. Use quando a pessoa falar em "design system", "tokens", "tema do app", "cores do app", "padronizar o visual", ou na etapa 2 do guia acesso-remoto-0-comece-aqui.
---

# Etapa 2: design system

Resultado: uma única fonte da verdade (`brand/tokens.css`) espelhada no app (`flutter/lib/brand.dart`)
e no site (`site/index.html`), para que app, site e materiais tenham a mesma cara.

Leia `brand/BRAND.md` (criado na etapa 1). Se não existir, rode a etapa 1 antes.

## 1. Perguntas (só o que o BRAND.md ainda não responde)

1. Tema: só escuro, só claro, ou os dois? (o ICDESK é escuro; o app aceita os dois)
2. Cantos: retos, levemente arredondados (8 px) ou bem arredondados (16 px)?
3. Densidade: compacto (mais informação na tela) ou espaçoso?
4. Cor de "conectado/online": manter verde padrão ou usar a cor de acento da marca?
   Lembre: cores de status (ok, aviso, erro) **não** podem ser a cor principal da marca,
   senão o usuário confunde destaque com alerta.

## 2. Definir os tokens

Reescreva `brand/tokens.css` no mesmo formato do arquivo atual, com:
- Marca: fundo, principal, principal-claro (hover/links), acento, texto.
- Status: ok, aviso, offline.
- Superfícies derivadas: `surface`, `surface-2`, `hover` (para tema escuro, clareie o fundo em ~4%, ~7%, ~10%).
- Gradiente do logo, se houver.
- Fonte de título (`@import` do Google Fonts) e fonte de texto.
- Contraste: texto sobre fundo ≥ 4,5:1 e texto sobre botão principal ≥ 4,5:1. Calcule e,
  se falhar, ajuste a cor e avise a pessoa.

Mostre a paleta à pessoa (uma tabela com hex, papel e contraste) e só siga depois do "ok".

## 3. Aplicar no app

- `flutter/lib/brand.dart` (classe `IcBrand`): troque cada constante pelo token equivalente.
  Mantenha os nomes das constantes (o app inteiro usa `IcBrand.gold`, `IcBrand.richBlack` etc.);
  só os valores mudam. Atualize os comentários `// --cx-...` se renomear tokens no CSS.
- Procure cores fixas que sobraram: `git grep -nE "0xFFC5A059|0xFF0D0D0D|C5A059|0D0D0D" -- flutter res`
  e troque pelas novas.
- Instalador do Windows (MSI) e textos de loja usam o nome, já trocado na etapa 1.

## 4. Aplicar no site

O template do site fica em `site/index.html`, com as variáveis no bloco `:root` no topo do `<style>`.
Copie os valores de `brand/tokens.css` para lá (mesmos nomes `--cx-*`). O site é finalizado na etapa 5.

## 5. Guia de uso

Acrescente ao `brand/BRAND.md` uma seção "Como usar" curta: qual cor para fundo, para botões,
para links, para status; tamanho mínimo do logo; o que não fazer (ex.: não usar a cor principal
como alerta, não distorcer o logo).

## 6. Salvar

`git add -A && git commit -m "design system: tokens aplicados no app e no site"` e siga para
`acesso-remoto-3-servidor` (ou para a 4, se o servidor já estiver no ar).
