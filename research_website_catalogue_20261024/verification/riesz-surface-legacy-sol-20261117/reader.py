"""One bounded legacy-data route; read-only Git objects, no project imports/execution."""
import base64
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import time
import traceback
import zipfile

M = Path('/Users/alec/Documents/Math')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
P = M / 'research_website_catalogue_20261024'
OWN = P / 'verification/riesz-surface-legacy-sol-20261117'
SRC = P / 'papers/23202994/sources'
REVIEWS = P / 'papers/23202994/reviews'
K3 = P / 'papers/23204176/reviews/scope-sol-continuation-20261117'
COMMIT = '386463ab847f283920e746a48f52079ac8b3d735'
MHEAD = 'a4ce3c37dad209339e490d18dcced6c48cf912d2'
WHEAD = '7d5ac8ea5dc8d6cddee457da7a5b40042d36d344'
TREES = {'native_main': '6ccfd5ab446400dc7fb3933dcc2e374cb415fa90',
         'designated_release': 'e63ba1f227e5aa2f0e06fd6a52b36afa1531a4d0'}
QUERY = re.compile(r'23202994|hypersingular|riesz|triangular[\s_–—-]*lattice|universal[\s_–—-]*optimality', re.I)
GIT_CALLS = []
START = datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def oid(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def put(name, value):
    path = OWN / name
    assert not path.exists(), 'fresh output ' + name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def git(repo, args, input_bytes=None):
    allowed = {'rev-parse', 'for-each-ref', 'ls-tree', 'cat-file'}
    assert args and args[0] in allowed
    argv = ['git', '--no-optional-locks', '-C', str(repo)] + args
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tick = time.monotonic()
    run = subprocess.run(argv, input=input_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    n = len(GIT_CALLS)
    out = f'git-streams/{n:03d}.stdout.bin'
    err = f'git-streams/{n:03d}.stderr.bin'
    (OWN / 'git-streams').mkdir(exist_ok=True)
    (OWN / out).write_bytes(run.stdout)
    (OWN / err).write_bytes(run.stderr)
    GIT_CALLS.append({'argv': argv, 'started_UTC': started, 'elapsed_seconds': time.monotonic()-tick,
                      'exit_code': run.returncode, 'stdin_sha256': sha(input_bytes) if input_bytes is not None else None,
                      'stdout': out, 'stdout_bytes': len(run.stdout), 'stdout_sha256': sha(run.stdout),
                      'stderr': err, 'stderr_bytes': len(run.stderr), 'stderr_sha256': sha(run.stderr)})
    assert run.returncode == 0 and not run.stderr, 'read-only Git failure ' + repr(argv)
    return run.stdout


def inventory(root):
    rows = []
    def visit(path):
        info = path.lstat()
        rel = path.relative_to(root).as_posix()
        row = {'path': rel, 'mode_octal': oct(stat.S_IMODE(info.st_mode)),
               'hidden_component': any(s.startswith('.') and s != '.' for s in Path(rel).parts)}
        if stat.S_ISDIR(info.st_mode):
            children = sorted(path.iterdir(), key=lambda p: os.fsencode(p.name))
            row.update(kind='directory', empty=not children)
            rows.append(row)
            for child in children:
                visit(child)
        elif stat.S_ISREG(info.st_mode):
            data = path.read_bytes()
            row.update(kind='file', bytes=len(data), sha256=sha(data), git_blob_oid=oid(data))
            rows.append(row)
        elif stat.S_ISLNK(info.st_mode):
            row.update(kind='symlink', target=os.readlink(path))
            rows.append(row)
        else:
            raise AssertionError('unsupported actual object ' + str(path))
    visit(root)
    return rows


def counts(rows):
    return {'files': sum(r['kind'] == 'file' for r in rows),
            'childdirs': sum(r['kind'] == 'directory' for r in rows)-1,
            'symlinks': sum(r['kind'] == 'symlink' for r in rows),
            'hidden_objects': sum(r['hidden_component'] for r in rows),
            'empty_dirs': sum(r.get('empty', False) for r in rows)}


def native_state(repo, expected):
    gd = repo / '.git'
    files = {}
    for name in ['HEAD', 'index', 'config']:
        path = gd / name
        info = path.lstat()
        assert stat.S_ISREG(info.st_mode)
        data = path.read_bytes()
        files[name] = {'bytes': len(data), 'sha256': sha(data), 'mode_octal': oct(stat.S_IMODE(info.st_mode))}
    head = git(repo, ['rev-parse', 'HEAD']).decode().strip()
    assert head == expected, 'protected HEAD pin'
    refs = git(repo, ['for-each-ref', '--format=%(refname) %(objectname) %(symref)', 'refs/heads']).decode()
    return {'gitdir_files': files, 'resolved_HEAD': head, 'local_heads': refs,
            'loose_local_heads_topology': inventory(gd / 'refs/heads'),
            'excluded_nonlocal_state': ['FETCH_HEAD', 'remote-tracking refs', 'nonlocal refs', 'object-database additions']}


def guards():
    roots = {str(x): inventory(x) for x in [SRC, REVIEWS, K3, W / 'public', M / 'docs']}
    assert counts(roots[str(SRC)])['files'] == 39 and counts(roots[str(SRC)])['childdirs'] == 15
    assert counts(roots[str(K3)])['files'] == 1016 and counts(roots[str(K3)])['childdirs'] == 38
    assert counts(roots[str(W / 'public')])['files'] == 781 and counts(roots[str(W / 'public')])['childdirs'] == 377
    native = {'M': native_state(M, MHEAD), 'W': native_state(W, WHEAD)}
    clearance = P / 'verification/root-clearance-23202994-20261117.json'
    return {'roots': roots, 'root_counts': {k: counts(v) for k, v in roots.items()}, 'native': native,
            'clearance': {'bytes': len(clearance.read_bytes()), 'sha256': sha(clearance.read_bytes())},
            'AGENTS_sha256': sha((M / 'AGENTS.md').read_bytes())}


def authenticate_source(rows):
    manifest = json.loads((SRC / 'SOURCE_MANIFEST.json').read_bytes())
    final = json.loads((SRC / 'SOURCE_FINAL.json').read_bytes())
    assert manifest['schema'] == 'source-custody-manifest-v1'
    assert sha((SRC / 'SOURCE_MANIFEST.json').read_bytes()) == final['manifest']['sha256']
    assert final['manifest']['sha256'] == '7a6854f7ebb1caf7a0f26c5cb6014872ee0ce93f03414c3f48d965ff13c9a976'
    actual = {r['path']: r for r in rows}
    terminals = manifest['terminal_control_topology']
    assert set(actual) == {r['path'] for r in manifest['entries']} | {r['path'] for r in terminals}
    for r in manifest['entries'] + terminals:
        for key in ['kind', 'mode_octal', 'hidden_component', 'empty', 'bytes', 'sha256']:
            if key in r:
                assert actual[r['path']][key] == r[key], 'source manifest field ' + r['path']
    assert sha((K3 / 'FINAL_SEAL.json').read_bytes()) == '6a17374661feb3d770de266bb05a40be686c436431f62576bbd215fbfe36c134'


def zip_metadata(label, data):
    result = {'label': label, 'outer_bytes': len(data), 'outer_sha256': sha(data), 'outer_git_blob_oid': oid(data), 'members': []}
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        infos = z.infolist()
        assert len(infos) <= 2048 and sum(i.file_size for i in infos) <= 128*1024*1024, 'bounded archive'
        assert len({i.filename for i in infos}) == len(infos), 'duplicate ZIP names'
        for info in infos:
            assert not info.filename.startswith('/') and '..' not in Path(info.filename).parts
            content = z.read(info)
            item = {'name': info.filename, 'is_directory': info.is_dir(), 'uncompressed_bytes': info.file_size,
                    'compressed_bytes': info.compress_size, 'CRC32': f'{info.CRC:08x}',
                    'compression_method': info.compress_type, 'external_attr': info.external_attr,
                    'date_time': list(info.date_time), 'sha256': sha(content), 'git_blob_oid': oid(content)}
            result['members'].append(item)
            leaf = Path(info.filename).name.lower()
            if not info.is_dir() and (leaf in ('readme.md', 'zenodo-metadata.json', 'citation.cff') or leaf.endswith('.tex')):
                txt = content.decode('utf-8', errors='strict')
                if leaf.endswith('.tex'):
                    txt = '\n'.join(txt.splitlines()[:90]) + '\n'
                name = 'archive-association/' + label + '/' + info.filename.replace('/', '__') + '.txt'
                target = OWN / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(txt)
                item['association_excerpt'] = name
                item['excerpt_scope'] = 'first90TeXlines' if leaf.endswith('.tex') else 'whole_document'
    return result


def main():
    before = guards()
    authenticate_source(before['roots'][str(SRC)])
    put('GUARDS_BEFORE.json', {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'guard': before})
    trees = {}
    all_oids = set()
    for label, tree in TREES.items():
        raw = git(M, ['ls-tree', '-rz', '-r', '--full-tree', tree])
        rows = []
        for record in raw.split(b'\0'):
            if not record:
                continue
            meta, path = record.split(b'\t', 1)
            mode, kind, obj = meta.decode().split()
            assert kind == 'blob', 'docs leaf must be blob'
            name = path.decode('utf-8', errors='strict')
            rows.append({'path': name, 'mode': mode, 'kind': kind, 'oid': obj})
            all_oids.add(obj)
        trees[label] = rows
    clearance_path = 'research_website_catalogue_20261024/verification/root-clearance-23202994-20261117.json'
    clearance_blob = git(M, ['cat-file', 'blob', COMMIT + ':' + clearance_path])
    assert clearance_blob == (P / 'verification/root-clearance-23202994-20261117.json').read_bytes()
    assert git(M, ['rev-parse', MHEAD + ':docs']).decode().strip() == TREES['native_main']
    assert git(M, ['rev-parse', COMMIT + ':docs']).decode().strip() == TREES['designated_release']
    ordered_oids = sorted(all_oids)
    batch = git(M, ['cat-file', '--batch'], ('\n'.join(ordered_oids)+'\n').encode())
    blobs = {}
    pos = 0
    for expected in ordered_oids:
        end = batch.index(b'\n', pos)
        got, kind, size = batch[pos:end].decode().split()
        assert got == expected and kind == 'blob'
        size = int(size)
        data = batch[end+1:end+1+size]
        assert batch[end+1+size:end+2+size] == b'\n' and oid(data) == expected
        blobs[expected] = data
        pos = end+2+size
    assert pos == len(batch)
    put('DOCS_GIT_MAPS.json', {'scope': TREES, 'maps': trees})
    physical = before['roots'][str(M / 'docs')]
    put('DOCS_PHYSICAL_MAP.json', {'root': str(M / 'docs'), 'entries': physical, 'counts': counts(physical)})
    native_assets = []
    zip_inputs = {}
    for path in sorted((SRC / 'zenodo-files').iterdir()):
        data = path.read_bytes()
        native_assets.append({'path': str(path), 'bytes': len(data), 'sha256': sha(data), 'git_blob_oid': oid(data)})
        if path.suffix == '.zip':
            zip_inputs['native_record'] = data
    assert len(native_assets) == 2
    pdf = next(r for r in native_assets if r['path'].endswith('/paper.pdf'))
    assert pdf['bytes'] == 87127 and pdf['sha256'] == 'b9e7c887787b911b55f012cc640621fedc282dd71e8c57fa01c1f9db49612d9d'
    candidates = []
    exact_assets = []
    parents = set()
    for row in physical:
        if row['kind'] != 'file':
            continue
        rel = row['path']
        data = (M / 'docs' / rel).read_bytes()
        for asset in native_assets:
            if row['sha256'] == asset['sha256']:
                exact_assets.append({'scope': 'physical', 'path': rel, 'native_asset': asset['path']})
        try:
            txt = data.decode('utf-8', errors='strict')
        except UnicodeDecodeError:
            continue
        hits = sorted(set(m.group(0).lower() for m in QUERY.finditer(txt + '\n' + rel)))
        if hits:
            candidates.append({'scope': 'physical', 'path': rel, 'bytes': len(data), 'sha256': sha(data), 'oid': oid(data), 'hits': hits})
            parents.add(str(Path(rel).parent))
    for scope, rows in trees.items():
        for row in rows:
            data = blobs[row['oid']]
            row['bytes'] = len(data)
            row['sha256'] = sha(data)
            for asset in native_assets:
                if sha(data) == asset['sha256']:
                    exact_assets.append({'scope': scope, 'path': row['path'], 'native_asset': asset['path']})
            try:
                txt = data.decode('utf-8', errors='strict')
            except UnicodeDecodeError:
                continue
            hits = sorted(set(m.group(0).lower() for m in QUERY.finditer(txt + '\n' + row['path'])))
            if hits:
                candidates.append({'scope': scope, **row, 'hits': hits})
                parents.add(str(Path(row['path']).parent))
    associated = []
    for parent in sorted(parents):
        for scope in ['physical'] + list(trees):
            available = physical if scope == 'physical' else trees[scope]
            for row in available:
                path = row['path']
                if str(Path(path).parent) != parent or row['kind'] != 'file' and scope == 'physical':
                    continue
                data = (M / 'docs' / path).read_bytes() if scope == 'physical' else blobs[row['oid']]
                name = 'candidate-data/' + scope + '/' + path
                target = OWN / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                associated.append({'scope': scope, 'path': path, 'saved': name, 'bytes': len(data), 'sha256': sha(data), 'oid': oid(data)})
                if path.endswith('/source-and-verification.zip'):
                    zip_inputs[scope + '_' + parent.replace('/', '_')] = data
    zips = [zip_metadata(label, data) for label, data in zip_inputs.items()]
    put('NATIVE_ASSETS.json', {'items': native_assets, 'native_version': '1.0.0', 'declared_date': '2026-10-06'})
    put('ZIP_CORRESPONDENCE.json', {'bounded_metadata': zips, 'no_member_executed': True})
    put('SEARCH_EVIDENCE.json', {'query': QUERY.pattern, 'corpora': ['current physical Math/docs'] + list(TREES),
         'candidate_hits': candidates, 'candidate_parents': sorted(parents), 'associated_files': associated,
         'exact_native_outer_asset_matches': exact_assets,
         'limits': 'Three explicit corpora only; no global history, live website or remote absence claim.'})
    put('DOCS_GIT_MAPS_COMPLETE.json', {'scope': TREES, 'maps': trees})
    put('AWAITING_PERSONAL_READ.json', {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'candidate_hits': len(candidates), 'associated_files': len(associated), 'candidate_parents': sorted(parents)})
    print('READY_FOR_PERSONAL_READ', flush=True)
    assert input().strip() == 'SEAL_AFTER_PERSONAL_READ', 'explicit own data-stage marker'
    assert (OWN / 'REPORT.md').is_file() and (OWN / 'DECISION.json').is_file()
    decision = json.loads((OWN / 'DECISION.json').read_bytes())
    assert decision['actual_canonical'] is None and decision['redirect_source'] is None
    after = guards()
    assert before == after, 'protected before/after state changed'
    put('GUARDS_AFTER.json', {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            'guard': after, 'whole_before_after_exact': True})
    put('GIT_READS.json', {'calls': GIT_CALLS, 'all_read_only': True})
    put('READER_EXIT.json', {'exit_code': 0, 'started_UTC': START,
                           'finished_UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                           'one_invocation': True, 'no_retry': True})
    print('ALL_GUARDS_EXACT; FINALIZING_FINITE_PACKET', flush=True)
    sys.stdout.flush()
    terminals = {'FINAL_MANIFEST.json', 'FINAL.json'}
    for name in sorted(terminals):
        with (OWN / name).open('xb'):
            pass
    entries = inventory(OWN)
    for row in entries:
        if row['path'] in terminals:
            row.pop('bytes')
            row.pop('sha256')
            row.pop('git_blob_oid')
            row['terminal_control'] = True
    manifest = {'schema': 'bounded-legacy-manifest-v1', 'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'root': str(OWN), 'entries': entries, 'counts': counts(entries),
                'exact_recursive_hash_exclusions': sorted(terminals), 'no_hidden_empty_mode_exclusions': True}
    (OWN / 'FINAL_MANIFEST.json').write_text(json.dumps(manifest, indent=2, sort_keys=True)+'\n')
    final = {'schema': 'bounded-legacy-final-v1', 'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'record': '23202994', 'row': 190, 'scope': 'three explicit legacy docs corpora',
             'manifest_sha256': sha((OWN / 'FINAL_MANIFEST.json').read_bytes()),
             'report_sha256': sha((OWN / 'REPORT.md').read_bytes()), 'counts': counts(entries),
             'terminal_pair': sorted(terminals), 'protected_state_exact': True,
             'reader_invocations': 1, 'reader_exit': 0, 'completion_percent': 100,
             'scientific_clearance_inherited_only': True, 'actual_canonical': None, 'redirect_source': None,
             'follow_up': None, 'private_only': True, 'quiescent': True}
    (OWN / 'FINAL.json').write_text(json.dumps(final, indent=2, sort_keys=True)+'\n')
    actual = inventory(OWN)
    expected = {r['path']: r for r in entries}
    assert {r['path'] for r in actual} == set(expected)
    for row in actual:
        old = expected[row['path']]
        if row['path'] in terminals:
            assert row['kind'] == old['kind'] and row['mode_octal'] == old['mode_octal']
        else:
            assert row == old, 'finite own namespace changed ' + row['path']


try:
    main()
except BaseException:
    (OWN / 'FAILURE.txt').write_text(traceback.format_exc())
    traceback.print_exc()
    raise
