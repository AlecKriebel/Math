"""ROOT installs exact already-read source copies, without running any role."""
from pathlib import Path
import hashlib, json, os, stat, datetime

A = Path(__file__).absolute().parent
P = A / 'post_push_foreign_epoch_preparation_v5'
R = A.parents[2]

def sha(b): return hashlib.sha256(b).hexdigest()
def regular(p, mode):
    assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
    assert stat.S_IMODE(p.stat().st_mode) == mode
    return p.read_bytes()

def main():
    assert __debug__ and stat.S_IMODE(A.stat().st_mode) == 0o755
    assert sha(regular(P / 'SOURCE_MANIFEST.json', 0o444)) == '7d6c549ddd7a3d65a0f329e4d1e550a2b91a9c51b09fb1a7291d8e25e0920fda'
    V = A / 'corrective_source_adversary_v5'
    assert sha(regular(V / 'SELF_MANIFEST.json', 0o444)) == '1ae1a446fcb55a8311f27700bb75ff5f2ee93a4ee491063cf404dd186944531d'
    assert sha(regular(V / 'VERDICT.json', 0o444)) == '239d3b8944c064cce99b11c6e4b593a0372bead8127017ad242d31cf3413a1cb'
    copies = {}
    for name, digest in [
        ('author_post_push_foreign_epoch_v5.py', 'e396740d8fca9b6793f36bac0f9e941f6564ad6e2a145de783978df64444965f'),
        ('execute_post_push_foreign_epoch_phase_v5.py', 'd1cd7bfda4cec402b08fda5fb1d6130514b8c1f2b918acea7833bf388d0bf61c'),
        ('run_post_push_foreign_epoch_phase_v5.py', 'b33287188a949bfbd8721c36fab0240b8a4c9870ad8a9bedb98cc6e5c06d3f8a'),
        ('inspect_complete_actual_post_epoch_v5.py', 'ad0bf843b7a81201a47fe6abca326334d17dacd5bb960259ea2077b8401846e9'),
    ]:
        b = regular(P / name, 0o444); assert sha(b) == digest
        copies[name] = b
    copies['ROOT_POST_EPOCH_V5_INSPECTION_PRELAUNCH_SOURCE.py'] = copies['inspect_complete_actual_post_epoch_v5.py']
    b = regular(A.parent / 'pr45_9900007' / 'capture_root_command.py', 0o644)
    assert len(b) == 2593 and sha(b) == 'c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec'
    copies['capture_root_command.py'] = b
    for name in copies:
        assert not (A / name).exists() and not (A / name).is_symlink()
    os.umask(0o022)
    rows = []
    for name, body in copies.items():
        q = A / name
        with q.open('xb') as f:
            f.write(body); f.flush(); os.fsync(f.fileno())
        assert regular(q, 0o644) == body
        rows.append(dict(path=q.relative_to(R).as_posix(), bytes=len(body), sha256=sha(body), full_mode=0o644))
    print(json.dumps(dict(status='PASS_EXACT_ROOT_V5_SOURCE_INSTALL_ONLY', actual_pid=os.getpid(),
        utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), files=rows,
        candidate_SOURCE_or_prior_evidence_modified=False, role_or_native_or_Git_or_remote_executed=False), indent=2))

if __name__ == '__main__': main()
