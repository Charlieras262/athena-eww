#!/bin/bash
case "$1" in
status)
  dunstctl is-paused
  ;;
toggle)
  dunstctl set-paused toggle
  ;;
esac
