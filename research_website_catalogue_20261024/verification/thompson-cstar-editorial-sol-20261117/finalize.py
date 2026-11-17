"""Passive finite packet closure; no project imports, builds or publication."""
from pathlib import Path
import datetime, hashlib, json, stat

L = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/thompson-cstar-editorial-sol-20261117')
assert not any((L / name).exists() for name in ('FINAL.json', 'MANIFEST.json', 'SEAL.json'))
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda name: json.loads((L / name).read_text())
before = load('CUSTODY_BEFORE.json'); after = load('CUSTODY_AFTER.json')
assert after['before_after_exact'] and before['source_entries'] == after['source_entries']
assert before['specific_inputs'] == after['specific_inputs']

def input_row(path, relative):
    st = path.lstat()
    r = {'path': relative, 'mode_octal': oct(stat.S_IMODE(st.st_mode))}
    if stat.S_ISDIR(st.st_mode):
        r.update(kind='directory', empty=not any(path.iterdir()))
    else:
        assert stat.S_ISREG(st.st_mode), ('unexpected input kind', str(path))
        b = path.read_bytes()
        r.update(kind='file', bytes=len(b), sha256=sha(b), md5=hashlib.md5(b).hexdigest())
    return r

source = Path(before['source_root'])
current = [input_row(p, '.' if p == source else p.relative_to(source).as_posix()) for p in [source] + sorted(source.rglob('*'), key=lambda p: p.relative_to(source).as_posix())]
assert current == before['source_entries'], 'source changed at finite closure'
for old in before['specific_inputs']:
    assert input_row(Path(old['path']), old['path']) == old, ('specific input changed', old['path'])
assert before['source_files'] == 55 and before['source_child_directories'] == 14
run = load('BUILDER_RUN.json'); built = load('BUILD_RECEIPT.json'); model = load('MODEL.json')
assert run['attempt_count'] == 1 and run['repair_or_retry_count'] == 0 and run['exit'] == 0
assert sha((L / 'build_private.py').read_bytes()) == run['builder_sha256']
for stream in ('stdout', 'stderr'):
    b = (L / ('BUILDER.' + stream)).read_bytes()
    assert len(b) == run[stream + '_bytes'] and sha(b) == run[stream + '_sha256']
assert run['stderr_bytes'] == 0 and run['scientific_source_execution'] is False
assert not (L / 'CUSTODY_BEFORE.stderr').read_bytes() and not (L / 'CUSTODY_AFTER.stderr').read_bytes()
assert all(built['checks'].values()) and built['private_only'] and not built['publication_authority']
assert model['private_only'] and not model['publication_authority'] and model['robots'] == 'noindex,nofollow'
null_fields = ['actual_canonical', 'base_url', 'production_url', 'page_publication_date', 'AA', 'legacy_route', 'legacy_redirect', 'follow_up']
assert all(model[k] is None for k in null_fields)
assert model['native_version'] is None and not model['native_version_field_present']
assert model['host_edition_label'] == 'v1' and model['native_publication_date'] == '2026-10-06'
assert [r['native_filename'] for r in built['assets']] == ['thompson-cstar-verification.zip', 'thompson-cstar-source.zip', 'paper.pdf']
for r in built['assets']:
    local = L / 'private-page' / r['local_filename']
    original = source / 'zenodo-files' / r['native_filename']
    assert local.read_bytes() == original.read_bytes()
    assert sha(local.read_bytes()) == r['sha256']
assert sha((L / 'private-page/index.html').read_bytes()) == built['page_sha256']
assert sha((L / 'MODEL.json').read_bytes()) == built['model_sha256']
assert sha((L / 'private-page/citation.bib').read_bytes()) == built['bib_sha256']
assert sha((L / 'private-page/research.css').read_bytes()) == 'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a'
utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
with (L / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- ' + utc + ': final passive reauthentication exact; private writer completion100%. All original input bytes/modes/topology and specific inputs remain exact. Finite namespace sealed; publication authorityfalse. STOP.\n')
final = {
    'schema': 'private-factual-editorial-FINAL-v1', 'UTC': utc, 'record_id': '23204212',
    'status': 'FROZEN_PRIVATE_EDITORIAL_ONLY', 'completion_percent': 100, 'publication_authority': False,
    'page': 'private-page/index.html', 'model': 'MODEL.json', 'report': 'EDITORIAL_REPORT.md',
    'proposed_slug': model['proposed_slug'], 'route_assignment_or_collision_certificate': False,
    'source_files': 55, 'source_child_directories': 14, 'source_whole_bytes_modes_topology_exact': True,
    'source_final_sha256': 'b68fbb425b7d910a2508c46ff311491a1c797568dcf39d3c7deb0a0545e1afd5',
    'source_manifest_sha256': 'afa64c126da0aabc4a44ec242553e5b2354540eb1b0b60e55ab7b1a9855a09be',
    'specific_editorial_inputs_exact': True, 'builder_attempt_count': 1, 'builder_exit': 0,
    'builder_stdout_bytes': run['stdout_bytes'], 'builder_stderr_bytes': run['stderr_bytes'], 'repair_or_retry_count': 0,
    'page_sha256': built['page_sha256'], 'model_sha256': built['model_sha256'], 'bib_sha256': built['bib_sha256'],
    'three_native_assets_original_order_bytes_exact': True, 'shared_CSS_exact': True,
    'native_API_author_version': None, 'native_API_version_field_present': False, 'host_edition_label': 'v1',
    'host_label_not_author_version': True, 'declared_original_date': '2026-10-06', 'record_created': model['native_record_created'],
    'all_null_publication_fields': {key: None for key in null_fields}, 'robots': 'noindex,nofollow',
    'no_new_scientific_route': True, 'source_or_website_mutations': 0,
    'limits': built['limits'] + ['Root copy/fact/legacy/collision and any public deployment checks remain separate', 'AI/unrefereed disclosure and contribution-based passive invitation retained'],
    'frozen_namespace': str(L), 'terminal_controls': ['MANIFEST.json', 'SEAL.json'],
}
for name in ('FINAL.json', 'MANIFEST.json', 'SEAL.json'):
    (L / name).write_text('{}\n')
paths = [L] + sorted(L.rglob('*'), key=lambda p: p.relative_to(L).as_posix())
final['packet_file_count'] = sum(p.is_file() for p in paths)
final['packet_child_directory_count'] = sum(p.is_dir() for p in paths) - 1
(L / 'FINAL.json').write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n')

def namespace_rows():
    rows = []
    for p in [L] + sorted(L.rglob('*'), key=lambda p: p.relative_to(L).as_posix()):
        relative = '.' if p == L else p.relative_to(L).as_posix()
        st = p.lstat()
        r = {'path': relative, 'mode_octal': oct(stat.S_IMODE(st.st_mode)), 'hidden_component': any(t.startswith('.') for t in p.relative_to(L).parts)}
        if stat.S_ISDIR(st.st_mode):
            r.update(kind='directory', empty=not any(p.iterdir()))
        else:
            assert stat.S_ISREG(st.st_mode), ('unexpected packet kind', relative)
            b = p.read_bytes()
            r.update(kind='file', bytes=len(b))
            if relative in ('MANIFEST.json', 'SEAL.json'):
                r['digest_exclusion'] = 'exact terminal recursive hash exclusion only; actual bytes/mode/topology retained'
            else:
                r['sha256'] = sha(b)
        rows.append(r)
    return rows

for iteration in range(20):
    rows = namespace_rows()
    manifest = {'schema': 'finite-whole-private-editorial-namespace-v1', 'UTC': utc, 'root': str(L), 'file_count': final['packet_file_count'], 'child_directory_count': final['packet_child_directory_count'], 'exact_recursive_digest_exclusions': ['MANIFEST.json', 'SEAL.json'], 'entries': rows}
    (L / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
    seal = {'schema': 'finite-private-editorial-seal-v1', 'UTC': utc, 'status': final['status'], 'completion_percent': 100, 'publication_authority': False, 'manifest_sha256': sha((L / 'MANIFEST.json').read_bytes()), 'FINAL_sha256': sha((L / 'FINAL.json').read_bytes()), 'file_count': final['packet_file_count'], 'child_directory_count': final['packet_child_directory_count'], 'exact_terminal_recursive_digest_exclusions': ['MANIFEST.json', 'SEAL.json'], 'all_namespace_modes_hidden_empty_and_terminal_bytes_in_manifest': True, 'source_inputs_55_files_14_child_directories_exact': True, 'freeze_instruction': 'All actual namespace files/directories immutable after this closure; no further writer actions.'}
    (L / 'SEAL.json').write_text(json.dumps(seal, indent=2) + '\n')
    if rows == namespace_rows():
        break
else:
    raise AssertionError('terminal byte-count fixed point not reached')
assert load('MANIFEST.json')['entries'] == namespace_rows()
assert sha((L / 'MANIFEST.json').read_bytes()) == load('SEAL.json')['manifest_sha256']
assert sha((L / 'FINAL.json').read_bytes()) == load('SEAL.json')['FINAL_sha256']
print(json.dumps({'status': final['status'], 'completion_percent': 100, 'publication_authority': False, 'file_count': final['packet_file_count'], 'child_directory_count': final['packet_child_directory_count'], 'FINAL_sha256': sha((L / 'FINAL.json').read_bytes()), 'MANIFEST_sha256': sha((L / 'MANIFEST.json').read_bytes()), 'SEAL_sha256': sha((L / 'SEAL.json').read_bytes()), 'page_sha256': built['page_sha256'], 'model_sha256': built['model_sha256']}))
