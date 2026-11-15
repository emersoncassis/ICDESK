---
name: acesso-remoto-5-site
description: Cria e publica no GitHub Pages a landing page da sua versão do acesso remoto, com a sua marca e os links de download que se atualizam sozinhos a cada build. Use quando a pessoa falar em "site", "landing page", "página de download", "GitHub Pages", ou na etapa 5 do guia acesso-remoto-0-comece-aqui.
---

# Etapa 5: site no GitHub Pages

O template fica em `site/` (cópia do site do ICDESK: https://emersoncassis.github.io/ICDESK/).
Os botões de download leem a release `nightly` do próprio repositório pela API do GitHub e
detectam o sistema do visitante. Publicado em `https://USUARIO.github.io/REPOSITORIO/`, o site
descobre sozinho de qual repositório puxar os arquivos.

Leia `brand/BRAND.md` e `brand/tokens.css` antes de começar.

## 1. Perguntas

1. Título e slogan da página (sugira a partir do BRAND.md).
2. Quais 3 a 6 recursos destacar? (sugestão: controle da tela, arquivos, chat, criptografia,
   servidor próprio, multiplataforma)
3. Para quem é e qual problema resolve? (vira a seção "O que resolve")
4. Contato: WhatsApp, e-mail ou site da empresa para o rodapé? (opcional)
5. Vai usar domínio próprio (ex.: `desk.empresa.com.br` para o site)? Use outro subdomínio
   que não o do servidor, ex.: `www` ou `acesso`.

## 2. Personalizar `site/`

- `site/index.html`: troque ICDESK e IC TEAM pelos nomes da marca, os textos de cada seção
  e as cores do bloco `:root` (valores de `brand/tokens.css`).
- Em `<script>`, ajuste `FALLBACK_REPO` para `USUARIO/REPOSITORIO` (usado fora do github.io,
  por exemplo com domínio próprio).
- Troque `site/assets/logo.svg`, `favicon.png` e `apple-touch-icon.png` pelo logo da marca
  (pode exportar do `res/icon.png`).
  O `.gitignore` do projeto ignora `*.png` e `*.svg`: adicione com `git add -f site/assets`.
- `site/seu-servidor.html` é o guia "faça a sua versão". Mantenha (ajudando outras pessoas) ou
  remova o link para ele no `index.html`.
- Mantenha no rodapé o crédito ao RustDesk e a licença AGPL-3.0, e mantenha o aviso de uso com autorização.

Abra `site/index.html` no navegador e confira no computador e no celular (largura ~390 px).

## 3. Publicar

O site vai para o ramo `gh-pages`, separado do código do app:
```bash
git add site && git commit -m "site: landing page" && git push
git worktree add --orphan -b gh-pages ../site-pages     # só na primeira vez (git ≥ 2.42)
cp -r site/. ../site-pages/ && touch ../site-pages/.nojekyll
cd ../site-pages && git add -A && git commit -m "site" && git push -u origin gh-pages && cd -
```
Nas próximas vezes: copie `site/` de novo para `../site-pages`, commit e push.

Depois, no GitHub: **Settings > Pages > Build and deployment > Source: Deploy from a branch**,
branch `gh-pages`, pasta `/ (root)`. Em 1 ou 2 minutos o site abre em
`https://USUARIO.github.io/REPOSITORIO/`.

Domínio próprio (opcional): em Settings > Pages > Custom domain, informe o subdomínio e crie no
DNS um registro **CNAME** dele apontando para `USUARIO.github.io`. Marque "Enforce HTTPS" quando liberar.

## 4. Fechar

Confira se os botões de download baixam os arquivos certos. Atualize o `README.md` com o link do
site. Pronto: marca, servidor, apps e site no ar.
