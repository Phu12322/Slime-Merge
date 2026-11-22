# Slime Merge

Game 2D casual vat ly voi Matter.js — keo tha, dung hop slime, mo khoa moc bong.

## Chay thu (web)

Mo file `slime-merge.html` bang trinh duyet (can mang lan dau de tai Matter.js CDN, sau do co `matter.min.js` offline).

## Ban Windows (.exe)

File build san: `dist/SlimeMerge.exe` (~18MB)
Tien trinh luu ben canh file exe: `slime_save.json` (tu dong tao).

## Build lai exe

```
pip install pyinstaller pywebview
python -m PyInstaller SlimeMerge.spec --noconfirm
```

## Cau truc

- `slime-merge.html` — game chinh (offline font Be Vietnam Pro trong `fonts/`)
- `app.py` — chay pywebview + luu tien trinh
- `matter.min.js` — du phong offline
- `fonts/` — font Viet offline
- `avatar.png`, `icon.ico` — icon game
