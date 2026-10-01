#!/usr/bin/env python3
"""Reproduce this exact-head audit without installs or publication/Git writes.

Source downloads, extracted text, runtime and unchanged script copies belong only
in the ignored .tmp folder. Use --refresh-sources for independent current PDF
downloads. A Python with SymPy 1.14.0, or the already provisioned ignored runtime,
is needed only to replay the old reviewer script.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parent
HEAD = '90a81313f3f65a7914fb6d5a9950fa087ea7467e'
PREFIX = 'unsolved_math_prioritization/attempts/7000019/'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def demand(yes, why):
    if not yes:
        raise AssertionError(why)


def main():
    args = argparse.ArgumentParser()
    args.add_argument('--refresh-sources', action='store_true')
    args.add_argument('--legacy-python', default=sys.executable)
    options = args.parse_args()
    repo = next(p for p in ROOT.parents if (p / '.git').exists())
    tmp = ROOT / '.tmp'
    tmp.mkdir(exist_ok=True)
    receipt = {'head': HEAD, 'future_bytes_certified': False,
               'source_bytes': [], 'legacy_runs': []}
    snap = tmp / 'original_snapshot'
    for f in json.loads((ROOT / 'ORIGINAL_SNAPSHOT_RECEIPT.json').read_text())['files']:
        b = subprocess.check_output(['git', 'show', HEAD + ':' + f['path']], cwd=repo)
        demand(sha(b) == f['sha256'], f['path'] + ' differs from exact-head receipt')
        dest = snap / f['path']
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            demand(dest.read_bytes() == b, 'Stored snapshot changed: ' + f['path'])
        else:
            dest.write_bytes(b)
    sources = tmp / 'sources'
    sources.mkdir(exist_ok=True)
    initial = json.loads((ROOT / 'SOURCE_RECEIPT_INITIAL.json').read_text())
    for item in initial:
        if item['name'] == 'ghomi_mo2017':
            continue  # Dynamic HTML is a historical receipt, not a stable-byte test.
        dest = sources / (item['name'] + '.pdf')
        if options.refresh_sources or not dest.exists():
            b = urllib.request.urlopen(item['requested_url'], timeout=45).read()
            demand(sha(b) == item['sha256'], 'Current source PDF bytes changed')
            dest.write_bytes(b)
        demand(sha(dest.read_bytes()) == item['sha256'], 'Cached PDF bytes changed')
        subprocess.run(['pdftotext', '-layout', str(dest), str(dest.with_suffix('.txt'))], check=True)
        receipt['source_bytes'].append({'name': item['name'], 'sha256': sha(dest.read_bytes())})
    old = json.loads((ROOT / 'GHOMI_EARLIER_SOURCE_RECEIPT.json').read_text())
    dest = sources / 'ghomi2004.pdf'
    if options.refresh_sources or not dest.exists():
        b = urllib.request.urlopen(old['url'], timeout=45).read()
        demand(sha(b) == old['sha256'], 'Older source PDF bytes changed')
        dest.write_bytes(b)
    demand(sha(dest.read_bytes()) == old['sha256'], 'Older PDF bytes changed')
    subprocess.run(['pdftotext', '-layout', str(dest), str(dest.with_suffix('.txt'))], check=True)
    receipt['source_bytes'].append({'name': 'ghomi2004', 'sha256': sha(dest.read_bytes())})
    manifest = json.loads((repo / 'unsolved_math_prioritization/manifest.json').read_text())
    cache = repo / 'unsolved_math_prioritization/cache'
    for name, record in manifest['files'].items():
        b = (cache / name).read_bytes()
        demand(len(b) == record['bytes'] and sha(b) == record['sha256'], 'Raw dataset changed')
    db = sqlite3.connect((cache / 'catalog.sqlite').as_uri() + '?mode=ro&immutable=1', uri=True)
    row = db.execute('select payload,report from records where key=?', ('7000019',)).fetchone()
    demand(row is not None, 'Missing SQLite target')
    packet = snap / PREFIX
    demand(json.loads(row[0]) == json.loads((packet / 'source_record.json').read_text()),
           'SQLite source mismatch')
    demand(json.loads(row[1]) == json.loads((packet / 'prior_report.json').read_text()),
           'SQLite joined prior mismatch')
    demand(list(db.execute('select revision from metadata')) ==
           [('37e53eabe540fb458758e198be61634bd02ee008',)], 'SQLite revision mismatch')
    db.close()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    if (tmp / 'runtime/sympy').exists():
        env['PYTHONPATH'] = str(tmp / 'runtime')
    subprocess.run([options.legacy_python, '-c', 'import sympy; assert sympy.__version__ == "1.14.0"'],
                   env=env, check=True)
    replay = tmp / 'reproduce_legacy'
    for name, expected in [('verify.py', 'verification.json'),
                           ('review/submitted_verify.py', 'review/verification.json'),
                           ('review/independent_checks.py', 'review/independent_results.json')]:
        b = (packet / name).read_bytes()
        script = replay / name
        script.parent.mkdir(parents=True, exist_ok=True)
        script.write_bytes(b)
        r = subprocess.run([options.legacy_python, str(script)], capture_output=True, env=env, check=True)
        output = script.with_name('independent_results.json').read_bytes() if name.endswith(
            'independent_checks.py') else r.stdout
        demand(script.read_bytes() == b, 'Legacy script changed while running')
        demand(output == (packet / expected).read_bytes(), 'Legacy output is not byte-exact')
        receipt['legacy_runs'].append({'script': name, 'script_sha256': sha(b),
                                      'output_sha256': sha(output), 'byte_exact': True})
    subprocess.run([sys.executable, str(ROOT / 'controls.py')], check=True, cwd=repo)
    receipt['controls_result_sha256'] = sha((ROOT / 'CONTROLS_RESULT.json').read_bytes())
    first_party = ROOT / 'FIRST_PARTY_MANIFEST.json'
    if first_party.exists():
        manifest = json.loads(first_party.read_text())
        actual = sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*')
                        if p.is_file() and '.tmp' not in p.relative_to(ROOT).parts
                        and '__pycache__' not in p.relative_to(ROOT).parts
                        and p.name != 'FIRST_PARTY_MANIFEST.json')
        demand(actual == sorted(x['path'] for x in manifest['files']),
               'First-party manifest scope changed')
        for item in manifest['files']:
            b = (ROOT / item['path']).read_bytes()
            demand(len(b) == item['bytes'] and sha(b) == item['sha256'],
                   'First-party audit bytes changed: ' + item['path'])
        receipt['first_party_manifest_checked'] = True
    receipt['status'] = 'PASS_EXACT_ORIGINAL_HEAD_ONLY'
    (tmp / 'REPRODUCE_LAST_RUN.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
