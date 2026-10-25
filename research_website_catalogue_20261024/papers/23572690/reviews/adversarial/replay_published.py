#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent
SRC=HERE.parents[1]/'sources/published-source/bv-generators-source-and-verification'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory():return {str(p.relative_to(SRC)):digest(p) for p in sorted(SRC.rglob('*')) if p.is_file()}
def main():
    before=inventory();started=datetime.now(timezone.utc).isoformat()
    manifest=json.loads((SRC/'source-manifest.json').read_text())
    assert set(before)=={'source-manifest.json'}|{r['path'] for r in manifest['files']}
    for row in manifest['files']:
        p=SRC/row['path'];assert p.stat().st_size==row['bytes'] and digest(p)==row['sha256']
    rows=[]
    with tempfile.TemporaryDirectory(prefix='bv-check-',dir=HERE/'cache') as temp:
        work=Path(temp)/'source';shutil.copytree(SRC,work)
        for mode,options in [('ordinary',[]),('optimized',['-OO'])]:
            cmd=[sys.executable,'-I','-S','-B',*options,str(work/'exact_checks.py')]
            r=subprocess.run(cmd,cwd=work,capture_output=True,timeout=60)
            (HERE/f'replay-{mode}.stdout.txt').write_bytes(r.stdout)
            (HERE/f'replay-{mode}.stderr.txt').write_bytes(r.stderr)
            assert r.returncode==0 and r.stdout==(SRC/'CHECK_RESULTS.json').read_bytes()
            rows.append({'mode':mode,'flags':['-I','-S','-B',*options],'exit_code':r.returncode,
                         'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'byte_identical_to_published_expected':True})
    after=inventory();assert before==after
    out={'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,
         'script_sha256':before['exact_checks.py'],'source':str(SRC),'source_sha256':before,
         'source_files':len(before),'all_source_files_unchanged':True,'runs':rows,
         'scope':'Unmodified isolated published exact-checker replay; no package builder, historical assessment, proof assistant or universal cohomology computation.'}
    (HERE/'replay-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
