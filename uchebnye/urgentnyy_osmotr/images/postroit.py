#!/usr/bin/env python3
"""Схемы к материалу «Протокол ургентного осмотра».

    python3 postroit.py

Схемы построены по протоколу ургентного осмотра Станции (Трофимова И. А.,
2025–2026). Временные отметки на развёртке осмотра условны: они передают
порядок и одновременность действий, а не нормативы длительности.
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
GOLUBOY = "#5499c7"
KRASNYY = "#a93226"
ORANZH = "#ca6f1e"
ZELENYY = "#1e8449"
FON = "#eef2f4"
FON_KR = "#f6e7e5"
FON_OR = "#f9efe3"
FON_SIN = "#e4eef6"
FON_ZEL = "#e8f3ec"

SHIRINA = 8.3


def ramka(ax, x, y, w, h, tekst, fon=FON, kant="#aab7bd", razmer=8.4,
          zhirnyy=False, tsvet=TEMNYY, sleva=False):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.005,rounding_size=0.01",
        linewidth=0.9, edgecolor=kant, facecolor=fon, zorder=2))
    tx, ha = (x + 0.012, "left") if sleva else (x + w / 2, "center")
    ax.text(tx, y + h / 2, tekst, ha=ha, va="center", fontsize=razmer,
            color=tsvet, fontweight="bold" if zhirnyy else "normal",
            zorder=3, linespacing=1.4)


def strelka(ax, ot, do, tsvet=SERYY, tolshchina=1.0):
    ax.add_patch(FancyArrowPatch(ot, do, arrowstyle="-|>", mutation_scale=10,
                                 linewidth=tolshchina, color=tsvet, zorder=1,
                                 shrinkA=1, shrinkB=1))


# --------------------------------------------------------------------------
# Схема 1. Развёртка осмотра: дорожка лидера и дорожка адъютора
# --------------------------------------------------------------------------
def shema_razvertka(imya="razvertka_osmotra.png"):
    fig, ax = plt.subplots(figsize=(SHIRINA, 4.9))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    nazvaniya = [
        ("Сознание", FON_SIN, "#9bbdd8",
         "Обращение\nк пациенту,\nшкала AVPU",
         "Наблюдение\nза дыханием\nи движениями"),
        ("A", FON_KR, "#c8a09b",
         "Проходимость\nдыхательных\nпутей,\nустранение\nнарушения",
         "Воздуховод,\nсанация,\nвентиляция\nмешком"),
        ("B", FON_OR, "#d8b283",
         "Эффективность\nдыхания,\nшея,\nгрудная клетка,\nаускультация,\nперкуссия",
         "Пульсоксиметрия,\nзатем кислород\nили вентиляция\nмешком"),
        ("C", FON_ZEL, "#a3cdb4",
         "Пульс,\nсимметричность,\nбелое пятно,\nтоны сердца,\nЭКГ и анамнез",
         "Артериальное\nдавление,\nсосудистый\nдоступ"),
        ("D", FON, "#aab7bd",
         "Шкала комы\nГлазго, зрачки,\nтонус и сила,\nменингеальные\nсимптомы",
         "Глюкометрия"),
        ("E", FON, "#aab7bd",
         "Живот,\nбедренные\nартерии,\nконечности,\nкожа, спина",
         "Термометрия\nс начала этапа"),
    ]
    w, zazor, x0 = 0.142, 0.011, 0.088
    etapy = [(nz, x0 + i * (w + zazor), w, fon, kant, lid, ad)
             for i, (nz, fon, kant, lid, ad) in enumerate(nazvaniya)]

    ax.text(0.5, 0.965, "Порядок осмотра: две дорожки идут одновременно",
            ha="center", va="center", fontsize=9.6, fontweight="bold", color=TEMNYY)

    for nazvanie, x, w, fon, kant, lider, adyutor in etapy:
        ramka(ax, x, 0.845, w, 0.070, nazvanie, fon=fon, kant=kant,
              razmer=10.5, zhirnyy=True, tsvet=TEMNYY)
        ramka(ax, x, 0.480, w, 0.335, lider, fon="white", kant=kant, razmer=7.2)
        ramka(ax, x, 0.150, w, 0.300, adyutor, fon=fon, kant=kant, razmer=7.2)
        strelka(ax, (x + w / 2, 0.843), (x + w / 2, 0.820), tsvet=kant, tolshchina=0.8)

    ax.text(0.040, 0.648, "ЛИДЕР", ha="center", va="center", fontsize=9.0,
            fontweight="bold", color=SINIY, rotation=90)
    ax.text(0.040, 0.300, "АДЪЮТОР", ha="center", va="center", fontsize=9.0,
            fontweight="bold", color=ORANZH, rotation=90)

    ax.plot([0.088, 0.988], [0.075, 0.075], color=SERYY, linewidth=1.1)
    ax.add_patch(FancyArrowPatch((0.088, 0.075), (0.995, 0.075), arrowstyle="-|>",
                                 mutation_scale=12, linewidth=1.1, color=SERYY, zorder=3))
    ax.text(0.54, 0.028, "время: осмотр не прерывается, выявленное нарушение устраняется "
                        "на том же этапе, где обнаружено",
            ha="center", va="center", fontsize=8.0, color=SERYY, style="italic")

    fig.savefig(imya)
    plt.close(fig)
    print(imya)


# --------------------------------------------------------------------------
# Схема 2. Обратимые причины остановки кровообращения по этапам осмотра
# --------------------------------------------------------------------------
def shema_4g4t(imya="obratimye_prichiny.png"):
    fig, ax = plt.subplots(figsize=(SHIRINA, 4.1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.965, "Где при осмотре выявляется каждая из обратимых причин",
            ha="center", va="center", fontsize=9.6, fontweight="bold", color=TEMNYY)

    stolbcy = [
        (0.010, "A и B", FON_KR, "#c8a09b",
         ["Гипоксия:", "проходимость ВДП,", "эффективность дыхания,", "сатурация",
          "", "Напряжённый пневмоторакс:", "смещение трахеи,", "перкуссия, вены шеи"]),
        (0.257, "C", FON_ZEL, "#a3cdb4",
         ["Гиповолемия:", "пульс, белое пятно,", "давление", "",
          "Тромбоз коронарный", "и лёгочный:", "ЭКГ в 12 отведениях", "",
          "Тампонада сердца:", "тоны, вены шеи,", "гипотензия"]),
        (0.504, "D", FON_SIN, "#9bbdd8",
         ["Токсические причины:", "зрачки, запах,", "обстановка на месте", "",
          "Гипогликемия", "как причина", "нарушения сознания:", "глюкометрия"]),
        (0.751, "E и анамнез", FON_OR, "#d8b283",
         ["Гипотермия:", "термометрия,", "волна Осборна на ЭКГ", "",
          "Гипо- и гиперкалиемия:", "анамнез, ЭКГ,", "экспресс-исследование", "",
          "Источник кровопотери:", "живот, спина,", "ректальное исследование"]),
    ]
    w = 0.239
    for x, nazvanie, fon, kant, punkty in stolbcy:
        ramka(ax, x, 0.845, w, 0.065, nazvanie, fon=fon, kant=kant,
              razmer=10.0, zhirnyy=True)
        tekst = "\n".join(punkty)
        ramka(ax, x, 0.145, w, 0.680, tekst, fon="white", kant=kant, razmer=7.6, sleva=True)
        strelka(ax, (x + w / 2, 0.843), (x + w / 2, 0.828), tsvet=kant, tolshchina=0.8)

    ramka(ax, 0.010, 0.020, 0.980, 0.105,
          "Поиск ведётся по ходу осмотра, до развития остановки кровообращения: "
          "к моменту, когда причина становится\nпричиной смерти, время на её устранение уже утрачено",
          fon=FON, kant="#aab7bd", razmer=8.2)

    fig.savefig(imya)
    plt.close(fig)
    print(imya)


# --------------------------------------------------------------------------
# Схема 3. Дыхательные пути: находка — действие — повторная оценка
# --------------------------------------------------------------------------
def shema_vdp(imya="vetvlenie_vdp.png"):
    fig, ax = plt.subplots(figsize=(SHIRINA, 4.3))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ramka(ax, 0.230, 0.900, 0.540, 0.075,
          "Сознание снижено или отсутствует:\nоценка проходимости и оценка дыхания одновременно",
          fon="#dfe6ea", kant="#8fa3ab", razmer=8.8, zhirnyy=True)

    vetvi = [
        (0.008, "Проходимы", FON_ZEL, "#a3cdb4", ZELENYY,
         "Речь сохранена,\nпосторонних\nзвуков нет",
         "Переход\nк разделу B"),
        (0.256, "Храп", FON_OR, "#d8b283", ORANZH,
         "Западение\nкорня языка",
         "Выдвижение\nнижней челюсти,\nвоздуховод"),
        (0.504, "Булькающее\nдыхание", FON_OR, "#d8b283", ORANZH,
         "Жидкое содержимое\nв дыхательных\nпутях",
         "Санация верхних\nдыхательных\nпутей"),
        (0.752, "Стридор", FON_KR, "#c8a09b", KRASNYY,
         "Сужение на уровне\nгортани: отёк,\nинородное тело",
         "Решение\nо протекции\nдыхательных путей"),
    ]
    w = 0.240
    for x, nazvanie, fon, kant, tsvet, mehanizm, deystvie in vetvi:
        strelka(ax, (0.5, 0.898), (x + w / 2, 0.838), tsvet=kant, tolshchina=0.9)
        ramka(ax, x, 0.760, w, 0.075, nazvanie, fon=fon, kant=kant,
              razmer=9.4, zhirnyy=True, tsvet=tsvet)
        ramka(ax, x, 0.575, w, 0.165, mehanizm, fon="white", kant=kant, razmer=7.6)
        strelka(ax, (x + w / 2, 0.573), (x + w / 2, 0.552), tsvet=kant, tolshchina=0.9)
        ramka(ax, x, 0.400, w, 0.150, deystvie, fon=fon, kant=kant, razmer=7.7)
        if nazvanie != "Проходимы":
            strelka(ax, (x + w / 2, 0.398), (x + w / 2, 0.358), tsvet=kant, tolshchina=0.9)

    ramka(ax, 0.008, 0.235, 0.984, 0.120,
          "Повторная оценка проходимости после каждого вмешательства.\n"
          "Методы протекции применяются последовательно: воздуховод → надгортанное устройство\n"
          "или интубация трахеи → коникотомия, каждый следующий — при неэффективности предыдущего",
          fon=FON, kant="#aab7bd", razmer=7.6)

    ramka(ax, 0.008, 0.070, 0.984, 0.090,
          "Апноэ при отсутствии сознания: осмотр прекращается,\n"
          "начинается сердечно-лёгочная реанимация",
          fon=FON_KR, kant="#c8a09b", razmer=8.4, zhirnyy=True, tsvet=KRASNYY)

    fig.savefig(imya)
    plt.close(fig)
    print(imya)


if __name__ == "__main__":
    shema_razvertka()
    shema_4g4t()
    shema_vdp()
