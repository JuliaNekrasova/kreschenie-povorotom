#!/usr/bin/env python3
"""Схема к разбору «Жизнеугрожающая астма».

    python3 postroit.py

Модель однокамерная: лёгкое — эластичный резервуар с податливостью C,
соединённый с атмосферой через сопротивление R. Вдох — постоянный поток,
выдох пассивный, объём над функциональной остаточной ёмкостью убывает
экспоненциально с постоянной времени tau = R·C. Числа подобраны под порядок
величин у взрослого с тяжёлой обструкцией при частоте дыхания 26 в минуту;
это учебная модель зависимостей, а не результат измерений у пациентки.
"""

from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

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
KRASNYY = "#a93226"
SERYY = "#7f8c8d"
ZELENYY = "#1e8449"

CHD = 26                 # дыхательных циклов в минуту
T_CIKL = 60.0 / CHD      # с
T_VD = 0.8               # длительность вдоха, с
T_VYD = T_CIKL - T_VD    # длительность выдоха, с
DO = 0.40                # дыхательный объём, л
C = 0.05                 # податливость, л/см вод. ст.
TAU_NORMA = 0.4          # постоянная времени без обструкции, с
TAU_OBSTR = 2.0          # постоянная времени при тяжёлой обструкции, с
CPAP = 5.0               # внешнее ПДКВ, см вод. ст.
CIKLOV = 8


def krivaya(tau: float, shag: float = 0.005) -> tuple[np.ndarray, np.ndarray]:
    """Объём над ФОЕ во времени для серии циклов, начиная с ФОЕ."""
    t_vse, v_vse = [], []
    v0, t0 = 0.0, 0.0
    for _ in range(CIKLOV):
        t = np.arange(0, T_VD, shag)
        t_vse.append(t0 + t)
        v_vse.append(v0 + DO * t / T_VD)
        v_konec_vd = v0 + DO
        t = np.arange(0, T_VYD, shag)
        t_vse.append(t0 + T_VD + t)
        v_vse.append(v_konec_vd * np.exp(-t / tau))
        v0 = v_konec_vd * np.exp(-T_VYD / tau)
        t0 += T_CIKL
    return np.concatenate(t_vse), np.concatenate(v_vse)


def ravnovesnyy_ostatok(tau: float) -> float:
    """Объём над ФОЕ в конце выдоха в установившемся режиме, л."""
    k = np.exp(-T_VYD / tau)
    return DO * k / (1 - k)


def risunok() -> None:
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(10.2, 3.7), gridspec_kw={"width_ratios": [1.75, 1]}
    )

    for tau, cvet, podpis in (
        (TAU_NORMA, SERYY, f"Без обструкции (τ = {TAU_NORMA:g} с)".replace(".", ",")),
        (TAU_OBSTR, KRASNYY, f"Тяжёлая обструкция (τ = {TAU_OBSTR:g} с)"),
    ):
        t, v = krivaya(tau)
        ax1.plot(t, v * 1000, color=cvet, lw=1.6, label=podpis)

    v_ost = ravnovesnyy_ostatok(TAU_OBSTR)
    auto_peep = v_ost / C
    ax1.axhline(v_ost * 1000, color=KRASNYY, lw=0.9, ls="--")
    ax1.annotate(
        f"Объём в конце выдоха ≈ {v_ost * 1000:.0f} мл над ФОЕ\n"
        f"внутреннее ПДКВ ≈ {auto_peep:.0f} см вод. ст.",
        xy=(T_CIKL * 6.6, v_ost * 1000), xytext=(T_CIKL * 4.1, 930),
        fontsize=8.3, color=KRASNYY,
        arrowprops=dict(arrowstyle="->", color=KRASNYY, lw=0.8),
    )
    ax1.axhline(0, color=TEMNYY, lw=0.8)
    ax1.text(0.05, 18, "ФОЕ", fontsize=8, color=TEMNYY)
    ax1.set_xlim(0, T_CIKL * CIKLOV)
    ax1.set_ylim(-60, 1120)
    ax1.set_xlabel("Время, с")
    ax1.set_ylabel("Объём лёгких над ФОЕ, мл")
    ax1.set_title(f"А. Динамическая гиперинфляция при ЧДД {CHD} в минуту")
    ax1.legend(loc="upper left", fontsize=8, frameon=False)

    porog_bez = auto_peep
    porog_cpap = max(auto_peep - CPAP, 0)
    stolby = ax2.barh(
        [1, 0], [porog_bez, porog_cpap], color=[KRASNYY, ZELENYY], height=0.5
    )
    for st, znach in zip(stolby, (porog_bez, porog_cpap)):
        ax2.text(znach + 0.2, st.get_y() + st.get_height() / 2,
                 f"{znach:.0f} см вод. ст.", va="center", fontsize=8.5, color=TEMNYY)
    ax2.set_yticks([1, 0])
    ax2.set_yticklabels(["Без внешнего\nПДКВ", f"CPAP\n{CPAP:g} см вод. ст."])
    ax2.set_xlim(0, porog_bez + 3.2)
    ax2.set_xlabel("Снижение давления до начала\nпотока на вдохе, см вод. ст.")
    ax2.set_title("Б. Пороговая нагрузка на вдохе")
    ax2.grid(axis="y", visible=False)
    ax2.set_axisbelow(True)

    fig.tight_layout()
    fig.savefig("auto_pdkv.png")
    plt.close(fig)


if __name__ == "__main__":
    risunok()
