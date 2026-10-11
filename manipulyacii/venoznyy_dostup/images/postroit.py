#!/usr/bin/env python3
"""Схемы к материалу «Периферический венозный доступ».

    python3 postroit.py

1. etapy_vvedeniya.png — три этапа введения периферического катетера в разрезе.
2. oshibki.png — механизмы типичных неудач: сквозной прокол, смещение вены,
   катетер, оставшийся вне просвета.
3. babochka.png — введение иглы-бабочки: хват за сложенные крылья, угол,
   натяжение кожи.
4. propusknaya_sposobnost.png — пропускная способность катетеров по данным
   изготовителя (B. Braun, Vasofix Safety).
5. algoritm.png — последовательность действий при трудном венозном доступе
   на догоспитальном этапе.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.edgecolor": "#95a5a6",
    "axes.labelcolor": "#1c2833",
    "xtick.color": "#566573",
    "ytick.color": "#566573",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.dpi": 220,
    "savefig.bbox": "tight",
})

TEMNYY = "#1c2833"
SERYY = "#566573"
KOZHA = "#f5d7c4"
KOZHA_KANT = "#d9a88a"
KLETCHATKA = "#fbeee4"
VENA = "#4a6fa5"
VENA_PROSVET = "#8fb0d9"
KROV = "#a93226"
IGLA = "#7f8c8d"
KATETR = "#e59866"
ZELENYY = "#1e8449"
KRASNYY = "#a93226"
SINIY = "#2471a3"
FON = "#eef2f4"
FON_SIN = "#e4eef6"
FON_ZEL = "#e9f5ec"
FON_KR = "#f6e7e5"
FON_OR = "#f9efe3"


def strelka(ax, xy_ot, xy_do, tsvet=SERYY, tolshchina=1.1, mut=11):
    ax.add_patch(FancyArrowPatch(xy_ot, xy_do, arrowstyle="-|>", mutation_scale=mut,
                                 linewidth=tolshchina, color=tsvet, zorder=6,
                                 shrinkA=0, shrinkB=0))


def tkani(ax, vena_y=0.32, vena_h=0.16, vena_x=(0.0, 1.0)):
    """Кожа, подкожная клетчатка и вена в продольном разрезе."""
    ax.add_patch(Rectangle((0, 0), 1, 0.78, facecolor=KLETCHATKA, edgecolor="none", zorder=0))
    ax.add_patch(Rectangle((0, 0.70), 1, 0.08, facecolor=KOZHA, edgecolor=KOZHA_KANT,
                           linewidth=0.8, zorder=1))
    ax.add_patch(Rectangle((vena_x[0], vena_y), vena_x[1] - vena_x[0], vena_h,
                           facecolor=VENA_PROSVET, edgecolor=VENA, linewidth=2.2, zorder=1))
    ax.text(0.015, 0.735, "кожа", fontsize=7, color=SERYY, va="center", zorder=7)
    ax.text(0.015, vena_y + vena_h / 2, "вена", fontsize=7, color="white",
            fontweight="bold", va="center", zorder=7)


def igla_s_katetrom(ax, x_konchik, y_konchik, ugol_grad, dlina=0.62, otstup_katetra=0.045,
                    katetr_sdvinut=0.0):
    import math
    a = math.radians(ugol_grad)
    dx, dy = math.cos(a), math.sin(a)
    # игла: от кончика назад-вверх
    x0, y0 = x_konchik + dx * dlina, y_konchik + dy * dlina
    ax.plot([x_konchik, x0], [y_konchik, y0], color=IGLA, linewidth=1.6, zorder=4,
            solid_capstyle="butt")
    # срез иглы
    ax.add_patch(Polygon([(x_konchik, y_konchik),
                          (x_konchik + dx * 0.03 - dy * 0.008, y_konchik + dy * 0.03 + dx * 0.008),
                          (x_konchik + dx * 0.03, y_konchik + dy * 0.03)],
                         closed=True, facecolor=IGLA, edgecolor=IGLA, zorder=4))
    # катетер: начинается на otstup от кончика иглы, может быть сдвинут вперёд
    s0 = otstup_katetra - katetr_sdvinut
    kx0, ky0 = x_konchik + dx * s0, y_konchik + dy * s0
    kx1, ky1 = x_konchik + dx * (dlina * 0.8), y_konchik + dy * (dlina * 0.8)
    ax.plot([kx0, kx1], [ky0, ky1], color=KATETR, linewidth=5.0, alpha=0.85, zorder=3,
            solid_capstyle="round")
    return (x0, y0), (kx0, ky0)


def shema_etapy(imya="etapy_vvedeniya.png"):
    fig, osi = plt.subplots(1, 3, figsize=(10.2, 3.4))
    zag = ["1. Вход в вену под углом 15–30°,\nсрез иглы вверх",
           "2. Обратный ток крови: угол 5–10°,\nпродвинуть систему ещё на 1–2 мм",
           "3. Игла неподвижна,\nкатетер сдвигается с иглы в вену"]
    for n, ax in enumerate(osi):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.05)
        ax.set_aspect("auto")
        ax.axis("off")
        tkani(ax)
        ax.set_title(zag[n], fontsize=8.6, color=TEMNYY, loc="left")
    # этап 1: кончик иглы только вошёл в просвет, катетер ещё снаружи
    igla_s_katetrom(osi[0], 0.30, 0.44, 22)
    osi[0].add_patch(Rectangle((0.83, 0.86), 0.06, 0.07, facecolor=KROV, edgecolor=TEMNYY,
                               linewidth=0.6, zorder=6))
    osi[0].text(0.80, 0.895, "кровь в\nкамере", fontsize=7, ha="right", va="center", color=KROV)
    osi[0].annotate("кончик катетера\nещё вне вены", xy=(0.345, 0.465), xytext=(0.48, 0.12),
                    fontsize=7, color=TEMNYY, ha="left",
                    arrowprops=dict(arrowstyle="-", color=SERYY, lw=0.8))
    # этап 2: угол уменьшен, система продвинута — катетер в просвете
    igla_s_katetrom(osi[1], 0.24, 0.40, 8)
    strelka(osi[1], (0.72, 0.60), (0.56, 0.575), tsvet=ZELENYY, tolshchina=1.4)
    osi[1].text(0.74, 0.62, "на 1–2 мм", fontsize=7.4, color=ZELENYY, ha="left")
    osi[1].annotate("катетер\nв просвете", xy=(0.30, 0.41), xytext=(0.36, 0.08),
                    fontsize=7, color=TEMNYY, ha="left",
                    arrowprops=dict(arrowstyle="-", color=SERYY, lw=0.8))
    # этап 3: игла на месте, катетер сдвинут вперёд
    igla_s_katetrom(osi[2], 0.24, 0.40, 8, katetr_sdvinut=0.22)
    strelka(osi[2], (0.62, 0.36), (0.30, 0.36), tsvet=ZELENYY, tolshchina=1.4)
    osi[2].text(0.47, 0.235, "катетер вперёд", fontsize=7.4, color=ZELENYY, ha="center")
    osi[2].text(0.86, 0.95, "игла\nне двигается", fontsize=7, color=KRASNYY, ha="right", va="top")
    fig.tight_layout()
    fig.savefig(imya)
    plt.close(fig)
    print(imya)


def shema_oshibki(imya="oshibki.png"):
    fig, osi = plt.subplots(1, 3, figsize=(10.2, 3.4))
    zag = ["Сквозной прокол: крутой угол,\nигла вышла через заднюю стенку",
           "Ускользающая вена: без натяжения\nкожи вена смещается от иглы",
           "Продвижение катетера сразу после\nпоявления крови: катетер вне вены"]
    for n, ax in enumerate(osi):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.05)
        ax.axis("off")
        ax.set_title(zag[n], fontsize=8.6, color=TEMNYY, loc="left")
    # 1. сквозной прокол
    tkani(osi[0])
    igla_s_katetrom(osi[0], 0.30, 0.25, 40, dlina=0.75)
    osi[0].add_patch(plt.Circle((0.31, 0.27), 0.06, color=KROV, alpha=0.45, zorder=2))
    osi[0].text(0.40, 0.12, "кровь уходит в ткани —\nгематома («вена лопнула»)",
                fontsize=7, color=KRASNYY)
    # 2. смещение вены: поперечный разрез
    ax = osi[1]
    ax.add_patch(Rectangle((0, 0), 1, 0.78, facecolor=KLETCHATKA, edgecolor="none"))
    ax.add_patch(Rectangle((0, 0.70), 1, 0.08, facecolor=KOZHA, edgecolor=KOZHA_KANT,
                           linewidth=0.8))
    ax.add_patch(plt.Circle((0.50, 0.44), 0.10, facecolor=VENA_PROSVET, edgecolor=VENA,
                            linewidth=2.0, linestyle="--", alpha=0.6))
    ax.add_patch(plt.Circle((0.70, 0.44), 0.10, facecolor=VENA_PROSVET, edgecolor=VENA,
                            linewidth=2.2))
    ax.plot([0.50, 0.50], [0.95, 0.45], color=IGLA, linewidth=1.8)
    strelka(ax, (0.58, 0.44), (0.62, 0.44), tsvet=KRASNYY, tolshchina=1.2)
    ax.text(0.50, 0.20, "поперечный разрез:\nвена «уходит» в сторону", fontsize=7,
            color=TEMNYY, ha="center")
    # 3. катетер не в вене
    tkani(osi[2])
    igla_s_katetrom(osi[2], 0.30, 0.44, 24, otstup_katetra=0.075)
    osi[2].annotate("в вене только кончик иглы;\nкатетер упирается в стенку\nи заворачивается",
                    xy=(0.37, 0.475), xytext=(0.45, 0.07), fontsize=7, color=KRASNYY,
                    arrowprops=dict(arrowstyle="-", color=SERYY, lw=0.8))
    fig.tight_layout()
    fig.savefig(imya)
    plt.close(fig)
    print(imya)


def shema_babochka(imya="babochka.png"):
    fig, ax = plt.subplots(figsize=(8.0, 3.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    # предплечье/кисть в разрезе
    ax.add_patch(Rectangle((0, 0), 1, 0.50, facecolor=KLETCHATKA, edgecolor="none"))
    ax.add_patch(Rectangle((0, 0.44), 1, 0.06, facecolor=KOZHA, edgecolor=KOZHA_KANT, lw=0.8))
    ax.add_patch(Rectangle((0.0, 0.345), 1.0, 0.07, facecolor=VENA_PROSVET, edgecolor=VENA, lw=2))
    # игла под углом 10–15°
    import math
    # по оси x единица в 8/3,6 раза длиннее, чем по оси y: 27° в данных ≈ 13° на рисунке
    a = math.radians(27)
    xk, yk = 0.36, 0.38
    x1, y1 = xk + math.cos(a) * 0.33, yk + math.sin(a) * 0.33
    ax.plot([xk, x1], [yk, y1], color=IGLA, lw=1.8, zorder=4)
    # крылья, сложенные вверх
    ax.add_patch(Polygon([(x1, y1), (x1 + 0.025, y1 + 0.28), (x1 + 0.075, y1 + 0.28),
                          (x1 + 0.06, y1)], closed=True, facecolor="#48c9b0",
                         edgecolor="#138d75", lw=1.0, zorder=5))
    ax.plot([x1 + 0.06, 0.78], [y1, y1 + 0.30], color="#bdc3c7", lw=3.5, zorder=3)
    ax.text(0.79, y1 + 0.31, "трубка", fontsize=7.4, color=SERYY, ha="left", va="center")
    # пальцы, держащие крылья
    ax.add_patch(plt.Circle((x1 + 0.005, y1 + 0.22), 0.035, facecolor="#f0c8a8",
                            edgecolor=KOZHA_KANT, zorder=6))
    ax.add_patch(plt.Circle((x1 + 0.10, y1 + 0.22), 0.035, facecolor="#f0c8a8",
                            edgecolor=KOZHA_KANT, zorder=6))
    ax.text(x1 - 0.06, 0.98, "крылья сложены вверх и зажаты\nбольшим и указательным пальцами",
            fontsize=7.6, color=TEMNYY, ha="right", va="top")
    # угол
    ax.plot([xk, xk + 0.30], [yk, yk], color=SERYY, lw=0.6, ls=":")
    ax.text(xk + 0.32, yk - 0.005, "10–15°", fontsize=7.6, color=SINIY, va="center", ha="left")
    ax.text(0.03, yk - 0.12, "срез вверх; после появления крови\nв трубке — продвинуть на 2–3 мм вдоль вены",
            fontsize=7.2, color=TEMNYY, ha="left", va="top")
    # натяжение кожи: ниже места пункции, со стороны павильона, в направлении от иглы
    ax.add_patch(plt.Circle((0.87, 0.53), 0.04, facecolor="#f0c8a8", edgecolor=KOZHA_KANT,
                            zorder=6))
    strelka(ax, (0.84, 0.53), (0.98, 0.53), tsvet=ZELENYY, tolshchina=1.6, mut=13)
    ax.text(0.99, 0.28, "большой палец второй руки\nнатягивает кожу на 3–5 см ниже\nместа пункции, от иглы",
            fontsize=7.4, color=ZELENYY, ha="right", va="top")
    # направление введения иглы
    strelka(ax, (0.30, 0.56), (0.10, 0.56), tsvet=SINIY, tolshchina=1.2)
    ax.text(0.20, 0.59, "игла направлена к сердцу,\nот натягивающего пальца", fontsize=7.2,
            color=SINIY, ha="center", va="bottom")
    ax.text(0.015, 0.38, "вена", fontsize=7, color="white", fontweight="bold", va="center")
    fig.savefig(imya)
    plt.close(fig)
    print(imya)


def shema_propusk(imya="propusknaya_sposobnost.png"):
    # B. Braun Vasofix Safety: калибр, цвет, диаметр × длина, поток (мл/мин)
    dannye = [
        ("24G", "#f4d03f", "0,7 × 19", 22),
        ("22G", "#3498db", "0,9 × 25", 36),
        ("20G", "#f1948a", "1,1 × 33", 61),
        ("18G", "#27ae60", "1,3 × 45", 96),
        ("17G", "#f2f3f4", "1,5 × 45", 128),
        ("16G", "#95a5a6", "1,7 × 50", 196),
        ("14G", "#e67e22", "2,2 × 50", 343),
    ]
    fig, ax = plt.subplots(figsize=(8.0, 3.4))
    for i, (g, cvet, razm, potok) in enumerate(dannye):
        ax.barh(i, potok, color=cvet, edgecolor=TEMNYY, linewidth=0.6, height=0.68)
        ax.text(potok + 5, i, f"{potok} мл/мин", va="center", fontsize=7.8, color=TEMNYY,
                bbox=dict(facecolor="white", edgecolor="none", pad=1.0), zorder=5)
        ax.text(-8, i, f"{g}  ({razm} мм)", va="center", ha="right", fontsize=7.8,
                color=TEMNYY)
    ax.set_yticks([])
    ax.set_xlim(0, 400)
    ax.set_xlabel("пропускная способность, мл/мин")
    ax.axvline(1000 / 10, color=KRASNYY, lw=1.0, ls="--", zorder=1)
    ax.text(103, 6.45, "1000 мл за 10 мин", fontsize=7.2, color=KRASNYY, va="center")
    for storona in ("top", "right", "left"):
        ax.spines[storona].set_visible(False)
    fig.tight_layout()
    fig.savefig(imya)
    plt.close(fig)
    print(imya)


def ramka(ax, x, y, w, h, tekst, fon=FON, kant="#aab7bd", razmer=8.2, zhirnyy=False,
          tsvet=TEMNYY):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.012",
                                linewidth=0.9, edgecolor=kant, facecolor=fon, zorder=2))
    t = ax.text(x + w / 2, y + h / 2, tekst, ha="center", va="center", fontsize=razmer,
                color=tsvet, fontweight="bold" if zhirnyy else "normal", zorder=3,
                linespacing=1.4)
    r = ax.figure.canvas.get_renderer()
    (x0, y0), (x1, y1) = ax.transData.transform([(0, 0), (w, h)])
    while t.get_fontsize() > 6.0:
        e = t.get_window_extent(r)
        if e.width <= (x1 - x0) * 0.92 and e.height <= (y1 - y0) * 0.86:
            break
        t.set_fontsize(t.get_fontsize() - 0.2)


def shema_algoritm(imya="algoritm.png"):
    fig, ax = plt.subplots(figsize=(8.3, 6.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ramka(ax, 0.10, 0.88, 0.80, 0.09,
          "Оценка: вена не видна без жгута и не пальпируется со жгутом —\nвысокая вероятность неудачи первой попытки",
          fon=FON_SIN, kant="#9bbdd8", tsvet=SINIY, zhirnyy=True)
    strelka(ax, (0.5, 0.875), (0.5, 0.835))
    ramka(ax, 0.10, 0.68, 0.80, 0.15,
          "Подготовка до прокола: освещение (фонарь); рука ниже уровня сердца;\n"
          "согревание кисти и предплечья 5–15 мин; жгут или манжета тонометра\n"
          "(40–60 мм рт. ст.); выбор места на предплечье и тыле кисти;\n"
          "устойчивая поза, опора кисти на руку пациента",
          fon=FON, kant="#aab7bd")
    strelka(ax, (0.5, 0.675), (0.5, 0.635))
    ramka(ax, 0.10, 0.53, 0.80, 0.10,
          "Попытка 1 и попытка 2 одного исполнителя;\nкаждая новая попытка — новым катетером и проксимальнее предыдущей",
          fon=FON_ZEL, kant="#a3c9a8", tsvet=ZELENYY, zhirnyy=True)
    strelka(ax, (0.5, 0.525), (0.5, 0.485))
    ramka(ax, 0.10, 0.38, 0.80, 0.10,
          "Неудача после двух попыток → передать попытку более опытному\nчлену бригады (не более 4 попыток суммарно)",
          fon=FON_OR, kant="#d8b283", tsvet="#ca6f1e", zhirnyy=True)
    strelka(ax, (0.30, 0.375), (0.30, 0.300))
    strelka(ax, (0.70, 0.375), (0.70, 0.300))
    ramka(ax, 0.02, 0.10, 0.46, 0.19,
          "Состояние позволяет отложить введение:\nвнутримышечный, интраназальный,\nсублингвальный путь, если он\nпредусмотрен для препарата;\nвенозный доступ — в стационаре",
          fon=FON, kant="#aab7bd")
    ramka(ax, 0.52, 0.10, 0.46, 0.19,
          "Требуется немедленное\nвнутривенное введение (шок, остановка\nкровообращения, судороги):\nвнутрикостный доступ\n(«Катетеризация вены или\nвнутрикостный доступ» в Алгоритмах)",
          fon=FON_KR, kant="#c8a09b", tsvet=KRASNYY, zhirnyy=True)
    ax.text(0.5, 0.035, "Вены нижней конечности у взрослых — вынужденная мера: выше риск тромбофлебита и тромбоза",
            ha="center", fontsize=7.6, color=SERYY, style="italic")
    fig.savefig(imya)
    plt.close(fig)
    print(imya)


if __name__ == "__main__":
    shema_etapy()
    shema_oshibki()
    shema_babochka()
    shema_propusk()
    shema_algoritm()
