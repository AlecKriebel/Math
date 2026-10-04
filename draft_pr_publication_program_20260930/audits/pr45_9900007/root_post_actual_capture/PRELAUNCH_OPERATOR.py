"""ROOT runs the independently reviewed PR45 administrative phases with real captures."""
from pathlib import Path
import argparse,datetime as dt,hashlib,json,os,subprocess,sys
A=Path(__file__).resolve().parent;R=A.parents[2];H=A/'acceptance_preparation_family'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return{'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def eq(a,b):
    if type(a)is not type(b):return False
    if type(a)is dict:return a.keys()==b.keys()and all(eq(a[k],b[k])for k in a)
    if type(a)is list:return len(a)==len(b)and all(eq(x,y)for x,y in zip(a,b))
    return a==b
def stamp():return dt.datetime.now(dt.timezone.utc).isoformat()
def put(p,b):
    with p.open('xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
def main():
    assert __debug__ and os.environ.get('PYTHONOPTIMIZE','')in('','0')
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['preflight','overlay','prepush','finalize','mirror','post']);p.add_argument('--merge-queue-preimage-sha256');a=p.parse_args()
    cdir=A/'root_final_reconciliation_actual_capture';c=load(cdir/'CAPTURE.json')
    assert c['actual_execution']is True and c['completed']is True and c['exit_code']==0 and c['status']=='PASS'and c['pid']==88023
    assert eq(c['native13_before'],c['native13_after'])and c['main_head_before']==c['main_head_after']
    assert c['source_unchanged']is True and sha((cdir/'PRELAUNCH_SOURCE.py').read_bytes())==sha((H/'seal_final_evidence.py').read_bytes())==c['source_sha256']
    assert sha((cdir/'PRELAUNCH_OPERATOR.py').read_bytes())=='541c4ecf92caf69036adeaf3dbfa2c3e964fd194222ec1bf8100b03394f50a7a'
    for k in ['stdout','stderr']:
        z=c[k];b=(cdir/z['path']).read_bytes();assert len(b)==z['bytes']and sha(b)==z['sha256']
    plan=load(A/'ROOT_FINAL_PLAN.json');final=A/'final_review';receipt=load(final/'ROOT_FINAL_RECONCILIATION.json');mf=load(final/'FINAL_MANIFEST.json')
    assert eq(plan,receipt['entire_scope'])and eq(plan,load(final/'ROOT_REVIEWED_SCOPE.json'))and eq(receipt['bindings_before'],receipt['bindings_after'])
    assert receipt['actual_root_reconciliation']is True and receipt['science_helpers_executed']is False and receipt['shared_mutations']is False
    assert dt.datetime.fromisoformat(c['started_utc'])<=dt.datetime.fromisoformat(receipt['utc'])<=dt.datetime.fromisoformat(c['finished_utc'])
    assert mf['self_excluded']==['FINAL_MANIFEST.json']and mf['files_count']==len(mf['files'])==2
    for z in mf['files']:
        b=(final/z['path']).read_bytes();assert len(b)==z['bytes']and sha(b)==z['sha256']
    stdout=load(cdir/'stdout.bin');assert stdout['final_receipt_sha256']==sha((final/'ROOT_FINAL_RECONCILIATION.json').read_bytes())and stdout['final_manifest_sha256']==sha((final/'FINAL_MANIFEST.json').read_bytes())
    prep=load(H/'PREPARATION_MANIFEST.json');source_pins={z['path']:z['sha256']for z in prep['files']}
    name={'mirror':'state_mirror_reconciliation.py','post':'verify_post_acceptance.py'}.get(a.phase,'integrate_reviewed_partial.py')
    script=H/name;body=script.read_bytes();assert sha(body)==source_pins[name]
    previous=load(H/'INPUT_BINDINGS.json')
    refs={'final-plan':A/'ROOT_FINAL_PLAN.json','final-receipt':final/'ROOT_FINAL_RECONCILIATION.json',
          'final-manifest':final/'FINAL_MANIFEST.json','reconciliation-capture':cdir/'CAPTURE.json',
          'previous-mirror':R/previous['previous_mirror']['path'],'previous-post':R/previous['previous_post']['path'],
          'fresh-preimage':A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES_V2.json','root-bindings':A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json'}
    argv=['/usr/bin/python3','-B',str(script),'--execute','--preparation-manifest-sha256','867faf71a96ada5acf2a92539bfdacd3b69bd3a1a1e0cb7e37ea6a106be1958e']
    for flag,q in refs.items():z=ref(q);argv.extend(['--'+flag,z['path'],'--'+flag+'-sha256',z['sha256']])
    if a.phase not in ['mirror','post']:argv.append(a.phase)
    if a.phase=='overlay':assert a.merge_queue_preimage_sha256;argv.extend(['--merge-queue-preimage-sha256',a.merge_queue_preimage_sha256])
    dest=A/('root_'+a.phase+('_retry2_actual_capture' if a.phase=='preflight' else '_actual_capture'));dest.mkdir()
    operator=Path(__file__).read_bytes();put(dest/'PRELAUNCH_SOURCE.py',body);put(dest/'PRELAUNCH_OPERATOR.py',operator)
    pre={'schema':'ROOT_reviewed_acceptance_phase_prelaunch_v1','phase':a.phase,'argv':argv,'cwd':str(R),
         'operator_pid':os.getpid(),'operator_sha256':sha(operator),'source_sha256':sha(body),'prepared_utc':stamp(),'stdin_supplied':False}
    put(dest/'PRELAUNCH.json',(json.dumps(pre,indent=2)+'\n').encode())
    rec={**pre,'schema':'ROOT_actual_reviewed_acceptance_phase_capture_v1','started_utc':stamp(),'actual_execution':False,'completed':False,'pid':None,'exit_code':None}
    out=err=b''
    try:
        child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        rec.update(actual_execution=True,pid=child.pid);out,err=child.communicate();rec.update(completed=True,exit_code=child.returncode)
    except BaseException:
        import traceback
        rec['operator_error']=traceback.format_exc()
    rec.update(finished_utc=stamp(),source_unchanged=script.read_bytes()==body,operator_unchanged=Path(__file__).read_bytes()==operator)
    for k,b in [('stdout',out),('stderr',err)]:put(dest/(k+'.bin'),b);rec[k]={'path':k+'.bin','bytes':len(b),'sha256':sha(b)}
    rec['status']='PASS'if rec['completed']is True and rec['exit_code']==0 and rec['source_unchanged']and rec['operator_unchanged']and 'operator_error'not in rec else'FAIL'
    put(dest/'CAPTURE.json',(json.dumps(rec,indent=2)+'\n').encode());print(json.dumps(rec,indent=2));return 0 if rec['status']=='PASS'else 1
if __name__=='__main__':sys.exit(main())
