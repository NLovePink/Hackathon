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
        return   folder /"lofi-guitar-calm_85bpm_C_major.wav"
    elif ph <= 8:
        return folder/"slow-calm-guitar-melody_109bpm_G_major.wav"
    elif ph <= 11:
        return folder/ ""
    elif ph <= 14:
        return folder/""
    else: return folder/""

for ph in df["ph"]:
        pygame.mixer.music.load(phToSound(ph))
        pygame.mixer.music.play()
        pygame.time.wait(2000)
        pygame.mixer.music.stop()
