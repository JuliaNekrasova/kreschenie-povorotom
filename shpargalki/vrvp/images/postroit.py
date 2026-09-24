#!/usr/bin/env python3
"""Схемы к материалу «Кровотечение из варикозно расширенных вен пищевода».

    python3 postroit.py

Содержание схем воспроизводит информационно-методическое письмо
ГБУЗ ССиНМП им. А. С. Пучкова № 1-14/2380 от 25.06.2021 и, в части
инфузионной терапии, раздел «Хирургические заболевания» приказа
Департамента здравоохранения города Москвы № 535 от 18.05.2023.

На схеме шокового индекса точками показаны значения письма, пунктиром —
линейный пересчёт по шагу «0,1 индекса = 0,2 л»: при индексах 1,5 и 2,0
они расходятся.

Высота блоков считается по числу строк текста, ширина проверяется оценкой
длины строки: при нехватке места скрипт печатает предупреждение, а не
молча выпускает схему с текстом за рамкой.
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
FON = "#eef2f4"
FON_KR = "#f6e7e5"
FON_OR = "#f9efe3"
FON_SIN = "#e4eef6"

SHIRINA = 8.3
MEZHSTROCHNYY = 1.42
DOLYA_EM = 0.56          # средняя ширина знака DejaVu Sans в долях кегля


class Polotno:
    """Оси на весь рисунок: доли осей совпадают с долями рисунка."""

    def __init__(self, vysota: float, shirina: float = SHIRINA):
        self.fig = plt.figure(figsize=(shirina, vysota))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.axis("off")
        self.shirina_pt = shirina * 72
        self.vysota_pt = vysota * 72

    def vysota_bloka(self, tekst: str, razmer: float, otstup: float = 7.0) -> float:
        strok = tekst.count("\n") + 1
        return (strok * razmer * MEZHSTROCHNYY + otstup) / self.vysota_pt

    def blok(self, x, y_verh, w, tekst, fon=FON, kant="#aab7bd", razmer=8.4,
             zhirnyy=False, tsvet=TEMNYY, vyravnivanie="center", imya=""):
        h = self.vysota_bloka(tekst, razmer)
        y = y_verh - h
        self.ax.add_patch(FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.004,rounding_size=0.010",
            linewidth=0.9, edgecolor=kant, facecolor=fon, zorder=2))
        if vyravnivanie == "center":
            tx, ha = x + w / 2, "center"
        else:
            tx, ha = x + 0.012, "left"
        self.ax.text(tx, y + h / 2, tekst, ha=ha, va="center", fontsize=razmer,
                     color=tsvet, fontweight="bold" if zhirnyy else "normal",
                     zorder=3, linespacing=MEZHSTROCHNYY)
        self.proverit(tekst, w, razmer, imya or tekst.split("\n")[0])
        return y

    def proverit(self, tekst, w, razmer, imya):
        dostupno = w * self.shirina_pt - 8
        for stroka in tekst.split("\n"):
            nado = len(stroka) * DOLYA_EM * razmer
            if nado > dostupno:
                print(f"  ! тесно: «{imya}» — строка «{stroka[:34]}…» "
                      f"{nado:.0f} pt при доступных {dostupno:.0f} pt")

    def strelka(self, xy_ot, xy_do, tsvet=SERYY, tolshchina=1.0):
        self.ax.add_patch(FancyArrowPatch(
            xy_ot, xy_do, arrowstyle="-|>", mutation_scale=11,
            linewidth=tolshchina, color=tsvet, zorder=1, shrinkA=1, shrinkB=1))

    def zapisat(self, imya):
        self.fig.savefig(imya)
        plt.close(self.fig)
        print(imya)


# --------------------------------------------------------------------------
# Схема 1. От уровня блока к источнику кровотечения
# --------------------------------------------------------------------------
def shema_gipertenziya(imya="portalnaya_gipertenziya.png"):
    p = Polotno(5.75)
    ax = p.ax

    ax.text(0.5, 0.977, "Уровень блока кровотоку",
            ha="center", va="center", fontsize=9.6, fontweight="bold", color=TEMNYY)

    formy = [
        (0.020, "Надпечёночная",
         "Тромбоз печёночных вен\n(синдром Бадда — Киари),\nинвазивная опухоль,\n"
         "обструкция нижней полой вены,\nзаболевания сердца и сосудов"),
        (0.345, "Внутрипечёночная",
         "Наиболее частая форма;\nкапилляризация синусоидов,\nложные дольки:\n"
         "вирусный гепатит, билиарный\nцирроз, алкогольный гепатит"),
        (0.670, "Подпечёночная",
         "Тромбоз воротной\nи селезёночной вены,\nвисцеральная\nартериовенозная фистула"),
    ]
    shir = 0.310
    nizy = []
    for x, nazvanie, prichiny in formy:
        p.blok(x, 0.952, shir, nazvanie, fon=FON_SIN, kant="#9bbdd8",
               razmer=9.2, zhirnyy=True, tsvet=SINIY)
        nizy.append(p.blok(x, 0.930 - p.vysota_bloka(nazvanie, 9.2), shir, prichiny,
                           fon="white", razmer=7.6))

    y = min(nizy) - 0.035
    for (x, _, _), niz in zip(formy, nizy):
        p.strelka((x + shir / 2, niz - 0.002), (0.5, y + 0.004))

    gipertenziya = ("ПОРТАЛЬНАЯ ГИПЕРТЕНЗИЯ\n"
                    "норма 5–10 мм рт. ст.; выше 12 мм рт. ст. —\n"
                    "портальная гипертензия и риск разрыва вен пищевода")
    y = p.blok(0.215, y, 0.570, gipertenziya, fon="#dfe6ea", kant="#8fa3ab",
               razmer=8.8, zhirnyy=True)

    y -= 0.030
    p.strelka((0.5, y + 0.032), (0.5, y + 0.004))
    kollaterali = ("Сеть портосистемных коллатералей: портальная гипертензия сохраняется,\n"
                   "сброс крови идёт по портокавальным анастомозам")
    y = p.blok(0.100, y, 0.800, kollaterali, fon=FON, razmer=8.4, zhirnyy=True)

    anastomozy = [
        (0.020, FON_KR, "#c8a09b", KRASNYY,
         "Гастроэзофагеальные",
         "Воротная вена → верхняя полая\nчерез венечную вену желудка,\nнепарную и полунепарную вены",
         "Варикозно расширенные вены\nпищевода и кардиального\nотдела желудка — источник\nмассивного кровотечения"),
        (0.345, FON, "#aab7bd", SERYY,
         "Околопупочные",
         "Расширенные вены передней\nбрюшной стенки,\nрасходящиеся от пупка",
         "«Голова медузы» — признак\nпортальной гипертензии\nпри осмотре, а не источник\nкровотечения"),
        (0.670, FON, "#aab7bd", SERYY,
         "Ректальные",
         "Венозные сплетения прямой\nкишки → нижняя полая вена\nчерез геморроидальные вены",
         "Варикозно расширенные\nгеморроидальные вены —\nвторой возможный источник\nкровотечения"),
    ]
    verh_vetvey = y - 0.032
    niz_vetvey = 1.0
    for x, fon, kant, tsvet, nazvanie, put_krovi, sledstvie in anastomozy:
        p.strelka((0.5, y - 0.002), (x + shir / 2, verh_vetvey + 0.004), tsvet=tsvet)
        y1 = p.blok(x, verh_vetvey, shir, nazvanie, fon=fon, kant=kant,
                    razmer=9.0, zhirnyy=True, tsvet=tsvet)
        y2 = p.blok(x, y1 - 0.008, shir, put_krovi, fon="white", kant=kant, razmer=7.6)
        p.strelka((x + shir / 2, y2 - 0.002), (x + shir / 2, y2 - 0.026), tsvet=tsvet)
        y3 = p.blok(x, y2 - 0.028, shir, sledstvie, fon=fon, kant=kant, razmer=7.8)
        niz_vetvey = min(niz_vetvey, y3)

    prochee = ("Прочие следствия портальной гипертензии: застойная спленомегалия "
               "с гиперспленизмом,\nасцит, печёночная и портокавальная энцефалопатия")
    p.blok(0.020, niz_vetvey - 0.026, 0.960, prochee, fon=FON, razmer=8.2)

    p.zapisat(imya)


# --------------------------------------------------------------------------
# Схема 2. Шоковый индекс и степени кровопотери
# --------------------------------------------------------------------------
def shema_indeks(imya="shokovyy_indeks.png"):
    fig, osi = plt.subplots(2, 1, figsize=(SHIRINA, 4.9),
                            gridspec_kw={"height_ratios": [2.2, 1.0]})

    ax = osi[0]
    pisma = [(0.5, 0.0, "норма"), (1.0, 1.0, "20 % ОЦК"),
             (1.5, 1.5, "30 % ОЦК"), (2.0, 2.0, "40 % ОЦК")]
    indeksy = np.linspace(0.5, 2.0, 100)
    ax.plot(indeksy, 2 * (indeksy - 0.5), color=SERYY, linewidth=1.1,
            linestyle=(0, (4, 3)),
            label="линейный пересчёт: 0,1 индекса = 0,2 л (4 % ОЦК)")
    ax.plot([t[0] for t in pisma], [t[1] for t in pisma], color=KRASNYY,
            linewidth=1.6, marker="o", markersize=6,
            label="значения письма № 1-14/2380")

    for x, y, podpis in pisma:
        if y:
            ax.annotate(f"{str(y).replace('.', ',')} л, {podpis}", (x, y),
                        textcoords="offset points", xytext=(9, -11),
                        fontsize=8.0, color=KRASNYY)
        else:
            ax.annotate(podpis, (x, y), textcoords="offset points",
                        xytext=(9, -4), fontsize=8.0, color=SERYY)
    ax.annotate("при индексе 2,0 линейное\nправило даёт 3 л (60 % ОЦК)",
                (2.0, 3.0), textcoords="offset points", xytext=(-140, -4),
                fontsize=8.0, color=SERYY)

    ax.set_xlim(0.4, 2.2)
    ax.set_ylim(-0.3, 3.5)
    ax.set_xticks([0.5, 1.0, 1.5, 2.0])
    ax.set_xticklabels(["0,5", "1,0", "1,5", "2,0"])
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(["0", "1", "2", "3"])
    ax.set_xlabel("шоковый индекс Альговера = ЧСС / АД систолическое")
    ax.set_ylabel("объём кровопотери, л")
    ax.set_title("Соответствие шокового индекса объёму кровопотери", loc="left")
    ax.grid(axis="y", color="#e5e9eb", linewidth=0.8)
    ax.set_axisbelow(True)
    for storona in ("top", "right"):
        ax.spines[storona].set_visible(False)
    ax.legend(loc="upper left", fontsize=7.8, frameon=False)

    ax2 = osi[1]
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    ax2.text(0.0, 0.94, "Степени острой кровопотери (таблица 1 письма)",
             ha="left", va="center", fontsize=9.3, fontweight="bold", color=TEMNYY)

    stepeni = [
        (0.020, "#f4f7f8", "#aab7bd", SINIY, "1 ст. — лёгкая",
         "Состояние удовлетворительное\nЧСС 80–100 в минуту\nАД сист. в пределах нормы\n"
         "Дефицит ОЦК до 20 %\nКровопотеря до 1000 мл"),
        (0.345, FON_OR, "#d8b283", ORANZH, "2 ст. — средняя",
         "Состояние средней тяжести\nЧСС до 110 в минуту\nАД сист. не ниже 90 мм рт. ст.\n"
         "Дефицит ОЦК 20–29 %\nКровопотеря 1500 мл"),
        (0.670, FON_KR, "#c8a09b", KRASNYY, "3 ст. — тяжёлая",
         "Состояние тяжёлое\nЧСС более 110 в минуту\nАД сист. ниже 90 мм рт. ст.\n"
         "Дефицит ОЦК 30 % и более\nКровопотеря 2000 мл"),
    ]
    shir = 0.310
    for x, fon, kant, tsvet, nazvanie, priznaki in stepeni:
        ax2.add_patch(FancyBboxPatch(
            (x, 0.700), shir, 0.145,
            boxstyle="round,pad=0.004,rounding_size=0.010",
            linewidth=0.9, edgecolor=kant, facecolor=fon, zorder=2))
        ax2.text(x + shir / 2, 0.772, nazvanie, ha="center", va="center",
                 fontsize=9.0, fontweight="bold", color=tsvet, zorder=3)
        ax2.add_patch(FancyBboxPatch(
            (x, 0.030), shir, 0.640,
            boxstyle="round,pad=0.004,rounding_size=0.010",
            linewidth=0.9, edgecolor=kant, facecolor="white", zorder=2))
        ax2.text(x + 0.012, 0.350, priznaki, ha="left", va="center",
                 fontsize=7.7, color=TEMNYY, zorder=3, linespacing=1.5)

    fig.tight_layout()
    fig.savefig(imya)
    plt.close(fig)
    print(imya)


# --------------------------------------------------------------------------
# Схема 3. Объём помощи на вызове
# --------------------------------------------------------------------------
def shema_pomoshch(imya="pomoshch_vrvp.png"):
    p = Polotno(4.45)

    y_levo = p.blok(0.020, 0.980, 0.470,
                    "Рвота жидкой красной кровью\nили сгустками вишнёвого цвета",
                    fon=FON_KR, kant="#c8a09b", razmer=8.6, zhirnyy=True, tsvet=KRASNYY)
    y_pravo = p.blok(0.510, 0.980, 0.470,
                     "Признаки поражения печени: телеангиоэктазии,\n"
                     "расширение подкожных вен брюшной стенки,\n"
                     "желтуха, асцит; цирроз печени в анамнезе",
                     fon=FON, razmer=7.9)

    y = min(y_levo, y_pravo) - 0.034
    p.strelka((0.255, y_levo - 0.002), (0.440, y + 0.004))
    p.strelka((0.745, y_pravo - 0.002), (0.560, y + 0.004))

    y = p.blok(0.120, y, 0.760,
               "Оценка: общее состояние; сознание, дыхание, кровообращение;\n"
               "ЧСС и АД → шоковый индекс; перкуссия и пальпация живота",
               fon="#dfe6ea", kant="#8fa3ab", razmer=8.5, zhirnyy=True)

    p.strelka((0.5, y - 0.002), (0.5, y - 0.030))
    p.ax.text(0.5, y - 0.048, "Объём помощи выездной бригады по письму № 1-14/2380",
              ha="center", va="center", fontsize=9.2, fontweight="bold", color=TEMNYY)

    meropriyatiya = [
        ("Венозный\nдоступ", FON, "#aab7bd"),
        ("Ингаляция\nкислорода", FON, "#aab7bd"),
        ("Транексамовая\nкислота 750 мг\nвнутривенно", FON_OR, "#d8b283"),
        ("Инфузионная\nтерапия\nпо «Алгоритмам»", FON, "#aab7bd"),
        ("Терлипрессин\n1,0 мг в 10 мл\nнатрия хлорида\n0,9 % внутривенно", FON_KR, "#c8a09b"),
    ]
    w, zazor = 0.186, 0.0175
    x0 = (1 - (5 * w + 4 * zazor)) / 2
    verh = y - 0.070
    nizy = []
    for i, (tekst, fon, kant) in enumerate(meropriyatiya):
        x = x0 + i * (w + zazor)
        nizy.append(p.blok(x, verh, w, tekst, fon=fon, kant=kant, razmer=7.9))

    y = min(nizy) - 0.030
    for i, niz in enumerate(nizy):
        x = x0 + i * (w + zazor)
        p.strelka((x + w / 2, niz - 0.002), (x + w / 2, y + 0.004), tolshchina=0.85)

    y = p.blok(0.020, y, 0.960,
               "Медицинская эвакуация в кратчайшие сроки в профильный стационар\n"
               "с проведением при транспортировке всех необходимых мероприятий",
               fon=FON_SIN, kant="#9bbdd8", razmer=8.6, zhirnyy=True, tsvet=SINIY)

    y_levo = p.blok(0.020, y - 0.028, 0.470,
                    "Вазоактивный препарат назначается\n"
                    "как можно раньше: снижение портального\n"
                    "давления удерживает гемодинамику\n"
                    "во время транспортировки",
                    fon="white", kant="#c8a09b", razmer=7.8)
    y_pravo = p.blok(0.510, y - 0.028, 0.470,
                     "Стационарный этап: вазоконстрикторы,\n"
                     "блокаторы протонной помпы,\n"
                     "эндоскопический гемостаз",
                     fon="white", razmer=7.8)

    p.blok(0.020, min(y_levo, y_pravo) - 0.026, 0.960,
           "Схема применения терлипрессина в письме ограничена первоначальной дозой 1,0 мг:\n"
           "повторное введение, интервал и длительность терапии, противопоказания\n"
           "и нежелательные реакции в документе не описаны",
           fon=FON, razmer=8.0)

    p.zapisat(imya)


if __name__ == "__main__":
    shema_gipertenziya()
    shema_indeks()
    shema_pomoshch()
