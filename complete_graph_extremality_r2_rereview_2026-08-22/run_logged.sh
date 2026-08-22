#!/bin/zsh

set -u

review_root="${0:A:h}"
log_file="$review_root/records/COMMANDS.log"

if (( $# < 2 )); then
  print -u2 "usage: $0 LABEL COMMAND [ARG ...]"
  exit 64
fi

label="$1"
shift

{
  print
  print -- "=== $(date -u '+%Y-%m-%dT%H:%M:%SZ') :: $label ==="
  print -- "cwd: $PWD"
  print -n -- "argv:"
  for arg in "$@"; do
    printf ' %q' "$arg"
  done
  print
} | tee -a "$log_file"

set +e
"$@" 2>&1 | tee -a "$log_file"
command_status=${pipestatus[1]}
set -e

print -- "exit_status: $command_status" | tee -a "$log_file"
exit "$command_status"

