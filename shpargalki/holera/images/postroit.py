#!/usr/bin/env python3
"""Схема к материалу «Холера».

    python3 postroit.py

Порядок действий воспроизводит письма № 1-14/771, № 1-14/600
и № 1-14/2454 и приказ № 2710 от 10.11.2023.
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
    ax.text(x + w / 2, y + h / 2, tekst, ha="center", va="center",
            fontsize=razmer, color=tsvet,
            fontweight="bold" if zhirnyy else "normal",
            zorder=3, linespacing=1.45)


def strelka(ax, xy_ot, xy_do, tsvet=SERYY, tolshchina=1.1):
    ax.add_patch(FancyArrowPatch(
        xy_ot, xy_do, arrowstyle="-|>", mutation_scale=11,
        linewidth=tolshchina, color=tsvet, zorder=1, shrinkA=1, shrinkB=1))


def shema(imya="podozrenie_na_holeru.png"):
    fig, ax = plt.subplots(figsize=(8.3, 4.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.97, "Действия при подозрении на холеру",
            ha="center", va="center", fontsize=9.6, fontweight="bold",
            color=TEMNYY)

    ramka(ax, 0.020, 0.795, 0.460, 0.110,
          "ЕГДЦ при оформлении вызова: у пациента\nс рвотой и диареей уточняется выезд за рубеж,\n"
          "сведения вносятся в приложение к вызову",
          fon=FON_SIN, kant="#9bbdd8", razmer=8.2)
    ramka(ax, 0.520, 0.795, 0.460, 0.110,
          "Бригада на месте: эпидемиологический анамнез —\n"
          "выезды за пределы страны и по России\n"
          "в пределах 5 суток (инкубация)",
          fon=FON_SIN, kant="#9bbdd8", razmer=8.2)

    strelka(ax, (0.500, 0.790), (0.500, 0.720), tolshchina=1.0)
    ramka(ax, 0.020, 0.565, 0.960, 0.150,
          "Клиническое сочетание: профузная водянистая диарея («рисовый отвар»)\n"
          "и рвота без тошноты, быстрая дегидратация, нормальная температура\n"
          "+ выезд в неблагополучный регион в пределах инкубационного периода",
          fon=FON_OR, kant="#d8b283", razmer=8.4, tsvet="#ca6f1e",
          zhirnyy=True)

    strelka(ax, (0.500, 0.560), (0.500, 0.490), tolshchina=1.0)
    ramka(ax, 0.020, 0.335, 0.960, 0.150,
          "ПОДОЗРЕНИЕ НА ХОЛЕРУ — режим приказа № 2710 от 10.11.2023:\n"
          "работа в СИЗ, изоляция пациента, дезинфекция,\n"
          "уведомление старшего врача смены",
          fon=FON_KR, kant="#c8a09b", razmer=8.4, tsvet=KRASNYY,
          zhirnyy=True)

    strelka(ax, (0.260, 0.330), (0.260, 0.265), tolshchina=1.0)
    strelka(ax, (0.740, 0.330), (0.740, 0.265), tolshchina=1.0)
    ramka(ax, 0.020, 0.040, 0.470, 0.220,
          "Помощь по состоянию (Алгоритмы, ОКИ/дегидратация):\n"
          "• оральная регидратация при сохранном питье;\n"
          "• инфузия кристаллоидов при выраженной\n"
          "  дегидратации и шоке",
          fon=FON_ZEL, kant="#a3c9a8", razmer=8.2, tsvet=ZELENYY)
    ramka(ax, 0.510, 0.040, 0.470, 0.220,
          "Маршрутизация:\n"
          "госпитализация в стационар\n"
          "инфекционного профиля;\n"
          "карантинная инфекция — режим\n"
          "до лабораторного ответа",
          fon=FON, kant="#aab7bd", razmer=8.2)

    fig.savefig(imya)
    plt.close(fig)
    print(imya)


if __name__ == "__main__":
    shema()
