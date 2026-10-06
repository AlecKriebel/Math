#!/usr/bin/env python3
"""Full LOCAL audit verifier, requiring private sources and workspace bindings.

This is deliberately not a public default. The portable check_arithmetic.py
is self-contained; this verifier checks the complete private audit package.
No writes, mode changes or Python bytecode generation are performed here.
"""
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path
import stat,subprocess,sys

base=Path(__file__).resolve().parent
def utc():return datetime.now(timezone.utc).isoformat()
def current(p):
    data=p.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
            'mode':stat.S_IMODE(p.stat().st_mode)}
def inventory():
    out={}
    for p in sorted(base.rglob('*')):
        assert not p.is_symlink(),str(p)+' unexpected namespace symlink'
        if p.is_file():out[str(p.relative_to(base))]=current(p)
    return out
def pin_ok(v):
    observed=current(Path(v['path']))
    for key in ['bytes','sha256']:
        assert observed[key]==v[key],str(v['path'])+' '+key
    if 'mode' in v:assert observed['mode']==v['mode'],str(v['path'])+' mode'
before=inventory()
manifest=json.loads((base/'MANIFEST.json').read_text())
assert manifest['excluded_namespace_files']==['MANIFEST.json']
expected=manifest['files']
assert {k:v for k,v in before.items() if k!='MANIFEST.json'}==expected,'namespace bodies/modes/inventory'
external=json.loads((base/'EXTERNAL_BINDINGS.json').read_text())
assert external['candidate_head']=='96395a4f506af6a6045e3cd59afcba2db6b7e2e7'
for v in external['files']:pin_ok(v)
sources=json.loads((base/'SOURCES.json').read_text())
for source in sources['direct_primary_sources']:
    pin_ok(source['pdf'])
    for v in source['inspected_original_renders']:pin_ok(v)
# Validate exact historical streams/receipt bindings, including real failures.
expected_failures={'013_runtime_probe','014_bundled_runtime_probe','020_mutant_drop_twist',
                   '021_mutant_wrong_radical','022_mutant_wrong_cyclotomic','023_mutant_wrong_norm_degree'}
receipts=sorted((base/'executions').iterdir())
assert len(receipts)==28,'exact reviewed receipt inventory'
receipt_summary=[]
for folder in receipts:
    data=json.loads((folder/'metadata.json').read_text())
    assert data['child_launched'] is True,folder.name
    assert data['actual_child_exit_code']==(1 if folder.name in expected_failures else 0),folder.name+' exit'
    assert data['unchanged_inputs'] and data['input_before']==data['input_after'],folder.name+' inputs'
    assert data['start_utc']<=data['end_utc'],folder.name+' UTC order'
    assert data['actual_env']==manifest['execution_environment'],folder.name+' env'
    assert data['actual_cwd']==str(base),folder.name+' cwd'
    for v in data['input_before']+data['output_pins']+[data['capture_program']]:pin_ok(v)
    assert (folder/'stdout.txt').is_file() and (folder/'stderr.txt').is_file()
    receipt_summary.append({'name':folder.name,'actual_exit_code':data['actual_child_exit_code']})
# Full source/dependency check and six exact mathematical stream replays.
argv=[sys.executable,'-B',str(base/'replay_controls.py')]
start=utc()
child=subprocess.run(argv,cwd=base,env=manifest['execution_environment'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
end=utc()
assert child.returncode==0,child.stderr.decode(errors='replace')
result=json.loads(child.stdout)
assert result['status']=='PASS' and result['replayed_mathematical_streams']==6
assert child.stderr==b''
# Check external source bodies/modes again and require whole namespace stability.
for v in external['files']:pin_ok(v)
for source in sources['direct_primary_sources']:
    pin_ok(source['pdf'])
    for v in source['inspected_original_renders']:pin_ok(v)
after=inventory()
assert before==after,'namespace changed during read-only replay'
print(json.dumps({'status':'PASS','scope':'Full LOCAL audit;private sources,original renders,frozen candidate and approved dependency trees required.',
                  'namespace_files_unchanged':len(before),'manifest_sha256':before['MANIFEST.json']['sha256'],
                  'native_receipts':receipt_summary,'positive_mathematical_streams':2,'negative_mutant_streams':4,
                  'actual_replay_argv':argv,'actual_replay_env':manifest['execution_environment'],
                  'actual_replay_cwd':str(base),'start_utc':start,'end_utc':end,
                  'actual_replay_exit_code':child.returncode,'full_replay_stdout':child.stdout.decode(),
                  'full_replay_stderr':child.stderr.decode(),'all_namespace_bodies_modes_inventory_unchanged':True},indent=2,sort_keys=True))
