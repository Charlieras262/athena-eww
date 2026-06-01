#!/bin/bash
HYPRLAND_INSTANCE_SIGNATURE=$(ls /run/user/$(id -u)/hypr/ | head -1)

generate() {
  ACTIVE=$(hyprctl monitors -j | jq '.[] | select(.focused == true) | .activeWorkspace.id')
  OCCUPIED=$(hyprctl workspaces -j | jq -r '.[] | select(.windows > 0) | .id' | tr '\n' ' ')

  echo -n '['
  for i in {1..6}; do
    [ "$i" -gt 1 ] && echo -n ','
    if [ "$i" -eq "$ACTIVE" ]; then
      STATE="active"
    elif [[ " $OCCUPIED " =~ " $i " ]]; then
      STATE="occupied"
    else
      STATE="empty"
    fi
    echo -n "{\"id\": $i, \"state\": \"$STATE\"}"
  done
  echo ']'
}

generate
socat -u UNIX-CONNECT:/run/user/$(id -u)/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock - | while read -r line; do
  case ${line%>>*} in
  workspace | focusedmon | destroyworkspace | createworkspace | urgent)
    generate
    ;;
  esac
done
