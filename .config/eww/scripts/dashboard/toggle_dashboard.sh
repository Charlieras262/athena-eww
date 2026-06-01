#!/bin/bash
EWW="$(which eww)"
STATE_FILE="/tmp/eww_dashboard"
LOCK_FILE="/tmp/eww_dashboard.lock"

if [ -f "$LOCK_FILE" ]; then
  exit 0
fi
touch "$LOCK_FILE"

## Run eww daemon if not running already
if [[ ! $(pidof eww) ]]; then
  ${EWW} daemon
  sleep 1
fi

close_dash() {
  "$EWW" close \
    window_dashboard
  rm -f "$STATE_FILE"
}

case "$1" in
close)
  close_dash
  ;;
*)
  if [[ ! -f "$STATE_FILE" ]]; then
    touch "$STATE_FILE"
    "$EWW" --no-daemonize open window_dashboard
  else
    close_dash
  fi
  ;;
esac

rm -f "$LOCK_FILE"
