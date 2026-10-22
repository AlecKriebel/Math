#!/usr/bin/env python3
"""Disposable documented-command and deliberate corruption checks for review02."""
from pathlib import Path
import shutil, subprocess, json, hashlib, datetime, tarfile, sys
ROOT=Path(__file__).resolve().parent
CANDIDATE=ROOT.parent.parent/'preprint_v1_0'
def command(path,args):
    r=subprocess.run(args,cwd=path,capture_output=True,text=True)
    return {'args':args,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
def clone(name):
    p=ROOT/'replay'/'controls'/name
    shutil.copytree(CANDIDATE,p,dirs_exist_ok=True);return p
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
records=[]
for name,mutation in [
    ('altered_content',lambda p:(p/'paper.tex').write_bytes((p/'paper.tex').read_bytes()+b'\n% changed\n')),
    ('unmanifested_content',lambda p:(p/'unmanifested.md').write_text('Additional content\n')),
    ('altered_archive',lambda p:(p/'supportkit-v1.0.tar.gz').write_bytes((p/'supportkit-v1.0.tar.gz').read_bytes()[:-1]+b'X')),
    ('altered_wrapper_metadata',lambda p:(p/'zenodo-deposit.json').write_text(json.dumps({'metadata':{},'files':[]}))),
    ('missing_wrapper',lambda p:(p/'zenodo-deposit.json').unlink()),
]:
    p=clone(name);mutation(p);r=command(p,[sys.executable,'verify_package.py']);need(r['exit_code']!=0,name+' was not rejected');records.append(dict(control=name,**r))
    (ROOT/(name+'_STDOUT.txt')).write_text(r['stdout']);(ROOT/(name+'_STDERR.txt')).write_text(r['stderr'])

# Redo the clean-extraction test in a fresh destination with only archive members.
p=ROOT/'replay'/'controls'/'clean_extract';p.mkdir(parents=True,exist_ok=True)
with tarfile.open(CANDIDATE/'supportkit-v1.0.tar.gz') as tf:tf.extractall(p,filter='data')
kit=p/'rank_one_uniqueness_v1_0'
before=command(kit,[sys.executable,'verify_package.py']);build=command(kit,[sys.executable,'build_archive.py']);after=command(kit,[sys.executable,'verify_package.py'])
need(before['exit_code']!=0 and after['exit_code']!=0 and 'zenodo-deposit.json' in before['stderr'],'clean extraction defect changed')
need(build['exit_code']==0,'clean archive build failed')
need((kit/'supportkit-v1.0.tar.gz').read_bytes()==(CANDIDATE/'supportkit-v1.0.tar.gz').read_bytes(),'clean archive rebuild differs')
for label,result in [('CLEAN_VERIFY_BEFORE',before),('CLEAN_BUILD',build),('CLEAN_VERIFY_AFTER',after)]:
    (ROOT/(label+'_STDOUT.txt')).write_text(result['stdout']);(ROOT/(label+'_STDERR.txt')).write_text(result['stderr'])

guard=[]
code="import flow_check; B=flow_check.build([1]); flow_check.feasible(B,[flow_check.Q(-1)]*len(B['E']),flow_check.Q(0))"
flowdir=ROOT/'replay/flow_source_01'
for mode,args in [('normal',[sys.executable,'-c',code]),('optimized',[sys.executable,'-O','-c',code])]:
    q=command(flowdir,args);need(q['exit_code']!=0 and 'RuntimeError: capacity' in q['stderr'],'flow failure guard inactive');guard.append(dict(mode=mode,**q))
    (ROOT/('FLOW_GUARD_'+mode+'_STDERR.txt')).write_text(q['stderr'])

result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'controls':records,'flow_explicit_guards':guard,'clean_extraction':{'verify_before_build':before['exit_code'],'build':build['exit_code'],'verify_after_build':after['exit_code'],'deterministic_rebuild_byte_identical':True,'specific_failure':'Missing intentionally excluded zenodo-deposit.json at unconditional verifier line84','new_P2_finding':True},'limits':'Deliberate corruption controls support implemented integrity gates, not adversarial authenticity or mathematical theorem verification.'}
(ROOT/'NEGATIVE_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'controls':len(records),'guards':len(guard),'clean_extraction':result['clean_extraction']},indent=2))
