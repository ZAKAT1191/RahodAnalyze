# 🚀 Настройка автоматической сборки через GitHub Actions

## 📋 Пошаговая инструкция

### 1. 📁 Создание репозитория на GitHub

1. Идите на [github.com](https://github.com)
2. Нажмите кнопку **"New repository"** (зеленая кнопка)
3. Заполните:
   - **Repository name**: `divergence-analyzer` (или любое другое)
   - **Description**: `Анализатор расхождений валютных пар`
   - ✅ **Public** (чтобы использовать бесплатные Actions)
   - ✅ **Add a README file**
4. Нажмите **"Create repository"**

### 2. 📤 Загрузка файлов в репозиторий

#### Способ 1: Через веб-интерфейс GitHub
1. В созданном репозитории нажмите **"uploading an existing file"**
2. Перетащите все файлы из папки `DivergenceAnalyzer`:
   ```
   divergence_analyzer_gui.py
   requirements.txt
   README.md
   .github/workflows/build.yml
   build_analyzer.bat
   build_analyzer_mac.sh
   ```
3. Напишите commit message: `🎉 Initial release`
4. Нажмите **"Commit changes"**

#### Способ 2: Через Git (если установлен)
```bash
# Клонируем репозиторий
git clone https://github.com/ВАШ_USERNAME/divergence-analyzer.git
cd divergence-analyzer

# Копируем файлы из папки DivergenceAnalyzer
# (скопируйте все файлы вручную)

# Добавляем файлы
git add .
git commit -m "🎉 Initial release"
git push origin main
```

### 3. 🔧 Проверка структуры файлов

Убедитесь, что в репозитории есть такая структура:
```
divergence-analyzer/
├── .github/
│   └── workflows/
│       └── build.yml                 # ⚡ GitHub Actions
├── divergence_analyzer_gui.py        # 🐍 Основное приложение
├── requirements.txt                  # 📦 Зависимости
├── README.md                         # 📖 Документация
├── build_analyzer.bat               # 🪟 Сборка для Windows
└── build_analyzer_mac.sh            # 🍎 Сборка для Mac
```

### 4. 🚀 Запуск автоматической сборки

#### Автоматический запуск:
- Сборка запустится автоматически при каждом **push** в ветку `main`

#### Ручной запуск:
1. Идите в репозиторий на GitHub
2. Вкладка **"Actions"** 
3. Слева выберите **"Build Multi-Platform Apps"**
4. Нажмите **"Run workflow"** → **"Run workflow"**

### 5. 📦 Получение собранных приложений

#### Во время сборки:
1. **Actions** → выберите текущую сборку
2. Прокрутите вниз до **"Artifacts"**
3. Скачайте:
   - `Windows-Build` (для Windows)
   - `macOS-Build` (для Mac)
   - `Linux-Build` (для Linux)

#### После успешной сборки:
1. Автоматически создается **Release** 
2. Идите в **"Releases"** (справа в репозитории)
3. Скачайте нужный файл:
   - `divergence-analyzer-windows.exe`
   - `divergence-analyzer-macos`
   - `divergence-analyzer-linux`

## 📊 Мониторинг сборки

### ✅ Успешная сборка:
- Зеленая галочка в **Actions**
- Новый релиз в **Releases**
- Готовые файлы для скачивания

### ❌ Ошибка сборки:
- Красный крестик в **Actions**
- Нажмите на сборку → посмотрите логи
- Исправьте ошибки → сделайте новый push

## 🔄 Автоматические обновления

После настройки, каждый push в репозиторий будет:
1. 🔨 Собирать приложения для всех платформ
2. 📦 Создавать новый релиз
3. 🎯 Автоматически версионировать (v1, v2, v3...)

## 🎛️ Настройки

### Изменить версию Python:
В файле `.github/workflows/build.yml` измените:
```yaml
python-version: '3.9'  # → '3.10' или '3.11'
```

### Добавить новые зависимости:
В файле `requirements.txt` добавьте:
```
pandas
matplotlib
numpy
новая_библиотека
```

### Изменить название приложения:
В файле `.github/workflows/build.yml` найдите:
```yaml
--name "DivergenceAnalyzer"  # → "НовоеНазвание"
```

## 🆘 Возможные проблемы

### 1. Ошибка "No module named 'tkinter'"
**Решение**: tkinter включен в стандартную поставку Python на GitHub Actions

### 2. Ошибка с matplotlib
**Решение**: Добавьте в requirements.txt:
```
matplotlib>=3.0.0
```

### 3. Слишком большой размер файла
**Решение**: Добавьте в build.yml:
```yaml
pyinstaller --onefile --windowed --exclude-module pytest
```

### 4. Ошибка доступа к GitHub Actions
**Решение**: Убедитесь, что репозиторий **Public**

## 🎉 Результат

После настройки у вас будет:
- ✅ **Автоматическая сборка** для Windows, Mac, Linux
- ✅ **Готовые исполняемые файлы** 
- ✅ **Автоматические релизы**
- ✅ **Бесплатно** (до 2000 минут в месяц)

## 📞 Поддержка

Вопросы и предложения - @zakat1191 тг
