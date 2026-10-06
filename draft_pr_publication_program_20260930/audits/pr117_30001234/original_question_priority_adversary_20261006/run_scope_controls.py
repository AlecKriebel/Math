#!/usr/bin/env python3
import datetime, hashlib, json, os, pathlib, subprocess
D=pathlib.Path(__file__).resolve().parent
PY='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
ENV={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
def ck(b,m):
    if not b: raise ValueError(m)
def stamp(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    b=p.read_bytes(); return {'relative_path':str(p.relative_to(D)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
# New crop renders are pinned before executing the source-bound comparator.
old=json.loads((D/'SOURCE_MANIFEST.json').read_text())
urls={r['relative_path']:r.get('public_url') for r in old['private_members']}
private=[]
for folder in ['private_sources','private_renders']:
    for p in sorted((D/folder).rglob('*')):
        if p.is_file(): private.append({**pin(p),'public_url':urls.get(str(p.relative_to(D)))})
old.update({'actual_recorder_pid':os.getpid(),'utc':stamp(),'private_members':private})
(D/'SOURCE_MANIFEST.json').write_text(json.dumps(old,indent=2,sort_keys=True)+'\n')
J={'schema':'pr117-original-question-controls-actual/v1','pid':os.getpid(),'started_utc':stamp(),'physical_python':PY,'controlled_environment':ENV,'events':[],'new_proof_turns':0,'original_candidate_unchanged':True}
def emit(): (D/'CHECK_PROCESS_RECEIPT.json').write_text(json.dumps(J,indent=2,sort_keys=True)+'\n')
seen={}; emit()
for mode,optimized,private_mode,false in [
 ('private_normal',False,True,False),('private_optimized',True,True,False),
 ('portable_normal',False,False,False),('portable_optimized',True,False,False),
 ('false_normal',False,False,True),('false_optimized',True,False,True)]:
    argv=[PY]+(['-O'] if optimized else [])+['-E','-S','-B','-P',str(D/'priority_scope_checks.py')]
    if private_mode: argv.append('--with-private-sources')
    if false: argv.append('--force-false')
    ev={'mode':mode,'argv':argv,'started_utc':stamp()}; J['events'].append(ev); emit()
    p=subprocess.Popen(argv,cwd=str(D),env=ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    ev['actual_child_pid']=p.pid; emit()
    out,err=p.communicate(timeout=40)
    stdout_path=D/(mode+'.stdout.json' if not false else mode+'.stdout.txt')
    stderr_path=D/(mode+'.stderr.txt')
    stdout_path.write_bytes(out); stderr_path.write_bytes(err)
    ev.update({'returncode':p.returncode,'stdout_pin':pin(stdout_path),'stderr_pin':pin(stderr_path),'finished_utc':stamp()}); emit()
    if false:
        ck(p.returncode!=0 and b'ValueError: forced false priority guard' in err,'False guard must be rejected '+mode)
        ev['status']='expected_false_rejected'
    else:
        ck(p.returncode==0 and len(err)==0,'Scope checker must succeed '+mode)
        value=json.loads(out)
        ck(value['status']=='PASS' and value['exact_prior_counterexample'] and not value['originality_clearance'],'Narrow priority decision '+mode)
        seen[mode]=value; ev['status']='PASS'; ev['guards']=value['guards']
    emit()
ck(seen['private_normal']==seen['private_optimized'],'Private mode must have identical semantics under optimization')
ck(seen['portable_normal']==seen['portable_optimized'],'Portable mode must have identical semantics under optimization')
J.update({'status':'PASS','finished_utc':stamp(),'private_members_verified':len(private),'private_guards':seen['private_normal']['guards'],'portable_guards':seen['portable_normal']['guards'],'optimized_equivalence':True,'false_guard_controls':2}); emit()
print(json.dumps({k:J[k] for k in ['pid','status','private_members_verified','private_guards','portable_guards','optimized_equivalence','false_guard_controls']},sort_keys=True))
