#!/bin/zsh
set -u
set -o pipefail

log_path="/Users/alec/Documents/Math/complete_graph_extremality_referee_audit_2026-08-22/records/independent_crosschecks.log"

{
  print -- ""
  print -- "timestamp_utc: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  print -- "cwd: $PWD"
  printf 'argv:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  print -- "exit_status: $command_status"
  exit "$command_status"
} 2>&1 | tee -a "$log_path"

exit "${pipestatus[1]}"
