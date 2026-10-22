"""Authenticate this file externally before execution. Read-only, standard library."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REFUSED: Python -I -S -B required')
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import tempfile
import zipfile

PINS = {'leaf_space_10300029_frozen_v1.zip': [10214, '0a6048d92a27bfa34391e530f3bbbcf34b30688831b2df2e2017173ce936c5a1'], 'FREEZE_RECEIPT.json': [991, '6f912e9cc0ddb90d6b6d5aaf6ca793a713e38b779da19a0522f551be1bb7c2b3'], 'LEAF_SPACE_10300029_INDEPENDENT_AUDIT_SAFE.zip': [20901, 'cb38a62c2b72c13c59851b04f3efe8a23dd4a34cd498c6103e1f9dfde3f3a82f'], 'LEAF_SPACE_10300029_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': [1313, 'bb4faab75adbd492b06cf24d0181f553e3d6dec3a1649ca867172c9c999657f0'], 'LEAF_SPACE_10300029_INDEPENDENT_AUDIT_RECEIPT.json': [3049, 'fd8a5128466cef0ef14f19abcb850fe1e428d774c63e0ab5c57745b543515c60']}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def unique(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, 'duplicate JSON key')
        out[key] = value
    return out


def nonfinite(value):
    raise ValueError('nonfinite JSON value')


def parse(b):
    return json.loads(b, object_pairs_hook=unique, parse_constant=nonfinite)


def safe_path(p):
    p = Path(p)
    need(p.is_absolute() and str(p.resolve()) == str(p), 'canonical absolute path required')
    for part in [p] + list(p.parents):
        need(not part.is_symlink(), 'symlink or symlink ancestor')
    return p


def regular(p):
    p = safe_path(p)
    need(stat.S_ISREG(p.lstat().st_mode), 'regular file required')
    need(p.stat().st_size < 2000000, 'file size ceiling')
    return p.read_bytes()


def verify(root, manifest_pin):
    root = safe_path(root)
    need(safe_path(__file__) == root / 'publication_bootstrap.py', 'wrong operative entrypoint')
    need(stat.S_ISDIR(root.lstat().st_mode), 'directory required')
    mb = regular(root / 'PUBLICATION_MANIFEST.json')
    need(re.fullmatch('[0-9a-f]{64}', manifest_pin) is not None and sha(mb) == manifest_pin,
         'external manifest pin mismatch')
    manifest = parse(mb)
    need(type(manifest) is dict and set(manifest) == {'schema', 'problem_id', 'files'}, 'manifest schema')
    need(type(manifest['schema']) is int and manifest['schema'] == 1, 'manifest version')
    need(type(manifest['problem_id']) is int and manifest['problem_id'] == 10300029, 'problem identity')
    entries = manifest['files']
    need(type(entries) is dict and entries, 'manifest entries')
    expected_dirs = set()
    for name, item in entries.items():
        need(type(name) is str, 'path type')
        p = PurePosixPath(name)
        need(str(p) == name and not p.is_absolute() and '..' not in p.parts and '\\' not in name,
             'unsafe manifest path')
        need(type(item) is dict and set(item) == {'bytes', 'sha256'}, 'entry schema')
        need(type(item['bytes']) is int and 0 <= item['bytes'] < 2000000, 'entry size')
        need(type(item['sha256']) is str and re.fullmatch('[0-9a-f]{64}', item['sha256']) is not None,
             'entry digest')
        expected_dirs.update(str(p) for p in p.parents if str(p) != '.')
    files, dirs = set(), set()
    for base, ds, fs in os.walk(root, followlinks=False):
        for name in ds:
            p = Path(base) / name
            need(not p.is_symlink() and stat.S_ISDIR(p.lstat().st_mode), 'nonregular directory')
            dirs.add(str(p.relative_to(root)))
        for name in fs:
            p = Path(base) / name
            need(not p.is_symlink() and stat.S_ISREG(p.lstat().st_mode), 'nonregular inventory entry')
            files.add(str(p.relative_to(root)))
    need(files == set(entries) | {'PUBLICATION_MANIFEST.json'} and dirs == expected_dirs,
         'strict package inventory')
    payload = {}
    for name, item in entries.items():
        b = regular(root / name)
        need(item == {'bytes': len(b), 'sha256': sha(b)}, 'package bytes mismatch: ' + name)
        payload[name] = b
        if name.endswith('.json'):
            parse(b)
    for name, pin in PINS.items():
        b = payload[name]
        need((len(b), sha(b)) == tuple(pin), 'immutable input pin: ' + name)
    author_receipt = parse(payload['FREEZE_RECEIPT.json'])
    audit_external = parse(payload['LEAF_SPACE_10300029_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'])
    audit_receipt = parse(payload['LEAF_SPACE_10300029_INDEPENDENT_AUDIT_RECEIPT.json'])
    need(audit_receipt['members'] == audit_external['members'], 'audit receipt manifest binding')
    for record in ('archive', 'author_archive', 'author_receipt', 'external_manifest'):
        item = audit_receipt[record]
        need((item['bytes'], item['sha256']) == tuple(PINS[item['filename']]), 'external receipt binding')
    need((author_receipt['bytes'], author_receipt['sha256']) == tuple(PINS['leaf_space_10300029_frozen_v1.zip']),
         'author receipt binding')
    member_count = 0
    for folder, zname, rows in [
        ('author', 'leaf_space_10300029_frozen_v1.zip', author_receipt['members']),
        ('audit', 'LEAF_SPACE_10300029_INDEPENDENT_AUDIT_SAFE.zip', audit_external['members'])]:
        records = {row['path']: row for row in rows}
        need(len(records) == len(rows), 'duplicate manifest member')
        with zipfile.ZipFile(io.BytesIO(payload[zname])) as z:
            infos = z.infolist()
            need(not z.comment and len(infos) == len(records) and set(z.namelist()) == set(records), 'archive inventory')
            for i in infos:
                need(i.filename == i.orig_filename and '/' not in i.filename and '\\' not in i.filename
                     and i.filename not in ('.', '..'), 'archive path')
                need(i.create_system == 3 and i.external_attr >> 16 == stat.S_IFREG | 0o444
                     and i.flag_bits == 0 and i.compress_type == zipfile.ZIP_DEFLATED
                     and not i.extra and not i.comment, 'archive metadata')
                b = z.read(i)
                need(records[i.filename] == {'path': i.filename, 'bytes': len(b), 'sha256': sha(b)}
                     and i.file_size == len(b), 'archive member identity')
                need(payload[folder + '/' + i.filename] == b, 'loose member binding')
                b.decode('utf-8')
                member_count += 1
        internal = parse(payload[folder + '/MANIFEST.json'])
        need(internal['payload_members'] == [row for row in rows if row['path'] != 'MANIFEST.json'],
             'internal manifest binding')
    status = parse(payload['author/STATUS.json'])
    acceptance = parse(payload['audit/ACCEPTANCE.json'])
    need(status['overall_disposition'] == acceptance['overall_disposition'] == 'unsolved', 'status gate')
    need(status['substantive_approaches_used'] == acceptance['substantive_author_approaches'] == 3,
         'three approaches only')
    need(acceptance['verdict'] == 'accept_exact_frozen_version_as_scoped_partial'
         and acceptance['correction_patch_required'] is False and acceptance['novelty_claim'] is False
         and acceptance['proof_assistant_verification'] is False, 'acceptance scope')
    need(status['mathematical_executable_included'] is False, 'data-only author')
    source = parse(payload['audit/SOURCE_INSPECTION.json'])['canonical_match']
    need(source['rank'] == 845 and source['unique_catalog_match'] is True
         and source['unique_problem_match'] is True and source['complete_pair_match_to_author_selected_record'] is True,
         'canonical source binding')
    return root, payload, {'verdict': 'PASS', 'problem_id': 10300029, 'files': len(files),
                          'archive_members': member_count, 'status': 'unsolved', 'turns': '3/5',
                          'scope': 'Integrity and scoped disposition; no mathematical execution'}


def execute(path, raw, args, flags, cwd):
    code = 'import sys;sys.argv=sys.argv[1:];__file__=sys.argv[0];exec(compile('+repr(raw)+',__file__,"exec"))'
    p = subprocess.run([sys.executable, '-I', '-S', '-B', *flags, '-c', code, str(path),
                        *map(str, args)], cwd=cwd, capture_output=True, timeout=180)
    need(p.returncode == 0 and not p.stderr, 'authenticated execution failed: ' + p.stderr.decode())
    return parse(p.stdout)


def replay(root, payload, corpus=None):
    results = []
    with tempfile.TemporaryDirectory(prefix='finite-radius-publication-') as td:
        clean = Path(td) / 'relocated'; clean.mkdir()
        for name, raw in payload.items():
            p = clean / name; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(raw)
        for optimized in (False, True):
            flags = ['-O'] if optimized else []
            if corpus:
                name = 'verify_corpus_bindings.py'
                got = execute(clean/name, payload[name], corpus, flags, td)
                need(got['statement_match'] is True and got['review_match'] is True and got['catalog_rank'] == 845,
                     'source replay')
                results.append({'kind': 'complete_source_bindings', 'optimized': optimized, 'result': got})
                continue
            name = 'audit/VERIFY_AUTHOR.py'
            got = execute(clean/name, payload[name], [clean/'leaf_space_10300029_frozen_v1.zip',
                          clean/'FREEZE_RECEIPT.json'], flags, td)
            need(got['verdict'] == 'PASS' and got['receipt_verified'] is True, 'author verification')
            results.append({'kind': 'author_integrity', 'optimized': optimized, 'result': got})
            name = 'audit/TEST_VERIFY_AUTHOR.py'
            got = execute(clean/name, payload[name], [clean/'audit/VERIFY_AUTHOR.py',
                          clean/'leaf_space_10300029_frozen_v1.zip', clean/'FREEZE_RECEIPT.json'], flags, td)
            need(got['verdict'] == 'PASS' and got['positive_cli_runs'] == 4 and got['negative_cli_runs'] == 46
                 and got['structural_and_json_negative_runs'] == 22 and got['harness_optimized'] == optimized,
                 'regression counts')
            results.append({'kind': 'audit_regressions', 'optimized': optimized, 'result': got})
    need(verify(root, sha(regular(root/'PUBLICATION_MANIFEST.json')))[1] == payload, 'post-replay change')
    return results


def main():
    need(len(sys.argv) == 3 or (len(sys.argv) == 4 and sys.argv[3] == '--replay')
         or (len(sys.argv) == 7 and sys.argv[3] == '--corpus'),
         'usage: publication_bootstrap.py ROOT MANIFEST_SHA256 [--replay | --corpus CATALOG PROBLEMS REPORTS]')
    root, payload, result = verify(sys.argv[1], sys.argv[2])
    if len(sys.argv) > 3:
        result['replays'] = replay(root, payload, sys.argv[4:] if sys.argv[3] == '--corpus' else None)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps({'verdict': 'FAIL', 'error': str(error)}, sort_keys=True))
        sys.exit(1)
