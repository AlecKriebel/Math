#!/usr/bin/env python3
"""Read-only verification; --write-receipt only writes this bundle's audit receipt."""
from pathlib import Path
import argparse, datetime, hashlib, json, re, subprocess

E = Path(__file__).resolve().parent

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        while b := f.read(1048576):
            h.update(b)
    return h.hexdigest()

def bound(p, b):
    return p.is_file() and p.stat().st_size == b['bytes'] and sha(p) == b['sha256']

def read(name):
    return json.loads((E / name).read_text())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write-receipt', action='store_true')
    args = ap.parse_args()
    problems = []
    baseline = read('preservation-before.json')
    for r in baseline['files']:
        if not bound(Path(r['path']), r):
            problems.append({'kind': 'preservation', 'path': r['path']})
    screenshots = read('screenshot-manifest.json')['captures']
    for r in screenshots:
        p = E / r['file']
        if not bound(p, r):
            problems.append({'kind': 'screenshot', 'path': r['file']})
        t = subprocess.check_output(['/usr/bin/sips', '-g', 'pixelWidth', '-g', 'pixelHeight', str(p)], text=True)
        dims = [int(re.search(r'pixelWidth: (\d+)', t)[1]), int(re.search(r'pixelHeight: (\d+)', t)[1])]
        if dims != [r['width'], r['height']] or dims not in [[390,844], [2056,1146]]:
            problems.append({'kind': 'screenshot_dimensions', 'path': r['file'], 'actual': dims})
        m = r['metrics']
        if 'narrow' in r['file'] and (m['width'] != 390 or m['height'] != 844 or m['visualWidth'] != 390):
            problems.append({'kind': 'narrow_metrics', 'path': r['file']})
    downloads = read('actual-download-verification.json')['files']
    for r in downloads:
        b = {'bytes': r['expected_bytes'], 'sha256': r['expected_sha256']}
        for name in [r['path'], r['site_path'], *r['matching_primary_sources']]:
            if not bound(Path(name), b):
                problems.append({'kind': 'download_binding', 'path': name})
        if not r['matching_primary_sources']:
            problems.append({'kind': 'no_source_match', 'file': r['filename']})
    for r in read('inherited-root-evidence.json')['files']:
        if not bound(Path(r['path']), r):
            problems.append({'kind': 'inherited_evidence', 'path': r['path']})
    cleanup = read('browser-cleanup.json')
    if cleanup['remaining_own'] or not cleanup['all_original_ids_urls_preserved']:
        problems.append({'kind': 'browser_cleanup'})
    events = read('browser-events.json')
    returns = [r for r in events if r['step'].endswith('actual-Research-return')]
    if not {'slit-narrow-actual-Research-return', 'gaussian-desktop-actual-Research-return', 'gaussian-narrow-actual-Research-return'} <= {r['step'] for r in returns}:
        problems.append({'kind': 'missing_return'})
    for r in returns:
        if r['url'] != 'https://aleckriebel.com/research/' or r['index']['count'] != 52:
            problems.append({'kind': 'index_return', 'step': r['step']})
    manifest = E / 'evidence-manifest.json'
    if manifest.is_file():
        for r in read('evidence-manifest.json')['files']:
            if not bound(E / r['file'], r):
                problems.append({'kind': 'evidence_manifest', 'path': r['file']})
        if sha(manifest) != read('SEAL.json')['evidence_manifest_sha256']:
            problems.append({'kind': 'seal'})
    result = {
        'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'all_custody_checks_pass': not problems,
        'main_two_paper_browser_gates': 'PASS with independently visible article/PDF evidence; script verifies custody only',
        'preservation_paths': len(baseline['files']),
        'public_site_files': baseline['public_site_files'],
        'distinct_screenshot_files': len(screenshots),
        'capture_events': len(read('capture-events.json')),
        'actual_downloads': len(downloads),
        'distinct_download_tabs': len({r['tab_id'] for r in downloads}),
        'remaining_own_tabs': len(cleanup['remaining_own']),
        'original_tabs_preserved': cleanup['protected_tab_count'],
        'amplifier_legacy_browser_gate': 'PENDING: old article observed at ordinary old URL',
        'native_sheet_or_overall_programme_PASS_claimed': False,
        'problems': problems,
    }
    if args.write_receipt:
        (E / 'audit-receipt.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return bool(problems)

if __name__ == '__main__':
    raise SystemExit(main())
