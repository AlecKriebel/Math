#!/usr/bin/env python3
"""Read-only offline authentication and bounded relationship replay. No network or subprocesses.
Run with a trusted interpreter: python3 -I -S -B verify_artifact.py --manifest-sha256 EXTERNAL_PIN.
The external pin and interpreter are trust inputs. Stable local inputs are assumed; no hostile-host sandbox.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: require -I -S -B startup')
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def unique(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, 'duplicate JSON key')
        out[key] = value
    return out


def load_bytes(data):
    return json.loads(data, object_pairs_hook=unique)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def safe(name):
    p = PurePosixPath(name)
    need(isinstance(name, str) and name and not p.is_absolute() and '..' not in p.parts
         and str(p) == name and '\\' not in name and all(ord(c) >= 32 and ord(c) != 127 for c in name), 'unsafe path')
    return name


def read(path):
    need(hasattr(os, 'O_NOFOLLOW'), 'O_NOFOLLOW required')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode), 'nonregular input')
        need(before.st_size <= 200_000_000, 'input size cap')
        with os.fdopen(fd, 'rb', closefd=False) as f:
            data = f.read(before.st_size + 1)
        after = os.fstat(fd)
        need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) ==
             (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), 'changed input')
        need(len(data) == before.st_size, 'short/long read')
        return data
    finally:
        os.close(fd)


def walk(root):
    files, dirs = set(), set()
    def descend(path, prefix=''):
        for entry in os.scandir(path):
            name = prefix + entry.name
            safe(name)
            need(not entry.is_symlink(), 'symlink input')
            if entry.is_dir(follow_symlinks=False):
                dirs.add(name)
                descend(entry.path, name + '/')
            else:
                need(entry.is_file(follow_symlinks=False), 'special input')
                files.add(name)
    need(root.is_absolute() and not root.is_symlink() and root.is_dir(), 'unsafe root')
    descend(root)
    return files, dirs


def authenticate(root, manifest, seal, expected_pin, actual_files, envelope):
    raw = read(root / manifest)
    need(re.fullmatch('[0-9a-f]{64}', expected_pin) is not None and digest(raw) == expected_pin, 'external manifest pin')
    need(read(root / seal) == (expected_pin + '  ' + manifest + '\n').encode(), 'detached seal')
    obj = load_bytes(raw)
    entries = obj['files']
    need(type(entries) is dict and set(entries) | set(envelope) == actual_files, 'closed inventory')
    for name, item in entries.items():
        safe(name)
        need(type(item) is dict and type(item['bytes']) is int and item['bytes'] >= 0
             and re.fullmatch('[0-9a-f]{64}', item['sha256']) is not None, 'manifest schema')
        data = read(root / name)
        need(len(data) == item['bytes'] and digest(data) == item['sha256'], 'payload mismatch: ' + name)
    return obj


def zip_check(raw):
    z = zipfile.ZipFile(io.BytesIO(raw))
    names = z.namelist()
    need(len(names) == len(set(names)) and len(names) <= 10000, 'ZIP duplicate/count')
    need(sum(i.file_size for i in z.infolist()) <= 200_000_000, 'ZIP size cap')
    for item in z.infolist():
        safe(item.filename)
        need(not item.is_dir() and stat.S_IFMT(item.external_attr >> 16) in (0, stat.S_IFREG)
             and not item.flag_bits & 1, 'ZIP nonregular/encrypted')
    need(z.testzip() is None, 'ZIP CRC')
    return z


def zip_manifest(z, name, prefix=''):
    m = load_bytes(z.read(name))
    need(set(prefix + k for k in m['files']) == {k for k in z.namelist() if k.startswith(prefix)} - {name}, 'ZIP closed manifest')
    for key, item in m['files'].items():
        safe(prefix + key)
        b = z.read(prefix + key)
        need(type(item['bytes']) is int and len(b) == item['bytes'] and digest(b) == item['sha256'], 'ZIP payload')
    return m


def replay(root):
    P = root / 'private'
    j = lambda name: load_bytes(read(P / name))
    capture = j('input_capture.json')['files']
    for name, info in capture.items():
        b = read(P / 'inputs' / safe(name))
        need(len(b) == info['bytes'] and digest(b) == info['sha256'] and blob(b) == info['git_blob'], 'captured input')
    commit = j('checkpoint_commit.json')
    need(commit['sha'] == '318e955171ce8a8886048806e2e29f9200327d06', 'checkpoint commit')
    tree = j('checkpoint_root_tree.json')
    sub = j('checkpoint_sweep_tree.json')
    need(tree['sha'] == commit['tree']['sha'] and not tree.get('truncated') and not sub.get('truncated'), 'checkpoint trees')
    folder = next(v for v in tree['tree'] if v['path'] == 'final_full_solution_sweep_20261020_01a15be7')
    need(folder['sha'] == sub['sha'], 'checkpoint subtree')
    remote = {v['path']: v for v in sub['tree']}
    bindings = j('checkpoint_binding.json')['files']
    need(set(bindings) == set(capture), 'checkpoint capture coverage')
    equal_count = 0
    for name, info in capture.items():
        remote_blob = remote.get(name, {}).get('sha')
        equal = remote_blob == info['git_blob']
        need(bindings[name] == {'checkpoint_blob': remote_blob, 'snapshot_blob': info['git_blob'], 'equal': equal}, 'checkpoint binding')
        if equal:
            equal_count += 1
        else:
            need(remote_blob is None and (name.startswith('eligibility/') or name.endswith('_PUBLICATION_LEADS.json') or name == 'LATEST_CHECKPOINT_RECEIPT.json'), 'checkpoint mismatch')
    need(equal_count == 46, 'checkpoint bound file count')
    state = j('inputs/STATE.json')
    need((state['next_pr'], state['last_completely_processed_pr'], state['completed_pr_count']) == (967, 966, 958), 'frozen cursor')
    journal = [load_bytes(v) for v in read(P / 'inputs/dispositions.jsonl').splitlines()]
    need([v['pr'] for v in journal] == list(range(9, 967)), 'journal numeric coverage')
    journal_by = {v['pr']: v for v in journal}
    inventory = j('inputs/rest_inventory.json')['pull_requests']
    prs = {v['number']: v for v in inventory}
    need(len(prs) == len(inventory), 'duplicate inventory PR')
    cases = j('independent_structural_results.json')['cases']
    need([v['pr'] for v in cases] == list(range(938, 967)), '29 case coverage')
    counts = {'unsolved': 0, 'already_solved': 0, 'claimed_solved': 0}
    for case in cases:
        n = case['pr']
        e = j(f'inputs/eligibility/pr{n:04d}.json')
        d = j(f'inputs/PR{n:04d}_DISPOSITION.json')
        p = prs[n]
        need(d == journal_by[n] and d['pr'] == e['pr'] == n, 'journal/disposition identity')
        for key, field in [('inventory_head_sha', 'headRefOid'), ('inventory_base_sha', 'baseRefOid')]:
            need(d[key] == e[key] == p[field], 'PR immutable identity')
        need(case['head'] == p['headRefOid'] and case['base'] == p['baseRefOid'] and case['comparison'] == p['baseRefOid'] + '...' + p['headRefOid'], 'actual comparison')
        need(d['pr_state'] == p['state'] and d['inventory_updated_at'] == p['updatedAt'] and d['inventory_body_sha256'] == digest((p.get('body') or '').encode()), 'inventory bytes')
        changed = {v['path']: v for v in case['changed_paths']}
        cached = {v['filename']: v for v in e['files']}
        need(len(changed) == len(case['changed_paths']) == len(cached) == len(e['files']) == e['file_count'] and set(changed) == set(cached) == set(e['changed_paths']), 'complete path coverage')
        for path, item in changed.items():
            safe(path)
            need(item['sha'] == cached[path]['sha'] and item['type'] == 'blob' and item['mode'] in ['100644', '100755'], 'actual head blob')
        parsed = []
        for q in case['queue']:
            raw = read(P / f'pr{n:04d}/queue.head')
            patch = read(P / f'pr{n:04d}/queue.patch')
            need(blob(raw) == q['head_blob'] == changed[q['path']]['sha'] and digest(raw) == q['sha256'] and digest(patch) == q['patch_sha256'], 'QUEUE actual blob/patch')
            need([v['sha'] for v in e['queue_changes'] if v['path'] == q['path']] == [q['head_blob']], 'cached QUEUE identity')
            for line in patch.decode().splitlines():
                if not line.startswith('+') or line.startswith('+++'):
                    continue
                line = line[1:]
                cols = [v.strip() for v in re.split(r'(?<!\\)\|', line.strip().strip('|'))]
                if len(cols) >= 9 and cols[0].isdigit():
                    parsed.append({'queue_path': q['path'], 'source_line': line, 'problem_id': cols[1].split('/')[0].strip(), 'status': cols[7]})
        key = lambda v: (v['queue_path'], v['source_line'], v['problem_id'], v['status'])
        need(sorted(map(key, parsed)) == sorted(map(key, e['added_queue_rows'])) == sorted(map(key, case['rows'])), 'own added canonical rows')
        ids = sorted({v for path in changed for v in re.findall(r'(?:^|/)(?:attempts|problems)/(\d+)(?=/|_)', path)})
        need(ids == d['problem_ids'] == [case['problem_id']] and parsed and all(v['problem_id'] == ids[0] and v['status'] == case['status'] for v in parsed), 'row/problem correspondence')
        need(all(path in ['QUEUE.md', 'unsolved_math_prioritization/QUEUE.md'] or re.search(r'(?:^|/)(?:attempts|problems)/' + ids[0] + r'(?=/|_)', path) for path in changed), 'path/problem correspondence')
        counts[case['status']] += 1
        published = n in [938, 946, 948, 952]
        expected = 'skip_entirely_already_published' if published else 'skip_explicit_non_claimed_solved'
        need(case['disposition'] == d['disposition'] == expected and (case['status'] == 'claimed_solved') == published, 'disposition eligibility')
        need(all(d[k] is False for k in ['new_mathematical_audit', 'new_publication', 'spreadsheet_mutation']) and d['requires_final_live_head_recheck'] is True, 'bounded action scope')
        if not published:
            need(d['current_classification'] == case['status'] and d['explicit_pr_queue_statuses'] == [case['status']] and d['queue_source_lines'] == [v['source_line'] for v in parsed] and d['queue_blob_shas'] == [v['head_blob'] for v in case['queue']], 'excluded row binding')
    need(counts == {'unsolved': 18, 'already_solved': 7, 'claimed_solved': 4} and sum(len(v['changed_paths']) for v in cases) == 1075, 'bounded totals')
    ledger = j('fresh_ledger.json')
    fetch = j('ledger_fetch.json')
    params = load_bytes(fetch['argv'][-1])
    need(params == {'spreadsheetId': '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20', 'range': "'Math Puzzles'!A:AQ"} and fetch['sha256'] == digest(read(P / 'fresh_ledger.json')), 'fresh exact ledger range')
    need(ledger['values'][0] == ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes'] and len(ledger['values']) == 178, 'ledger shape')
    archives = j('independent_archive_results.json')['cases']
    scope = j('scope_inspection.json')
    need([v['pr'] for v in archives] == [938, 946, 948, 952] and set(scope['cases']) == {'938', '946', '948', '952'} and scope['findings'] == [] and scope['new_scientific_or_priority_certification'] is False, 'scope bounded findings')
    for a, row, expected_originals in zip(archives, [108, 117, 129, 132], [44, 33, 24, 33]):
        n = a['pr']
        D = P / f'pr{n:04d}'
        details = j(f'inputs/PR{n:04d}_PUBLICATION_COVERAGE_DETAILS.json')
        wrapper = j(f'inputs/PR{n:04d}_PUBLICATION_VERIFICATION.json')
        metadata = j(f'pr{n:04d}/public/metadata.json')
        receipt = j(f'pr{n:04d}/public/fetch_receipt.json')
        need(metadata['id'] == details['record'] == wrapper['record'] and metadata['doi'] == details['doi'] == wrapper['doi'], 'public record identity')
        need(receipt['doi']['http_status'] == 200 and receipt['doi']['final_url'] == 'https://zenodo.org/records/' + str(metadata['id']), 'DOI destination')
        for key in ['title', 'description', 'creators', 'publication_date']:
            need(metadata['metadata'][key] == wrapper[key], 'metadata coverage')
        need(len(metadata['files']) == len(receipt['files']) == 2, 'two public files')
        raws = {}
        for item in metadata['files']:
            name = safe(item['key'])
            b = read(D / 'public' / name)
            info = next(v for v in receipt['files'] if v['name'] == name)
            old = next(v for v in details['public_files'] if v['name'] == name)
            need(len(b) == item['size'] == info['bytes'] == old['bytes'] and item['checksum'] == 'md5:' + hashlib.md5(b).hexdigest() and digest(b) == info['sha256'] == old['sha256'], 'provider/public file bytes')
            raws[name.rsplit('.', 1)[1]] = b
        z = zip_check(raws['zip'])
        outer = zip_manifest(z, details['manifest_name'])
        need(len(z.namelist()) == details['archive_members'] == a['archive_members'] and len(outer['files']) == details['manifested_payloads'] and digest(z.read(details['manifest_name'])) == details['manifest_sha256'], 'root archive binding')
        if n == 946:
            inner = zip_manifest(z, 'package/PACKAGE_MANIFEST.json', 'package/')
            need(len(inner['files']) == 207 and digest(z.read('package/PACKAGE_MANIFEST.json')) == details['inner_manifest']['sha256'], 'inner complete manifest')
        originals = a['original_bindings']
        prefix = 'original_packet/' if n == 938 else ('package/original/' if n == 946 else 'original/')
        need(len(originals) == expected_originals and {v['member'] for v in originals} == {v for v in z.namelist() if v.startswith(prefix)}, 'whole original tree coverage')
        need({(v['path'], v['member'], v['bytes'], v['sha256']) for v in originals} == {(v['path'], v['member'], v['bytes'], v['sha256']) for v in details['original_bindings']}, 'root original binding')
        for item in originals:
            b = read(D / 'head' / safe(item['path']))
            need(z.read(item['member']) == b and len(b) == item['bytes'] and digest(b) == item['sha256'] and blob(b) == item['head_blob'], 'original scientific blob')
        need(z.read(a['pdf']['member']) == raws['pdf'], 'embedded/external PDF')
        if n == 948:
            raw = z.read(details['nested_original_archive']['path'])
            nz = zip_check(raw)
            em = load_bytes(z.read('original/unsolved_math_prioritization/attempts/30004549/ANTI_INVARIANT_30004549_R3_AUTHOR_EXTERNAL_MANIFEST.json'))
            need(len(nz.namelist()) == 7 and {v['path'] for v in em['files']} == set(nz.namelist()) and len(raw) == em['archive']['bytes'] and digest(raw) == em['archive']['sha256'], 'nested closed inventory')
            for item in em['files']:
                b = nz.read(item['path'])
                need(len(b) == item['bytes'] and digest(b) == item['sha256'], 'nested payload')
        vals = ledger['values'][row - 1]
        pid = details['problem_id']
        prurl = 'https://github.com/AlecKriebel/Math/pull/' + str(n)
        need(vals[2] == 'https://doi.org/' + details['doi'], 'ledger primary DOI')
        for pattern in [r'(?<!\d)' + pid + r'(?!\d)', re.escape(prurl) + r'(?!\d)']:
            need([i for i, v in enumerate(ledger['values'], 1) if re.search(pattern, ' '.join(map(str, v)))] == [row], 'ledger unique identity')
        need([i for i, v in enumerate(ledger['values'], 1) if len(v) > 2 and details['doi'] in v[2]] == [row], 'ledger DOI uniqueness')
        lead = j(f'inputs/PR{n:04d}_PUBLICATION_LEADS.json')
        need(len(lead['matches']) == 1 and lead['matches'][0]['values'] == vals and lead['matches'][0]['row'] == row, 'cached/fresh ledger bytes')
        qr = j(f'pr{n:04d}/question/receipt.json')
        qb = read(D / 'question/question.pdf')
        need(qr['http_status'] == 200 and qb.startswith(b'%PDF') and len(qb) == qr['bytes'] and digest(qb) == qr['sha256'], 'fresh original question source')
        for v in scope['cases'][str(n)]['read_artifacts'].values():
            if type(v) is dict:
                b = read(P / safe(v['path']))
                need(len(b) == v['bytes'] and digest(b) == v['sha256'], 'manual scope input')
    end = j('parent_state_end_observation.json')
    need(end['scope_bound_to_frozen_snapshot'] is True and end['captured_next_pr'] == 967
         and {v['path'] for v in end['changed_captured_inputs_after_capture']} <= {'STATE.json', 'dispositions.jsonl'}, 'concurrent parent boundary')
    return {'status': 'PASS_BOUNDED_29', 'cases': 29, 'changed_paths': 1075, 'nonclaimed': 25, 'existing_publications': 4,
            'scope': 'Identity, eligibility, coverage and recorded limitations only; no new proof, priority, global completion or human certificate.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).absolute().parent)
    parser.add_argument('--manifest-sha256', required=True)
    args = parser.parse_args()
    root = args.root.absolute()
    files, dirs = walk(root)
    public = {v for v in files if not v.startswith('private/')}
    envelope = {'OUTPUT_MANIFEST.json', 'OUTPUT_MANIFEST.sha256'}
    manifest = authenticate(root, 'OUTPUT_MANIFEST.json', 'OUTPUT_MANIFEST.sha256', args.manifest_sha256, public, envelope)
    private_files = {v[len('private/'):] for v in files if v.startswith('private/')}
    private = authenticate(root / 'private', 'PRIVATE_MANIFEST.json', 'PRIVATE_MANIFEST.sha256', manifest['private_binding']['sha256'], private_files, {'PRIVATE_MANIFEST.json', 'PRIVATE_MANIFEST.sha256'})
    need(len(private['files']) == manifest['private_binding']['payloads'], 'private count')
    expected_dirs = {str(PurePosixPath(v).parent) for v in files}
    expected_dirs |= {str(p) for v in files for p in PurePosixPath(v).parents}
    expected_dirs.discard('.')
    need(dirs == expected_dirs, 'closed directory namespace')
    print(json.dumps(replay(root), sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('REJECT: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
