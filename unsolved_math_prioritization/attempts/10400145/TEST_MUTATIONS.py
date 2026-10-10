#!/usr/bin/env python3
"""Disposable publication-boundary controls; authenticate this file first."""
from pathlib import Path
import copy,hashlib,json,os,shutil,subprocess,sys,tempfile
def need(c,m):
    if not c:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def run(root,mode,cwd=None,env=None,args=()):
    return subprocess.run([sys.executable,'-I','-S','-B',*mode,str(root/'BOOTSTRAP.py'),str(root),'--integrity-only',*args],cwd=cwd,env=env,capture_output=True,timeout=30)
def refresh(root,raw):
    old=(root/'PUBLICATION_MANIFEST.json').read_bytes();mh=sha(raw)
    v=root/'VERIFY_PUBLICATION.py';v.write_bytes(v.read_bytes().replace(sha(old).encode(),mh.encode()))
    b=root/'BOOTSTRAP.py';text=b.read_text();text=text.replace(sha(old),mh)
    import re
    text=re.sub(r"VERIFIER_SHA='[a-f0-9]{64}'", "VERIFIER_SHA='"+sha(v.read_bytes())+"'",text)
    b.write_text(text);(root/'PUBLICATION_MANIFEST.json').write_bytes(raw)
def main():
    need(len(sys.argv)==2,'usage: TEST_MUTATIONS.py PACKET');root=Path(sys.argv[1]).absolute()
    original={str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}
    modes=[[],['-O'],['-OO']];negative=[];positive=[]
    with tempfile.TemporaryDirectory(prefix='habiro-wrapper-controls-') as tmp:
        temp=Path(tmp)
        def case(name):
            d=temp/name;shutil.copytree(root,d);return d
        for mode in modes:
            p=run(root,mode);need(p.returncode==0 and not p.stderr,'baseline');positive.append({'name':'integrity-baseline','mode':mode,'stdout_sha256':sha(p.stdout)})
        attacks=['stale-proof','stale-audit-one','stale-audit-two','checker','bootstrap-payload','manifest','missing','extra','extra-empty-dir','symlink-file','symlink-dir','fifo','verifier','wrong-status-repinned']
        for name in attacks:
            d=case(name)
            target={'stale-proof':'author_v3/packet/PROOF_AND_STATUS.md','stale-audit-one':'audit_algebra/INDEPENDENT_AUDIT.md','stale-audit-two':'audit_source_bridge/FULL_AUDIT.md','checker':'author_v3/packet/verify.py','bootstrap-payload':'author_v3/bootstrap.py','manifest':'PUBLICATION_MANIFEST.json','verifier':'VERIFY_PUBLICATION.py'}.get(name)
            if target:
                p=d/target;p.write_bytes(p.read_bytes()+b'\n# changed\n')
            elif name=='missing':(d/'author_v3/packet/CLAIMS.json').unlink()
            elif name=='extra':(d/'extra.txt').write_text('unexpected')
            elif name=='extra-empty-dir':(d/'extra-directory').mkdir()
            elif name=='symlink-file':
                p=d/'author_v3/packet/CLAIMS.json';p.unlink();p.symlink_to(root/'author_v3/packet/CLAIMS.json')
            elif name=='symlink-dir':shutil.rmtree(d/'audit_algebra');(d/'audit_algebra').symlink_to(root/'audit_algebra',target_is_directory=True)
            elif name=='fifo':os.mkfifo(d/'unexpected-fifo')
            elif name=='wrong-status-repinned':
                p=d/'author_v3/packet/CLAIMS.json';c=json.loads(p.read_bytes());c['status']='unsolved';p.write_text(json.dumps(c))
                m=json.loads((d/'PUBLICATION_MANIFEST.json').read_bytes())
                for e in m['files']:
                    if e['path']=='author_v3/packet/CLAIMS.json':e.update(bytes=len(p.read_bytes()),sha256=sha(p.read_bytes()))
                refresh(d,(json.dumps(m)+'\n').encode())
            for mode in modes:
                p=run(d,mode);need(p.returncode!=0 and b'REJECT:' in p.stderr,'integrity attack accepted: '+name);negative.append({'name':name,'mode':mode,'rejected':True})
        base=json.loads((root/'PUBLICATION_MANIFEST.json').read_bytes())
        changes=[('wrong-type-id',lambda m:m.update(problem_id=True)),('wrong-rank',lambda m:m.update(rank=1009)),('wrong-status',lambda m:m.update(status='unsolved')),('wrong-resolution',lambda m:m.update(resolution='positive')),('wrong-approaches',lambda m:m.update(approaches=1.0)),('missing-key',lambda m:m.pop('rank')),('extra-key',lambda m:m.update(extra=1)),('empty-files',lambda m:m.update(files=[])),('non-list-files',lambda m:m.update(files={})),('duplicate-entry',lambda m:m['files'].append(m['files'][0])),('unsafe-path',lambda m:m['files'][0].update(path='../escape')),('absolute-path',lambda m:m['files'][0].update(path='/escape')),('boolean-size',lambda m:m['files'][0].update(bytes=True)),('bad-hash-type',lambda m:m['files'][0].update(sha256=7)),('unknown-entry-key',lambda m:m['files'][0].update(extra=0))]
        variants=[]
        for name,mutate in changes:
            m=copy.deepcopy(base);mutate(m);variants.append((name,json.dumps(m).encode()))
        variants += [('duplicate-json-key',b'{"rank":1010,'+(root/'PUBLICATION_MANIFEST.json').read_bytes().lstrip()[1:]),('invalid-json',b'{'),('non-object',b'[]'),('nonfinite',b'{"rank":NaN}')]
        for name,raw in variants:
            d=case(name);refresh(d,raw)
            for mode in modes:
                p=run(d,mode);need(p.returncode!=0 and b'REJECT:' in p.stderr,'schema attack accepted: '+name);negative.append({'name':name,'mode':mode,'rejected':True,'disposable_pins_deliberately_refreshed':True})
        hostile=temp/'hostile';hostile.mkdir();sentinel=hostile/'EXECUTED'
        for n in ['json','hashlib','pathlib','subprocess','sitecustomize']:(hostile/(n+'.py')).write_text('open('+repr(str(sentinel))+',"w").write("bad")\nraise RuntimeError("hostile import")\n')
        env=dict(os.environ);env['PYTHONPATH']=str(hostile);env['PYTHONSTARTUP']=str(hostile/'json.py')
        for mode in modes:
            p=run(root,mode,hostile,env);need(p.returncode==0 and not p.stderr and not sentinel.exists(),'hostile imports');positive.append({'name':'hostile-cwd-pythonpath','mode':mode,'stdout_sha256':sha(p.stdout)})
        for label,args in [('one-corpus',['--problems',str(temp/'absent')]),('optional-integrity',['--source-dir',str(temp)])]:
            for mode in modes:
                p=run(root,mode,args=args);need(p.returncode!=0 and b'REJECT:' in p.stderr,'CLI conflict accepted');negative.append({'name':label,'mode':mode,'rejected':True})
    after={str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()};need(original==after,'original packet changed')
    need(len(set(e['stdout_sha256'] for e in positive))==1,'optimization or hostile cwd changed result')
    print(json.dumps({'status':'PASS','negative_count':len(negative),'positive_count':len(positive),'originals_unchanged':True,'negative':negative,'positive':positive},sort_keys=True))
if __name__=='__main__':main()
