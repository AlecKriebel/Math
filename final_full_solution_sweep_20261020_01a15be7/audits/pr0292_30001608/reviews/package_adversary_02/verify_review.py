"""Read-only check of the final independent-review seal. Standard library only."""
from pathlib import Path
import argparse
import hashlib
import json


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def inspect(path, row):
    require(path.is_file() and not path.is_symlink(), 'Missing or symlinked file: ' + str(path))
    content = path.read_bytes()
    require(len(content) == row['bytes'], 'Size changed: ' + str(path))
    require(hashlib.sha256(content).hexdigest() == row['sha256'], 'Hash changed: ' + str(path))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--include-private', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    seal = json.loads((root / 'FINAL_SEAL.json').read_text())
    for row in seal['candidate_inputs']:
        inspect(Path(row['absolute_path']), row)
    checked = 0
    for row in seal['authored_evidence']:
        rel = Path(row['path'])
        require(not rel.is_absolute() and '..' not in rel.parts, 'Unsafe evidence path')
        inspect(root / rel, row)
        checked += 1
    if args.include_private:
        for row in seal['private_reading_identity_pins']:
            inspect(root / row['path'], row)
    verdict = json.loads((root / 'VERDICT.json').read_text())
    require(verdict['review_status'] == 'COMPLETE' and verdict['completion_percent'] == 100,
            'Review is incomplete')
    require(not verdict['mandatory_repairs'] and not verdict['material_objections'],
            'Unexpected unresolved objection')
    require(verdict['exact_remaining_mathematical_gap'] is None, 'Mathematical gap remains')
    print(json.dumps({'status': 'PASS_FINAL_REVIEW_SEAL', 'candidate_inputs': len(seal['candidate_inputs']),
                      'authored_evidence_files': checked, 'private_reading_checked': args.include_private,
                      'scope': 'Byte integrity and verdict consistency; no replacement for reading the proof.'},
                     indent=2))


if __name__ == '__main__':
    main()
