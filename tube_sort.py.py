import random
from copy import deepcopy

class Tube:
    def __init__(self, items=None, max_size=4):
        self.max_size = max_size
        self.items = items if items else []

    def is_empty(self):
        return len(self.items) == 0

    def is_full(self):
        return len(self.items) == self.max_size

    def top_item(self):
        return self.items[-1] if not self.is_empty() else None

    def can_receive(self, item):
        return (not self.is_full()) and (self.is_empty() or self.top_item() == item)

    def add_item(self, item):
        if self.can_receive(item):
            self.items.append(item)
            return True
        return False

    def pour_into(self, other_tube):
        if not self.is_empty() and other_tube.can_receive(self.top_item()):
            item = self.items.pop()
            other_tube.add_item(item)
            return True
        return False

    def is_completed(self):
        if self.is_empty():
            return True
        return len(set(self.items)) == 1 and len(self.items) == 4

    def __str__(self):
        return " ".join(self.items) if self.items else "[Пусто]"

class Game:
    def __init__(self):
        self.tubes = []
        self.setup_game()

    def setup_game(self):
        colors = ['A', 'B', 'C', 'D']
        items = colors * 4 
        random.shuffle(items)
        
        self.tubes = []
        for i in range(4):
            self.tubes.append(Tube(items[i*4:(i+1)*4]))
        for _ in range(2):
            self.tubes.append(Tube())

    def is_level_complete(self):
        return all(tube.is_completed() for tube in self.tubes)

    def move_item(self, from_idx, to_idx):
        if 0 <= from_idx < len(self.tubes) and 0 <= to_idx < len(self.tubes):
            return self.tubes[from_idx].pour_into(self.tubes[to_idx])
        return False

    def display(self):
        print("\n" + "="*30)
        for i, tube in enumerate(self.tubes):
            print(f"{i+1}: {tube}")
        print("="*30)

    def play(self):
        print("=== Игра: Сортировка колб ===")
        print("Правила:")
        print("- 6 колб: 4 заполнены (по 4 предмета), 2 пустые")
        print("- Перемещайте верхний предмет из одной колбы в другую")
        print("- Можно класть предмет только на такой же или в пустую колбу")
        print("- Уровень пройден, когда в каждой колбе 4 одинаковых предмета или она пуста\n")

        moves = 0
        while not self.is_level_complete():
            self.display()
            try:
                from_tube = int(input("Откуда перемещаем (1-6)? ")) - 1
                to_tube = int(input("Куда перемещаем (1-6)? ")) - 1
                if self.move_item(from_tube, to_tube):
                    moves += 1
                else:
                    print("⚠ Неверный ход! Проверьте правила.")
            except ValueError:
                print("⚠ Введите числа от 1 до 6!")

        print(f"\n🎉 Поздравляем! Уровень пройден за {moves} ходов!")
        self.display()

if __name__ == "__main__":
    game = Game()
    game.play()