#!/usr/bin/env python3
"""Схемы к материалу «Сахарный диабет у детей».

    python3 postroit.py

Содержание схем воспроизводит информационно-методическое письмо
№ 1-14/4455 от 03.11.2022 и раздел «Общая педиатрия» приказа № 535
от 18.05.2023 (внутренние страницы 175–176). Кривые дыхания условные:
они передают соотношение глубины и частоты, а не измеренные объёмы.
"""

from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.edgecolor": "#95a5a6",
    "axes.labelcolor": "#1c2833",
    "axes.titlesize": 9.5,
    "axes.titleweight": "bold",
    "axes.titlecolor": "#1c2833",
    "xtick.color": "#566573",
    "ytick.color": "#566573",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.dpi": 220,
    "savefig.bbox": "tight",
})

TEMNYY = "#1c2833"
SERYY = "#566573"
SINIY = "#2471a3"
GOLUBOY = "#5499c7"
KRASNYY = "#a93226"
ORANZH = "#ca6f1e"
FON = "#eef2f4"
FON_KR = "#f6e7e5"
FON_OR = "#f9efe3"
FON_SIN = "#e4eef6"

SHIRINA = 8.3


def ramka(ax, x, y, w, h, tekst, fon=FON, kant="#aab7bd", razmer=8.6,
          zhirnyy=False, tsvet=TEMNYY, vyravnivanie="center"):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.012",
        linewidth=0.9, edgecolor=kant, facecolor=fon, zorder=2))
    if vyravnivanie == "center":
        tx, ha = x + w / 2, "center"
    else:
        tx, ha = x + 0.014, "left"
    ax.text(tx, y + h / 2, tekst, ha=ha, va="center", fontsize=razmer,
            color=tsvet, fontweight="bold" if zhirnyy else "normal",
            zorder=3, linespacing=1.45)


def strelka(ax, xy_ot, xy_do, tsvet=SERYY, tolshchina=1.1):
    ax.add_patch(FancyArrowPatch(
        xy_ot, xy_do, arrowstyle="-|>", mutation_scale=11,
        linewidth=tolshchina, color=tsvet, zorder=1, shrinkA=1, shrinkB=1))


# --------------------------------------------------------------------------
# Схема 1. От признака к дозе
# --------------------------------------------------------------------------
def shema_reshenie(imya="reshenie_glyukometriya.png"):
    fig, ax = plt.subplots(figsize=(SHIRINA, 5.45))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    priznaki = [
        "Сонливость",
        "Бледность\nкожных покровов",
        "Боли в животе\nи (или) рвота",
        "Ощущение\nнехватки воздуха",
        "Учащённое\nмочеиспускание",
        "Потеря аппетита\nи веса",
    ]
    w, zazor = 0.148, 0.018
    x0 = (1 - (6 * w + 5 * zazor)) / 2
    for i, t in enumerate(priznaki):
        x = x0 + i * (w + zazor)
        ramka(ax, x, 0.875, w, 0.072, t, fon=FON, razmer=7.9)
        strelka(ax, (x + w / 2, 0.873), (x + w / 2, 0.836), tolshchina=0.85)

    ax.text(0.5, 0.965, "Ребёнок любого возраста: любой из шести признаков",
            ha="center", va="center", fontsize=9.4, fontweight="bold", color=TEMNYY)

    ramka(ax, 0.185, 0.762, 0.63, 0.070,
          "ГЛЮКОМЕТРИЯ ОБЯЗАТЕЛЬНА\nписьмо № 1-14/4455 от 03.11.2022",
          fon="#dfe6ea", kant="#8fa3ab", razmer=9.2, zhirnyy=True)

    vetvi = [
        (0.020, FON_KR, "#c8a09b", KRASNYY,
         "Глюкоза < 3,9 ммоль/л",
         "Гипогликемическое\nсостояние",
         "Декстроза 10 % — 2 мл/кг\nвнутривенно капельно\nПовторная глюкометрия"),
        (0.345, FON, "#aab7bd", SERYY,
         "Глюкоза 3,9–11 ммоль/л",
         "Диабетическая причина\nне подтверждена",
         "Поиск другой причины\nсимптома; при ухудшении —\nповторная глюкометрия"),
        (0.670, FON_OR, "#d8b283", ORANZH,
         "Глюкоза > 11 ммоль/л",
         "Кетоацидоз: запах ацетона,\nдегидратация,\nдыхание Куссмауля",
         "Натрия хлорид 0,9 % —\n10–20 мл/кг капельно\nПовторная глюкометрия"),
    ]
    shir = 0.310
    for x, fon, kant, tsvet, zagolovok, sostoyanie, dejstvie in vetvi:
        strelka(ax, (0.5, 0.760), (x + shir / 2, 0.700), tsvet=tsvet, tolshchina=1.0)
        ramka(ax, x, 0.628, shir, 0.068, zagolovok, fon=fon, kant=kant,
              razmer=9.0, zhirnyy=True, tsvet=tsvet)
        ramka(ax, x, 0.510, shir, 0.098, sostoyanie, fon="white", kant=kant, razmer=8.0)
        strelka(ax, (x + shir / 2, 0.626), (x + shir / 2, 0.610), tsvet=tsvet, tolshchina=0.9)
        strelka(ax, (x + shir / 2, 0.508), (x + shir / 2, 0.470), tsvet=tsvet, tolshchina=0.9)
        ramka(ax, x, 0.340, shir, 0.128, dejstvie, fon=fon, kant=kant, razmer=8.2)

    ax.plot([0.02, 0.98], [0.285, 0.285], color="#aab7bd", linewidth=0.8)
    ax.text(0.5, 0.285, "  нарушение сознания  ", ha="center", va="center",
            fontsize=8.4, color=SERYY, style="italic",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.5), zorder=4)

    ramka(ax, 0.020, 0.130, 0.465, 0.132,
          "Гипогликемическая кома\n"
          "Санация ВДП, воздуховод, доступ,\n"
          "декстроза 10 % — 2 мл/кг капельно,\n"
          "ЭКГ, повторная глюкометрия",
          fon=FON_KR, kant="#c8a09b", razmer=8.1)
    ramka(ax, 0.515, 0.130, 0.465, 0.132,
          "Гипергликемическая кома\n"
          "Глюкометрия, пульсоксиметрия,\n"
          "натрия хлорид 0,9 % — 10–20 мл/кг капельно;\n"
          "при шоке — гиповолемический шок, стр. 160",
          fon=FON_OR, kant="#d8b283", razmer=8.1)

    ramka(ax, 0.020, 0.012, 0.960, 0.100,
          "Общее для обеих ком: кислород при SpO₂ ≤ 93 %; транспортировка на носилках;\n"
          "при уровне сознания меньше 8 баллов по шкале комы Глазго после терапии —\n"
          "раздел «Детская анестезиология и реаниматология», кома неустановленного генеза, внутр. стр. 161",
          fon=FON_SIN, kant="#9bbdd8", razmer=8.2)

    fig.savefig(imya)
    plt.close(fig)
    print(imya)


# --------------------------------------------------------------------------
# Схема 2. Стадии кетоацидоза
# --------------------------------------------------------------------------
def shema_stadii(imya="stadii_dka.png"):
    fig, ax = plt.subplots(figsize=(SHIRINA, 3.65))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.add_patch(FancyArrowPatch((0.03, 0.10), (0.985, 0.10), arrowstyle="-|>",
                                 mutation_scale=15, linewidth=1.4, color=SERYY, zorder=1))
    ax.text(0.5, 0.030, "нарастание декомпенсации", ha="center", va="center",
            fontsize=8.4, color=SERYY, style="italic")

    stadii = [
        (0.030, "#f4f7f8", "#aab7bd", SINIY, "I стадия",
         "Общая слабость,\nнарастание жажды и полиурии,\nповышение аппетита\nпри потере веса,\nзапах ацетона\nв выдыхаемом воздухе",
         "Сознание сохранено"),
        (0.353, FON_OR, "#d8b283", ORANZH, "II стадия — прекома",
         "Нарастание тех же симптомов,\nодышка, снижение аппетита,\nтошнота, рвота,\nболи в животе;\nгипергликемия,\nгиперкетонемия, кетонурия",
         "Сонливость,\nсомнолентно-сопорозное\nсостояние"),
        (0.676, FON_KR, "#c8a09b", KRASNYY, "III стадия — кома",
         "Коллапс, олигоанурия,\nдегидратация: язык «сухой\nкак тёрка», заеды;\nкуссмаулевское дыхание;\nпризнаки ДВС: холодные\nсинюшные конечности, нос, уши",
         "Сознание утрачено,\nрефлексы снижены\nили выпадают"),
    ]
    shir = 0.294
    for x, fon, kant, tsvet, nazvanie, priznaki, soznanie in stadii:
        ramka(ax, x, 0.845, shir, 0.072, nazvanie, fon=fon, kant=kant,
              razmer=9.4, zhirnyy=True, tsvet=tsvet)
        ramka(ax, x, 0.455, shir, 0.370, priznaki, fon="white", kant=kant, razmer=7.7)
        ramka(ax, x, 0.270, shir, 0.165, soznanie, fon=fon, kant=kant, razmer=7.9)
        ax.plot([x + shir / 2, x + shir / 2], [0.268, 0.135], color=kant,
                linewidth=0.9, linestyle=(0, (3, 2)), zorder=1)
        ax.plot([x + shir / 2], [0.10], marker="o", markersize=5,
                color=tsvet, zorder=3)

    fig.savefig(imya)
    plt.close(fig)
    print(imya)


# --------------------------------------------------------------------------
# Схема 3. Дыхание Куссмауля
# --------------------------------------------------------------------------
def shema_dyhanie(imya="dyhanie_kussmaulya.png"):
    fig, osi = plt.subplots(2, 1, figsize=(SHIRINA, 3.5), sharex=True)
    t = np.linspace(0, 60, 3000)

    # ребёнок школьного возраста: 20 дыханий в минуту, обычная глубина
    norma = np.sin(2 * np.pi * t / 3.0)
    # Куссмауля: глубокое, ритмичное, урежённое — 12 в минуту, амплитуда выше
    kussmaul = 2.6 * np.sin(2 * np.pi * t / 5.0)

    for ax, krivaya, tsvet, zagolovok, podpis in [
        (osi[0], norma, SINIY, "Обычное дыхание",
         "около 20 в минуту, глубина обычная"),
        (osi[1], kussmaul, KRASNYY, "Дыхание Куссмауля",
         "около 10–12 в минуту, глубина резко увеличена, ритм правильный, дыхание шумное"),
    ]:
        ax.plot(t, krivaya, color=tsvet, linewidth=1.5)
        ax.axhline(0, color="#c9d1d3", linewidth=0.8, zorder=0)
        ax.set_ylim(-3.6, 4.4)
        ax.set_yticks([])
        ax.set_title(zagolovok, loc="left", color=tsvet)
        ax.text(0.995, 0.97, podpis, transform=ax.transAxes, ha="right", va="top",
                fontsize=8.1, color=SERYY)
        for storona in ("top", "right", "left"):
            ax.spines[storona].set_visible(False)

    osi[1].set_xlim(0, 60)
    osi[1].set_xticks(range(0, 61, 10))
    osi[1].set_xlabel("секунды")

    fig.tight_layout()
    fig.savefig(imya)
    plt.close(fig)
    print(imya)


if __name__ == "__main__":
    shema_reshenie()
    shema_stadii()
    shema_dyhanie()
