"""Independent read-only whole-boundary inventory; never imports target code."""
from pathlib import Path, PurePosixPath
import json, hashlib, ast, collections, datetime, stat

ROOT = Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr39_9500008')
OUT = ROOT / 'whole_current_source_first_family'

def pairs(rows):
    d = {}
    for k, v in rows:
        if k in d:
            raise ValueError('duplicate JSON key: ' + k)
        d[k] = v
    return d

def strict(blob):
    return json.loads(blob, object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON: ' + x)))

def validate_member(anchor, row):
    relative = row['path']
    pure = PurePosixPath(relative)
    assert not pure.is_absolute() and '..' not in pure.parts and str(pure) == relative
    p = anchor / relative
    for q in [p, *p.parents]:
        if q == anchor.parent:
            break
        assert not q.is_symlink(), 'symlink: ' + str(q)
    assert p.is_file(), 'missing: ' + str(p)
    b = p.read_bytes()
    assert len(b) == row.get('bytes', row.get('size'))
    assert hashlib.sha256(b).hexdigest() == row['sha256'], 'hash: ' + str(p)
    if 'mode' in row:
        assert format(stat.S_IMODE(p.stat().st_mode), '04o') == row['mode']
    return b

MANIFESTS = [
 ('reviewed_candidate/MANIFEST.json', 'reviewed_candidate', True),
 ('reviewed_candidate/CURRENT_PROOF_DEPENDENCIES.json', '.', False),
 ('current_execution_revision/REVISION_MANIFEST.json', 'current_execution_revision', True),
 ('root_typed_entry_preparation_family/PREPARATION_MANIFEST.json', 'root_typed_entry_preparation_family', True),
 ('root_typed_entry_execution_revision/PREPARATION_MANIFEST.json', 'root_typed_entry_execution_revision', True),
 ('root_typed_entry_actual_capture/TYPED_ENTRY_MANIFEST.json', 'root_typed_entry_actual_capture', True),
 ('root_typed_entry_actual_capture_v2/TYPED_ENTRY_MANIFEST.json', 'root_typed_entry_actual_capture_v2', True),
]

def main():
    data = {'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'manifest_checks': [], 'strict_json_failures': [], 'unique_python_sources': [],
            'all_read_members': [], 'utf8_decode_failures': []}
    blobs = {}
    for name, anchor_name, complete in MANIFESTS:
        path = ROOT / name
        b = path.read_bytes(); m = strict(b); anchor = ROOT / anchor_name
        rows = m['files']
        paths = [r['path'] for r in rows]
        assert len(paths) == len(set(paths))
        for r in rows:
            raw = validate_member(anchor, r)
            full = str((anchor / r['path']).relative_to(ROOT))
            blobs[full] = raw
        if complete:
            actual = set()
            for q in anchor.rglob('*'):
                assert not q.is_symlink(), 'inventory symlink: ' + str(q)
                if q.is_file(): actual.add(q.relative_to(anchor).as_posix())
            assert actual == set(paths) | {path.relative_to(anchor).as_posix()}, 'closure: ' + name
        data['manifest_checks'].append({'path': name, 'sha256': hashlib.sha256(b).hexdigest(),
                                       'members': len(rows), 'complete_inventory': complete, 'passed': True})
        blobs[name] = b
    for name in ['root_current_typed_outer_capture', 'root_current_typed_outer_capture_v2']:
        p = ROOT / name
        for q in p.rglob('*'):
            assert not q.is_symlink()
            if q.is_file(): blobs[str(q.relative_to(ROOT))] = q.read_bytes()
    code = collections.defaultdict(list)
    for name, raw in sorted(blobs.items()):
        sha = hashlib.sha256(raw).hexdigest()
        data['all_read_members'].append({'path': name, 'bytes': len(raw), 'sha256': sha})
        try: text = raw.decode('utf8')
        except UnicodeDecodeError as e:
            data['utf8_decode_failures'].append({'path': name, 'error': str(e)}); continue
        if name.endswith('.py'):
            ast.parse(text, filename=name)
            code[sha].append(name)
        if name.endswith('.json') or name.endswith('.json.run1'):
            try: strict(text)
            except Exception as e:
                data['strict_json_failures'].append({'path': name, 'bytes': len(raw), 'sha256': sha,
                                                    'error': str(e), 'raw_utf8': text})
    for sha, names in code.items():
        text = blobs[names[0]].decode('utf8')
        data['unique_python_sources'].append({'sha256': sha, 'paths': names, 'bytes': len(blobs[names[0]]),
                                             'lines': len(text.splitlines())})
    data['read_member_count'] = len(blobs)
    data['unique_content_count'] = len({hashlib.sha256(b).hexdigest() for b in blobs.values()})
    (OUT / 'WHOLE_BOUNDARY_INVENTORY.json').write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps({k:v for k,v in data.items() if k not in ['all_read_members', 'unique_python_sources']}, indent=2))

if __name__ == '__main__': main()
