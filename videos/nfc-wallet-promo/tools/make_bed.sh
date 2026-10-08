#!/bin/sh
# Rebuilds the music bed from the steady, full-energy stretches of the MusicGen
# take (assets/music/bed.wav), skipping its thin intro and the drop-outs at
# 24-30 s, 82-84 s and 100 s. Crossfades of 0.4 s, then levelled to -16 LUFS.
set -e
cd "$(dirname "$0")/../assets/music"
SEGS="102:124 128:140 58:76 86:98 102:124 128:140 58:76 86:98 102:114"
i=0; inputs=""; filter=""
for s in $SEGS; do
  a=${s%:*}; b=${s#*:}
  inputs="$inputs -ss $a -to $b -i bed.wav"
  i=$((i+1))
done
# Chain acrossfade over all inputs.
prev="[0:a]"
n=1
while [ $n -lt $i ]; do
  out="[x$n]"
  filter="$filter${prev}[$n:a]acrossfade=d=0.4:c1=tri:c2=tri$out;"
  prev=$out
  n=$((n+1))
done
filter="${filter}${prev}loudnorm=I=-16:TP=-2:LRA=7,afade=t=in:d=0.3,atrim=0:137[out]"
ffmpeg -v error -y $inputs -filter_complex "$filter" -map "[out]" -ar 48000 -ac 2 bed-v2.wav
echo "bed-v2.wav $(ffprobe -v error -show_entries format=duration -of csv=p=0 bed-v2.wav)s"
