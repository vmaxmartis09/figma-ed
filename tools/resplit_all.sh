#!/bin/bash
# re-split story CSS (adds coordinates) and crop screens for every story that has story.png
S=/private/tmp/claude-501/-Volumes-Data-figma-ediva/45e49075-ca3e-483c-b781-38ee4d32769c/scratchpad
while IFS=$'\t' read -r PAGE PATHJ NAME DIR; do
  O="$DIR/_story"
  [ -f "$O/story_all.css" ] && python3 /Volumes/Data/figma-ediva/tools/split_story.py "$O/story_all.css" "$O/screens" >/dev/null 2>&1
  [ -f "$O/story.png" ] && python3 /Volumes/Data/figma-ediva/tools/crop_story.py "$O" 2>&1 | tail -1
done < $S/stories.tsv
