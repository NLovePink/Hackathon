import pygame
import numpy as np
import pandas as pd
import pygame
import pathlid as Path

df = pd.read_csv(Path(__file__).parent / "odin 2026.csv")
ph_values = df["VaporPressure"]




#!/usr/bin/env python3
"""Convert text (letters, numbers, punctuation) to Morse code audio (.mp3).

Usage:
    python morse.py "HELLO WORLD 123" output.mp3
    python morse.py --csv data.csv --column VaporPressure --limit 10 output.mp3

This script uses only Python's standard library (no extra packages to
install). The one external tool it needs is ffmpeg, which converts the
WAV file to MP3. Install it with one of:
    Windows:  winget install ffmpeg
    macOS:    brew install ffmpeg
    Linux:    sudo apt install ffmpeg

Morse timing (ITU standard, 1 unit = dot length):
    dot = 1 unit, dash = 3 units
    gap between elements in a letter = 1 unit
    gap between letters = 3 units
    gap between words = 7 units
"""
# Terminal Command Note: python MorseCode\morse.py --csv "MorseCode\odin 2026.csv" --column VaporPressure --limit 10 vapor_pressure.mp3
# Above note shows how to convert the VaporPressure column from the CSV file to Morse code audio.

import argparse
import csv
import math
import shutil
import subprocess
import sys
import wave
from array import array
from pathlib import Path

# ---------------------------------------------------------------------------
# Morse code table (ITU): letters, digits, common punctuation
# ---------------------------------------------------------------------------
MORSE_CODE = {
    # Letters
    "A": ".-",    "B": "-...",  "C": "-.-.",  "D": "-..",
    "E": ".",     "F": "..-.",  "G": "--.",   "H": "....",
    "I": "..",    "J": ".---",  "K": "-.-",   "L": ".-..",
    "M": "--",    "N": "-.",    "O": "---",   "P": ".--.",
    "Q": "--.-",  "R": ".-.",   "S": "...",   "T": "-",
    "U": "..-",   "V": "...-",  "W": ".--",   "X": "-..-",
    "Y": "-.--",  "Z": "--..",
    # Digits
    "0": "-----", "1": ".----", "2": "..---", "3": "...--",
    "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----.",
    # Punctuation
    ".": ".-.-.-", ",": "--..--", "?": "..--..", "'": ".----.",
    "!": "-.-.--", "/": "-..-.",  "(": "-.--.",  ")": "-.--.-",
    "&": ".-...",  ":": "---...", ";": "-.-.-.", "=": "-...-",
    "+": ".-.-.",  "-": "-....-", "_": "..--.-", '"': ".-..-.",
    "$": "...-..-", "@": ".--.-.",
}

# ---------------------------------------------------------------------------
# Audio settings
# ---------------------------------------------------------------------------
SAMPLE_RATE = 44100      # Hz (samples per second, CD quality)
FREQUENCY = 700          # Hz tone for dots/dashes
UNIT = 0.08              # seconds per dot (1 unit); dash = 3 units
AMPLITUDE = 0.5          # 0.0-1.0 (half volume)
MAX_INT16 = 32767        # largest 16-bit sample value


def text_to_morse(text):
    """Convert text to a Morse code string. Letters separated by spaces,
    words separated by ' / '. Unknown characters are skipped."""
    words = text.upper().split()
    morse_words = []
    for word in words:
        morse_letters = []
        for char in word:
            if char in MORSE_CODE:
                morse_letters.append(MORSE_CODE[char])
        if morse_letters:
            morse_words.append(" ".join(morse_letters))
    return " / ".join(morse_words)


def _tone(duration):
    """Generate a sine-wave tone of the given duration (seconds).
    Returns an array of 16-bit samples."""
    n = int(SAMPLE_RATE * duration)
    fade = int(SAMPLE_RATE * 0.005)  # 5ms fade to avoid clicks
    samples = array("h")
    for i in range(n):
        t = i / SAMPLE_RATE
        value = AMPLITUDE * math.sin(2 * math.pi * FREQUENCY * t)
        # Fade in at the start and out at the end.
        if i < fade:
            value *= i / fade
        elif i >= n - fade:
            value *= (n - i) / fade
        samples.append(int(value * MAX_INT16))
    return samples


def _silence(duration):
    """Generate silence of the given duration (seconds).
    Returns an array of 16-bit zero samples."""
    return array("h", [0]) * int(SAMPLE_RATE * duration)


def morse_to_samples(morse):
    """Convert a Morse code string (from text_to_morse) to audio samples."""
    parts = array("h")
    for symbol in morse:
        if symbol == ".":
            parts.extend(_tone(UNIT))          # dot = 1 unit
            parts.extend(_silence(UNIT))       # element gap = 1 unit
        elif symbol == "-":
            parts.extend(_tone(UNIT * 3))      # dash = 3 units
            parts.extend(_silence(UNIT))       # element gap = 1 unit
        elif symbol == " ":
            # Letter gap = 3 units total; 1 unit already added after
            # the last element, so add 2 more.
            parts.extend(_silence(UNIT * 2))
        elif symbol == "/":
            # Word gap = 7 units total; the spaces around '/' each add
            # 2 units (4 total) plus the 1-unit element gap, so add 2 more.
            parts.extend(_silence(UNIT * 2))
    return parts


def write_wav(samples, wav_path):
    """Write 16-bit samples as a mono WAV file."""
    with wave.open(str(wav_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(samples.tobytes())


def convert_to_mp3(wav_path, mp3_path):
    """Convert a WAV file to MP3 using ffmpeg."""
    if shutil.which("ffmpeg") is None:
        raise RuntimeError(
            "ffmpeg was not found on your system. It is needed to make MP3 "
            "files. Install it with one of:\n"
            "  Windows:  winget install ffmpeg\n"
            "  macOS:    brew install ffmpeg\n"
            "  Linux:    sudo apt install ffmpeg\n"
            "Then restart your terminal and run this script again."
        )
    result = subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(wav_path), str(mp3_path)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {result.stderr.strip()}")


def text_to_mp3(text, mp3_path, keep_wav=False):
    """Convert text to Morse code audio and save as an MP3 file.
    Returns the Morse code string."""
    morse = text_to_morse(text)
    if not morse:
        raise ValueError("No convertible characters found in text.")
    samples = morse_to_samples(morse)
    wav_path = Path(mp3_path).with_suffix(".wav")
    write_wav(samples, wav_path)
    convert_to_mp3(wav_path, mp3_path)
    if not keep_wav:
        wav_path.unlink()
    return morse


def csv_to_mp3(csv_path, mp3_path, column=None, separator=" ", limit=None):
    """Read a CSV file, convert its text to Morse code audio, save as MP3.
    If column is given, converts that column only; otherwise converts all
    cells row by row. If limit is given, only the first `limit` rows are
    used. Returns (morse_code, text_used)."""
    texts = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV file has no header row.")
        if column is not None:
            if column not in reader.fieldnames:
                raise ValueError(
                    f"Column '{column}' not found. "
                    f"Available columns: {', '.join(reader.fieldnames)}"
                )
            for i, row in enumerate(reader):
                if limit is not None and i >= limit:
                    break
                value = row.get(column, "")
                if value:
                    texts.append(str(value))
        else:
            for i, row in enumerate(reader):
                if limit is not None and i >= limit:
                    break
                values = [str(v) for v in row.values() if v]
                if values:
                    texts.append(separator.join(values))
    text = separator.join(texts)
    morse = text_to_mp3(text, mp3_path)
    return morse, text


def main():
    parser = argparse.ArgumentParser(
        description="Convert text or CSV data to Morse code audio (.mp3)."
    )
    parser.add_argument("input", help="Text to convert, or CSV file with --csv.")
    parser.add_argument("output", help="Output MP3 file path.")
    parser.add_argument("--csv", action="store_true",
                        help="Treat input as a CSV file path.")
    parser.add_argument("--column", default=None,
                        help="CSV column to convert (default: all columns).")
    parser.add_argument("--limit", type=int, default=None,
                        help="Only convert the first N rows of the CSV.")
    parser.add_argument("--separator", default=" ",
                        help="Separator between CSV cells/rows (default: space).")
    parser.add_argument("--keep-wav", action="store_true",
                        help="Keep the intermediate WAV file.")
    args = parser.parse_args()

    if args.csv:
        morse, text = csv_to_mp3(args.input, args.output, args.column, args.separator, args.limit)
        print(f"Text from CSV: {text}")
    else:
        morse = text_to_mp3(args.input, args.output, args.keep_wav)
        print(f"Text: {args.input}")
    print(f"Morse: {morse}")
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
