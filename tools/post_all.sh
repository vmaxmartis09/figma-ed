#!/bin/bash
# overview + texts for every in-scope story that has screens (skips Archive/Translation/Proposal/Cover)
S=/private/tmp/claude-501/-Volumes-Data-figma-ediva/45e49075-ca3e-483c-b781-38ee4d32769c/scratchpad
while IFS=$'\t' read -r PAGE PATHJ NAME DIR; do
  case "$DIR" in *Archive*|*Translation*|*Proposal*|*Cover*) continue;; esac
  O="$DIR/_story"; [ -f "$O/screens/screens.json" ] || continue
  [ -f "$O/story.png" ] && python3 /Volumes/Data/figma-ediva/tools/overview.py "$O" 2>&1 | tail -1
  python3 /Volumes/Data/figma-ediva/tools/build_texts.py "$O" 2>&1 | tail -1
done < $S/stories.tsv
echo POSTDONE
