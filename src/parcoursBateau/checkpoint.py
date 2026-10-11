from __future__ import annotations
from typing import Optional
from bateau import Bateau
import math


class CheckPoint:
    nb = 1
    def __init__(self, x: int, y: int, next_CheckPoint: Optional[CheckPoint] = None, radius: float = 0.4):
        self.name = str(CheckPoint.nb)
        CheckPoint.nb += 1
        self.x = x
        self.y = y
        self.radius = radius
        self.next_CheckPoint = next_CheckPoint
        self.bateau_viewed = []

    def reset(self):
        self.bateau_viewed.clear()

    def collision(self, bateau: Bateau, cp_name:str, bonus_arrival: int) -> bool:
        distance = math.sqrt((bateau.x - self.x) ** 2 + (bateau.y - self.y) ** 2)
        if distance <= self.radius and cp_name == self.name:

            if not (bateau in self.bateau_viewed):
                self.bateau_viewed.append(bateau)
                bateau.recompense(10)
                # print(f"Le bateau {bateau.name} est rentré en contact avec le checkpoint {self.name}.")

                bateau.bonus_arrival += bonus_arrival
                self.__give_next_checkPoint(bateau)
                return True
        
        return False

    def __give_next_checkPoint(self, bateau: Bateau):
        if self.next_CheckPoint:
            bateau.new_goal(self.next_CheckPoint.x, self.next_CheckPoint.y, self.next_CheckPoint.name)
            # print(f"Nouvelle coordonnée du bateau ({bateau.goal_x},{bateau.goal_y}) : {bateau.cp_name}")
                

    def to_dict(self):
        return {
            "n": self.name,
            "x": self.x,
            "y": self.y,
        }
    
    def to_list(self):
        return [self.x, self.y]
