import pygame
import csv
from pathlib import Path

folder = Path(__file__).parent
sounds = folder.parent / "Sounds"
with open(folder / "purpleair 2026.csv", newline="") as f:
    pm25_values = [float(row["pm2.5_atm"]) for row in csv.DictReader(f) if row["pm2.5_atm"]]

def pm25_values_ToSound(pm25):
    if pm25 <= 9.0:
        return sounds / "chill-drums_125bpm.wav"
    elif pm25 <= 35.4:
        return sounds / "crunchy-loud-drums-loop_138bpm.wav"
    elif pm25 <= 55.4:
        return sounds / "in-suspense-moderate-drum-top-loop_C_major.wav"
    else:
        return sounds / "11325622-noise-drum-loop-134bpm-245852.mp3"

pygame.mixer.init()

try:
    for pm25_value in pm25_values:
        sound = pm25_values_ToSound(pm25_value)
        print(f"PM2.5 {pm25_value} -> {sound.name}")
        pygame.mixer.music.load(str(sound))
        pygame.mixer.music.play()
        pygame.time.wait(2000)
        pygame.mixer.music.stop()
except KeyboardInterrupt:
    pass

pygame.mixer.quit()
