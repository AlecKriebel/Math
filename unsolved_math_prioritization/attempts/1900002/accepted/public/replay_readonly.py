#!/usr/bin/env python3
"""External pin and genuinely permission-enforced read-only replay; stdlib only."""
import argparse,hashlib,json,os,pathlib,shutil,stat,subprocess,sys,tempfile
KNOWN={'b2ec1f02b3dd1633c277403e28f7ef34b14d906a7255ddde4d533b43b32670b6':'original_v1','3cc10cb75fbaf266f990e3dc99dc46fd36095439fd6a345d9ec672a023df4ea0':'corrected_v3'}
def need(ok,msg):
    if not ok:raise ValueError(msg)
def digest(data):return hashlib.sha256(data).hexdigest()
def inventory(root):
    out={}
    for p in [root,*sorted(root.rglob('*'))]:
        need(not p.is_symlink(),'symlink in release')
        q={'mode':stat.S_IMODE(p.stat().st_mode),'kind':'directory' if p.is_dir() else 'file'}
        if p.is_file():b=p.read_bytes();q.update(bytes=len(b),sha256=digest(b))
        out['.' if p==root else p.relative_to(root).as_posix()]=q
    return out
def freeze(root):
    for p in sorted(root.rglob('*'),key=lambda p:len(p.parts),reverse=True):p.chmod(0o555 if p.is_dir() else 0o444)
    root.chmod(0o555)
def thaw(root):
    if not root.exists():return
    for p in [root,*root.rglob('*')]:p.chmod(0o755 if p.is_dir() else 0o644)
def deny_writes(root):
    probes=[]
    for p in [root,*sorted(root.rglob('*'))]:
        need(not p.stat().st_mode&0o222,'writable mode')
        target=p/'FORBIDDEN_WRITE_PROBE' if p.is_dir() else p
        try:
            with target.open('xb' if p.is_dir() else 'ab'):pass
        except PermissionError:probes.append('.' if p==root else p.relative_to(root).as_posix())
        else:raise ValueError('actual write succeeded')
    return probes
def invoke(cmd,cwd):
    r=subprocess.run(cmd,capture_output=True,text=True,cwd=cwd,timeout=180)
    need(r.returncode==0,'replay failed: '+r.stderr)
    return json.loads(r.stdout)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--release',type=pathlib.Path,required=True);ap.add_argument('--independent',type=pathlib.Path,required=True);ap.add_argument('--problems',type=pathlib.Path);ap.add_argument('--reports',type=pathlib.Path);ap.add_argument('--sources',type=pathlib.Path);a=ap.parse_args()
    need(os.geteuid()!=0,'unprivileged account required');root=a.release.resolve();control=a.independent.resolve()
    pin=digest((root/'bootstrap.py').read_bytes());need(pin in KNOWN,'external bootstrap pin mismatch')
    before=inventory(root);probes=deny_writes(root);results=[];negatives=[]
    data=[]
    for key in ('problems','reports','sources'):
        value=getattr(a,key)
        if value is not None:data+=['--'+key,str(value.resolve())]
    with tempfile.TemporaryDirectory(prefix='ikea-independent-readonly-') as tmp:
        temp=pathlib.Path(tmp);copy=temp/'release';shutil.copytree(root,copy)
        audit=temp/'audit';audit.mkdir();shutil.copyfile(control,audit/'independent_controls.py');freeze(audit)
        freeze(copy)
        try:
            copybefore=inventory(copy);copyprobes=deny_writes(copy);auditprobes=deny_writes(audit)
            for optimize in range(3):
                flags=['-I','-S','-B']+(['-'+'O'*optimize] if optimize else [])
                bas=invoke([sys.executable,*flags,str(root/'bootstrap.py'),*data],temp)
                rel=invoke([sys.executable,*flags,str(copy/'bootstrap.py'),*data],temp)
                independent=invoke([sys.executable,*flags,str(audit/'independent_controls.py'),'--checker',str(copy/'bundle/author/verify_math.py')],temp)
                need(bas==rel,'relocation changed result')
                results.append({'optimize':optimize,'original':bas,'relocated':rel,'independent':independent})
                hostile=temp/('bad-bootstrap-'+str(optimize)+'.py');hostile.write_text('raise RuntimeError("must not execute")\n')
                need(digest(hostile.read_bytes()) not in KNOWN,'hostile bootstrap trusted');negatives.append('externally_unpinned_bootstrap-'+str(optimize))
                # Run the real authenticated bootstrap against changed artifacts.
                for kind in ('changed_author','forged_target','extra_inventory','author_symlink'):
                    b=temp/(kind+str(optimize));shutil.copytree(root/'bundle',b);thaw(b)
                    if kind=='changed_author':(b/'author/RESULT.md').write_text('changed')
                    elif kind=='forged_target':
                        p=b/'EXTERNAL_MANIFEST.json';m=json.loads(p.read_text());m['problem_id']=1900001;p.write_text(json.dumps(m))
                    elif kind=='extra_inventory':(b/'extra').mkdir()
                    else:
                        p=b/'author/RESULT.md';p.unlink();p.symlink_to(root/'bundle/author/RESULT.md')
                    r=subprocess.run([sys.executable,*flags,str(root/'bootstrap.py'),'--bundle',str(b)],capture_output=True,text=True,cwd=temp,timeout=120)
                    need(r.returncode!=0,'tampered distribution accepted');negatives.append(kind+'-'+str(optimize))
            need(inventory(copy)==copybefore,'readonly relocated release changed')
        finally:thaw(copy);thaw(audit)
    need(inventory(root)==before,'frozen source changed')
    print(json.dumps({'accepted':True,'release':KNOWN[pin],'uid':os.geteuid(),'bootstrap_sha256':pin,'read_only_enforcement':'0444 files and 0555 directories; actual append/create attempts denied to uid 1000; not claimed to be an immutable mount','original_write_denials':probes,'relocated_write_denials':copyprobes,'independent_script_write_denials':auditprobes,'runs':results,'negative_controls':negatives,'unchanged':True,'inventory':before},indent=2,sort_keys=True))
if __name__=='__main__':main()
