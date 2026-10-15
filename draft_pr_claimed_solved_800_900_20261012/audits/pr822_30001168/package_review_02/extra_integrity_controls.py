#!/usr/bin/env python3
"""Review-owned input-binding attacks on the portable gate and published builder."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys, tempfile

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
ASSEMBLY=AUDIT.parents[1]/'work/pr822_revision_r2'
PIN='b3ac480b710b4a2a6ac8fb438b09697357e0796fe879d614afb54429c10aa374'

def need(ok,label):
    if not ok:raise RuntimeError(label)

def main():
    records=[]
    source=ASSEMBLY/'publication_20261013/verification_package'
    builder=ASSEMBLY/'publication_20261013/preprint/build_verification.py'
    with tempfile.TemporaryDirectory(dir=HERE/'private_sources',prefix='independent integrity attacks with spaces ') as td:
        base=Path(td)
        for opt in (False,True):
            flags=['-I','-B']+(['-O'] if opt else [])
            for label in ['portable extra empty directory','portable same-size paper corruption','portable symlink','portable wrong external pin','builder wrong pin','builder unbound verifier','builder output inside input','builder nonempty output']:
                case=base/str(len(records));case.mkdir()
                pack=case/'input package with spaces';shutil.copytree(source,pack)
                pin=PIN; output=case/'fresh output'
                if label=='portable extra empty directory':(pack/'unexpected').mkdir()
                if label=='portable same-size paper corruption':
                    p=pack/'note.tex';b=p.read_bytes();p.write_bytes(b'!'+b[1:])
                if label=='portable symlink':
                    p=pack/'note.tex';p.unlink();p.symlink_to(source/'note.tex')
                if label in ('portable wrong external pin','builder wrong pin'):pin='0'*64
                if label=='builder unbound verifier':
                    with (pack/'verify_package.py').open('a') as f:f.write('\nraise RuntimeError("EXECUTED_UNBOUND_CHECKER")\n')
                if label=='builder output inside input':output=pack/'new output'
                if label=='builder nonempty output':
                    output.mkdir();(output/'sentinel').write_text('preserve me')
                if label.startswith('portable'):
                    command=[sys.executable,*flags,str(pack/'verify_package.py'),pin]
                    expected='external index pin' if 'pin' in label else ('nonregular member' if 'symlink' in label else ('digest: note.tex' if 'corruption' in label else 'closed inventory'))
                else:
                    command=[sys.executable,*flags,str(builder),'--from-package',str(pack),'--trusted-index-sha256',pin,'--output-root',str(output)]
                    expected={'builder wrong pin':'external input index pin mismatch','builder unbound verifier':'trusted input verifier binding failed','builder output inside input':'outside the intact input package','builder nonempty output':'fresh or empty directory'}[label]
                before={str(p.relative_to(case)):hashlib.sha256(p.read_bytes()).hexdigest() for p in case.rglob('*') if p.is_file()}
                p=subprocess.run(command,cwd='/',capture_output=True,text=True,timeout=90)
                need(p.returncode!=0 and expected in p.stderr,'expected failure '+label+' '+p.stderr)
                after={str(p.relative_to(case)):hashlib.sha256(p.read_bytes()).hexdigest() for p in case.rglob('*') if p.is_file()}
                need(before==after,'negative control wrote input/output '+label)
                records.append({'case':label,'optimized':opt,'accepted':False,'expected_diagnostic':expected,'returncode':p.returncode,'stderr':p.stderr,'before_after_file_hashes_equal':True,'command':command})
                shutil.rmtree(case)
    result={'status':'PASS','expected_rejections':len(records),'cases':records,'mutation_scope':'disposable review copies only'}
    (HERE/'EXTRA_INTEGRITY_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','expected_rejections':len(records)}))

if __name__=='__main__':main()
