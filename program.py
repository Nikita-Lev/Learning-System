import sys
import random
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
            QLabel,
            QComboBox,
            QLineEdit,
            QPushButton,
            QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QCheckBox
)
from PyQt5.QtCore import QSize, Qt, QObject
from PyQt5.QtGui import QPixmap
from Educator import Ui_MainWindow



# Ответы на задания
class Answers:
    def __init__(self, edNames, answs):
        # Количество полей ввода
        self.edN = len(edNames)
        
        # Список названий кнопок
        self.edNames = edNames
        
        # Ответы на задания
        self.answs = answs
         
        
# Ответы в виде чисел
class AnswerNum(Answers):
    def __init__(self, edNames, answs, order = True):
        super().__init__(edNames, answs)
    
        # Важен ли порядок ответов
        self.order = order
        
    
    # Проверка правильности ответов
    def CheckAnswers(self, userAnsws, taskNum):
        # Если не важен порядок ответов, сравнивать как множества
        if self.order == False:
            return set(userAnsws) == set(self.answs[taskNum])
        
        return userAnsws == self.answs[taskNum]
    
    
    # Формирование виджетов
    def CreateWidgets(self):
        # Список полей ввода ответов и кнопок
        self.edits = QHBoxLayout()
        for editText in self.edNames:
            edit = QLineEdit()
            edit.setMaxLength(10)
            edit.setPlaceholderText(editText)
            edit.setFixedWidth(100)
            
            self.edits.addWidget(edit)    


# Ответы в виде выбора вариантов
class AnswerVar(Answers):
    def __init__(self, edNames, answs):
        super().__init__(edNames, answs)
        
    
    # Проверка правильности ответов
    def CheckAnswers(self, userAnsws, taskNum):
        pass
    
    
    # Формирование виджетов
    def CreateWidgets(self):
        # Список полей ввода ответов и кнопок
        self.edits = QHBoxLayout()
        
        self.variants = QVBoxLayout()
        
        for editText in self.edNames:
            edit = QCheckBox(editText)
            
            self.variants.addWidget(edit)
        
        self.edits.addLayout(self.variants)  

# Поля для ввода ответов и ответы
answers = [AnswerNum(['X', 'Y'],
                   [['3', '-2'], ['-1', '-2'], ['2', '3']]),
           AnswerNum(['X'],
                   [['3'], ['3.5'], ['0']]),
           AnswerNum(['X1', 'X2'],
                   [['2', '5'], ['2', '3'], ['2', '3'], ['0.4', '1.2'], ['-20', '15'], ['-5', '-3'], ['-5', '-3'], ['-', '-'], ['-19', '2']], order = False),
           AnswerNum(['X'],
                   [['-6'], ['4'], ['2'], ['10']]),
           AnswerNum(['X1', 'X2'],
                   [['-27', '-1'], ['-1', '7']], order = False),
           AnswerNum(['X'],
                   [['-'], ['-26'], ['-2'], ['-7'], ['-3'], ['-1.5'], ['-6'], ['-1']]),
           AnswerNum(['X'],
                   [['-'], ['2'], ['26'], ['4'], ['13'], ['28'], ['6']]),
           AnswerNum(['X'],
                   [['-'], ['-1'], ['-'], ['2'], ['1']]),
           AnswerVar(['A', 'B', 'C', 'D'], [[0], [1]])
           ]

# путь к файлам
dirs = ['Системы уравнений/', 'Показательные уравнения/',
        'Квадратное уравнение/', 'Линейные уравнения с одной переменной/',
        'Дробно-рациональные уравнения/', 'Иррациональные уравнения/',
        'Логарифмические уравнения/', 'Уравнения с модулем/',
        'Биквадратные уравнения/']

# Заголовок заданий
taskTitles = ['Решите систему уравнений', 'Решите показательное уравнение',
              'Решите квадратное уравнение', 'Решите линейное уравнение', 
              'Решение дробно-рациональное уравнение', 'Решите иррациональное уравнение',
              'Решите логарифмическое уравнение', 'Решите уравнение с модулем',
              'Решите биквадратное уравнение']
# Названия методов
methodNames = [['Метод подстановки', 'Метод исключения'],
               ['Графический', 'Уравнивание показателей', 'Введение новой переменной', 'Однородные уравнения'],
               ['Дискриминант', 'Теорема Виета'],
               ['Метод решения'],
               ['Метод пропорций', 'Метод избавления от дробей'],
               ['Метод 1', 'Метод 2', 'Метод 3', 'Метод 4', 'Метод 5', 'Метод 6'],
               ['Метод потенциирования', 'Простейшие логарифмические уравнения'],
               ['Метод 1', 'Метод 2', 'Метод 3'],
               ['Метод введения новой переменной']
               ]



# Общая схема
class MentalScheme(QWidget):
    def __init__(self, imgN):
        super().__init__()
        
        self.imgL = QHBoxLayout()
        
        self.img = QLabel()
        self.img.setPixmap(QPixmap(dirs[imgN] + 'main.jpg'))
        
        self.imgL.addWidget(self.img)
    
        self.setLayout(self.imgL)

# Методы решений
class SolutionMethods(QWidget):
    def __init__(self, themNum):
        super().__init__()
        
        self.themNum = themNum
        self.names = methodNames[self.themNum]
        self.method = QLabel()
        
        self.VBox = QVBoxLayout() # Вертикальный контейнер
        
        n = len(self.names)
        # Если методов несколько, создать кнопки выбора
        if n > 1:
            self.HBox = QHBoxLayout() # Горизонтальный контейнер
            
            for i in range(n):
                but = QPushButton(self.names[i])
                but.setObjectName(f'{i}')
                but.clicked.connect(self.MethodChoice)
                
                # but.clicked.connect(lambda ch, btn=but: self.MethodChoice(btn))
                
                self.HBox.addWidget(but) # Расположение кнопок в строку
            
            self.VBox.addLayout(self.HBox) # Добавление набора кнопок в контейнер
        # Иначе отобразить метод
        else:
            self.ShowMethod(0)
        
        self.VBox.addStretch()
        self.setLayout(self.VBox)
        
    # Выбор метода
    def MethodChoice(self):
        numb = int(self.sender().objectName())
        self.ShowMethod(numb)
    
    # Показать метод решения
    def ShowMethod(self, mNum):
        # Отображение методов решений
        self.method.setPixmap(QPixmap(dirs[self.themNum] + f'method {mNum}'))
        self.VBox.addWidget(self.method) # Добавление картинок в контейнер


# Вкладка с заданиями
class TaskTab(QWidget):
    def __init__(self, themNum):
        super().__init__()
    
        self.themNum = themNum
        
        self.answers = answers[themNum]
        self.answers.CreateWidgets()
        
        self.layout = QVBoxLayout()
        
        self.taskNm = 0 # Номер задания
        self.tNms = len(self.answers.answs) # Всего заданий
        
        self.lbl = QLabel(taskTitles[self.themNum] + f' ({self.taskNm+1}/{self.tNms})' +'\nНет корня — прочерк (-)') # Заголовок задания и счётчик
        self.layout.addWidget(self.lbl)
        
        # Случайная последовательность заданий
        self.taskNums = list(range(self.tNms)) 
        random.shuffle(self.taskNums)
        
        # Изображение задания
        self.taskImg = QLabel()
        self.taskImg.setPixmap(QPixmap(dirs[self.themNum] + f'{self.taskNums[self.taskNm]}.jpg'))
        
        self.layout.addWidget(self.taskImg)
        
        self.score = [False] * self.tNms # Результаты
        
        # Кнопка перехода на следующее задание
        self.nextBut = QPushButton()
        self.nextBut.clicked.connect(self.ChangeTask)
        
        self.layout.addLayout(self.answers.edits) # Добавление полей ввода и кнопок
        
        self.setLayout(self.layout)
        
    
    # Проверка ответов
    def CheckAnswer(self):
        res = self.answers.CheckAnswers([self.answers.edits.itemAt(i).widget().text() for i in range(self.answers.edN)], self.taskNums[self.taskNm])
        if res == True:
            self.score[self.taskNm] = True # Записать в счёт результатов
        return res
    
    # Изменить пример
    def ChangeTask(self):
        # Проверить правильность введённого ответа
        self.CheckAnswer()
        
        # Очистка полей ввода
        for i in range(self.answers.edN): 
            self.answers.edits.itemAt(i).widget().clear()
        
        self.taskNm += 1 # Увеличение номера задания
        
        # Если задания закончились, вывести общие результаты
        if self.taskNm == self.tNms:
            # Очистка layout
            while self.layout.count():
                child = self.layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            # Таблица результатов
            self.results = QTableWidget()
            self.results.setColumnCount(2)
            self.results.setRowCount(self.tNms+1)
            self.results.setHorizontalHeaderLabels(["Номер задания", "Результат"])
            
            # Заполнение результатов
            for i in range(self.tNms):
                self.results.setItem(i, 0, QTableWidgetItem(str(i+1)))
                if self.score[i] == True:
                    self.results.setItem(i, 1, QTableWidgetItem("Верно"))
                else:
                    self.results.setItem(i, 1, QTableWidgetItem("Не верно"))
            
            # Итоговый результат
            
            self.results.setItem(len(self.score), 0, QTableWidgetItem('Результат'))
            self.results.setItem(len(self.score), 1, QTableWidgetItem(str(round(sum(self.score) / len(self.score) * 100)) + '%'))
            
            self.layout.addWidget(self.results)
            
            # Начать заново
            #self.retry = QPushButton('Начать заново')
            #self.retry.clicked.connect(self.retryTest)
            #self.layout.addWidget(self.retry)
            
        else:
            # Обновить номер задания
            self.lbl.setText(taskTitles[self.themNum] + f' ({self.taskNm+1}/{self.tNms})')
        
            # Обновить задание
            self.taskImg.setPixmap(QPixmap(dirs[self.themNum] + f'{self.taskNums[self.taskNm]}.jpg'))
            
    def retryTest(self):
        pass

# Вкладка тренировочных заданий
class TrainTab(TaskTab):
    def __init__(self, themNum):
        super().__init__(themNum)
        
        
        self.msg = QLabel() # Сообщение о правильности решения
        self.solutionImg = QLabel() # Изображение решения
        
        self.mist = 0 # Признак ответа
        
        # Кнока показа решения
        self.solutionBut = QPushButton('Показать решение')
        self.solutionBut.clicked.connect(self.ShowSolution)
        self.answers.edits.addWidget(self.solutionBut)
        
        # Добавление кнопки решить ещё
        self.nextBut.setText('Решить ещё')
        self.answers.edits.addWidget(self.nextBut)

        # Кнопка проверки ответа
        self.check = QPushButton('Проверить')
        self.check.clicked.connect(self.MsgAnswer)
        
        self.layout.addWidget(self.check)
        
        self.layout.addStretch() # Прижатие виджетов к верху страницы
        
    # Показать решение
    def ShowSolution(self):
        self.msg.clear()
        self.solutionImg.setPixmap(QPixmap(dirs[self.themNum] + f'{self.taskNums[self.taskNm]}_s.jpg'))
        self.layout.addWidget(self.solutionImg)
        self.solutionBut.setEnabled(False)
        
    # Сообщение о правильности ответа
    def MsgAnswer(self):
        if self.mist == 1:
            self.msg.clear()
        
        # Вывод сообщения о правильности ответа
        if self.CheckAnswer() == True:
            self.msg.setText('Решено верно!')
        else:
            self.msg.setText('Не верно, попробуйте ещё раз')
        
        self.layout.addWidget(self.msg, Qt.AlignHCenter)
        
        self.mist = 1
        
    # Смена задания
    def ChangeTask(self):
        super().ChangeTask() # очистка полей ввода
        
        # Убрать лишние элементы
        self.msg.clear()
        self.solutionBut.setEnabled(True)
        self.solutionImg.clear()
        self.mist = 0
        

# Вкладка контрольных заданий
class ControlTab(TaskTab):
    def __init__(self, themNum):
        super().__init__(themNum)
        
        # Добавление кнопки Подтвердить
        self.nextBut.setText('Подтвердить')
        self.layout.addWidget(self.nextBut)
        
        self.layout.addStretch() # Прижатие виджетов к верху страницы

# Приложение
class LearningSystemApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
        
        
        
        self.comboBox.currentIndexChanged.connect(self.ChangeTheme)
        
        self.theme = self.comboBox.currentIndex() # выбранная тема
        
        
        # Вкладки
        self.scheme = QStackedWidget()
        self.methods = QStackedWidget()
        self.trainTab = QStackedWidget()
        self.controlTab = QStackedWidget()
        
        # Добавление виджетов на вкладки
        for i in range(len(taskTitles)):
            self.scheme.addWidget(MentalScheme(i))
            self.methods.addWidget(SolutionMethods(i))
            self.trainTab.addWidget(TrainTab(i))
            self.controlTab.addWidget(ControlTab(i))
        
        # Добавление вкладок
        self.tabs.addTab(self.scheme, 'Общая схема')
        self.tabs.addTab(self.methods, 'Метод решения')
        self.tabs.addTab(self.trainTab, 'Тренировочные задания')
        self.tabs.addTab(self.controlTab, "Контрольные задания")
        
        # Начальное отображение первой темы
        self.scheme.setCurrentIndex(self.theme)
        self.methods.setCurrentIndex(self.theme)
        self.trainTab.setCurrentIndex(self.theme)
        self.controlTab.setCurrentIndex(self.theme)
        

    
    # Изменение темы
    def ChangeTheme(self, ind):
        # Общая схема
        self.scheme.setCurrentIndex(ind)
        
        # Методы решения
        self.methods.setCurrentIndex(ind)
        
        # Тренировочные задания
        self.trainTab.setCurrentIndex(ind)
        
        # Контрольные задания
        self.controlTab.setCurrentIndex(ind)
        
        
def main():
    app = QApplication(sys.argv)

    window = LearningSystemApp()
    window.show()

    app.exec()

    
if __name__ == '__main__':
    main()