import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import timedelta

class DivergenceAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализатор расхождений валютных пар")
        self.root.geometry("1200x800")
        
        # Переменные
        self.csv_file1 = tk.StringVar()
        self.csv_file2 = tk.StringVar()
        self.symbol1 = tk.StringVar(value="aud")
        self.symbol2 = tk.StringVar(value="cad")
        self.segment_days = tk.StringVar(value="2")
        
        # Данные
        self.df = None
        self.results = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # Заголовок с контактом
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        title_label = ttk.Label(title_frame, text="Анализатор расхождений валютных пар", 
                               font=("Arial", 16, "bold"))
        title_label.pack()
        
        contact_label = ttk.Label(title_frame, text="Вопросы и предложения - @zakat1191 тг", 
                                 font=("Arial", 10), foreground="gray")
        contact_label.pack()
        
        # Основной фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Левая панель - настройки
        left_frame = ttk.LabelFrame(main_frame, text="Загрузка CSV файлов", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # CSV файл 1
        ttk.Label(left_frame, text="CSV файл для пары 1:").pack(anchor=tk.W, pady=2)
        csv1_frame = ttk.Frame(left_frame)
        csv1_frame.pack(fill=tk.X, pady=2)
        ttk.Entry(csv1_frame, textvariable=self.csv_file1, width=25).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(csv1_frame, text="Выбрать файл", command=lambda: self.select_csv_file(1)).pack(side=tk.RIGHT, padx=(5,0))
        
        # CSV файл 2
        ttk.Label(left_frame, text="CSV файл для пары 2:").pack(anchor=tk.W, pady=(10,2))
        csv2_frame = ttk.Frame(left_frame)
        csv2_frame.pack(fill=tk.X, pady=2)
        ttk.Entry(csv2_frame, textvariable=self.csv_file2, width=25).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(csv2_frame, text="Выбрать файл", command=lambda: self.select_csv_file(2)).pack(side=tk.RIGHT, padx=(5,0))
        
        # Название пар
        ttk.Label(left_frame, text="Название пары 1:").pack(anchor=tk.W, pady=(10,2))
        ttk.Entry(left_frame, textvariable=self.symbol1).pack(fill=tk.X, pady=2)
        
        ttk.Label(left_frame, text="Название пары 2:").pack(anchor=tk.W, pady=(10,2))
        ttk.Entry(left_frame, textvariable=self.symbol2).pack(fill=tk.X, pady=2)
        
        # Длина сегмента
        ttk.Label(left_frame, text="Длина сегмента (дни):").pack(anchor=tk.W, pady=(10,2))
        ttk.Entry(left_frame, textvariable=self.segment_days).pack(fill=tk.X, pady=2)
        
        # Кнопка анализа
        ttk.Button(left_frame, text="Загрузить и анализировать", 
                  command=self.load_and_analyze).pack(pady=20, fill=tk.X)
        
        # Правая панель - результаты
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Notebook для вкладок
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка "График"
        self.graph_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.graph_frame, text="График")
        
        # Вкладка "Результаты"
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Результаты")
    
    def select_csv_file(self, file_number):
        """Выбор CSV файла"""
        filename = filedialog.askopenfilename(
            title=f"Выберите CSV файл для пары {file_number}",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            if file_number == 1:
                self.csv_file1.set(filename)
            else:
                self.csv_file2.set(filename)
    
    def load_data_from_csv(self):
        """Загрузка данных из CSV файлов"""
        if not self.csv_file1.get() or not self.csv_file2.get():
            messagebox.showerror("Ошибка", "Выберите оба CSV файла")
            return None
        
        try:
            # Загрузка первого файла
            df1 = pd.read_csv(self.csv_file1.get(), header=None, 
                             names=["Date", "Time", "Open", "High", "Low", "Close", "Volume"])
            df1["datetime"] = pd.to_datetime(df1["Date"] + " " + df1["Time"])
            df1.set_index("datetime", inplace=True)
            df1 = df1[["Close"]].rename(columns={"Close": self.symbol1.get()})
            
            # Загрузка второго файла
            df2 = pd.read_csv(self.csv_file2.get(), header=None, 
                             names=["Date", "Time", "Open", "High", "Low", "Close", "Volume"])
            df2["datetime"] = pd.to_datetime(df2["Date"] + " " + df2["Time"])
            df2.set_index("datetime", inplace=True)
            df2 = df2[["Close"]].rename(columns={"Close": self.symbol2.get()})
            
            # Объединяем данные
            df = df1.join(df2, how='inner')
            
            messagebox.showinfo("Успех", f"Загружено {len(df)} записей из CSV файлов")
            return df
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки CSV файлов: {str(e)}")
            return None

    def load_and_analyze(self):
        """Загрузка данных и запуск анализа"""
        # Загружаем данные
        self.df = self.load_data_from_csv()
        if self.df is not None:
            # Запускаем анализ
            self.analyze_data()

    def analyze_data(self):
        """Анализ расхождений"""
        if self.df is None:
            messagebox.showerror("Ошибка", "Сначала загрузите данные")
            return
        
        try:
            # Получаем параметры
            segment_days = int(self.segment_days.get())
            symbol1 = self.symbol1.get()
            symbol2 = self.symbol2.get()
            
            # Разбивка на сегменты
            start_date = self.df.index.min()
            end_date = self.df.index.max()
            segment = timedelta(days=segment_days)
            
            self.results = []
            thresholds = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.5, 2.0]
            threshold_reached = {t: 0 for t in thresholds}
            threshold_reverted = {t: 0 for t in thresholds}
            
            while start_date < end_date:
                segment_end = start_date + segment
                segment_data = self.df[(self.df.index >= start_date) & (self.df.index < segment_end)]
                
                if len(segment_data) > 1:
                    # Нормализация
                    price1_0 = segment_data[symbol1].iloc[0]
                    price2_0 = segment_data[symbol2].iloc[0]
                    
                    price1_norm = 100 * (segment_data[symbol1] / price1_0 - 1)
                    price2_norm = 100 * (segment_data[symbol2] / price2_0 - 1)
                    
                    diff_series = (price1_norm - price2_norm).abs()
                    
                    # Расхождение
                    max_diff = diff_series.max()
                    time_max = diff_series.idxmax()
                    
                    after_max = diff_series[diff_series.index > time_max]
                    time_min_after = after_max.idxmin() if not after_max.empty else None
                    min_after = after_max.min() if not after_max.empty else None
                    
                    # Пороговая обработка
                    for t in thresholds:
                        if max_diff >= t:
                            threshold_reached[t] += 1
                            if min_after is not None and min_after <= 0.05:
                                threshold_reverted[t] += 1
                    
                    self.results.append({
                        "start": start_date,
                        "end": segment_end,
                        "max_diff": max_diff,
                        "time_max": time_max,
                        "min_after": min_after,
                        "time_min_after": time_min_after,
                        "diff_series": diff_series
                    })
                
                start_date = segment_end
            
            # Отображение результатов
            self.display_results(threshold_reached, threshold_reverted)
            self.plot_results()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка анализа: {str(e)}")

    def display_results(self, threshold_reached, threshold_reverted):
        """Отображение результатов в виде текста"""
        # Очищаем предыдущие результаты
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Создаем скроллируемый текст
        text_frame = ttk.Frame(self.results_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(text_frame)
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Consolas", 10))
        text_widget.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=text_widget.yview)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Формируем компактный текст результатов
        symbol1_name = self.symbol1.get()
        symbol2_name = self.symbol2.get()
        
        result_text = "="*60 + "\n"
        result_text += f"{'АНАЛИЗ РАСХОЖДЕНИЙ ВАЛЮТНЫХ ПАР':^60}\n"
        result_text += f"{symbol1_name} vs {symbol2_name}\n"
        result_text += "="*60 + "\n\n"
        
        # Компактная статистика
        total_segments = len(self.results)
        if total_segments > 0:
            avg_diff = sum(r['max_diff'] for r in self.results) / total_segments
            max_diff_result = max(self.results, key=lambda x: x['max_diff'])
            max_diff = max_diff_result['max_diff']
            max_diff_date = max_diff_result['start'].strftime("%Y-%m-%d")
            
            result_text += "📊 СТАТИСТИКА\n"
            result_text += "-"*40 + "\n"
            result_text += f"📈 Среднее расхождение:      {avg_diff:>7.2f}%\n"
            result_text += f"🔺 Максимальное расхождение: {max_diff:>7.2f}%\n"
            result_text += f"📅 Дата максимума:           {max_diff_date}\n"
            result_text += f"📊 Всего сегментов:          {total_segments:>7}\n"
            result_text += "\n"
        
        # Пороговый анализ
        result_text += "🎯 ПОРОГОВЫЙ АНАЛИЗ\n"
        result_text += "-"*40 + "\n"
        result_text += f"{'Порог':>8} {'Достигнуто':>12} {'Сошлось':>10}\n"
        result_text += "-"*40 + "\n"
        
        thresholds = [0.5, 0.7, 1.0, 1.5, 2.0]
        for t in thresholds:
            reached = threshold_reached[t]
            reverted = threshold_reverted[t] 
            result_text += f"{t:>7.1f}% {reached:>11} {reverted:>9}\n"
        
        text_widget.insert(tk.END, result_text)
        text_widget.config(state=tk.DISABLED)

    def plot_results(self):
        """Построение графика"""
        # Очищаем предыдущий график
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        if not self.results:
            return
        
        # Создаем фигуру
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # График 1: Максимальные расхождения по сегментам
        dates = [r['start'].date() for r in self.results]
        max_diffs = [r['max_diff'] for r in self.results]
        
        ax1.plot(dates, max_diffs, 'b-o', markersize=4)
        ax1.set_title('Максимальные расхождения по сегментам')
        ax1.set_ylabel('Расхождение (%)')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # График 2: Гистограмма распределения расхождений
        ax2.hist(max_diffs, bins=20, alpha=0.7, edgecolor='black')
        ax2.set_title('Распределение максимальных расхождений')
        ax2.set_xlabel('Расхождение (%)')
        ax2.set_ylabel('Количество сегментов')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Встраиваем график в tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = DivergenceAnalyzer(root)
    root.mainloop()