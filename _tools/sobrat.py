#!/usr/bin/env python3
"""Сборка PDF и страниц сайта проекта «Крещение поворотом».

    python3 _tools/sobrat.py            # PDF материалов и страницы сайта
    python3 _tools/sobrat.py --pdf      # только PDF
    python3 _tools/sobrat.py --web      # только страницы сайта

Страницы сайта собираются из markdown-файлов репозитория: титульная из README.md,
оговорки из DISCLAIMER.md, журнал изменений из CHANGELOG.md. Текста, зашитого в
скрипт, нет намеренно — иначе один и тот же абзац приходится править в двух
местах, и сайт неизбежно расходится с репозиторием.

Материал существует в одном виде — PDF формата A4, вёрстка которого сделана под
чтение и печать. HTML-пересборка текста материала не делается намеренно: она
ломает типографику, ради которой эта вёрстка и существует.

Нужны pandoc и weasyprint.
"""

from __future__ import annotations

import html
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

KOREN = Path(__file__).resolve().parent.parent
SAYT = KOREN / "docs"

PROEKT = "Крещение поворотом"
ADRES_REPO = "https://github.com/JuliaNekrasova/kreschenie-povorotom"
ADRES_ISSUES = f"{ADRES_REPO}/issues"

# Разделы README, нужные в репозитории, но не нужные читателю сайта.
RAZDELY_NE_DLYA_SAYTA = ("Как собрать локально",)

# Ссылки в markdown ведут на файлы репозитория; на сайте у них другие адреса.
ZAMENY_SSYLOK = {
    'href="docs/': 'href="',
    'href="DISCLAIMER.md"': 'href="ogovorki.html"',
    'href="CHANGELOG.md"': 'href="izmeneniya.html"',
    'href="README.md"': 'href="./"',
    'href="LICENSE"': 'href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ru"',
    'href="LICENSE-CODE"': f'href="{ADRES_REPO}/blob/main/LICENSE-CODE"',
    'href="../../issues/new/choose"': f'href="{ADRES_ISSUES}/new/choose"',
    'href="../../issues"': f'href="{ADRES_ISSUES}"',
}


@dataclass
class Material:
    papka: str  # папка внутри razbory/
    zagolovok: str

    @property
    def istochnik(self) -> Path:
        return KOREN / "razbory" / self.papka / "razbor.md"

    @property
    def stil_pechati(self) -> Path:
        return KOREN / "razbory" / self.papka / "print_a4.css"

    @property
    def papka_sayta(self) -> Path:
        return SAYT / "razbory" / self.papka

    @property
    def pdf(self) -> Path:
        return self.papka_sayta / f"{self.papka}.pdf"


MATERIALY: list[Material] = [
    Material(
        papka="bol_v_grudi_posle_invazivnoy_kardiologii",
        zagolovok="Боль в груди после инвазивного вмешательства на сердце",
    ),
]


STRANITSA = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{opisanie}">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<header class="verh">
  <a class="nazad" href="./">{proekt}</a>
</header>
<main class="tekst">
{telo}
</main>
<footer class="niz">
{podval}
</footer>
</body>
</html>
"""

PODVAL = (
    '<p>Тексты и схемы — <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ru">'
    "CC BY-NC-SA 4.0</a>, код — MIT. Проект личный, с работодателем автора не связан.</p>"
    '<p><a href="ogovorki.html">Оговорки</a> · '
    '<a href="izmeneniya.html">Журнал изменений</a> · '
    f'<a href="{ADRES_ISSUES}/new/choose">Сообщить об ошибке в материале</a></p>'
)


def v_html(istochnik: Path) -> str:
    return subprocess.run(
        ["pandoc", istochnik.name, "-t", "html5"],
        cwd=istochnik.parent,
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def bez_razdelov(tekst: str, zagolovki: tuple[str, ...]) -> str:
    """Выбрасывает разделы (## ...), перечисленные в zagolovki."""
    stroki, ostavlyat = [], True
    for stroka in tekst.split("\n"):
        if stroka.startswith("## "):
            ostavlyat = stroka[3:].strip() not in zagolovki
        if ostavlyat:
            stroki.append(stroka)
    return "\n".join(stroki)


def stranitsa_iz_markdown(
    istochnik: Path,
    imya: str,
    zagolovok: str,
    opisanie: str,
    razdely_ubrat: tuple[str, ...] = (),
) -> Path:
    tekst = istochnik.read_text(encoding="utf-8")
    if razdely_ubrat:
        tekst = bez_razdelov(tekst, razdely_ubrat)

    vremennyy = istochnik.parent / "_stranitsa.md"
    vremennyy.write_text(tekst, encoding="utf-8")
    try:
        telo = v_html(vremennyy)
    finally:
        vremennyy.unlink(missing_ok=True)

    for bylo, stalo in ZAMENY_SSYLOK.items():
        telo = telo.replace(bylo, stalo)

    SAYT.mkdir(parents=True, exist_ok=True)
    cel = SAYT / imya
    cel.write_text(
        STRANITSA.format(
            title=zagolovok,
            opisanie=html.escape(opisanie, quote=True),
            proekt=PROEKT,
            telo=telo,
            podval=PODVAL,
        ),
        encoding="utf-8",
    )
    return cel


def sobrat_pdf(material: Material) -> Path:
    papka = material.istochnik.parent
    vremennyy = papka / "_sborka.html"
    vremennyy.write_text(
        '<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        f"<title>{html.escape(material.zagolovok)}</title></head><body>\n"
        f"{v_html(material.istochnik)}\n</body></html>",
        encoding="utf-8",
    )
    material.papka_sayta.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            [
                "weasyprint",
                "-s",
                material.stil_pechati.name,
                vremennyy.name,
                str(material.pdf),
            ],
            cwd=papka,
            check=True,
            capture_output=True,
            text=True,
        )
    finally:
        vremennyy.unlink(missing_ok=True)
    return material.pdf


def stranits(pdf: Path) -> str:
    vyvod = subprocess.run(
        ["pdfinfo", str(pdf)], check=True, capture_output=True, text=True
    ).stdout
    for stroka in vyvod.split("\n"):
        if stroka.startswith("Pages:"):
            return stroka.split(":", 1)[1].strip()
    return "?"


def sobrat_sayt() -> None:
    stranitsy = [
        stranitsa_iz_markdown(
            KOREN / "README.md",
            "index.html",
            PROEKT,
            "Клинические разборы реальных случаев из практики скорой медицинской помощи.",
            RAZDELY_NE_DLYA_SAYTA,
        ),
        stranitsa_iz_markdown(
            KOREN / "DISCLAIMER.md",
            "ogovorki.html",
            f"Оговорки — {PROEKT}",
            "Статус материалов, клинические случаи, изображения, ошибки.",
        ),
        stranitsa_iz_markdown(
            KOREN / "CHANGELOG.md",
            "izmeneniya.html",
            f"Журнал изменений — {PROEKT}",
            "Что и когда изменилось в материалах.",
        ),
    ]
    (SAYT / ".nojekyll").write_text("", encoding="utf-8")
    for stranitsa in stranitsy:
        print(f"страница: {stranitsa.relative_to(KOREN)}")


def main() -> None:
    argumenty = sys.argv[1:]
    delat_pdf = not argumenty or "--pdf" in argumenty
    delat_veb = not argumenty or "--web" in argumenty

    if delat_pdf:
        for material in MATERIALY:
            pdf = sobrat_pdf(material)
            print(f"PDF: {pdf.relative_to(KOREN)} — {stranits(pdf)} стр.")

    if delat_veb:
        sobrat_sayt()


if __name__ == "__main__":
    main()
