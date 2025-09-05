@echo off
echo Сборка анализатора расхождений в .exe файл...

echo.
echo Установка зависимостей...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo Сборка .exe файла...
pyinstaller --onefile --windowed --name "DivergenceAnalyzer" divergence_analyzer_gui.py

echo.
echo Готово! .exe файл находится в папке dist/
echo Размер файла: примерно 80-120 МБ
echo.
echo Для запуска на другом компьютере:
echo 1. Скопируйте DivergenceAnalyzer.exe
echo 2. Установите MetaTrader 5 (для загрузки данных из MT5)
echo 3. Запустите .exe файл
pause
