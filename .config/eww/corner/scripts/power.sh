#!/bin/bash
case "$1" in
p-shutdown) hyprshutdown -p "systemctl poweroff" ;;
p-reboot) hyprshutdown -p "systemctl reboot" ;;
p-suspend)
  (sleep 0.5 && systemctl suspend) &
  hyprlock --immediate-render
  ;;
p-logout) hyprshutdown ;;
esac
