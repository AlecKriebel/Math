"""Actual pinned candidate replay on owned copies; retain every failure."""
from pathlib import Path
import datetime, hashlib, json, os, platform, shutil, subprocess, sys, time

HERE = Path(__file__).resolve().parent.parent
ORIGINAL = HERE.parent.parent / 'original/unsolved_math_prioritization/attempts/2616'
BOOT_SHA = '128bfd14af0273eb4bd850ae95be8a0cbe908795c0032c003894809d733575b5'
MANIFEST_SHA = '0bb884f5c4ae98204a5455e78c5c869905457a21021e86040c58e8e2f01a3ab4'
VERIFIER_SHA = 'cff4f5e102973803175b304b3cd472dd6f28d3843eac7bbacac809b1a9bde7de'
MUTATION_SHA = 'bfdce9c386882fdb92840e977a6466fe4c4618d0094429e7651396d574fc9ce6'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok, text):
    if not ok: raise RuntimeError(text)

def main():
    require(sha(ORIGINAL/'BOOTSTRAP.py') == BOOT_SHA, 'bootstrap external authentication')
    require(sha(ORIGINAL/'PUBLICATION_MANIFEST.json') == MANIFEST_SHA, 'manifest external authentication')
    require(sha(ORIGINAL/'verify_publication.py') == VERIFIER_SHA, 'verifier external authentication')
    require(sha(ORIGINAL/'mutation_tests.py') == MUTATION_SHA, 'mutation external authentication')
    packet = HERE/'fixtures/replay_packet'
    shutil.copytree(ORIGINAL, packet)
    env = dict(os.environ)
    env.update(TMPDIR=str(HERE/'tmp'), TMP=str(HERE/'tmp'), TEMP=str(HERE/'tmp'),
               PYTHONDONTWRITEBYTECODE='1')
    interpreter = sys.executable
    receipts = []
    def run(label, args, timeout=300):
        command = [interpreter, '-I', '-S', '-B', *args]
        started = datetime.datetime.now(datetime.timezone.utc).isoformat()
        t = time.monotonic()
        try:
            p = subprocess.run(command, cwd=HERE, env=env, capture_output=True, timeout=timeout)
            rc, stdout, stderr = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired as e:
            rc, stdout, stderr = 'TIMEOUT', e.stdout or b'', e.stderr or b''
        entry = dict(label=label, launch_utc=started, elapsed_seconds=time.monotonic()-t,
                     command=command, cwd=str(HERE), returncode=rc,
                     stdout=stdout.decode(errors='replace'), stderr=stderr.decode(errors='replace'),
                     status='REPRODUCED' if rc == 0 else 'NOT_REPRODUCED')
        receipts.append(entry)
        (HERE/'receipts/actual_reproduction.json').write_text(json.dumps(dict(
            host=dict(uid=os.getuid(), euid=os.geteuid(), interpreter=interpreter,
                      python=sys.version, platform=platform.platform(), optimization=sys.flags.optimize),
            temp_environment={k:env[k] for k in ('TMPDIR','TMP','TEMP')},
            historical_python_3_12_14_uid1000='NOT_REPRODUCED: unavailable historical runtime/account; actual host preserved',
            commands=receipts), indent=2)+'\n')
        print(json.dumps({k:entry[k] for k in ('label','launch_utc','elapsed_seconds','returncode','status')}) , flush=True)
    for label, mode in [('normal', []), ('O', ['-O']), ('OO', ['-OO'])]:
        run('BOOTSTRAP_'+label, [*mode, str(packet/'BOOTSTRAP.py'), str(packet)])
    for label, mode in [('normal', []), ('O', ['-O']), ('OO', ['-OO'])]:
        run('MUTATION_'+label, [*mode, str(packet/'mutation_tests.py'), '--root', str(packet), '--bootstrap-sha256', BOOT_SHA])
    require(all(sha(packet/p.relative_to(ORIGINAL)) == sha(p) for p in ORIGINAL.rglob('*') if p.is_file()), 'Owned replay copy changed')

if __name__ == '__main__': main()
