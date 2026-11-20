"""Сборка литературной виньетки в автономный HTML: razbor.md -> lit_01_tsitadel.html."""
import re
import subprocess
import sys
from pathlib import Path

PAPKA = Path(__file__).resolve().parent
VYHOD = PAPKA / f'{PAPKA.name}.html'

subprocess.run(
    ['pandoc', 'razbor.md', '-f', 'markdown', '-t', 'html5', '--standalone',
     '--template', 'shablon.html', '--embed-resources', '-o', str(VYHOD)],
    cwd=PAPKA, check=True)

html = VYHOD.read_text(encoding='utf-8')
vneshnie = re.findall(r'<(?:script|link|img|iframe)[^>]+(?:src|href)="https?://[^"]+"', html)
if vneshnie:
    sys.exit(f'внешние ресурсы в файле: {vneshnie}')
print(f'{VYHOD.name}: {VYHOD.stat().st_size // 1024} КБ')
