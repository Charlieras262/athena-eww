#!/usr/bin/env bash

get_status() {
  audio_status=$(amixer get Master | grep -o '\[on\]\|\[off\]' | head -n1)
  if [ "$audio_status" = "[off]" ]; then
    audio="muted"
  else
    audio="unmuted"
  fi

  mic_status=$(amixer get Capture | grep -o '\[on\]\|\[off\]' | head -n1)
  if [ "$mic_status" = "[off]" ]; then
    mic="muted"
  else
    mic="unmuted"
  fi

  printf '{"audio": "%s", "mic": "%s"}\n' "$audio" "$mic"
}

get_status

pactl subscribe | stdbuf -oL grep --line-buffered "change" | while read -r _; do
  get_status
done
