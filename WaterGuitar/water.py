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

import pygame
import pandas as pd
from pathlib import Path

folder = Path(__file__).parent
df = pd.read_csv(folder / "alan 2026.csv")
ph_values = df["Ph"]          # must match the CSV header exactly (case-sensitive)

WINDOW = (800, 600)
SECONDS_PER_READING = 2

# (max pH, sound file, image file). Fill in the blank ones with your own files.
RANGES = [
    (5,  "lofi-guitar-calm_85bpm_C_major.wav",       "ph_low.png"),
    (8,  "slow-calm-guitar-melody_109bpm_G_major.wav", "ph_neutral.png"),
    (11, "",                                          "ph_high.png"),
    (14, "",                                          "ph_very_high.png"),
]

def ph_to_media(ph):
    for max_ph, sound, image in RANGES:
        if ph <= max_ph:
            return (folder / sound if sound else None), folder / image
    return None, None   # pH above 14

def load_fit(path):
    img = pygame.image.load(path).convert_alpha()
    w, h = img.get_size()
    scale = min(WINDOW[0] / w, WINDOW[1] / h)
    return pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(WINDOW)
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

previous_ph = None
running = True

for ph in ph_values:
    if not running:
        break

    # Only change image and sound when the pH actually changes
    if ph != previous_ph:
        sound, image = ph_to_media(ph)
        print(f"pH changed: {previous_ph} -> {ph}")

        # Sound
        pygame.mixer.music.stop()
        if sound and sound.exists():
            pygame.mixer.music.load(str(sound))
            pygame.mixer.music.play()

        # Image
        screen.fill((0, 0, 0))
        if image and image.exists():
            img = load_fit(str(image))
            screen.blit(img, img.get_rect(center=(WINDOW[0] // 2, WINDOW[1] // 2)))
        label = font.render(f"pH {ph}", True, (255, 255, 255))
        screen.blit(label, (20, 20))
        pygame.display.flip()

        previous_ph = ph

    # Wait for this reading's time slot, keeping the window responsive
    end_time = pygame.time.get_ticks() + SECONDS_PER_READING * 1000
    while pygame.time.get_ticks() < end_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                end_time = 0
        clock.tick(30)

pygame.mixer.music.stop()
pygame.quit()