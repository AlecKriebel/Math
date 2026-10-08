#!/usr/bin/env python3
"""Replay the narrow ledger semantic correction on disposable packet copies."""
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
OLD={'manifest':'4a68c2510b717b1e6e4afcf267fdc0b40bf97a8156eab1c4c44c51f65e7410da','verifier':'7fb843326a441b6898836dc50b59fea41a6c9bf071352ad3470008a76f84e469','bootstrap':'b79a21252ad5d12e5cf44bed4543578d15226f15ed12c2d2594fa79697e9a950'}
NEW={'manifest':'af6631e1537a26720df4234f41974a8de54185e5bd625bc24d6997f3174c1958','verifier':'5603afacfc7d8754eb5a94b61097863b01776dcca023210e46e6e96090695945','bootstrap':'714afb752a56c50c447f778a2ffbf301b5c5f28b4fd99b54a1768151e5863304'}
def need(x,message):
    if not x:raise ValueError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snap(base):return {str(p.relative_to(base)):(sha(p),p.stat().st_mode&0o777) for folder in ['packet','freeze'] for p in sorted((base/folder).iterdir())}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('revision2');ap.add_argument('corrected');args=ap.parse_args()
    need(sys.flags.isolated==1 and os.geteuid()!=0,'isolated nonroot audit required')
    roots=[Path(args.revision2).resolve(),Path(args.corrected).resolve()];pins=[OLD,NEW];before=[snap(p) for p in roots]
    for base,pin in zip(roots,pins):
        need(sha(base/'freeze/FREEZE_MANIFEST.json')==pin['manifest'],'manifest pin')
        need(sha(base/'packet/verify.py')==pin['verifier'],'verifier pin')
        need(sha(base/'freeze/bootstrap.py')==pin['bootstrap'],'bootstrap pin')
    same=[p.name for p in (roots[0]/'packet').iterdir() if p.name!='verify.py']
    need(all((roots[0]/'packet'/n).read_bytes()==(roots[1]/'packet'/n).read_bytes() for n in same),'unrelated packet bytes changed')
    cases=[('boolean approach turn',lambda x:x['approaches'][0].__setitem__('turn',True)),('floating approach turn',lambda x:x['approaches'][0].__setitem__('turn',1.0))]
    for key in ['source_lookup_proof_turns','duplicate_gate_proof_turns','audit_packaging_proof_turns']:
        for value,label in [(False,'boolean zero'),(0.0,'floating zero'),(1,'nonzero'),(None,'null')]:
            cases.append((key+' '+label,lambda x,k=key,v=value:x.__setitem__(k,v)))
    results=[]
    for flags in [[],['-O'],['-OO']]:
        for name,mutate in cases:
            outcomes=[]
            for which,(base,pin) in enumerate(zip(roots,pins)):
                with tempfile.TemporaryDirectory(prefix='cycle-ledger-correction-') as td:
                    d=Path(td)
                    for folder in ['packet','freeze']:
                        shutil.copytree(base/folder,d/folder);(d/folder).chmod(0o755)
                        for p in (d/folder).iterdir():p.chmod(0o644)
                    p=d/'packet/LEDGER.json';ledger=json.loads(p.read_bytes());mutate(ledger);p.write_text(json.dumps(ledger))
                    mf=d/'freeze/FREEZE_MANIFEST.json';m=json.loads(mf.read_bytes());m['files']['LEDGER.json']={'bytes':p.stat().st_size,'sha256':sha(p)};mf.write_text(json.dumps(m))
                    cmd=[sys.executable,'-I','-B',*flags,str(base/'packet/verify.py'),'--packet',str(d/'packet'),'--manifest',str(mf),'--manifest-sha256',sha(mf)]
                    r=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
                    need((r.returncode==0)==(which==0),'unexpected old/new semantic outcome: '+name)
                    boot=subprocess.run([sys.executable,'-I','-B',*flags,str(d/'freeze/bootstrap.py'),str(d/'packet')],capture_output=True,text=True,timeout=30)
                    need(boot.returncode!=0,'fixed bootstrap accepted mutated manifest')
                    outcomes.append({'slice':'revision2' if which==0 else 'corrected','direct_accepts':r.returncode==0,'fixed_bootstrap_rejects':True})
            results.append({'case':name,'optimize':2 if flags==['-OO'] else 1 if flags else 0,'outcomes':outcomes})
    need([snap(p) for p in roots]==before,'frozen input changed')
    print(json.dumps({'schema':'erdos-cycle-sets-ledger-correction-controls-v1','uid':os.geteuid(),'case_count':len(cases),'old_new_pairs':len(results),'old_direct_acceptances':len(results),'corrected_direct_rejections':len(results),'fixed_bootstrap_rejections':2*len(results),'unchanged_nonverifier_files':sorted(same),'frozen_bytes_and_modes_unchanged':True,'results':results},indent=2))
if __name__=='__main__':main()
