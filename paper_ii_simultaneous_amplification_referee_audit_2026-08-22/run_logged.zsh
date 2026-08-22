#!/bin/zsh

set -u

audit_root="/Users/alec/Documents/Math/paper_ii_simultaneous_amplification_referee_audit_2026-08-22"

if (( $# < 3 )); then
  print -u2 "usage: $0 LABEL WORKDIR COMMAND [ARG ...]"
  exit 64
fi

label="$1"
command_workdir="$2"
shift 2

started_at="$(date -Iseconds)"
command_id="$(date '+%Y%m%dT%H%M%S')-$RANDOM"
command_display=""
for command_part in "$@"; do
  command_display+="${(q)command_part} "
done
command_display="${command_display% }"

{
  print -- "----- $command_id | $started_at | $label -----"
  print -- "cwd: $command_workdir"
  print -- "command: $command_display"
} | tee -a "$audit_root/logs/full_transcript.log"

set +e
(
  cd "$command_workdir" || exit 200
  "$@"
) 2>&1 | tee -a "$audit_root/logs/full_transcript.log"
command_status=${pipestatus[1]}
set -e

finished_at="$(date -Iseconds)"
print -- "exit_status: $command_status | finished: $finished_at" | tee -a "$audit_root/logs/full_transcript.log"
printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
  "$command_id" "$started_at" "$finished_at" "$command_status" \
  "$label" "$command_workdir" "$command_display" >> "$audit_root/logs/commands.tsv"

exit "$command_status"
