## GitHub workflow

### 1. Первый запуск Git в системе

```bash
git config --global user.name "Dima"
git config --global user.email "your_email@example.com"
```
Git использует эти данные в коммитах.

### 2.Авторизация в GitHub (сделал оба, чтобы попробовать)

#### Вариант A: HTTPS

`https://github.com/d-pascenco/pd_log_controller.git`

При git push Git запросит логин и токен. Вместо пароля GitHub использует Personal Access Token.

#### Вариант B: SSH

```bash
mkdir -p /home/pd/pd_log_controller/.ssh/git
ssh-keygen -t ed25519 -C "моя_почта" -f /home/pd/pd_log_controller/.ssh/git/id_ed25519
ssh-add /home/pd/pd_log_controller/.ssh/git/id_ed25519
cat /home/pd/pd_log_controller/.ssh/git/id_ed25519.pub
```
Копирую публичный ключ и добавляю его в GitHub: Settings -> SSH and GPG keys -> New SSH key.
Проверка подключения: `ssh -T git@github.com`.
Сообщение `Hi d-pascenco! You've successfully authenticated, but GitHub does not provide shell access.` означает, 
что SSH-ключ работает и GitHub нас принял.

### 3. Первое подключение локального проекта к GitHub

```bash
git init
git add .
# если попало что-то лишнее, но коммита еще не было, то можно отменить `git restore --staged .`
git commit -m "Initial commit"
git branch -M main
git remote add origin <REMOTE_URL>
git push -u origin main

git remote add origin https://github.com/d-pascenco/pd_log_controller.git
## или
git remote add origin git@github.com:d-pascenco/pd_log_controller.git
```
`remote add origin` привязывает локальный репозиторий к удалённому репозиторию GitHub. 
В качестве <REMOTE_URL> используется либо HTTPS URL, либо SSH URL.

### 4. Обычный рабочий цикл

```bash
git status
git add .
git commit -m "Describe changes"
git push
```
`git status` показывает изменения.
`git push` отправляет коммиты в удалённый репозиторий.

### 5. Получение изменений

```bash
git pull
```
`git pull` забирает изменения из удалённого репозитория в локальный.

### 6. Полезные команды

```bash
git remote -v
git branch
git log --oneline
```
`git remote -v` показывает привязанный удалённый репозиторий.
`git branch` показывает ветки.

### 7. Работа с ветками

```bash
git branch
git switch -c название_ветки
git add .
git commit -m "что сделал"
git push -u origin feature/login
git switch main
git merge feature/login
git push
git branch -d feature/login
```

Лучше называть так:
```text
feature/... — новая функция.
fix/... — исправление бага.
docs/... — документация.
hotfix/... — срочный фикс.
```

`git switch -c` создаёт и сразу переключает на новую ветку.

`git merge` объединяет ветку обратно в текущую.

---
### 8. Самые частые флаги:
```text
 -m — сообщение коммита.
 -c — создать ветку.
 -u — связать локальную ветку с удалённой.
 -d — удалить ветку.
 -a — все файлы.
 -r — рекурсивно.
 -f — принудительно.
 --amend — изменить последний коммит.
 --no-edit — не менять сообщение коммита.
 --graph — показать дерево веток.
 --stat — показать статистику изменений.
 --name-only — показать только имена файлов.
```

### 9. .gitignore

.gitignore — это файл, который говорит Git, какие файлы и папки не отслеживать и не коммитить.
Нужен, чтобы не тащить в репозиторий .env, .venv, __pycache__, логи, сборки, IDE-файлы и др и 
не засорять историю Git мусором.

Лежит обычно в корне репозитория рядом с .git и проектом.
Можно сделать и глобальный ignore для всех репозиториев, и локальный для одного проекта.

**Как работает (пример):**

```text
.venv/
__pycache__/
*.pyc
.env
.idea/
.vscode/
```

**Синтаксис:**
`#` — комментарий.
`name` — игнорировать файл или папку с этим именем.
`*.log` — все .log файлы.
`dir/` — папка целиком.
`!file` — исключение, вернуть файл обратно из игнора.

**Важно:**
Если файл уже был добавлен в Git, .gitignore сам по себе его не уберёт из отслеживания.
Для этого нужно убрать файл из индекса, например через git rm --cached <file>.

**Команды, которые часто используют вместе:**
`git status` и `git add .` затем
git rm --cached <file> — перестать отслеживать файл, но оставить его локально.
git check-ignore -v <file> — понять, почему файл игнорируется.


