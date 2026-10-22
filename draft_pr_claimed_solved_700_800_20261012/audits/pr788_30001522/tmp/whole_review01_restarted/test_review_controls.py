"""Damage controls on temporary copies only; pass an owned scratch directory."""
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path

def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--packet-root',type=Path,required=True);a.add_argument('--preprint-root',type=Path,required=True);a.add_argument('--scratch-root',type=Path,required=True);a.add_argument('--manifest-sha256',required=True);a.add_argument('--checker-sha256',required=True);x=a.parse_args()
    results=[]
    cases=['baseline relocated','wrong manifest pin','wrong checker pin','payload damage','missing member','unlisted member','extra directory','payload symlink','manifest symlink','checker damage','source proof damage','wrong released PDF','extra empty source directory','missing fresh primary bank']
    for o in(False,True):
        for case in cases:
            with tempfile.TemporaryDirectory(dir=x.scratch_root,prefix='review-negative-')as tmp:
                w=Path(tmp);r=w/'review';shutil.copytree(x.packet_root,r);p=x.preprint_root;args=[];mpin=x.manifest_sha256;cpin=x.checker_sha256
                if case=='wrong manifest pin':mpin='0'*64
                elif case=='wrong checker pin':cpin='0'*64
                elif case=='payload damage':q=r/'REPORT.md';q.write_bytes(q.read_bytes()+b'\nDamage\n')
                elif case=='missing member':(r/'REPORT.md').unlink()
                elif case=='unlisted member':(r/'unlisted').write_text('extra')
                elif case=='extra directory':(r/'unlisted_directory').mkdir()
                elif case in('payload symlink','manifest symlink'):
                    q=r/('REPORT.md'if case=='payload symlink'else'MANIFEST.json');z=w/'outside';z.write_bytes(q.read_bytes());q.unlink();q.symlink_to(z)
                elif case=='checker damage':q=r/'verify_review.py';q.write_bytes(q.read_bytes()+b'\n# Damage\n')
                elif case in('source proof damage','wrong released PDF','extra empty source directory'):
                    p=w/'preprint';p.mkdir();shutil.copytree(x.preprint_root/'source',p/'source')
                    bindings=json.loads((r/'INPUT_BINDINGS.json').read_text())
                    for e in bindings['preprint_files']:
                        q=p/e['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(x.preprint_root/e['path'],q)
                    if case=='source proof damage':q=next((p/'source/audit/intake/original').rglob('PROOF.md'));q.write_bytes(q.read_bytes()+b'\nDamage\n')
                    elif case=='wrong released PDF':q=p/'output/pdf/paper.pdf';q.write_bytes(q.read_bytes()+b'\nDamage\n')
                    else:(p/'source/unlisted_empty_directory').mkdir()
                elif case=='missing fresh primary bank':args=['--primary-root',str(w)]
                cmd=[sys.executable,'-I','-B']+(['-O']if o else[])+[str(r/'verify_review.py'),'--packet-root',str(r),'--preprint-root',str(p),'--manifest-sha256',mpin,'--checker-sha256',cpin]+args
                run=subprocess.run(cmd,cwd='/',capture_output=True,text=True,timeout=30,env=dict(os.environ,TMPDIR=str(x.scratch_root)))
                val=json.loads(run.stdout);accepted=run.returncode==0 and val.get('result')=='PASS';expected=case.startswith('baseline')
                if accepted!=expected:raise ValueError('Unexpected control outcome: '+case+run.stdout+run.stderr)
                results.append({'case':case,'optimized':o,'expected_accept':expected,'accepted':accepted,'control_pass':True,'error':val.get('error').replace(str(w),'{fixture}') if val.get('error') else None})
    print(json.dumps({'result':'PASS','count':len(results),'controls':results,'scope':'Temporary copies only; frozen source, release and sealed packet remain unchanged.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
