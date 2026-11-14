import pygame
import numpy as np
import pandas as pd
import pygame
import pathlid as Path
folder = Path(__file__).parent 
df = pd.read_csv(Path(__file__).parent / "purpleair 2026.csv")
pm25_values = df["pm2.5"]

def pm25_values_ToSound(pm25):
    if pm25 <= 50:
        return   folder /""
    elif pm25 <= 150:
        return folder/""
    elif pm25 <= 200:
        return folder/ ""
    else:
        return folder/"11325622-noise-drum-loop-134bpm-245852.mp3"
for pm25_values in df["pm2.5"]:
        pygame.mixer.music.loa(pm25_values_ToSound(ph))
        pygame.mixer.music.play()
        pygame.time.wait(2000)
        pygame.mixer.music.stop()