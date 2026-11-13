import pygame
import numpy as np
import pandas as pd
import pygame
import pathlid as Path

folder = Path(__file__).parent
df = pd.read_csv(Path(__file__).parent / "alan 2026.csv")
ph_values = df["Ph"]

Sample_rate = 44100

pygame.mixer.init()

def phToSound(ph):
    if ph <= 5:
        return   folder /""
