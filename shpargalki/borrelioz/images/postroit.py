#!/usr/bin/env python3
"""Схема к материалу «Иксодовый клещевой боррелиоз».

    python3 postroit.py

Доли форм болезни воспроизводят информационное письмо № 1-14/1539
от 14.05.2024. Схема условная: она передаёт последовательность этапов
и соотношение долей, а не измеренную кинетику.
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
SINIY = "#2471a3"
KRASNYY = "#a93226"
ORANZH = "#ca6f1e"
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
    ax.text(x + w / 2, y + h / 2, tekst, ha="center", va="center",
            fontsize=razmer, color=tsvet,
            fontweight="bold" if zhirnyy else "normal",
            zorder=3, linespacing=1.45)


def strelka(ax, xy_ot, xy_do, tsvet=SERYY, tolshchina=1.1):
    ax.add_patch(FancyArrowPatch(
        xy_ot, xy_do, arrowstyle="-|>", mutation_scale=11,
        linewidth=tolshchina, color=tsvet, zorder=1, shrinkA=1, shrinkB=1))


def shema_formy(imya="formy_bolezni.png"):
    fig, ax = plt.subplots(figsize=(8.3, 4.9))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.97, "От укуса клеща к клиническим формам и маршрутизации",
            ha="center", va="center", fontsize=9.6, fontweight="bold",
            color=TEMNYY)

    # верхняя цепочка: укус -> инкубация -> формы
    ramka(ax, 0.020, 0.800, 0.220, 0.115,
          "Присасывание клеща\nIxodes; инокуляция\nBorrelia burgdorferi\nсо слюной",
          fon=FON_SIN, kant="#9bbdd8", razmer=8.2)
    ramka(ax, 0.280, 0.800, 0.190, 0.115,
          "Инкубационный период\n5–30 суток",
          fon=FON, kant="#aab7bd", razmer=8.4)
    strelka(ax, (0.240, 0.857), (0.280, 0.857))
    strelka(ax, (0.470, 0.857), (0.510, 0.857))

    ramka(ax, 0.510, 0.800, 0.470, 0.115,
          "Локальная стадия: кольцевидная мигрирующая\nэритема в месте присасывания — растёт, с просветлением\nв центре, горячая, болезненная, с зудом и парестезиями",
          fon=FON_OR, kant="#d8b283", razmer=8.0, tsvet=ORANZH,
          zhirnyy=True)

    # формы с долями
    strelka(ax, (0.745, 0.795), (0.745, 0.715), tolshchina=1.0)

    formy = [
        (0.020, "Эритемная\n60,52 %", FON_OR, "#d8b283", ORANZH),
        (0.265, "Лихорадочная\nбез эритемы\n28,46 %", FON, "#aab7bd", TEMNYY),
        (0.510, "Без характерных\nсимптомов\n10,41 %", FON, "#aab7bd", TEMNYY),
        (0.755, "Неврологическая\n0,61 %", FON_KR, "#c8a09b", KRASNYY),
    ]
    for x, nazv, fon, kant, tsvet in formy:
        ramka(ax, x, 0.560, 0.225, 0.150, nazv, fon=fon, kant=kant,
              razmer=8.6, zhirnyy=True, tsvet=tsvet)

    # диссеминация
    strelka(ax, (0.245, 0.555), (0.245, 0.475), tolshchina=1.0)
    ramka(ax, 0.020, 0.335, 0.450, 0.135,
          "Диссеминация: нейроборрелиоз (менингит,\nневриты черепных нервов, синдром Баннварта),\nнарушения проводимости и ритма, миокардит,\nартриты",
          fon=FON_KR, kant="#c8a09b", razmer=8.0, tsvet=KRASNYY)

    ramka(ax, 0.510, 0.335, 0.470, 0.135,
          "Практическое следствие: у ~29 % заболевших эритемы\nнет — лихорадка после укуса клеща в анамнезе\nсама по себе показание к направлению к врачу",
          fon=FON, kant="#aab7bd", razmer=8.2)

    # маршрутизация
    ramka(ax, 0.020, 0.030, 0.640, 0.250,
          "Действия бригады по письму:\n"
          "• при t > 38 °C — парацетамол 500 мг внутрь\n"
          "  или метамизола натрий 1000 мг в/м;\n"
          "• направление к врачу поликлиники;\n"
          "• эвакуация в инфекционный стационар — только\n"
          "  при признаках серозного менингита\n"
          "  или менингоэнцефалита",
          fon=FON_ZEL, kant="#a3c9a8", razmer=8.2, tsvet=ZELENYY)

    ramka(ax, 0.690, 0.030, 0.290, 0.250,
          "Тот же клещ передаёт\nклещевой энцефалит —\nболезнь другой природы,\nсо своей профилактикой;\nобе не исключают друг друга",
          fon=FON_SIN, kant="#9bbdd8", razmer=8.0)

    fig.savefig(imya)
    plt.close(fig)
    print(imya)


if __name__ == "__main__":
    shema_formy()
