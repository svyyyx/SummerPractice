import tkinter as tk
from tkinter import messagebox
from random import randint
from termcolor import colored, cprint


class Game:
    def __init__(self) -> None:
        # Создание пустой доски 3x3 (None - пустая клетка)
        self.board = [[None for i in range(3)] for i in range(3)]

    def display_board(self, numbers=None):
        # Определяем, показывать ли номера строк/столбцов
        show_numbers_x = True if numbers == 'x' or numbers == 'both' else False
        show_numbers_y = True if numbers == 'y' or numbers == 'both' else False

        for row_count, row in enumerate(self.board):
            # Разделительная линия между строками (кроме первой)
            if row_count != 0:
                print(f'\n   {"-" * 10}')

            for col_count, col in enumerate(row):
                # Показываем номера строк слева
                if col_count == 0 and show_numbers_x:
                    print(str(row_count + 1), ' ', end="")
                elif col_count == 0:
                    print('   ', end="")

                # Заменяем None на пробел для красивого отображения
                col = ' ' if col is None else col
                print(col, end="")

                # Вертикальные разделители между столбцами
                if col_count != 2:
                    print(" | ", end="")

            # После последней строки добавляем номера столбцов
            if row_count == 2:
                if show_numbers_y:
                    print("\n\n   1   2   3", end="")
                print('\n')

    def place_piece(self, piece, x_pos, y_pos):
        # Размещение фигуры на доске
        self.board[x_pos][y_pos] = piece


# Лямбда-функция для проверки, все ли элементы в списке одинаковы
all_equal = lambda iterable: iterable.count(iterable[0]) == len(iterable)


def all_pieces(board):
    # Собираем все фигуры с доски в один список
    all_pieces = list()
    for row in range(3):
        for column in range(3):
            all_pieces.append(board[row][column])
    return all_pieces


def check_win(board):
    # Проверка ничьи (все клетки заполнены)
    if all(all_pieces(board)):  # all() вернет True если нет None
        return 'Ничья'

    # Проверка строк на победу
    for row in board:
        if all_equal(row) and all(row):  # all(row) проверяет что нет None
            return 'Победа'

    # Проверка столбцов на победу
    for i in range(3):
        column = [board[0][i], board[1][i], board[2][i]]
        if all_equal(column) and all(column):
            return 'Победа'

    # Проверка диагоналей
    tl_br = [board[0][0], board[1][1], board[2][2]]  # Слева-направо ↘
    tr_bl = [board[0][2], board[1][1], board[2][0]]  # Справа-налево ↙
    for cross in [tl_br, tr_bl]:
        if all_equal(cross) and all(cross):
            return 'Победа'

    # Игра продолжается
    return False


def computerMove(board):
    # Умный ИИ: проверяет возможные победы/поражения
    for row_count, row in enumerate(board):
        for col_count, column in enumerate(row):
            if column == None:  # Если клетка свободна
                # Проверяем оба варианта: может ли X или O выиграть
                for piece in ['x', 'o']:
                    board[row_count][col_count] = piece  # Временная установка фигуры
                    if check_win(board) == 'Победа':
                        # Нашли выигрышный ход - возвращаем его
                        return row_count, col_count
                    board[row_count][col_count] = None  # Откатываем изменение

    # Если нет выигрышных ходов - случайный ход
    random_move = [randint(0, 2), randint(0, 2)]
    # Повторяем пока не найдем свободную клетку
    while board[random_move[0]][random_move[1]] != None:
        random_move = [randint(0, 2), randint(0, 2)]
    return random_move


class TicTacToeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Крестики-нолики")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        # Настройка цветов
        self.bg_color = "#f0f0f0"
        self.button_color = "#ffffff"
        self.x_color = "#ff6b6b"  # Красный для X
        self.o_color = "#4ecdc4"  # Бирюзовый для O
        self.font = ("Arial", 20, "bold")

        self.root.configure(bg=self.bg_color)

        # Создание игры
        self.game = Game()

        # Создание интерфейса
        self.create_widgets()

        # Кто ходит первым (True - человек, False - компьютер)
        self.human_turn = True

    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(self.root, text="Крестики-нолики",
                               font=("Arial", 24, "bold"),
                               bg=self.bg_color,
                               fg="#333333")
        title_label.pack(pady=20)

        # Статус игры
        self.status_label = tk.Label(self.root, text="Ваш ход (X)",
                                     font=("Arial", 16),
                                     bg=self.bg_color,
                                     fg="#333333")
        self.status_label.pack(pady=10)

        # Игровое поле
        self.board_frame = tk.Frame(self.root, bg=self.bg_color)
        self.board_frame.pack(pady=20)

        # Создание кнопок для игрового поля
        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(self.board_frame,
                                   text="",
                                   font=self.font,
                                   width=6,
                                   height=3,
                                   bg=self.button_color,
                                   relief="raised",
                                   bd=3,
                                   command=lambda row=i, col=j: self.human_move(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        # Панель управления
        control_frame = tk.Frame(self.root, bg=self.bg_color)
        control_frame.pack(pady=20)

        # Кнопка новой игры
        new_game_btn = tk.Button(control_frame,
                                 text="Новая игра",
                                 font=("Arial", 14),
                                 bg="#6a89cc",
                                 fg="white",
                                 relief="raised",
                                 bd=2,
                                 command=self.new_game)
        new_game_btn.pack(side=tk.LEFT, padx=10)

        # Кнопка выхода
        exit_btn = tk.Button(control_frame,
                             text="Выход",
                             font=("Arial", 14),
                             bg="#e55039",
                             fg="white",
                             relief="raised",
                             bd=2,
                             command=self.root.quit)
        exit_btn.pack(side=tk.LEFT, padx=10)

        # Информация о игре
        info_label = tk.Label(self.root,
                              text="Вы играете за X, компьютер за O",
                              font=("Arial", 12),
                              bg=self.bg_color,
                              fg="#666666")
        info_label.pack(pady=10)

        # Консольный вывод (опционально)
        self.console_frame = tk.Frame(self.root, bg=self.bg_color)
        self.console_frame.pack(pady=10)

        console_label = tk.Label(self.console_frame,
                                 text="Консольный вывод:",
                                 font=("Arial", 10),
                                 bg=self.bg_color,
                                 fg="#666666")
        console_label.pack()

        self.console_text = tk.Text(self.console_frame,
                                    height=4,
                                    width=40,
                                    font=("Courier", 8))
        self.console_text.pack()

    def update_board(self):
        """Обновляет отображение игрового поля"""
        for i in range(3):
            for j in range(3):
                piece = self.game.board[i][j]
                if piece == 'x':
                    self.buttons[i][j].config(text="X", fg=self.x_color, state="disabled")
                elif piece == 'o':
                    self.buttons[i][j].config(text="O", fg=self.o_color, state="disabled")
                else:
                    self.buttons[i][j].config(text="", state="normal")

    def human_move(self, row, col):
        """Обработка хода человека"""
        if not self.human_turn or self.game.board[row][col] is not None:
            return

        # Ход человека
        self.game.place_piece('x', row, col)
        self.update_board()
        self.log_to_console(f"Вы поставили X на позицию ({row + 1}, {col + 1})")

        # Проверка результата
        result = check_win(self.game.board)
        if result:
            self.game_over(result)
            return

        # Переход хода к компьютеру
        self.human_turn = False
        self.status_label.config(text="Ход компьютера...")

        # Задержка перед ходом компьютера для лучшего UX
        self.root.after(1000, self.computer_move)

    def computer_move(self):
        """Ход компьютера"""
        if self.human_turn:
            return

        move = computerMove(self.game.board)
        self.game.place_piece('o', move[0], move[1])
        self.update_board()
        self.log_to_console(f"Компьютер поставил O на позицию ({move[0] + 1}, {move[1] + 1})")

        # Проверка результата
        result = check_win(self.game.board)
        if result:
            self.game_over(result)
            return

        # Переход хода к человеку
        self.human_turn = True
        self.status_label.config(text="Ваш ход (X)")

    def game_over(self, result):
        """Обработка окончания игры"""
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state="disabled")

        if result == 'Победа':
            winner = "Вы победили!" if not self.human_turn else "Компьютер победил!"
            self.status_label.config(text=winner)
            self.log_to_console(f"*** {winner} ***")
            messagebox.showinfo("Игра окончена", winner)
            cprint('GG', 'green', 'on_blue')
        else:
            self.status_label.config(text="Ничья!")
            self.log_to_console("*** Ничья! ***")
            messagebox.showinfo("Игра окончена", "Ничья!")
            cprint('GG', 'green', 'on_blue')

    def new_game(self):
        """Начать новую игру"""
        self.game = Game()
        self.human_turn = True
        self.status_label.config(text="Ваш ход (X)")
        self.update_board()
        self.log_to_console("=== Новая игра ===")

    def log_to_console(self, message):
        """Добавляет сообщение в консольный вывод"""
        self.console_text.insert(tk.END, message + "\n")
        self.console_text.see(tk.END)

    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


def play_console():
    """Оригинальная консольная версия игры"""
    game = Game()

    while True:
        for piece in ['x', 'o']:  # Поочередные ходы
            print(f"Ход {piece.upper()}-ов")

            # Ход компьютера (всегда 'O')
            if piece == 'o':
                move = computerMove(game.board)
                game.place_piece('o', move[0], move[1])
            else:
                # Ход человека
                game.display_board(numbers='y')  # Показываем номера столбцов
                y_pos = int(input("Выбери позицию по Y: ")) - 1  # Столбец
                game.display_board(numbers='x')  # Показываем номера строк
                x_pos = int(input("Выбери позицию по X: ")) - 1  # Строка

                # Проверка, что клетка свободна
                if game.board[x_pos][y_pos] == None:
                    game.place_piece(piece, x_pos, y_pos)
                else:
                    print("Место занято, попробуйте выбрать другое место.")
                    continue  # Пропускаем проверку победы и продолжаем ход

            game.display_board()
            result = check_win(game.board)

            # Проверка окончания игры
            if result == 'Победа' or result == 'Ничья':
                game.display_board()
                print('-' * 20)
                if result == 'Победа':
                    print(piece.upper(), 'Победил!')  # Текущий игрок победил
                else:
                    print('Ничья')
                print('-' * 20)

                # Предложение сыграть again
                restart = input('Сыграть заново? [д/н]? ')
                cprint('GG', 'green', 'on_blue')
                if restart.lower() == 'н':
                    return
                game = Game()  # Новая игра
                break  # Выходим из цикла for и начинаем новую игру


def main():
    """Главная функция с выбором режима игры"""
    print("Выберите режим игры:")
    print("1 - Графический интерфейс")
    print("2 - Консольная версия")

    choice = input("Ваш выбор (1 или 2): ")

    if choice == "1":
        app = TicTacToeGUI()
        app.run()
    elif choice == "2":
        play_console()
    else:
        print("Неверный выбор, запускаю графический интерфейс...")
        app = TicTacToeGUI()
        app.run()


if __name__ == "__main__":
    main()