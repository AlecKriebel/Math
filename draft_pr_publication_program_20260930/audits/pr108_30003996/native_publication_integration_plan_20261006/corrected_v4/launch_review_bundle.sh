#!/bin/sh
# Nonexecuted native launcher draft. A pure startup probe is available for fixtures.
set -eu
if [ "$#" -ne 2 ]; then
  echo 'Expected pinned absolute Python path and future config path or --verify-startup-only' >&2
  exit 2
fi
case "$1" in /*) ;; *) echo 'Absolute reviewed Python executable required' >&2; exit 2 ;; esac
script_directory=$(CDPATH= cd -- "$(/usr/bin/dirname -- "$0")" && pwd)
if [ "$2" = '--verify-startup-only' ]; then
  exec /usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C LANG=C TZ=UTC "$1" -E -S -B "$script_directory/prepare_review_bundle.py" --verify-startup-only
fi
exec /usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C LANG=C TZ=UTC "$1" -E -S -B "$script_directory/prepare_review_bundle.py" --config "$2"
