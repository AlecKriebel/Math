"""ROOT installs five exact personally reviewed V6 copies; no role execution."""
from pathlib import Path
import hashlib, json, os, stat, datetime

A = Path(__file__).absolute().parent
P = A / 'post_push_foreign_epoch_preparation_v6'
R = A.parents[2]

def sha(b): return hashlib.sha256(b).hexdigest()
def regular(p, mode):
    assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
    assert stat.S_IMODE(p.stat().st_mode) == mode
    return p.read_bytes()

def main():
    assert __debug__ and stat.S_IMODE(A.stat().st_mode) == 0o755
    assert sha(regular(P / 'SOURCE_READY.json', 0o444)) == 'c41aa5d82d4b6240ea496b180d6b73fbff09d02574942c4741cadd5c80b19e26'
    assert sha(regular(P / 'SOURCE_MANIFEST.json', 0o444)) == 'aea1b2933d03cc7c20bad7341e11d0dc5e675949810c34eb051707f0c43bc159'
    V = A / 'corrective_source_adversary_v6'
    assert sha(regular(V / 'SELF_MANIFEST.json', 0o444)) == '540d17325a78233ffc6dc0e287aea660defdb63a50b2782989cafdc6414f776f'
    assert sha(regular(V / 'VERDICT.json', 0o444)) == 'ca9dfc36e91cff5f59ad17707228e647b409bb15b205bb736a465ee629f8512c'
    assert json.loads(regular(V / 'VERDICT.json', 0o444))['mandatory_findings'] == []
    assert len(regular(A / 'capture_root_command.py', 0o644)) == 2593
    assert sha(regular(A / 'capture_root_command.py', 0o644)) == 'c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec'
    copies = {}
    for name, digest in [
        ('author_post_push_foreign_epoch_v6.py', '522a96387ad6a4a670cb1b45ec23b1f67f8c5009281c554e60b0567516a67a65'),
        ('execute_post_push_foreign_epoch_phase_v6.py', '180c4e2c2546340d665288a83f65199e3dd98c452ac1fb28986d182eabf842b8'),
        ('run_post_push_foreign_epoch_phase_v6.py', '31da8103c5da9ddf00cb8aa19f2cc11184e372f5ae0cc734d7b665b51f8402e4'),
        ('inspect_complete_actual_post_epoch_v6.py', '9f6665375efc01a415cbc028300fe581a6c807dd58f8bf97e97e12b8790de33a'),
    ]:
        body = regular(P / name, 0o444)
        assert sha(body) == digest
        copies[name] = body
    copies['ROOT_POST_EPOCH_V6_INSPECTION_PRELAUNCH_SOURCE.py'] = copies['inspect_complete_actual_post_epoch_v6.py']
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
    print(json.dumps(dict(status='PASS_EXACT_ROOT_V6_SOURCE_INSTALL_ONLY', actual_pid=os.getpid(),
        utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), files=rows,
        existing_ROOT_operator_reused_unchanged=True,
        candidate_SOURCE_or_prior_evidence_modified=False, role_or_native_or_Git_or_remote_executed=False), indent=2))

if __name__ == '__main__': main()
