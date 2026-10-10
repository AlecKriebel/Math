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
        r = audit.audit_one(entry, inventory, catalog)
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
    # Even a changeset that exactly matches its forged receipt must not count if
    # its local patch bytes differ from the frozen content-review hash.
    patch_path = place / 'patches/23271172.json'
    p = json.loads(patch_path.read_text())
    p['metadata']['keywords'].append('unapproved tag')
    patch_path.write_text(json.dumps(p))
    run('local approved patch changed after content review', actual_after, 'frozen_patch_hash')

out = {'generated_utc': datetime.now(timezone.utc).isoformat(), 'controls': results,
       'all_passed': all(x['passed'] for x in results),
       'audit_tool_sha256': hashlib.sha256((ROOT / 'audit_receipts.py').read_bytes()).hexdigest(),
       'source_receipt': 'receipts/23271172/after.json',
       'remote_actions': False, 'actual_receipts_or_patches_changed': False}
(ROOT / 'reviews/FINAL_RECEIPT_AUDIT_CONTROLS.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'controls':len(results),'all_passed':out['all_passed']}))
