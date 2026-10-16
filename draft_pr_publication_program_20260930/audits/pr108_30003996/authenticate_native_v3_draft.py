"""Authenticate sealed V3 draft custody; never commission or execute native work."""
from pathlib import Path
import datetime, hashlib, json, os, stat

A = Path(__file__).resolve().parent
D = A / 'native_publication_integration_plan_20261006/corrected_v3'

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def pin(path):
    require(path.is_file() and not path.is_symlink(), str(path))
    body = path.read_bytes()
    return {'path': str(path), 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}

manifest_pin = pin(D / 'OUTPUT_MANIFEST.json')
require(manifest_pin['sha256'] == 'c8dd6e401fe64a57d048f5420c47e3afea3b9269649948f098dc645ccdcbe8e4', 'manifest differs')
manifest = json.loads((D / 'OUTPUT_MANIFEST.json').read_bytes())
seal = json.loads((D / 'SEAL_RECEIPT.json').read_bytes())
require(seal['output_manifest'] == manifest_pin, 'seal manifest binding')
names = set()
total = 0
for entry in manifest['files']:
    name = entry['relative_path']
    require(name not in names and not Path(name).is_absolute() and '..' not in Path(name).parts, 'unsafe/duplicate name')
    names.add(name)
    path = D / name
    require(path.resolve().is_relative_to(D), 'outside draft')
    actual = pin(path)
    require(actual['bytes'] == entry['bytes'] and actual['sha256'] == entry['sha256'], 'body differs: ' + name)
    require(format(stat.S_IMODE(path.stat().st_mode), '04o') == entry['mode'], 'mode differs: ' + name)
    total += actual['bytes']
actual_names = {str(p.relative_to(D)) for p in D.rglob('*') if p.is_file()}
require(actual_names == names | {'OUTPUT_MANIFEST.json', 'SEAL_RECEIPT.json'}, 'actual inventory differs')
require(len(names) == manifest['file_count'] == seal['manifested_file_count'] == 91, 'count')
require(total == manifest['total_bytes'] == seal['manifested_bytes'] == 591392, 'total bytes')
require(manifest['core_family'] == seal['core_family'], 'core family differs')
core_names = {'prepare_review_bundle.py', 'v3_guards.py', 'bounded_process.py', 'native_assess_worker.py', 'launch_review_bundle.sh'}
require(set(seal['core_family']) == core_names, 'core family inventory')
for name, expected in seal['core_family'].items():
    actual = pin(D / name)
    require({k: actual[k] for k in ('bytes', 'sha256')} == expected, 'core body: ' + name)
results = []
for mode, pid in [('NORMAL', 6728), ('OPTIMIZED', 6834)]:
    result_path = D / (mode + '_FIXTURE_RESULTS.json')
    result = json.loads(result_path.read_bytes())
    require(result['actual_PID'] == pid and result['exit_code'] == 0 and result['tests'] == 27 and result['all_passed'], 'fixture result')
    require(result['fixture_only'] and result['native_prepare_assess_export_install_executions'] == result['service_calls'] == 0, 'fixture scope')
    for stream in ('stdout', 'stderr'):
        expected = result[stream]
        actual = pin(Path(expected['path']))
        require(all(actual[k] == expected[k] for k in ('path', 'bytes', 'sha256')), 'fixture stream binding')
    require('Ran 27 tests' in Path(result['stderr']['path']).read_text() and Path(result['stderr']['path']).read_text().rstrip().endswith('OK'), 'fixture full output')
    results.append({'mode': mode, 'PID': pid, 'tests': 27, 'exit_code': 0, 'result': pin(result_path)})
require(not seal['actual_runtime_configuration_prepared'] and not seal['capacity_clearance'], 'draft authority')
receipt = {
    'schema': 'pr108-root-native-v3-draft-authentication/v1',
    'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'actual_operator_PID': os.getpid(),
    'manifest': manifest_pin, 'seal': pin(D / 'SEAL_RECEIPT.json'),
    'manifested_files_verified': 91, 'actual_files_verified': 93,
    'manifested_bytes_verified': total, 'core_family': seal['core_family'],
    'root_full_read_of_all_five_core_programs': True,
    'root_full_PLAN_read_completed_with_private_config_paragraph_readback': True,
    'fixture_custody_authenticated': results,
    'fresh_independent_source_review_pending': True,
    'reported_worker_control_correspondence_issue_under_review': True,
    'actual_execution_inputs_or_configuration_created': False,
    'native_execution_or_export_clearance': False,
    'mathematics_or_published_package_reopened': False,
    'new_central_proof_search_turns': 0,
}
output = A / 'ROOT_NATIVE_V3_DRAFT_AUTHENTICATION_20261006.json'
require(not output.exists(), 'refuse to replace receipt')
output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
print(json.dumps({'receipt': pin(output), 'manifested_files': 91, 'core_programs': 5, 'native_clearance': False}))
