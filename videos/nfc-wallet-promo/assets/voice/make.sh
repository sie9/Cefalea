#!/bin/sh
# Regenerates the voice-over lines with local Kokoro (voice em_alex, Spanish).
cd "$(dirname "$0")"
export HYPERFRAMES_PYTHON="$HOME/.venvs/hf-audio/bin/python"
while IFS="$(printf '\t')" read -r id text; do
  npx --yes hyperframes@0.8.140 tts "$text" -v em_alex -l es -s 1.1 -o "vo-$id.wav" --json | tail -n 1
done < lines.tsv
