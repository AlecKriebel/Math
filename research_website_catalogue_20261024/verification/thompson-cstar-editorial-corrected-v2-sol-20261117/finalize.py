"""Passive closure of the separate successful v2 copy packet; no transformer rerun."""
from pathlib import Path
import datetime, hashlib, json, stat

L = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/thompson-cstar-editorial-corrected-v2-sol-20261117')
assert not any((L / name).exists() for name in ('FINAL.json', 'MANIFEST.json', 'SEAL.json'))
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda name: json.loads((L / name).read_text())
before = load('CUSTODY_BEFORE.json'); after = load('CUSTODY_AFTER.json')
assert before['snapshots'] == after['snapshots'] and before['specific_inputs'] == after['specific_inputs']
assert after['before_after_exact'] and before['prior_literal_failure_preserved']

def row(p, relative):
    st = p.lstat()
    r = {'path': relative, 'mode_octal': oct(stat.S_IMODE(st.st_mode)), 'mtime_ns': st.st_mtime_ns, 'ctime_ns': st.st_ctime_ns, 'hidden_component': any(t.startswith('.') for t in Path(relative).parts if t != '.')}
    if stat.S_ISDIR(st.st_mode):
        r.update(kind='directory', empty=not any(p.iterdir()))
    else:
        assert stat.S_ISREG(st.st_mode), str(p)
        b = p.read_bytes(); r.update(kind='file', bytes=len(b), empty=not b, sha256=sha(b), md5=hashlib.md5(b).hexdigest())
    return r

for name, snapshot in before['snapshots'].items():
    root = Path(snapshot['root'])
    entries = [row(p, '.' if p == root else p.relative_to(root).as_posix()) for p in [root] + sorted(root.rglob('*'), key=lambda p: p.relative_to(root).as_posix())]
    assert entries == snapshot['entries'], ('protected whole tree changed at closure', name)
for old in before['specific_inputs']:
    assert row(Path(old['path']), old['path']) == old, ('specific input changed at closure', old['path'])
run = load('TRANSFORM_RUN.json'); change = load('COPY_CORRECTION.json'); model = load('MODEL.json')
assert run['attempt_count_in_this_authorized_lane'] == 1 and run['repair_or_retry_count'] == 0 and run['exit'] == 0
assert sha((L / 'copy_transformer.py').read_bytes()) == run['transformer_sha256']
for stream in ('stdout', 'stderr'):
    b = (L / ('TRANSFORM.' + stream)).read_bytes()
    assert len(b) == run[stream + '_bytes'] and sha(b) == run[stream + '_sha256']
assert run['stderr_bytes'] == 0 and not run['original_builder_execution'] and not run['scientific_source_execution']
old_root = Path(before['snapshots']['original_writer']['root'])
original = (old_root / 'private-page/index.html').read_bytes(); corrected = (L / 'private-page/index.html').read_bytes()
old_clause = change['old_clause'].encode(); new_clause = change['new_clause'].encode()
assert original.count(old_clause) == 1 and corrected.count(new_clause) == 1
assert corrected == original.replace(old_clause, new_clause, 1) and original == corrected.replace(new_clause, old_clause, 1)
assert sha(corrected) == change['new_page_sha256'] == '1885856dbf199b10703652fb9a07d55119c2c02ae2d3f081d441fd68892514e3'
assert len(corrected) == 15524
assert (L / 'MODEL.json').read_bytes() == (old_root / 'MODEL.json').read_bytes()
assert sha((L / 'MODEL.json').read_bytes()) == change['model_sha256']
assert change['model_change_allowlist'] == [] and change['model_changed_fields'] == []
for old in change['unchanged_files']:
    assert (L / 'private-page' / old['name']).read_bytes() == (old_root / 'private-page' / old['name']).read_bytes()
    assert sha((L / 'private-page' / old['name']).read_bytes()) == old['sha256']
null_fields = ['actual_canonical', 'base_url', 'production_url', 'page_publication_date', 'AA', 'legacy_route', 'legacy_redirect', 'follow_up']
assert all(model[k] is None for k in null_fields) and model['robots'] == 'noindex,nofollow'
assert model['private_only'] and not model['publication_authority']
utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
with (L / 'RESEARCH_LOG.md').open('a') as log:
    log.write('\n- ' + utc + ': all four original trees and specific inputs freshly reauthenticated exact at closure. Private correction completion100%; finite namespace frozen. No publication or independent corrected-byte fact certificate. STOP.\n')
final = {
    'schema': 'private-closed-copy-correction-FINAL-v2', 'UTC': utc, 'record_id': '23204212',
    'status': 'FROZEN_PRIVATE_CORRECTION_PREPARED', 'completion_percent': 100, 'publication_authority': False,
    'page': 'private-page/index.html', 'model': 'MODEL.json', 'report': 'CORRECTION_REPORT.md', 'change_receipt': 'COPY_CORRECTION.json',
    'page_bytes': 15524, 'page_sha256': change['new_page_sha256'], 'old_page_sha256': change['old_page_sha256'],
    'model_sha256': change['model_sha256'], 'model_bytes_exact': True, 'model_change_allowlist': [],
    'only_authorized_definition_clause_changed': True, 'whole_article_forward_reverse_exact': True,
    'abstract_SEO_native_facts_and_all_other_article_bytes_unchanged': True, 'native_three_assets_citation_CSS_exact': True,
    'protected_tree_counts': {k: {'files': v['file_count'], 'child_directories': v['child_directory_count']} for k, v in before['snapshots'].items()},
    'protected_whole_bytes_modes_timestamps_hidden_empty_topology_exact': True, 'root_review_clearance_and_all_external_pins_exact': True,
    'fact_terminal_hash_exclusions_exact': ['FINAL_MANIFEST.json', 'FINAL_SEAL.json'],
    'fact_terminal_nulls_are_markers_and_actual_full_bytes_externally_pinned': True,
    'fact_manifest_external_sha256': '056a582ec4ca0525882a8a95f1db67f267050932b50febd44d409fa8e8637afa',
    'fact_seal_external_sha256': 'eb51f8476628f017a55f0855ec80de3a34c65e3d66ac79014a881575f0a71817',
    'prior_failed_six_file_namespace_unchanged': True, 'prior_literal_failure_sha256': change['prior_failure_sha256'],
    'prior_failure_is_not_scientific_or_input_failure': True, 'prior_failure_before_page_generation': True,
    'v2_transformer_attempts': 1, 'v2_transformer_exit': 0, 'v2_transformer_stdout_bytes': run['stdout_bytes'], 'v2_transformer_stderr_bytes': run['stderr_bytes'], 'v2_repair_or_retry_count': 0,
    'original_builder_executions': 0, 'scientific_source_executions': 0, 'scientific_manuscript_PASS_unchanged': True,
    'all_publication_fields': {k: None for k in null_fields}, 'robots': 'noindex,nofollow',
    'independent_corrected_byte_fact_adoption': None, 'root_actual_copy_read_and_independent_fact_check_still_required': True,
    'limits': change['limits'], 'frozen_namespace': str(L), 'terminal_controls': ['MANIFEST.json', 'SEAL.json'],
}
for name in ('FINAL.json', 'MANIFEST.json', 'SEAL.json'):
    (L / name).write_text('{}\n')
paths = [L] + sorted(L.rglob('*'), key=lambda p: p.relative_to(L).as_posix())
final['packet_file_count'] = sum(p.is_file() for p in paths)
final['packet_child_directory_count'] = sum(p.is_dir() for p in paths) - 1
(L / 'FINAL.json').write_text(json.dumps(final, indent=2) + '\n')

def namespace():
    rows = []
    for p in [L] + sorted(L.rglob('*'), key=lambda p: p.relative_to(L).as_posix()):
        relative = '.' if p == L else p.relative_to(L).as_posix()
        st = p.lstat()
        r = {'path': relative, 'mode_octal': oct(stat.S_IMODE(st.st_mode)), 'hidden_component': any(t.startswith('.') for t in p.relative_to(L).parts)}
        if stat.S_ISDIR(st.st_mode):
            r.update(kind='directory', empty=not any(p.iterdir()))
        else:
            assert stat.S_ISREG(st.st_mode), relative
            b = p.read_bytes(); r.update(kind='file', bytes=len(b), empty=not b)
            if relative in ('MANIFEST.json', 'SEAL.json'):
                r['content_hash_exclusion'] = 'Exact terminal recursive pair only; actual bytes/modes/topology retained; external pins supplied at handoff'
            else:
                r['sha256'] = sha(b)
        rows.append(r)
    return rows

for iteration in range(20):
    rows = namespace()
    manifest = {'schema': 'finite-whole-private-correction-namespace-v2', 'UTC': utc, 'root': str(L), 'file_count': final['packet_file_count'], 'child_directory_count': final['packet_child_directory_count'], 'terminal_content_hash_exclusions_exact': ['MANIFEST.json', 'SEAL.json'], 'entries': rows}
    (L / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
    seal = {'schema': 'finite-private-correction-seal-v2', 'UTC': utc, 'status': final['status'], 'completion_percent': 100, 'publication_authority': False, 'manifest_sha256': sha((L / 'MANIFEST.json').read_bytes()), 'FINAL_sha256': sha((L / 'FINAL.json').read_bytes()), 'file_count': final['packet_file_count'], 'child_directory_count': final['packet_child_directory_count'], 'exact_recursive_digest_exclusions': ['MANIFEST.json', 'SEAL.json'], 'all_hidden_empty_files_directories_modes_and_terminal_byte_counts_in_manifest': True, 'protected_original_trees_and_inputs_exact': True, 'prior_literal_failure_preserved': True, 'stop_for_root_corrected_byte_fact_adoption': True}
    (L / 'SEAL.json').write_text(json.dumps(seal, indent=2) + '\n')
    if rows == namespace():
        break
else:
    raise AssertionError('finite terminal byte-count fixed point not reached')
assert load('MANIFEST.json')['entries'] == namespace()
assert load('SEAL.json')['manifest_sha256'] == sha((L / 'MANIFEST.json').read_bytes())
assert load('SEAL.json')['FINAL_sha256'] == sha((L / 'FINAL.json').read_bytes())
print(json.dumps({'status': final['status'], 'completion_percent': 100, 'publication_authority': False, 'file_count': final['packet_file_count'], 'child_directory_count': final['packet_child_directory_count'], 'FINAL_sha256': sha((L / 'FINAL.json').read_bytes()), 'MANIFEST_sha256': sha((L / 'MANIFEST.json').read_bytes()), 'SEAL_sha256': sha((L / 'SEAL.json').read_bytes()), 'page_sha256': change['new_page_sha256'], 'model_sha256': change['model_sha256']}))
