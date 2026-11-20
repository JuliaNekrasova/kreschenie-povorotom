"""Схема фаз приступа по тексту романа: images/fazy_pristupa.png."""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

FON, PANEL, LINIYA, TEKST, SERYY, ORANZH = '#080c10', '#151d25', '#26333d', '#edf2f4', '#91a0aa', '#f47a21'
plt.rcParams['font.family'] = 'DejaVu Sans'

FAZY = [
    ('Аура', 'сознание сохранено', '«необычайный внутренний\nсвет озарил его душу»;\n«может быть, полсекунды»'),
    ('Иктальный крик', 'переход к утрате\nсознания', '«ясно и сознательно помнил\nначало, самый первый звук\nсвоего страшного вопля»'),
    ('Тонико-клоническая\nфаза', 'сознание утрачено', '«сознание его угасло»;\n«конвульсии и судороги\nовладевают всем телом»'),
    ('Постиктальный\nпериод', 'восстановление\nсознания', 'во фрагменте\nне описан'),
]

fig, ax = plt.subplots(figsize=(13, 5.2))
fig.patch.set_facecolor(FON)
ax.set_facecolor(FON)
ax.set_xlim(0, 13)
ax.set_ylim(0, 5.2)
ax.axis('off')

for i, (faza, soznanie, citata) in enumerate(FAZY):
    x = 0.3 + i * 3.2
    akcent = ORANZH if i < 2 else LINIYA
    ax.add_patch(FancyBboxPatch((x, 3.0), 2.8, 1.5, boxstyle='round,pad=0.04', fc=PANEL, ec=akcent, lw=1.6))
    ax.text(x + 1.4, 3.95, faza, ha='center', va='center', fontsize=14, color=TEKST, fontweight='bold')
    ax.text(x + 1.4, 3.3, soznanie, ha='center', va='center', fontsize=10.5, color=SERYY)
    ax.text(x + 1.4, 1.75, citata, ha='center', va='center', fontsize=10.5, color=TEKST, style='italic')
    if i < len(FAZY) - 1:
        ax.annotate('', xy=(x + 3.15, 3.75), xytext=(x + 2.85, 3.75),
                    arrowprops=dict(arrowstyle='->', color=SERYY, lw=1.5))

ax.plot([0.3, 6.7], [4.85, 4.85], color=ORANZH, lw=2.5)
ax.text(3.5, 5.0, 'фокальное начало', ha='center', va='bottom', fontsize=11, color=ORANZH)
ax.plot([6.7, 12.7], [4.85, 4.85], color=SERYY, lw=2.5)
ax.text(9.7, 5.0, 'билатеральное распространение', ha='center', va='bottom', fontsize=11, color=SERYY)
ax.text(6.5, 0.35, 'Классификация ILAE 2017: фокальный приступ с переходом в билатеральный тонико-клонический',
        ha='center', va='center', fontsize=11, color=SERYY)

fig.savefig(Path(__file__).resolve().parent / 'images' / 'fazy_pristupa.png', dpi=160, facecolor=FON, bbox_inches='tight', pad_inches=0.15)
