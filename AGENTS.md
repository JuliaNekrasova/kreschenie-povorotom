# AGENTS.md

Проект **«Крещение поворотом»** — статический сайт на Jekyll (GitHub Pages) с
учебными материалами для скорой помощи. Кроме сайта в репозитории есть Python-
конвейер сборки PDF и автономные интерактивные HTML-тренажёры.

## Cursor Cloud specific instructions

Среда уже настроена стартовым скриптом (Ruby 3.2, `github-pages` gem через
bundler, Python 3.12, `pandoc`, `weasyprint`, `poppler-utils`). Ниже —
неочевидные моменты для запуска/разработки.

### Компоненты и как их запускать

| Компонент | Что это | Как запустить локально |
| --- | --- | --- |
| Сайт (Jekyll / GitHub Pages) | Главный продукт; `index` собирается из `README.md`, тема `jekyll-theme-primer` | `bundle3.2 exec jekyll serve --host 0.0.0.0 --port 4000 --livereload` |
| Сборка PDF | `_tools/sobrat.py` собирает PDF из `<папка>/razbor.md` через pandoc + weasyprint | `python3 _tools/sobrat.py [имя_папки ...]` (без аргументов — все материалы) |
| Гайды тренажёров | `trenazhery/*/guide/sobrat_guide.py` — сборка + проверка гайда | `python3 trenazhery/<тренажёр>/guide/sobrat_guide.py` |
| Тренажёры | Автономные HTML-файлы `trenazhery/*/*_trenazher.html`, вся логика внутри | Открыть напрямую или через dev-сервер |

### Неочевидные моменты

- **`bundle`/`jekyll` называются `bundle3.2`.** Ubuntu ставит бинарь как
  `bundle3.2` (плюс `~/.local/share/gem/ruby/3.2.0/bin` добавлен в PATH в
  `~/.bashrc`). В неинтерактивных скриптах используйте `bundle3.2 exec jekyll …`.
- **Плагины GitHub Pages подключает Gemfile, а не `_config.yml`.** Тэги
  `{% seo %}` и `{% github_edit_link %}` и переменные `site.github.*` работают
  только через `bundle exec` с `github-pages` в группе `:jekyll_plugins`. Локальный
  `Gemfile` нужен исключительно для локальной сборки — прод GitHub Pages его
  игнорирует и собирает своим окружением.
- **Предупреждение `GitHub Metadata: No GitHub API authentication` при сборке —
  норма.** Без токена `jekyll-github-metadata` подставляет значения по умолчанию;
  на сборку сайта это не влияет.
- **`_site/` — артефакт сборки, не коммитить** (уже в `.gitignore`).
- **`sobrat.py` перезаписывает PDF рядом с исходником.** После тестовой пересборки
  бинарники PDF меняются (метаданные/время) — восстанавливайте их
  `git checkout -- <pdf>`, чтобы не коммитить лишние диффы.
- **`razbor.md` — единственный источник материала**; HTML-версия статьи
  намеренно не собирается (ломается типографика), только PDF формата A4.
