import pygame
import pandas as pd
import pathlid as Path

folder = Path(__file__).parent
df = pd.read_csv(folder / "purpleair 2026.csv")

def pm25_values_ToSound(pm25):
    if pm25 <= 9.0:
        return folder / "chill-drums_125bpm.wav"
    elif pm25 <= 35.4:
        return folder / "crunchy-loud-drums-loop_138bpm.wav"
    elif pm25 <= 55.4:
        return folder / "in-suspense-moderate-drum-top-loop_C_major.wav"
    else:
        return folder / "11325622-noise-drum-loop-134bpm-245852.mp3"

for pm25_value in df["pm2.5"]:
    sound = pm25_values_ToSound(pm25_value)
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()
    pygame.time.wait(2000)
    pygame.mixer.music.stop()