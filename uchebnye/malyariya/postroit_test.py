#!/usr/bin/env python3
"""Сборка теста по материалу «Малярия».

    python3 postroit_test.py

Результат — один автономный файл malyariya_test.html: картинки вложены
в него base64, внешних запросов нет, работает без сети и с телефона.
Так же собраны тренажёры раздела, чтобы файл можно было просто скачать
и открыть.

Вопросы и разборы правильных ответов лежат в списке VOPROSY ниже; текст
разборов намеренно повторяет формулировки материала, чтобы тест учил, а
не только проверял.
"""

from __future__ import annotations

import base64
import html
import json
from pathlib import Path

PAPKA = Path(__file__).resolve().parent
KARTINKI = PAPKA / "images"
CEL = PAPKA / "malyariya_test.html"


def v_base64(fayl: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(fayl.read_bytes()).decode("ascii")


# --- вопросы --------------------------------------------------------------
# tip: "odin" — один правильный ответ; verno — индекс правильного варианта.
# kartinka: ключ из словаря KARTINKI_HTML, если к вопросу идёт изображение.

VOPROSY = [
    {
        "tema": "Цикл",
        "vopros": "Почему комар для малярийного плазмодия — окончательный хозяин, а человек — промежуточный?",
        "varianty": [
            "Комар живёт дольше, и паразит успевает пройти в нём весь цикл",
            "В комаре происходит половое размножение, в человеке — только бесполое",
            "В комаре паразит размножается численно, а в человеке лишь сохраняется",
            "Так сложилось исторически; биологического содержания в этих словах нет",
        ],
        "verno": 1,
        "razbor": "Окончательным хозяином называют организм, в котором паразит размножается половым путём. "
                  "В человеке идёт только бесполое размножение — шизогония, а слияние гамет возможно "
                  "исключительно в желудке комара. Отсюда и следствие: комар — не «летающий шприц», "
                  "а место, где паразит спаривается.",
    },
    {
        "tema": "Цикл",
        "vopros": "На фотографии самка Anopheles во время питания. По какому признаку род узнаётся на глаз?",
        "varianty": [
            "Полосатые лапки и пятнистые крылья",
            "Тело приподнято под углом к поверхности, хоботок продолжает его линию",
            "Тело параллельно поверхности, хоботок направлен к ней под углом",
            "Размер: Anopheles заметно крупнее прочих комаров",
        ],
        "verno": 1,
        "razbor": "У Anopheles тело приподнято под углом к поверхности и хоботок продолжает линию тела. "
                  "У Culex и Aedes наоборот: тело держится почти параллельно поверхности, а хоботок "
                  "направлен к ней под углом. Признак используется в полевой энтомологии.",
        "kartinka": "komar",
    },
    {
        "tema": "Цикл",
        "vopros": "Пациент вернулся из Африки и на третий день после возвращения слёг с лихорадкой 39 °С. Что следует из срока?",
        "varianty": [
            "Это типичная тропическая малярия: инкубация у falciparum короткая",
            "Это малярия, но обязательно vivax — только у неё бывает такая ранняя лихорадка",
            "Лихорадка этого срока малярией, полученной в поездке, объясниться не может",
            "Срок ничего не значит: малярия начинается в любое время после укуса",
        ],
        "verno": 2,
        "razbor": "Тканевая шизогония занимает минимум 5–7 суток у P. falciparum и больше у остальных видов, "
                  "и всё это время болезнь бессимптомна. Раньше седьмого дня после укуса малярии не бывает — "
                  "паразит физически не успевает пройти печень. Обратное, однако, неверно: через восемь месяцев "
                  "малярия вполне возможна.",
    },
    {
        "tema": "Цикл",
        "vopros": "Что такое гипнозоиты и у каких видов они есть?",
        "varianty": [
            "Дремлющие формы в гепатоцитах; P. vivax и P. ovale",
            "Дремлющие формы в эритроцитах; P. falciparum",
            "Дремлющие формы в селезёнке; все четыре вида",
            "Незрелые гаметоциты в костном мозге; P. malariae",
        ],
        "verno": 0,
        "razbor": "Часть спорозоитов P. vivax и P. ovale, попав в гепатоцит, не делится, а замирает на 7–14 месяцев "
                  "и дольше. Отсюда и растянутая инкубация, и отдалённые рецидивы вплоть до трёх лет. "
                  "У P. falciparum и P. malariae гипнозоитов нет.",
    },
    {
        "tema": "Цикл",
        "vopros": "На схеме отмечен цикл длительностью 48 часов. Где он происходит?",
        "varianty": [
            "В гепатоцитах — это тканевая шизогония",
            "В эритроцитах — это эритроцитарная шизогония",
            "В желудке комара — это спорогония",
            "В слюнных железах комара — это дозревание спорозоитов",
        ],
        "verno": 1,
        "razbor": "48 часов — длительность одного эритроцитарного цикла у P. vivax, P. ovale и P. falciparum; "
                  "у P. malariae он занимает 72 часа. Тканевая шизогония на схеме подписана отдельно — "
                  "5–6 суток, а спорогония в комаре — 8–15 суток.",
        "kartinka": "cikl",
    },
    {
        "tema": "Приступ",
        "vopros": "Чем непосредственно вызван малярийный приступ?",
        "varianty": [
            "Механической закупоркой капилляров заражёнными эритроцитами",
            "Одновременным разрушением множества эритроцитов и выходом мерозоитов в кровь",
            "Выходом мерозоитов из гепатоцитов в кровь",
            "Токсином, который плазмодий выделяет в фазе трофозоита",
        ],
        "verno": 1,
        "razbor": "Приступ привязан к одному моменту цикла: одновременному разрушению эритроцитов, при котором "
                  "в плазму попадают продукты распада и выбрасываются пирогенные цитокины. Ключевое слово — "
                  "«одновременно»: ритм приступов означает, что популяция паразитов синхронизирована.",
    },
    {
        "tema": "Приступ",
        "vopros": "Почему трёхдневная малярия называется трёхдневной, если её цикл — 48 часов?",
        "varianty": [
            "Название описывает длительность приступа: он тянется около трёх суток",
            "При счёте включают оба крайних дня: приступ, свободный день, приступ на третий день",
            "Название отражает трёхфазность приступа: озноб, жар, пот",
            "Это устаревшая ошибка перевода с латыни, содержания в названии нет",
        ],
        "verno": 1,
        "razbor": "Античный счёт включает оба крайних дня. День приступа считают первым, свободный — вторым, "
                  "следующий приступ приходится на третий день: tertiana. При четырёхдневной между приступами "
                  "два свободных дня, и следующий выпадает на четвёртый день: quartana.",
    },
    {
        "tema": "Приступ",
        "vopros": "У больного в фазе озноба холодные руки, цианоз слизистых и «гусиная кожа». Что с температурой тела?",
        "varianty": [
            "Она снижена — отсюда и субъективный холод",
            "Она нормальная, повышение начнётся только в фазе жара",
            "Она может быть уже около 40 °С",
            "Определить нельзя: в фазе озноба измерение недостоверно",
        ],
        "verno": 2,
        "razbor": "В фазе озноба установочная точка терморегуляции резко смещена вверх, и организм воспринимает "
                  "нормальную температуру как низкую: отсюда вазоконстрикция, дрожь и субъективный холод при уже "
                  "растущей температуре. Именно это описал Сенкевич: руки и лоб холодные, а температура страшно высокая.",
    },
    {
        "tema": "Тропическая малярия",
        "vopros": "Почему паразитемия при тропической малярии способна нарастать несопоставимо выше, чем при трёхдневной?",
        "varianty": [
            "P. falciparum заражает эритроциты любого возраста, а P. vivax — преимущественно молодые",
            "Эритроцитарный цикл у P. falciparum короче — 24 часа вместо 48",
            "P. falciparum размножается и в эритроцитах, и в лейкоцитах",
            "У P. falciparum нет иммунного контроля со стороны селезёнки",
        ],
        "verno": 0,
        "razbor": "P. vivax внедряется преимущественно в ретикулоциты, P. malariae — в старые эритроциты; и те и другие "
                  "составляют малую долю эритроцитарной массы, поэтому паразитемия ограничена сама собой. "
                  "Для P. falciparum доступны эритроциты любого возраста.",
    },
    {
        "tema": "Тропическая малярия",
        "vopros": "Больной без сознания, лактат повышен, метаболический ацидоз. Паразитемия в мазке — 20 тыс. в 1 мкл. Как это оценить?",
        "varianty": [
            "Тяжёлой малярии нет: для неё требуется паразитемия свыше 100 тыс. в 1 мкл",
            "Это тяжёлая малярия: пороговое число паразитов для диагноза не обязательно",
            "Диагноз неясен, нужно дождаться роста паразитемии и повторить мазок",
            "Это не малярия: при церебральной малярии паразитемия всегда высокая",
        ],
        "verno": 1,
        "razbor": "Высокая паразитемия — один из самостоятельных признаков угрозы, а не обязательное условие. "
                  "Из-за секвестрации зрелых форм в микроциркуляции паразитемия в мазке недооценивает массу "
                  "паразита; известны смерти от церебральной малярии при очень низкой паразитемии. "
                  "Нарушенное сознание и ацидоз сами по себе означают тяжёлую малярию.",
    },
    {
        "tema": "Осложнения",
        "vopros": "Какое из осложнений малярии может быть вызвано не паразитом, а лечением?",
        "varianty": [
            "Церебральная малярия",
            "Малярийный алгид",
            "Гемоглобинурийная лихорадка",
            "Разрыв селезёнки",
        ],
        "verno": 2,
        "razbor": "Гемоглобинурийная лихорадка — следствие массивного внутрисосудистого гемолиза, который бывает "
                  "и при интенсивной инвазии, и от препаратов (хинин, примахин, сульфаниламиды) у лиц с дефицитом "
                  "Г-6-ФДГ. Паразитов в крови при ней очень мало или нет вовсе, а при быстрой отмене препарата "
                  "состояние улучшается. Именно поэтому перед примахином учитывают дефицит фермента.",
    },
    {
        "tema": "Диагностика",
        "vopros": "Зачем готовят и толстую каплю, и тонкий мазок?",
        "varianty": [
            "Толстая капля — чтобы найти паразита, тонкий мазок — чтобы определить вид",
            "Толстая капля — для вида, тонкий мазок — для подсчёта паразитемии",
            "Толстая капля — для falciparum, тонкий мазок — для остальных видов",
            "Это два названия одного препарата, разница только в способе окраски",
        ],
        "verno": 0,
        "razbor": "В толстой капле объём крови в 30–40 раз больше, поэтому чувствительность выше — она решает задачу "
                  "«найти». Но эритроциты при её приготовлении разрушаются. В тонком мазке они лежат одним слоем, "
                  "и морфология стадий различима — он решает задачу «определить вид». Определение вида обязательно.",
    },
    {
        "tema": "Диагностика",
        "vopros": "Экспресс-тест на малярию отрицательный, но клиника и эпиданамнез убедительны. Что верно?",
        "varianty": [
            "Диагноз снят: чувствительность современных тестов близка к 100 %",
            "Нужно повторить тест через сутки и при повторном отрицательном результате диагноз снять",
            "Отрицательный тест диагноз не снимает, в том числе из-за мутаций с потерей HRP2 и HRP3",
            "Тест недостоверен всегда, ориентироваться следует только на клинику",
        ],
        "verno": 2,
        "razbor": "Большинство экспресс-тестов распознают антигены HRP2 и HRP3, а у части паразитов мутации не дают "
                  "этим белкам экспрессироваться — такой возбудитель тестом не выявляется. В 2024 году мутации "
                  "регистрировались в 42 странах, а в шести превысили 15 %. Экспресс-тест дополняет микроскопию, "
                  "а не заменяет её.",
    },
    {
        "tema": "Диагностика",
        "vopros": "Больной поступил на третий день болезни: лихорадка есть, селезёнка не увеличена, анемии нет. Как это влияет на версию малярии?",
        "varianty": [
            "Диагноз маловероятен: классическая триада неполна",
            "Диагноз остаётся вероятным: селезёнка увеличивается после 2–3 приступов, анемия — со второй недели",
            "Диагноз возможен только для четырёхдневной малярии",
            "Диагноз исключается, если селезёнка не увеличена при повторном осмотре через час",
        ],
        "verno": 1,
        "razbor": "Опираться на полноту триады нельзя: печень и селезёнка отчётливо увеличиваются только после "
                  "2–3 приступов, анемия развивается со второй недели. На третий день тропической малярии из триады "
                  "может быть одна лихорадка — и это та форма, которая убивает быстрее всех.",
    },
    {
        "tema": "Лечение",
        "vopros": "Больной с трёхдневной малярией получил курс хлорохина, приступы прекратились, паразиты из крови исчезли. Зачем ему ещё 14 дней примахина?",
        "varianty": [
            "Чтобы добить гаметоциты и сделать больного незаразным для комаров",
            "Чтобы предупредить устойчивость к хлорохину",
            "Чтобы уничтожить гипнозоиты в печени и предотвратить отдалённый рецидив",
            "Чтобы восстановить эритроциты и вылечить анемию",
        ],
        "verno": 2,
        "razbor": "Хлорохин действует на эритроцитарные стадии и до печени не достаёт. Гипнозоиты остаются, "
                  "и без гистошизотропного препарата болезнь вернётся через 6–8 месяцев, иногда через 1–3 года. "
                  "Такое лечение называют радикальным — в отличие от купирования приступа.",
    },
    {
        "tema": "Лечение",
        "vopros": "Почему производные артемизинина назначают в комбинации, а не отдельно?",
        "varianty": [
            "Отдельно они не действуют на гаметоциты",
            "Они быстро выводятся, и при монотерапии возникают рецидивы",
            "Отдельно они слишком токсичны, комбинация позволяет снизить дозу",
            "Комбинация нужна только там, где есть устойчивость к хлорохину",
        ],
        "verno": 1,
        "razbor": "Препараты артемизинина действуют очень быстро и на кровяные стадии, и на гаметоциты, но быстро "
                  "выводятся из организма — при монотерапии возникают рецидивы. Отсюда и само понятие комбинированной "
                  "терапии на основе артемизинина, которую ВОЗ называет наиболее эффективным методом лечения "
                  "falciparum-малярии.",
    },
    {
        "tema": "Геном",
        "vopros": "Почему P. vivax не встречается у коренных жителей Западной Африки?",
        "varianty": [
            "Там слишком жарко для спорогонии P. vivax",
            "Там нет подходящих видов Anopheles",
            "На эритроцитах отсутствуют антигены Даффи — рецептор для мерозоитов P. vivax",
            "P. falciparum вытесняет P. vivax из-за более короткого цикла",
        ],
        "verno": 2,
        "razbor": "Мерозоиту P. vivax для проникновения в эритроцит нужен рецептор — изоантигены Даффи. У коренных "
                  "жителей Западной Африки их нет, и вид там просто не встречается. Это объясняет географическую "
                  "странность: самый распространённый в мире плазмодий отсутствует в регионе с самой тяжёлой малярией.",
    },
    {
        "tema": "Приезжий",
        "vopros": "Взрослый житель эндемичного района и турист имеют одинаковую паразитемию. Почему прогноз у них разный?",
        "varianty": [
            "У приезжих обычно другой вид плазмодия",
            "У местного жителя есть приобретённый иммунитет, у неиммунного приезжего его нет",
            "У приезжих хуже переносимость противомалярийных препаратов",
            "Разницы нет: тяжесть определяется только уровнем паразитемии",
        ],
        "verno": 1,
        "razbor": "В гиперэндемичных очагах у взрослых паразит обнаруживается редко, а при инфицировании клинических "
                  "проявлений может не быть вовсе — сказывается приобретённый иммунитет. У приезжего иммунитета нет, "
                  "поэтому та же паразитемия для него опасна. Неиммунные путешественники стоят в группах риска рядом "
                  "с детьми до пяти лет и беременными.",
    },
    {
        "tema": "История",
        "vopros": "Какое рассуждение привело Баттиста Грасси к переносчику малярии?",
        "varianty": [
            "Малярия есть всюду, где есть комары, значит переносчик — комар",
            "Комары без малярии бывают, малярии без комаров не бывает — значит виноват один определённый вид",
            "Малярия отступает после осушения болот, значит дело в болотном воздухе",
            "Комары кусают ночью, а приступы начинаются утром — значит цикл занимает часы",
        ],
        "verno": 1,
        "razbor": "Наблюдение «комары есть, малярии нет» само по себе выглядит опровержением комариной теории, "
                  "а «малярии без комаров не бывает» её поддерживает. Вместе они дают вывод, которого не даёт ни одно "
                  "по отдельности: переносчик — не комары вообще, а один конкретный вид. Им оказался Anopheles claviger, "
                  "которого местные жители называли «занзароне».",
    },
    {
        "tema": "История",
        "vopros": "Что в рецепте Гэ Хуна подсказало Ту Юю способ выделения артемизинина?",
        "varianty": [
            "Указание кипятить траву дольше обычного",
            "Отсутствие указания нагревать: сок предписывалось выжать",
            "Точная дозировка в двух шэн воды",
            "Указание использовать корень, а не листья",
        ],
        "verno": 1,
        "razbor": "Почти все травяные снадобья готовили отваром, то есть кипятили. Гэ Хун нагревать не велел — "
                  "он велел выжать сок. Ту Юю предположила, что нагревание разрушает действующее вещество, и перешла "
                  "к экстракции при пониженной температуре этиловым эфиром. 4 октября 1971 года образец № 191 показал "
                  "полное подавление малярии у грызунов. Подсказкой оказалась технологическая мелочь.",
    },
]


# --- сборка ---------------------------------------------------------------

def sobrat() -> None:
    kartinki = {
        "komar": v_base64(KARTINKI / "komar_anopheles.jpg", "image/jpeg"),
        "cikl": v_base64(KARTINKI / "cikl_malyarii.png", "image/png"),
    }
    podpisi = {
        "komar": "Самка Anopheles gambiae во время питания кровью. "
                 "CDC / James Gathany, общественное достояние",
        "cikl": "Жизненный цикл малярийного плазмодия. Bbkkk, Wikimedia Commons, "
                "CC BY-SA 4.0, подписи переведены",
    }

    dannye = json.dumps(
        {"voprosy": VOPROSY, "kartinki": kartinki, "podpisi": podpisi},
        ensure_ascii=False,
    )

    CEL.write_text(SHABLON.replace("__DANNYE__", dannye), encoding="utf-8")
    razmer = CEL.stat().st_size / 1024
    print(f"{CEL.name} — {len(VOPROSY)} вопросов, {razmer:.0f} КБ")


SHABLON = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0d1117">
<title>Малярия — тест по материалу</title>
<style>
:root{
  --bg:#0d1117; --panel:#151b23; --panel2:#1b232d;
  --line:#26303c; --txt:#e6edf3; --muted:#8ea0b3; --dim:#5c6b7c;
  --ok:#37d39a; --bad:#ff6b6b; --warn:#f7b955; --accent:#38bdf8;
  --mint:#a9d7c6; --green:#0d8f76;
  --r:14px;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{
  background:
    radial-gradient(1200px 600px at 15% -10%, #16202b 0%, transparent 60%),
    radial-gradient(900px 500px at 110% 10%, #10202c 0%, transparent 55%),
    var(--bg);
  color:var(--txt);
  font:15.5px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,"Helvetica Neue",Arial,sans-serif;
  -webkit-font-smoothing:antialiased;
  padding:0 0 70px;
}
h1,h2,h3{margin:0;font-weight:650;letter-spacing:-.01em}
button{font:inherit;color:inherit;cursor:pointer;border:0;background:none}
.wrap{max-width:820px;margin:0 auto;padding:0 18px}

.hero{
  border-bottom:1px solid var(--line);
  background:linear-gradient(180deg,rgba(13,143,118,.12),transparent 70%);
  padding:24px 0 20px;margin-bottom:22px;
}
.hero h1{font-size:24px;line-height:1.2}
.hero h1 span{color:var(--mint)}
.hero p{margin:8px 0 0;color:var(--muted);font-size:14px}

/* прогресс */
.progress{display:flex;align-items:center;gap:12px;margin:0 0 18px}
.pbar{flex:1;height:6px;border-radius:100px;background:var(--panel2);overflow:hidden}
.pbar i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--green),var(--mint));transition:width .25s}
.pnum{font-size:13px;color:var(--muted);white-space:nowrap;font-variant-numeric:tabular-nums}

.card{
  background:var(--panel);border:1px solid var(--line);border-radius:var(--r);
  padding:20px 20px 18px;
}
.tema{
  display:inline-block;font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;
  color:var(--mint);background:rgba(13,143,118,.16);border:1px solid rgba(169,215,198,.22);
  padding:3px 10px;border-radius:100px;margin-bottom:12px;
}
.vopros{font-size:17.5px;font-weight:600;line-height:1.4;margin:0 0 6px}

figure{margin:14px 0 4px;text-align:center}
figure img{max-width:100%;border-radius:10px;border:1px solid var(--line);display:block;margin:0 auto}
figcaption{font-size:12px;color:var(--dim);margin-top:7px;text-align:left}

.varianty{display:flex;flex-direction:column;gap:9px;margin-top:16px}
.var{
  display:flex;gap:12px;align-items:flex-start;text-align:left;width:100%;
  padding:12px 14px;border-radius:11px;
  border:1px solid var(--line);background:var(--panel2);
  transition:.14s;line-height:1.45;
}
.var:hover:not(:disabled){border-color:var(--mint);background:#202b36}
.var:disabled{cursor:default}
.var .bukva{
  flex:0 0 24px;height:24px;border-radius:7px;display:grid;place-items:center;
  font-size:12.5px;font-weight:700;background:#26303c;color:var(--muted);
}
.var.verno{border-color:var(--ok);background:rgba(55,211,154,.10)}
.var.verno .bukva{background:var(--ok);color:#08150f}
.var.nerno{border-color:var(--bad);background:rgba(255,107,107,.10)}
.var.nerno .bukva{background:var(--bad);color:#1a0b0b}

.razbor{
  margin-top:16px;padding:13px 15px;border-radius:11px;
  background:rgba(56,189,248,.07);border-left:3px solid var(--accent);
  font-size:14.5px;line-height:1.55;color:#cfe0ee;
}
.razbor b{color:var(--txt)}

.nav{display:flex;justify-content:flex-end;margin-top:18px}
.knopka{
  padding:11px 22px;border-radius:10px;font-weight:650;font-size:15px;
  background:var(--green);color:#eafff8;transition:.14s;
}
.knopka:hover{background:#0fa588}
.knopka.prizrak{background:transparent;border:1px solid var(--line);color:var(--muted)}
.knopka.prizrak:hover{border-color:var(--mint);color:var(--txt)}

/* итог */
.itog{text-align:center;padding:30px 20px}
.procent{font-size:64px;font-weight:750;line-height:1;letter-spacing:-.03em}
.procent.a{color:var(--ok)} .procent.b{color:var(--mint)}
.procent.c{color:var(--warn)} .procent.d{color:var(--bad)}
.itog .schet{margin-top:10px;color:var(--muted);font-size:15px}
.verdikt{margin:18px auto 0;max-width:560px;font-size:15.5px;line-height:1.55}
.po-temam{margin:26px auto 0;max-width:560px;text-align:left}
.po-temam h3{font-size:14px;color:var(--muted);font-weight:600;margin-bottom:10px;
  text-transform:uppercase;letter-spacing:.05em}
.tstroka{display:flex;align-items:center;gap:11px;padding:7px 0;border-top:1px solid var(--line);font-size:14.5px}
.tstroka .imya{flex:1}
.tstroka .ball{font-variant-numeric:tabular-nums;color:var(--muted);font-size:13.5px}
.tstroka .tbar{flex:0 0 84px;height:5px;border-radius:100px;background:var(--panel2);overflow:hidden}
.tstroka .tbar i{display:block;height:100%;background:var(--mint)}
.itog-nav{display:flex;gap:10px;justify-content:center;margin-top:28px;flex-wrap:wrap}

.razbor-vse{margin-top:34px;text-align:left}
.razbor-vse h3{font-size:14px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:14px}
.ritem{border:1px solid var(--line);border-radius:11px;padding:14px 16px;margin-bottom:10px;background:var(--panel)}
.ritem .rq{font-weight:600;line-height:1.45}
.ritem .rmeta{display:flex;gap:8px;align-items:center;margin-bottom:8px}
.znak{flex:0 0 20px;height:20px;border-radius:6px;display:grid;place-items:center;font-size:12px;font-weight:700}
.znak.v{background:var(--ok);color:#08150f} .znak.n{background:var(--bad);color:#1a0b0b}
.ritem .rotv{margin-top:8px;font-size:14px;color:var(--muted)}
.ritem .rotv b{color:var(--ok);font-weight:600}
.ritem .rotv .moy{color:var(--bad);font-weight:600}
.ritem .rraz{margin-top:9px;font-size:14px;line-height:1.55;color:#cfe0ee}

.podval{margin-top:34px;padding-top:16px;border-top:1px solid var(--line);
  color:var(--dim);font-size:12.5px;line-height:1.6}
.podval a{color:var(--muted)}

@media(max-width:560px){
  .hero h1{font-size:20px}
  .vopros{font-size:16.5px}
  .procent{font-size:52px}
  .card{padding:16px 15px 15px}
}
</style>
</head>
<body>

<div class="hero"><div class="wrap">
  <h1>Малярия — <span>тест по материалу</span></h1>
  <p><span id="skolko"></span> Ответ виден сразу, с разбором; итог с процентами — в конце.
     Серия «Крещение поворотом».</p>
</div></div>

<div class="wrap">
  <div class="progress" id="progress">
    <div class="pbar"><i id="pbar"></i></div>
    <div class="pnum" id="pnum"></div>
  </div>
  <div id="ekran"></div>
  <div class="podval">
    Тест по учебному материалу «Малярия» серии «Крещение поворотом». Текст — CC BY-NC-SA 4.0.
    Иллюстрации: схема цикла — Bbkkk, Wikimedia Commons, CC BY-SA 4.0, подписи переведены;
    фотография переносчика — CDC / James Gathany, общественное достояние.
    Материал учебный: не заменяет протоколы и клинические рекомендации.
  </div>
</div>

<script>
const D = __DANNYE__;
const V = D.voprosy;
const BUKVY = ["А","Б","В","Г","Д"];

let i = 0;              // текущий вопрос
let otvety = [];        // выбранный индекс (в исходной нумерации вариантов)
let otvechen = false;   // на текущий вопрос уже ответили
let poryadok = [];      // порядок показа вариантов по каждому вопросу

/* Варианты показываются в случайном порядке: иначе правильный ответ
   распределён по буквам неравномерно и тест проходится без чтения вопросов.
   Заодно повторное прохождение перестаёт быть проверкой памяти на буквы. */
function peremeshat(){
  poryadok = V.map(function(q){
    const a = q.varianty.map(function(_, n){ return n; });
    for (let k = a.length - 1; k > 0; k--){
      const j = Math.floor(Math.random() * (k + 1));
      const t = a[k]; a[k] = a[j]; a[j] = t;
    }
    return a;
  });
}

document.getElementById("skolko").textContent =
  "Вопросов: " + V.length + ".";

const ekran = document.getElementById("ekran");
const pbar = document.getElementById("pbar");
const pnum = document.getElementById("pnum");
const progress = document.getElementById("progress");

function ekranirovat(s){
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

function obnovitProgress(){
  progress.style.display = "flex";
  pbar.style.width = (i / V.length * 100) + "%";
  pnum.textContent = "Вопрос " + (i + 1) + " из " + V.length;
}

function pokazatVopros(){
  const q = V[i];
  obnovitProgress();
  otvechen = otvety[i] !== undefined;

  let kart = "";
  if (q.kartinka){
    kart = '<figure><img src="' + D.kartinki[q.kartinka] + '" alt="">' +
           '<figcaption>' + ekranirovat(D.podpisi[q.kartinka]) + '</figcaption></figure>';
  }

  let varianty = poryadok[i].map(function(orig, poz){
    return '<button class="var" data-n="' + orig + '">' +
           '<span class="bukva">' + BUKVY[poz] + '</span>' +
           '<span>' + ekranirovat(q.varianty[orig]) + '</span></button>';
  }).join("");

  ekran.innerHTML =
    '<div class="card">' +
      '<span class="tema">' + ekranirovat(q.tema) + '</span>' +
      '<p class="vopros">' + ekranirovat(q.vopros) + '</p>' +
      kart +
      '<div class="varianty" id="varianty">' + varianty + '</div>' +
      '<div id="posle"></div>' +
    '</div>';

  document.querySelectorAll("#varianty .var").forEach(function(b){
    b.addEventListener("click", function(){ otvetit(+b.dataset.n); });
  });

  if (otvechen) pokazatRazbor();
  window.scrollTo({top:0, behavior:"smooth"});
}

function otvetit(n){
  if (otvechen) return;
  otvety[i] = n;
  otvechen = true;
  pokazatRazbor();
}

function pokazatRazbor(){
  const q = V[i];
  const moy = otvety[i];
  document.querySelectorAll("#varianty .var").forEach(function(b){
    const n = +b.dataset.n;
    b.disabled = true;
    if (n === q.verno) b.classList.add("verno");
    else if (n === moy) b.classList.add("nerno");
  });
  const verno = moy === q.verno;
  document.getElementById("posle").innerHTML =
    '<div class="razbor"><b>' + (verno ? "Верно. " : "Неверно. ") + '</b>' +
    ekranirovat(q.razbor) + '</div>' +
    '<div class="nav"><button class="knopka" id="dalshe">' +
    (i + 1 < V.length ? "Дальше" : "Показать результат") + '</button></div>';
  document.getElementById("dalshe").addEventListener("click", function(){
    if (i + 1 < V.length){ i++; pokazatVopros(); } else { pokazatItog(); }
  });
}

function pokazatItog(){
  progress.style.display = "none";
  const vsego = V.length;
  let verno = 0;
  V.forEach(function(q, n){ if (otvety[n] === q.verno) verno++; });
  const pc = Math.round(verno / vsego * 100);

  let klass, verdikt;
  if (pc >= 90){
    klass = "a";
    verdikt = "Материал разобран. Механизмы, а не только формулировки: видно, что цикл " +
              "используется как объяснение, а не заучен.";
  } else if (pc >= 75){
    klass = "b";
    verdikt = "Хороший результат. Пробелы точечные — посмотрите разбор ниже по тем вопросам, " +
              "где ответ разошёлся.";
  } else if (pc >= 50){
    klass = "c";
    verdikt = "Основа есть, но половина ошибок обычно приходится на выводы из цикла: сроки инкубации, " +
              "смысл ритма лихорадки и роль печени. Эти разделы стоит перечитать.";
  } else {
    klass = "d";
    verdikt = "Стоит вернуться к материалу и начать с раздела о жизненном цикле: из него выводятся " +
              "и сроки, и ритм лихорадки, и логика лечения. Остальное после этого запоминать почти не нужно.";
  }

  // разбивка по темам
  const temy = {};
  V.forEach(function(q, n){
    if (!temy[q.tema]) temy[q.tema] = {v:0, vsego:0};
    temy[q.tema].vsego++;
    if (otvety[n] === q.verno) temy[q.tema].v++;
  });
  let stroki = Object.keys(temy).map(function(t){
    const o = temy[t];
    const p = Math.round(o.v / o.vsego * 100);
    return '<div class="tstroka"><span class="imya">' + ekranirovat(t) + '</span>' +
           '<span class="tbar"><i style="width:' + p + '%"></i></span>' +
           '<span class="ball">' + o.v + " / " + o.vsego + '</span></div>';
  }).join("");

  // подробный разбор
  let razbory = V.map(function(q, n){
    const moy = otvety[n];
    const ok = moy === q.verno;
    let stroka = '<div class="rotv"><b>Верно: ' + ekranirovat(q.varianty[q.verno]) + '</b>';
    if (!ok){
      stroka += '<br><span class="moy">Ваш ответ: ' +
                (moy === undefined ? "не отвечено" : ekranirovat(q.varianty[moy])) + '</span>';
    }
    stroka += '</div>';
    return '<div class="ritem">' +
      '<div class="rmeta"><span class="znak ' + (ok ? "v" : "n") + '">' + (ok ? "✓" : "✕") + '</span>' +
      '<span class="tema" style="margin:0">' + ekranirovat(q.tema) + '</span></div>' +
      '<div class="rq">' + (n + 1) + ". " + ekranirovat(q.vopros) + '</div>' +
      stroka + '<div class="rraz">' + ekranirovat(q.razbor) + '</div></div>';
  }).join("");

  ekran.innerHTML =
    '<div class="card itog">' +
      '<div class="procent ' + klass + '">' + pc + '%</div>' +
      '<div class="schet">' + verno + " из " + vsego + " верно</div>" +
      '<div class="verdikt">' + verdikt + '</div>' +
      '<div class="po-temam"><h3>По разделам</h3>' + stroki + '</div>' +
      '<div class="itog-nav">' +
        '<button class="knopka" id="snova">Пройти заново</button>' +
        '<button class="knopka prizrak" id="oshibki">Показать только ошибки</button>' +
      '</div>' +
    '</div>' +
    '<div class="razbor-vse" id="razborVse"><h3>Разбор всех вопросов</h3>' + razbory + '</div>';

  document.getElementById("snova").addEventListener("click", function(){
    i = 0; otvety = []; peremeshat(); pokazatVopros();
  });

  let tolkoOshibki = false;
  document.getElementById("oshibki").addEventListener("click", function(){
    tolkoOshibki = !tolkoOshibki;
    this.textContent = tolkoOshibki ? "Показать все вопросы" : "Показать только ошибки";
    document.querySelectorAll("#razborVse .ritem").forEach(function(el){
      const ok = el.querySelector(".znak").classList.contains("v");
      el.style.display = (tolkoOshibki && ok) ? "none" : "";
    });
  });

  window.scrollTo({top:0, behavior:"smooth"});
}

peremeshat();
pokazatVopros();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    sobrat()
