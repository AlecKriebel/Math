#!/usr/bin/env python3
"""Fixed-bootstrap baseline and delivery-integrity, schema and scope negatives."""
import copy,hashlib,json,os,re,shutil,subprocess,sys,tempfile
from pathlib import Path
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(ok,message):
    if not ok:raise ValueError(message)
def thaw(root):
    root.chmod(0o755)
    for p in root.rglob('*'):
        if p.is_dir() and not p.is_symlink():p.chmod(0o755)
        elif p.is_file() and not p.is_symlink() and p.stat().st_nlink==1:p.chmod(0o644)
def freeze(root):
    for p in root.iterdir():
        if p.is_file() and not p.is_symlink() and p.stat().st_nlink==1:p.chmod(0o444)
        elif p.is_dir() and not p.is_symlink():p.chmod(0o555)
    root.chmod(0o555)
def main():
    need(len(sys.argv)==5,'packet, actual before/after QUEUE, external bootstrap hash required')
    root,before,after=[Path(os.path.abspath(x)) for x in sys.argv[1:4]];bp=sys.argv[4]
    need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000');need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B')
    bootstrap=(root/'BOOTSTRAP.py').read_bytes();need(sha(bootstrap)==bp,'external bootstrap pin')
    code=bootstrap.decode();mp=re.search("MANIFEST_SHA256 = '([0-9a-f]{64})'",code).group(1);vp=re.search("VERIFIER_SHA256 = '([0-9a-f]{64})'",code).group(1)
    verifier=(root/'verify_publication.py').read_bytes();need(sha(verifier)==vp,'authenticated verifier');need(sha((root/'PUBLICATION_MANIFEST.json').read_bytes())==mp,'fixed manifest')
    ns={'__name__':'authenticated_test_target'};exec(compile(verifier,'<authenticated-test-target>','exec'),ns)
    initial=ns['integrity'](root,before,after,mp,bp);snap=initial[0];physical=ns['readonly'](root,before,after)
    mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize];env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C')
    baseline=subprocess.run([sys.executable,'-I','-S','-B',*mode,str(root/'BOOTSTRAP.py'),str(root),str(before),str(after)],capture_output=True,cwd=root,env=env,timeout=120)
    need(baseline.returncode==0 and baseline.stderr==b'','baseline failed');result=ns['parse'](baseline.stdout)
    need(result['whole_delivery_unchanged'] is True,'baseline unchanged')
    for item in result['replays']:ns['compare_output'](item['script'],item['stdout'].encode(),item['stderr'].encode(),snap[ns['refname']('stdout')],snap[ns['refname']('stderr')])
    negatives=[]
    def fixture(label,change,omit=None):
        with tempfile.TemporaryDirectory(prefix='prismatic-negative-') as td:
            td=Path(td);p=td/'packet';shutil.copytree(root,p);thaw(p);b=td/'before.md';a=td/'after.md';b.write_bytes(initial[1]);a.write_bytes(initial[2]);change(p,b,a);freeze(p);b.chmod(0o444);a.chmod(0o444)
            args=[str(p),str(b),str(a)]
            if omit is not None:args.pop(omit)
            try:
                r=subprocess.run([sys.executable,'-I','-S','-B',*mode,str(root/'BOOTSTRAP.py'),*args],cwd=root,env=env,capture_output=True,timeout=20)
                need(r.returncode==1 and r.stdout==b'' and r.stderr in (b'REJECT: bootstrap integrity validation failed\n',b'REJECT: strict publication validation failed\n'),'negative accepted: '+label)
                negatives.append(dict(control=label,exit_code=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode()))
            finally:thaw(p)
    for n in sorted(snap):fixture('changed member '+n,lambda p,b,a,n=n:(p/n).write_bytes(b'altered\n'))
    fixture('missing member',lambda p,b,a:(p/'ACCEPTANCE.md').unlink())
    fixture('extra member',lambda p,b,a:(p/'EXTRA').write_bytes(b'extra\n'))
    fixture('extra directory',lambda p,b,a:(p/'EXTRA').mkdir())
    def symlink(p,b,a):(p/'ACCEPTANCE.md').unlink();(p/'ACCEPTANCE.md').symlink_to(root/'ACCEPTANCE.md')
    def hardlink(p,b,a):os.link(p/'ACCEPTANCE.md',p.parent/'linked')
    def fifo(p,b,a):(p/'ACCEPTANCE.md').unlink();os.mkfifo(p/'ACCEPTANCE.md')
    fixture('symbolic link',symlink);fixture('hard link',hardlink);fixture('special member',fifo)
    fixture('actual before queue mismatch',lambda p,b,a:b.write_bytes(initial[1]+b'\n'))
    fixture('actual after queue mismatch',lambda p,b,a:a.write_bytes(initial[2]+b'\n'))
    fixture('missing required before argument',lambda p,b,a:None,1);fixture('missing required after argument',lambda p,b,a:None,2)
    def reseal(p,b,a):
        (p/'ACCEPTANCE.json').write_bytes(b'{}\n');m=json.loads((p/'PUBLICATION_MANIFEST.json').read_bytes())
        for x in m['files']:
            if x['path']=='ACCEPTANCE.json':x.update(bytes=3,sha256=sha(b'{}\n'))
        (p/'PUBLICATION_MANIFEST.json').write_text(json.dumps(m))
    fixture('replacement manifest cannot replace external pin',reseal)
    semantic=[]
    def reject(label,call):
        try:call()
        except (ValueError,TypeError,KeyError,json.JSONDecodeError) as e:semantic.append(dict(control=label,rejected=True,error=str(e)));return
        raise ValueError('semantic accepted: '+label)
    for label,raw in [('duplicate keys',b'{"a":1,"a":2}'),('NaN',b'{"x":NaN}'),('Infinity',b'{"x":Infinity}'),('negative Infinity',b'{"x":-Infinity}'),('overflow',b'{"x":1e9999}'),('trailing content',b'{} true'),('malformed JSON',b'{')]:reject(label,lambda raw=raw:ns['parse'](raw))
    manifest=ns['parse'](snap['PUBLICATION_MANIFEST.json'])
    def bad_manifest(label,change):
        m=copy.deepcopy(manifest);change(m);reject(label,lambda:ns['validate_manifest'](m,snap))
    for label,value in [('schema bool',True),('schema float',1.0),('schema string','1')]:bad_manifest(label,lambda m,value=value:m.update(schema=value))
    bad_manifest('manifest unknown key',lambda m:m.update(extra=0));bad_manifest('manifest missing key',lambda m:m.pop('schema'));bad_manifest('files wrong type',lambda m:m.update(files={}));bad_manifest('missing inventory row',lambda m:m['files'].pop());bad_manifest('duplicate inventory row',lambda m:m['files'].__setitem__(0,copy.deepcopy(m['files'][1])))
    for label,value in [('bool bytes',True),('float bytes',1.0),('negative bytes',-1),('large bytes',10**30),('string bytes','1')]:bad_manifest(label,lambda m,value=value:m['files'][0].update(bytes=value))
    for value in ['../outside','/tmp/outside',1,'BOOTSTRAP.py','PUBLICATION_MANIFEST.json']:bad_manifest('invalid manifest path '+str(value),lambda m,value=value:m['files'][0].update(path=value))
    bad_manifest('bad digest',lambda m:m['files'][0].update(sha256='z'*64))
    acceptance=ns['EXPECTED_ACCEPTANCE']
    for key,value in [('schema',True),('canonical_problem_id',30004167.0),('new_proof_search_attempts',False),('new_proof_claim',True),('full_affine_source_formulation_certified',True),('full_global_target_certified',True),('novelty_claim',True),('companion_queue_row_changed',True),('p_flatness_necessary',True),('guo_relative_tp_coefficients_explicitly_included',False),('completed_comodule_ext_category','VERIFIED'),('spectral_sequence_page_conventions','VERIFIED'),('coefficient_twist','epsilon^i'),('queue_status','already_solved'),('queue_turns','1/5'),('imported_theorem_proof_replay','PASS'),('source_body_replay','PASS')]:
        obj=copy.deepcopy(acceptance);obj[key]=value;reject('scope '+key,lambda obj=obj:ns['validate_acceptance'](obj))
    obj=copy.deepcopy(acceptance);obj['extra']=0;reject('scope extra field',lambda:ns['validate_acceptance'](obj))
    obj=copy.deepcopy(ns['EXPECTED_QUEUE']);obj['changed_split_column']=True;reject('queue binding exact types',lambda:ns['validate_queue_binding'](obj))
    b,a=initial[1:3];reject('queue added line',lambda:ns['validate_queue_delta'](b,a+b'\n'));reject('queue header changed',lambda:ns['validate_queue_delta'](b,b'x'+a[1:]))
    lines=a.splitlines(keepends=True);i=next(i for i,l in enumerate(lines) if b'| 30004167 / OWR-16941-008 |' in l)
    for col,value in [(8,b' already_solved '),(9,b' 1/5 '),(10,b' changed chat '),(12,b' changed DOI '),(1,b' 9999 ')]:
        changed=list(lines);cells=changed[i].split(b'|');cells[col]=value;changed[i]=b'|'.join(cells);raw=b''.join(changed);reject('queue forbidden column '+str(col),lambda raw=raw:ns['validate_queue_delta'](b,raw))
    raw=a.replace(b'| 30004168 / OWR-16941-009 |',b'| 30004169 / OWR-16941-009 |');reject('companion row changed',lambda:ns['validate_queue_delta'](b,raw))
    out=snap[ns['refname']('stdout')];err=snap[ns['refname']('stderr')]
    def bad_output(label,raw,error=err):reject(label,lambda:ns['compare_output']('check_scope.py',raw,error,out,err))
    for label,raw in [('PASS only',b'{"status":"PASS"}\n'),('extra output',out+b'PASS\n'),('changed formatting',out.replace(b'"status": "PASS"',b'"status":"PASS"')),('integer bool',out.replace(b'"schema": 1',b'"schema": true')),('integer float',out.replace(b'"schema": 1',b'"schema": 1.0')),('false theorem PASS',out.replace(b'"imported_theorem_proof_replay": "NOT_RUN"',b'"imported_theorem_proof_replay": "PASS"'))]:bad_output(label,raw)
    bad_output('unexpected stderr',out,b'warning\n')
    other=snap['check_scope.mode'+str((sys.flags.optimize+1)%3)+'.reference.stdout'];bad_output('wrong optimization mode',other)
    need(ns['same'](1,True) is False and ns['same'](1,1.0) is False and ns['same']({'x':[1]}, {'x':[True]}) is False,'recursive exact-type comparison')
    with tempfile.TemporaryDirectory(prefix='prismatic-hostile-') as td:
        td=Path(td);sentinel=td/'TRIGGERED';evil='from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("bad")\nraise RuntimeError("hostile import")\n'
        for n in ['sitecustomize.py','usercustomize.py','json.py','hashlib.py','check_scope.py']:(td/n).write_text(evil)
        hostile=dict(env,PYTHONPATH=str(td),PYTHONSTARTUP=str(td/'sitecustomize.py'),PYTHONHOME=str(td),PYTHONINSPECT='1',PYTHONDONTWRITEBYTECODE='0')
        h=subprocess.run([sys.executable,'-I','-S','-B',*mode,str(root/'BOOTSTRAP.py'),str(root),str(before),str(after)],cwd=td,env=hostile,capture_output=True,timeout=120)
        need(h.returncode==0 and h.stdout==baseline.stdout and h.stderr==baseline.stderr and not sentinel.exists(),'full hostile baseline differs')
        hostile_record=dict(exit_code=h.returncode,stdout=h.stdout.decode(),stderr=h.stderr.decode(),sentinel_created=False,complete_baseline_output_equal=True)
    need(ns['integrity'](root,before,after,mp,bp)==initial,'whole delivery changed')
    print(json.dumps(dict(schema=1,canonical_problem_id=30004167,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,bootstrap_sha256=bp,manifest_sha256=mp,physical_denials=physical,baseline=dict(exit_code=baseline.returncode,stdout=baseline.stdout.decode(),stderr=baseline.stderr.decode()),integrity_negative_controls=negatives,semantic_negative_controls=semantic,hostile_full_baseline=hostile_record,whole_delivery_unchanged=True,validation_scope='DELIVERY_ONLY_NOT_IMPORTED_THEOREM_PROOFS'),sort_keys=True))
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired) as e:
        print('REJECT: mutation harness failed: '+type(e).__name__+': '+str(e),file=sys.stderr);sys.exit(1)
