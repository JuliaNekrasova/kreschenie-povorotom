#!/usr/bin/env python3
"""Схемы к журнальному клубу «Остановка сердца».

    python3 postroit.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Rectangle

plt.rcParams["font.family"] = "DejaVu Sans"
INK = "#1a1a1a"
MUT = "#5f5f5f"
ACC = "#8c2f2f"
BOX = "#e8e4dc"
W = 8.3


def torso(ax):
    ax.add_patch(FancyBboxPatch(
        (0, 0), 1.0, 1.35, boxstyle="round,pad=0.02,rounding_size=0.18",
        fc="#f6f3ee", ec=INK, lw=1.2))
    ax.plot([0.12, 0.88], [1.19, 1.19], color=MUT, lw=0.8, ls=":")
    ax.plot([0.10, 0.90], [0.30, 0.30], color=MUT, lw=0.8, ls=":")
    ax.add_patch(Ellipse((0.57, 0.62), 0.44, 0.36, angle=-18, fc="#d9cfc4", ec=INK, lw=1.0))
    ax.text(0.57, 0.62, "желудочки", ha="center", va="center", fontsize=7.4, color=INK)


def pad(ax, x, y, tag, dashed=False, color=INK):
    ax.add_patch(Circle(
        (x, y), 0.105, fc="none" if dashed else BOX, ec=color, lw=1.4,
        ls="--" if dashed else "-", zorder=3))
    ax.text(x, y, tag, ha="center", va="center", fontsize=8.6, color=color, zorder=4)


def arrow(ax, p1, p2, rad=0.0, lw=1.6, color=ACC, style="-|>"):
    ax.add_patch(FancyArrowPatch(
        p1, p2, arrowstyle=style, mutation_scale=12, color=color,
        lw=lw, connectionstyle=f"arc3,rad={rad}", zorder=2))


def shema_elektrody(imya="elektrody.png"):
    fig, axes = plt.subplots(1, 3, figsize=(W, 4.2))
    for ax in axes:
        ax.set_xlim(-0.18, 1.18)
        ax.set_ylim(-1.05, 1.5)
        ax.axis("off")

    a = axes[0]
    torso(a)
    pad(a, 0.22, 1.05, "1")
    pad(a, 0.93, 0.60, "2")
    arrow(a, (0.30, 0.99), (0.83, 0.64), rad=-0.20)
    pad(a, 0.86, 0.14, "✗", dashed=True, color=ACC)
    a.set_title("Переднебоковое (AL)", fontsize=10.5, color=INK, pad=8)
    a.text(0.5, -0.20,
           "1 — правая подключичная область\n2 — средняя подмышечная линия,\nV межреберье\n✗ — частая ошибка: электрод\nсмещён вперёд и вниз",
           ha="center", va="top", fontsize=8.0, color=INK)
    a.text(0.5, -0.78, "Ток идёт по касательной к желудочкам",
           ha="center", va="top", fontsize=7.6, color=MUT)

    b = axes[1]
    torso(b)
    pad(b, 0.30, 1.02, "1")
    pad(b, 0.62, 0.06, "2", dashed=True, color=MUT)
    arrow(b, (0.33, 0.92), (0.60, 0.19))
    b.set_title("Переднезаднее (AP)", fontsize=10.5, color=INK, pad=8)
    b.text(0.5, -0.20,
           "1 — слева от грудины, спереди\n2 — межлопаточная область,\nсзади (показан пунктиром)",
           ha="center", va="top", fontsize=8.0, color=INK)
    b.text(0.5, -0.78, "Желудочки оказываются между электродами",
           ha="center", va="top", fontsize=7.6, color=MUT)

    c = axes[2]
    torso(c)
    pad(c, 0.22, 1.05, "1")
    pad(c, 0.93, 0.60, "1")
    pad(c, 0.47, 1.02, "2")
    pad(c, 0.62, 0.06, "2", dashed=True, color=MUT)
    arrow(c, (0.30, 0.99), (0.83, 0.64), rad=-0.20, lw=1.3)
    arrow(c, (0.49, 0.92), (0.61, 0.19), lw=1.3)
    c.set_title("Двойная последовательная (DSED)", fontsize=10.5, color=INK, pad=8)
    c.text(0.5, -0.20,
           "1 — первый дефибриллятор,\nпереднебоковое положение\n2 — второй дефибриллятор,\nпереднезаднее положение",
           ha="center", va="top", fontsize=8.0, color=INK)
    c.text(0.5, -0.78, "Разряды с интервалом в доли секунды",
           ha="center", va="top", fontsize=7.6, color=MUT)

    fig.suptitle("Положение электродов и распределение тока через миокард",
                 fontsize=11.5, color=INK, y=0.99)
    fig.tight_layout(rect=[0, 0.0, 1, 0.93])
    fig.savefig(imya, dpi=200, facecolor="white")
    plt.close(fig)


def shema_refibrillyatsiya(imya="refibrillyatsiya.png"):
    fig, ax = plt.subplots(figsize=(W, 4.35))
    ax.set_xlim(-2, 122)
    ax.set_ylim(-0.20, 5.05)
    ax.axis("off")

    ax.text(60, 4.88, "Рецидив фибрилляции — не восстановление кровообращения",
            ha="center", va="center", fontsize=11.2, color=INK)

    ax.text(0, 4.48, "разряд", ha="left", va="center", fontsize=8.2, color=INK)
    ax.text(120, 4.48, "плановая проверка ритма", ha="right", va="center", fontsize=8.2, color=INK)

    ax.text(0, 4.12, "1. Ритм пациента", ha="left", va="center", fontsize=8.8, color=INK)
    ax.add_patch(Rectangle((0, 3.28), 120, 0.68, fc="#f0ece4", ec=INK, lw=1.0))
    ax.add_patch(Rectangle((0, 3.28), 30, 0.68, fc="#e3cfcf", ec=ACC, lw=1.2))
    ax.text(15, 3.62, "ФЖ чаще всего\nвозвращается здесь",
            ha="center", va="center", fontsize=7.8, color=ACC)
    ax.text(75, 3.62, "если вернулась — уже идёт,\nплановой проверки ещё нет",
            ha="center", va="center", fontsize=7.8, color=MUT)

    ax.text(0, 2.95, "2. Что видит бригада без фильтрации артефакта",
            ha="left", va="center", fontsize=8.8, color=INK)
    ax.add_patch(Rectangle((0, 2.12), 120, 0.68, fc="#eef1f3", ec=INK, lw=1.0))
    ax.text(60, 2.46, "компрессии, артефакт на мониторе, ритм не читается",
            ha="center", va="center", fontsize=8.4, color=INK)

    ax.plot([0, 0], [2.12, 4.38], color=INK, lw=1.1)
    ax.plot([120, 120], [2.12, 4.38], color=INK, lw=1.1)

    for t in (0, 30, 60, 90, 120):
        ax.plot([t, t], [2.04, 2.12], color=MUT, lw=0.8)
        ax.text(t, 1.90, f"{t} с", ha="center", va="top", fontsize=8.0, color=MUT)

    arrow(ax, (30, 1.35), (118, 1.35), style="<|-|>", color=ACC, lw=1.2)
    ax.text(74, 1.02,
            "Если ФЖ вернулась на 20-й секунде, до проверки остаётся около полутора минут\n"
            "незамеченной фибрилляции: компрессии идут, повторный разряд не наносится.",
            ha="center", va="top", fontsize=8.4, color=ACC)
    ax.text(60, 0.22,
            "Фильтрация артефакта компрессий (see-through CPR) позволяет увидеть рецидив, не прерывая массаж.",
            ha="center", va="top", fontsize=7.8, color=MUT)

    fig.tight_layout()
    fig.savefig(imya, dpi=200, facecolor="white")
    plt.close(fig)


def shema_ventilyatsiya(imya="ventilyatsiya.png"):
    fig, ax = plt.subplots(figsize=(W, 2.9))
    ax.set_xlim(-2, 76)
    ax.set_ylim(-1.7, 2.2)
    ax.axis("off")
    ax.text(-2, 2.0, "Счёт по часам против счёта по компрессиям",
            ha="left", va="center", fontsize=11.0, color=INK)
    ax.text(-2, 1.35, "по часам", ha="left", va="center", fontsize=9.0, color=MUT)
    ax.add_patch(Rectangle((16, 1.18), 56, 0.34, fc="#f0ece4", ec=MUT, lw=0.9))
    ax.text(44, 1.34, "«вдох каждые 6 секунд» — под нагрузкой счёт сбивается в гипервентиляцию",
            ha="center", va="center", fontsize=8.2, color=MUT)
    ax.text(-2, 0.10, "по компрессиям", ha="left", va="center", fontsize=9.0, color=INK)
    x = 16.0
    for _ in range(4):
        for _i in range(12):
            ax.plot([x, x], [-0.12, 0.32], color=INK, lw=1.5)
            x += 0.92
        ax.annotate("", xy=(x + 0.5, 0.62), xytext=(x + 0.5, 0.05),
                    arrowprops=dict(arrowstyle="-|>", color=ACC, lw=1.6))
        ax.text(x + 0.5, 0.72, "вдох", ha="center", va="bottom", fontsize=8.0, color=ACC)
        x += 2.3
    ax.text(16, -0.58, "12 компрессий — вдох, и так далее", ha="left", va="center", fontsize=9.2, color=INK)
    ax.text(16, -1.00,
            "При частоте компрессий 120 в минуту это ровно 10 вдохов в минуту:\n"
            "частоту задаёт ритм массажа, а не секундомер.",
            ha="left", va="top", fontsize=8.2, color=MUT)
    fig.tight_layout()
    fig.savefig(imya, dpi=200, facecolor="white")
    plt.close(fig)


def shema_etco2(imya="etco2.png"):
    fig, ax = plt.subplots(figsize=(W, 4.35))
    ax.set_xlim(-1, 52)
    ax.set_ylim(-0.15, 5.15)
    ax.axis("off")

    ax.text(25.5, 4.98, "Капнометрия во время реанимации: три диапазона и скачок",
            ha="center", va="center", fontsize=11.2, color=INK)

    # Шкала
    bands = [
        (0, 10, "#dcd2c8"),
        (10, 20, "#e9e2d6"),
        (20, 50, "#e0e6dc"),
    ]
    for x0, x1, col in bands:
        ax.add_patch(Rectangle((x0, 3.55), x1 - x0, 0.38, fc=col, ec=INK, lw=0.9))
    for t in (0, 10, 20, 30, 40, 50):
        ax.plot([t, t], [3.93, 4.02], color=MUT, lw=0.8)
        ax.text(t, 4.08, str(t), ha="center", va="bottom", fontsize=8.0, color=MUT)
    ax.text(51.2, 4.08, "мм рт. ст.", ha="left", va="bottom", fontsize=8.0, color=MUT)

    arrow(ax, (22, 4.55), (40, 4.55), lw=1.5)
    ax.text(31, 4.72, "внезапный устойчивый подъём на 10 и более, часто до 35–45 → оценить пульс",
            ha="center", va="bottom", fontsize=8.4, color=ACC)

    kartochki = [
        (0.4, 16.6, "#dcd2c8",
         "Ниже 10 мм рт. ст.",
         "Читается не сразу, а после\nпримерно 20 минут качественной\nСЛР, если обратимые причины\nуже исключены.\nВероятность восстановления\nкровообращения очень низкая."),
        (17.4, 33.6, "#e9e2d6",
         "10–20 мм рт. ст.",
         "В любой момент реанимации.\nКомпрессии и вентиляцию\nпересматривают: глубина,\nотпускание грудины, утечка\nчерез маску, частота вдохов."),
        (34.4, 50.6, "#e0e6dc",
         "20 мм рт. ст. и выше",
         "В любой момент реанимации.\nКомпрессии создают ощутимый\nкровоток. Это не цель и не\nоснование прекратить или\nпродолжить реанимацию."),
    ]
    for x0, x1, col, zag, tekst in kartochki:
        ax.add_patch(FancyBboxPatch(
            (x0, 0.35), x1 - x0, 2.95,
            boxstyle="round,pad=0.02,rounding_size=0.04",
            fc=col, ec=INK, lw=0.8))
        ax.text((x0 + x1) / 2, 2.95, zag, ha="center", va="top",
                fontsize=9.0, color=INK, fontweight="bold")
        ax.text((x0 + x1) / 2, 2.52, tekst, ha="center", va="top",
                fontsize=7.7, color=INK, linespacing=1.35)

    fig.tight_layout()
    fig.savefig(imya, dpi=200, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    shema_elektrody("elektrody.png")
    shema_refibrillyatsiya("refibrillyatsiya.png")
    shema_ventilyatsiya("ventilyatsiya.png")
    shema_etco2("etco2.png")
    print("Готово: elektrody.png, refibrillyatsiya.png, ventilyatsiya.png, etco2.png")
