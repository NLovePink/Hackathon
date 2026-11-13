import pygame
import numpy as np
import pandas as pd
import pygame
import pathlid as Path

df = pd.read_csv(Path(__file__).parent / "odin 2026.csv")
ph_values = df["VaporPressure"]




from morseutils.translator import MorseCodeTranslator as mct

translator = mct()
