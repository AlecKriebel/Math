"""SOURCE-ONLY UNEXECUTED ROOT readback helper. Never runs scientific operators.

Usage: python root_readback_geometric_family.py /absolute/ROOT_CLOSE.json /absolute/READBACK.json
ROOT must own/capture this actual run. Private primary cache is not accessed.
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# The imported module only defines lean custody validation; its main is guarded.
sys.dont_write_bytecode = True  # Preserve exact inventory; no __pycache__ mutation.
from root_close_geometric_family import FAMILY, digest, validate


def main():
    assert len(sys.argv) == 3
    prior_path = Path(sys.argv[1]).resolve(); output = Path(sys.argv[2]).resolve()
    assert FAMILY not in prior_path.parents and FAMILY not in output.parents
    assert not output.exists()
    prior_bytes = prior_path.read_bytes(); prior = json.loads(prior_bytes)
    fresh = validate()
    for key, value in fresh.items(): assert prior[key] == value
    assert prior['validation_complete'] and prior['executing_pid'] > 0
    result = {'schema': 'pr57-geometric-ROOT-readback-receipt/v1',
              'utc': datetime.now(timezone.utc).isoformat(), 'executing_pid': os.getpid(),
              'original_close_receipt_absolute_path': str(prior_path),
              'original_close_receipt_sha256': digest(prior_bytes),
              'readback_matches_current_full_bytes_modes': True, 'validation': fresh,
              'private_primary_cache_read': False, 'mathematical_operators_executed': False,
              'receipt_is_actual_only_if_owned_and_captured_by_ROOT': True}
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x') as f: f.write(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__': main()
