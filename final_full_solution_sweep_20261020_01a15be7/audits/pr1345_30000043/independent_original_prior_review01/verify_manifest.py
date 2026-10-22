"""Read-only closed-member, Git-blob and certified-polynomial replay."""
from pathlib import Path
import json,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parent
REPO=Path('/Users/alec/Documents/Math')
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    m=json.loads((ROOT/'MANIFEST.json').read_text())
    paths=list(ROOT.rglob('*'))
    need(not any(p.is_symlink() for p in paths),'symlink')
    files=[p for p in paths if p.is_file()]
    need({str(p.relative_to(ROOT)) for p in files}==set(m['members'])|{'MANIFEST.json'},'member set')
    for name,rec in m['members'].items():
        b=(ROOT/name).read_bytes()
        need(len(b)==rec['bytes'] and sha(b)==rec['sha256'],'member hash: '+name)
    total=sum(p.stat().st_size for p in files)
    need(total<=6*1024*1024,'6MiB cap')
    need(subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()=='main','main branch')
    pin=json.loads((ROOT/'PINNED_MEMBER_HASHES.json').read_text())
    need(pin['head']=='6455aec3553e2f16ab001c8f8996583ce73aba13','head')
    need(len(pin['members'])==27,'27 pinned paths')
    for rec in pin['members']:
        b=subprocess.check_output(['git','show',pin['head']+':'+rec['path']],cwd=REPO)
        obj=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        need(obj==rec['blob'] and sha(b)==rec['sha256'] and len(b)==rec['bytes'],'pinned blob')
    for rec in pin['external_inputs']:
        b=Path(rec['path']).read_bytes()
        need(sha(b)==rec['sha256'] and len(b)==rec['bytes'],'external input changed')
    expected=(ROOT/'CONTROL_RESULTS.json').read_bytes()
    for mode in [[],['-O'],['-OO']]:
        need(subprocess.check_output([sys.executable,*mode,str(ROOT/'independent_controls.py')],cwd=ROOT)==expected,'control replay')
    s=(ROOT/'independent_controls.py').read_text()
    variants=[('if k%2==0','if k%2!=0'),('(-1)**n*comb','comb'),('scale(eps*eps,V(Vs(v)))','scale(eps*eps,v)')]
    for before,after in variants:
        need(s.count(before)==1,'mutation anchor')
        for mode in [[],['-O'],['-OO']]:
            z=subprocess.run([sys.executable,*mode,'-c',s.replace(before,after)],cwd=ROOT,capture_output=True)
            need(z.returncode!=0 and b'RuntimeError' in z.stderr,'mutation not rejected')
    doi=json.loads((ROOT/'datacite_record.json').read_text())['data']['attributes']
    need(doi['doi']=='10.5281/zenodo.23438995' and doi['state']=='findable' and doi['isActive'],'DOI receipt')
    need(doi['registered']=='2026-10-17T16:01:32.000Z','DOI date')
    need(sha((ROOT/'ferudun2026.pdf').read_bytes())=='4c94d59915ef1b90ab1d731e643a8cd6524c616d502fc96e4ed6cb2b12466558','public full-target source pin')
    print(json.dumps({'status':'pass','payload_members':len(m['members']),'pinned_blobs':27,'bytes_including_manifest':total,
          'control_modes':3,'rejected_mutations':9,'main_branch':True,'public_full_target_doi':'10.5281/zenodo.23438995',
          'manifest_sha256':sha((ROOT/'MANIFEST.json').read_bytes())},sort_keys=True))
if __name__=='__main__':main()
