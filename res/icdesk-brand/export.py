#!/usr/bin/env python3
"""Render the ICDESK brand SVGs into every icon slot of the app."""
import io, os, re, shutil, sys
import cairosvg
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SVG = os.path.join(HERE, "svg")
REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "../..")


def png(name, w, h=None):
    data = cairosvg.svg2png(url=os.path.join(SVG, name), output_width=w, output_height=h or w)
    return Image.open(io.BytesIO(data)).convert("RGBA")


def save(img, rel, mode=None):
    path = os.path.join(REPO, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if mode:
        img = img.convert(mode)
    img.save(path, optimize=True)
    print("  ", rel, img.size)


def pick(size):
    """Badge detail level by pixel size."""
    if size <= 48:
        return "badge_tiny.svg"
    if size <= 96:
        return "badge_simple.svg"
    return "badge_full.svg"


def ico(rel, sizes):
    """ImageMagick ICO (BMP entries <256px, PNG for 256) — safest for Windows/tray loaders."""
    import subprocess, tempfile
    tmp = tempfile.mkdtemp()
    files = []
    for s in sizes:
        f = os.path.join(tmp, f"{s}.png"); png(pick(s), s).save(f); files.append(f)
    subprocess.run(["convert", *files, os.path.join(REPO, rel)], check=True)
    print("  ", rel, sizes)


def copy_svg(name, rel):
    shutil.copy(os.path.join(SVG, name), os.path.join(REPO, rel))
    print("  ", rel)


print("res/")
save(png("badge_full.svg", 1024), "res/icon.png")
save(png("mac_icon.svg", 1024), "res/mac-icon.png")
for s, rel in ((32, "res/32x32.png"), (64, "res/64x64.png"), (128, "res/128x128.png"), (256, "res/128x128@2x.png")):
    save(png(pick(s), s), rel)
ico("res/icon.ico", [16, 24, 32, 48, 64, 128, 256])
ico("res/tray-icon.ico", [16, 24, 32])
save(png("mono_black.svg", 48), "res/mac-tray-light-x2.png", "LA")
save(png("mono_black.svg", 60), "res/mac-tray-dark-x2.png")
copy_svg("badge_full.svg", "res/scalable.svg")
copy_svg("badge_tiny.svg", "res/logo.svg")
copy_svg("wordmark_light.svg", "res/logo-header.svg")
copy_svg("wordmark_light.svg", "res/rustdesk-banner.svg")

print("flutter/assets")
copy_svg("badge_simple.svg", "flutter/assets/icon.svg")
# home-screen logo (max 300x60 logical -> render @2x height 120)
for name, rel in (("wordmark_dark.svg", "flutter/assets/logo_dark.png"),
                  ("wordmark_light.svg", "flutter/assets/logo_light.png"),
                  ("wordmark_light.svg", "flutter/assets/logo.png")):
    src = open(os.path.join(SVG, name)).read()
    w = float(re.search(r'viewBox="0 0 ([\d.]+) 300"', src).group(1))
    save(png(name, round(w * 120 / 300), 120), rel)

print("windows / macOS")
ico("flutter/windows/runner/resources/app_icon.ico", [16, 24, 32, 48, 64, 128, 256])
mac = png("mac_icon.svg", 1024)
mac.save(os.path.join(REPO, "flutter/macos/Runner/AppIcon.icns"),
         sizes=[(16, 16), (32, 32), (64, 64), (128, 128), (256, 256), (512, 512), (1024, 1024)])
print("   flutter/macos/Runner/AppIcon.icns")

print("android")
AND = "flutter/android/app/src/main/res"
for d, s in (("mdpi", 48), ("hdpi", 72), ("xhdpi", 96), ("xxhdpi", 144), ("xxxhdpi", 192)):
    sq = "app_square_simple.svg" if s < 144 else "app_square_full.svg"
    save(png(sq, s), f"{AND}/mipmap-{d}/ic_launcher.png")
    save(png("badge_simple.svg", s), f"{AND}/mipmap-{d}/ic_launcher_round.png")
    save(png("android_fg.svg", int(s * 2.25)), f"{AND}/mipmap-{d}/ic_launcher_foreground.png")
    save(png("mono_white.svg", s // 2), f"{AND}/mipmap-{d}/ic_stat_logo.png", "LA")
bgxml = os.path.join(REPO, AND, "values/ic_launcher_background.xml")
_xml = open(bgxml).read()
open(bgxml, "w").write(re.sub(r"#[0-9a-fA-F]{6}", "#0D0D0D", _xml))
print("  ", AND + "/values/ic_launcher_background.xml -> #0D0D0D")
save(png("app_square_full.svg", 256), "fastlane/metadata/android/en-US/images/icon.png")

print("iOS")
IOS = "flutter/ios/Runner/Assets.xcassets/AppIcon.appiconset"
for f in sorted(os.listdir(os.path.join(REPO, IOS))):
    m = re.match(r"Icon-App-([\d.]+)x[\d.]+@(\d)x\.png", f)
    if not m:
        continue
    s = round(float(m.group(1)) * int(m.group(2)))
    sq = "app_square_simple.svg" if s < 120 else "app_square_full.svg"
    save(png(sq, s), f"{IOS}/{f}", "RGB")  # App Store rejects alpha
