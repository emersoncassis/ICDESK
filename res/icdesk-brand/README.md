# ICDESK — identidade visual

Logo inspirado no emblema **IC TEAM**: bezel dourado com marcações, anel prateado, monograma **IC** chanfrado e "REMOTE ACCESS" no anel.

| Arquivo (svg/) | Uso |
|---|---|
| `badge_full.svg` | Ícone principal (≥128 px), `res/icon.png`, `res/scalable.svg` |
| `badge_simple.svg` | 64–96 px, `flutter/assets/icon.svg`, Android round |
| `badge_tiny.svg` | ≤48 px, tray, `res/logo.svg` |
| `mac_icon.svg` | macOS (`res/mac-icon.png`, `AppIcon.icns`) |
| `app_square_*.svg` | iOS / Android legacy / Play Store |
| `android_fg.svg` | Android adaptive foreground (fundo `#0D0D0D`) |
| `mono_*.svg` | Tray do macOS e ícone de notificação Android |
| `wordmark_*.svg` | Logo horizontal (`flutter/assets/logo*.png`, banner) |

Cores: ouro `#C9A85F` / `#EAD39A` / `#A8853F`, preto `#0D0D0D`, prata `#7D7D7D`/`#D9D9D9`.

## Regenerar

```bash
pip install cairosvg fonttools pillow   # + ImageMagick (convert)
python3 gen.py       # recria svg/ (essa pasta não é versionada: o .gitignore ignora *.svg)
python3 export.py    # grava todos os ícones no repositório
```

Fonte: Barlow Semi Condensed Bold (SIL Open Font License).
