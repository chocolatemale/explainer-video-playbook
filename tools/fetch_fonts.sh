#!/usr/bin/env bash
set -euo pipefail
out=${1:-build/fonts}
mkdir -p "$out"
base=https://raw.githubusercontent.com/google/fonts/main/ofl
for family in notosanssc notoserifsc; do
  if [[ "$family" == notosanssc ]]; then name=NotoSansSC; else name=NotoSerifSC; fi
  curl --fail --location --retry 3 "$base/$family/$name%5Bwght%5D.ttf" -o "$out/$name.ttf.part"
  mv "$out/$name.ttf.part" "$out/$name.ttf"
  curl --fail --location --retry 3 "$base/$family/OFL.txt" -o "$out/OFL-$name.txt"
done
