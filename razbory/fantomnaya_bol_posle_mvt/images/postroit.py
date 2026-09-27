#!/usr/bin/env python3
"""Схемы к разбору «Фантом, который возвращает подрыв».

    python3 postroit.py

Схемы обобщают источники, перечисленные в материале. Величины эффектов
приведены по опубликованным исследованиям и указаны в подписях к рисункам.
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
FON_ZEL = "#e8f3ec"

SHIRINA = 8.3


def ramka(ax, x, y, w, h, tekst, fon=FON, kant="#aab7bd", razmer=8.2,
          zhirnyy=False, tsvet=TEMNYY, sleva=False):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.005,rounding_size=0.01",
        linewidth=0.9, edgecolor=kant, facecolor=fon, zorder=2))
    tx, ha = (x + 0.012, "left") if sleva else (x + w / 2, "center")
    ax.text(tx, y + h / 2, tekst, ha=ha, va="center", fontsize=razmer,
            color=tsvet, fontweight="bold" if zhirnyy else "normal",
            zorder=3, linespacing=1.45)


def strelka(ax, ot, do, tsvet=SERYY, tolshchina=1.0):
    ax.add_patch(FancyArrowPatch(ot, do, arrowstyle="-|>", mutation_scale=10,
                                 linewidth=tolshchina, color=tsvet, zorder=1,
                                 shrinkA=1, shrinkB=1))


# --------------------------------------------------------------------------
# Схема 1. Три уровня формирования фантомной боли
# --------------------------------------------------------------------------
def shema_urovni(imya="urovni_boli.png"):
    fig, ax = plt.subplots(figsize=(SHIRINA, 4.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    urovni = [
        (0.048, "Периферический", FON_KR, "#c8a09b", KRASNYY,
         "Невромы: эктопическая\nспонтанная активность,\nмеханическая\nчувствительность",
         "Точечная болезненность\nс прострелом в фантом,\nзависимость от протеза,\nответ на местный анестетик",
         "Местные анестетики,\nпродлённая перинейральная\nблокада,\nхирургия нерва"),
        (0.365, "Спинальный", FON_OR, "#d8b283", ORANZH,
         "Центральная\nсенситизация задних\nрогов: расширение\nрецептивных полей",
         "Аллодиния\nи гипералгезия культи,\nсуммация боли\nпри повторной стимуляции",
         "Антиконвульсанты,\nNMDA-антагонисты,\nантидепрессанты"),
        (0.682, "Кортикальный", FON_SIN, "#9bbdd8", SINIY,
         "Реорганизация\nсоматосенсорной\nи моторной коры;\nболевые следы",
         "Телескопирование,\nискажение схемы тела,\nвоспроизведение\nпрошлой боли",
         "Зеркальная терапия,\nградуированное\nдвигательное\nпредставление"),
    ]
    w = 0.296
    for x, nazvanie, fon, kant, tsvet, mehanizm, priznaki, vozdeystvie in urovni:
        ramka(ax, x, 0.880, w, 0.072, nazvanie, fon=fon, kant=kant,
              razmer=10.0, zhirnyy=True, tsvet=tsvet)
        ramka(ax, x, 0.640, w, 0.220, mehanizm, fon="white", kant=kant, razmer=7.7)
        ramka(ax, x, 0.380, w, 0.240, priznaki, fon="white", kant=kant, razmer=7.7)
        ramka(ax, x, 0.110, w, 0.245, vozdeystvie, fon=fon, kant=kant, razmer=7.7)
        strelka(ax, (x + w / 2, 0.878), (x + w / 2, 0.864), tsvet=kant, tolshchina=0.8)
        strelka(ax, (x + w / 2, 0.638), (x + w / 2, 0.624), tsvet=kant, tolshchina=0.8)
        strelka(ax, (x + w / 2, 0.378), (x + w / 2, 0.358), tsvet=kant, tolshchina=0.8)

    ax.text(0.022, 0.755, "механизм", rotation=90, ha="center", va="center",
            fontsize=7.4, color=SERYY, style="italic")
    ax.text(0.022, 0.500, "признаки", rotation=90, ha="center", va="center",
            fontsize=7.4, color=SERYY, style="italic")
    ax.text(0.022, 0.232, "воздействие", rotation=90, ha="center", va="center",
            fontsize=7.4, color=SERYY, style="italic")

    ramka(ax, 0.048, 0.010, 0.930, 0.085,
          "Опиоиды действуют на всех трёх уровнях, но ни один из них не устраняют:\n"
          "снижение боли достигается подавлением передачи, а не прекращением её источника",
          fon=FON, kant="#aab7bd", razmer=8.2)

    fig.savefig(imya)
    plt.close(fig)
    print(imya)


# --------------------------------------------------------------------------
# Схема 2. Маршрут пациента и вмешательства по этапам
# --------------------------------------------------------------------------
def shema_marshrut(imya="okno_reamputacii.png"):
    fig, ax = plt.subplots(figsize=(SHIRINA, 3.9))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    etapy = [
        (0.010, "Вызов\nскорой помощи", FON_KR, "#c8a09b", KRASNYY,
         "Морфин: ответ\nу 42 % пациентов\n(Huse, 2001)",
         "Действует\nна текущий приступ.\nНи один механизм\nне устраняется"),
        (0.257, "Эвакуация\nпри отделяемом", FON_OR, "#d8b283", ORANZH,
         "Обработка раны,\nасептическая повязка,\nэвакуация\n(приказ № 535)",
         "Размыкает круг\nповторных вызовов,\nускоряет решение\nоб операции"),
        (0.504, "Реампутация", FON_ZEL, "#a3cdb4", ZELENYY,
         "Реиннервация мышц\nвместо иссечения невром:\n3,5 балла в пользу\n(Dumanian, 2019)",
         "Единственная\nвозможность обработать\nтри невромы;\nповторно не возникает"),
        (0.751, "Реабилитация", FON_SIN, "#9bbdd8", SINIY,
         "Зеркальная терапия,\nградуированное\nдвигательное\nпредставление",
         "Доступно и безопасно;\nдостоверность\nдоказательств\nочень низкая"),
    ]
    w = 0.239
    for x, nazvanie, fon, kant, tsvet, chto, znachenie in etapy:
        ramka(ax, x, 0.845, w, 0.090, nazvanie, fon=fon, kant=kant,
              razmer=9.2, zhirnyy=True, tsvet=tsvet)
        ramka(ax, x, 0.545, w, 0.275, chto, fon="white", kant=kant, razmer=7.6)
        ramka(ax, x, 0.245, w, 0.280, znachenie, fon=fon, kant=kant, razmer=7.6)

    for x in [0.257, 0.504, 0.751]:
        strelka(ax, (x - 0.009, 0.690), (x - 0.001, 0.690), tsvet=SERYY, tolshchina=1.2)

    ramka(ax, 0.010, 0.010, 0.980, 0.205,
          "Отдельно от маршрута: продлённая шестидневная перинейральная блокада — 3,0 против 4,5 балла\n"
          "через четыре недели после окончания инфузии, улучшение не менее 2 баллов у 57 % против 26 %\n"
          "(Ilfeld, 2021). Выполняется в специализированных центрах и не привязана к сроку операции",
          fon=FON, kant="#aab7bd", razmer=8.0)

    fig.savefig(imya)
    plt.close(fig)
    print(imya)


if __name__ == "__main__":
    shema_urovni()
    shema_marshrut()
