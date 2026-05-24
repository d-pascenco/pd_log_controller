# Полный воркфлоу подготовки хоста

## Overview

В рамках проекта создан хост на Oracle Cloud Free Tier, SSH.
Ниже описана подробная последовательность действий.

## 1. Создание инстанса в Oracle Cloud

### 1.1 Создание инстанса

В Oracle Cloud Console:
- `Compute`
- `Instances`
- `Create Instance`

### 1.2 Параметры инстанса

При создании были выбраны следующие параметры:
- **Shape:** `VM.Standard.E2.1.Micro`
- **Image:** `RESF-Rocky-9-x86_64-Base-9.6-20250827`
- **Public IP:** включён
- **SSH key:** загружен при создании инстанса

## 2. Настройка сети Oracle Cloud

После создания нового инстанса потребовалась ручная проверка сетевой конфигурации.

### 2.1 Security List

В Security List были настроены входящие правила.

#### Ingress Rules

| Source     | Protocol | Destination Port | Назначение |
|------------|----------|------------------|------------|
| 0.0.0.0/0  | TCP      | 22               | SSH        |
| 0.0.0.0/0  | TCP      | 80               | HTTP       |
| 0.0.0.0/0  | TCP      | 443              | HTTPS      |
| 0.0.0.0/0  | TCP      | 8501             | Streamlit  |
| 0.0.0.0/0  | TCP      | 8000             | FastAPI    |
| 0.0.0.0/0  | TCP      | 5432             | PostgreSQL |

### 2.2 Проверка подсети

Подсеть из коробки имела параметры:
- тип: `Public Subnet`
- CIDR: `10.0.0.0/24`
Это означало, что инстанс может использовать публичный доступ, 
но только при наличии правильного маршрута через Internet Gateway.

### 2.3 Internet Gateway

Для VCN был создан Internet Gateway.
Путь в интерфейсе:
- `Networking`
- `Virtual Cloud Networks`
- выбрать VCN
- `Internet Gateway`
- `Create Internet Gateway`

### 2.4 Route Table

В `Default Route Table` было добавлено правило:
- **Destination CIDR block:** `0.0.0.0/0`
- **Target Type:** `Internet Gateway`

Без этого правила внешний трафик до инстанса не дойдет.

### 2.5 Firewall (Rocky Linux)
На хосте используется Rocky Linux, поэтому для управления firewall используется `firewalld`.

Установка `firewalld`:
```bash
sudo dnf install firewalld -y
```

Запуск и добавление в автозагрузку:
```bash
sudo systemctl enable --now firewalld
```

Проверка состояния:
```bash
sudo firewall-cmd --state
```

Ожидаемый вывод:
```text
running
```

В дальнейшем на хосте открыть вышеперечисленные порты можно через следующие команды:

```bash
sudo firewall-cmd --permanent --add-port=22/tcp
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --permanent --add-port=8501/tcp
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --permanent --add-port=5432/tcp
```

Применить изменения:
```bash
sudo firewall-cmd --reload
```

Проверка открытых портов внутри сервера:
```bash
sudo firewall-cmd --list-ports
```

Ожидаемый вывод будет примерно таким:
```text
22/tcp 80/tcp 443/tcp 8501/tcp 8000/tcp
```

Посмотреть полную конфигурацию firewall:
```bash
sudo firewall-cmd --list-all
```

Важно: открыть порт в `firewalld` недостаточно. В Oracle Cloud этот же порт должен быть открыт в `Security List` или `Network Security Group`.

### 2.6 Сохранение firewall-правил после перезагрузки
На Rocky Linux при использовании `firewalld` правила с параметром `--permanent` сохраняются автоматически и переживают перезагрузку.

Проверяю, что `firewalld` включён в автозагрузку:
```bash
sudo systemctl is-enabled firewalld
```
Ожидаемый вывод:
```text
enabled
```
Проверка состояния сервиса:
```bash
sudo systemctl status firewalld
```

### 2.7 Проверка портов снаружи
Проверка снаружи:
```bash
ncat -zv наш_ip 80
ncat -zv наш_ip 8501
ncat -zv наш_ip 8000
ncat -zv наш_ip 5432
```
Если порт открыт и приложение слушает этот порт, ответ будет примерно таким:
```text
Ncat: Connected to наш_ip:8501.
```
Если порт открыт в Oracle Cloud и `firewalld`, но приложение не запущено, подключение может не пройти.

Проверка слушающих портов на сервере:
```bash
sudo ss -tulpn
```

Для Streamlit:
```bash
sudo ss -tulpn | grep 8501
```

Для FastAPI:
```bash
sudo ss -tulpn | grep 8000
```

## 3. Первая диагностика SSH-доступа

### 3.1 Подключение по SSH

Команда:
```bash
ssh -i /путь/к/ssh-ключу/ssh-key-2026-04-12.key rocky@публичный_айпи_адрес_инстанса
```

### 3.2 Установка SSH-клиента, если его нет.
а. Linux.
```bash
sudo dnf install openssh-clients -y
```

б. Windows
- «Пуск» → «Параметры» → «Приложения» → «Дополнительные компоненты» → «Добавить компонент» → найти OpenSSH Client → установить.
- `Settings` → `Apps` → `Optional Features` → `Add a feature` → выбрать `OpenSSH Client` → установить.
Затем открываем PowerShell и подключаемся.

### 3.2 Ошибка прав на приватный ключ
```text
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for '/home/что-то там/ssh-key-2026-04-12.key' are too open.
This private key will be ignored.
Load key "/home/что-то там/ssh-key-2026-04-12.key": bad permissions
rocky@адрес_хоста: Permission denied (publickey).
```

Решение - были изменены права на ключи:
```bash
chmod 700 /home/pd/pd_log_controller/.ssh
chmod 600 /home/pd/pd_log_controller/.ssh/ssh-hse-priv.key
chmod 644 /home/pd/pd_log_controller/.ssh/ssh-hse-pub.pub
```

Пояснение:
- `700` для папки `.ssh` — владелец может читать, писать и заходить в папку;
- `600` для приватного ключа — читать и изменять может только владелец;
- `644` для публичного ключа — публичный ключ может быть доступен для чтения.

Если случайно поставить права `600` на папку `.ssh`, файлы внутри могут не отображаться, потому что у папки не будет права на вход.

Исправление:
```bash
chmod 700 /home/pd/pd_log_controller/.ssh
```

### 3.3 Ошибка неправильного указания SSH-ключа
Неправильная команда:
```bash
ssh -l /home/pd/pd_log_controller/.ssh/ssh-hse-priv.key rocky@158.101.7.150
```
Опция `-l` означает login, то есть имя пользователя, а не путь к ключу.

Правильно использовать опцию `-i`:
```bash
ssh -i /home/pd/pd_log_controller/.ssh/ssh-hse-priv.key rocky@158.101.7.150
```

## 4. Проверка характеристик системы
После успешного входа по SSH были выполнены команды для получения информации о системе.

### 4.1 Команды
```bash
uname -a
cat /etc/os-release
lscpu
cat /proc/meminfo | grep MemTotal
df -h
hostname -I
```

### 4.2 Посмотреть конфиг
```bash
cat /etc/os-release
```

### 4.3 Полученные характеристики

По выводу системы:
- **OS:** Rocky Linux 9.7 (Blue Onyx)
- **CPU:** 2 vCPU
- **Model name:** AMD EPYC 7551 32-Core Processor
- **RAM:** 1 GB
- **Disk:** 46 GB доступного пространства на корневом разделе

Можно одной командой:
```bash
echo "=== OS ===" && cat /etc/os-release | grep -E "PRETTY_NAME|VERSION" && echo "=== CPU ===" && lscpu | grep -E "Model name|CPU\(s\)" && echo "=== RAM ===" && cat /proc/meminfo | grep MemTotal && echo "=== DISK ===" && df -h
```

## 5. Обновление системы
После входа на сервер была выполнена базовая подготовка системы.

### 5.1 Обновление системы
Для Rocky Linux используется пакетный менеджер `dnf`.
```bash
sudo dnf upgrade -y
```

### 5.2 Установка базовых утилит
```bash
sudo dnf install -y git curl wget nano htop tmux firewalld openssh-clients
```
### 5.3 Проверка репозиториев
Посмотреть подключённые репозитории:
```bash
sudo dnf repolist
```

## 6. Запуск приложений проекта

### 6.1 Streamlit
Streamlit обычно использует порт `8501`.
Чтобы приложение было доступно снаружи сервера, нужно запускать его на адресе `0.0.0.0`:
```bash
streamlit run app/Home.py --server.address 0.0.0.0 --server.port 8501
```

Проверить, что порт слушается:
```bash
sudo ss -tulpn | grep 8501
```

Если всё правильно, в выводе должно быть что-то похожее на:
```text
0.0.0.0:8501
```

Если вместо этого указано:
```text
127.0.0.1:8501 -- значит приложение доступно только внутри сервера.
```

### 6.2 FastAPI
FastAPI обычно запускается через `uvicorn` на порту `8000`.

Пример запуска:
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

Проверить, что порт слушается:
```bash
sudo ss -tulpn | grep 8000
```