"""Read-only closed-member, pinned-input, branch, cap and exact replay check."""
from pathlib import Path
import hashlib,json,subprocess,sys

ROOT=Path(__file__).resolve().parent
REPO=Path('/Users/alec/Documents/Math')

def need(ok,message):
    if not ok: raise RuntimeError(message)

def digest(b): return hashlib.sha256(b).hexdigest()

def run():
    m=json.loads((ROOT/'MANIFEST.json').read_text())
    files=[p for p in ROOT.rglob('*') if p.is_file()]
    need(not any(p.is_symlink() for p in ROOT.rglob('*')),'symlink')
    need({str(p.relative_to(ROOT)) for p in files}==set(m['members'])|{'MANIFEST.json'},'closed member mismatch')
    for name,rec in m['members'].items():
        b=(ROOT/name).read_bytes()
        need(len(b)==rec['bytes'] and digest(b)==rec['sha256'],'member mismatch: '+name)
    total=sum(p.stat().st_size for p in files)
    need(total<=8*1024*1024,'8MiB cap')
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()
    need(branch=='main','branch changed')
    pinned=json.loads((ROOT/'PINNED_MEMBER_HASHES.json').read_text())
    need(pinned['head']=='300ad33db51517aba03ce04aa7f257de3d7757c1','head identity')
    need(len(pinned['members'])==8,'pinned path count')
    for rec in pinned['members']:
        b=subprocess.check_output(['git','show',pinned['head']+':'+rec['path']],cwd=REPO)
        obj=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        need(obj==rec['blob'] and len(b)==rec['bytes'] and digest(b)==rec['sha256'],'pinned blob mismatch')
    for rec in pinned['external_inputs']:
        b=Path(rec['path']).read_bytes()
        need(len(b)==rec['bytes'] and digest(b)==rec['sha256'],'external input changed: '+rec['path'])
    expected=(ROOT/'CONTROL_RESULTS.json').read_bytes()
    for mode in [[],['-O'],['-OO']]:
        actual=subprocess.check_output([sys.executable,*mode,str(ROOT/'independent_controls.py')],cwd=ROOT)
        need(actual==expected,'control replay differs')
    s=(ROOT/'independent_controls.py').read_text()
    mutations={
        'floor_instead_of_ceil':('r=(n+k-1)//k','r=n//k'),
        'single_completion_instead_of_full_family':('image=[evaluate(a,xp,field) for a in params]','image=[evaluate(params[0],xp,field)]'),
        'zero_reference_instead_of_exact_contact_family':('exact=[a for a in params if a[k]]','exact=[dict.fromkeys(range(k,n),0)]')}
    for before,after in mutations.values():
        need(s.count(before)==1,'mutation anchor')
        for mode in [[],['-O'],['-OO']]:
            r=subprocess.run([sys.executable,*mode,'-c',s.replace(before,after)],cwd=ROOT,capture_output=True)
            need(r.returncode!=0 and b'RuntimeError' in r.stderr,'mutation escaped')
    print(json.dumps({'status':'pass','payload_members':len(m['members']),'pinned_blobs':8,
          'bytes_including_manifest':total,'branch':branch,'control_modes':3,'rejected_mutations':9,
          'manifest_sha256':digest((ROOT/'MANIFEST.json').read_bytes())},sort_keys=True))

if __name__=='__main__': run()
