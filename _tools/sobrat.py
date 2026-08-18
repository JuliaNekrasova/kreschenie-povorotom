#!/usr/bin/env python3
"""Сборка PDF материалов проекта «Крещение поворотом».

    python3 _tools/sobrat.py                  # собрать все материалы
    python3 _tools/sobrat.py bol_v_grudi...   # только указанные папки

Материал существует в одном виде — PDF формата A4, вёрстка которого сделана под
чтение с экрана и под печать. HTML-версия текста намеренно не собирается: она
ломает типографику, ради которой эта вёрстка и существует. PDF лежит рядом с
исходником и на GitHub открывается прямо в браузере.

Нужны pandoc и weasyprint.
"""

from __future__ import annotations

import html
import subprocess
import sys
from pathlib import Path

KOREN = Path(__file__).resolve().parent.parent
RAZBORY = KOREN / "razbory"
VINYETKI = KOREN / "vinyetki"
EKG = KOREN / "ekg"
CHEKLISTY = KOREN / "cheklisty"
SPRAVOCHNIKI = KOREN / "spravochniki"


def istochnik_materiala(papka: Path) -> Path:
    return papka / "razbor.md"


def v_html(istochnik: Path) -> str:
    # encoding обязателен: без него на Windows чтение вывода идёт в cp1251
    # и падает на первом же кириллическом символе, оставляя пустой PDF.
    return subprocess.run(
        ["pandoc", istochnik.name, "-t", "html5"],
        cwd=istochnik.parent,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout


def zagolovok_iz_md(istochnik: Path) -> str:
    for stroka in istochnik.read_text(encoding="utf-8").split("\n"):
        if 'class="maintitle"' in stroka:
            return stroka.split(">", 1)[1].rsplit("<", 1)[0].strip()
    return istochnik.parent.name


def stranits(pdf: Path) -> str:
    try:
        vyvod = subprocess.run(
            ["pdfinfo", str(pdf)],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        # poppler есть не везде; pypdf нужен только для этой строки отчёта
        try:
            import pypdf
        except ImportError:
            return "?"
        return str(len(pypdf.PdfReader(str(pdf)).pages))
    for stroka in vyvod.split("\n"):
        if stroka.startswith("Pages:"):
            return stroka.split(":", 1)[1].strip()
    return "?"


def sobrat(papka: Path) -> Path:
    istochnik = istochnik_materiala(papka)
    if not istochnik.exists():
        raise SystemExit(f"нет файла материала: {istochnik}")
    stil = papka / "print_a4.css"
    if not stil.exists():
        raise SystemExit(f"нет стиля печати: {stil}")

    vremennyy = papka / "_sborka.html"
    vremennyy.write_text(
        '<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        f"<title>{html.escape(zagolovok_iz_md(istochnik))}</title></head><body>\n"
        f"{v_html(istochnik)}\n</body></html>",
        encoding="utf-8",
    )
    cel = papka / f"{papka.name}.pdf"
    try:
        subprocess.run(
            ["weasyprint", "-s", stil.name, vremennyy.name, cel.name],
            cwd=papka,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    finally:
        vremennyy.unlink(missing_ok=True)
    return cel


def vse_papki() -> list[Path]:
    papki = []
    for koren in (RAZBORY, VINYETKI, EKG, CHEKLISTY, SPRAVOCHNIKI):
        if not koren.is_dir():
            continue
        papki.extend(
            sorted(
                p
                for p in koren.iterdir()
                if p.is_dir() and (p / "razbor.md").exists()
            )
        )
    return papki


def vybor(argumenty: list[str]) -> list[Path]:
    papki = vse_papki()
    if not argumenty:
        return papki
    otobrano = []
    for argument in argumenty:
        imya = argument.rstrip("/").split("/")[-1]
        podhodyat = [p for p in papki if p.name == imya]
        if not podhodyat:
            raise SystemExit(f"неизвестный материал: {argument}")
        otobrano.extend(podhodyat)
    return otobrano


def main() -> None:
    for papka in vybor(sys.argv[1:]):
        pdf = sobrat(papka)
        print(f"{pdf.relative_to(KOREN)} — {stranits(pdf)} стр.")


if __name__ == "__main__":
    main()
