"""Сборка краткого гайда ТИТР в PDF."""

import shutil
import subprocess
import tempfile
from pathlib import Path

from weasyprint import CSS, HTML


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "TITR_kratkiy_guide.md"
STYLES = HERE / "TITR_kratkiy_guide.css"
OUTPUT = HERE.parent / "TITR_kratkiy_guide.pdf"
SCREENSHOTS = (
    HERE / "start_session_approved.png",
    HERE / "workspace_approved.png",
    HERE / "debrief.png",
)


def main() -> None:
    for tool in ("pandoc", "pdftotext"):
        if shutil.which(tool) is None:
            raise SystemExit(f"Не найден {tool}")
    missing_shots = [path.name for path in SCREENSHOTS if not path.exists()]
    if missing_shots:
        raise SystemExit(
            "Не найдены скриншоты: "
            + ", ".join(missing_shots)
            + ". Запустите guide/capture_guide_screenshots.py"
        )

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
        "Карта задач · 1–4",
        "Карта задач · 5–8",
        "Карта задач · 9–10",
        "Как читать проверку и разбор",
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
