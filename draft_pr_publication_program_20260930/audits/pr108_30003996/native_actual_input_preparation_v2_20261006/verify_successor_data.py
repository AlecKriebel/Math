#!/usr/bin/env python3
"""Read-only equality/capacity check for the narrow inert data successor."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import datetime, difflib, hashlib, json, os

D = Path(__file__).absolute().parent
A = D.parent
OLD = A / 'native_actual_input_preparation_20261006'
OLD_DATA = OLD / 'draft_0dd29832e98382f5'
HELPER = A / 'native_publication_integration_plan_20261006/corrected_v5'
FIXED_MAIN = 'f36cb1e34696d460b9cfb5b03425998de48c4669'

def canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(path):
    return json.loads(path.read_bytes())

def main():
    assert sys.flags.ignore_environment and sys.flags.no_site and sys.flags.dont_write_bytecode
    dirs = [p for p in D.glob('draft_*') if p.is_dir()]
    assert len(dirs) == 1
    newdir = dirs[0]
    oldbytes = (OLD_DATA / 'EXECUTION_INPUTS_DRAFT.json').read_bytes()
    newbytes = (newdir / 'EXECUTION_INPUTS_DRAFT.json').read_bytes()
    old, new = json.loads(oldbytes), json.loads(newbytes)
    assert newbytes == canonical(new)
    assert sha(oldbytes) == '0dd29832e98382f5d73ddbc93b139e23d9f11d8cc2f60d53fe4050ce01b709bf'
    assert new['effective']['main_parent'] == old['effective']['main_parent'] == FIXED_MAIN
    for key in ['schema', 'template_only', 'effective', 'input_files']:
        assert canonical(new[key]) == canonical(old[key]), key
    assert len(new['input_files']) == 180
    assert sum(pin['bytes'] for pin in new['input_files']) == 1846309
    family = load(HELPER / 'CORE_FAMILY_MANIFEST.json')['program_files']
    program_changes = []
    for before, after in zip(old['program_files'], new['program_files']):
        name = Path(after['path']).name
        assert name == Path(before['path']).name
        assert after['path'] == before['path'].replace('/corrected_v4/', '/corrected_v5/')
        assert {key: after[key] for key in ['bytes', 'sha256']} == family[name]
        if {key: before[key] for key in ['bytes', 'sha256']} != {key: after[key] for key in ['bytes', 'sha256']}:
            program_changes.append(name)
    assert program_changes == ['v3_guards.py']
    for name in ['EXACT_INPUT_USAGE.json', 'PROPOSED_GATE_CHECKED_ARTIFACT_USAGE.json', 'PRIVATE_EXPORT_EXCLUSIONS.json']:
        assert (newdir / name).read_bytes() == (OLD_DATA / name).read_bytes(), name
    before = (OLD / 'build_execution_inputs.py').read_bytes()
    expected = before.decode().replace("D.name == 'corrected_v4'", "D.name == 'corrected_v5'").replace('Corrected V4 helper only', 'Corrected V5 helper only').replace('Await sealed corrected V4 contract', 'Await sealed corrected V5 contract').encode()
    assert (D / 'build_execution_inputs.py').read_bytes() == expected
    predecessor = load(D / 'PREDECESSOR_UNCHANGED_INPUT_PINS.json')['files']
    for pin in predecessor:
        data = Path(pin['path']).read_bytes()
        assert len(data) == pin['bytes'] and sha(data) == pin['sha256']
    v4 = HELPER.parent / 'corrected_v4'
    diff = []
    for name in family:
        before = (v4 / name).read_text()
        after = (HELPER / name).read_text()
        diff.extend(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True), fromfile='sealed_corrected_v4/' + name, tofile='corrected_v5/' + name))
    assert ''.join(diff).encode() == (HELPER / 'CORE_SOURCE_DIFF.patch').read_bytes()
    capacity = load(newdir / 'CAPACITY_PLAN_WITH_RESERVED_GATES.json')
    oldcapacity = load(OLD_DATA / 'CAPACITY_PLAN_WITH_RESERVED_GATES.json')
    assert capacity['entries'] == oldcapacity['entries']
    assert len(capacity['entries']) + 1 == capacity['file_count_cap'] == 427
    assert sum(entry['max_bytes'] for entry in capacity['entries']) + capacity['exclusive_atomic_write_slot_max_bytes'] == capacity['max_materialized_bytes'] == 135358232
    assert capacity['future_commit_overhead_bytes'] == 16 * 1024 * 1024
    assert capacity['headroom_bytes'] == 32 * 1024 * 1024
    assert capacity['runtime_overhead_bytes'] == 8 * 1024 * 1024
    assert capacity['required_free_bytes'] == 194078488
    journal = load(newdir / 'READ_ONLY_GIT_PROCESS_JOURNAL.json')
    assert len(journal['records']) == 16
    assert all(record['exit_code'] == 0 and record['ambient_inherited'] is False for record in journal['records'])
    receipt = {'schema': 'pr108-inert-input-successor-exact-verification/v1', 'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'actual_verifier_PID': os.getpid(), 'new_execution_inputs_sha256': sha(newbytes), 'new_data_folder': str(newdir),
               'old_execution_inputs_sha256': sha(oldbytes), 'all_effective_choices_exactly_unchanged': True,
               'nongate_registry_and_usage_exactly_unchanged': True, 'private_export_exclusions_exactly_unchanged': True,
               'only_program_source_hash_change': program_changes, 'all_five_program_paths_select_V5': True,
               'predecessor_files_reauthenticated': len(predecessor), 'capacity_inventory_and_reserves_exactly_unchanged': True,
               'required_free_bytes': capacity['required_free_bytes'], 'snapshot_free_bytes': capacity['observed_free_bytes'],
               'snapshot_sufficient': capacity['current_capacity_sufficient'], 'successful_local_Git_read_records': len(journal['records']),
               'native_prepare_assess_export_executions': 0, 'service_calls': 0, 'config_or_new_gates_created': 0,
               'previous_proof_priority_package_PDF_validation_repeated': False, 'input_preparation_percent': 100, 'mathematical_discovery_percent': 100}
    (D / 'EXACT_SUCCESSOR_VERIFICATION.json').write_bytes(canonical(receipt))
    print(json.dumps(receipt, sort_keys=True))

if __name__ == '__main__':
    main()
