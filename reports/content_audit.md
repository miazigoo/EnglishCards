# Отчет аудита контента baseline cards.json (1529 карточек)

- **Всего карточек проверено:** 1529
- **Карточек с шаблонными заметками («ключевая сущность / паттерн»):** 682 (44.6%)
- **Карточек со смешанной латиницей/кириллицей в транскрипции:** 603
- **Карточек с фиктивной IPA транскрипцией:** 202
- **Карточек с ошибками в коде:** 7
- **Требуют исправления/обогащения:** 966

## Ключевые дефекты эталонных карточек

1. **`rsplit()` (ID 45):** содержит `RsplitService` и псевдо-IPA `/rsplit/`. Требует разбора `right + split` («разделить справа»), сравнения с `split()` и сохранения порядка результата слева направо.
2. **`zip()` (ID 1):** переводится только как «сшивает итераторы». Требует ясного объяснения попарного объединения по позициям и примера с именами и оценками.
3. **`issubclass()` (ID 4):** содержит `IssubclassService`. Требует реальных классов `Animal`/`Dog` и проверки наследования.
4. **`getattr()` (ID 6):** содержит вызов `getattr(order, field_name, default=0.0)` с запрещенным именованным аргументом. Требует позиционного аргумента `getattr(order, 'total_weight', 0.0)`.
5. **`filter()` (ID 17):** смешивает `python.builtins.filter` и `QuerySet.filter`. Требует разделения на две самостоятельные единицы.

## Пример записей с замечаниями

| ID | Термин | Категория | Действие | Замечания |
| :---: | :--- | :--- | :---: | :--- |
| 1 | `enumerate()` | Python: встроенные методы и функции | **fix** | mixed_script_ru_transcription: 'инuмерэйт' |
| 2 | `zip()` | Python: встроенные методы и функции | **fix** | zip_needs_positional_pairing_explanation |
| 3 | `isinstance()` | Python: встроенные методы и функции | **fix** | mixed_script_ru_transcription: 'iсiнстaнce', bogus_literal_ipa: '/isinstance/' |
| 4 | `issubclass()` | Python: встроенные методы и функции | **fix** | template_example_note, mixed_script_ru_transcription: 'iссuбcлaсс', bogus_literal_ipa: '/issubclass/', issubclass_needs_animal_dog_inheritance_example |
| 5 | `hasattr()` | Python: встроенные методы и функции | **fix** | mixed_script_ru_transcription: 'хaсaттр', bogus_literal_ipa: '/hasattr/' |
| 6 | `getattr()` | Python: встроенные методы и функции | **fix** | mixed_script_ru_transcription: 'гeтaттр', bogus_literal_ipa: '/getattr/', code_issue: getattr() uses illegal keyword argument 'default=', getattr_has_keyword_arg_error |
| 7 | `setattr()` | Python: встроенные методы и функции | **fix** | mixed_script_ru_transcription: 'сeтaттр', bogus_literal_ipa: '/setattr/' |
| 8 | `delattr()` | Python: встроенные методы и функции | **fix** | template_example_note, mixed_script_ru_transcription: 'дeлaттр', bogus_literal_ipa: '/delattr/' |
| 9 | `callable()` | Python: встроенные методы и функции | **fix** | template_example_note |
| 10 | `iter()` | Python: встроенные методы и функции | **fix** | template_example_note, mixed_script_ru_transcription: 'iтeр', bogus_literal_ipa: '/iter/' |
| 11 | `next()` | Python: встроенные методы и функции | **fix** | template_example_note |
| 12 | `all()` | Python: встроенные методы и функции | **fix** | template_example_note |
| 13 | `any()` | Python: встроенные методы и функции | **fix** | template_example_note, mixed_script_ru_transcription: 'энi' |
| 14 | `sorted()` | Python: встроенные методы и функции | **fix** | template_example_note |
| 15 | `reversed()` | Python: встроенные методы и функции | **fix** | template_example_note |
| 16 | `map()` | Python: встроенные методы и функции | **fix** | template_example_note |
| 17 | `filter()` | Python: встроенные методы и функции | **split** | filter_needs_builtin_vs_queryset_separation |
| 18 | `sum()` | Python: встроенные методы и функции | **fix** | template_example_note |
| 19 | `min()` | Python: встроенные методы и функции | **fix** | template_example_note |
| 20 | `max()` | Python: встроенные методы и функции | **fix** | template_example_note |
| 21 | `abs()` | Python: встроенные методы и функции | **fix** | template_example_note, mixed_script_ru_transcription: 'эйбiэс' |
| 22 | `round()` | Python: встроенные методы и функции | **fix** | template_example_note |
| 23 | `divmod()` | Python: встроенные методы и функции | **fix** | template_example_note, mixed_script_ru_transcription: 'дiвмoд', bogus_literal_ipa: '/divmod/' |
| 24 | `pow()` | Python: встроенные методы и функции | **fix** | template_example_note |
| 25 | `slice()` | Python: встроенные методы и функции | **fix** | template_example_note |
| 26 | `repr()` | Python: встроенные методы и функции | **fix** | template_example_note |
| 27 | `eval()` | Python: встроенные методы и функции | **fix** | template_example_note, mixed_script_ru_transcription: 'eвaл', bogus_literal_ipa: '/eval/' |
| 28 | `exec()` | Python: встроенные методы и функции | **fix** | template_example_note |
| 29 | `breakpoint()` | Python: встроенные методы и функции | **fix** | template_example_note, mixed_script_ru_transcription: 'брeaкпoiнт', bogus_literal_ipa: '/breakpoint/' |
| 30 | `hash()` | Python: встроенные методы и функции | **fix** | template_example_note |
