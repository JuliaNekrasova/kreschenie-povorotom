#!/usr/bin/env python3
"""Схемы к разбору «Чрезвертельный перелом у пациентки 100 лет».

    python3 postroit.py

zony_bedra.png — проксимальный отдел правой бедренной кости, вид спереди:
    А — анатомические зоны и граница прикрепления капсулы сустава;
    Б — типичные линии переломов с кодами AO/OTA 2018.
garden.png — классификация переломов шейки бедренной кости Garden.
kadry_radiopaedia.jpg — рентгенограмма и МРТ из случая Radiopaedia
    (Tigges S., rID 187366), скомпонованы рядом; исходные кадры в radiopaedia_ishodniki/.

Контур кости условный: пропорции приближены к взрослой бедренной кости
(шеечно-диафизарный угол около 130°), это схема, а не анатомический атлас.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Arc
from matplotlib.path import Path as MPath

PAPKA = Path(__file__).resolve().parent

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.titlesize": 10.5,
    "axes.titleweight": "bold",
    "axes.titlecolor": "#1c2833",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.dpi": 220,
    "savefig.bbox": "tight",
})

TEMNYY = "#1c2833"
KOST = "#f4ecd8"
KOST_KRAY = "#6e5f45"
KAPSULA = "#2471a3"
KAPSULA_ZALIVKA = "#d6eaf8"
KRASNYY = "#a93226"
ORANZH = "#ca6f1e"
ZELENYY = "#1e8449"
FIOLET = "#7d3c98"
SERYY = "#7f8c8d"

# Условная система координат, мм; медиальная сторона слева, диафиз вертикален.
# Ось шейки выходит из точки OSNOVANIE под углом 130° к диафизу (40° к горизонтали).
OSNOVANIE = np.array([0.0, 135.0])
OS_SHEYKI = np.array([-np.cos(np.radians(40)), np.sin(np.radians(40))])
NORMAL = np.array([OS_SHEYKI[1], -OS_SHEYKI[0]])     # направлена вверх-латерально
GOLOVKA = tuple(OSNOVANIE + 65 * OS_SHEYKI)
R_GOL = 22.0


def na_sheyke(s: float, smeshchenie: float = 0.0) -> np.ndarray:
    """Точка на расстоянии s от основания по оси шейки, со смещением по нормали."""
    return OSNOVANIE + s * OS_SHEYKI + smeshchenie * NORMAL


def chaikin(tochki: np.ndarray, iteracii: int = 4) -> np.ndarray:
    """Сглаживание замкнутой ломаной методом Чайкина."""
    p = tochki
    for _ in range(iteracii):
        q = 0.75 * p + 0.25 * np.roll(p, -1, axis=0)
        r = 0.25 * p + 0.75 * np.roll(p, -1, axis=0)
        p = np.empty((2 * len(q), 2))
        p[0::2], p[1::2] = q, r
    return p


POLUSHIRINA_SHEYKI = 13.0


def styk_s_golovkoy(h: float) -> tuple[float, float]:
    """Параметр s и угол (рад) точки, где край шейки со смещением h входит в головку."""
    s = 65 - np.sqrt(R_GOL ** 2 - h ** 2)
    v = na_sheyke(s, h) - np.array(GOLOVKA)
    return s, np.arctan2(v[1], v[0])


def kontur_kosti() -> np.ndarray:
    """Замкнутый контур по часовой стрелке от латерального края диафиза внизу."""
    s_v, ug_v = styk_s_golovkoy(POLUSHIRINA_SHEYKI)
    s_n, ug_n = styk_s_golovkoy(-POLUSHIRINA_SHEYKI)
    lateral = [(15, 0), (15, 60), (15, 104), (17, 132), (21, 150), (24, 162),
               (21, 171), (13, 175), (6, 171), (3, 163)]                       # большой вертел и вертельная ямка
    verh = [tuple(na_sheyke(s, POLUSHIRINA_SHEYKI + 3 * (1 - s / s_v))) for s in (12, 30, s_v)]
    ugly = np.linspace(ug_v, ug_n + 2 * np.pi, 70)
    golovka = [(GOLOVKA[0] + R_GOL * np.cos(a), GOLOVKA[1] + R_GOL * np.sin(a)) for a in ugly]
    niz = [tuple(na_sheyke(s, -POLUSHIRINA_SHEYKI - 4 * (1 - s / s_n))) for s in (s_n, 28)]
    medial = [(-24, 133), (-19, 126), (-24, 121), (-31, 116), (-29, 110), (-19, 106),   # малый вертел
              (-15, 98), (-15, 60), (-15, 0)]
    return np.array(lateral + verh + golovka + niz + medial, dtype=float)


def narisovat_kost(ax, zalivka: str = KOST) -> None:
    syroy = kontur_kosti()
    # Сглаживается всё, кроме дуги головки, — у неё точек достаточно.
    gladkiy = chaikin(syroy, 3)
    gladkiy = np.vstack([gladkiy[gladkiy[:, 1] > 3], [(-15, 0), (15, 0)]])
    ax.add_patch(Polygon(gladkiy, closed=True, fc=zalivka, ec=KOST_KRAY, lw=1.3, zorder=2))
    x = np.linspace(-15, 15, 30)
    ax.plot(x, 1.2 * np.sin(x / 3.0), color=KOST_KRAY, lw=1.0, zorder=4)


def kapsula_kontur() -> tuple[np.ndarray, np.ndarray]:
    """Капсула: спереди крепится по межвертельной линии, проксимально — по краю вертлужной впадины."""
    t = np.linspace(0, 1, 40)
    nachalo, konec = np.array([9.0, 160.0]), np.array([-21.0, 126.0])
    mezh = nachalo + np.outer(t, konec - nachalo) + np.outer(np.sin(np.pi * t), [-4.0, 3.0])
    niz = [na_sheyke(22, -18), na_sheyke(40, -18)]
    ugly = np.radians(np.linspace(250, 60, 60))
    duga = np.column_stack([GOLOVKA[0] + 28 * np.cos(ugly), GOLOVKA[1] + 28 * np.sin(ugly)])
    verh = [na_sheyke(45, 17), na_sheyke(22, 17)]
    obvod = np.vstack([mezh, niz, duga, verh])
    return obvod, mezh


def kapsula(ax, zalivka: bool) -> None:
    obvod, mezh = kapsula_kontur()
    if zalivka:
        ax.add_patch(Polygon(obvod, closed=True, fc=KAPSULA_ZALIVKA, ec="none", alpha=0.55, zorder=3))
    ax.add_patch(Polygon(obvod, closed=True, fill=False, ec=KAPSULA, lw=1.3, ls=(0, (5, 3)), zorder=5))
    ax.plot(mezh[:, 0], mezh[:, 1], color=KAPSULA, lw=2.4, zorder=6)


def podpis(ax, xy, xytext, tekst, cvet=TEMNYY, ha="left") -> None:
    ax.annotate(tekst, xy=xy, xytext=xytext, fontsize=8.3, color=cvet, va="center", ha=ha,
                arrowprops=dict(arrowstyle="-", color=cvet if cvet != TEMNYY else SERYY, lw=0.7),
                zorder=8)


def risunok_zony() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 6.6))

    # А. Зоны.
    narisovat_kost(ax1)
    kapsula(ax1, zalivka=True)
    ax1.add_patch(Polygon([(-15, 108), (15, 108), (15, 58), (-15, 58)], closed=True,
                          fc="none", ec=FIOLET, hatch="////", lw=0, alpha=0.5, zorder=4))
    for y in (108, 58):
        ax1.plot([-30, 30], [y, y], color=FIOLET, lw=0.8, ls=":", zorder=6)

    podpis(ax1, GOLOVKA, (-108, 222), "Головка")
    podpis(ax1, tuple(na_sheyke(32, -6)), (-108, 128), "Шейка — внутри\nкапсулы")
    podpis(ax1, (14, 168), (40, 200), "Большой вертел")
    podpis(ax1, (-22, 115), (-108, 100), "Малый вертел")
    podpis(ax1, (6, 136), (40, 142), "Вертельная область —\nвне капсулы")
    podpis(ax1, (0, 83), (40, 83), "Подвертельная зона:\nот малого вертела\nна 5 см дистальнее", cvet=FIOLET)
    podpis(ax1, (-6, 145), (-108, 60), "Межвертельная линия —\nпередняя граница\nприкрепления капсулы",
           cvet=KAPSULA)
    ax1.text(-108, 246, "Пунктир и голубая заливка — пространство,\nограниченное капсулой сустава",
             fontsize=7.9, color=KAPSULA, va="center")
    ax1.set_title("А. Зоны проксимального отдела и капсула", loc="left")

    # Б. Линии переломов.
    narisovat_kost(ax2)
    kapsula(ax2, zalivka=False)

    def poperek(s: float, h: float) -> list:
        return [tuple(na_sheyke(s, h)), tuple(na_sheyke(s, -h))]

    linii = [
        (poperek(47, 15), KRASNYY, "31B1 —\nсубкапитальный", (-108, 128)),
        (poperek(31, 16), KRASNYY, "31B2 —\nтрансцервикальный", (-108, 102)),
        (poperek(12, 17), ORANZH, "31B3 —\nбазисцервикальный", (-108, 76)),
        ([(22, 158), (-22, 121)], ZELENYY, "31A1–A2 — чрезвертельный:\nот большого вертела\nк малому вертелу",
         (40, 184)),
        ([(-21, 128), (15, 98)], FIOLET, "31A3 — межвертельный\nс обратной косой\nлинией", (40, 120)),
        ([(-15, 86), (15, 79)], SERYY, "Подвертельный", (40, 74)),
    ]
    for (a, b), cvet, tekst, xytext in linii:
        ax2.plot([a[0], b[0]], [a[1], b[1]], color=cvet, lw=2.6, zorder=7, solid_capstyle="round")
        if xytext[0] < 0:
            konec_linii = a if a[1] < b[1] else b
        else:
            konec_linii = a if a[0] > b[0] else b
        podpis(ax2, konec_linii, xytext, tekst, cvet=cvet)
    ax2.text(-108, 256, "31C — переломы головки (Pipkin I–IV) не показаны",
             fontsize=7.9, color=SERYY, va="center")
    ax2.set_title("Б. Типичные линии переломов, AO/OTA 2018", loc="left")

    for ax in (ax1, ax2):
        ax.set_xlim(-110, 104)
        ax.set_ylim(40, 262)
        ax.set_aspect("equal")
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(PAPKA / "zony_bedra.png")
    plt.close(fig)


def povernut(tochki: np.ndarray, centr: tuple[float, float], ugol_grad: float) -> np.ndarray:
    a = np.radians(ugol_grad)
    m = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
    return (tochki - centr) @ m.T + centr


def panel_garden(ax, tip: int) -> None:
    """Упрощённая схема: впадина, головка, шейка; линия — медиальные компрессионные трабекулы."""
    cg = np.array([0.0, 0.0])
    r = 10.0
    # Вертлужная впадина.
    ax.add_patch(Arc(cg, 2 * r + 5, 2 * r + 5, theta1=20, theta2=200, color=SERYY, lw=2.2))
    # Шейка — четырёхугольник от головки вниз-латерально под 130° к диафизу.
    os_sheyki = np.array([np.cos(np.radians(-40)), np.sin(np.radians(-40))])
    norm = np.array([-os_sheyki[1], os_sheyki[0]])
    konec = cg + os_sheyki * 18
    # Дистальный фрагмент: шейка, большой и малый вертелы, начало диафиза.
    sheyka = chaikin(np.array([
        cg + os_sheyki * 4 + norm * 6.5, cg + os_sheyki * 17 + norm * 5.5,
        (21, -4), (25, -3), (28, -8), (27.5, -14), (26, -38), (15.5, -38),
        (15.5, -24), (12, -20), (13, -17.5), cg + os_sheyki * 18 - norm * 6.5,
        cg + os_sheyki * 4 - norm * 6.5,
    ]), 2)
    # Линия перелома поперёк шейки.
    lp = cg + os_sheyki * 11
    linia = np.array([lp + norm * 6.8, lp - norm * 6.8])
    # Трабекулы: в головке направлены к верхнему полюсу, в шейке — продолжение к дуге Адамса.
    trab_gol = np.array([cg + np.array([2.0, 8.5]), lp - norm * 1.0])
    trab_sh = np.array([lp - norm * 1.0, konec - norm * 5.0, (15.8, -26)])

    sdvig_sheyki = np.zeros(2)
    ugol_golovki = 0.0
    nepolnyy = False
    if tip == 1:
        ugol_golovki, nepolnyy = -14.0, True      # вальгусное вколачивание, медиальный кортикал цел
    elif tip == 2:
        ugol_golovki = 0.0
    elif tip == 3:
        ugol_golovki, sdvig_sheyki = 22.0, np.array([2.5, 2.0])    # варус, частичное смещение
    elif tip == 4:
        ugol_golovki, sdvig_sheyki = 0.0, np.array([7.0, 7.0])     # полное смещение, головка в анатомичном положении

    # Фрагмент шейки с диафизом.
    ax.add_patch(Polygon(sheyka + sdvig_sheyki, closed=True, fc=KOST, ec=KOST_KRAY, lw=1.2, zorder=2))
    ax.plot(*(trab_sh + sdvig_sheyki).T, color=KRASNYY, lw=1.8, zorder=4)
    # Головка поворачивается вокруг центра.
    golovka = Circle(cg, r, fc=KOST, ec=KOST_KRAY, lw=1.2, zorder=3)
    ax.add_patch(golovka)
    ax.plot(*povernut(trab_gol, tuple(cg), ugol_golovki).T, color=KRASNYY, lw=1.8, zorder=5)
    if nepolnyy:
        ax.plot(*linia[:1].T, alpha=0)
        chast = np.array([linia[0], linia[0] + (linia[1] - linia[0]) * 0.65])
        ax.plot(*chast.T, color=TEMNYY, lw=1.6, zorder=6)
    else:
        ax.plot(*(linia + sdvig_sheyki * 0.5).T, color=TEMNYY, lw=1.6, zorder=6)
    ax.set_xlim(-16, 38)
    ax.set_ylim(-40, 18)
    ax.set_aspect("equal")
    ax.axis("off")


def risunok_garden() -> None:
    opisanie = {
        1: "I — неполный, вальгусно\nвколоченный; нижний\nкортикальный слой цел",
        2: "II — полный,\nбез смещения;\nтрабекулы на одной линии",
        3: "III — полный, частичное\nсмещение в варус;\nтрабекулы под углом",
        4: "IV — полное смещение;\nголовка во впадине\nв анатомичном положении",
    }
    fig, osi = plt.subplots(1, 4, figsize=(10.4, 3.4))
    for tip, ax in zip(range(1, 5), osi):
        panel_garden(ax, tip)
        ax.set_title(opisanie[tip], fontsize=8.6, fontweight="normal", color=TEMNYY)
    fig.text(0.5, 0.02,
             "Красная линия — медиальные компрессионные трабекулы головки и шейки. "
             "I–II — стабильные, III–IV — нестабильные с нарушением кровоснабжения головки.",
             ha="center", fontsize=8, color=SERYY)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(PAPKA / "garden.png")
    plt.close(fig)


def kadry_radiopaedia() -> None:
    from PIL import Image

    ish = PAPKA / "radiopaedia_ishodniki"
    rg = Image.open(ish / "rentgen_kosaya.jpg").convert("L")
    mrt = Image.open(ish / "mrt_t1_koronar.jpg").convert("L")
    # Вставка-локализатор в правом нижнем углу кадра МРТ закрывается обрезкой.
    mrt = mrt.crop((0, 0, int(mrt.width * 0.88), int(mrt.height * 0.80)))
    vys = 640
    rg = rg.resize((round(rg.width * vys / rg.height), vys), Image.LANCZOS)
    mrt = mrt.resize((round(mrt.width * vys / mrt.height), vys), Image.LANCZOS)
    zazor = 14
    holst = Image.new("L", (rg.width + zazor + mrt.width, vys), 255)
    holst.paste(rg, (0, 0))
    holst.paste(mrt, (rg.width + zazor, 0))
    holst.save(PAPKA / "kadry_radiopaedia.jpg", quality=92)


if __name__ == "__main__":
    risunok_zony()
    risunok_garden()
    kadry_radiopaedia()
