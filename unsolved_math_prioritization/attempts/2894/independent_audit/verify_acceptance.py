#!/usr/bin/env python3
"""Pinned exact-artifact acceptance replay. This does not certify mathematical theorems."""
import hashlib,json,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path
PINS={
 'AUTHOR':('FOUR_MANIFOLD_SIMPLE_2894_AUTHOR_EXTERNAL_MANIFEST.json','224df160047e5e01f24127fcf2bccee3add613fa1b0dee08235b1664f7983e7a','FOUR_MANIFOLD_SIMPLE_2894_AUTHOR_SAFE_FREEZE.zip','2a89bece1a2e10133910bc3fcde5a604e9e41de2ea50620d290be71ad864a9d4',10990),
 'CORRECTED':('FOUR_MANIFOLD_SIMPLE_2894_CORRECTED_EXTERNAL_MANIFEST.json','2aefce4fc9c27e800a14249e8c1ff132f8bff1bc0c65ec1f480fa2a31fe2bd26','FOUR_MANIFOLD_SIMPLE_2894_CORRECTED_SAFE.zip','407d0d67f37d548eaa55e1cf85455ad218e123d56a4880791a78c5bd8ca912de',11662)
}
EXPECTED={'README.md','REPORT.md','PROOF.md','status.json','sources.json','verification_metadata.json','research_log.json','verify_packet.py'}
def require(ok,msg):
    if not ok: raise ValueError(msg)
def h(b): return hashlib.sha256(b).hexdigest()
def main():
    require(len(sys.argv)<=2,'Usage: verify_acceptance.py [AUDIT_DIRECTORY]')
    root=Path(sys.argv[1]) if len(sys.argv)==2 else Path(__file__).resolve().parent
    require(root.is_dir() and not root.is_symlink(),'Invalid audit root')
    results=[]
    for label,(mn,mh,zn,zh,sz) in PINS.items():
        mp=root/mn; zp=root/zn
        require(mp.is_file() and not mp.is_symlink(),'Invalid manifest')
        require(h(mp.read_bytes())==mh,'Pinned external manifest mismatch: '+label)
        m=json.loads(mp.read_text())
        require(zp.is_file() and not zp.is_symlink(),'Invalid archive')
        require(zp.stat().st_size==sz and h(zp.read_bytes())==zh,'Pinned ZIP mismatch: '+label)
        require(m['zip']['sha256']==zh and m['zip']['bytes']==sz,'Manifest archive contradiction')
        with tempfile.TemporaryDirectory(prefix='four manifold acceptance ') as td:
            packet=Path(td)/'packet'; packet.mkdir()
            with zipfile.ZipFile(zp) as z:
                entries=z.infolist(); names=[e.filename for e in entries]
                require(len(names)==len(set(names)) and set(names)==EXPECTED,'Unsafe archive inventory')
                for e in entries:
                    require(not e.is_dir() and stat.S_IFMT(e.external_attr>>16) in (0,stat.S_IFREG),'Unsafe archive member type')
                    (packet/e.filename).write_bytes(z.read(e))
            require({i['path'] for i in m['files']}==EXPECTED and len(m['files'])==8,'Manifest inventory mismatch')
            for item in m['files']:
                b=(packet/item['path']).read_bytes(); require(len(b)==item['bytes'] and h(b)==item['sha256'],'Member binding mismatch')
            s=json.loads((packet/'status.json').read_text())
            if label=='CORRECTED':
                require(s['disposition']=='unsolved' and s['queue_status']=='unsolved','Canonical status mismatch')
                require(s['full_problem_solved'] is False and s['new_solution_claimed'] is False,'Unsupported claim')
            for optimized in (False,True):
                cp=subprocess.run([sys.executable]+(['-O'] if optimized else [])+[str(packet/'verify_packet.py'),str(packet),str(mp.resolve()),str(zp.resolve())],capture_output=True,text=True,timeout=30)
                require(cp.returncode==0,'Bound packet verifier failed: '+label)
                r=json.loads(cp.stdout); require(r['zip_verified'] is True and r['mathematical_theorems_verified_by_code'] is False,'Verifier scope mismatch')
                results.append({'packet':label,'optimized':optimized,'passed':True})
    print(json.dumps({'result':'pass','canonical_status':'unsolved','turns':'1/5','part_a':'accepted_cited_theorem_implication','part_b':'unresolved','replays':results,'mathematical_theorems_certified':False},sort_keys=True))
if __name__=='__main__':
    try: main()
    except Exception as exc:
        print(json.dumps({'result':'fail','error':str(exc)},sort_keys=True),file=sys.stderr); sys.exit(1)
