## Описание используемых библиотек и основных их функций

### 1. Pathlib

Встроенная библиотека Python.
До неё использовали os
```python
import os
os.path.join(...)
os.path.exists(...)
os.listdir(...)
```
...НО pathlib делает это чище, безопаснее и удобнее.
Docs: https://docs.python.org/3/library/pathlib.html
Назначение: удобный способ работать с путями к файлам и папкам в Python.
Основная идея: путь — это объект.
`path = Path("/home/pd/project")` - теперь это объект с методами.

* a. Построение путей: `Path("data") / "raw" / "file.csv"`
* b. Получение текущей директории файла: `BASE_DIR = Path(__file__).resolve().parent`
* c. проверка существования файла: `path.exists()`
* d. Проверка файла: `path.is_file()`
* e. Проверка папки: `path.is_dir()`
* f. Создание папок: `Path('logs').mkdir()` (с вложенными папками `Path("data/raw").mkdir(parents=True, exist_ok=True)`)
* g. Чтение файлы: `path.read_text()` (json-файлов `import json ,, data = json.loads(path.read_text())`)
* h. Запись файлов: `path.write_text('hello')`
* i. Получение имени файла: `path.name`
* j. Имя без разширения: `path.stem`
* k. Расширение файла: `path.suffix`
* l. Родительская директория: `path.parent`
* m. Перебор файлов: `for file in Path("logs").iterdir(): ,, print(file)`
* n. Рекурсивный поиск: `Path("logs").rglob("*.log")`
* o. Абсолютный путь: `path.resolve()`
* p. Удаление файлов: `path.unlink()` (папки `path.rmdir()`)
* q. Работа с расширениями: `path.with_suffix(".json")`

### 2. Pandas
### 3. Numpy
### 4. Matplotlib