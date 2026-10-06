"""ROOT launches only the already reviewed explicit PR44 administrative phases.

Mutating phases preserve their real before/after differences, rather than use
the read-only final-sealer operator. Every actual child source and stream is saved.
"""
from pathlib import Path
import argparse, datetime as dt, hashlib, json, os, subprocess, sys
A=Path(__file__).resolve().parent;R=A.parents[2];H=A/'acceptance_preparation_family'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def equal(a,b):
    if type(a)is not type(b):return False
    if type(a)is dict:return set(a)==set(b)and all(equal(a[k],b[k])for k in a)
    if type(a)is list:return len(a)==len(b)and all(equal(x,y)for x,y in zip(a,b))
    return a==b
def inspect_final():
    p=A/'root_final_reconciliation_actual_capture';c=load(p/'CAPTURE.json')
    assert c['actual_execution']is True and c['completed']is True and c['status']=='PASS'and type(c['pid'])is int and c['pid']==29359 and c['exit_code']==0
    assert equal(c['native13_before'],c['native13_after'])and c['main_head_before']==c['main_head_after']
    assert c['source_unchanged']is True and sha((p/'PRELAUNCH_SOURCE.py').read_bytes())==c['source_sha256']==sha((H/'seal_final_evidence.py').read_bytes())
    assert sha((p/'PRELAUNCH_OPERATOR.py').read_bytes())=='f4a1ae7322a048ee3bce39654928b07b72cbdae6d3d593bad1830664a4167ee1'
    assert {q.name for q in p.iterdir()}=={'CAPTURE.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'}
    for k in ['stdout','stderr']:
        b=(p/c[k]['path']).read_bytes();assert len(b)==c[k]['bytes']and sha(b)==c[k]['sha256']
    plan=load(A/'ROOT_FINAL_PLAN.json');f=A/'final_acceptance';m=load(f/'FINAL_MANIFEST.json');receipt=load(f/'ROOT_FINAL_RECONCILIATION.json')
    assert equal(plan,load(f/'ROOT_REVIEWED_SCOPE.json'))and equal(plan,receipt['entire_scope'])and equal(receipt['bindings_before'],receipt['bindings_after'])
    assert receipt['actual_root_reconciliation']is True and receipt['science_helpers_executed']is False and receipt['shared_mutations']is False
    assert dt.datetime.fromisoformat(c['started_utc'])<=dt.datetime.fromisoformat(receipt['utc'])<=dt.datetime.fromisoformat(c['finished_utc'])
    assert len(m['files'])==m['files_count']==2 and m['self_excluded']==['FINAL_MANIFEST.json']
    assert {q.name for q in f.iterdir()}=={z['path']for z in m['files']}|{'FINAL_MANIFEST.json'}
    import stat
    for q in f.iterdir():assert stat.S_IMODE(q.stat().st_mode)==0o444
    for z in m['files']:
        b=(f/z['path']).read_bytes();assert len(b)==z['bytes']and sha(b)==z['sha256']
    stdout=load(p/'stdout.bin');assert stdout['final_manifest_sha256']==sha((f/'FINAL_MANIFEST.json').read_bytes())and stdout['final_receipt_sha256']==sha((f/'ROOT_FINAL_RECONCILIATION.json').read_bytes())
def main():
    assert __debug__
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['preflight','overlay','prepush','finalize','mirror','post']);p.add_argument('--merge-queue-preimage-sha256');a=p.parse_args()
    inspect_final()
    sources={'mirror':('state_mirror_reconciliation.py','ce7c815efd82abcb521b8ea323040a9d0c37f06d9eec84fa01ffa78996d4aab1'),'post':('verify_post_acceptance.py','2f4d608a4dd9933a2f6441747477170e233764df8b71b24ce036c20bbdd091dd')}
    name,pin=sources.get(a.phase,('integrate_reviewed_partial.py','4a7c7f3ad1982a12d9c11e237506826bd1eb9ecd35a81d607243d68f43cbc32d'))
    script=H/name;body=script.read_bytes();assert sha(body)==pin
    refs={'final-plan':A/'ROOT_FINAL_PLAN.json','final-receipt':A/'final_acceptance/ROOT_FINAL_RECONCILIATION.json','final-manifest':A/'final_acceptance/FINAL_MANIFEST.json','reconciliation-capture':A/'root_final_reconciliation_actual_capture/CAPTURE.json','previous-mirror':A.parent/'pr43_30004386/state_mirror_bindings.json','previous-post':A.parent/'pr43_30004386/post_acceptance_verification.json','fresh-preimage':A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json','root-bindings':A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json'}
    argv=['/usr/bin/python3','-B',str(script),'--execute','--preparation-manifest-sha256','413ae6bab4142da7b611d910f801cf8ab92d7d085fad4ceed7203074538442de']
    for flag,q in refs.items():z=ref(q);argv.extend(['--'+flag,z['path'],'--'+flag+'-sha256',z['sha256']])
    if a.phase not in sources:argv.append(a.phase)
    if a.phase=='overlay':assert a.merge_queue_preimage_sha256;argv.extend(['--merge-queue-preimage-sha256',a.merge_queue_preimage_sha256])
    dest=A/('root_'+a.phase+'_actual_capture');dest.mkdir()
    (dest/'PRELAUNCH_SOURCE.py').write_bytes(body);(dest/'PRELAUNCH_OPERATOR.py').write_bytes(Path(__file__).read_bytes())
    rec={'schema':'ROOT_actual_reviewed_acceptance_phase_capture_v1','phase':a.phase,'argv':argv,'cwd':str(R),'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'source_sha256':pin,'stdin_supplied':False}
    c=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);b,e=c.communicate()
    rec.update(actual_execution=True,completed=True,pid=c.pid,exit_code=c.returncode,finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),source_unchanged=script.read_bytes()==body)
    for k,v in [('stdout',b),('stderr',e)]:
        (dest/(k+'.bin')).write_bytes(v);rec[k]={'path':k+'.bin','bytes':len(v),'sha256':sha(v)}
    rec['status']='PASS'if c.returncode==0 and rec['source_unchanged']else'FAIL'
    (dest/'CAPTURE.json').write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps(rec,indent=2));return 0 if rec['status']=='PASS'else 1
if __name__=='__main__':sys.exit(main())
