# Dependency Graph Visualizer (Variant 25)

Инструмент командной строки на чистом Python для анализа и построения графа зависимостей пакетов Ubuntu (apt).

## Требования
* Python 3.8+
* PyYAML

## Структура проекта
* `src/main.py` — основной исполняемый файл приложения.
* `config.yaml` — файл конфигурации параметров запуска.
* `test_graph.txt` — тестовый файл графа для режима тестирования.
* `run.sh` — скрипт быстрой сборки и запуска.
* `tests/` — директория для тестов.

## Конфигурация (`config.yaml`)
Пример параметров:
```yaml
package_name: "A"
repository_url: "test_graph.txt"
test_mode: true
package_version: "1.0.0"
output_image: "graph.png"
ascii_tree: false
max_depth: 3

## Запуск
bash
./run.sh