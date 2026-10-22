#!/usr/bin/env python3
"""Run fail-closed corruption tests against a separately trusted verifier copy."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def execute(script, args, mode=0, cwd=None):
    env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE', None)
    command=[sys.executable, '-B']+([] if mode == 0 else ['-O' if mode == 1 else '-OO'])+[str(script), *map(str,args)]
    return subprocess.run(command, cwd=cwd, env=env, capture_output=True, timeout=180)

def repin(root):
    f=root/'PUBLIC_MANIFEST.json'; data=json.loads(f.read_bytes())
    for name in data['files']:
        raw=(root/name).read_bytes();data['files'][name]={'bytes':len(raw),'sha256':digest(raw)}
    raw=(json.dumps(data,indent=2,sort_keys=True)+'\n').encode();f.write_bytes(raw)
    return digest(raw)

def main():
    require(len(sys.argv)==2, 'Supply the external public-manifest SHA-256')
    pin=sys.argv[1]; mode=sys.flags.optimize
    verifier=ROOT/'verify_publication.py'
    baseline=execute(verifier,[pin,ROOT,'--inventory-only'],mode)
    require(baseline.returncode==0, 'Baseline inventory failed: '+baseline.stderr.decode())
    cases=[]
    def trial(name, edit, new_pin=False):
        with tempfile.TemporaryDirectory(prefix='soliton-mutation-') as d:
            root=Path(d)/'packet';shutil.copytree(ROOT,root)
            edit(root)
            used=repin(root) if new_pin else pin
            result=execute(verifier,[used,root,'--inventory-only'],mode)
            require(result.returncode != 0, 'Corruption survived: '+name)
            cases.append({'case':name,'rejected':True,'verifier_actual_optimization':mode})
    trial('delete original proof',lambda r:(r/'release/PARTIAL_RESULTS.md').unlink())
    trial('unexpected root file',lambda r:(r/'EXTRA').write_text('extra'))
    trial('unexpected empty directory',lambda r:(r/'EXTRA_DIR').mkdir())
    trial('original proof byte change',lambda r:(r/'release/PARTIAL_RESULTS.md').write_bytes((r/'release/PARTIAL_RESULTS.md').read_bytes()+b'\n'))
    trial('full audit byte change',lambda r:(r/'audit_release/FULL_AUDIT.md').write_bytes((r/'audit_release/FULL_AUDIT.md').read_bytes()+b'\n'))
    trial('corrected proof byte change',lambda r:(r/'audit_release/PARTIAL_RESULTS.corrected.md').write_bytes((r/'audit_release/PARTIAL_RESULTS.corrected.md').read_bytes()+b'\n'))
    trial('correction patch byte change',lambda r:(r/'audit_release/CORRECTION.patch').write_bytes((r/'audit_release/CORRECTION.patch').read_bytes()+b'\n'))
    def link_file(r):
        f=r/'release/PARTIAL_RESULTS.md';f.unlink();f.symlink_to(ROOT/'release/PARTIAL_RESULTS.md')
    trial('payload symlink',link_file)
    def link_dir(r):
        shutil.rmtree(r/'audit_release');(r/'audit_release').symlink_to(ROOT/'audit_release',target_is_directory=True)
    trial('directory symlink',link_dir)
    trial('outer manifest byte change',lambda r:(r/'PUBLIC_MANIFEST.json').write_bytes((r/'PUBLIC_MANIFEST.json').read_bytes()+b'\n'))
    trial('verifier copy changed',lambda r:(r/'verify_publication.py').write_text('print("PASS")\n'))
    trial('forged original manifest after outer repin',lambda r:(r/'release/AUTHOR_MANIFEST.json').write_bytes((r/'release/AUTHOR_MANIFEST.json').read_bytes()+b'\n'),True)
    trial('forged audit manifest after outer repin',lambda r:(r/'audit_release/AUDIT_MANIFEST.json').write_bytes((r/'audit_release/AUDIT_MANIFEST.json').read_bytes()+b'\n'),True)
    trial('changed replay output after outer repin',lambda r:(r/'release/CHECK_RESULTS.json').write_bytes((r/'release/CHECK_RESULTS.json').read_bytes()+b'\n'),True)
    wrong=execute(verifier,['0'*64,ROOT,'--inventory-only'],mode)
    require(wrong.returncode!=0,'Wrong external pin accepted')
    cases.append({'case':'wrong external anchor','rejected':True,'verifier_actual_optimization':mode})
    direct=[]
    edits=[('release/check_algebra.py','s.diff(logH,c)-g)','s.diff(logH,c)-g-1)'),
           ('audit_release/independent_controls.py','deriv*drift,4*e*b*(c-lam))','deriv*drift,5*e*b*(c-lam))')]
    for name,old,new in edits:
        source=(ROOT/name).read_text();require(source.count(old)==1,'Ambiguous deliberate mathematical mutation')
        with tempfile.TemporaryDirectory(prefix='soliton-algebra-mutation-') as d:
            f=Path(d)/'wrong.py';f.write_text(source.replace(old,new))
            for child_mode in (0,1,2):
                run=execute(f,[],child_mode,cwd=d)
                require(run.returncode!=0 and b'RuntimeError' in run.stderr,'Wrong mathematics survived optimization')
                direct.append({'script':name,'actual_child_optimization':child_mode,'rejected':True})
    print(json.dumps({'status':'PASS','inventory_mutations_rejected':len(cases),
                      'inventory_cases':cases,'direct_mathematical_mutations_rejected':len(direct),
                      'direct_cases':direct,'scope':'Integrity and deliberate finite-algebra corruption controls only.'},indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
