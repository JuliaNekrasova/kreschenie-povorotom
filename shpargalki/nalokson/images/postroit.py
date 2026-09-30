#!/usr/bin/env python3
"""Схемы к материалу «Налоксон».

    python3 postroit.py

Содержание схем воспроизводит информационно-методическое письмо
№ 1-14/185 от 26.01.2026 «Об особенностях применения лекарственного
средства Налоксон при оказании скорой медицинской помощи». Временные
кривые на третьей схеме условные: они передают соотношение длительностей,
а не измеренные концентрации.
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
KRASNYY = "#a93226"
ORANZH = "#ca6f1e"
ZELENYY = "#1e8449"
FON = "#eef2f4"
FON_KR = "#f6e7e5"
FON_OR = "#f9efe3"
FON_SIN = "#e4eef6"
FON_ZEL = "#e9f5ec"

SHIRINA = 8.3


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


# --------------------------------------------------------------------------
# Схема 1. Три степени опиоидного отравления и статус налоксона
# --------------------------------------------------------------------------
def shema_stepeni(imya="stepeni_otravleniya.png"):
    fig, ax = plt.subplots(figsize=(SHIRINA, 5.1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.975, "Степени отравления опиоидами и место налоксона",
            ha="center", va="center", fontsize=9.6, fontweight="bold",
            color=TEMNYY)

    kolonki = [
        (0.020, FON_ZEL, "#a3c9a8", ZELENYY, "Лёгкая степень",
         "ШКГ 13–14 (оглушение)\n"
         "Миоз, реакция на свет\nснижена; птоз, нистагм,\nнарушение конвергенции\n"
         "Дыхание: урежение\nпри засыпании\nВитальные функции\nне нарушены",
         "НАЛОКСОН ПОКАЗАН"),
        (0.355, FON_OR, "#d8b283", ORANZH, "Средняя степень",
         "ШКГ 7–12 (сопор,\nповерхностная кома)\n"
         "Миоз до «точечных\nзрачков», реакция\nна свет снижена\nили отсутствует\n"
         "Брадипноэ; бледность\nили цианоз; реакция\nна боль снижена",
         "НАЛОКСОН\nПРОТИВОПОКАЗАН"),
        (0.690, FON_KR, "#c8a09b", KRASNYY, "Тяжёлая степень",
         "ШКГ менее 7\n(глубокая кома)\n"
         "Реакция зрачков на свет,\nкорнеальные, кашлевой\nи глоточный рефлексы\nотсутствуют; арефлексия\n"
         "Брадипноэ, единичные\nдыхательные движения\nили длительное апноэ;\nгемодинамика нарушена",
         "НАЛОКСОН\nПРОТИВОПОКАЗАН"),
    ]
    shir = 0.290
    for x, fon, kant, tsvet, nazvanie, priznaki, status in kolonki:
        ramka(ax, x, 0.855, shir, 0.068, nazvanie, fon=fon, kant=kant,
              razmer=9.4, zhirnyy=True, tsvet=tsvet)
        ramka(ax, x, 0.410, shir, 0.425, priznaki, fon="white", kant=kant,
              razmer=7.4)
        ramka(ax, x, 0.305, shir, 0.085, status, fon=fon, kant=kant,
              razmer=8.8, zhirnyy=True, tsvet=tsvet)

    strelka(ax, (0.5, 0.300), (0.5, 0.258), tolshchina=1.0)
    ramka(ax, 0.020, 0.150, 0.465, 0.108,
          "При средней и тяжёлой степени первичны\n"
          "обеспечение проходимости дыхательных путей\n"
          "и оксигенация (вентиляция), а не антидот",
          fon=FON_SIN, kant="#9bbdd8", razmer=8.2)
    ramka(ax, 0.515, 0.150, 0.465, 0.108,
          "Признаки гипоксии сами по себе —\n"
          "противопоказание: цианоз, мидриаз, сопор,\n"
          "кома, аспирация, десатурация",
          fon=FON_SIN, kant="#9bbdd8", razmer=8.2)

    ramka(ax, 0.020, 0.018, 0.960, 0.098,
          "Противопоказание при средней и тяжёлой степени объясняется тем, что резкое пробуждение\n"
          "на фоне сохраняющейся гипоксии резко повышает потребность ЦНС в кислороде и субстратах",
          fon=FON, kant="#aab7bd", razmer=8.2)

    fig.savefig(imya)
    plt.close(fig)
    print(imya)


# --------------------------------------------------------------------------
# Схема 2. Причинная цепочка: почему налоксон противопоказан при гипоксии
# --------------------------------------------------------------------------
def shema_gipoksiya(imya="protivopokazanie_gipoksiya.png"):
    fig, ax = plt.subplots(figsize=(SHIRINA, 3.9))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.965, "Механизм противопоказания при гипоксии",
            ha="center", va="center", fontsize=9.6, fontweight="bold",
            color=TEMNYY)

    ramka(ax, 0.020, 0.655, 0.290, 0.180,
          "Угнетение дыхания\nопиоидами\nсо сформировавшейся\nгипоксией",
          fon=FON_KR, kant="#c8a09b", razmer=8.0, tsvet=KRASNYY, zhirnyy=True)
    ramka(ax, 0.365, 0.655, 0.270, 0.180,
          "Введение налоксона:\nрезкое восстановление\nсознания",
          fon=FON, kant="#aab7bd", razmer=8.0)
    ramka(ax, 0.660, 0.655, 0.320, 0.180,
          "Резкий рост потребности ЦНС\nв кислороде и энергетических\nсубстратах",
          fon=FON_OR, kant="#d8b283", razmer=8.0, tsvet=ORANZH)
    strelka(ax, (0.310, 0.745), (0.365, 0.745))
    strelka(ax, (0.635, 0.745), (0.660, 0.745))

    strelka(ax, (0.820, 0.650), (0.820, 0.520), tolshchina=1.0)
    ramka(ax, 0.505, 0.320, 0.475, 0.195,
          "Декомпенсация энергетического\nобмена: отёк-набухание\nголовного мозга, отёк лёгких,\nрост вероятности летального исхода",
          fon=FON_KR, kant="#c8a09b", razmer=8.2, tsvet=KRASNYY, zhirnyy=True)

    ramka(ax, 0.020, 0.320, 0.465, 0.195,
          "Порядок действий по письму:\n"
          "сначала проходимость дыхательных путей,\n"
          "оксигенация и вентиляция; мониторинг\n"
          "сатурации, ЧСС, ЧДД и АД обязателен",
          fon=FON_ZEL, kant="#a3c9a8", razmer=8.2, tsvet=ZELENYY)

    ax.plot([0.165, 0.165], [0.653, 0.517], color=SERYY, linewidth=0.9,
            linestyle=(0, (3, 2)), zorder=1)
    ax.text(0.175, 0.580, "альтернативный путь", ha="left", va="center",
            fontsize=7.6, color=SERYY, style="italic")

    ramka(ax, 0.020, 0.020, 0.960, 0.290,
          "Практическое следствие. Препарат, названный антидотом, при глубоком опиоидном\n"
          "угнетении на догоспитальном этапе введению не подлежит: лечебным мероприятием\n"
          "остаётся вентиляция, восстанавливающая оксигенацию. Налоксон по письму относится\n"
          "к состояниям без гипоксии — лёгкой степени отравления и угнетению дыхательного\n"
          "центра без признаков кислородной недостаточности.",
          fon=FON, kant="#aab7bd", razmer=8.4)

    fig.savefig(imya)
    plt.close(fig)
    print(imya)


# --------------------------------------------------------------------------
# Схема 3. Окно ренаркотизации: длительность действия налоксона
#          против периода полувыведения опиоидов
# --------------------------------------------------------------------------
def shema_renarkotizaciya(imya="renarkotizaciya.png"):
    fig, ax = plt.subplots(figsize=(SHIRINA, 3.6))

    # Часы после введения налоксона
    ax.set_xlim(0, 48)
    ax.set_ylim(-0.5, 3.6)

    polosy = [
        (0.5, 20 / 60, 30 / 60, SINIY,
         "Налоксон в/в:\nдействие 20–30 мин"),
        (1.5, 0, 3.0, "#5499c7",
         "Налоксон в/м или п/к:\nдействие 2,5–3 ч"),
        (2.5, 0, 48, "#ca6f1e",
         "Метадон: период полувыведения\nдо 48 ч (письмо)"),
    ]
    for y, a, b, tsvet, podpis in polosy:
        ax.barh(y, b - a, left=a, height=0.55, color=tsvet, alpha=0.75,
                edgecolor="none", zorder=2)
        ax.text(b + 0.8, y, podpis, va="center", ha="left", fontsize=7.9,
                color=TEMNYY)

    ax.axvspan(0.5, 48, color="#f6e7e5", alpha=0.35, zorder=0)
    ax.annotate("", xy=(48, 0.05), xytext=(0.5, 0.05),
                arrowprops=dict(arrowstyle="<->", color=KRASNYY, lw=1.0))
    ax.text(24, -0.22, "окно ренаркотизации: угнетение дыхания может вернуться "
            "в любой точке этого интервала",
            ha="center", va="center", fontsize=7.8, color=KRASNYY)

    ax.set_yticks([])
    ax.set_xlabel("часы после введения налоксона")
    ax.set_xticks(range(0, 49, 6))
    for storona in ("top", "right", "left"):
        ax.spines[storona].set_visible(False)

    ax.text(0.995, 1.02,
            "Длительность действия налоксона короче периода полувыведения опиоида:\n"
            "угнетение дыхания возвращается — требуются наблюдение и повторное введение",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8.2,
            color=SERYY, style="italic")

    fig.tight_layout()
    fig.savefig(imya)
    plt.close(fig)
    print(imya)


if __name__ == "__main__":
    shema_stepeni()
    shema_gipoksiya()
    shema_renarkotizaciya()
