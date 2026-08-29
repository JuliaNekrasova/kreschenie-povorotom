#!/usr/bin/env python3
"""Графики к разбору «Тахисистолия при фибрилляции предсердий».

    python3 postroit.py

Модель однокамерная, феноменологическая: наполнение желудочка описано
экспоненциальным насыщением по времени диастолы, сократимость задана
предельным ударным объёмом. Числа подобраны так, чтобы соответствовать
порядку величин у пожилого пациента; это учебная модель зависимостей,
а не результат измерений у конкретного больного.
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
    "axes.titlesize": 10.5,
    "axes.titleweight": "bold",
    "axes.titlecolor": "#1c2833",
    "xtick.color": "#566573",
    "ytick.color": "#566573",
    "axes.grid": True,
    "grid.color": "#dfe4e6",
    "grid.linewidth": 0.6,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.dpi": 220,
    "savefig.bbox": "tight",
})

TEMNYY = "#1c2833"
SINIY = "#2471a3"
GOLUBOY = "#5499c7"
KRASNYY = "#a93226"
ORANZH = "#ca6f1e"
SERYY = "#7f8c8d"
ZELENYY = "#1e8449"


# --- физиология модели ---------------------------------------------------

def sistola(chss: np.ndarray | float) -> np.ndarray | float:
    """Длительность механической систолы, с.

    Систола при учащении тоже укорачивается, но несопоставимо слабее
    диастолы: основной вклад в укорочение цикла даёт диастола.
    """
    return np.clip(0.30 - 0.0005 * (np.asarray(chss, dtype=float) - 60), 0.20, None)


def diastola(chss: np.ndarray | float) -> np.ndarray:
    """Время наполнения желудочка, с."""
    return np.clip(60.0 / np.asarray(chss, dtype=float) - sistola(chss), 0.01, None)


def udarnyy_obem(t_dia: np.ndarray | float, uo_max: float, tau: float) -> np.ndarray:
    """Ударный объём как функция времени наполнения (насыщение)."""
    return uo_max * (1.0 - np.exp(-np.asarray(t_dia, dtype=float) / tau))


# Постоянная наполнения: у пожилого сердца релаксация замедлена
# (диастолическая дисфункция), поэтому наполнение сильнее зависит от времени.
TAU = 0.32

# Субстраты. Ключ модели — разная чувствительность к бета-блокаде.
# Сердце с сохранённым резервом теряет от блокады немного; сердце, выброс
# которого держится на максимальной симпатической стимуляции, теряет
# несопоставимо больше — именно поэтому приказ уводит застойную
# недостаточность на амиодарон, а не на метопролол.
SUBSTRATY = {
    "sohrannyy": {"podpis": "Сохранённая сократимость", "uo_max": 88.0, "beta": 0.92},
    "snizhennyy": {"podpis": "Сниженная сократимость (ФВ ≈ 25 %)", "uo_max": 40.0, "beta": 0.70},
}


# --- рисунок 1: куда девается диастола -----------------------------------

def risunok_diastola() -> None:
    chss = np.array([60, 80, 100, 120, 140, 160, 180, 200])
    sis = sistola(chss)
    dia = diastola(chss)

    figura, os = plt.subplots(figsize=(7.0, 3.5))
    x = np.arange(len(chss))

    os.bar(x, sis * 1000, width=0.62, color=SINIY, label="Систола", zorder=3)
    os.bar(x, dia * 1000, width=0.62, bottom=sis * 1000, color=GOLUBOY,
           label="Диастола (наполнение)", zorder=3)

    for i, (s, d) in enumerate(zip(sis, dia)):
        os.text(i, s * 1000 / 2, f"{s*1000:.0f}", ha="center", va="center",
                color="white", fontsize=8, fontweight="bold", zorder=4)
        os.text(i, s * 1000 + d * 1000 / 2, f"{d*1000:.0f}", ha="center", va="center",
                color=TEMNYY, fontsize=8, fontweight="bold", zorder=4)

    # выделить рабочую точку пациентки
    i160 = int(np.where(chss == 160)[0][0])
    os.annotate("ЧЖС 160:\nнаполнение 125 мс —\nкороче рукопожатия",
                xy=(i160 - 0.02, (sis[i160] + dia[i160]) * 1000 + 15),
                xytext=(i160 + 1.15, 570),
                fontsize=8.5, color=KRASNYY, fontweight="bold", ha="left",
                linespacing=1.45,
                arrowprops=dict(arrowstyle="->", color=KRASNYY, lw=1.3,
                                connectionstyle="arc3,rad=-0.10"))

    os.set_xticks(x)
    os.set_xticklabels(chss)
    os.set_xlabel("Частота желудочковых сокращений, мин⁻¹")
    os.set_ylabel("Длительность фазы, мс")
    # заголовок убран — подпись идёт в markdown-caption
    os.set_ylim(0, 770)
    # легенда уходит вправо-вниз: сверху справа стоит выноска, снизу — короткие столбики
    os.legend(loc="center right", bbox_to_anchor=(1.0, 0.60),
              frameon=False, fontsize=8.5)
    os.set_axisbelow(True)

    figura.savefig("ris1_diastola.png")
    plt.close(figura)


# --- рисунок 2: кривая Франка–Старлинга ----------------------------------

def risunok_starling() -> None:
    kdo = np.linspace(60, 150, 500)

    # сохранённая сократимость: крутой участок в рабочем диапазоне
    uo_sohr = 88 * (1 - np.exp(-(kdo - 48) / 42))
    # сниженная сократимость (ФВ ≈ 25 %): кривая и опущена, и распластана —
    # желудочек работает почти на пределе наполнения, добавка объёма даёт мало
    uo_sniz = 30 * (1 - np.exp(-(kdo - 40) / 28))

    figura, os = plt.subplots(figsize=(7.0, 4.2))

    kdo_bystro, kdo_medlenno = 78.0, 116.0
    for x, podpis, cvet_p in ((kdo_bystro, "ЧЖС 160", KRASNYY),
                              (kdo_medlenno, "ЧЖС 110", SERYY)):
        # вертикаль не тянем на всю высоту: низ и верх нужны под подписи
        os.plot([x, x], [14, 92], color=cvet_p, lw=1.0, ls=":", zorder=1)
        os.text(x, 97, podpis, fontsize=8, color=cvet_p, ha="center",
                va="top", fontweight="bold")

    os.plot(kdo, uo_sohr, color=SINIY, lw=2.6, zorder=3)
    os.plot(kdo, uo_sniz, color=KRASNYY, lw=2.6, zorder=3)

    # подписи прямо у кривых — отдельная легенда только отнимает место
    os.text(148, 85, "сохранённая сократимость", fontsize=8.4, color=SINIY,
            ha="right", va="center", fontweight="bold")
    os.text(148, 34, "сниженная сократимость (ФВ ≈ 25 %)", fontsize=8.4,
            color=KRASNYY, ha="right", va="center", fontweight="bold")

    def tochka(kdo_t: float, krivaya, cvet: str) -> float:
        uo_t = float(np.interp(kdo_t, kdo, krivaya))
        os.plot([kdo_t], [uo_t], "o", color=cvet, ms=7.5, mec="white", mew=1.4, zorder=5)
        return uo_t

    a1 = tochka(kdo_bystro, uo_sohr, SINIY)
    a2 = tochka(kdo_medlenno, uo_sohr, SINIY)
    b1 = tochka(kdo_bystro, uo_sniz, KRASNYY)
    b2 = tochka(kdo_medlenno, uo_sniz, KRASNYY)

    # вертикальные скобки прироста на правой границе диапазона
    skobka_x = kdo_medlenno + 4.0
    for niz, verh, cvet, y_podpisi in ((a1, a2, SINIY, (a1 + a2) / 2),
                                       (b1, b2, KRASNYY, 14.0)):
        os.add_patch(FancyArrowPatch((skobka_x, niz), (skobka_x, verh),
                                    arrowstyle="<|-|>", mutation_scale=10,
                                    color=cvet, lw=1.5, zorder=4))
        os.plot([kdo_bystro, skobka_x], [niz, niz],
                color=cvet, lw=0.8, alpha=0.45, zorder=2)
        os.text(skobka_x + 2.0, y_podpisi, f"+{verh - niz:.0f} мл\nна удар",
                color=cvet, fontsize=8.8, fontweight="bold", va="center",
                ha="left", linespacing=1.35)

    os.text(62.5, 76, "крутой участок:\nнаполнение ограничивает выброс",
            fontsize=8, color=SINIY, ha="left", va="center", linespacing=1.4)
    os.text(75, 7.5, "плато: желудочек почти полон,\nдобавка объёма ничего не даёт",
            fontsize=8, color=KRASNYY, ha="center", va="center", linespacing=1.4)

    os.set_xlabel("Конечно-диастолический объём, мл")
    os.set_ylabel("Ударный объём, мл")
    # заголовок убран
    os.set_xlim(60, 150)
    os.set_ylim(0, 100)
    os.set_axisbelow(True)

    figura.savefig("ris2_starling.png")
    plt.close(figura)


# --- рисунок 3: сердечный выброс против частоты --------------------------

def risunok_vybros() -> None:
    chss = np.linspace(50, 210, 500)
    t_dia = diastola(chss)

    poryadok = [("sohrannyy", SINIY), ("snizhennyy", KRASNYY)]
    figura, oси = plt.subplots(1, 2, figsize=(7.4, 3.7), sharey=False)

    for os, (klyuch, cvet) in zip(oси, poryadok):
        s = SUBSTRATY[klyuch]
        uo = udarnyy_obem(t_dia, s["uo_max"], TAU)
        mo = chss * uo / 1000.0                                  # л/мин
        uo_bb = udarnyy_obem(t_dia, s["uo_max"] * s["beta"], TAU)
        mo_bb = chss * uo_bb / 1000.0

        os.plot(chss, mo, color=cvet, lw=2.4, zorder=3, label="Без препарата")
        os.plot(chss, mo_bb, color=cvet, lw=1.8, ls="--", zorder=3,
                label="После бета-блокады")

        verh = float(mo.max()) * 1.30
        os.set_ylim(0, verh)

        pik = float(chss[np.argmax(mo)])
        os.axvline(pik, color=SERYY, lw=1.0, ls=":", zorder=2)
        os.text(pik + 5, verh * 0.20, f"максимум\nвыброса\nЧЖС {pik:.0f}",
                fontsize=7.2, color=SERYY, va="center", ha="left", linespacing=1.35)

        # рабочая точка 160 и результат урежения до 110 по кривой с блокадой
        mo160 = float(np.interp(160, chss, mo))
        mo110 = float(np.interp(110, chss, mo_bb))
        os.plot([160], [mo160], "o", color=cvet, ms=7.5, mec="white", mew=1.4, zorder=6)
        os.plot([110], [mo110], "s", color=cvet, ms=7.5, mec="white", mew=1.4, zorder=6)
        os.text(167, mo160 + verh * 0.035, "исходно\n160", fontsize=7.5, color=cvet,
                fontweight="bold", ha="left", va="bottom", linespacing=1.3)
        os.text(110, mo110 - verh * 0.05, "110", fontsize=7.5, color=cvet,
                fontweight="bold", ha="center", va="top")

        rastet = mo110 >= mo160
        # дугу ведём поверху при росте и понизу при падении, чтобы не лечь на кривую
        os.add_patch(FancyArrowPatch((160, mo160), (110, mo110),
                                    connectionstyle=f"arc3,rad={0.30 if rastet else -0.30}",
                                    arrowstyle="-|>", mutation_scale=12,
                                    color=TEMNYY, lw=1.4, zorder=5))

        cvet_itoga = ZELENYY if rastet else KRASNYY
        os.text(136, verh * 0.845,
                f"{'+' if rastet else '−'}{abs(mo110 - mo160):.1f} л/мин\n"
                f"{'урежение выгодно' if rastet else 'урежение вредит'}",
                fontsize=8.6, fontweight="bold", ha="center", va="center",
                color=cvet_itoga, linespacing=1.5,
                bbox=dict(boxstyle="round,pad=0.32", fc="white",
                          ec=cvet_itoga, lw=0.9, alpha=0.95))

        os.text(132, verh * 0.93,
                f"{(1-s['beta'])*100:.0f} % сократимости\nснимает бета-блокада",
                fontsize=8.2, color=cvet, ha="center", va="top",
                fontweight="bold", linespacing=1.35)
        os.set_xlabel("ЧЖС, мин⁻¹")
        os.set_xlim(50, 212)
        os.set_axisbelow(True)
        os.legend(loc="lower left", frameon=False, fontsize=7.5)

    oси[0].set_ylabel("Сердечный выброс, л/мин")
    # общий заголовок убран — подпись в markdown

    figura.savefig("ris3_vybros.png")
    plt.close(figura)


# --- рисунок 4: дефицит пульса при ФП ------------------------------------

def risunok_deficit() -> None:
    rr = np.array([0.30, 0.46, 0.38, 0.25, 0.54, 0.33, 0.27, 0.49, 0.36, 0.24, 0.44, 0.31])
    t_dia = np.clip(rr - 0.20, 0.01, None)
    uo = udarnyy_obem(t_dia, 88.0, TAU)
    porog = 26.0                            # ниже — удар не даёт ощутимой пульсовой волны

    momenty = np.concatenate([[0.0], np.cumsum(rr)[:-1]])

    figura, (os1, os2) = plt.subplots(2, 1, figsize=(7.2, 4.1), sharex=True,
                                      gridspec_kw={"height_ratios": [1, 1.5]})

    # верх: сам ритм
    for t in momenty:
        os1.plot([t, t], [0, 1], color=TEMNYY, lw=1.4, zorder=3)
    for t, interval in zip(momenty, rr):
        os1.annotate("", xy=(t + interval, 0.45), xytext=(t, 0.45),
                     arrowprops=dict(arrowstyle="<->", color=SERYY, lw=0.7))
        os1.text(t + interval / 2, 0.56, f"{interval*1000:.0f}",
                 fontsize=6.5, color=SERYY, ha="center")
    os1.set_ylim(0, 1.15)
    os1.set_yticks([])
    os1.set_ylabel("R–R, мс", fontsize=8.5)
    os1.grid(False)
    for storona in ("top", "right", "left", "bottom"):
        os1.spines[storona].set_visible(False)
    os1.tick_params(axis="x", length=0)
    # заголовок рисунка убран

    # низ: ударный объём удара, завершающего соответствующий интервал
    cveta = [GOLUBOY if v >= porog else KRASNYY for v in uo]
    os2.bar(momenty + rr / 2, uo, width=rr * 0.55, color=cveta, zorder=3)
    os2.axhline(porog, color=TEMNYY, lw=1.2, ls="--", zorder=4)
    os2.text(2.62, porog + 3.0,
             f"порог ощутимой пульсовой волны ≈ {porog:.0f} мл",
             fontsize=7.5, color=TEMNYY, ha="left", va="bottom")

    poteryano = int(np.sum(uo < porog))
    os2.text(0.015, 0.96,
             f"{poteryano} из {len(uo)} сокращений — дефицит пульса:\n"
             "аускультативное давление ловится не на каждом ударе",
             transform=os2.transAxes, fontsize=8, color=KRASNYY,
             va="top", linespacing=1.4)

    os2.set_ylim(0, 80)
    os2.set_xlim(-0.02, float(momenty[-1] + rr[-1]) + 0.02)
    os2.set_xlabel("Время, с")
    os2.set_ylabel("Ударный объём, мл", fontsize=8.5)
    os2.set_axisbelow(True)

    figura.savefig("ris4_deficit.png")
    plt.close(figura)


# --- рисунок 5: развилка алгоритма ---------------------------------------

def risunok_razvilka() -> None:
    figura, os = plt.subplots(figsize=(7.3, 4.9))
    os.set_xlim(0, 10)
    os.set_ylim(1.5, 10)          # низ обрезан по последнему блоку
    os.axis("off")

    STROKA = 0.30          # высота строки текста в единицах осей
    OTSTUP = 0.30          # вертикальный запас внутри рамки

    def blok(x, w, verh, tekst, fon, ramka, razmer=7.8, zhirno=False):
        """Рисует рамку под текст, привязывая её ВЕРХНИЙ край к `verh`."""
        strok = tekst.count("\n") + 1
        h = strok * STROKA + OTSTUP
        y = verh - h
        os.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle="round,pad=0.06,rounding_size=0.10",
                                    facecolor=fon, edgecolor=ramka, linewidth=1.2,
                                    zorder=3))
        os.text(x + w / 2, y + h / 2, tekst, ha="center", va="center",
                fontsize=razmer, color=TEMNYY, linespacing=1.42,
                fontweight="bold" if zhirno else "normal", zorder=4)
        return y            # низ рамки — точка выхода стрелки

    def strelka(x1, y1, x2, y2, podpis=None, cvet=SERYY):
        os.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                     mutation_scale=11, color=cvet, lw=1.3, zorder=2))
        if podpis:
            os.text((x1 + x2) / 2, (y1 + y2) / 2, podpis, fontsize=8.2,
                    color=cvet, ha="center", va="center", fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.16", fc="white", ec=cvet, lw=0.8))

    # 1. вход
    niz = blok(2.85, 4.3, 9.95,
               "ФП с тахисистолией\nЭКГ · мониторинг · венозный доступ",
               "#eaf2f8", SINIY, razmer=8.4, zhirno=True)

    # 2. фильтр: частота как компенсация — ДО выбора терапии
    strelka(5.0, niz, 5.0, 8.62)
    niz = blok(0.9, 8.2, 8.62,
               "Сначала: частота — это болезнь или компенсация?\n"
               "лихорадка · гиповолемия · гипоксия · боль · сепсис · ТЭЛА · анемия\n"
               "урежая компенсаторную тахисистолию, снимают компенсацию, а не причину",
               "#f4f6f7", SERYY, razmer=7.6)

    # 3. главная развилка
    strelka(5.0, niz, 5.0, 6.95)
    niz_vopros = blok(2.55, 4.9, 6.95,
                      "Гипотония, ОЛЖН\nили затяжной ангинозный приступ?",
                      "#fef5e7", ORANZH, razmer=8.4, zhirno=True)

    # 4. ветви
    strelka(3.0, niz_vopros + 0.10, 1.95, 5.30, "да", KRASNYY)
    strelka(7.0, niz_vopros + 0.10, 8.05, 5.30, "нет", ZELENYY)

    niz_l = blok(0.10, 4.55, 5.30,
                 "ОСЛОЖНЁННАЯ — независимо от давности\n"
                 "Гепарин 5000 МЕ в/в\n"
                 "или эноксапарин 1 мг/кг п/к\n"
                 "(на антикоагулянтах — не вводить)\n"
                 "Премедикация: диазепам 10 мг в/в\n"
                 "ЭИТ 100 Дж → до 200 Дж\n"
                 "не более 5 разрядов",
                 "#fdecea", KRASNYY, razmer=7.6)

    niz_p = blok(5.35, 4.55, 5.30,
                 "ТОЛЬКО ЧАСТОТА, ритм не восстанавливать\n"
                 "Застойная СН: амиодарон\n5 мг/кг, max 450 мг, 250 мл Д5%\nза 20 мин\n"
                 "Без застоя: метопролол по 5 мг в/в,\n"
                 "ориентир верхней границы 15 мг",
                 "#eafaf1", ZELENYY, razmer=7.6)

    # 5. тактика
    verh_takt = min(niz_l, niz_p) - 0.55
    strelka(2.4, niz_l, 3.9, verh_takt)
    strelka(7.6, niz_p, 6.1, verh_takt)
    blok(2.05, 5.9, verh_takt,
         "ЧЖС ≥ 130 после терапии → эвакуация\n"
         "Впервые выявленный пароксизм → стационар",
         "#eaf2f8", SINIY, razmer=8.0)

    # заголовок рисунка убран — подпись в markdown

    figura.savefig("ris5_razvilka.png")
    plt.close(figura)


# --- служебная печать чисел для текста -----------------------------------

def pechat_chisel(verbose: bool = False) -> None:
    """Диагностическая печать модельных чисел. По умолчанию — тихий режим."""
    if not verbose:
        return

    print("--- диастола по частоте ---")
    for c in (60, 80, 100, 110, 120, 140, 160, 180, 200):
        print(f"ЧЖС {c:3d}: цикл {60000/c:6.1f} мс, систола {sistola(c)*1000:5.1f}, "
              f"диастола {diastola(c)*1000:5.1f} мс")

    print("\n--- выброс по частоте ---")
    chss = np.linspace(50, 210, 2000)
    for klyuch, s in SUBSTRATY.items():
        uo = udarnyy_obem(diastola(chss), s["uo_max"], TAU)
        mo = chss * uo / 1000
        uo_bb = udarnyy_obem(diastola(chss), s["uo_max"] * s["beta"], TAU)
        mo_bb = chss * uo_bb / 1000
        mo160 = float(np.interp(160, chss, mo))
        mo110 = float(np.interp(110, chss, mo_bb))
        print(f"{klyuch:11s}: пик на ЧЖС {chss[np.argmax(mo)]:.0f} ({mo.max():.2f} л/мин); "
              f"160 без препарата → {mo160:.2f}; "
              f"110 после блокады → {mo110:.2f}; "
              f"итог {mo110 - mo160:+.2f} л/мин")

    print("\n--- дефицит пульса ---")
    rr = np.array([0.30, 0.46, 0.38, 0.25, 0.54, 0.33, 0.27, 0.49, 0.36, 0.24, 0.44, 0.31])
    uo = udarnyy_obem(np.clip(rr - 0.20, 0.01, None), 88.0, TAU)
    print(f"средний R–R {rr.mean()*1000:.0f} мс (≈{60/rr.mean():.0f} мин⁻¹), "
          f"УО от {uo.min():.0f} до {uo.max():.0f} мл, "
          f"ниже порога 26 мл: {int(np.sum(uo < 26))} из {len(uo)}")


if __name__ == "__main__":
    import sys
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    risunok_diastola()
    risunok_starling()
    risunok_vybros()
    risunok_deficit()
    risunok_razvilka()
    pechat_chisel(verbose)
    print("\nГрафики пересохранены")
