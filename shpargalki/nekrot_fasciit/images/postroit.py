#!/usr/bin/env python3
"""Схема к материалу «Некротизирующие инфекции кожи и мягких тканей».

    python3 postroit.py

Содержание воспроизводит информационное письмо № 1-14/1774
от 16.06.2025.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.dpi": 220,
    "savefig.bbox": "tight",
})

TEMNYY = "#1c2833"
SERYY = "#566573"
KRASNYY = "#a93226"
ZELENYY = "#1e8449"
FON = "#eef2f4"
FON_KR = "#f6e7e5"
FON_OR = "#f9efe3"
FON_SIN = "#e4eef6"
FON_ZEL = "#e9f5ec"


def ramka(ax, x, y, w, h, tekst, fon=FON, kant="#aab7bd", razmer=8.6,
          zhirnyy=False, tsvet=TEMNYY):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.012",
        linewidth=0.9, edgecolor=kant, facecolor=fon, zorder=2))
    t = ax.text(x + w / 2, y + h / 2, tekst, ha="center", va="center",
                fontsize=razmer, color=tsvet,
                fontweight="bold" if zhirnyy else "normal",
                zorder=3, linespacing=1.45)
    vpisat(ax, t, w, h)


def vpisat(ax, t, w, h, zapas_w=0.92, zapas_h=0.88, minimum=6.0):
    """Уменьшает кегль, пока текст не помещается в рамку w × h (доли осей)."""
    fig = ax.figure
    r = fig.canvas.get_renderer()
    (x0, y0), (x1, y1) = ax.transData.transform([(0, 0), (w, h)])
    shir, vys = (x1 - x0) * zapas_w, (y1 - y0) * zapas_h
    while t.get_fontsize() > minimum:
        e = t.get_window_extent(r)
        if e.width <= shir and e.height <= vys:
            break
        t.set_fontsize(t.get_fontsize() - 0.2)


def strelka(ax, xy_ot, xy_do, tsvet=SERYY, tolshchina=1.1):
    ax.add_patch(FancyArrowPatch(
        xy_ot, xy_do, arrowstyle="-|>", mutation_scale=11,
        linewidth=tolshchina, color=tsvet, zorder=1, shrinkA=1, shrinkB=1))


def shema(imya="podozrenie_na_fasciit.png"):
    fig, ax = plt.subplots(figsize=(8.3, 5.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.97,
            "Некротизирующая инфекция: ранняя картина скудна — подозрение до некроза",
            ha="center", va="center", fontsize=9.4, fontweight="bold",
            color=TEMNYY)

    # три колонки признаков
    ramka(ax, 0.020, 0.680, 0.300, 0.200,
          "Ранние характерные:\nболь и болезненность\nбез изменений кожи;\n"
          "потеря чувствительности\nв зоне боли",
          fon=FON_OR, kant="#d8b283", razmer=8.0, tsvet="#ca6f1e",
          zhirnyy=True)
    ramka(ax, 0.350, 0.680, 0.300, 0.200,
          "Местные:\nэритема без чётких\nграниц; отёк за её\n"
          "пределами; мацерация,\nбуллы",
          fon=FON, kant="#aab7bd", razmer=8.0)
    ramka(ax, 0.680, 0.680, 0.300, 0.200,
          "Системные:\nтахикардия, гипотония;\nтахипноэ с десатурацией;\n"
          "лихорадка; заторможенность\nили возбуждение",
          fon=FON, kant="#aab7bd", razmer=8.0)

    t = ax.text(0.5, 0.640, "+ фактор риска: сахарный диабет, иммунодефицит, цирроз печени,\n"
                "инъекционное употребление наркотиков, алкоголизм, приём стероидов, травма, возраст > 50 лет",
                ha="center", va="center", fontsize=7.8, color=SERYY,
                style="italic", linespacing=1.35)
    vpisat(ax, t, 0.96, 0.07)

    strelka(ax, (0.500, 0.610), (0.500, 0.545), tolshchina=1.0)
    ramka(ax, 0.020, 0.430, 0.960, 0.110,
          "ПОДОЗРЕНИЕ: экспресс-прокальцитонин при локальных проявлениях\n"
          "инфекции кожи и при системных признаках",
          fon=FON_SIN, kant="#9bbdd8", razmer=8.4, tsvet="#2471a3",
          zhirnyy=True)

    strelka(ax, (0.500, 0.425), (0.500, 0.360), tolshchina=1.0)
    ramka(ax, 0.020, 0.245, 0.960, 0.110,
          "ЭВАКУАЦИЯ В СТАЦИОНАР С ОТДЕЛЕНИЕМ ГНОЙНОЙ ХИРУРГИИ — ВСЕМ\n"
          "летальность 13,9–30 %; отсрочка обработки увеличивает риск",
          fon=FON_KR, kant="#c8a09b", razmer=8.4, tsvet=KRASNYY,
          zhirnyy=True)

    ramka(ax, 0.020, 0.030, 0.470, 0.180,
          "По пути:\n"
          "• t > 38 °C — метамизол натрия;\n"
          "• интоксикация — инфузия комбинированных\n"
          "  солевых растворов",
          fon=FON_ZEL, kant="#a3c9a8", razmer=8.2, tsvet=ZELENYY)
    ramka(ax, 0.510, 0.030, 0.470, 0.180,
          "Инфекционно-токсический шок:\n"
          "интенсивная терапия по разделу\n"
          "«Анестезиология и реаниматология»\n"
          "Алгоритмов",
          fon=FON, kant="#aab7bd", razmer=8.2)

    fig.savefig(imya)
    plt.close(fig)
    print(imya)


if __name__ == "__main__":
    shema()
