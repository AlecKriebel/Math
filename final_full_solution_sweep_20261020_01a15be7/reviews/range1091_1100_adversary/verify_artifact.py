#!/usr/bin/env python3
"""Read-only offline check of this bounded review's captured artifacts.

Run a byte-identical NEW PRIVATE COPY of this script, supplying an externally
trusted OUTPUT_MANIFEST.json SHA-256 and the review directory. No network,
archive execution/import/extraction, Git operations, writes, or universal proof
or priority certification. Captures attest their stated retrieval time only.
"""
import argparse
import ast
import hashlib
import html
import json
import math
import re
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath

CHECKPOINT = '3d96b1a20c93d0bcb0f1826cfe9f19a967cf3563'
ROOT_TREE = 'df34bc3b5f7a40cb58cd7259e2958fd5e85103bf'
EFFORT_TREE = '92da973052ccf01e609b1714c2f861efb794fb65'
EFFORT = 'final_full_solution_sweep_20261020_01a15be7'
BASE = 'f6caddda8f8be2cdb3e91494325d8f7f365bc3fc'
HEADS = [
 '2b201686b2273798824154c0620bd265d466cfea',
 'e292fdce71eba508a5d1e9b5bed8e42402dd1484',
 '886b8432b349c46718300431ea27c2c755067d97',
 '954dd70b49458026e29b8dae63243391249008d8',
 '842fe594fc8722b5fda18f2fb83ecae8b0f40f01',
 '1abfe8a9e0747bf5d509bc0f89f28cf8d2b7875d',
 'ad7b0eeef847da65afe1b691705cfa6e832e8201',
 'f37a3ff66595fcf75bb18bf859be8594c3662242',
 '7c98ebe6a6952917a707106a288a2d8588284eca',
 '1a3bcb164bc2a7a6708283c02aa2ca676c7f6b05']
COUNTS = [6, 7, 7, 8, 10, 8, 8, 9, 8, 8]
PUBLIC = {'.gitignore', 'REVIEW.md', 'CHECK_RESULTS.json', 'RESEARCH_LOG.md', 'verify_artifact.py'}
PUBS = [(1094, 23431313, 146, '2100509', 129, 128, 109),
        (1097, 23431676, 147, '3000016', 198, 197, 760),
        (1098, 23431716, 148, '3000018', 124, 123, 86)]

def need(ok, text):
    if not ok:
        raise ValueError(text)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def gitblob(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def pairs(xs):
    v = {}
    for k, x in xs:
        need(k not in v, 'duplicate JSON key: ' + k)
        v[k] = x
    return v

def strict(b):
    def bad(x):
        raise ValueError('nonfinite JSON: ' + x)
    def number(x):
        n = float(x)
        need(math.isfinite(n), 'nonfinite JSON number')
        return n
    return json.loads(b, object_pairs_hook=pairs, parse_constant=bad, parse_float=number)

def pathok(s):
    need(isinstance(s, str) and s and '\\' not in s and '\0' not in s, 'unsafe path')
    p = PurePosixPath(s)
    need(not p.is_absolute() and '..' not in p.parts and '.' not in p.parts and str(p) == s,
         'noncanonical path: ' + s)
    return s

def treehash(entries):
    entries = sorted(entries, key=lambda e: (e['path'] + ('/' if e['type'] == 'tree' else '')).encode())
    b = b''.join(e['mode'].lstrip('0').encode() + b' ' + e['path'].encode() + b'\0' + bytes.fromhex(e['sha']) for e in entries)
    return hashlib.sha1(b'tree ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def inventory(root):
    files, dirs = set(), set()
    def visit(folder, prefix):
        for p in folder.iterdir():
            name = prefix + p.name
            pathok(name)
            mode = p.lstat().st_mode
            need(not stat.S_ISLNK(mode), 'symlink: ' + name)
            if stat.S_ISDIR(mode):
                dirs.add(name)
                visit(p, name + '/')
            else:
                need(stat.S_ISREG(mode), 'nonregular entry: ' + name)
                files.add(name)
    visit(root, '')
    need(len(files | dirs) == len({x.casefold() for x in files | dirs}), 'case aliases')
    return files, dirs

def check_records(root, records):
    need(isinstance(records, list), 'records must be array')
    names = []
    for r in records:
        need(isinstance(r, dict) and set(r) == {'path', 'bytes', 'sha256'}, 'record schema')
        pathok(r['path'])
        need(type(r['bytes']) is int and r['bytes'] >= 0, 'invalid byte count')
        need(isinstance(r['sha256'], str) and re.fullmatch('[0-9a-f]{64}', r['sha256']) is not None, 'invalid hash')
        b = (root / r['path']).read_bytes()
        need(len(b) == r['bytes'] and sha(b) == r['sha256'], 'byte/hash mismatch: ' + r['path'])
        names.append(r['path'])
    need(names == sorted(names) and len(names) == len(set(names)) == len({x.casefold() for x in names}), 'unordered/duplicate paths')
    return set(names)

def run(root, anchor):
    need(root.exists() and not root.is_symlink() and root.is_dir(), 'invalid review root')
    need(re.fullmatch('[0-9a-f]{64}', anchor) is not None, 'invalid external anchor')
    manifest_bytes = (root / 'OUTPUT_MANIFEST.json').read_bytes()
    need(sha(manifest_bytes) == anchor, 'external manifest anchor mismatch')
    need((root / 'OUTPUT_MANIFEST.sha256').read_bytes() == (anchor + '  OUTPUT_MANIFEST.json\n').encode(), 'sidecar mismatch')
    m = strict(manifest_bytes)
    need(set(m) == {'schema', 'checkpoint', 'reviewed_prs', 'scope', 'public', 'private'}, 'manifest schema')
    need(m['schema'] == 'range1091-1100-review-v1' and m['checkpoint'] == CHECKPOINT and m['reviewed_prs'] == list(range(1091, 1101)), 'manifest identity')
    need(m['scope'] == 'bounded_disposition_and_existing_publication_coverage_only', 'manifest scope')
    need(set(m['private']) == {'records', 'directories'}, 'private schema')
    files, dirs = inventory(root)
    pub = check_records(root, m['public'])
    private = check_records(root / 'private', m['private']['records'])
    need(pub == PUBLIC, 'public file closure')
    privdirs = m['private']['directories']
    need(isinstance(privdirs, list) and all(isinstance(x, str) for x in privdirs), 'private directories schema')
    for x in privdirs:
        pathok(x)
    need(privdirs == sorted(set(privdirs)), 'private directories unique/order')
    need(files == PUBLIC | {'OUTPUT_MANIFEST.json', 'OUTPUT_MANIFEST.sha256'} | {'private/' + x for x in private}, 'closed full file inventory')
    need(dirs == {'private'} | {'private/' + x for x in privdirs}, 'closed directory inventory')
    need(Path(__file__).read_bytes() == (root / 'verify_artifact.py').read_bytes(), 'executing verifier differs from sealed source')
    need((root / '.gitignore').read_bytes() == b'private/\n', 'private ignore rule')
    P = root / 'private'
    def load(s):
        return strict((P / s).read_bytes())
    c = load('remote_commit.json')
    rt = load('remote_root_tree.json')
    et = load('remote_effort_tree.json')
    need(c['sha'] == CHECKPOINT and c['tree']['sha'] == ROOT_TREE and rt['sha'] == ROOT_TREE and not rt['truncated'], 'checkpoint root binding')
    need(treehash(rt['tree']) == ROOT_TREE, 'root Git tree hash')
    need(next(x['sha'] for x in rt['tree'] if x['path'] == EFFORT) == EFFORT_TREE and et['sha'] == EFFORT_TREE and not et['truncated'], 'effort tree binding')
    idx = {x['path']: x for x in et['tree']}
    need(len(idx) == len(et['tree']), 'duplicate effort tree paths')
    groups = {'': []}
    for e in et['tree']:
        pathok(e['path'])
        parent = str(PurePosixPath(e['path']).parent)
        parent = '' if parent == '.' else parent
        groups.setdefault(parent, []).append(dict(e, path=PurePosixPath(e['path']).name))
        if e['type'] == 'tree':
            groups.setdefault(e['path'], [])
    for folder, entries in groups.items():
        expected = EFFORT_TREE if folder == '' else idx[folder]['sha']
        need(treehash(entries) == expected, 'recursive Git tree: ' + folder)
    frozen_files = ['STATE.json', 'dispositions.jsonl', 'rest_inventory.json', 'ROOT_DISPOSABLE_DUPLICATE_COMPACTION_20261021.json']
    sr = load('STRUCTURAL_RESULTS.json')
    need(sr['checkpoint'] == CHECKPOINT and sr['actual_paths'] == 79 and len(sr['cases']) == 10, 'structural receipt')
    for e in sr['parent_pins']:
        b = (P / 'frozen' / e['path']).read_bytes()
        need(len(b) == e['bytes'] and sha(b) == e['sha256'] and gitblob(b) == e['git_oid'] == idx[e['path']]['sha'], 'parent pin')
        frozen_files.append(e['path'])
    for f in frozen_files:
        need(gitblob((P / 'frozen' / f).read_bytes()) == idx[f]['sha'], 'frozen immutable blob: ' + f)
    journal = [strict(x) for x in (P / 'frozen/dispositions.jsonl').read_bytes().splitlines()]
    need([j['pr'] for j in journal] == list(range(9, 1101)) and load('frozen/STATE.json')['next_pr'] == 1101, 'frozen journal coverage')
    inv = {x['number']: x for x in load('frozen/rest_inventory.json')['pull_requests']}
    for i, n in enumerate(range(1091, 1101)):
        s = sr['cases'][i]
        need(s['pr'] == n and s['head'] == HEADS[i] and s['base'] == BASE and s['paths'] == COUNTS[i], 'case identity')
        p = inv[n]
        need(p['headRefOid'] == HEADS[i] and p['baseRefOid'] == BASE and sha((p['body'] or '').encode()) == s['body_sha256'], 'inventory identity')
        d = load(f'frozen/PR{n}_DISPOSITION.json')
        need(journal[n - 9] == d and d['inventory_head_sha'] == HEADS[i] and d['inventory_base_sha'] == BASE and d['inventory_body_sha256'] == s['body_sha256'], 'journal/disposition binding')
        scope = load(f'frozen/PR{n}_PINNED_SCOPE_VERIFICATION.json')
        need(scope['head'] == HEADS[i] and scope['base'] == BASE and scope['path_count'] == COUNTS[i] and scope['all_complete_paths_equal'] is True and scope['all_added_rows_equal'] is True and scope['added_queue_rows'] == [] and scope['queue_blobs'] == [], 'pinned scope')
        e = load(f'cache/eligibility{n}.json')
        blobs = load(f'original/{n}/BLOBS.json')
        need(len(blobs) == COUNTS[i] and len({b['path'] for b in blobs}) == COUNTS[i] and {b['path'] for b in blobs} == set(e['changed_paths']), 'actual complete paths')
        for b in blobs:
            pathok(b['path'])
            need(PurePosixPath(b['path']).name != 'QUEUE.md', 'unexpected QUEUE edit')
            raw = (P / f'original/{n}' / b['path']).read_bytes()
            cached = [x for x in e['files'] if x['filename'] == b['path']]
            need(len(cached) == 1 and cached[0]['sha'] == b['git_oid'] == gitblob(raw) and len(raw) == b['bytes'] and sha(raw) == b['sha256'], 'actual blob identity')
        for folder in ['live', 'final_live']:
            live = load(f'{folder}/{n}.json')
            need(live['number'] == n and live['head']['sha'] == HEADS[i] and live['base']['sha'] == BASE and sha((live['body'] or '').encode()) == s['body_sha256'], 'live capture identity')
            need(live['merged'] is (n in [1094, 1097, 1098]), 'live merged state')
    rows = load('sheet_final.json')['values']
    need(rows[0] == ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes'], 'sheet schema')
    for n, record, row, problem, members, payloads, copies_expected in PUBS:
        prefix = f'pub{n}/'
        api = load(prefix + 'record.json')
        receipt = load(prefix + 'FETCH_RECEIPTS.json')
        need(api['id'] == record and api['doi'] == f'10.5281/zenodo.{record}' and api['submitted'] is True, 'published record identity')
        need(receipt['doi_resolution']['status'] == 200 and receipt['doi_resolution']['final_url'] == f'https://zenodo.org/records/{record}', 'DOI captured resolution')
        need([i for i, r in enumerate(rows, 1) if len(r) > 2 and r[2] == f'https://doi.org/10.5281/zenodo.{record}'] == [row], 'unique DOI ledger row')
        need(rows[row - 1] == load('sheet.json')['values'][row - 1] and '/pull/' + str(n) in rows[row - 1][0] and re.search(r'(?<!\d)' + problem + r'(?!\d)', rows[row - 1][0]), 'semantic row identity')
        need(len(api['files']) == 2, 'all provider payloads')
        zpath = None
        for f in api['files']:
            pathok(f['key'])
            b = (P / prefix / f['key']).read_bytes()
            need(type(f['size']) is int and len(b) == f['size'] and 'md5:' + hashlib.md5(b).hexdigest() == f['checksum'], 'provider size/MD5')
            rr = [x for x in receipt['files'] if x['name'] == f['key']]
            need(len(rr) == 1 and len(b) == rr[0]['bytes'] and sha(b) == rr[0]['sha256'] and rr[0]['receipt']['status'] == 200, 'provider SHA-256 receipt')
            if f['key'].endswith('.zip'):
                zpath = P / prefix / f['key']
        need(zpath is not None, 'missing support ZIP')
        pdf = (P / prefix / 'paper.pdf').read_bytes()
        with zipfile.ZipFile(zpath) as z:
            names = z.namelist()
            need(len(names) == members and len(names) == len(set(names)) == len({x.casefold() for x in names}) and z.testzip() is None, 'archive unique/CRC/count')
            for x in z.infolist():
                pathok(x.filename)
                need(not x.is_dir() and not x.flag_bits & 1 and stat.S_IFMT(x.external_attr >> 16) in [0, stat.S_IFREG], 'unsafe archive entry')
            def zj(s):
                return strict(z.read(s))
            def zb(s, e):
                b = z.read(s)
                need(type(e['bytes']) is int and len(b) == e['bytes'] and sha(b) == e['sha256'], 'archive bound copy: ' + s)
                return b
            es = zj('MANIFEST.json')['records' if n == 1094 else 'entries']
            need(len(es) == payloads and len({e['path'] for e in es}) == payloads and set(names) == {'MANIFEST.json'} | {e['path'] for e in es}, 'closed archive manifest')
            for e in es:
                zb(e['path'], e)
            ps = 'historical/SUBMITTED_PINS.json' if n == 1094 else 'provenance/selected/SUBMITTED_PINS.json' if n == 1097 else 'history/SUBMITTED_PINS.json'
            originals = load(f'original/{n}/BLOBS.json')
            pins = zj(ps)['files']
            need(len(pins) == len(originals) and {x['repository_path'] for x in pins} == {x['path'] for x in originals}, 'all actual originals covered')
            for e in pins:
                need(zb(str(PurePosixPath(ps).parent) + '/' + e['snapshot_path'], e) == (P / f'original/{n}' / e['repository_path']).read_bytes(), 'actual head/snapshot bytes')
            cfg = zj('metadata.json')
            copies = 0
            if n == 1094:
                need(cfg == zj('.zenodo.json') == zj('metadata_api.json')['metadata'] and z.read('paper.pdf') == pdf, '1094 metadata/PDF')
                for mf in ['CUSTODY_MAP.json', 'TERMINAL_SOURCE_COPY_LEDGER.json']:
                    for e in zj(mf)['copies']:
                        zb(e['copy_path'], e)
                        copies += 1
            elif n == 1097:
                need(cfg == zj('zenodo-metadata.json')['metadata'] and z.read('paper.pdf') == pdf, '1097 metadata/PDF')
                exceptions = []
                for mf in ['provenance/CUSTODY.json', 'provenance/repair01/CUSTODY.json', 'provenance/terminal_admin_20261016/CUSTODY.json']:
                    for e in zj(mf)['entries']:
                        if 'copy_path' not in e:
                            continue
                        loc = e['copy_path']
                        raw = z.read(loc)
                        if len(raw) != e['bytes'] or sha(raw) != e['sha256']:
                            need(mf == 'provenance/repair01/CUSTODY.json' and loc == 'scripts/verify.py' and e['bytes'] == 627 and e['sha256'] == 'd16d1508cafd9cb2a85af016b8f0c5610f13c38f9a80398941a7727f2a3da2cb', 'unrecognized historical stale locator')
                            loc = 'provenance/terminal_admin_20261016/before/kit/scripts/verify.py'
                            exceptions.append(loc)
                        zb(loc, e)
                        copies += 1
                need(len(exceptions) == 1, 'exactly one qualified before-copy locator')
                current = zj('provenance/terminal_admin_20261016/STAGE_RESOLUTION.json')['entries']
                need(len(current) == 4025, 'current stage resolution rows')
                exact = 0
                for e in current:
                    rr = e['portable_resolution']
                    if rr['state'] == 'EXACT_DISTRIBUTED_BYTES':
                        zb(rr['path'], e)
                        exact += 1
                need(exact == 3001, 'current exact resolution count')
                cp = zj('provenance/terminal_admin_20261016/COPIES.json')['entries']
                need(len(cp) == 37, 'terminal copies')
                for e in cp:
                    zb(e['copy_path'], e)
            else:
                need(cfg == zj('zenodo-api.json')['metadata'] == zj('publication/zenodo-deposit.json')['metadata'], '1098 native metadata')
                source = ast.parse(z.read('code/metadata_constants.py'))
                constants = [x for x in source.body if isinstance(x, ast.Assign) and isinstance(x.targets[0], ast.Name) and x.targets[0].id == 'EXPECTED_METADATA']
                need(len(constants) == 1 and ast.literal_eval(constants[0].value) == cfg, '1098 parsed metadata constant')
                binding = zj('ARTIFACT_BINDINGS.json')['paper.pdf']
                need('paper.pdf' not in names and len(pdf) == binding['bytes'] and sha(pdf) == binding['sha256'], 'mandatory external PDF binding')
                for mf in ['CUSTODY_SELECTION.json', 'terminal/REVIEW_STAGE_SELECTION.json']:
                    for e in zj(mf)['entries']:
                        if e.get('disposition') == 'EXACT_AUTHORED_COPY':
                            zb(e['destination'], e)
                            copies += 1
            need(copies == copies_expected, 'selected copy count')
            meta = api['metadata']
            need(meta['resource_type']['type'] == cfg['upload_type'] and meta['resource_type']['subtype'] == cfg['publication_type'] and meta['license']['id'] == cfg['license'], 'native type/license mapping')
            for k, v in cfg.items():
                if k in ['upload_type', 'publication_type', 'license']:
                    continue
                need(html.unescape(meta[k]) == html.unescape(v) if k == 'description' else meta[k] == v, 'all authored provider metadata: ' + k)
            need(z.read('paper.tex') == (P / prefix / 'paper.tex').read_bytes(), 'read manuscript exact source')
    controls = load('CONTROL_RECEIPTS.json')
    need(len(controls) == 3 and [x['mode'] for x in controls] == [[], ['-O'], ['-OO']] and all(x['returncode'] == 0 and x['stderr'] == '' for x in controls) and len({x['stdout'] for x in controls}) == 1, 'finite control receipts')
    finite = strict(controls[0]['stdout'])
    need(finite['finite_controls_only'] is True and finite['archive_code_imported_or_executed'] is False and finite['universal_theorem_priority_or_historical_replay_certificate'] is False, 'control limits')
    cr = strict((root / 'CHECK_RESULTS.json').read_bytes())
    need(cr['checkpoint'] == CHECKPOINT and cr['reviewed_prs'] == list(range(1091, 1101)) and cr['new_publications'] == 0 and cr['actionable_substantive_findings'] == [] and cr['universal_or_priority_certificate'] is False, 'review result scope')
    return {'result': 'PASS', 'checkpoint': CHECKPOINT, 'prs': 10, 'actual_blobs': 79,
            'existing_publications': 3, 'public_payloads': len(pub), 'private_payloads': len(private),
            'private_directories': len(privdirs), 'archive_code_executed': False,
            'scope': 'captured bytes, identities, archive coverage, and bounded review only'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--expected-public-sha256', required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(run(args.root, args.expected_public_sha256), sort_keys=True))
    except (OSError, ValueError, KeyError, TypeError, IndexError, StopIteration, zipfile.BadZipFile, SyntaxError) as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        sys.exit(1)
