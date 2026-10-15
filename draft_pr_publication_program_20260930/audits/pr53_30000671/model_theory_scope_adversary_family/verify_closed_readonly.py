"""UNEXECUTED separate ROOT-only readback; never writes this or another family."""
import json
import sys
from closed_scope_common import closed_check

def main():
    assert len(sys.argv) == 2 and len(sys.argv[1]) == 64
    n, ndirs, refs, caps = closed_check(sys.argv[1])
    print(json.dumps({'status': 'PASS_SEPARATE_ADVERSARY_READBACK_ONLY',
                      'actual_manifest_sha256': sys.argv[1], 'closed_files': n,
                      'directories': ndirs, 'external_fixed_references': refs,
                      'actual_independent_capture_objects': caps,
                      'root_approval': False, 'native_state_or_git_writes': False}))

if __name__ == '__main__':
    main()
