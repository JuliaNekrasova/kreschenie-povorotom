#!/usr/bin/env python3
"""Сборка сайта и PDF для проекта «Крещение поворотом».

    python3 _tools/sobrat.py            # сайт в docs/ и PDF для печати
    python3 _tools/sobrat.py --pdf      # только PDF
    python3 _tools/sobrat.py --web      # только сайт

Веб-версия и PDF собираются из одного и того же markdown: расхождение между
тем, что человек читает с телефона, и тем, что он распечатал на подстанции,
недопустимо. Разница только в CSS.

Нужны pandoc и weasyprint.
"""

from __future__ import annotations

import html
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

KOREN = Path(__file__).resolve().parent.parent
SAYT = KOREN / "docs"

PROEKT = "Крещение поворотом"
ADRES_ISSUES = "https://github.com/JuliaNekrasova/kreschenie-povorotom/issues"


@dataclass
class Material:
    papka: str  # папка внутри razbory/
    zagolovok: str
    podzagolovok: str
    versiya: str
    data: str

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
    def imya_pdf(self) -> str:
        return f"{self.papka}.pdf"


MATERIALY: list[Material] = [
    Material(
        papka="bol_v_grudi_posle_invazivnoy_kardiologii",
        zagolovok="Боль в груди после инвазивного вмешательства на сердце",
        podzagolovok=(
            "Катетерная аблация, ЧКВ, имплантация устройств: маршруты доступа, "
            "осложнения по срокам, распознавание на догоспитальном этапе"
        ),
        versiya="1.0",
        data="15.08.2026",
    ),
]


STRANITSA = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{opisanie}">
<link rel="stylesheet" href="{koren}assets/site.css">
</head>
<body>
<header class="verh">
  <a class="nazad" href="{koren}">{proekt}</a>
</header>
<main class="{klass}">
{telo}
</main>
<footer class="niz">
{podval}
</footer>
</body>
</html>
"""


def v_html(istochnik: Path) -> str:
    return subprocess.run(
        ["pandoc", istochnik.name, "-t", "html5"],
        cwd=istochnik.parent,
        check=True,
        capture_output=True,
        text=True,
    ).stdout


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
    cel = material.papka_sayta / material.imya_pdf
    try:
        subprocess.run(
            ["weasyprint", "-s", material.stil_pechati.name, vremennyy.name, str(cel)],
            cwd=papka,
            check=True,
            capture_output=True,
            text=True,
        )
    finally:
        vremennyy.unlink(missing_ok=True)
    return cel


def stranits(pdf: Path) -> str:
    vyvod = subprocess.run(
        ["pdfinfo", str(pdf)], check=True, capture_output=True, text=True
    ).stdout
    for stroka in vyvod.split("\n"):
        if stroka.startswith("Pages:"):
            return stroka.split(":", 1)[1].strip()
    return "?"


def sobrat_stranitsu(material: Material) -> None:
    material.papka_sayta.mkdir(parents=True, exist_ok=True)

    kartinki = material.istochnik.parent / "images"
    if kartinki.is_dir():
        cel = material.papka_sayta / "images"
        if cel.exists():
            shutil.rmtree(cel)
        shutil.copytree(kartinki, cel)

    podval = (
        f'<p>Версия {material.versiya} от {material.data}. '
        f'<a href="{material.imya_pdf}">Скачать PDF для печати</a>.</p>'
        f'<p>Текст и оригинальные схемы — лицензия '
        f'<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ru">CC BY-NC-SA 4.0</a>. '
        f'Материал учебный и не заменяет действующие протоколы.</p>'
        f'<p>Нашли ошибку в дозе, сроке или механизме — '
        f'<a href="{ADRES_ISSUES}/new/choose">сообщите</a>. Это важнее вежливости.</p>'
    )

    (material.papka_sayta / "index.html").write_text(
        STRANITSA.format(
            title=f"{material.zagolovok} — {PROEKT}",
            opisanie=material.podzagolovok,
            koren="../../",
            proekt=PROEKT,
            klass="material",
            telo=v_html(material.istochnik),
            podval=podval,
        ),
        encoding="utf-8",
    )


def sobrat_titul() -> None:
    stroki = []
    for material in MATERIALY:
        stroki.append(
            f'<li><a class="karta" href="razbory/{material.papka}/">'
            f"<span class=\"nazvanie\">{html.escape(material.zagolovok)}</span>"
            f"<span class=\"opisanie\">{html.escape(material.podzagolovok)}</span>"
            f'<span class="sluzhebnoe">версия {material.versiya} от {material.data}</span>'
            f"</a></li>"
        )

    telo = f"""<h1>{PROEKT}</h1>
<p class="lid">Клинические разборы догоспитальной практики: случай, теория, итог случая.</p>

<blockquote class="epigraf">
<p>«Эх, Додерляйна бы сейчас почитать!» — тоскливо думал я, намыливая руки. Увы, сделать это сейчас было невозможно.</p>
<p class="podpis">М. А. Булгаков, «Крещение поворотом»</p>
</blockquote>

<p>Читать во время вызова невозможно — значит, читать надо до него. Ветвлений и вариантов ответа здесь нет:
у реального вызова их тоже не бывает. Дойдя до места, где надо решать, остановитесь и скажите вслух, что делаете,
и только потом читайте дальше.</p>

<h2>Разборы</h2>
<ul class="spisok">
{chr(10).join(stroki)}
</ul>

<h2>Оговорка</h2>
<p>Материалы учебные. Они не заменяют действующие протоколы, клинические рекомендации и распоряжения службы.
Дозы, показания и маршрутизацию проверяйте по первоисточникам, действующим на момент чтения.
Клинические случаи — обезличенные учебные виньетки, а не выписки из медицинской документации.</p>
"""

    podval = (
        '<p>Тексты и схемы — <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ru">CC BY-NC-SA 4.0</a>, '
        'код — MIT. Проект личный, с работодателем автора не связан.</p>'
        f'<p><a href="{ADRES_ISSUES}/new/choose">Сообщить об ошибке в материале</a></p>'
    )

    SAYT.mkdir(parents=True, exist_ok=True)
    (SAYT / "index.html").write_text(
        STRANITSA.format(
            title=PROEKT,
            opisanie="Клинические разборы догоспитальной практики: случай, теория, итог случая.",
            koren="",
            proekt=PROEKT,
            klass="titul",
            telo=telo,
            podval=podval,
        ),
        encoding="utf-8",
    )
    (SAYT / ".nojekyll").write_text("", encoding="utf-8")


def main() -> None:
    argumenty = sys.argv[1:]
    delat_pdf = not argumenty or "--pdf" in argumenty
    delat_veb = not argumenty or "--web" in argumenty

    for material in MATERIALY:
        if delat_pdf:
            pdf = sobrat_pdf(material)
            print(f"PDF: {pdf.relative_to(KOREN)} — {stranits(pdf)} стр.")
        if delat_veb:
            sobrat_stranitsu(material)
            print(f"страница: {(material.papka_sayta / 'index.html').relative_to(KOREN)}")

    if delat_veb:
        sobrat_titul()
        print(f"титульная: {(SAYT / 'index.html').relative_to(KOREN)}")


if __name__ == "__main__":
    main()
