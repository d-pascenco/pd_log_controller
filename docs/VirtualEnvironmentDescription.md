### Установка виртуального окружения

### 1. Проверка

a. Если есть старое окружение, то удаляем его

```bash
rm -rf название_окружения
```

b. Далее проверить, какое окружение используется (системное или виртуальное, если оно есть)
```bash
which python
which pip
python -m pip --version
```
Если вывод будет вида:
```text
/usr/bin/python
/usr/bin/pip
pip 26.1.1 from /usr/lib/python3.14/site-packages/pip (python 3.14)
```
Значит нужно инициализировать новое:
```bash
python -m venv .venv
source .venv/bin/activate
```
Запрашиваем версию:
```bash
python --version
```

Команда `source .venv/bin/activate` активирует окружение
Команда `deactivate` - деактивирует его