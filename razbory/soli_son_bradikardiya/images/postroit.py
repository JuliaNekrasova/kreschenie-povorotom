#!/usr/bin/env python3
"""Схемы к разбору «Соли, сон и брадикардия».

    python3 postroit.py

1. formuly.png — структурные формулы амфетамина, катинона, мефедрона и α-PVP
   (исходные изображения Wikimedia Commons лежат в _formuly/, см. материал).
2. chss_son.png — частота сердечных сокращений во сне и бодрствовании у
   здоровых молодых мужчин по Brodsky et al., 1977, в сопоставлении с
   показателями пациента.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

PAPKA = Path(__file__).resolve().parent

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
SVETLO_SINIY = "#aed6f1"
KRASNYY = "#a93226"
ORANZH = "#ca6f1e"


def shema_formuly(imya="formuly.png"):
    istochniki = [
        ("Amphetamine.png", "Амфетамин", "фенилэтиламин без кетогруппы"),
        ("Cathinone.png", "Катинон", "β-кетогруппа (алкалоид ката)"),
        ("Mephedrone.png", "Мефедрон (4-MMC)", "N-метил, 4-метил; субстрат"),
        ("Alpha-PVP.png", "α-PVP", "пирролидиновое кольцо; блокатор"),
    ]
    shir_yach, vys_ris, vys_podp = 520, 330, 90
    holst = Image.new("RGB", (shir_yach * 4, vys_ris + vys_podp), "white")
    risovat = ImageDraw.Draw(holst)
    shrifty = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
    shrift_zag = ImageFont.truetype(str(shrifty / "DejaVuSans-Bold.ttf"), 30)
    shrift_pod = ImageFont.truetype(str(shrifty / "DejaVuSans.ttf"), 22)
    for n, (fayl, zag, pod) in enumerate(istochniki):
        im = Image.open(PAPKA / "_formuly" / fayl).convert("LA")
        fon = Image.new("RGB", im.size, "white")
        fon.paste(im.convert("RGB"), mask=im.split()[-1])
        fon.thumbnail((shir_yach - 50, vys_ris - 30))
        x0 = n * shir_yach + (shir_yach - fon.width) // 2
        y0 = (vys_ris - fon.height) // 2
        holst.paste(fon, (x0, y0))
        for tekst, shrift, y, cvet in ((zag, shrift_zag, vys_ris + 8, TEMNYY),
                                       (pod, shrift_pod, vys_ris + 50, SERYY)):
            w = risovat.textlength(tekst, font=shrift)
            risovat.text((n * shir_yach + (shir_yach - w) / 2, y), tekst, fill=cvet, font=shrift)
    for n in range(1, 4):
        risovat.line([(n * shir_yach, 20), (n * shir_yach, vys_ris + vys_podp - 20)],
                     fill="#d5dbdb", width=2)
    holst.save(PAPKA / imya, optimize=True)
    print(imya)


def shema_chss(imya="chss_son.png"):
    fig, ax = plt.subplots(figsize=(8.0, 3.4))
    # Brodsky et al., 1977: 50 студентов-медиков мужского пола, суточное мониторирование ЭКГ
    stroki = [
        ("Сон: минимальная ЧСС", 33, 55, 43),
        ("Сон: средняя ЧСС", 45, 70, 56),
        ("Бодрствование: минимальная ЧСС", 37, 65, 53),
        ("Бодрствование: средняя ЧСС", 67, 90, 80),
    ]
    for i, (podp, mn, mx, sr) in enumerate(stroki):
        y = len(stroki) - i
        ax.plot([mn, mx], [y, y], color=SVETLO_SINIY, lw=9, solid_capstyle="butt", zorder=1)
        ax.plot([sr], [y], "o", color=SINIY, ms=6, zorder=2)
        ax.text(mn - 1.5, y, f"{mn}", ha="right", va="center", fontsize=7.5, color=SERYY)
        ax.text(mx + 1.5, y, f"{mx}", ha="left", va="center", fontsize=7.5, color=SERYY)
    ax.axvspan(40, 42, color=KRASNYY, alpha=0.18, zorder=0)
    ax.axvline(41, color=KRASNYY, lw=1.2, ls="--", zorder=0)
    ax.text(41, 4.75, "пациент во сне\n40–42", ha="center", va="bottom", fontsize=7.6,
            color=KRASNYY, bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
    ax.axvline(70, color=ORANZH, lw=1.2, ls="--", zorder=0)
    ax.text(70, 4.75, "при пробуждении\nоколо 70", ha="center", va="bottom", fontsize=7.6,
            color=ORANZH, bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
    ax.set_yticks(range(len(stroki), 0, -1))
    ax.set_yticklabels([s[0] for s in stroki])
    ax.set_xlim(25, 100)
    ax.set_ylim(0.4, 5.6)
    ax.set_xlabel("частота сердечных сокращений, уд/мин")
    ax.plot([], [], color=SVETLO_SINIY, lw=7, label="диапазон у 50 здоровых студентов-медиков мужского пола")
    ax.plot([], [], "o", color=SINIY, ms=5, label="среднее")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=7.4, frameon=False)
    for storona in ("top", "right"):
        ax.spines[storona].set_visible(False)
    fig.tight_layout()
    fig.savefig(PAPKA / imya)
    plt.close(fig)
    print(imya)


if __name__ == "__main__":
    shema_formuly()
    shema_chss()
