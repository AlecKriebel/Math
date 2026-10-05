#!/usr/bin/env python3
"""Replay the exact author freeze and adversarial controls in disposable copies.
Usage: python3 replay_author.py PATH_TO_AUTHOR_SAFE_FREEZE.zip [--write]
No author input file is modified. Requires mpmath for the author's controls.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile

EXPECTED_SHA='63b3aee3a0e44e17b4ed2fc3d01065708f87dd3dd7e5fee397e85683c1a300e1'
EXPECTED_SIZE=24951
FILES={'CHECK_RESULTS.json','LIMITATIONS.md','MANIFEST.json','PRIOR_WORK_CHECK.json',
       'PROOFS.md','README.md','RESEARCH_LOG.md','SOURCE_VERIFICATION.json',
       'verify_manifest.py','verify_math.py'}
HERE=Path(__file__).resolve().parent


def require(ok,msg):
    if not ok:
        raise RuntimeError(msg)


def replay(path):
    data=path.read_bytes()
    require(len(data)==EXPECTED_SIZE and hashlib.sha256(data).hexdigest()==EXPECTED_SHA,
            'The supplied author freeze is not the reviewed input')
    rows=[]
    with tempfile.TemporaryDirectory(prefix='aleksandrov-audit-') as temp:
        root=Path(temp);author=root/'author';author.mkdir()
        with zipfile.ZipFile(path) as z:
            require(set(z.namelist())==FILES and len(z.namelist())==len(FILES),'Unexpected ZIP members')
            for name in z.namelist():
                require(Path(name).name==name,'Unsafe ZIP path')
                (author/name).write_bytes(z.read(name))
        for optimized in [False,True]:
            flags=['-O'] if optimized else []
            for script in ['verify_manifest.py','verify_math.py']:
                p=subprocess.run([sys.executable,*flags,script],cwd=author,
                                 capture_output=True,text=True)
                require(p.returncode==0,'Clean author replay failed: '+p.stderr)
                rows.append({'mode':'optimized' if optimized else 'normal',
                             'case':'clean','script':script,'exit_code':p.returncode})
            for kind in ['proof_bytes','missing_file','extra_file','saved_result']:
                target=root/('case_'+kind+str(optimized));shutil.copytree(author,target)
                script='verify_manifest.py'
                if kind=='proof_bytes':
                    p=target/'PROOFS.md';p.write_bytes(p.read_bytes()+b'\ncorruption\n')
                elif kind=='missing_file':
                    (target/'LIMITATIONS.md').unlink()
                elif kind=='extra_file':
                    (target/'unexpected.txt').write_text('unexpected extra file')
                else:
                    p=target/'CHECK_RESULTS.json';j=json.loads(p.read_text());j['status']='FAIL'
                    p.write_text(json.dumps(j,indent=2,sort_keys=True)+'\n');script='verify_math.py'
                p=subprocess.run([sys.executable,*flags,script],cwd=target,
                                 capture_output=True,text=True)
                require(p.returncode!=0,'Tamper control escaped: '+kind)
                rows.append({'mode':'optimized' if optimized else 'normal',
                             'case':kind,'script':script,'rejected':True})
    require(path.read_bytes()==data,'Author freeze changed during replay')
    return {'schema':'author-freeze-adversarial-replay-v1','status':'PASS',
            'author_zip_bytes':len(data),'author_zip_sha256':EXPECTED_SHA,
            'cases':rows,'author_input_unchanged':True,
            'mathematical_proof_not_certified_by_tests':True}


if __name__=='__main__':
    require(len(sys.argv) in [2,3] and (len(sys.argv)==2 or sys.argv[2]=='--write'),
            'Usage: replay_author.py PATH_TO_AUTHOR_SAFE_FREEZE.zip [--write]')
    result=json.dumps(replay(Path(sys.argv[1]).resolve()),indent=2,sort_keys=True)+'\n'
    if len(sys.argv)==3:
        (HERE/'REPLAY_RESULTS.json').write_text(result)
    else:
        require((HERE/'REPLAY_RESULTS.json').read_text()==result,'Replay receipt differs')
    print('PASS: exact author archive, clean replays and tamper controls; archive unchanged')
