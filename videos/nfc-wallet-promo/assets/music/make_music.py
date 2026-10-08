"""Generates the music bed with MusicGen (facebook/musicgen-small) on CPU.

Each chunk continues the tail of the previous one (audio prompt), so the
~140 s track evolves instead of looping a single 30 s seed.
Usage: python make_music.py <out.wav> <seconds>
"""
import sys
import numpy as np
import soundfile as sf
import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration

OUT, TOTAL = sys.argv[1], float(sys.argv[2])
PROMPT = ("fast energetic upbeat electro pop, 140 bpm, four on the floor kick, "
          "punchy claps, bright plucky synth lead, driving bass, promotional, no vocals")
FIRST, STEP, CONTEXT = 28.0, 18.0, 8.0

torch.manual_seed(140)
proc = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
sr = model.config.audio_encoder.sampling_rate
frame_rate = model.config.audio_encoder.frame_rate

def gen(seconds, prompt_audio=None):
    kwargs = dict(text=[PROMPT], padding=True, return_tensors="pt")
    if prompt_audio is not None:
        kwargs.update(audio=prompt_audio, sampling_rate=sr)
    inputs = proc(**kwargs)
    with torch.no_grad():
        out = model.generate(**inputs, do_sample=True, guidance_scale=3.0,
                             max_new_tokens=int(seconds * frame_rate))
    return out[0, 0].numpy()

track = gen(FIRST)
print(f"chunk 1: {len(track)/sr:.1f}s", flush=True)
while len(track) / sr < TOTAL:
    ctx = track[-int(CONTEXT * sr):]
    out = gen(CONTEXT + STEP, ctx)
    new = out[len(ctx):]
    track = np.concatenate([track, new])
    print(f"total: {len(track)/sr:.1f}s", flush=True)

track = track[: int(TOTAL * sr)]
fade = int(2.0 * sr)
track[-fade:] *= np.linspace(1.0, 0.0, fade)
track = track / max(1e-6, np.abs(track).max()) * 0.9
sf.write(OUT, track, sr)
print("ok", OUT, f"{len(track)/sr:.1f}s")
