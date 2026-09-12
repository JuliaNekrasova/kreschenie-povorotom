#!/usr/bin/env python3
"""Схемы к чеклисту «Боль в грудной клетке».

    python3 postroit.py

Схемы условные. Профили интенсивности боли построены как качественные
кривые, отражающие описанный в источниках характер начала и динамики,
а не результат измерений. Анатомические ориентиры точек наложения
электродов даны приближённо и не заменяют пальпацию межреберий.
"""

from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon

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
        linewidth=tolshchina, color=tsvet, zorder=1,
        shrinkA=1, shrinkB=1))


# --------------------------------------------------------------------------
# Схема 1. Ступени осмотра при боли в грудной клетке
# --------------------------------------------------------------------------
def shema_stupeni(imya="stupeni.png"):
    fig, ax = plt.subplots(figsize=(SHIRINA, 7.55))
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.01, 1.03)
    ax.axis("off")

    ramka(ax, 0.135, 0.948, 0.73, 0.052,
          "Жалоба на боль или дискомфорт в грудной клетке",
          fon="#dfe6ea", kant="#8fa3ab", razmer=9.6, zhirnyy=True)

    # Шина параллельных действий
    ax.plot([0.108, 0.892], [0.928, 0.928], color=SERYY, linewidth=1.0, zorder=1)
    ax.plot([0.5, 0.5], [0.948, 0.928], color=SERYY, linewidth=1.0, zorder=1)
    ax.text(0.5, 0.928, "  выполняется одновременно, до подробного расспроса  ",
            ha="center", va="center", fontsize=8.2, color=SERYY, style="italic",
            zorder=4, bbox=dict(facecolor="white", edgecolor="none", pad=1.5))

    odnovremenno = [
        "Покой, положение\nпо переносимости",
        "Монитор,\nпульсоксиметрия",
        "АД\nна обеих руках",
        "ЭКГ в 12 отведениях\nв течение 10 минут",
        "Глюкометрия,\nвенозный доступ",
    ]
    w, zazor = 0.176, 0.026
    x0 = (1 - (5 * w + 4 * zazor)) / 2
    for i, t in enumerate(odnovremenno):
        x = x0 + i * (w + zazor)
        ramka(ax, x, 0.845, w, 0.062, t, fon=FON, razmer=8.2)
        strelka(ax, (x + w / 2, 0.928), (x + w / 2, 0.909), tolshchina=0.9)

    strelka(ax, (0.5, 0.843), (0.5, 0.812))
    ramka(ax, 0.115, 0.726, 0.77, 0.082,
          "Признаки нестабильности: SpO₂ ≤ 90 %, САД < 90 мм рт. ст., ЧД > 30 или < 10 в минуту,\n"
          "угнетение сознания, признаки шока или отёка лёгких,\nаритмия с нарушением гемодинамики",
          fon=FON_KR, kant="#c8a09b", razmer=8.3)

    strelka(ax, (0.35, 0.724), (0.25, 0.694), tsvet=KRASNYY)
    strelka(ax, (0.65, 0.724), (0.75, 0.694), tsvet=SINIY)
    ax.text(0.285, 0.712, "есть", ha="right", va="center", fontsize=8.2,
            color=KRASNYY, fontweight="bold")
    ax.text(0.715, 0.712, "нет", ha="left", va="center", fontsize=8.2,
            color=SINIY, fontweight="bold")

    ramka(ax, 0.025, 0.600, 0.455, 0.094,
          "Помощь по ведущему синдрому\nи эвакуация начинаются немедленно;\n"
          "расспрос и осмотр продолжаются\nв салоне и не задерживают выезд",
          fon=FON_KR, kant="#c8a09b", razmer=8.1)
    ramka(ax, 0.520, 0.600, 0.455, 0.094,
          "Последовательный сбор данных\nпо ступеням 1–5; повторная оценка\n"
          "гемодинамики и записи ЭКГ\nпри изменении состояния",
          fon=FON, razmer=8.1)

    stupeni = [
        ("Ступень 1", "Характеристика боли: условия возникновения, характер, локализация, иррадиация,\n"
                      "длительность и ритм, условия усиления и ослабления"),
        ("Ступень 2", "Анамнез: давность и динамика приступов, сходство с прежними ощущениями,\n"
                      "факторы риска, перенесённые вмешательства, принимаемые препараты"),
        ("Ступень 3", "Физикальное обследование: пульс и АД на обеих руках, аускультация сердца\n"
                      "и лёгких, вены шеи, пальпация грудной клетки, осмотр ног и кожи"),
        ("Ступень 4", "ЭКГ: сопоставление с прежними плёнками, дополнительные отведения V₇–V₉\n"
                      "и V₃R–V₄R по показаниям, повторная запись при сохраняющейся боли"),
        ("Ступень 5", "Имеющиеся документы: прежние плёнки и выписки, результаты ЭхоКГ,\n"
                      "нагрузочных проб и коронарографии, упаковки принимаемых препаратов"),
    ]
    strelka(ax, (0.75, 0.598), (0.75, 0.576))
    strelka(ax, (0.25, 0.598), (0.25, 0.576))

    y = 0.516
    for nomer, tekst in stupeni:
        ramka(ax, 0.035, y, 0.93, 0.058, "", fon="white", kant="#c3ced3")
        ax.add_patch(FancyBboxPatch(
            (0.035, y), 0.112, 0.058,
            boxstyle="round,pad=0.006,rounding_size=0.012",
            linewidth=0.9, edgecolor="#8fa3ab", facecolor="#dfe6ea", zorder=4))
        ax.text(0.091, y + 0.029, nomer, ha="center", va="center",
                fontsize=8.3, color=TEMNYY, fontweight="bold", zorder=5)
        ax.text(0.165, y + 0.029, tekst, ha="left", va="center", fontsize=8.3,
                color=TEMNYY, zorder=5, linespacing=1.5)
        y -= 0.072

    y_diff = y + 0.072 - 0.122
    ramka(ax, 0.035, y_diff, 0.93, 0.102,
          "Дифференциальный ряд: первыми исключаются шесть состояний\nс непосредственной угрозой жизни —\n"
          "острый коронарный синдром, тромбоэмболия лёгочной артерии, расслоение аорты,\n"
          "напряжённый пневмоторакс, тампонада сердца, спонтанный разрыв пищевода",
          fon=FON_KR, kant="#c8a09b", razmer=8.3)
    strelka(ax, (0.5, y + 0.072), (0.5, y_diff + 0.104))

    y_konec = y_diff - 0.082
    ramka(ax, 0.035, y_konec, 0.93, 0.052,
          "Маршрутизация по ведущему диагнозу и документирование объёма обследования",
          fon="#dfe6ea", kant="#8fa3ab", razmer=8.8, zhirnyy=True)
    strelka(ax, (0.5, y_diff), (0.5, y_konec + 0.054))

    fig.savefig(imya, dpi=220, bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------------------
# Схема 2. Профиль интенсивности боли во времени
# --------------------------------------------------------------------------
def shema_profil(imya="profil_boli.png"):
    t = np.linspace(0, 1, 400)

    perikard = np.full_like(t, 0.72)
    for nachalo, konec in ((0.28, 0.44), (0.66, 0.82)):
        perikard[(t > nachalo) & (t < konec)] = 0.26

    myshechnaya = np.full_like(t, 0.12)
    for nachalo, konec in ((0.12, 0.22), (0.38, 0.48), (0.62, 0.72), (0.84, 0.94)):
        myshechnaya[(t > nachalo) & (t < konec)] = 0.80

    profili = [
        ("Расслоение аорты",
         np.where(t < 0.03, t / 0.03 * 0.88, 0.88 - 0.06 * t),
         "максимальна с первой секунды,\nбез периода нарастания; может мигрировать",
         KRASNYY),
        ("Острый коронарный синдром",
         np.clip(0.88 * (1 - np.exp(-4.5 * t)) - 0.06 * t, 0, 0.9),
         "нарастание за минуты, затем плато\nи волнообразное течение",
         SINIY),
        ("Тромбоэмболия лёгочной артерии",
         np.where(t < 0.04, t / 0.04 * 0.62, 0.62 - 0.14 * t),
         "внезапная, умеренной интенсивности;\nведущая жалоба — одышка",
         ORANZH),
        ("Спонтанный пневмоторакс",
         np.where(t < 0.03, t / 0.03 * 0.85,
                  0.14 + 0.71 * np.exp(-3.2 * (t - 0.03))),
         "резкое начало, в течение часа стихает;\nодышка сохраняется",
         GOLUBOY),
        ("Перикардит",
         perikard,
         "часы и дни; снижение в положении\nсидя с наклоном вперёд",
         "#7d6608"),
        ("Костно-мышечная боль",
         myshechnaya,
         "возникает при определённых движениях,\nвоспроизводится при пальпации",
         SERYY),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(SHIRINA, 4.1))
    for ax, (nazvanie, y, podpis, tsvet) in zip(axes.ravel(), profili):
        y = np.clip(y, 0, 0.9)
        ax.plot(t, y, color=tsvet, linewidth=1.9)
        ax.fill_between(t, 0, y, color=tsvet, alpha=0.10)
        ax.set_title(nazvanie, pad=5)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.42)
        ax.set_xticks([])
        ax.set_yticks([])
        for storona in ("top", "right"):
            ax.spines[storona].set_visible(False)
        ax.spines["left"].set_color("#aab7bd")
        ax.spines["bottom"].set_color("#aab7bd")
        ax.text(0.02, 1.38, podpis, fontsize=7.5, color=SERYY,
                va="top", ha="left", linespacing=1.4)
        ax.set_xlabel("время", fontsize=7.4, labelpad=1)
        ax.set_ylabel("интенсивность", fontsize=7.4, labelpad=2)

    fig.tight_layout(pad=0.7)
    fig.savefig(imya, dpi=220, bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------------------
# Схема 3. Дополнительные отведения
# --------------------------------------------------------------------------
def _tors(ax, vid="pered"):
    kontur = Polygon([
        (0.16, 0.86), (0.34, 0.93), (0.66, 0.93), (0.84, 0.86),
        (0.80, 0.62), (0.78, 0.10), (0.22, 0.10), (0.20, 0.62),
    ], closed=True, facecolor="#f7f9fa", edgecolor="#aab7bd", linewidth=1.0)
    ax.add_patch(kontur)
    ax.add_patch(plt.Circle((0.5, 1.01), 0.065, facecolor="#f7f9fa",
                            edgecolor="#aab7bd", linewidth=1.0))
    for znak in (-1, 1):
        ax.plot([0.5 + znak * 0.17, 0.5 + znak * 0.30],
                [0.925, 0.86], color="#aab7bd", linewidth=1.0)
    if vid == "pered":
        ax.plot([0.5, 0.5], [0.80, 0.42], color="#d5dbdd", linewidth=9,
                solid_capstyle="round", zorder=2)
        ax.text(0.5, 0.83, "грудина", ha="center", fontsize=7.2, color=SERYY)
    else:
        ax.plot([0.5, 0.5], [0.86, 0.16], color="#d5dbdd", linewidth=7,
                solid_capstyle="round", zorder=2)
        ax.text(0.5, 0.89, "позвоночник", ha="center", fontsize=7.2, color=SERYY)


def _tochka(ax, x, y, podpis, tsvet, sdvig=(0, 0.045), razmer=8.0):
    ax.add_patch(plt.Circle((x, y), 0.022, facecolor=tsvet,
                            edgecolor="white", linewidth=0.8, zorder=5))
    ax.text(x + sdvig[0], y + sdvig[1], podpis, ha="center", va="center",
            fontsize=razmer, color=tsvet, fontweight="bold", zorder=6)


def shema_otvedeniya(imya="otvedeniya.png"):
    fig, axes = plt.subplots(1, 2, figsize=(SHIRINA, 4.3))

    ax = axes[0]
    _tors(ax, "pered")
    ax.set_title("Вид спереди: правые грудные отведения V₃R и V₄R", pad=8)
    standart = [(0.435, 0.60, "V₁", (-0.005, 0.05)), (0.565, 0.60, "V₂", (0.005, 0.05)),
                (0.615, 0.545, "V₃", (0.045, 0.012)), (0.655, 0.49, "V₄", (0.0, -0.05)),
                (0.720, 0.485, "V₅", (0.0, -0.05)), (0.780, 0.48, "V₆", (0.0, -0.05))]
    for x, y, p, sd in standart:
        _tochka(ax, x, y, p, "#8fa3ab", sdvig=sd, razmer=7.6)
    for x, y, p in [(0.395, 0.545, "V₃R"), (0.355, 0.49, "V₄R")]:
        _tochka(ax, x, y, p, KRASNYY, sdvig=(-0.055, 0.0))
    ax.annotate("V₁ и V₂ — четвёртое\nмежреберье у краёв грудины",
                xy=(0.565, 0.60), xytext=(0.775, 0.70), fontsize=7.3,
                color=SERYY, ha="center",
                arrowprops=dict(arrowstyle="-", color="#aab7bd", linewidth=0.8))
    ax.annotate("V₄ — пятое межреберье\nпо среднеключичной линии,\n"
                "V₄R и V₃R — зеркально справа",
                xy=(0.355, 0.49), xytext=(0.36, 0.24), fontsize=7.3,
                color=SERYY, ha="center",
                arrowprops=dict(arrowstyle="-", color="#aab7bd", linewidth=0.8))
    ax.text(0.5, -0.05, "правая половина тела пациента — слева на схеме",
            ha="center", fontsize=7.2, color=SERYY, style="italic")

    ax = axes[1]
    _tors(ax, "zad")
    ax.set_title("Вид сзади: задние отведения V₇–V₉", pad=8)
    ax.plot([0.22, 0.50], [0.50, 0.50], color="#c3ced3", linewidth=0.8,
            linestyle=(0, (3, 3)), zorder=1)
    for x, y, p in [(0.255, 0.50, "V₇"), (0.355, 0.50, "V₈"), (0.455, 0.50, "V₉")]:
        _tochka(ax, x, y, p, SINIY, sdvig=(0, 0.058))
    ax.annotate("уровень V₆ по горизонтали:\nV₇ — задняя подмышечная линия,\n"
                "V₈ — под углом лопатки,\nV₉ — у левого края позвоночника",
                xy=(0.29, 0.49), xytext=(0.40, 0.22), fontsize=7.3,
                color=SERYY, ha="center",
                arrowprops=dict(arrowstyle="-", color="#aab7bd", linewidth=0.8))
    ax.text(0.5, -0.05, "левая половина тела пациента — слева на схеме",
            ha="center", fontsize=7.2, color=SERYY, style="italic")

    for ax in axes:
        ax.set_xlim(0.05, 0.95)
        ax.set_ylim(-0.09, 1.12)
        ax.set_aspect("equal")
        ax.axis("off")

    fig.tight_layout(pad=0.8)
    fig.savefig(imya, dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    shema_stupeni()
    shema_profil()
    shema_otvedeniya()
    print("Готово: stupeni.png, profil_boli.png, otvedeniya.png")
