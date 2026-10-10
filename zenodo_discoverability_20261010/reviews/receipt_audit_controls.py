"""Falsification controls for the independent disk-only receipt auditor.

Mutants exist only in a temporary local directory. Approved patches and actual
receipts are never modified. Each mutant preserves the optimistic verification
booleans so the auditor must detect changed data rather than trust those claims.
"""
import copy
import hashlib
import importlib.util
import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('independent_receipt_audit', ROOT / 'audit_receipts.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
entry = next(x for x in json.loads((ROOT / 'APPROVED_PROPOSALS.json').read_text())['records'] if x['id'] == 23271172)
inventory = {x['id']: x for x in json.loads((ROOT / 'INVENTORY.json').read_text())['records']}
catalog = {x['id']: x for x in json.loads((ROOT / 'SOURCE_CATALOG.json').read_text())}
actual_after = json.loads((ROOT / 'receipts/23271172/after.json').read_text())
baseline_hashes = {'23271172': {'sha256': hashlib.sha256((ROOT / 'receipts/23271172/before.json').read_bytes()).hexdigest()}}
results = []
with tempfile.TemporaryDirectory(prefix='receipt-falsification-', dir=ROOT / 'reviews') as temporary:
    audit.HERE = place = Path(temporary)
    (place / 'patches').mkdir()
    (place / 'receipts/23271172').mkdir(parents=True)
    (place / 'reviews').mkdir()
    shutil.copyfile(ROOT / 'patches/23271172.json', place / 'patches/23271172.json')
    shutil.copyfile(ROOT / 'receipts/23271172/before.json', place / 'receipts/23271172/before.json')
    shutil.copyfile(ROOT / entry['independent_content_review'], place / entry['independent_content_review'])
    target = place / 'receipts/23271172/after.json'

    def run(name, mutant, required_failure=None):
        target.write_text(json.dumps(mutant))
        r = audit.audit_one(entry, inventory, catalog, baseline_hashes)
        failed_checks = [x['check'] for x in r['errors']]
        correct = r['status'] == ('pass' if required_failure is None else 'fail')
        if required_failure:
            correct = correct and required_failure in failed_checks
        results.append({'control': name, 'status': r['status'], 'expected_failure': required_failure,
                        'failed_checks': failed_checks, 'passed': correct})
        if not correct:
            raise RuntimeError(name + ': auditor did not reject the intended alteration')

    run('unchanged actual public receipt', actual_after)
    m = copy.deepcopy(actual_after)
    m['doi'] = '10.5281/zenodo.99999999'
    run('new record DOI while verification booleans remain true', m, 'preserved_doi')
    m = copy.deepcopy(actual_after)
    m['identity']['parent_pids']['doi']['identifier'] = '10.5281/zenodo.99999998'
    run('changed concept DOI', m, 'full_identity_exact')
    m = copy.deepcopy(actual_after)
    m['identity']['version_ids'].append('99999997')
    m['identity']['version_count'] += 1
    run('extra version with self-consistent count', m, 'full_identity_exact')
    m = copy.deepcopy(actual_after)
    m['native']['pids'].pop('oai')
    run('public OAI deletion', m, 'preserved_native_pids')
    m = copy.deepcopy(actual_after)
    m['native_files']['entries']['k108_counterexample.pdf']['links']['content'] = 'https://example.invalid/changed'
    run('file content link changed with byte manifest unchanged', m, 'preserved_native_files')
    m = copy.deepcopy(actual_after)
    m['native_files']['entries']['k108_counterexample.pdf']['access']['hidden'] = True
    run('file hidden flag changed with checksum unchanged', m, 'preserved_native_files')
    m = copy.deepcopy(actual_after)
    m['native']['metadata']['creators'][0]['affiliations'][0]['name'] = 'Changed affiliation'
    run('rich native affiliation altered', m, 'all_unpatched_native_metadata_exact')
    m = copy.deepcopy(actual_after)
    m['native']['metadata']['description'] = '<p>Unqualified claim with the caveats removed.</p>'
    run('scientific scope caveats dropped', m, 'scientific_scope_description_exact')
    m = copy.deepcopy(actual_after)
    m['native']['metadata']['subjects'].append({'subject':'unsupported invented classification'})
    run('unapproved extra native search subject', m, 'intended_native_subjects')
    m = copy.deepcopy(actual_after)
    m['native']['metadata']['languages'][0]['id'] = 'fra'
    run('wrong native language while legacy English remains', m, 'intended_native_languages')
    before_path = place / 'receipts/23271172/before.json'
    actual_before = json.loads(before_path.read_text())
    m_before, m = copy.deepcopy(actual_before), copy.deepcopy(actual_after)
    for rec in (m_before, m):
        rec['conceptrecid'] = '99999996'
        rec['identity']['parent_id'] = '99999996'
        rec['identity']['parent_pids']['doi']['identifier'] = '10.5281/zenodo.99999996'
    before_path.write_text(json.dumps(m_before))
    run('coherently changed original and final concept identities', m, 'baseline_matches_original_inventory_identity')
    before_path.write_text(json.dumps(actual_before))
    m_before, m = copy.deepcopy(actual_before), copy.deepcopy(actual_after)
    for rec in (m_before, m):
        rec['native']['pids'].pop('oai')
        rec['identity']['pids'].pop('oai')
    before_path.write_text(json.dumps(m_before))
    run('coherently deleted OAI from both original and final public views', m, 'before_required_public_oai_identity')
    before_path.write_text(json.dumps(actual_before))
    m_before, m = copy.deepcopy(actual_before), copy.deepcopy(actual_after)
    for rec in (m_before, m):
        rec['native_files']['entries']['k108_counterexample.pdf']['links']['content'] = 'https://example.invalid/changed'
    before_path.write_text(json.dumps(m_before))
    run('coherently altered original and final native file links', m, 'frozen_original_baseline_hash')
    before_path.write_text(json.dumps(actual_before))
    raw = {'id':'23271172','is_published':True,'is_draft':False,
           **copy.deepcopy(actual_after['native']), 'files':actual_after['native_files'],
           'parent':{'id':'99999995','pids':actual_after['identity']['parent_pids']},
           'versions':actual_after['identity']['versions']}
    raw_path = place / 'receipts/23271172/native_published.json'
    raw_path.write_text(json.dumps(raw))
    run('full native public record parent ID contradicts summarized identity', actual_after, 'full_native_public_record_parent_id_exact')
    raw_path.unlink()
    # Even a changeset that exactly matches its forged receipt must not count if
    # its local patch bytes differ from the frozen content-review hash.
    patch_path = place / 'patches/23271172.json'
    p = json.loads(patch_path.read_text())
    p['metadata']['keywords'].append('unapproved tag')
    patch_path.write_text(json.dumps(p))
    run('local approved patch changed after content review', actual_after, 'frozen_patch_hash')

# Exercise the exact reviewed name-order repair and the newly bound raw preview
# evidence on independent clones. These are application-schema controls, not
# edits to the original receipts or a broadened permission to rename authors.
repair_entry = next(x for x in json.loads((ROOT / 'APPROVED_PROPOSALS.json').read_text())['records'] if x['id'] == 22770864)
with tempfile.TemporaryDirectory(prefix='receipt-preview-falsification-', dir=ROOT / 'reviews') as temporary:
    audit.HERE = place = Path(temporary)
    (place / 'patches').mkdir()
    (place / 'reviews').mkdir()
    repair_dest = place / 'receipts/22770864'
    shutil.copytree(ROOT / 'receipts/22770864', repair_dest)
    shutil.copyfile(ROOT / 'patches/22770864.json', place / 'patches/22770864.json')
    shutil.copyfile(ROOT / repair_entry['independent_content_review'], place / repair_entry['independent_content_review'])
    repair_actual = {name: json.loads((repair_dest / (name + '.json')).read_text())
                     for name in ('after', 'preview_repair_pre', 'preview_repair_post')}
    repair_baseline = {'22770864': {'sha256': hashlib.sha256((repair_dest / 'before.json').read_bytes()).hexdigest()}}

    def repair_run(name, mutate=None, required_failure=None):
        clones = copy.deepcopy(repair_actual)
        if mutate:
            mutate(clones)
        for key, value in clones.items():
            (repair_dest / (key + '.json')).write_text(json.dumps(value))
        r = audit.audit_one(repair_entry, inventory, catalog, repair_baseline)
        failures = [x['check'] for x in r['errors']]
        correct = r['status'] == ('pass' if required_failure is None else 'fail')
        if required_failure:
            correct = correct and required_failure in failures
        results.append({'control': name, 'status': r['status'], 'expected_failure': required_failure,
                        'failed_checks': failures, 'passed': correct})
        if not correct:
            raise RuntimeError(name + ': auditor did not reject the intended alteration')

    repair_run('exact reviewed name-order repair and original-preview restoration')
    repair_run('unauthorized creator rename after reviewed reversal',
               lambda x: x['after']['native']['metadata']['creators'][0]['person_or_org'].update(name='Unapproved, Author'),
               'intended_native_creators')
    repair_run('identifier loss during approved creator correction',
               lambda x: x['after']['native']['metadata']['creators'][0]['person_or_org'].update(identifiers=[]),
               'intended_native_creators')
    repair_run('affiliation loss during approved creator correction',
               lambda x: x['after']['native']['metadata']['creators'][0].update(affiliations=[]),
               'intended_native_creators')
    repair_run('creator role changed during approved correction',
               lambda x: x['after']['native']['metadata']['creators'][0].update(role={'id':'other'}),
               'intended_native_creators')
    repair_run('unsafe preview payload carries PID operation',
               lambda x: x['preview_repair_pre']['payload'].update(pids={}),
               'preview_repair_payload_only_original_display_and_reviewed_metadata')
    repair_run('unsafe preview payload carries file entries',
               lambda x: x['preview_repair_pre']['payload']['files'].update(entries={}),
               'preview_repair_payload_only_original_display_and_reviewed_metadata')
    repair_run('unsafe preview payload carries access change',
               lambda x: x['preview_repair_pre']['payload'].update(access={'record':'restricted'}),
               'preview_repair_payload_only_original_display_and_reviewed_metadata')

    def wrong_route(clones):
        for route in clones['after']['verification']['mutation_routes']:
            if route['path'] == '/api/records/22770864/draft':
                route['path'] = '/api/records/99999999/draft'
    repair_run('preview restoration targets a different record', wrong_route,
               'record_bound_mutation_route_PUT_/api/records/99999999/draft')
    repair_run('preview restoration owner session belongs to another record',
               lambda x: x['preview_repair_pre']['session'].update(id=99999999),
               'preview_repair_owned_exact_reviewed_session')

    def change_file_access(clones):
        entry = next(iter(clones['preview_repair_post']['draft']['files']['entries'].values()))
        entry['access']['hidden'] = True
    repair_run('preview restoration changes hidden file setting with checksum unchanged', change_file_access,
               'preview_repair_post_full_files_exact_after_precise_draft_omissions')
    repair_run('preview raw evidence has a stale reviewed patch hash',
               lambda x: x['preview_repair_post'].update(patch_sha256='0'*64),
               'preview_repair_post_record_and_frozen_patch')

out = {'generated_utc': datetime.now(timezone.utc).isoformat(), 'controls': results,
       'all_passed': all(x['passed'] for x in results),
       'audit_tool_sha256': hashlib.sha256((ROOT / 'audit_receipts.py').read_bytes()).hexdigest(),
       'source_receipt': 'receipts/23271172/after.json',
       'remote_actions': False, 'actual_receipts_or_patches_changed': False}
(ROOT / 'reviews/FINAL_RECEIPT_AUDIT_CONTROLS.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'controls':len(results),'all_passed':out['all_passed']}))
