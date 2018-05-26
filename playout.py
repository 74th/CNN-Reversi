from typing import Tuple, List
import random
import copy


class Board():
    def __init__(self, size: int):
        self.size: int = size
        self.blacks: List[int] = [0 for i in range(size * size)]
        self.whites: List[int] = [0 for i in range(size * size)]
        self.enable: List[int] = [0 for i in range(size * size)]
        self.player: int = 0  # 0=black,1=white
        self.blacks[(int(size / 2) - 1) * size + int(size / 2) - 1] = 1
        self.blacks[int(size / 2) * size + int(size / 2)] = 1
        self.whites[int(size / 2) * size + int(size / 2) - 1] = 1
        self.whites[(int(size / 2) - 1) * size + int(size / 2)] = 1
        self.makeEnable()

    def Print(self):
        print(" ", end="")
        for i in range(self.size):
            print(i, end="")
        for i in range(self.size * self.size):
            if i % self.size == 0:
                print("")
                print(int(i / self.size), end="")
            if self.blacks[i] == 1:
                print("*", end="")
            elif self.whites[i] == 1:
                print("0", end="")
            elif self.enable[i] == 1:
                print("_", end="")
            else:
                print(".", end="")
        print("")

    def makeEnable(self):
        for i in range(self.size * self.size):
            self.enable[i] = self._isEnable(self.player, i)

    def xy(self, n: int) -> Tuple[int]:
        return (n % self.size, int(n / self.size))

    def n(self, x: int, y: int) -> int:
        return self.size * y + x

    def _isEnable(self, player: int, n: int) -> int:
        if self.player == 0:
            me = self.blacks
            victim = self.whites
        else:
            me = self.whites
            victim = self.blacks
        x, y = self.xy(n)
        if self.blacks[n] > 0 or self.whites[n] > 0:
            # すでに置かれていないこと
            return 0
        if self._isEnableLeft(victim, me, x, y):
            return 1
        if self._isEnableRight(victim, me, x, y):
            return 1
        if self._isEnableUp(victim, me, x, y):
            return 1
        if self._isEnableDown(victim, me, x, y):
            return 1
        if self._isEnableLeftUp(victim, me, x, y):
            return 1
        if self._isEnableLeftDown(victim, me, x, y):
            return 1
        if self._isEnableRightUp(victim, me, x, y):
            return 1
        if self._isEnableRightDown(victim, me, x, y):
            return 1
        return 0

    def _isEnableLeft(self, victim: List[int], me: List[int], x: int, y: int) -> bool:
        if x < 2:
            # 左に2つ以上間がない
            return False
        if victim[self.n(x - 1, y)] != 1:
            # 左は敵の色である
            return False
        for x2 in range(x - 2, -1, -1):
            if me[self.n(x2, y)] == 1:
                # 自分の色で挟んでいる
                return True
            if victim[self.n(x2, y)] == 0:
                # 相手の色が続かない
                return False
        # 自分の色で挟んでいない
        return False

    def _isEnableRight(self, victim: List[int], me: List[int], x: int, y: int) -> bool:
        if x + 2 >= self.size:
            # 右に2つ以上間がない
            return False
        if victim[self.n(x + 1, y)] != 1:
            # 左は敵の色でなければならない
            return False
        for x2 in range(x + 2, self.size, 1):
            if me[self.n(x2, y)] == 1:
                # 自分の色で挟んでいる
                return True
            if victim[self.n(x2, y)] == 0:
                # 相手の色が続かない
                return False
        # 自分の色で挟んでいない
        return False

    def _isEnableUp(self, victim: List[int], me: List[int], x: int, y: int) -> bool:
        if y < 2:
            # 左に2つ以上間がない
            return False
        if victim[self.n(x, y - 1)] != 1:
            # 左は敵の色である
            return False
        for y2 in range(y - 2, -1, -1):
            if me[self.n(x, y2)] == 1:
                # 自分の色で挟んでいる
                return True
            if victim[self.n(x, y2)] == 0:
                # 相手の色が続かない
                return False
        # 自分の色で挟んでいない
        return False

    def _isEnableDown(self, victim: List[int], me: List[int], x: int, y: int) -> bool:
        if y + 2 >= self.size:
            # 右に2つ以上間がない
            return False
        if victim[self.n(x, y + 1)] != 1:
            # 左は敵の色でなければならない
            return False
        for y2 in range(y + 2, self.size, 1):
            if me[self.n(x, y2)] == 1:
                # 自分の色で挟んでいる
                return True
            if victim[self.n(x, y2)] == 0:
                # 相手の色が続かない
                return False
        # 自分の色で挟んでいない
        return False

    def _isEnableLeftUp(self, victim: List[int], me: List[int], x: int, y: int) -> bool:
        if x < 2 or y < 2:
            # 左に2つ以上間がない
            return False
        if victim[self.n(x - 1, y - 1)] != 1:
            # 左は敵の色である
            return False
        y2 = y - 1
        for x2 in range(x - 2, -1, -1):
            y2 = y2 - 1
            if y2 < 0:
                # 自分の色で挟んでいない
                return False
            if me[self.n(x2, y2)] == 1:
                # 自分の色で挟んでいる
                return True
            if victim[self.n(x2, y2)] == 0:
                # 相手の色が続かない
                return False
        # 自分の色で挟んでいない
        return False

    def _isEnableLeftDown(self, victim: List[int], me: List[int], x: int, y: int) -> bool:
        if x < 2 or y + 2 >= self.size:
            # 左に2つ以上間がない
            return False
        if victim[self.n(x - 1, y + 1)] != 1:
            # 左は敵の色である
            return False
        y2 = y + 1
        for x2 in range(x - 2, -1, -1):
            y2 = y2 + 1
            if y2 >= self.size:
                # 自分の色で挟んでいない
                return False
            if me[self.n(x2, y2)] == 1:
                # 自分の色で挟んでいる
                return True
            if victim[self.n(x2, y2)] == 0:
                # 相手の色が続かない
                return False
        # 自分の色で挟んでいない
        return False

    def _isEnableRightUp(self, victim: List[int], me: List[int], x: int, y: int) -> bool:
        if x + 2 < self.size or y < 2:
            # 左に2つ以上間がない
            return False
        if victim[self.n(x + 1, y - 1)] != 1:
            # 左は敵の色である
            return False
        y2 = y - 1
        for x2 in range(x + 2, self.size, 1):
            y2 = y2 - 1
            if y2 < 0:
                # 自分の色で挟んでいない
                return False
            if me[self.n(x2, y2)] == 1:
                # 自分の色で挟んでいる
                return True
            if victim[self.n(x2, y2)] == 0:
                # 相手の色が続かない
                return False
        # 自分の色で挟んでいない
        return False

    def _isEnableRightDown(self, victim: List[int], me: List[int], x: int, y: int) -> bool:
        if x + 2 >= self.size or y + 2 >= self.size:
            # 右に2つ以上間がない
            return False
        if victim[self.n(x + 1, y + 1)] != 1:
            # 左は敵の色でなければならない
            return False
        y2 = y + 1
        for x2 in range(x + 2, self.size, 1):
            y2 = y2 + 1
            if y2 >= self.size:
                # 自分の色で挟んでいない
                return False
            if me[self.n(x2, y2)] == 1:
                # 自分の色で挟んでいる
                return True
            if victim[self.n(x2, y2)] == 0:
                # 相手の色が続かない
                return False
        # 自分の色で挟んでいない
        return False

    def put(self, x: int, y: int):
        if self.player == 0:
            me = self.blacks
            victim = self.whites
        else:
            me = self.whites
            victim = self.blacks

        self.changeLeft(victim, me, x, y)
        self.changeRight(victim, me, x, y)
        self.changeUp(victim, me, x, y)
        self.changeDown(victim, me, x, y)
        self.changeLeftUp(victim, me, x, y)
        self.changeLeftDown(victim, me, x, y)
        self.changeRightUp(victim, me, x, y)
        self.changeRightDown(victim, me, x, y)
        me[self.n(x, y)] = 1
        self.player = 1 if self.player == 0 else 0
        self.makeEnable()

    def changeLeft(self, victim: List[int], me: List[int], x: int, y: int):
        if not self._isEnableLeft(victim, me, x, y):
            return
        for x2 in range(x - 1, -1, -1):
            if victim[self.n(x2, y)] == 1:
                victim[self.n(x2, y)] = 0
                me[self.n(x2, y)] = 1
            else:
                return

    def changeRight(self, victim: List[int], me: List[int], x: int, y: int):
        if not self._isEnableRight(victim, me, x, y):
            return
        for x2 in range(x + 1, self.size, 1):
            if victim[self.n(x2, y)] == 1:
                victim[self.n(x2, y)] = 0
                me[self.n(x2, y)] = 1
            else:
                return

    def changeUp(self, victim: List[int], me: List[int], x: int, y: int):
        if not self._isEnableUp(victim, me, x, y):
            return
        for y2 in range(y - 1, -1, -1):
            if victim[self.n(x, y2)] == 1:
                victim[self.n(x, y2)] = 0
                me[self.n(x, y2)] = 1
            else:
                return

    def changeDown(self, victim: List[int], me: List[int], x: int, y: int):
        if not self._isEnableDown(victim, me, x, y):
            return
        for y2 in range(y + 1, self.size, 1):
            if victim[self.n(x, y2)] == 1:
                victim[self.n(x, y2)] = 0
                me[self.n(x, y2)] = 1
            else:
                return

    def changeLeftDown(self, victim: List[int], me: List[int], x: int, y: int):
        if not self._isEnableLeftDown(victim, me, x, y):
            return
        y2 = y
        for x2 in range(x - 1, -1, -1):
            y2 = y2 + 1
            if y2 < 0:
                return
            if victim[self.n(x2, y2)] == 1:
                victim[self.n(x2, y2)] = 0
                me[self.n(x2, y2)] = 1
            else:
                return

    def changeRightDown(self, victim: List[int], me: List[int], x: int, y: int):
        if not self._isEnableRightDown(victim, me, x, y):
            return
        y2 = y
        for x2 in range(x + 1, self.size, 1):
            y2 = y2 + 1
            if y2 < 0:
                return
            if victim[self.n(x2, y2)] == 1:
                victim[self.n(x2, y2)] = 0
                me[self.n(x2, y2)] = 1
            else:
                return

    def changeLeftUp(self, victim: List[int], me: List[int], x: int, y: int):
        if not self._isEnableLeftUp(victim, me, x, y):
            return
        y2 = y
        for x2 in range(x - 1, -1, -1):
            y2 = y2 - 1
            if y2 < 0:
                return
            if victim[self.n(x2, y2)] == 1:
                victim[self.n(x2, y2)] = 0
                me[self.n(x2, y2)] = 1
            else:
                return

    def changeRightUp(self, victim: List[int], me: List[int], x: int, y: int):
        if not self._isEnableRightUp(victim, me, x, y):
            return
        y2 = y
        for x2 in range(x + 1, self.size, 1):
            y2 = y2 - 1
            if y2 < 0:
                return
            if victim[self.n(x2, y2)] == 1:
                victim[self.n(x2, y2)] = 0
                me[self.n(x2, y2)] = 1
            else:
                return

    def endGame(self) -> bool:
        return 1 not in self.enable

    def getWinner(self) -> int:
        nBlacks = sum(self.blacks)
        nWhites = sum(self.whites)
        if nBlacks == nWhites:
            return -1
        if nBlacks > nWhites:
            return 0
        return 1


class Riverse():
    def __init__(self, size: int):
        self.boards = Board(size)


class RandomMachine():
    def NextStep(self, b: Board) -> Tuple[int]:
        if 1 not in b.enable:
            return None
        while True:
            n: int = random.randint(0, b.size * b.size - 1)
            if b.enable[n] == 1:
                return b.xy(n)

class User():
    def NextStep(self, b: Board) -> Tuple[int]:
        if 1 not in b.enable:
            return None
        x=0
        y=0
        while True:
            x=int(input("X:"))
            y=int(input("Y:"))
            if x < 0 or b.size <= x or y < 0 or b.size <= y:
                print("error input: ",x,y)
                continue
            if b.enable[b.n(x,y)]==0 :
                print("error input: ",x,y)
                continue
            break
        return (x,y)



class Branch():
    def __init__(self, p1, p2, b: Board):
        self.p1 = p1
        self.p2 = p2
        self.orgBoard = b

    def Run(self):
        b: Board = copy.deepcopy(self.orgBoard)
        b.Print()
        while True:
            if b.endGame():
                break
            p = self.p1.NextStep(b)
            print("B:", p[0], p[1])
            b.put(p[0],p[1])
            b.Print()
            if b.endGame():
                break
            p = self.p2.NextStep(b)
            print("W:", p[0], p[1])
            b.put(p[0],p[1])
            b.Print()
        w = b.getWinner()
        if w == 0:
            print("win black")
        elif w == 1:
            print("win black")
        else:
            print("draw")


b = Board(6)
p1 = User()
# p2 = RandomMachine()
p2 = RandomMachine()
br = Branch(p1,p2,b)
br.Run()