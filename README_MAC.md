# 🍎 Компиляция для macOS

## Требования

- **macOS 10.14+** (Mojave или новее)
- **Python 3.8+** (установить с [python.org](https://python.org))
- **Xcode Command Line Tools**: `xcode-select --install`

## 🚀 Быстрая сборка

```bash
# Дать права на выполнение
chmod +x build_analyzer_mac.sh

# Запустить сборку
./build_analyzer_mac.sh
```

## 📋 Ручная сборка

### 1. Подготовка окружения

```bash
# Создать виртуальное окружение
python3 -m venv venv_mac
source venv_mac/bin/activate

# Установить зависимости
pip install --upgrade pip
pip install pandas matplotlib numpy pyinstaller
```

### 2. Компиляция

```bash
# Базовая сборка
pyinstaller --onefile --windowed --name "DivergenceAnalyzer" divergence_analyzer_gui.py

# Расширенная сборка с иконкой
pyinstaller --onefile \
    --windowed \
    --name "DivergenceAnalyzer" \
    --icon=app.icns \
    --add-data "requirements.txt:." \
    divergence_analyzer_gui.py
```

### 3. Создание DMG пакета (опционально)

```bash
# Создать DMG для распространения
hdiutil create -volname "Divergence Analyzer" -srcfolder dist -ov DivergenceAnalyzer.dmg
```

## 📁 Структура файлов

```
DivergenceAnalyzer/
├── divergence_analyzer_gui.py     # Основное приложение
├── build_analyzer_mac.sh          # Скрипт сборки
├── requirements.txt               # Зависимости
├── app.icns                      # Иконка (опционально)
└── dist/
    └── DivergenceAnalyzer        # Готовое приложение
```

## 🛠️ Альтернативные способы

### 1. Через Docker (кросс-платформенная сборка)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt pyinstaller
RUN pyinstaller --onefile divergence_analyzer_gui.py

CMD ["./dist/divergence_analyzer_gui"]
```

### 2. Через GitHub Actions (автоматическая сборка)

```yaml
name: Build macOS App

on: [push]

jobs:
  build-macos:
    runs-on: macos-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt pyinstaller
    
    - name: Build app
      run: |
        pyinstaller --onefile --windowed divergence_analyzer_gui.py
    
    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: macos-app
        path: dist/
```

## 🎯 Универсальная сборка (Intel + Apple Silicon)

```bash
# Для универсальной сборки (Intel + M1/M2)
pyinstaller --onefile \
    --windowed \
    --target-architecture universal2 \
    --name "DivergenceAnalyzer" \
    divergence_analyzer_gui.py
```

## ⚠️ Возможные проблемы

### 1. Ошибка с tkinter
```bash
# Установить tkinter отдельно
brew install python-tk
```

### 2. Ошибка с matplotlib
```bash
# Установить matplotlib с поддержкой GUI
pip install matplotlib[gui]
```

### 3. Проблемы с путями
```python
# В коде использовать:
import os
import sys

if getattr(sys, 'frozen', False):
    # Если приложение собрано
    application_path = sys._MEIPASS
else:
    # Если запускается из исходников
    application_path = os.path.dirname(os.path.abspath(__file__))
```

## 📦 Распространение

1. **Простой способ**: Скопировать файл `dist/DivergenceAnalyzer`
2. **DMG пакет**: Создать через `hdiutil` (см. выше)
3. **App Bundle**: Создать структуру `.app` для Mac App Store

## 🔒 Код-подпись (для распространения)

```bash
# Подписать приложение (нужен Apple Developer ID)
codesign --sign "Developer ID Application: Your Name" dist/DivergenceAnalyzer

# Проверить подпись
codesign --verify --verbose dist/DivergenceAnalyzer
```

## 📞 Поддержка

Вопросы и предложения - @zakat1191 тг
