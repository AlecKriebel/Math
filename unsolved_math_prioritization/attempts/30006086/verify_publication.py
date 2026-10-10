"""Portable integrity, replay, expected rejection and mutation checks. No network.
The wrapper uses explicit checks, even under -O. Algebra runs without -O;
separate optimized invocations MUST reject. Expensive completed full-rank
outputs are checked, not unnecessarily recomputed. Optional --full-replay
repeats both 109-case rank suites in an isolated temporary copy.
"""
import argparse, hashlib, json, os, pathlib, shutil, subprocess, sys, tempfile, zipfile
ROOT=pathlib.Path(__file__).resolve().parent
AUDIT_MANIFEST='885d1664f83847f525286eff0c8f3fea927bdc7ac2688032472d57168b478194'
AUDIT_ZIP='970ace5d0705c32ecf11a4082f7a219e8b74ba9ac723164e8ce6aa63b8a92d91'

def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def get(p):return json.loads(p.read_text())
def integrity(root):
    m=get(root/'PUBLICATION_MANIFEST.json')
    entries=m['files']; names={x['path'] for x in entries}
    require(len(names)==len(entries),'Duplicate manifest paths')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    require(actual==names|{'PUBLICATION_MANIFEST.json'},'Unexpected or missing publication file')
    for x in entries:
        p=root/x['path'];require(p.resolve().is_relative_to(root.resolve()),'Unsafe path')
        b=p.read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'],'Publication hash mismatch: '+x['path'])
    a=root/'audited';require(sha((a/'AUDIT_SHA256SUMS.json').read_bytes())==AUDIT_MANIFEST,'Audit freeze mismatch')
    zb=(root/'AUDITED_PACKET.zip').read_bytes();require(len(zb)==65604 and sha(zb)==AUDIT_ZIP,'Audit archive mismatch')
    with zipfile.ZipFile(root/'AUDITED_PACKET.zip') as z:
        require(len(z.namelist())==len(set(z.namelist())),'Duplicate archive entries')
        names={p.relative_to(a).as_posix() for p in a.rglob('*') if p.is_file()}
        require(set(z.namelist())==names,'Archive inventory mismatch')
        for name in names:require(z.read(name)==(a/name).read_bytes(),'Archive member mismatch: '+name)
    for p in root.rglob('*'):
        require(not p.is_symlink(),'Symlink prohibited')
        if p.is_file():require(p.suffix.lower() not in {'.pdf','.png','.jpg','.jpeg','.html','.sqlite','.csv'},'Unexpected source/data format')
    return len(entries)

def run(args,cwd,ok=True):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
    p=subprocess.run([sys.executable,'-B',*args],cwd=cwd,env=env,text=True,capture_output=True)
    if ok:require(p.returncode==0,'Replay failed: '+str(args)+'\n'+p.stderr)
    else:require(p.returncode!=0 and p.stdout=='' and 'Run without -O:' in p.stderr,'Expected explicit optimized-mode rejection missing')
    return p

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--integrity-only',action='store_true');ap.add_argument('--full-replay',action='store_true');args=ap.parse_args()
    count=integrity(ROOT)
    result={'status':'PASS_PUBLICATION_WRAPPER','status_scope':'Scoped partial results, not full conjecture','sealed_publication_files':count,'target_status':'unsolved','turns':'5/5'}
    if args.integrity_only:
        print(json.dumps(result,sort_keys=True,indent=2));return
    with tempfile.TemporaryDirectory(prefix='loop-invariant-publication-') as t:
        p=pathlib.Path(t)/'packet';shutil.copytree(ROOT,p);a=p/'audited'
        saved=json.loads(run(['VERIFY_AUDIT.py'],a).stdout)
        require(saved['rank_cases']==109 and saved['author_controls']==2137 and saved['supplemental_controls']==319,'Saved-evidence coverage differs')
        optimized=[]
        for script in ['author/verify.py','audit/independent_rank_audit.py','audit/supplemental_controls.py']:
            r=run(['-O',script],a,ok=False);optimized.append({'script':script,'outcome':'EXPECTED_REJECTION','returncode':r.returncode,'stdout_bytes':len(r.stdout.encode())})
        run(['audit/independent_rank_audit.py','--multilinear-max','5','--binary-max','6'],a)
        smoke=get(a/'audit/INDEPENDENT_RANK_REPLAY.json');require(smoke['status']=='PASS' and len(smoke['cases'])==29,'Fresh bounded rank replay failed')
        supplement=run(['audit/supplemental_controls.py'],a).stdout
        require(supplement.encode()==(a/'audit/SUPPLEMENTAL_RESULTS.json').read_bytes(),'Fresh supplemental replay differs')
        # The publication does not inherit assertion-disabled mode from its parent.
        author_smoke="""import json,sys
sys.path.insert(0,'author')
import verify as v
expected=json.load(open('author/EXPECTED_RESULTS.json'))
cases=[x for x in expected['multilinear'] if sum(x['content'])<=5]+[x for x in expected['binary'] if sum(x['content'])<=6]
for x in cases:
 c=tuple(x['content']);v.dimensions(c)
 if v.check(c)!=x:raise RuntimeError('Author bounded replay mismatch')
print(json.dumps({'mode':'nonoptimized','cases':len(cases)}))
"""
        fresh_author=json.loads(run(['-c',author_smoke],a).stdout);require(fresh_author['cases']==29,'Author replay coverage differs')
        (a/'audit/INDEPENDENT_RANK_REPLAY.json').unlink()
        integrity(p)
        mutations=[]
        # Each altered packet must fail before executing altered content.
        for path in ['audited/author/RESULT.md','audited/author/EXPECTED_RESULTS.json','audited/audit/INDEPENDENT_RANK_RESULTS.json','audited/audit/ACCEPTANCE.json','audited/audit/AUDIT_REPORT.md','audited/audit/SUPPLEMENTAL_RESULTS.json','AUDITED_PACKET.zip','audited/AUDIT_SHA256SUMS.json']:
            f=p/path;original=f.read_bytes();f.write_bytes(original+b'X')
            try:integrity(p)
            except RuntimeError:mutations.append(path)
            else:raise RuntimeError('Mutation accepted: '+path)
            finally:f.write_bytes(original)
        stray=p/'UNEXPECTED.txt';stray.write_text('unexpected')
        try:integrity(p)
        except RuntimeError:mutations.append('unexpected file')
        else:raise RuntimeError('Unexpected file accepted')
        finally:stray.unlink()
        missing=p/'audited/author/README.md';old=missing.read_bytes();missing.unlink()
        try:integrity(p)
        except RuntimeError:mutations.append('missing file')
        else:raise RuntimeError('Missing file accepted')
        finally:missing.write_bytes(old)
        integrity(p)
        full='Saved completed 109-case author and independent rank outputs verified; expensive full recomputation not repeated.'
        if args.full_replay:
            r=run(['author/verify.py'],a);require(r.stdout.encode()==(a/'author/EXPECTED_RESULTS.json').read_bytes(),'Full author replay differs')
            run(['audit/independent_rank_audit.py'],a);z=get(a/'audit/INDEPENDENT_RANK_REPLAY.json')
            require(z==get(a/'audit/INDEPENDENT_RANK_RESULTS.json'),'Full independent replay differs')
            full='Both full 109-case calculations recomputed successfully in nonoptimized mode.'
        result.update({'saved_evidence':saved,'fresh_nonoptimized_author_rank_cases':29,'fresh_nonoptimized_independent_rank_cases':29,'fresh_nonoptimized_supplemental_controls':319,'optimized_algebra':optimized,'mutation_rejections':len(mutations),'full_rank_replay':full,'wrapper_optimized':not __debug__})
    integrity(ROOT)
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
