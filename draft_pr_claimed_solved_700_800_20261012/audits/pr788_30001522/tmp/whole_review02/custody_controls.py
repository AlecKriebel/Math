"""Run packet custody controls in separate scratch copies, without editing the sealed packet."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys

def need(ok,message):
    if not ok:raise ValueError(message)

def main():
    a=argparse.ArgumentParser(description=__doc__)
    for name in('packet','scratch','out','preprint-root','primary-root'):a.add_argument('--'+name,type=Path,required=True)
    a.add_argument('--expected-manifest-sha256',required=True);a.add_argument('--expected-checker-sha256',required=True);a.add_argument('--other-python',type=Path,required=True);x=a.parse_args()
    packet=x.packet.absolute();scratch=x.scratch.absolute();need(packet not in scratch.parents and scratch!=packet,'Use separate scratch')
    scratch.mkdir(parents=True,exist_ok=True)
    paths={}
    for name in('portable','changed','missing','extra','symlink','directory','forged'):
        q=scratch/name
        if q.exists():shutil.rmtree(q)
        shutil.copytree(packet,q);paths[name]=q
    p=paths['changed']/'REPORT.md';p.write_bytes(p.read_bytes()+b'\ncorrupted\n')
    (paths['missing']/'REPORT.md').unlink();(paths['extra']/'extra.txt').write_text('extra')
    p=paths['symlink']/'REPORT.md';p.unlink();p.symlink_to(packet/'REPORT.md')
    (paths['directory']/'unexpected_directory').mkdir()
    p=paths['forged']/'REPORT.md';p.write_bytes(p.read_bytes()+b'\nforged\n')
    mf=json.loads((paths['forged']/'MANIFEST.json').read_text())
    for row in mf['files']:
        if row['path']=='REPORT.md':row.update(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    (paths['forged']/'MANIFEST.json').write_text(json.dumps(mf,indent=2)+'\n')
    results=[]
    def run(name,root,py,opt,extra=(),mpin=None,cpin=None,positive=False):
        cmd=[str(py),'-I','-B']+(['-O']if opt else[])+[str(root/'custody_check.py'),'--packet',str(root),'--expected-manifest-sha256',mpin or x.expected_manifest_sha256,'--expected-checker-sha256',cpin or x.expected_checker_sha256]+list(extra)
        q=subprocess.run(cmd,cwd='/',capture_output=True,text=True,timeout=60);v=json.loads(q.stdout)
        ok=q.returncode==0 and v['result']=='PASS'if positive else q.returncode!=0 and v['result']=='FAIL'
        need(ok and not q.stderr,'Control failed: '+name)
        results.append({'case':name,'python':subprocess.check_output([str(py),'--version'],text=True).strip(),'optimized':opt,'expected_observed':True,'returncode':q.returncode,'error':v.get('error')})
    for py in(sys.executable,x.other_python):
        for opt in(False,True):run('relocated_positive',paths['portable'],py,opt,['--preprint-root',str(x.preprint_root),'--primary-root',str(x.primary_root),'--replay'],positive=True)
    for opt in(False,True):
        for name in('changed','missing','extra','symlink','directory','forged'):run(name,paths[name],sys.executable,opt)
        run('wrong_manifest_pin',paths['portable'],sys.executable,opt,mpin='0'*64)
        run('wrong_checker_pin',paths['portable'],sys.executable,opt,cpin='0'*64)
        run('missing_primary_root',paths['portable'],sys.executable,opt,['--primary-root',str(scratch/'absent')])
        run('missing_preprint_root',paths['portable'],sys.executable,opt,['--preprint-root',str(scratch/'absent')])
    result={'result':'PASS','checker_sha256':x.expected_checker_sha256,'manifest_pin_supplied_externally':True,'cases':results,'case_count':len(results),'scope':'Same controls rerun against final externally pinned seal; no packet/source mutation; full primary bodies remain in scratch.'}
    x.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'result':'PASS','controls':len(results)},sort_keys=True))

if __name__=='__main__':main()
