from checkpoint import CheckPoint
from collections.abc import Callable

class Set:
    """
    Gère le stockage des sets de parcours

    Adri2 > on devrait rajouter des méthodes permettant de visualiser les sets existants
    """

    def __init__(self):
        self.__sets: dict[str, Callable[[], None]] = {
            "1": self.__set1,
            "2": self.__set2,
            "3": self.__set3,
            "4": self.__set4,
            "5": self.__set5,
            "6": self.__set6,
            "10": self.__set10,
            "11": self.__set11,
            "12": self.__set12,
            "13": self.__set13
        }

        self.__checkpoints: list[CheckPoint] = []
        self.__set1()
        self.__temps: int = 0

    def get_temps(self) -> int:
        return self.__temps

    def get_checkpoints(self)  -> list[CheckPoint]:
        return self.__checkpoints

    def get_first_checkpoint(self) -> CheckPoint:
        return self.__checkpoints[-1]   # ne pas se tromper !  C'est -1 le premier à aller chercher !

    def get_last_checkpoint(self)  -> CheckPoint:
        return self.__checkpoints[0]

    def change_set(self, choix: str) -> None:
        CheckPoint.nb = 1
        self.__checkpoints.clear()
        try:
            self.__sets[choix]()
        except:
            print(f"set \"{choix}\" introuvable")
            self.__set1()

    def __set1(self):
        self.__temps = 120
        self.__checkpoints.append(CheckPoint(0, 0))
        self.__checkpoints.append(CheckPoint(9, 3, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(10, 3, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(5, 5, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(1, 1, self.__checkpoints[-1]))

    def __set2(self):
        self.__temps = 120
        self.__checkpoints.append(CheckPoint(0, 0))
        self.__checkpoints.append(CheckPoint(0, 1, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(1, 0, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(1, 1, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(2, 2, self.__checkpoints[-1]))

    def __set3(self):
        self.__temps = 120
        self.__checkpoints.append(CheckPoint(-5, 2))
        self.__checkpoints.append(CheckPoint(0, 1, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(1, 3, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-2, 8, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(2, 4, self.__checkpoints[-1]))

    def __set4(self):
        self.__temps = 500
        self.__checkpoints.append(CheckPoint(-5, 2))
        self.__checkpoints.append(CheckPoint(13, 9, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(17, 3, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-21, 8, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-20, 5, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(6, 11, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(1, 3, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-2, 8, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-20, 12, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(0, 14, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(1, 31, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-2, 21, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-20, 4, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(5, 15, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(8, 3, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-2, 8, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-20, 7, self.__checkpoints[-1]))

    def __set5(self):
        self.__temps = 600
        self.__checkpoints.append(CheckPoint(-15, 2))
        self.__checkpoints.append(CheckPoint(3, 9, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(1, -3, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-26, 8, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-10, -5, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(16, 1, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(12, -3, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-12, 8, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-2, -12, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(2, -6, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(4, 1, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-6, 1, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-2, 14, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(4, 5, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(9, 13, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-2, -8, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-3, -7, self.__checkpoints[-1]))

    
    def __set6(self):
        self.__temps = 300
        self.__checkpoints.append(CheckPoint(-4, 15))
        self.__checkpoints.append(CheckPoint(-3, 6, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(1, -3, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-16, 18, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-11, -15, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(6, 14, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(2, 3, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(15, 11, self.__checkpoints[-1]))


    def __set10(self):
        self.__temps = 80
        self.__checkpoints.append(CheckPoint(-20, -10))
        self.__checkpoints.append(CheckPoint(-10, 10, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(10, -10, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(10, 10, self.__checkpoints[-1]))


    def __set11(self):
        self.__temps = 300
        self.__checkpoints.append(CheckPoint(-19, 11))
        self.__checkpoints.append(CheckPoint(-19, 7, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-20, 7, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-20, 8, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(40, 8, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(40, 10, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(2, 2, self.__checkpoints[-1]))


    def __set12(self):
        self.__temps = 500
        self.__checkpoints.append(CheckPoint(10, -10))
        self.__checkpoints.append(CheckPoint(10, -10, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(10, -10, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-10, 10, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-10, -10, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(10, 10, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(0, -10, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(0, 10, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-10, 1, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(10, 1, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-10, -1, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(10, -1, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-10, 0, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(10, 0, self.__checkpoints[-1]))

    
    def __set13(self):
        self.__temps = 600
        self.__checkpoints.append(CheckPoint(4, 15))
        self.__checkpoints.append(CheckPoint(9, 15, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(10, 15, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(4, 15, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(4, 10, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(10, 10, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-30, -4, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-30, -3, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-29, -2, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-30, -3, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(30, -2, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-2, -2, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-4, 1, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(-3, 5, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(1, 6, self.__checkpoints[-1]))
        self.__checkpoints.append(CheckPoint(4, 4, self.__checkpoints[-1]))