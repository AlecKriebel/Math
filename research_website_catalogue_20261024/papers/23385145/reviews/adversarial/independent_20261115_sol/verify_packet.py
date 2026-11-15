#!/usr/bin/env python3
"""Read-only closure. No file writes/network; optional own bounded replay only."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23385145/sources')
EARLY_SHA = '9efb733a7681c935c9b65918756b9e7526ed7be40103df5f273c2cff590e6f02'
READY_SHA = '398351e05ac4ddc92510ea191c109dd22a48a177869872a8008ff2f8328581e5'
LITERAL = 'The full finite vertex-center theorem is supported in its stated exact-comparison model; no substantive gap found.'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def relative(value):
    require(type(value) is str and value and '\\' not in value and ':' not in value, 'Invalid relative path')
    q = PurePosixPath(value)
    require(not q.is_absolute() and '..' not in q.parts and q.as_posix() == value, 'Unsafe relative path')
    return Path(value)


def check_blob(data, record):
    require(type(record['bytes']) is int and record['bytes'] >= 0, 'Invalid byte count')
    require(len(data) == record['bytes'] and digest(data) == record['sha256'], 'Whole-byte binding mismatch')


def check_record(base, record):
    q = base / relative(record['path'])
    require(q.is_file() and not q.is_symlink() and q.resolve().is_relative_to(base), 'Missing, linked or escaped payload')
    check_blob(q.read_bytes(), record)


def inventory(base):
    result = set()
    for q in base.rglob('*'):
        require(not q.is_symlink(), 'Unexpected symlink')
        if q.is_file():
            result.add(q.relative_to(base).as_posix())
    return result


def self_checks():
    count = 0
    for value in ['', '../x', '/x', 'a/../x', 'a\\x', 'a:x', 'a//x']:
        try:
            relative(value)
        except RuntimeError:
            count += 1
        else:
            raise RuntimeError('Unsafe-path negative control escaped')
    record = {'bytes': 1, 'sha256': digest(b'a')}
    check_blob(b'a', record)
    for data, rec in [(b'b', record), (b'aa', record), (b'a', {'bytes': True, 'sha256': digest(b'a')})]:
        try:
            check_blob(data, rec)
        except RuntimeError:
            count += 1
        else:
            raise RuntimeError('Binding negative control escaped')
    return count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--preseal', action='store_true', help='Only for assembling this packet; final closure uses the outer seal.')
    ap.add_argument('--custody-only', action='store_true', help='Skip the bounded own mathematical replay.')
    args = ap.parse_args()
    manifest_path = ROOT / 'OWNED_MANIFEST.json'
    mb = manifest_path.read_bytes()
    manifest = json.loads(mb)
    require(manifest['owned_root'] == str(ROOT), 'Wrong owned root')
    require(manifest['record_id'] == 23385145, 'Wrong record')
    records = manifest['files']
    names = [r['path'] for r in records]
    require(len(names) == len(set(names)), 'Duplicate owned paths')
    require(set(names) == inventory(ROOT) - {'OWNED_MANIFEST.json', 'FINAL_SEAL.json'}, 'Owned inventory mismatch')
    for record in records:
        check_record(ROOT, record)
    if not args.preseal:
        seal = json.loads((ROOT / 'FINAL_SEAL.json').read_bytes())
        require(seal['record_id'] == 23385145 and seal['owned_manifest_sha256'] == digest(mb), 'Outer seal mismatch')
        require(seal['source_bindings_sha256'] == digest((ROOT / 'SOURCE_BINDINGS.json').read_bytes()), 'Source binding seal mismatch')
        require(seal['early_seal_sha256'] == EARLY_SHA, 'Wrong early seal pin')
        require(seal['scientific_findings_withheld_pending_root118_gate'] is True, 'Gate history altered')
    early_bytes = (ROOT / 'EARLY_INDEPENDENCE_SEAL.json').read_bytes()
    require(digest(early_bytes) == EARLY_SHA, 'Early independence seal changed')
    es = json.loads(early_bytes)
    em = (ROOT / es['manifest']).read_bytes()
    require(digest(em) == es['manifest_sha256'], 'Early manifest changed')
    for record in json.loads(em)['files']:
        check_record(ROOT / 'early', record)
    require(es['families'] == 8 and es['full_PDF_pages_read'] == 5 and es['controlling_TeX_lines_read'] == 311, 'Early reading contract mismatch')
    require(es['foreign_code_results_data_triage_primary_peer_opinions_before_seal'] is False, 'Independence history mismatch')
    sb = json.loads((ROOT / 'SOURCE_BINDINGS.json').read_bytes())
    require(sb['source_root'] == str(SOURCE), 'Wrong source root')
    source_paths = set()
    for record in sb['bindings']:
        q = Path(record['path'])
        require(q.is_absolute() and q.is_file() and not q.is_symlink() and q.resolve().is_relative_to(SOURCE), 'External binding escaped source')
        require(str(q) not in source_paths, 'Duplicate external binding')
        source_paths.add(str(q))
        check_blob(q.read_bytes(), record)
    require(digest((SOURCE / 'SOURCE_READY.json').read_bytes()) == READY_SHA, 'Wrong original source readiness')
    v = json.loads((ROOT / 'CUSTOM_VERDICT.json').read_bytes())
    require(v['literal_custom_verdict'] == LITERAL and v['full_original_quantified_claim_checked'] is True and v['narrowed_promotion_or_new_repair'] is False, 'Custom verdict mismatch')
    require(v['source_site_core_Sheet_Git_old_packet_mutations'] is False, 'Authority fence mismatch')
    normal = (ROOT / 'computations/own-normal.stdout').read_bytes()
    optimized = (ROOT / 'computations/own-optimized.stdout').read_bytes()
    require(normal == optimized, 'Own normal/optimized output difference')
    own = json.loads(normal)
    require(own['status'] == 'PASS' and all(own['excluded_wrong_variant_falsifiers'].values()) and len(own['excluded_wrong_variant_falsifiers']) == 8, 'Own result mismatch')
    for mode in ['normal', 'optimized']:
        receipt = json.loads((ROOT / ('computations/own-' + mode + '.receipt.json')).read_bytes())
        require(receipt['exit_code'] == 0, 'Own recorded execution failed')
        require((ROOT / ('computations/own-' + mode + '.stderr')).read_bytes() == b'', 'Own recorded stderr')
    r = ROOT / 'reproduction'
    supplied = json.loads((r / 'run-all-normal.receipt.json').read_bytes())
    require(supplied['exit_code'] == 0 and supplied['source_package_unchanged'] is True, 'Supplied replay failed')
    require((r / 'NATIVE_PACKAGE_BEFORE.json').read_bytes() == (r / 'NATIVE_PACKAGE_AFTER.json').read_bytes(), 'Native package changed')
    rows = [json.loads(line) for line in (r / 'run-all-normal.stdout').read_text().splitlines()]
    require(len(rows) == 6 and all(x['status'] == 'PASS' for x in rows), 'Supplied replay job result mismatch')
    last = rows[-1]
    for k, value in {'outer_payloads_verified':92, 'nested_entries_verified':54, 'original_inputs_verified':16, 'replayed_jobs':5, 'offline':True, 'frozen_payloads_unchanged':True}.items():
        require(last[k] == value, 'Supplied summary mismatch: ' + k)
    refusal = json.loads((r / 'run-all-optimized-rejection.receipt.json').read_bytes())
    require(refusal['exit_code'] == 1 and refusal['expected_rejection'] is True, 'Supplied optimized-mode refusal lost')
    require(b'Run with assertions enabled' in (r / 'run-all-optimized-rejection.stderr').read_bytes(), 'Wrong supplied refusal')
    negative = self_checks()
    replayed = False
    if not args.custody_only:
        command = [sys.executable, '-E', '-B'] + (['-O'] if sys.flags.optimize else []) + [str(ROOT / 'own_controls.py')]
        proc = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=90)
        require(proc.returncode == 0 and proc.stderr == b'' and proc.stdout == normal, 'Own full-output read-only replay mismatch')
        replayed = True
    print(json.dumps({'status':'PASS', 'record_id':23385145, 'owned_payloads_verified':len(records), 'source_bindings_verified':len(source_paths), 'early_owned_payloads_verified':len(json.loads(em)['files']), 'custody_negative_controls':negative, 'own_bounded_mathematical_replay':replayed, 'supplied_campaign_replayed_again':False, 'source_or_site_or_owned_writes':0, 'network':0, 'preseal_mode':args.preseal}, sort_keys=True))


if __name__ == '__main__':
    main()
