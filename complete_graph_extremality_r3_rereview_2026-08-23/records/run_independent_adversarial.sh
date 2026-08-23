#!/bin/zsh

set -eu

review_root="${0:A:h:h}"
package="$review_root/work/package"
trusted_python="/opt/homebrew/bin/python3"
case_root=$(mktemp -d "$review_root/work/adversarial.XXXXXX")
mkdir -p "$case_root/logs" "$case_root/home" "$case_root/tmp" "$case_root/caller"

expected_failure() {
  local label=$1
  local expected_status=$2
  local expected_text=$3
  shift 3
  local log="$case_root/logs/$label.log"
  set +e
  "$@" >"$log" 2>&1
  local actual_status=$?
  set -e
  print -- "$label status=$actual_status expected=$expected_status"
  if [[ "$actual_status" -ne "$expected_status" ]]; then
    sed -n '1,160p' "$log"
    print -u2 -- "FAIL: $label had the wrong status"
    exit 1
  fi
  if ! grep -F "$expected_text" "$log" >/dev/null; then
    sed -n '1,160p' "$log"
    print -u2 -- "FAIL: $label lacked the intended diagnostic"
    exit 1
  fi
  print -- "PASS: $label diagnostic=$expected_text"
}

fake_python="$package/source_and_certificates/universal_simultaneous_amplification/phase5_exact_threshold/paper_db_extremality/submission/fake_python_public_token.sh"
expected_failure root_fake_python 2 \
  "Refusing inherited PYTHON" \
  env -i PATH=/opt/homebrew/bin:/usr/bin:/bin \
  PYTHON="$fake_python" "$package/run_all_referee_checks.sh"
if grep -F "PAPER1_EXECUTION_SAFETY_OK" "$case_root/logs/root_fake_python.log" >/dev/null; then
  print -u2 -- "FAIL: package launcher invoked the token-printing fake interpreter"
  exit 1
fi
print -- "PASS: root fake interpreter was rejected before invocation"

expected_failure root_empty_python 2 \
  "Refusing inherited PYTHON" \
  env -i PATH=/opt/homebrew/bin:/usr/bin:/bin PYTHON= \
  "$package/run_all_referee_checks.sh"

paper="$package/source_and_certificates/universal_simultaneous_amplification/phase5_exact_threshold/paper_db_extremality"
expected_failure replay_no_internal_capability 2 \
  "replay.sh is an internal verifier stage" \
  env -i PATH=/opt/homebrew/bin:/usr/bin:/bin "$paper/replay.sh"
expected_failure bootstrap_no_mode 2 \
  "Usage: bootstrap_replay.sh" \
  env -i PATH=/opt/homebrew/bin:/usr/bin:/bin \
  BOOTSTRAP_PYTHON="$trusted_python" "$paper/submission/bootstrap_replay.sh"

package_case() {
  local mode=$1
  local expected_text=$2
  local copy="$case_root/package-$mode"
  cp -a "$package" "$copy"
  case "$mode" in
    extra-file) print -- hostile >"$copy/UNEXPECTED_FILE" ;;
    extra-dir) mkdir "$copy/UNEXPECTED_EMPTY_DIRECTORY" ;;
    symlink) ln -s PACKAGE_MANIFEST.sha256 "$copy/UNEXPECTED_SYMLINK" ;;
    fifo) mkfifo "$copy/UNEXPECTED_FIFO" ;;
    socket)
      local short_link="/tmp/r3-rereview-socket.$$"
      ln -s "$copy" "$short_link"
      "$trusted_python" -I - "$short_link/UNEXPECTED_SOCKET" <<'PY'
import socket
import sys

node = socket.socket(socket.AF_UNIX)
node.bind(sys.argv[1])
node.close()
PY
      unlink "$short_link"
      ;;
    pyc) print -- hostile >"$copy/UNEXPECTED.PYC" ;;
    pycache) mkdir "$copy/__PyCaChE__" ;;
    *) print -u2 -- "unknown package case: $mode"; exit 1 ;;
  esac
  expected_failure "package_$mode" 1 "$expected_text" \
    "$trusted_python" -I "$copy/verify_referee_package.py"
}

package_case extra-file "package node-set mismatch"
package_case extra-dir "package node-set mismatch"
package_case symlink "package contains a symlink"
package_case fifo "package contains a special node"
package_case socket "package contains a special node"
package_case pyc "package contains forbidden bytecode"
package_case pycache "package contains a forbidden bytecode/cache directory"

source_reject="$case_root/source-bytecode-reject"
cp -a "$package/source_and_certificates" "$source_reject"
target_relative="universal_simultaneous_amplification/phase4_landmark_closure/obstruction/r2_collision_closure/verify_direct_flow_screen.py"
"$trusted_python" -I \
  "/Users/alec/Documents/Math/complete_graph_extremality_r2_rereview_2026-08-22/records/build_timestamp_cache_fixture.py" \
  "$source_reject/$target_relative" >"$case_root/logs/bytecode_fixture_path.log"
negative_paper="$source_reject/universal_simultaneous_amplification/phase5_exact_threshold/paper_db_extremality"
expected_failure independent_valid_pyc_rejection 1 \
  "bundle tree contains a forbidden bytecode/cache directory" \
  env -i HOME="$case_root/home" TMPDIR="$case_root/tmp" \
  PATH=/opt/homebrew/bin:/usr/bin:/bin BOOTSTRAP_PYTHON="$trusted_python" \
  "$negative_paper/submission/bootstrap_replay.sh" --certified-package-stage
if find "$source_reject" -name PYCACHE_EXECUTED -print -quit | grep . >/dev/null; then
  print -u2 -- "FAIL: hostile bytecode marker appeared before exact-tree rejection"
  exit 1
fi
print -- "PASS: independently built timestamp-valid bytecode was rejected before import"

source_execute="$case_root/source-bytecode-execution-demo"
cp -a "$package/source_and_certificates" "$source_execute"
"$trusted_python" -I \
  "/Users/alec/Documents/Math/complete_graph_extremality_r2_rereview_2026-08-22/records/build_timestamp_cache_fixture.py" \
  "$source_execute/$target_relative" >"$case_root/logs/bytecode_demo_path.log"
(
  cd "$case_root/caller"
  "$trusted_python" -I - "$source_execute/$target_relative" <<'PY'
import importlib.util
from pathlib import Path
import sys

sys.path.insert(0, str(Path(sys.argv[1]).parent))
spec = importlib.util.spec_from_file_location("r3_hostile_pyc_demo", sys.argv[1])
if spec is None or spec.loader is None:
    raise SystemExit("cannot construct fixture import")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
PY
)
if [[ ! -f "$case_root/caller/PYCACHE_EXECUTED" ]]; then
  print -u2 -- "FAIL: timestamp-valid hostile bytecode fixture was not executable"
  exit 1
fi
if find "$source_execute" -name PYCACHE_EXECUTED -print -quit | grep . >/dev/null; then
  print -u2 -- "FAIL: execution-demo marker unexpectedly landed inside source tree"
  exit 1
fi
print -- "PASS: hostile pyc is demonstrably valid; relative sentinel lands in caller cwd"

print -- "ARTIFACT_ROOT: $case_root"
print -- "PASS: independent adversarial controls completed"
