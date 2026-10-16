#!/usr/bin/env python3
"""Root-requested new case-insensitive filesystem regression, disposable only."""
import datetime,hashlib,json,os,subprocess,sys,tempfile,zipfile
from pathlib import Path
W=Path(__file__).resolve().parent;A=W.parents[1];D=A/'preprint_v1_0';K=D/'verification_kit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snap(root):return {p.relative_to(root).as_posix():(p.stat().st_size,sha(p)) for p in root.rglob('*') if p.is_file()}
def main():
    if (W/'SEAL.json').exists():raise RuntimeError('Stage already sealed')
    canonical=snap(K);results=[]
    with tempfile.TemporaryDirectory(prefix='case-alias-scratch-',dir=W) as t:
        S=Path(t)
        with zipfile.ZipFile(D/'verification_kit.zip') as z:z.extractall(S)
        C=S/'verification_kit';alias=S/'VERIFICATION_KIT'
        if not alias.samefile(C):raise RuntimeError('This filesystem does not expose the required physical same-directory case alias')
        initial=snap(C)
        for optimized in [False,True]:
            destination=alias/'fresh-case-alias.zip';physical=C/'fresh-case-alias.zip'
            if destination.exists():raise RuntimeError('Fault destination must begin absent')
            argv=[sys.executable,'-I']+(['-O'] if optimized else [])+['build_archive.py','--output',str(destination)]
            run=subprocess.run(argv,cwd=C,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(S)),capture_output=True,text=True)
            accepted=run.returncode==0 and physical.is_file()
            rec={'optimized':optimized,'argv':argv,'cwd':str(C),'physical_directory_samefile':alias.samefile(C),'lexical_alias_outside_root':not destination.is_relative_to(C),'destination_initially_absent':True,'returncode':run.returncode,'stdout':run.stdout,'stderr':run.stderr,'accepted_and_created_physically_inside_kit':accepted}
            if physical.exists():
                rec['created_output']={'bytes':physical.stat().st_size,'sha256':sha(physical)};physical.unlink()
            if snap(C)!=initial:raise RuntimeError('Existing disposable protected input bytes changed')
            rec['all_preexisting_disposable_kit_bytes_unchanged']=True;results.append(rec)
    if snap(K)!=canonical:raise RuntimeError('Canonical candidate mutated')
    finding=all(r['accepted_and_created_physically_inside_kit'] for r in results)
    data={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'REPRODUCED_P3_CASE_ALIAS_OUTPUT_BOUNDARY' if finding else 'CASE_ALIAS_REJECTED_OR_MIXED','guard_file':'preprint_v1_0/verification_kit/verify.py','guard_sha256':sha(K/'verify.py'),'canonical_candidate_unchanged':True,'normal_and_optimized_results':results,'actionable_priority':'P3' if finding else None,'root_integrity_adoption_eligible':not finding,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_at':1032,'scope':'A fresh leaf under an uppercase spelling of the actual physical kit directory bypasses lexical Path containment. Both tests are disposable; no existing canonical or disposable payload is overwritten. Accepted output is an extra archive physically inside the kit.'}
    (W/'CASE_ALIAS_OUTPUT_FINDING.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k!='normal_and_optimized_results'},indent=2))
if __name__=='__main__':main()
