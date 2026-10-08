#!/usr/bin/env python3
"""Схемы к материалу «Пропафенон».

    python3 postroit.py

Данные взяты из опубликованных исследований, указанных в подписях и в
разделе «Источники» материала: Romano et al., 2001 (накопленная доля
восстановления синусового ритма при внутривенном пропафеноне и плацебо);
Bellandi et al., 1993 и Kochiadakis et al., 1998 (среднее время до
восстановления ритма при внутривенном пропафеноне и амиодароне).
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

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
ORANZH = "#ca6f1e"
SVETLYY = "#aab7bd"
FON_KR = "#f6e7e5"
KRASNYY = "#a93226"


def shema_skorost(imya="skorost_vosstanovleniya.png"):
    fig, (lev, prav) = plt.subplots(1, 2, figsize=(8.3, 3.6),
                                    gridspec_kw={"width_ratios": [1.15, 1]})

    # Левая панель: накопленная доля восстановления ритма (Romano et al., 2001)
    chasy = [0, 1, 3, 6, 24]
    propafenon = [0, 54.3, 68.3, 75.0, 92.1]
    placebo = [0, 22.2, 27.8, 35.2, 46.3]
    lev.axvspan(0, 20 / 60, color=FON_KR, zorder=0)
    lev.text(0.42, 96, "20 мин —\nожидание эффекта\nпо Алгоритмам", fontsize=7.4,
             color=KRASNYY, va="top", ha="left")
    # первый интервал не измерялся: отрезок 0–1 ч показан пунктиром
    lev.plot(chasy[:2], propafenon[:2], ":", color=SINIY, lw=1.4)
    lev.plot(chasy[:2], placebo[:2], ":", color=SVETLYY, lw=1.3)
    lev.plot(chasy[1:], propafenon[1:], "-o", color=SINIY, lw=1.8, ms=4,
             label="пропафенон в/в (n = 164)")
    lev.plot(chasy[1:], placebo[1:], "-o", color=SVETLYY, lw=1.6, ms=4,
             label="плацебо (n = 50)")
    for x, y in zip(chasy[1:], propafenon[1:]):
        lev.text(x, y + 3, f"{y:.0f}", ha="center", fontsize=7.4, color=SINIY)
    lev.set_xscale("symlog", linthresh=1)
    lev.set_xticks([0, 1, 3, 6, 24])
    lev.set_xticklabels(["0", "1", "3", "6", "24"])
    lev.set_xlim(0, 26)
    lev.set_ylim(0, 105)
    lev.set_xlabel("часы от начала введения")
    lev.set_ylabel("восстановлен синусовый ритм, %")
    lev.set_title("Накопленная доля восстановления ритма")
    lev.legend(loc="lower right", fontsize=7.4, frameon=False)
    for storona in ("top", "right"):
        lev.spines[storona].set_visible(False)

    # Правая панель: среднее время до восстановления ритма в двух РКИ
    issled = ["Bellandi\n1993", "Kochiadakis\n1998"]
    prop = [2.51, 2.0]
    amio = [11.21, 7.0]
    x = range(len(issled))
    shir = 0.36
    st1 = prav.bar([i - shir / 2 for i in x], prop, shir, color=SINIY,
                   label="пропафенон в/в")
    st2 = prav.bar([i + shir / 2 for i in x], amio, shir, color=ORANZH,
                   label="амиодарон в/в")
    for stolbcy in (st1, st2):
        for s in stolbcy:
            prav.text(s.get_x() + s.get_width() / 2, s.get_height() + 0.25,
                      f"{s.get_height():.1f}".replace(".", ","), ha="center",
                      fontsize=7.6, color=TEMNYY)
    prav.set_xticks(list(x))
    prav.set_xticklabels(issled)
    prav.set_ylabel("среднее время до ритма, ч")
    prav.set_ylim(0, 13)
    prav.set_title("Время до восстановления ритма")
    prav.legend(loc="upper right", fontsize=7.4, frameon=False)
    for storona in ("top", "right"):
        prav.spines[storona].set_visible(False)

    fig.tight_layout()
    fig.savefig(imya)
    plt.close(fig)
    print(imya)


if __name__ == "__main__":
    shema_skorost()
