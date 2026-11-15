"""Pure offline custody closure. No imports of builders/checkers or supplied code.

Default: authenticate the sealed local packet, original frozen inputs, and prior
packet bytes. Optional --live-baseline also compares the old website baseline.
Writes nothing; logs go to the caller's stdout. It never runs controls or science.
"""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import sys


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def verify(root, live_baseline=False):
    root = Path(root).resolve(); checks = 0

    def need(ok, why):
        nonlocal checks
        checks += 1
        if not ok: raise ValueError(why)

    def binding(path, size, digest):
        path = Path(path); need(not path.is_symlink() and path.is_file(), 'regular file: ' + str(path))
        raw = path.read_bytes(); need(len(raw) == size, 'size: ' + str(path)); need(sha(raw) == digest, 'SHA256: ' + str(path))
        return raw

    manifest_path = root / 'OWNED_MANIFEST.json'; seal_path = root / 'FINAL_SEAL.json'
    seal = json.loads(seal_path.read_text()); manifest_raw = manifest_path.read_bytes(); manifest = json.loads(manifest_raw)
    need(seal['manifest_SHA256'] == sha(manifest_raw), 'final manifest seal')
    need(seal['manifest_bytes'] == len(manifest_raw), 'manifest byte binding')
    rows = manifest['files']; names = [r['path'] for r in rows]
    need(len(names) == len(set(names)), 'unique owned paths')
    need(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names), 'owned relative namespace')
    actual = sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())
    need(actual == sorted(names + ['OWNED_MANIFEST.json', 'FINAL_SEAL.json']), 'complete owned regular-file namespace')
    need(not any(p.is_symlink() for p in root.rglob('*')), 'no hidden owned symlinks')
    for row in rows: binding(root / row['path'], row['bytes'], row['SHA256'])
    need(len(rows) == seal['owned_payload_count'], 'owned file count')
    frozen = json.loads((root / 'FROZEN_INPUTS.json').read_text())['files']
    need(len(frozen) == 607 and len({r['original_path'] for r in frozen}) == 607, 'all607 original bindings')
    for row in frozen:
        binding(row['original_path'], row['bytes'], row['SHA256'])
        binding(root / row['snapshot_path'], row['bytes'], row['SHA256'])
    boundary = (root / '.gitignore').read_text()
    need('/inputs/blobs/' in boundary.splitlines(), 'all raw input bodies private-ignored')
    for packet in json.loads((root / 'PROTECTED_PRIOR_PACKETS.json').read_text())['packets']:
        for row in packet['files']: binding(row['path'], row['bytes'], row['SHA256'])
    # Independently compare both complete ten-path output trees without a renderer.
    a, b = root / 'candidate-a/public', root / 'candidate-b/public'
    ar = sorted(str(p.relative_to(a)) for p in a.rglob('*') if p.is_file())
    br = sorted(str(p.relative_to(b)) for p in b.rglob('*') if p.is_file())
    need(ar == br and len(ar) == 10, 'paired exact10 namespaces')
    for rel in ar: need((a / rel).read_bytes() == (b / rel).read_bytes(), 'paired full bytes: ' + rel)
    if live_baseline:
        base = json.loads((root / 'FRESH_BASELINE.json').read_text()); public = Path(base['public_root'])
        need(sorted(str(p.relative_to(public)) for p in public.rglob('*') if p.is_file()) == sorted(r['path'] for r in base['public_files']), 'old585 released namespace remains current')
        for row in base['public_files']: binding(public / row['path'], row['bytes'], row['SHA256'])
        supplement = json.loads((root / 'ROOT_AUTHORIZED_CORE_SUPPLEMENT.json').read_text())
        need(supplement['authorized_current_SHA256'] == '405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0', 'exact authorized helper SHA')
        for row in base['installed_core_files'] + base['site_configurations']:
            if row['path'] == supplement['exact_original_path']:
                need(row == supplement['original_baseline_binding'], 'original supplementary baseline preserved')
                binding(row['path'], supplement['authorized_current_bytes'], supplement['authorized_current_SHA256'])
            else: binding(row['path'], row['bytes'], row['SHA256'])
        need(sha(Path(base['site_index_path']).read_bytes()) == base['site_index_SHA256'], 'website Git index unchanged')
    return {'status': 'PASS', 'scope': 'Pure offline custody; no semantic or scientific replay, no writes.', 'python': platform.python_version(),
        'optimized': not __debug__, 'checks': checks, 'owned_payloads': len(rows), 'original_inputs': len(frozen), 'paired_output_paths': len(ar),
        'private_ignored_bodies_still_locally_authenticated': True, 'live_baseline_explicitly_checked': live_baseline,
        'publication_installation_or_external_adoption_claim': False}


def main():
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument('--packet-root', required=True); ap.add_argument('--live-baseline', action='store_true')
    args = ap.parse_args()
    try: result = verify(args.packet_root, args.live_baseline)
    except Exception as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)}, indent=2)); sys.exit(1)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
