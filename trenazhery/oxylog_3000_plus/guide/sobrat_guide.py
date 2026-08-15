"""Сборка краткого гайда КОНТУР в PDF."""

import shutil
import subprocess
import tempfile
from pathlib import Path

from weasyprint import CSS, HTML


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "KONTUR_kratkiy_guide.md"
STYLES = HERE / "KONTUR_kratkiy_guide.css"
OUTPUT = HERE.parent / "KONTUR_kratkiy_guide.pdf"
SCREENSHOTS = ("workspace.png", "start_session.png", "debrief.png")


def main() -> None:
    for tool in ("pandoc", "pdftotext"):
        if shutil.which(tool) is None:
            raise SystemExit(f"Не найден {tool}")
    for shot in SCREENSHOTS:
        if not (HERE / shot).exists():
            raise SystemExit(f"Не найден скриншот интерфейса: {shot}")

    fragment = subprocess.run(
        ["pandoc", "-f", "gfm+fenced_divs", "-t", "html", str(SOURCE)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout

    with tempfile.TemporaryDirectory() as tmp:
        html = Path(tmp) / "guide.html"
        html.write_text(
            '<!doctype html><html lang="ru"><head><meta charset="utf-8"></head>'
            f"<body>{fragment}</body></html>",
            encoding="utf-8",
        )
        HTML(str(html), base_url=str(HERE)).write_pdf(
            str(OUTPUT),
            stylesheets=[CSS(str(STYLES))],
        )

    text = subprocess.run(
        ["pdftotext", str(OUTPUT), "-"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    pages = text.count("\f")
    required = (
        "Быстрый старт",
        "Стартовый экран: указать сотрудника",
        "Карта задач · 1–4",
        "Карта задач · 9–11",
        "Как читать автоматический разбор",
        "Пример автоматического разбора",
    )
    missing = [heading for heading in required if heading not in text]
    if missing:
        raise SystemExit(f"В PDF отсутствуют разделы: {', '.join(missing)}")
    if pages > 6:
        raise SystemExit(f"Гайд занял {pages} стр.; требуется не больше 6")
    print(f"{OUTPUT.name}: {pages} стр.")


if __name__ == "__main__":
    main()
