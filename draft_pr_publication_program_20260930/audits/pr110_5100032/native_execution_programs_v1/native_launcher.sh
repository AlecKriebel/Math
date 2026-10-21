#!/bin/sh
# Invoke through a separately recorded clean /usr/bin/env -i /bin/sh call.
set -eu
[ "$#" -eq 4 ] || exit 64
case "$1:$2:$3" in /*:/*:/*) ;; *) exit 64 ;; esac
if [ -n "$4" ]; then
  exec /usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C LANG=C TZ=UTC __CF_USER_TEXT_ENCODING="$4" "$1" -E -S -B -P "$2" --config "$3"
else
  exec /usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C LANG=C TZ=UTC "$1" -E -S -B -P "$2" --config "$3"
fi
