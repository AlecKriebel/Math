"""Own audit controls. This file is outside the sealed report bundle."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

D = Path(__file__).resolve().parent
P = D/'sealed'
M = 'a2806da4b642a30c304e78aac91b986375e98ea837c5fc97cfca6a3112eb0e4a'
L = '91cee94a55310b98734c3a7b82bc2a719d3ebfd06c5eaf388e69ba9807461bbc'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check(ok, why):
    if not ok:
        raise RuntimeError(why)


check(sha(P/'MANIFEST.json') == M, 'external manifest prehash')
check(sha(P/'verify_bundle.py') == L, 'external launcher prehash')
rows = []
with tempfile.TemporaryDirectory(prefix='closed controls ', dir=D/'excluded_scratch') as temporary:
    T = Path(temporary)
    hostile = T/'hostile cwd'
    hostile.mkdir()
    marker = T/'MUST_NOT_EXECUTE'
    payload = "from pathlib import Path\nPath("+repr(str(marker))+").write_text('BAD')\n"
    for name in ('json.py', 'sitecustomize.py', 'usercustomize.py'):
        (hostile/name).write_text(payload)
    startup = hostile/'startup.py'
    startup.write_text(payload)
    env = dict(os.environ, PYTHONPATH=str(hostile), PYTHONSTARTUP=str(startup))

    def run(label, root=P, optimized=False, expected=True):
        launcher = root/'verify_bundle.py'
        # This is the real pre-execution trust boundary, independent of self-check.
        if launcher.is_symlink() or sha(launcher) != L:
            passed = False
            result = 'rejected by external launcher prehash'
        else:
            args = [sys.executable, '-I', '-S', '-B']
            if optimized:
                args.append('-O')
            args += [str(launcher), str(root), M, L]
            proc = subprocess.run(args, cwd=hostile, env=env, capture_output=True, text=True)
            passed = proc.returncode == 0
            result = json.loads(proc.stdout) if passed else proc.stdout+proc.stderr
        check(passed == expected, label+' unexpected result '+str(result))
        check(not marker.exists(), label+' ran hostile payload')
        rows.append({'control':label,'expected_accept':expected,'actual_accept':passed,'pass':True})
        return result

    normal = run('normal isolated hostile cwd/import environment')
    optimized = run('optimized isolated hostile cwd/import environment', optimized=True)
    check(normal == optimized, 'normal/optimized output equivalence')
    relocated = T/'relocated bundle with spaces'
    shutil.copytree(P, relocated)
    run('relocated spaces normal', relocated)
    run('relocated spaces optimized', relocated, optimized=True)

    def damaged(label, edit):
        root = T/label
        shutil.copytree(P, root)
        edit(root)
        run(label, root, expected=False)

    damaged('changed report', lambda r:(r/'REPORT.md').write_text('changed'))
    damaged('changed finite checker payload', lambda r:(r/'finite_check.py').write_text(payload))
    damaged('extra file', lambda r:(r/'EXTRA').write_text('extra'))
    damaged('missing file', lambda r:(r/'CLAIMS.json').unlink())
    damaged('changed manifest', lambda r:(r/'MANIFEST.json').write_text('{}'))
    damaged('changed launcher externally rejected', lambda r:(r/'verify_bundle.py').write_text(payload))

    def member_link(r):
        p=r/'REPORT.md'
        p.unlink()
        p.symlink_to(P/'REPORT.md')
    damaged('symlink member', member_link)

    def manifest_link(r):
        p=r/'MANIFEST.json'
        p.unlink()
        p.symlink_to(P/'MANIFEST.json')
    damaged('symlink manifest', manifest_link)
    alias=T/'symlink root'
    alias.symlink_to(P, target_is_directory=True)
    run('symlink root',alias,expected=False)
    check(not marker.exists(), 'no hostile execution')

receipt={'schema':'cm-hodge-audit-control-receipt-v1',
 'timestamp_utc':datetime.now(timezone.utc).isoformat(),
 'completion_estimate_percent':100,'manifest_sha256':M,'launcher_sha256':L,
 'closed_authored_members':8,'controls':rows,'normal_optimized_equal':True,
 'hostile_payload_executed':False,'finite_result':normal['finite'],
 'geometric_proof_formalized':False,'source_bodies_excluded':True,
 'trust_boundary':'Externally pinned trusted Python/stdlib; no concurrent filesystem replacement.'}
(D/'VALIDATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
with (D/'research_log.md').open('a') as out:
    out.write('- '+receipt['timestamp_utc']+': Sealed bundle passes all '+str(len(rows))+
              ' normal/optimized/relocation/tamper controls; no hostile payload executed. Completion estimate: 100% of assigned CM/Hodge audit. Sealed report log remains frozen at its pre-control checkpoint; this completion receipt is external.\n')
print(json.dumps({'result':'PASS','controls':len(rows),'manifest_sha256':M,'launcher_sha256':L},sort_keys=True))
