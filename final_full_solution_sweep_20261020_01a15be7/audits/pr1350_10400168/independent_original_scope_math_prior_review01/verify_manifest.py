"""Read-only exact closed byte/mode/nsmtime seal and finite-diagnostic verification."""
import hashlib,json,stat,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent
REPO=Path('/Users/alec/Documents/Math')
def need(ok,why):
    if not ok:raise RuntimeError(why)
def sha(b):return hashlib.sha256(b).hexdigest()
def checkfile(f,x,label):
    need(not f.is_symlink(),label+' symlink')
    b=f.read_bytes();s=f.stat()
    need(len(b)==x['bytes'] and sha(b)==x['sha256'],label+' bytes/hash')
    need(stat.S_IMODE(s.st_mode)==x['mode'] and s.st_mtime_ns==x['mtime_ns'],label+' mode/nsmtime')
def main():
    mf=P/'MANIFEST.json';m=json.loads(mf.read_text());actual=[];dirs=['.']
    for f in P.rglob('*'):
        need(not f.is_symlink(),'symlink not allowed')
        if f.is_dir():dirs.append(f.relative_to(P).as_posix())
        elif f.is_file() and f!=mf:actual.append(f.relative_to(P).as_posix())
    need(sorted(actual)==sorted(x['path'] for x in m['members']),'closed file list')
    need(sorted(dirs)==sorted(x['path'] for x in m['directories']),'closed directory list')
    total=mf.stat().st_size
    for x in m['members']:
        checkfile(P/x['path'],x,x['path']);total+=x['bytes']
        if x['path'].startswith('private_sources/'):need(x['mode']==0o600,'raw source file privacy')
    for x in m['directories']:
        f=P if x['path']=='.' else P/x['path'];s=f.stat()
        need(stat.S_IMODE(s.st_mode)==x['mode'] and s.st_mtime_ns==x['mtime_ns'],'directory mode/nsmtime '+x['path'])
    need((P/'private_sources').stat().st_mode&0o777==0o700,'private source directory')
    need(total<=10*1024*1024,'10MiB cap')
    pins=json.loads((P/'PINNED_INPUTS.json').read_text());need(pins['count']==53 and len(pins['blobs'])==53,'pinned blob count')
    for x in pins['external_inputs']:checkfile(Path(x['path']),x,'external '+x['path'])
    for x in m['earlier_seal_references']:checkfile(Path(x['path']),x,'earlier seal '+x['path'])
    need(subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()=='main','main required')
    for x in pins['blobs']:
        b=subprocess.check_output(['git','show',pins['head']+':'+x['path']],cwd=REPO)
        need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'] and len(b)==x['bytes'] and sha(b)==x['sha256'],'pinned blob '+x['path'])
    row=json.loads((P/'PROPOSED_LEDGER_ROW.json').read_text());need(len(row)==1 and len(row[0])==4 and row[0][1]=='' and row[0][2]=='https://doi.org/10.1007/s00220-025-05434-y','four literal proposed cells')
    receipt=json.loads((P/'SOURCE_RECEIPTS.json').read_text());need(len(receipt)==13,'source receipt count')
    for x in receipt:need((P/'private_sources'/(x['id']+'_selected.txt')).is_file(),'private text missing '+x['id'])
    code=(P/'independent_controls.py').read_text();expected=(P/'CONTROL_RESULTS.json').read_bytes();modes=[[],['-O'],['-OO']]
    for mode in modes:
        r=subprocess.run([sys.executable,*mode,'-c',code],capture_output=True,timeout=20)
        need(r.returncode==0 and r.stdout==expected,'finite diagnostic replay '+str(mode))
    rejected=0
    for old,new in [('return -1 if g else 1','return 1'),('mm(mm(invdiag(Fout),P),Fin)','mm(mm(invdiag(Fin),P),Fout)'),('Q(n)**-5*len(seen)','Q(n)**-4*len(seen)')]:
        need(code.count(old)==1,'exact mutation replacement')
        for mode in modes:
            r=subprocess.run([sys.executable,*mode,'-c',code.replace(old,new)],capture_output=True,timeout=20)
            need(r.returncode!=0 and b'RuntimeError' in r.stderr,'mutation survived');rejected+=1
    print(json.dumps({'status':'pass','payload_members':len(m['members']),'pinned_blobs':53,'bytes_including_manifest':total,'control_modes':3,'rejected_mutations':rejected,'manifest_sha256':sha(mf.read_bytes()),'manifest_mode':stat.S_IMODE(mf.stat().st_mode),'manifest_mtime_ns':mf.stat().st_mtime_ns,'private_source_bodies':True,'writes':False,'scope':'AI audit; published general theorems imported; no human/formal verification claim.'},sort_keys=True))
if __name__=='__main__':main()
