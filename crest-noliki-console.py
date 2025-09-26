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
    if all(all_pieces(game.board)):  # all() вернет True если нет None
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


def play(piece):
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
            play(piece)  # Рекурсивный вызов для повторного хода


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


# Основная игровая логика
game = Game()

while True:
    for piece in ['x', 'o']:  # Поочередные ходы
        play(piece)
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
                break
            game = Game()  # Новая игра