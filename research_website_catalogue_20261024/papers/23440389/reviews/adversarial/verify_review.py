#!/usr/bin/env python3
"""Offline, read-only custody and recorded-result closure; never reruns science."""
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / 'sources'
EXCLUDED = {'OWNED_MANIFEST.json', 'FINAL_SEAL.json'}
READY_SHA = '8316224d19c14731bfe4a66946ea1fbe612965bcef284479ebfd9163846147a8'
EARLY_SHA = '1aea749968bd9a0dcdf36d81895a77e85a5e4403642fb4b4595e507f60a73c0b'
checks = 0


def need(condition, message):
    global checks
    checks += 1
    if not condition:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def local(root, name):
    need(isinstance(name, str), 'Non-string path')
    p = PurePosixPath(name)
    need(name != '' and not p.is_absolute() and '..' not in p.parts and str(p) == name,
         'Unsafe or noncanonical relative path')
    target = root / name
    need(not target.is_symlink(), 'Symlink payload')
    need(target.resolve().is_relative_to(root.resolve()), 'Payload escapes root')
    return target


def check_rows(root, rows):
    seen = set()
    for item in rows:
        p = local(root, item['path'])
        need(item['path'] not in seen, 'Duplicate manifest path')
        seen.add(item['path'])
        need(p.is_file(), 'Missing payload: ' + str(p))
        need(type(item['bytes']) is int and p.stat().st_size == item['bytes'], 'Payload size changed: ' + str(p))
        need(sha(p) == item['SHA256'], 'Payload hash changed: ' + str(p))
    return seen


def run(preseal=False):
    manifest = read(HERE / 'OWNED_MANIFEST.json')
    need(manifest['record_id'] == 23440389 and manifest['excluded_terminal_files'] == sorted(EXCLUDED), 'Manifest identity/exclusions')
    owned = check_rows(HERE, manifest['files'])
    actual = {p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file()} - EXCLUDED
    need(owned == actual, 'Owned manifest not complete')
    b = read(HERE / 'SOURCE_BINDINGS.json')
    need(b['record_id'] == 23440389 and Path(b['source_root']) == SOURCE, 'Source binding identity/root')
    bound = check_rows(SOURCE, b['files'])
    actual_source = {p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob('*') if p.is_file()}
    need(bound == actual_source, 'Original source custody file set changed')
    need(sha(SOURCE / 'SOURCE_READY.json') == READY_SHA, 'Original SOURCE_READY changed')
    sm = read(SOURCE / 'SOURCE_READY_MANIFEST.json')
    need(check_rows(SOURCE, sm['files']) == bound - {'SOURCE_READY_MANIFEST.json', 'SOURCE_READY_CLOSURE.json', 'SOURCE_READY_SEAL.json'}, 'Original source manifest boundary changed')
    ss = read(SOURCE / 'SOURCE_READY_SEAL.json')
    for name, key in [('SOURCE_READY.json','SOURCE_READY_SHA256'), ('SOURCE_READY_MANIFEST.json','SOURCE_READY_MANIFEST_SHA256'), ('SOURCE_READY_CLOSURE.json','SOURCE_READY_CLOSURE_SHA256')]:
        need(sha(SOURCE / name) == ss[key], 'Source terminal seal binding')
    ready = read(SOURCE / 'SOURCE_READY.json')
    need(ready['actual_statuses_in_dispatch_order'] == [200,301,200,200,200,200,200], 'Original transport chronology')
    need(ready['native_schema_distinctions']['versions_swh_original'] == [None], 'Original typed null distinction')
    need(ready['native_schema_distinctions']['record_swh_original'] == {}, 'Original empty object distinction')
    need(ready['native_schema_distinctions']['files_order_original'] == [], 'Original empty array/order distinction')
    need(ready['native_schema_distinctions']['files_default_preview_original'] is None, 'Original explicit null distinction')
    need(sha(HERE / 'EARLY_INDEPENDENCE_SEAL.json') == EARLY_SHA, 'Early independent seal changed')
    early = read(HERE / 'EARLY_INDEPENDENCE_SEAL.json')
    em = read(HERE / 'EARLY_MANIFEST.json')
    need(sha(HERE / 'EARLY_MANIFEST.json') == early['manifest_SHA256'], 'Early manifest binding')
    need(Path(em['owned_root']) == HERE / 'early', 'Early manifest root')
    check_rows(HERE / 'early', em['files'])
    need(early['full_actual_PDF_pages'] == 3 and early['full_actual_TeX_lines'] == 201 and early['fresh_individual_rasters_read'] == 3, 'Whole manuscript reading ledger')
    need(early['foreign_science_native_code_results_triage_old_current_peer_opinions_before_seal'] is False, 'Early independence declaration')
    freeze = read(HERE / 'OWN_RESULT_FREEZE_BEFORE_NATIVE.json')
    need(sha(HERE / 'own_controls.py') == freeze['own_code_SHA256'], 'Independent code pre-native freeze')
    need(sha(HERE / 'computations/own-normal.stdout') == freeze['own_normal_output_SHA256'], 'Independent result pre-native freeze')
    need(freeze['before_native_code_or_results_read'] is True, 'Own result chronology')
    own_results = []
    native_results = []
    for mode in ['normal', 'optimized']:
        receipt = read(HERE / f'computations/own-{mode}.receipt.json')
        need(receipt['exit_code'] == 0, 'Own control recorded failure')
        own = read(HERE / f'computations/own-{mode}.stdout')
        need(own['status'] == 'PASS' and own['network'] == own['writes'] == 0, 'Own control recorded disposition')
        need({n:own['fixed_cases'][n]['CSP_count'] for n in ['common4','common5','common6','displayed_bad5']} == {'common4':0,'common5':8,'common6':6336,'displayed_bad5':0}, 'Fixed exact counts')
        need(all(own['state_admissibility_and_boundary_falsifiers'].values()), 'Recorded state boundary rejection')
        need(own['counts']['six_tuple_extension_cases'] == 732 and own['counts']['exhaustive_star_two_list_instances'] == 10000, 'Recorded bounded diagnostics')
        own_results.append((HERE / f'computations/own-{mode}.stdout').read_bytes())
        r = read(HERE / f'reproduction/native-{mode}.receipt.json')
        need(r['exit_code'] == 0 and r['native_code_bytes_identical'] is True and r['native_specimen_bytes_identical'] is True, 'Private native reproduction identity/exit')
        need(r['complete_JSON_equals_original_expected'] is True and r['complete_bytes_equal_original_expected'] is True, 'Whole native expected comparison receipt')
        d = HERE / 'reproduction' / mode
        need((d / 'results.json').read_bytes() == (HERE / 'reproduction/expected_results.original.json').read_bytes(), 'Whole native expected result bytes')
        native_results.append((d / 'results.json').read_bytes())
    need(own_results[0] == own_results[1] and native_results[0] == native_results[1], 'Normal/-O byte comparison')
    selection = read(HERE / 'NATIVE_PROGRAM_SELECTION.json')
    need(selection['main_program']['SHA256'] == 'db37e09e5365d1b3e8c890a6f69bb70e67db79b6ed004cf0e71992badc261439', 'Exact native program selection')
    for name in ['verify.py', 'specimen.json', 'expected_results.json']:
        originals = [p for p in SOURCE.rglob(name) if p.parent.name == 'published-source']
        need(len(originals) == 1, 'Unique actual adjacent native support file')
        source_bytes = originals[0].read_bytes()
        if name == 'expected_results.json':
            need(source_bytes == (HERE / 'reproduction/expected_results.original.json').read_bytes(), 'Original native expected bytes')
        else:
            for mode in ['normal','optimized']:
                need(source_bytes == (HERE / 'reproduction' / mode / name).read_bytes(), 'Unchanged native private copy')
    verdict = read(HERE / 'CUSTOM_VERDICT.json')
    need(verdict['record_id'] == 23440389 and verdict['substantive_defect_found'] is False and verdict['exact_remaining_mathematical_gap'] is None, 'Literal scoped verdict')
    need(verdict['follow_up'] is None and verdict['public_install_authorized'] is False, 'Task boundary')
    if not preseal:
        seal = read(HERE / 'FINAL_SEAL.json')
        need(seal['OWNED_MANIFEST_SHA256'] == sha(HERE / 'OWNED_MANIFEST.json'), 'Final manifest seal')
        need(seal['REPORT_SHA256'] == sha(HERE / 'REPORT.md') and seal['CUSTOM_VERDICT_SHA256'] == sha(HERE / 'CUSTOM_VERDICT.json'), 'Final scientific disposition seal')
        need(seal['owned_payloads'] == len(owned) and seal['unchanged_source_files'] == len(bound), 'Final seal boundaries')
    print(json.dumps({'record_id':23440389,'verdict':'PASS','mode':'preseal' if preseal else 'sealed','checks':checks,'owned_payloads':len(owned),'unchanged_source_files':len(bound),'scientific_campaigns_rerun':0,'network_requests':0,'writes':0}, sort_keys=True))


if __name__ == '__main__':
    need(sys.argv[1:] in [[], ['--preseal']], 'Usage: verify_review.py [--preseal]')
    run(sys.argv[1:] == ['--preseal'])
