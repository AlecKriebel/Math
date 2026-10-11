#!/usr/bin/env python3
"""External native capture of already reviewed read-only family programs.

Writes only its new root-owned capture directory. Complete family and common
source/snapshot file bodies and permission modes are checked before/after.
"""
import argparse, datetime, hashlib, json, os, pathlib, stat, subprocess, sys
A = pathlib.Path(__file__).resolve().parent
WORKSPACE = pathlib.Path('/Users/alec/Documents/Math')
PYTHON = '/opt/homebrew/bin/python3'
ENV = {'PATH':'/opt/homebrew/bin:/usr/bin:/bin', 'LC_ALL':'C', 'TZ':'UTC', 'PYTHONHASHSEED':'0', 'PYTHONDONTWRITEBYTECODE':'1'}
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(path):
    path = pathlib.Path(path)
    content = path.read_bytes()
    return {'bytes':len(content), 'sha256':hashlib.sha256(content).hexdigest(), 'mode':stat.S_IMODE(path.stat().st_mode)}
def inventory(base):
    result = {}
    for p in sorted(base.rglob('*')):
        if p.is_symlink(): raise RuntimeError('Unexpected symbolic link: '+str(p))
        if p.is_file(): result[p.relative_to(base).as_posix()] = pin(p)
    return result
def require(test, reason):
    if not test: raise RuntimeError(reason)
def save(path, value): path.write_text(json.dumps(value,indent=2)+'\n')
parser = argparse.ArgumentParser()
parser.add_argument('family',choices=['honda_lifting','intrinsic_invariants'])
parser.add_argument('--label',required=True)
parser.add_argument('--post-seal',action='store_true')
args = parser.parse_args()
require(args.label.replace('_','').isalnum(), 'Unsafe capture label')
N = A / args.family
OUT = A / 'root_family_capture_private' / args.family / args.label
require(not OUT.exists(), 'Capture already exists; no overwrite')
OUT.mkdir(parents=True)
fixed = {
 'honda_lifting': {
  'AUDIT_MANIFEST.json':'1ec5a038e32117387861a940c3b67946b6c8797db6f90eb0e3fbc1ccac993264',
  'CLOSURE_PLAN.md':'fb3f639bf13c06702763653a83632a8c391af0a19619c07a8b1a30b0a9e22ea5',
  'REPORT.md':'9c83605b88cb4b5a674f9a609d469a2d88396765c4f9cfa8dbd71ec9c7f41a9b',
  'check_realization.py':'5d4a707e1598dbe549fc34a3964d768da9572297724479f4b9793ada056e4624',
  'verify_readonly.py':'925c9740350a3c9b4422acbcdb73a8475ea71b1242a1ef043a18d51b5cfd1524'},
 'intrinsic_invariants': {
  'audit_manifest.json':'3a05a08d812a22a77cd89cfbfb3426b1c84c227465cc422119393de147af8cc2',
  'closure_plan.md':'945b0fdab651396c326edfb4e1791eeca7af4f806377032d0001e70770d609c0',
  'public/report.md':'8bf930367fcfa750dd8728a66644a023f91566c62f7074f963dd7c34781efbf6',
  'public/verify_intrinsic.py':'fbbc16f32a989f723ff9271ef771019919227c1fe81dc3931c49a9c9e460f954',
  'public/construction.json':'e3a9cb8099209241c6d2ee446152dacfd49003c189cab45499c31559b9d323cd',
  'verify_private.py':'5e3f6db381bc5a01187106bc7ccbee120c96b44a5e2422c309c1640d4adfa47d'}
}[args.family]
for relative, expected in fixed.items(): require(pin(N/relative)['sha256']==expected,'Previously reviewed input changed: '+relative)
common_before = {'snapshot':inventory(A/'snapshot'), 'primary_sources':inventory(A/'root_sources_private'), 'root_source_gate':pin(A/'ROOT_SOURCE_ONLY_GATE.json'), 'root_first_candidate_gate':pin(A/'ROOT_FIRST_CANDIDATE_GATE.json')}
before = inventory(N)
binary = pathlib.Path(PYTHON).resolve()
binary_before = pin(binary)
program_before = pin(pathlib.Path(__file__))
save(OUT/'whole_before.json', {'namespace':before,'common':common_before,'binary':binary_before,'capturer':program_before})
executions = []
def capture(label, argv, expected=None):
    expected_pin = None
    if expected is not None:
        expected_bytes = expected.read_bytes()
        (OUT/(label+'.expected.stdout')).write_bytes(expected_bytes)
        expected_pin = pin(OUT/(label+'.expected.stdout'))
    start = now()
    pre = {'utc':start,'argv':argv,'cwd':str(N),'environment_exact':ENV,'binary':str(binary),'binary_pin':binary_before,'capturer_pin':program_before,'whole_before_record':pin(OUT/'whole_before.json'),'expected_stdout_pin':expected_pin}
    save(OUT/(label+'.preexecution.json'),pre)
    process = subprocess.run(argv,cwd=N,env=ENV,capture_output=True)
    end = now()
    (OUT/(label+'.stdout')).write_bytes(process.stdout)
    (OUT/(label+'.stderr')).write_bytes(process.stderr)
    actual = dict(pre, completed_utc=end, exit_status=process.returncode, stdout=pin(OUT/(label+'.stdout')), stderr=pin(OUT/(label+'.stderr')), stdout_text=process.stdout.decode(),stderr_text=process.stderr.decode())
    save(OUT/(label+'.json'),actual)
    executions.append({'label':label,'receipt':pin(OUT/(label+'.json')),'exit_status':process.returncode})
    require(process.returncode==0 and process.stderr==b'',label+' native failure')
    if expected is not None: require(process.stdout==expected_bytes,label+' whole stdout differs from preserved native output')
    return process.stdout
version = capture('interpreter_version',[PYTHON,'--version']).decode().strip()
if args.family=='honda_lifting':
    output = json.loads(capture('full_local',[PYTHON,'-B',str(N/'verify_readonly.py'),'--workspace',str(WORKSPACE),'--manifest',str(N/'AUDIT_MANIFEST.json')]))
    require(output['passed'] is True and output['namespace_file_count']==61 and output['workspace_input_count']==12,'Honda inventory scope changed')
    require(output['manifest_sha256']==fixed['AUDIT_MANIFEST.json'],'Honda manifest mismatch')
    require(len(output['readonly_reruns'])==2,'Missing Honda reruns')
    for run,name in zip(output['readonly_reruns'],['009_independent_realization_controls','010_submitted_checker']):
        expected=(N/'executions'/name/'stdout.txt').read_bytes()
        require(run['stdout'].encode()==expected and run['stderr']=='' and run['exit_code']==0 and run['input_before']==run['input_after'] and run['unchanged_inputs'] is True,'Honda whole rerun failed: '+name)
    require(output['seal_status']==('seal and closure outputs verified' if args.post_seal else 'not yet sealed'),'Wrong Honda closure stage')
else:
    capture('public_controls',[PYTHON,'-B',str(N/'public/verify_intrinsic.py'),'--spec',str(N/'public/construction.json')],N/'runs/independent_intrinsic_v2.stdout')
    command=[PYTHON,'-B',str(N/'verify_private.py'),'--manifest',str(N/'audit_manifest.json'),'--strict-host-binaries']
    if args.post_seal: command.append('--require-seal')
    output=json.loads(capture('full_private',command))
    require(output['status']=='pass' and output['external_files']==20 and output['inventory_files']==38 and output['strict_host_binaries'] is True and output['seal_required']==args.post_seal,'Intrinsic private scope changed')
    require(len(output['runs'])==7 and output['historical_executable_pins']==7,'Intrinsic complete historical native evidence missing')
after=inventory(N)
common_after={'snapshot':inventory(A/'snapshot'),'primary_sources':inventory(A/'root_sources_private'),'root_source_gate':pin(A/'ROOT_SOURCE_ONLY_GATE.json'),'root_first_candidate_gate':pin(A/'ROOT_FIRST_CANDIDATE_GATE.json')}
save(OUT/'whole_after.json',{'namespace':after,'common':common_after,'binary':pin(binary),'capturer':pin(pathlib.Path(__file__))})
require(before==after and common_before==common_after and binary_before==pin(binary) and program_before==pin(pathlib.Path(__file__)),'Whole file body/mode/input custody changed')
receipt={'utc':now(),'status':'PASS_ROOT_EXTERNAL_READONLY_COMPLETE_FAMILY_REPRODUCTION','family':args.family,'stage':'post_seal' if args.post_seal else 'preclosure','namespace_file_count':len(before),'whole_namespace_bodies_modes_unchanged':True,'common_source_and_original_snapshot_bodies_modes_unchanged':True,'binary_unchanged':True,'python_actual_native_version':version,'root_capturer_python':sys.version,'root_capturer_executable':sys.executable,'executions':executions,'whole_before':pin(OUT/'whole_before.json'),'whole_after':pin(OUT/'whole_after.json'),'capture_directory':str(OUT)}
save(OUT/'ROOT_RECEIPT.json',receipt)
print(json.dumps(receipt,indent=2))
