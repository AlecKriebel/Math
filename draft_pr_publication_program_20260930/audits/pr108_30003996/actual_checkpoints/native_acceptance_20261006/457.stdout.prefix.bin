"""Authenticate the narrow sealed V5 source correction; no native execution."""
from pathlib import Path
import datetime, difflib, hashlib, json, os, stat
A = Path(__file__).resolve().parent
D = A / 'native_publication_integration_plan_20261006/corrected_v5'
V4 = D.with_name('corrected_v4')
def require(ok, why):
    if not ok: raise RuntimeError(why)
def pin(p):
    require(p.is_file() and not p.is_symlink(), 'Nonregular file')
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
m = json.loads((D/'OUTPUT_MANIFEST.json').read_bytes())
s = json.loads((D/'SEAL_RECEIPT.json').read_bytes())
require(s['sealed'] is True and s['output_manifest'] == pin(D/'OUTPUT_MANIFEST.json'), 'Seal binding')
for row in m['files']:
    p = D/row['relative_path']; got = pin(p)
    require(got['bytes'] == row['bytes'] and got['sha256'] == row['sha256'], 'Manifest body: '+row['relative_path'])
    require(format(stat.S_IMODE(p.stat().st_mode), '04o') == row['mode'], 'File mode')
require(m['file_count'] == len(m['files']) and m['total_bytes'] == sum(x['bytes'] for x in m['files']), 'Manifest totals')
core = m['core_family']; diffs = []
for name, expected in core.items():
    actual = pin(D/name)
    require({k:actual[k] for k in ['bytes','sha256']} == expected, 'Core family')
    if name != 'v3_guards.py':
        require((V4/name).read_bytes() == (D/name).read_bytes(), 'Unexpected family change')
    diffs.append(''.join(difflib.unified_diff((V4/name).read_text().splitlines(True), (D/name).read_text().splitlines(True), fromfile='sealed_corrected_v4/'+name, tofile='corrected_v5/'+name)))
require(''.join(diffs).encode() == (D/'CORE_SOURCE_DIFF.patch').read_bytes(), 'Full exact source diff')
custody = []
for mode in ['NORMAL','OPTIMIZED']:
    p=D/(mode+'_FIXTURE_RESULTS.json'); x=json.loads(p.read_bytes())
    require(x['tests'] == 35 and x['all_passed'] is True and x['exit_code'] == 0 and type(x['actual_PID']) is int and x['actual_PID'] > 0, 'Actual fixture custody')
    for stream in ['stdout','stderr']:
        q=Path(x[stream]['path']); got=pin(q)
        require(got['bytes']==x[stream]['bytes'] and got['sha256']==x[stream]['sha256'], 'Fixture stream')
    require(b'Ran 35 tests' in Path(x['stderr']['path']).read_bytes() and Path(x['stderr']['path']).read_bytes().rstrip().endswith(b'OK'), 'Fixture terminal success')
    custody.append({'mode':mode,'PID':x['actual_PID'],'tests':35,'receipt':pin(p)})
r={'schema':'pr108-root-native-v5-draft-authentication/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),
   'manifest':pin(D/'OUTPUT_MANIFEST.json'),'seal':pin(D/'SEAL_RECEIPT.json'),'manifested_files_verified':len(m['files']),'manifested_bytes_verified':m['total_bytes'],
   'root_complete_V4_source_read_in_previous_review':True,'root_full_V5_source_diff_and_new_GH_guard_read':True,'root_V5_plan_diff_and_F10_ledger_read':True,
   'full_family_diff_regenerated_exactly':True,'only_core_changed':'v3_guards.py','core_family':core,'actual_fixture_custody_authenticated':custody,
   'joint_independent_source_and_actual_configuration_review_pending':True,'native_execution_or_export_clearance':False,'private_configuration_changed':False,
   'completed_mathematics_publication_services_reopened':False,'new_central_proof_search_turns':0}
out=A/'ROOT_NATIVE_V5_DRAFT_AUTHENTICATION_20261006.json'
require(not out.exists(), 'Receipt exists'); out.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
print(json.dumps({'manifested_files':len(m['files']),'tests_each_mode':35,'receipt':pin(out),'native_execution':False}))
