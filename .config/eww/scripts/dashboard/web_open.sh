#!/bin/bash
cmd="firefox --new-tab"

case "$1" in
--arch) $cmd "https://archlinux.org" & ;;
--gh) $cmd "https://github.com" & ;;
--ig) $cmd "https://instagram.com" & ;;
--wa) $cmd "https://web.whatsapp.com" & ;;
--mail) $cmd "https://mail.google.com" & ;;
esac
