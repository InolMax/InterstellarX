import sys
import math
import json
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QTextEdit, QCheckBox, QMessageBox, QScrollArea, QFrame, QTabWidget
)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScroller
from PySide6.QtGui import QIcon, QPixmap, QColor  # Добавлено для иконки
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import mplcyberpunk  # Импортируем библиотеку для стиля "cyberpunk"
try:
    import pyi_splash
    pyi_splash.close()  # Закрыть загрузочный экран
except ImportError:
    pass  # Пропустить, если модуль недоступен
 
 
 
class RoundedInputWidget(QFrame):
    def __init__(self, label_text, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #2E3440;
                border-radius: 15px;
                padding: 10px;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #ECEFF4;
            }
            QLineEdit {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 1px solid #4C566A;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.layout = QVBoxLayout(self)
        self.label = QLabel(label_text)
        self.layout.addWidget(self.label)
        self.entry = QLineEdit()
        self.layout.addWidget(self.entry)
 
class RocketCalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("InterstellarX")
        self.setGeometry(100, 100, 1200, 800)
 
        # Устанавливаем иконку окна в виде цвета (голубой)
        # Создаём иконку из цвета
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor(88, 192, 208))  # Голубой цвет
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)
 
        # Устанавливаем темный фон для всего приложения
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E3440;
            }
            QWidget {
                background-color: #2E3440;
                color: #ECEFF4;
            }
        """)
 
        # Основной виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
 
        # Создаем вкладки
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                background-color: #2E3440;
                border: 1px solid #4C566A;
                margin: -1px;
            }
            QTabBar::tab {
                background-color: #3B4252;
                color: #ECEFF4;
                padding: 10px;
                border: 1px solid #4C566A;
                border-bottom-color: #2E3440;
            }
            QTabBar::tab:selected {
                background-color: #2E3440;
                border-bottom-color: #2E3440;
            }
            QTabWidget {
                background-color: #2E3440;
                border: none;
            }
        """)
        main_layout.addWidget(self.tabs)
 
        # Вкладка для ввода-вывода информации
        self.input_output_tab = QWidget()
        self.tabs.addTab(self.input_output_tab, "Ввод-Вывод")
        self.setup_input_output_tab()
 
        # Вкладка для графика
        self.graph_tab = QWidget()
        self.tabs.addTab(self.graph_tab, "График")
        self.setup_graph_tab()
 
        # Загрузка параметров при запуске
        self.load_parameters()
 
    def setup_input_output_tab(self):
        layout = QVBoxLayout(self.input_output_tab)
 
        # Добавляем ScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setStyleSheet("""
    QScrollArea {
        border: none;
        background-color: #2E3440;
    }
    QScrollBar:vertical {
        background: #3B4252;  /* Цвет фона скроллбара */
        width: 12px;         /* Ширина скроллбара */
        margin: 0px 0px 0px 0px;
    }
    QScrollBar::handle:vertical {
        background: #88C0D0;  /* Цвет ползунка */
        min-height: 20px;     /* Минимальная высота ползунка */
        border-radius: 6px;   /* Закругление углов ползунка */
    }
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        background: none;     /* Убираем стрелки */
    }
    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {
        background: none;     /* Убираем фон вокруг ползунка */
    }
     """)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        scroll_layout.setSpacing(10)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
 
        # Включаем прокрутку одним пальцем
        QScroller.grabGesture(scroll_area.viewport(), QScroller.LeftMouseButtonGesture)
 
        # Поля ввода
        self.entry_Mpn = self.create_input_field("Полезная нагрузка, тонн:", scroll_layout)
        self.entry_q = self.create_input_field("Отношение массы баков к массе топлива:", scroll_layout)
        self.entry_F_base = self.create_input_field("Эталонное значение тяги, Н:", scroll_layout)
        self.entry_Mpower_base = self.create_input_field("Эталонное значение массы ду + эу, тонн:", scroll_layout)
        self.entry_Mfdot_base = self.create_input_field("Эталонный расход рабочего тела, кг/с:", scroll_layout)
        self.entry_F_start = self.create_input_field("Начальное значение тяги, Н:", scroll_layout)
        self.entry_F_end = self.create_input_field("Конечное значение тяги, Н:", scroll_layout)
        self.entry_Mf_start = self.create_input_field("Начальное значение массы топлива, тонн:", scroll_layout)
        self.entry_Mf_end = self.create_input_field("Конечное значение массы топлива, тонн:", scroll_layout)
        self.entry_stepF = self.create_input_field("Шаг перебора тяги, Н:", scroll_layout)
        self.entry_stepMf = self.create_input_field("Шаг перебора масс, тонн:", scroll_layout)
        self.entry_Dist = self.create_input_field("Расстояние, световые годы:", scroll_layout)
        self.entry_Dist.setText("4.367")  # Значение по умолчанию
 
        # CheckBox для двухступенчатой ракеты
        self.two_stage_checkbox = QCheckBox("Двухступенчатый")
        self.two_stage_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ECEFF4;
                font-size: 14px;
                padding: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #ECEFF4;
                border-radius: 5px;
            }
            QCheckBox::indicator:checked {
                background-color: #88C0D0;
                image: url('path_to_your_custom_image.png');  /* Замените на путь к вашему изображению */
            }
            QCheckBox::indicator:unchecked {
                background-color: #4C566A;
            }
        """)
        scroll_layout.addWidget(self.two_stage_checkbox)
 
        # ProgressBar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(QApplication.primaryScreen().size().width() - 40)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #3B4252;
                color: #ECEFF4;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #88C0D0;
                border-radius: 5px;
            }
        """)
        scroll_layout.addWidget(self.progress_bar)
 
        # Кнопки
        self.save_button = QPushButton("Сохранить введенные параметры")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #88C0D0;
                color: #2E3440;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
        """)
        self.save_button.setMinimumHeight(50)
        self.save_button.clicked.connect(self.save_parameters)
        scroll_layout.addWidget(self.save_button)
 
        self.calculate_button = QPushButton("Рассчитать")
        self.calculate_button.setStyleSheet("""
            QPushButton {
                background-color: #5E81AC;
                color: #ECEFF4;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8FBCBB;
            }
        """)
        self.calculate_button.setMinimumHeight(50)
        self.calculate_button.clicked.connect(self.calculate)
        scroll_layout.addWidget(self.calculate_button)
 
        self.plot_button = QPushButton("Построить график")
        self.plot_button.setStyleSheet("""
            QPushButton {
                background-color: #222946;
                color: #ECEFF4;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #444e75;
            }
        """)
        self.plot_button.setMinimumHeight(50)
        self.plot_button.clicked.connect(self.plot_graph)
        scroll_layout.addWidget(self.plot_button)
 
        # Область вывода
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("background-color: #3B4252; color: #ECEFF4;")
        self.output_area.setMinimumHeight(900)  # Увеличение высоты окна вывода
        self.output_area.setMaximumWidth(QApplication.primaryScreen().size().width() - 40)
        scroll_layout.addWidget(self.output_area)
 
        self.calculation_stopped = False  # Флаг для остановки расчета
 
    def reset_to_initial_state(self):
        """Сброс программы в начальное состояние."""
        self.progress_bar.setValue(0)
        self.progress_bar.setRange(0, 100)  # Обычное состояние
        self.output_area.clear()
        self.calculation_stopped = False  # Сброс флага
    def setup_graph_tab(self):
        layout = QVBoxLayout(self.graph_tab)
 
        # Создаем FigureCanvas для отображения графика
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.figure.patch.set_facecolor('#222946')
 
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
 
    def create_input_field(self, label_text, layout):
        widget = RoundedInputWidget(label_text)
        widget.setMaximumWidth(QApplication.primaryScreen().size().width() - 40)
        layout.addWidget(widget)
        return widget.entry
 
 
    def save_parameters(self):
        parameters = {
            "Mpn": self.entry_Mpn.text(),
            "q": self.entry_q.text(),
            "F_base": self.entry_F_base.text(),
            "Mpower_base": self.entry_Mpower_base.text(),
            "Mfdot_base": self.entry_Mfdot_base.text(),
            "F_start": self.entry_F_start.text(),
            "F_end": self.entry_F_end.text(),
            "Mf_start": self.entry_Mf_start.text(),
            "Mf_end": self.entry_Mf_end.text(),
            "stepF": self.entry_stepF.text(),
            "stepMf": self.entry_stepMf.text(),
            "Dist": self.entry_Dist.text(),
        }
        with open("parameters.json", "w") as file:
            json.dump(parameters, file)
        QMessageBox.information(self, "Сохранение", "Параметры успешно сохранены!")
 
    def load_parameters(self):
        try:
            with open("parameters.json", "r") as file:
                content = file.read()
                if not content.strip():  # Если файл пустой
                    parameters = {}
                else:
                    parameters = json.loads(content)
        except FileNotFoundError:
            parameters = {}
 
        # Устанавливаем значения по умолчанию, если параметры отсутствуют
        self.entry_Mpn.setText(parameters.get("Mpn", ""))
        self.entry_q.setText(parameters.get("q", ""))
        self.entry_F_base.setText(parameters.get("F_base", ""))
        self.entry_Mpower_base.setText(parameters.get("Mpower_base", ""))
        self.entry_Mfdot_base.setText(parameters.get("Mfdot_base", ""))
        self.entry_F_start.setText(parameters.get("F_start", ""))
        self.entry_F_end.setText(parameters.get("F_end", ""))
        self.entry_Mf_start.setText(parameters.get("Mf_start", ""))
        self.entry_Mf_end.setText(parameters.get("Mf_end", ""))
        self.entry_stepF.setText(parameters.get("stepF", ""))
        self.entry_stepMf.setText(parameters.get("stepMf", ""))
        self.entry_Dist.setText(parameters.get("Dist", "4.367"))
    def apply_graph_style(self):
        """Применяет стиль построения графика (например, cyberpunk)"""
        plt.style.use("cyberpunk")  # Применяем стиль "cyberpunk"
    def calculate(self):
        self.calculation_stopped = False
        try:
            # Заменяем запятую на точку для всех введенных значений
            Mpn = float(self.entry_Mpn.text().replace(',', '.'))
            q = float(self.entry_q.text().replace(',', '.'))
            F_base = float(self.entry_F_base.text().replace(',', '.'))
            Mpower_base = float(self.entry_Mpower_base.text().replace(',', '.'))
            Mfdot_base = float(self.entry_Mfdot_base.text().replace(',', '.'))
            F_start = float(self.entry_F_start.text().replace(',', '.'))
            F_end = float(self.entry_F_end.text().replace(',', '.'))
            Mf_start = float(self.entry_Mf_start.text().replace(',', '.'))
            Mf_end = float(self.entry_Mf_end.text().replace(',', '.'))
            stepF = float(self.entry_stepF.text().replace(',', '.'))
            stepMf = float(self.entry_stepMf.text().replace(',', '.'))
            Dist = float(self.entry_Dist.text().replace(',', '.')) * 9.461e15
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, введите корректные числа.")
            return
        # Проверка на корректность введенных значений
        if F_end <= F_start:
            QMessageBox.critical(self, "Ошибка", "Конечное значение тяги должно быть больше начального.")
            return
        if Mf_end <= Mf_start:
            QMessageBox.critical(self, "Ошибка", "Конечное значение массы топлива должно быть больше начального.")
            return
 
        self.progress_bar.setMaximum(int((F_end - F_start) / stepF * (Mf_end - Mf_start) / stepMf))
        self.progress_bar.setValue(0)
 
        min_t = float('inf')
        min_F = None
        min_Mf = None
        max_v_at_min_t = None
        percent_DistAcc_at_min_t = None
        MaxAcc_at_min_t = None
        u_at_min_t = None
        MassSum_at_min_t = None
        TimeAcc_at_min_t = None
        best_T1 = None
        best_T2 = None
        best_Mass1 = None
        best_Mass2 = None
        best_D1 = None
        best_D2 = None
        best_V1 = None
        best_V2 = None
        best_DistAcc = None
        best_DistCruise = None
        best_TimeCruise = None
        best_Mdy1 = None
        best_Mdy2 = None
        best_GForce1 = None
        best_GForce2 = None
        Savedbest_M1f = None
 
        F = F_start
        while F <= F_end and not self.calculation_stopped:
            Mf = Mf_start
            while Mf <= Mf_end and not self.calculation_stopped:
                if self.two_stage_checkbox.isChecked():
                    current_value, best_F1, best_M1f, current_MaxV, percent_DistAcc, MaxAcc, u, MassSum, TimeAcc, T1, T2, Mass1, Mass2, D1, D2, V1, V2, DistAcc, DistCruise, MaxV, TimeCruise, Mdy1, Mdy2, GForce1, GForce2 = self.calculate_two_stage(F, Mf, Mpn, q, F_base, Mpower_base, Mfdot_base, Dist, F_end)
                    if current_value < min_t:
                        Savedbest_M1f = best_M1f
                        min_t = current_value
                        min_F = F
                        min_Mf = Mf
                        max_v_at_min_t = current_MaxV
                        percent_DistAcc_at_min_t = percent_DistAcc
                        MaxAcc_at_min_t = MaxAcc
                        u_at_min_t = u
                        MassSum_at_min_t = MassSum
                        TimeAcc_at_min_t = TimeAcc
                        best_T1 = T1
                        best_T2 = T2
                        best_Mass1 = Mass1
                        best_Mass2 = Mass2
                        best_D1 = D1
                        best_D2 = D2
                        best_V1 = V1
                        best_V2 = V2
                        best_DistAcc = DistAcc
                        best_DistCruise = DistCruise
                        best_TimeCruise = TimeCruise
                        best_Mdy1 = Mdy1
                        best_Mdy2 = Mdy2
                        best_GForce1 = GForce1
                        best_GForce2 = GForce2
                else:
                    current_value, current_MaxV, percent_DistAcc, MaxAcc, u, MassSum, TimeAcc = self.calculate_single_stage(F, Mf, Mpn, q, F_base, Mpower_base, Mfdot_base, Dist)
                    # Если расчеты были остановлены, сбрасываем состояние и выходим из цикла
                    if self.calculation_stopped:
                        self.reset_to_initial_state()
                        return
                    # Проверка на inf в TimeCruise
                    if self.two_stage_checkbox.isChecked() and math.isinf(TimeCruise):
                        self.progress_bar.setFormat("Ошибка. Возможно мы не успели потратить топливо")
                        self.progress_bar.setValue(0)
                        QMessageBox.warning(self, "error 450","Возможно мы не успели потратить топливо")
 
                        self.calculation_stopped = True
                        return
 
                    elif not self.two_stage_checkbox.isChecked() and math.isinf(current_value):
                        self.progress_bar.setFormat("Ошибка. Возможно мы не успели потратить топливо")
                        self.progress_bar.setValue(0)
                        QMessageBox.warning(self, "error 458","Возможно мы не успели потратить топливо")
                        self.calculation_stopped = True
                        return
 
                    # Возвращаем стандартный формат ProgressBar
                    self.progress_bar.setFormat("%p%")
                    if current_value < min_t:
                        min_t = current_value
                        min_F = F
                        min_Mf = Mf
                        max_v_at_min_t = current_MaxV
                        percent_DistAcc_at_min_t = percent_DistAcc
                        MaxAcc_at_min_t = MaxAcc
                        u_at_min_t = u
                        MassSum_at_min_t = MassSum / 1000
                        TimeAcc_at_min_t = TimeAcc
                Mf += stepMf
                self.progress_bar.setValue(self.progress_bar.value() + 1)
                QApplication.processEvents()
            F += stepF
 
        # Время
        result_text = f"Минимальное время полета, лет: {min_t:.10f}\n"
        if TimeAcc_at_min_t is not None:
            result_text += f"Время ускорения, лет: {TimeAcc_at_min_t / 31536000:.10f}\n"
 
        if self.two_stage_checkbox.isChecked():
            result_text += f"Время работы первой ступени: {best_T1 / 31536000:.10f} лет\n"
            result_text += f"Время работы второй ступени: {best_T2 / 31536000:.10f} лет\n\n\n"
 
        # Скорости
        if max_v_at_min_t != float('inf'):
            speed_km_s = max_v_at_min_t / 1000
            speed_percent = (max_v_at_min_t / 299792458) * 100
            result_text += f"Максимальная скорость: {speed_km_s:.1f} км/с\n"
            result_text += f"Максимальная скорость: {speed_percent:.1f}% от скорости света\n"
        else:
            result_text += "Максимальная скорость при минимальном времени полета: бесконечность \n"
 
        if self.two_stage_checkbox.isChecked():
            result_text += f"Скорость от первой ступени: {best_V1 / 1000:.2f} км/с\n"
            result_text += f"Скорость от второй ступени: {best_V2 / 1000:.2f} км/с\n\n\n"
 
        # Массы
        result_text += f"Общая масса топлива: {min_Mf:.2f} тонн\n"
        if MassSum_at_min_t is not None:
            result_text += f"Стартовая масса: {MassSum_at_min_t:.2f} тонн\n"
 
        if self.two_stage_checkbox.isChecked():
            result_text += f"Масса топлива первой ступени: {Savedbest_M1f:.2f} тонн\n"
            result_text += f"Масса топлива второй ступени: {min_Mf - Savedbest_M1f:.2f} тонн\n"
            result_text += f"Масса блока первой ступени: {(best_Mass1 - best_Mass2) / 1000:.2f} тонн\n"
            result_text += f"Масса блока второй ступени: {(best_Mass2 - Mpn*1000) / 1000:.2f} тонн\n"
            result_text += f"Масса ДУ первой ступени: {best_Mdy1 / 1000:.2f} тонн\n"
            result_text += f"Масса ДУ второй ступени: {best_Mdy2 / 1000:.2f} тонн\n\n\n"
 
        # Остальное
        if percent_DistAcc_at_min_t is not None:
            result_text += f"Процент разгонного пути: {percent_DistAcc_at_min_t:.2f}%\n"
 
        if u_at_min_t is not None:
            result_text += f"Удельный импульс: {u_at_min_t:.2f} м/с\n"
            if not self.two_stage_checkbox.isChecked():
                result_text += f"Максимальное ускорение (g-force): {MaxAcc_at_min_t:.4f} g\n"
                result_text += f"Оптимальная тяга: {min_F} Н\n\n\n"
                result_text += f"Создано для группы https://vk.com/newexpanse\n"
                result_text += f"Разработал: https://vk.com/wendelstein7x\n"
                result_text += f"Почта: sun_maksim_@mail.ru\n"
                result_text += f"При помощи нейросети: deepseek.com\n"
                result_text += f"Pydroid 3 + PySide6\n"
                result_text += f"V1.0 01.01.2025\n"
 
        if self.two_stage_checkbox.isChecked():
            result_text += f"Тяга первой ступени: {F_base/Mpower_base/1000*best_Mdy1:.2f} Н\n"
            result_text += f"Тяга второй ступени: {F_base/Mpower_base/1000*best_Mdy2:.2f} Н\n"
            result_text += f"Расстояние работы первой ступени: {best_D1 / 9.461e15:.10f} световых лет\n"
            result_text += f"Расстояние работы второй ступени: {best_D2 / 9.461e15:.10f} световых лет\n"
            result_text += f"Общий путь ускорения: {best_DistAcc / 9.461e15:.10f} световых лет\n"
            result_text += f"Максимальное ускорение первой ступени: {best_GForce1:.4f} g\n"
            result_text += f"Максимальное ускорение второй ступени: {best_GForce2:.4f} g\n\n\n"
 
            result_text += f"Создано для группы https://vk.com/newexpanse\n"
            result_text += f"Разработал: https://vk.com/wendelstein7x\n"
            result_text += f"Почта: sun_maksim_@mail.ru\n"
            result_text += f"При помощи нейросети: deepseek.com\n"
            result_text += f"Pydroid 3 + PySide6\n"
            result_text += f"V1.0 01.01.2025\n"
        self.reset_to_initial_state()
 
        self.output_area.setPlainText(result_text)
 
    def calculate_single_stage(self, F, Mf, Mpn, q, F_base, Mpower_base, Mfdot_base, Dist):
        if self.calculation_stopped:
            return float('inf'), float('inf'), None, None, None, None, None
        newMpower = Mpower_base * 1000 / F_base * F
        newMfdot = Mfdot_base / F_base * F
        u = F / newMfdot
        TimeAcc = Mf * 1000 / newMfdot
        MassSum = Mf * 1000 + Mf * 1000 * q + newMpower + Mpn*1000
 
        if MassSum <= newMfdot * TimeAcc:
             QMessageBox.warning(self, "error 552","")
             self.calculation_stopped = True
 
        DistAcc = u * ((TimeAcc - MassSum / newMfdot) * math.log(MassSum / (MassSum - newMfdot * TimeAcc)) + TimeAcc)
        MaxV = u * math.log(MassSum / (MassSum - newMfdot * TimeAcc)) if MassSum > newMfdot * TimeAcc else float('inf')
        RelativeLossCoeff=math.tanh(MaxV/2.998e+8)
        MaxV = RelativeLossCoeff*2.998e+8
 
        DistCruise = Dist - DistAcc
        TimeCruise = DistCruise / MaxV if MaxV > 0 else float('inf')
        if DistAcc > Dist:
             QMessageBox.warning(self, "error 570", "Не успел потратить топливо")
             self.calculation_stopped = True
 
        TimeSum = (TimeAcc + TimeCruise) / 31536000
 
        percent_DistAcc = (DistAcc / Dist) * 100 if Dist > 0 else float('inf')
        MaxAcc = F / (Mf * 1000 + newMpower + Mpn * 1000) / 9.81
        return TimeSum, MaxV, percent_DistAcc, MaxAcc, u, MassSum, TimeAcc
 
    def calculate_two_stage(self, F, Mf, Mpn, q, F_base, Mpower_base, Mfdot_base, Dist, F_end):
 
        if self.calculation_stopped:
            return float('inf'), float('inf'), None, None, None, None, None, None
 
        u = F_base / Mfdot_base
 
        min_TimeSum = float('inf')
        best_F1 = None
        best_M1f = None
        max_v_at_min_t = None
        percent_DistAcc_at_min_t = None
        MaxAcc_at_min_t = None
        MassSum_at_min_t = None
        TimeAcc_at_min_t = None
        best_T1 = None
        best_T2 = None
        best_Mass1 = None
        best_Mass2 = None
        best_D1 = None
        best_D2 = None
        best_V1 = None
        best_V2 = None
        best_DistAcc = None
        best_DistCruise = None
        best_TimeCruise = None
        best_Mdy1 = None
        best_Mdy2 = None
        best_GForce1 = None
        best_GForce2 = None
        M1f = None
        M2f = None
 
        # Инициализация TimeSum
        TimeSum = float('inf')
 
 
        for F1 in np.arange(0.01*F, 0.99 * F, 0.01 * F):  
            for M1f in np.arange(0.01 * Mf, 0.99 * Mf, 0.01 * Mf):  # Начинаем перебор с 0.5 * Mf
                # Если расчеты были остановлены, сбрасываем состояние и выходим из цикла
                if self.calculation_stopped:
                        self.reset_to_initial_state()
                        return
                newMpower = Mpower_base * 1000 / F_base * F
                newMfdot = Mfdot_base / F_base * F
                F2 = F - F1
 
 
                M2f = Mf - M1f
 
                if F_end > F_base:
                  if F1 < F_base or F2 < F_base:
                    break
 
 
 
                M1f_kg = M1f * 1000
                M2f_kg = M2f * 1000
 
                M1dot = Mfdot_base / F_base * F1
                M2dot = Mfdot_base / F_base * F2
 
                # Время работы ступеней
                T1 = M1f_kg / M1dot
                T2 = M2f_kg / M2dot
 
                # Массы ступеней
                Mass2 = M2f_kg + M2f_kg * q + newMpower / F * F2 + Mpn * 1000
                Mass1 = M1f_kg + M1f_kg * q + newMpower / F * F1 + Mass2
 
                # Расстояние, пройденное ступенями
                D1 = u * ((T1 - Mass1 / M1dot) * math.log(Mass1 / (Mass1 - M1dot * T1)) + T1)
                D2 = u * ((T2 - Mass2 / M2dot) * math.log(Mass2 / (Mass2 - M2dot * T2)) + T2)
 
                # Скорости после ступеней
                V1 = u * math.log(Mass1 / (Mass1 - M1dot * T1))
                V2 = u * math.log(Mass2 / (Mass2 - M2dot * T2))
 
 
 
                # Общее расстояние ускорения
                DistAcc = D1 + D2
                DistCruise = Dist - DistAcc
 
                # Время крейсерского полета
                if DistCruise < 0:
                    QMessageBox.warning(self, "error 655","Не успел потратить топливо")
                    self.calculation_stopped = True
                    DistCruise=float('inf')
                    break
                else:
                    MaxV = V1 + V2
 
                    RelativeLossCoeff=math.tanh(MaxV/2.998e+8)
                    MaxV = RelativeLossCoeff*2.998e+8
                    if MaxV > 0:
                        TimeCruise = DistCruise / MaxV 
                    else:
                        QMessageBox.warning(self, "error 662","Слишком маленькая скорость")
                        self.calculation_stopped = True
                        TimeCruise = float('inf')
                        break
 
                # Общее время ускорения
                TimeAcc = T1 + T2
                TimeSum = (TimeAcc + TimeCruise) / 31536000  # Перевод в годы
 
                # Расчет максимального ускорения (g-force) для первой и второй ступени
                GForce1 = F1 / (Mass1 - M1dot * T1) / 9.81
                GForce2 = F2 / (Mass2 - M2dot * T2) / 9.81
 
                # Масса двигательной установки (ДУ) первой и второй ступени
                Mdy1 = newMpower / F * F1
                Mdy2 = newMpower / F * F2
 
                # Обновление минимального времени полета
                if TimeSum < min_TimeSum:
                  min_TimeSum = TimeSum
                  best_F1 = F1
                  best_M1f = M1f
                  max_v_at_min_t = V1 + V2
                  percent_DistAcc_at_min_t = (DistAcc / Dist) * 100 if Dist > 0 else float('inf')
                  MaxAcc_at_min_t = max(GForce1, GForce2)
                  MassSum_at_min_t = Mass1 / 1000  # Mass1 уже включает Mass2
                  TimeAcc_at_min_t = TimeAcc
                  best_T1 = T1
                  best_T2 = T2
                  best_Mass1 = Mass1
                  best_Mass2 = Mass2
                  best_D1 = D1
                  best_D2 = D2
                  best_V1 = V1
                  best_V2 = V2
                  best_DistAcc = DistAcc
                  best_DistCruise = DistCruise
                  best_TimeCruise = TimeCruise
                  best_Mdy1 = Mdy1
                  best_Mdy2 = Mdy2
                  best_GForce1 = GForce1
                  best_GForce2 = GForce2
 
        return min_TimeSum, best_F1, best_M1f, max_v_at_min_t, percent_DistAcc_at_min_t, MaxAcc_at_min_t, u, MassSum_at_min_t, TimeAcc_at_min_t, best_T1, best_T2, best_Mass1, best_Mass2, best_D1, best_D2, best_V1, best_V2, best_DistAcc, best_DistCruise, max_v_at_min_t, best_TimeCruise, best_Mdy1, best_Mdy2, best_GForce1, best_GForce2
 
    def plot_graph(self):
        self.calculation_stopped = False
        try:
            F_start = float(self.entry_F_start.text().replace(',', '.'))
            F_end = float(self.entry_F_end.text().replace(',', '.'))
            Mf_start = float(self.entry_Mf_start.text().replace(',', '.'))
            Mf_end = float(self.entry_Mf_end.text().replace(',', '.'))
            stepF = float(self.entry_stepF.text().replace(',', '.'))
            stepMf = float(self.entry_stepMf.text().replace(',', '.'))
            Dist = float(self.entry_Dist.text().replace(',', '.')) * 9.461e15
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, введите корректные числа.")
            return
        # Проверка на корректность введенных значений
        if F_end <= F_start:
            QMessageBox.critical(self, "Ошибка", "Конечное значение тяги должно быть больше начального.")
            return
        if Mf_end <= Mf_start:
            QMessageBox.critical(self, "Ошибка", "Конечное значение массы топлива должно быть больше начального.")
            return
 
        self.progress_bar.setMaximum(int((F_end - F_start) / stepF * (Mf_end - Mf_start) / stepMf))
        self.progress_bar.setValue(0)
 
        masses = []
        times = []
 
        F = F_start
        while F <= F_end and not self.calculation_stopped:
            Mf = Mf_start
            while Mf <= Mf_end and not self.calculation_stopped:
                if self.two_stage_checkbox.isChecked():
                    # Используем только current_value, остальные значения игнорируем
                    current_value, *_ = self.calculate_two_stage(F, Mf, float(self.entry_Mpn.text().replace(',', '.')), float(self.entry_q.text().replace(',', '.')), float(self.entry_F_base.text().replace(',', '.')), float(self.entry_Mpower_base.text().replace(',', '.')), float(self.entry_Mfdot_base.text().replace(',', '.')), Dist, F_end)
                else:
                    current_value, *_ = self.calculate_single_stage(F, Mf, float(self.entry_Mpn.text().replace(',', '.')), float(self.entry_q.text().replace(',', '.')), float(self.entry_F_base.text().replace(',', '.')), float(self.entry_Mpower_base.text().replace(',', '.')), float(self.entry_Mfdot_base.text().replace(',', '.')), Dist)
                if current_value != float('inf'):
                    times.append(current_value)
                    masses.append(Mf)
                Mf += stepMf
                self.progress_bar.setValue(self.progress_bar.value() + 1)
                QApplication.processEvents()
            F += stepF
 
        # Отображаем график на вкладке
        self.figure.clear()
        ax = self.figure.add_subplot(1,7,(2,7))
 
        # Применяем стиль "cyberpunk"
        plt.style.use("cyberpunk")
 
        self.figure.patch.set_facecolor('#222946')
        ax.set_facecolor('#222946')
        scatter = ax.scatter(masses, times, c=times, cmap='cool', marker='o')
        ax.set_title('Зависимость времени полета от массы топлива', fontsize=8, color='white')
        ax.set_xlabel('Масса топлива (тонн)', fontsize=8, color='white')
        ax.set_ylabel('Время полета (лет)', fontsize=8, color='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.grid(True)
 
        # Добавляем дополнительные эффекты из mplcyberpunk
        mplcyberpunk.add_glow_effects()
 
        self.canvas.draw()
 
        # Переключаемся на вкладку с графиком
        self.tabs.setCurrentIndex(1)
        self.reset_to_initial_state()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RocketCalculatorApp()
    window.show()
    sys.exit(app.exec())
