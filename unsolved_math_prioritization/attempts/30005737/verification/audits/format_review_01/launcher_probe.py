#!/usr/bin/env python3
"""Corrected hostile launcher probe. Prior false expectations remain recorded.

The initial hypothesis was that __PYVENV_LAUNCHER__ changes sys.executable
despite -I. It was falsified on this runtime, and no false replay occurred.
"""
import json, os, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import review as r
r.SEQ=max(int(p.name.split('-')[1].split('.')[0]) for p in r.TMP.glob('invocation-*.json'))
helper=r.TMP/'fake-launcher-v2.py'
helper.write_text('''import hashlib,json,sys
from pathlib import Path
c=json.loads(sys.argv[-1]);audit=Path(c['audit']);audit.joinpath('HOSTILE_LAUNCHER_EXECUTED').write_bytes(b'NO_ARCHIVAL_CHILDREN_EXECUTED\\n')
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def flags(mode):return {'optimize':mode,'isolated':1,'no_site':1,'dont_write_bytecode':1,'ignore_environment':1,'safe_path':True}
out=(json.dumps(c['root_result'],indent=2,sort_keys=True)+'\\n').encode()
kinds=['positive','positive','semantic_negative','require_false','corrupt','semantic_negative','require_false','corrupt']
modes=[0,1,0,0,0,1,1,1];events=[]
for kind,mode in zip(kinds,modes):
    events.append({'kind':kind,'measured_flags':flags(mode),'process':{'returncode':0 if kind=='positive' else 1,'stdout':{'bytes':966,'sha256':'2a0062610f5116c92c3689cbb2d12747260d0f42664a277cbb41aee3424046ff'}}})
print(json.dumps({'root_sha256':c['root_sha256'],'root_flags':flags(c['mode']),'root_compile_optimize':c['mode'],'root_stdout':pin(out),'root_output':c['root_result'],'events':events},sort_keys=True))
''')
launcher=r.TMP/'hostile-python-launcher-v2'
def quote(s):return "'"+str(s).replace("'","'\\''")+"'"
launcher.write_text('#!/bin/sh\nexec '+quote(r.PY)+' -I -S -B '+quote(helper)+' "$@"\n');launcher.chmod(0o755)
env=dict(os.environ,__PYVENV_LAUNCHER__=str(launcher))
meta,out,err=r.process('hostile_launcher_interpreter_identity_capability',[r.PY,'-I','-S','-B','-c','import json,sys,os; print(json.dumps({"executable":sys.executable,"base_executable":getattr(sys,"_base_executable",None),"launcher_in_environment":"__PYVENV_LAUNCHER__" in os.environ}))'],environment=env)
identity=json.loads(out)
r.result('isolated_runtime_ignores_hostile_launcher',meta['returncode']==0 and os.path.samefile(identity['executable'],r.PY) and not identity['launcher_in_environment'],dict(identity_receipt='invocation-%03d'%r.SEQ,base_same_actual=os.path.samefile(identity['base_executable'],r.PY),launcher_consumed=not identity['launcher_in_environment']))
capability=r.TMP/'launcher-direct-capability';capability.mkdir();(capability/'processes').mkdir()
config=dict(audit=str(capability/'processes'),mode=0,root_sha256='8e9fba86534cfb75167f9b47a24206d6ca2e03ada94c91725b9023dd026e125b',root_result=dict(integrity='passed',packet_files=18,original_archive_members=9,later_audits=2,finite_diagnostic_conditions_per_run=2896,normal_and_optimized_outputs_match=True,scope='Integrity and finite diagnostics only; not a formal proof.'))
meta,out,err=r.process('hostile_launcher_direct_payload_capability',[str(launcher),'-I','-S','-B','-c','unused',json.dumps(config)])
r.result('hostile_launcher_forged_payload_capability_proven',meta['returncode']==0 and err==b'' and (capability/'processes/HOSTILE_LAUNCHER_EXECUTED').exists() and len(json.loads(out)['events'])==8)
for mode in (0,1):
    receipt=r.TMP/('hostile-launcher-v2-replay-%d'%mode)
    value,meta,out,err=r.cli('hostile_launcher_forged_replay_%d'%mode,['verify',r.PIN,'--root',r.TMP/'portable','--receipt-dir',receipt],mode=mode,tool=r.TMP/'portable/portable.py',environment=env)
    fake=(receipt/'processes/HOSTILE_LAUNCHER_EXECUTED').exists()
    actual_child_receipts=[p for p in (receipt/'processes').glob('child-*.json') if len(p.name)==13]
    r.result('hostile_launcher_resisted_actual_children_%d'%mode,value is not None and value.get('status')=='PASS' and not fake and len(actual_child_receipts)==8,dict(tool_returncode=meta['returncode'],tool_status=value.get('status') if value else None,actual_child_receipts=len(actual_child_receipts),hostile_launcher_marker=fake))
r.save('LAUNCHER_PROBE_DISPOSITION.json',dict(timestamp_utc=r.stamp(),tool_sha256=r.TOOL_PIN,issue='NO_TOOL_DEFECT_FOUND',description='The initial launcher hypothesis was falsified. Under actual -I on this runtime, CPython ignores/consumes the hostile __PYVENV_LAUNCHER__; the forged launcher is not executed, and real archived child receipts are present. A direct payload capability control confirms that the malicious launcher itself works.',modes=[0,1],processes_total=r.SEQ,tests=r.RESULTS,requires_repair=False,prior_expectation_failures_preserved=True))
print(json.dumps(dict(processes_total=r.SEQ,corrected_tests_pass=all(x['passed'] for x in r.RESULTS))))
