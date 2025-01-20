import math
import pygame
from dataclasses import dataclass

@dataclass
class Hexagon:
    #Hexagon class#
    radius: float
    position: tuple(float, float)