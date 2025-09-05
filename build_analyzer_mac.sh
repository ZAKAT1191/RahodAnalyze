#!/bin/bash

# Скрипт для сборки приложения на macOS

echo "🍎 Сборка Анализатора расхождений для macOS..."

# Проверяем Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.8+ с https://python.org"
    exit 1
fi

# Создаем виртуальное окружение
echo "📦 Создание виртуального окружения..."
python3 -m venv venv_mac
source venv_mac/bin/activate

# Устанавливаем зависимости
echo "📋 Установка зависимостей..."
pip install --upgrade pip
pip install pandas matplotlib numpy pyinstaller

# Компилируем приложение
echo "🔨 Компиляция приложения..."
pyinstaller --onefile \
    --windowed \
    --name "DivergenceAnalyzer" \
    --icon=app.icns \
    --add-data "requirements.txt:." \
    divergence_analyzer_gui.py

# Проверяем результат
if [ -f "dist/DivergenceAnalyzer" ]; then
    echo "✅ Компиляция завершена успешно!"
    echo "📁 Исполняемый файл: dist/DivergenceAnalyzer"
    echo ""
    echo "🚀 Для запуска:"
    echo "   ./dist/DivergenceAnalyzer"
    echo ""
    echo "📦 Для создания DMG пакета:"
    echo "   hdiutil create -volname 'Divergence Analyzer' -srcfolder dist -ov DivergenceAnalyzer.dmg"
else
    echo "❌ Ошибка компиляции. Проверьте логи выше."
    exit 1
fi

# Деактивируем виртуальное окружение
deactivate

echo "🎉 Готово!"
