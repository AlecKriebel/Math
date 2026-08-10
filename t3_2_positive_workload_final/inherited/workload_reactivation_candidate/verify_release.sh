#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
echo '[1/6] finite and atlas checks'
"$ROOT/run_all.sh"
echo '[2/6] deterministic PDF build'
"$ROOT/manuscript/build.sh" >/dev/null
echo '[3/6] verification report pass 1'
python "$ROOT/src/make_verification_report.py" > /tmp/t3_report_1.json
echo '[4/6] verification report pass 2'
python "$ROOT/src/make_verification_report.py" > /tmp/t3_report_2.json
echo '[5/6] stable-report comparison'
cmp /tmp/t3_report_1.json /tmp/t3_report_2.json
if [ -f "$ROOT/certificates/MANIFEST.sha256" ]; then
  echo '[6/6] manifest'
  cd "$ROOT"
  sha256sum -c certificates/MANIFEST.sha256
fi
printf '%s\n' 'T3-2 RELEASE VERIFICATION PASSED'
