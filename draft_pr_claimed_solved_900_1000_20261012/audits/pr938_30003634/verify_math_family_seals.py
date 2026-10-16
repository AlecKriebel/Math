#!/usr/bin/env python3
"""Authenticate the final five audit maps; replay the independent Meyer route.

The mathematical judgments in the receipt require root's prior full reading of
the written arguments. This program authenticates evidence, not those judgments.
The last externally received seal must be supplied by the caller, never read
from a packet's self-assertion. No Git or service mutation is performed.
"""
import argparse
import datetime
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import root_replay

AUDIT = Path(__file__).absolute().parent


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--meyer-seal', required=True)
    args = parser.parse_args()
    need(re.fullmatch('[0-9a-f]{64}', args.meyer_seal), 'invalid supplied external seal')
    configurations = [
        ('topology_family', 'MANIFEST.json', '3a1d63dd809ffd527b193e323220ca7eb34d3acc93a3efc010820a0039e5694c'),
        ('goeritz_family', 'PUBLIC_MANIFEST.json', '4ad69f501889239782b6120a66fff9c4830fb683692eeebab5fdf59d5a899dda'),
        ('meyer_algebra_family', 'PUBLIC_MAP.json', args.meyer_seal),
        ('source_model_family', 'PUBLIC_MANIFEST.json', 'fe9ea4cc0bfc0c5ac4c017b9315a49f2c9cc5d2c6d9758795611c81740b1866a'),
        ('reproducibility_family', 'PUBLIC_MANIFEST.json', '342c41da878c06e5ad7d8967d128228a55b3ccb7d834ed55d626fc00b46fcd24'),
    ]
    _, original_before = root_replay.authenticate()
    rows = []
    authenticated = []
    for family, manifest_name, pin in configurations:
        folder = AUDIT / 'reviews' / family
        path = folder / manifest_name
        need(not path.is_symlink() and digest(path.read_bytes()) == pin, 'external map seal mismatch: ' + family)
        manifest = json.loads(path.read_bytes())
        files = manifest.get('files', manifest.get('records'))
        if isinstance(files, dict):
            entries = [dict(value, path=name) if isinstance(value, dict) else {'path': name, 'sha256': value} for name, value in files.items()]
        else:
            entries = files
        need(isinstance(entries, list) and entries, 'invalid curated map')
        names = set()
        for entry in entries:
            name = entry['path']
            need(isinstance(name, str) and not Path(name).is_absolute() and '..' not in Path(name).parts and name != manifest_name and name not in names, 'unsafe/duplicate/self map path')
            need(not any(part in {'private', 'tmp', 'raw', '__pycache__'} for part in Path(name).parts), 'private member')
            member = folder / name
            need(member.is_file() and not member.is_symlink(), 'nonregular curated member')
            raw = member.read_bytes()
            need(digest(raw) == entry['sha256'] and ('bytes' not in entry or type(entry['bytes']) is int and len(raw) == entry['bytes']), 'curated member mismatch')
            names.add(name)
            authenticated.append((member, digest(raw)))
        rows.append({'family': family, 'manifest': manifest_name, 'external_sha256': pin, 'curated_payload_count': len(entries), 'full_audit_and_result_read_by_root': True})
    folder = AUDIT / 'reviews/meyer_algebra_family'
    cp = subprocess.run([sys.executable, '-I', '-B', '-OO', str(folder / 'reproduce.py')], capture_output=True, timeout=180)
    need(cp.returncode == 0 and not cp.stderr, 'independent Meyer cold replay failed: ' + cp.stderr.decode(errors='replace')[-2000:])
    got = json.loads(cp.stdout)
    want = json.loads((folder / 'INDEPENDENT_RESULTS.json').read_bytes())
    got.pop('utc', None)
    want.pop('utc', None)
    need(got == want, 'independent Meyer mathematical output changed')
    for member, pin in authenticated:
        need(digest(member.read_bytes()) == pin, 'curated output changed during read-only replay')
    _, original_after = root_replay.authenticate()
    need(original_before == original_after, 'original44 changed')
    receipt = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'pr': 938, 'problem_id': 30003634, 'original_head': root_replay.HEAD, 'families': rows, 'curated_payload_count': sum(r['curated_payload_count'] for r in rows), 'original_files_actual_git_authenticated_before_and_after': 44, 'root_meyer_optimized_cold_replay': 'PASS full exact mathematical JSON, timestamp only omitted', 'root_other_independent_replays': ['ROOT_THREE_FAMILY_VERIFICATION.json', 'ROOT_REPRODUCIBILITY_FAMILY_VERIFICATION.json', 'ROOT_REPLAY_RECEIPT.json'], 'mathematical_judgment_from_written_arguments': 'No unresolved gap found: source ordinary-derived question, universal integral1solution signature obstruction, exact nested membership, independently certified nonzero ordinary signature, and stated n1/m>=3 scope all pass.', 'synthesis_conditions': 'All required/optional family clarifications retained in SYNTHESIS_REQUIREMENTS.md; originals remain provenance. Future paper and metadata must implement these conditions.', 'priority_verdict': 'NOT_STARTED; deep independent priority stage is next', 'publication_acceptance': False, 'original_author_turns': '1/5', 'positive_proof_search_turns_added': 0, 'completion_estimate_percent': 45}
    (AUDIT / 'ROOT_FINAL_MATH_REVIEW_VERIFICATION.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
