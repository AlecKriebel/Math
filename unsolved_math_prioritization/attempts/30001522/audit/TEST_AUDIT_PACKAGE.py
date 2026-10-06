"""Pinned-verifier mutation controls; temporary copies only."""
import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def require(ok,message):
    if not ok:
        raise ValueError(message)


def main():
    root=Path(__file__).resolve().parent
    source=(root/'VERIFY_AUDIT.py').read_bytes()
    manifest=json.loads((root/'MANIFEST.json').read_bytes())
    pin=next(r for r in manifest['files'] if r['name']=='VERIFY_AUDIT.py')
    require(len(source)==pin['bytes'] and hashlib.sha256(source).hexdigest()==pin['sha256'],'verifier source pin')
    encoded=base64.b64encode(source).decode('ascii')
    runner="import base64,sys;sys.argv=['pinned-audit-verifier',sys.argv[1]];exec(compile(base64.b64decode("+repr(encoded)+"),'<pinned verifier>','exec'),{'__name__':'__main__'})"
    modes=[('normal',[]),('optimized',['-O'])]
    rejected=[]

    def manifest_edit(p,edit):
        m=json.loads((p/'MANIFEST.json').read_text())
        edit(m)
        (p/'MANIFEST.json').write_text(json.dumps(m))

    def rehash(p,name):
        b=(p/name).read_bytes()
        def change(m):
            row=next(r for r in m['files'] if r['name']==name)
            row.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
        manifest_edit(p,change)

    def change_json(p,name,key,value):
        m=json.loads((p/name).read_text());m[key]=value
        (p/name).write_text(json.dumps(m));rehash(p,name)

    def link(p,name):
        (p/name).unlink();(p/name).symlink_to(root/name)

    def bad_checker(p):
        path=p/'INDEPENDENT_CHECKS.py';s=path.read_text()
        t=s.replace("(degree+1)-modular_rank(rows,p)==3", "(degree+1)-modular_rank(rows,p)==2")
        require(t!=s,'checker mutation applied')
        path.write_text(t);rehash(p,path.name)

    def duplicate_key(p):
        f=p/'MANIFEST.json';s=f.read_text()
        f.write_text('{"format":"free-p-toral-independent-audit-v1",'+s[1:])

    cases={
        'appended-audit':lambda p:(p/'AUDIT.md').write_bytes((p/'AUDIT.md').read_bytes()+b'changed'),
        'same-size-audit':lambda p:(p/'AUDIT.md').write_bytes(b'!'+(p/'AUDIT.md').read_bytes()[1:]),
        'missing-payload':lambda p:(p/'SOURCE_AUDIT.json').unlink(),
        'extra-file':lambda p:(p/'EXTRA.txt').write_text('unexpected'),
        'extra-directory':lambda p:(p/'extra').mkdir(),
        'cache-directory':lambda p:(p/'__pycache__').mkdir(),
        'payload-symlink':lambda p:link(p,'AUDIT.md'),
        'manifest-symlink':lambda p:link(p,'MANIFEST.json'),
        'fifo':lambda p:os.mkfifo(p/'unexpected.pipe'),
        'duplicate-member':lambda p:manifest_edit(p,lambda m:m['files'].append(dict(m['files'][0]))),
        'duplicate-json-key':duplicate_key,
        'traversal-name':lambda p:manifest_edit(p,lambda m:m['files'][0].update(name='../AUDIT.md')),
        'boolean-byte-count':lambda p:manifest_edit(p,lambda m:m['files'][0].update(bytes=True)),
        'invalid-digest':lambda p:manifest_edit(p,lambda m:m['files'][0].update(sha256='g'*64)),
        'rehash-wrong-checker-semantics':bad_checker,
        'rehash-wrong-expected':lambda p:change_json(p,'INDEPENDENT_RESULTS.json','semantic_controls',6),
        'rehash-wrong-author-binding':lambda p:change_json(p,'AUTHOR_BINDING.json','archive_sha256','0'*64),
        'rehash-wrong-review-binding':lambda p:change_json(p,'DATA_AUDIT.json','review_sha256','0'*64),
        'changed-verifier':lambda p:(p/'VERIFY_AUDIT.py').write_text('raise RuntimeError("untrusted")'),
    }
    with tempfile.TemporaryDirectory(prefix='independent-free-rank-') as tmp:
        temp=Path(tmp)
        def run(p,flags):
            return subprocess.run([sys.executable,'-I','-B']+flags+['-c',runner,str(p)],cwd=temp,capture_output=True,text=True,timeout=30)
        for mode,flags in modes:
            base=run(root,flags);require(base.returncode==0,'baseline '+mode+': '+base.stderr)
            moved=temp/('relocated-'+mode);shutil.copytree(root,moved)
            other=run(moved,flags)
            require(other.returncode==0 and json.loads(base.stdout)==json.loads(other.stdout),'relocation '+mode)
        for label,edit in cases.items():
            p=temp/label;shutil.copytree(root,p);edit(p)
            for mode,flags in modes:
                r=run(p,flags)
                require(r.returncode!=0 and 'FAIL:' in r.stderr,'mutant accepted: '+label+':'+mode)
                rejected.append(label+':'+mode)
        p=temp/'root-link';p.symlink_to(root,target_is_directory=True)
        for mode,flags in modes:
            r=run(p,flags)
            require(r.returncode!=0 and 'FAIL:' in r.stderr,'root symlink accepted')
            rejected.append('root-symlink:'+mode)
        # Intentionally demonstrate the integrity-only boundary. A rehashed prose
        # change cannot be expected to fail without an externally pinned manifest.
        p=temp/'scope-demonstration';shutil.copytree(root,p)
        (p/'AUDIT.md').write_bytes((p/'AUDIT.md').read_bytes()+b'\nTEST-ONLY PROSE CHANGE\n')
        rehash(p,'AUDIT.md')
        for mode,flags in modes:
            require(run(p,flags).returncode==0,'integrity-only boundary demonstration failed')
    return {'status':'PASS','baseline_and_relocation_runs':4,
            'mutation_cases':len(cases)+1,'mutant_rejections':len(rejected),
            'rejected_controls':rejected,'integrity_only_scope_demonstrations':2,
            'verifier_source_pinned_before_execution':True,
            'scope':'Finite packet controls; no formal mathematical proof or public-source reauthentication.'}


if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True,indent=2))
