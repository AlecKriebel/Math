#!/usr/bin/env python3
"""Normal/-O/relocation replay and actual corrupted-copy rejection."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parent
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
def need(v,m):
    if not v:raise ValueError(m)
def invoke(p,opt=False):return subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+[str(p/'verify.py')],cwd=p,env=ENV,capture_output=True,text=True)
def seal(p):
    old=json.loads((p/'MANIFEST.json').read_text());new={}
    for n in old:
        f=p/n
        if f.exists() and f.is_file() and not f.is_symlink():
            b=f.read_bytes();new[n]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
        else:new[n]=old[n]
    (p/'MANIFEST.json').write_text(json.dumps(new,indent=2,sort_keys=True)+'\n')
def main():
    pin=json.loads((ROOT/'SOURCE_PIN.json').read_text())
    for n,h in pin.items():need(hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,'preexecution source pin')
    normal=invoke(ROOT);opt=invoke(ROOT,True);need(normal.returncode==opt.returncode==0,'baseline replay');need(normal.stdout==opt.stdout,'normal/-O semantic equality')
    mutations=[]
    with tempfile.TemporaryDirectory(prefix='short cusp audit ') as td:
        td=pathlib.Path(td);p=td/'relocated packet';shutil.copytree(ROOT,p)
        r=invoke(p);need(r.returncode==0 and r.stdout==normal.stdout,'relocation replay')
        def trial(name,action,reseal=False):
            q=td/name;shutil.copytree(ROOT,q);action(q)
            if reseal:seal(q)
            for optimized in (False,True):need(invoke(q,optimized).returncode!=0,'mutation accepted: '+name)
            mutations.append(name)
        def claim(q,path,value):
            f=q/'CLAIMS.json';d=json.loads(f.read_text());v=d
            for key in path[:-1]:v=v[key]
            v[path[-1]]=value;f.write_text(json.dumps(d,indent=2)+'\n')
        trial('changed-proof',lambda q:(q/'PROOFS.md').write_text('changed'))
        trial('missing-proof',lambda q:(q/'PROOFS.md').unlink())
        trial('extra-source-pdf',lambda q:(q/'source.pdf').write_bytes(b'%PDF-1.0'))
        trial('extra-cache-directory',lambda q:(q/'__pycache__').mkdir())
        def symlink(q):(q/'PROOFS.md').unlink();(q/'PROOFS.md').symlink_to(ROOT/'PROOFS.md')
        trial('symlink-proof',symlink)
        for name,path,value in [('false-resolution',['full_resolution'],True),('normalized-norm',['target','norm'],'normalized by index'),('raw-coefficients',['target','coefficients'],'raw(n)'),('epsilon-zero',['target','epsilon'],'nonnegative'),('wrong-norm-scaling',['oldform','norm_N_power'],-11),('wrong-pair-constant',['oldform','prime_pair_lower_bound'],'1'),('all-oldspace-overclaim',['scope_guards','all_oldspace_proved'],True),('prime-level-overclaim',['scope_guards','prime_level_full_space_proved'],True),('false-target-counterexample',['oldform','positive_epsilon_counterexample'],True),('wrong-geometric-area',['geometry','area_lower_bound'],2),('observability-overclaim',['scope_guards','observability_is_proved'],True)]:
            trial(name,lambda q,path=path,value=value:claim(q,path,value),True)
        def null_report(q):
            f=q/'DATA_IDENTITY.json';d=json.loads(f.read_text());d['absent_report']=None;f.write_text(json.dumps(d)+'\n')
        trial('null-absent-report',null_report,True)
        def source_change(q):
            f=q/'verify.py';f.write_text(f.read_text()+'\n# unpinned edit\n')
        trial('unpinned-verifier-edit',source_change,True)
    print(json.dumps({'status':'pass','normal_optimized_relocation_agree':True,'mutation_cases_rejected':len(mutations),'mutation_executions':2*len(mutations),'mutations':mutations,'baseline':json.loads(normal.stdout)},sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:raise SystemExit('FAIL: '+str(e))
