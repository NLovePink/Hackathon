import importlib

try:
    pygame = importlib.import_module("pygame")
except ModuleNotFoundError as exc:
    if exc.name == "pygame":
        raise SystemExit("pygame is not installed. Install it with: python -m pip install pygame") from exc
    raise
from pathlib import Path

folder = Path(__file__).parent
df = pd.read_csv(folder / "alan 2026.csv")
ph_values = df["Ph"]         
WINDOW = (800, 600)
SECONDS_PER_READING = 2

RANGES = [
    (5,  "lofi-guitar-calm_85bpm_C_major.wav",       "Images/69d4f553a801270cc080e78402855353.jpg"),
    (8,  "slow-calm-guitar-melody_109bpm_G_major.wav", "Images/fc379ce281f69a164b428c7d5e83b3f8.jpg"),
    (11, "freesound_community-105-acdc-style-guitar-loop-01-68001.mp3",     "Images/b11444a0ff28f17e1c483437f334ea8e.jpg"),
    (14, "freesound_community-electric-guitar-metal-riff-107087.mp3",       "Images/fd9f8795efd6783bf45a527789cdf99a.jpg"),
]

def ph_to_media(ph):
    for max_ph, sound, image in RANGES:
        if ph <= max_ph:
            return (folder / sound if sound else None), folder / image
    return None, None  

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

    end_time = pygame.time.get_ticks() + SECONDS_PER_READING * 1000
    while pygame.time.get_ticks() < end_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                end_time = 0
        clock.tick(30)

pygame.mixer.music.stop()
pygame.quit()