import pygame
import numpy as np
import pandas as pd
import pygame
import pathlid as Path

df = pd.read_csv(Path(__file__).parent / "purpleair 2026.csv")
ph_values = df["pm2.5"]