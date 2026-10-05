"""Derive proposed helpers from the already ROOT-read1745 sources; execute no Git."""
from pathlib import Path
import difflib, hashlib, json, os, stat, datetime

N = Path(__file__).absolute().parent
O = N.parent / 'checkpoint_20261003_1745_preparation'
PINS = {
    'common.py': '08b22ced8b2174a334dc7f1191cfa5c28ddfb5dc18394c925678c736a312510f',
    'stage_checkpoint.py': '341849d4929099fb72f21a133db331f66e3e88386ced9c5e5c8d816c08e99bf1',
    'commit_checkpoint.py': 'fbc243a694ccc6f19231eb6cab7317d96b460e38f3cd4aa7d4ff01891c864424',
    'capture_source.py': 'dfe2ffc94b006eb8e0d164ba884f773ed68dde09df51ac1bbb2842448d2f041a',
}

def put(q, b):
    with q.open('xb') as f:
        f.write(b); f.flush(); os.fsync(f.fileno())

def replace(s, a, b):
    assert s.count(a) == 1, (a, s.count(a))
    return s.replace(a, b)

def main():
    assert __debug__ and N.name == 'checkpoint_20261003_1915_preparation'
    inputs, outputs, diffs = [], [], []
    for name, sha in PINS.items():
        f = O / name; b = f.read_bytes(); before = f.stat()
        assert not f.is_symlink() and hashlib.sha256(b).hexdigest() == sha
        s = b.decode()
        if name == 'common.py':
            s = replace(s, 'checkpoint_20261003_1745_preparation', 'checkpoint_20261003_1915_preparation')
        elif name == 'stage_checkpoint.py':
            s = replace(s, 'Checkpoint 20261003_1745 SOURCE reviewed by ROOT at ', 'Checkpoint 20261003_1915 SOURCE reviewed by ROOT at ')
        elif name == 'commit_checkpoint.py':
            s = replace(s, 'Checkpoint completed PR48 and PR57-60 research evidence', 'Checkpoint completed PR48 V6 and PR60-61 research evidence')
            s = replace(s, 'Prepared formal accepted snapshot37/180 (20.5556%). The PR57 preprint package remains unpublished.',
                        'Prepared formal accepted snapshot37/180 (20.5556%). Partial inventory38 is not completed acceptance; failed PR48 finalization is retained.')
        else:
            s = replace(s, "choices=['inventory_draft.py','build_scope.py','verify_source.py','read_source.py']",
                        "choices=['build_scope.py','verify_source.py','read_source.py']")
            s = replace(s, "q = N.parent / 'checkpoint_20261003_1745_preparation_readback_actual_capture'",
                        "q = N / 'actual_source_readback_capture'")
        out = s.encode(); put(N/name, out)
        inputs.append(dict(path=str(f), bytes=len(b), sha256=sha, full_mode=stat.S_IMODE(before.st_mode)))
        outputs.append(dict(name=name, bytes=len(out), sha256=hashlib.sha256(out).hexdigest(), full_mode=stat.S_IMODE((N/name).stat().st_mode)))
        diffs += list(difflib.unified_diff(b.decode().splitlines(True), s.splitlines(True), fromfile='1745/'+name, tofile='1915/'+name))
    put(N/'DERIVATION.diff', ''.join(diffs).encode())
    record = dict(schema='checkpoint1915-explicit-helper-derivation/v1', actual_pid=os.getpid(),
                  utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), inputs=inputs, outputs=outputs,
                  changes='Literal dedicated location, dated ROOT marker, commit prose; capture administrative allowlist and own-directory readback destination only.',
                  Git_or_native_or_production_helper_execution=False, ROOT_read_of_1915_not_claimed=True,
                  inherited_guards_unchanged=['private index','literal NUL path domain','foreign index entries/full flags/staged object IDs/worktree bytes/full modes','real-index lock','exact-parent CAS','disk preflight','failure receipts'])
    put(N/'DERIVATION.json', (json.dumps(record, indent=2, sort_keys=True)+'\n').encode())
    print(json.dumps(dict(status='SOURCE_HELPERS_DERIVED_ONLY', actual_pid=os.getpid(), files=list(PINS), bytes=sum(z['bytes'] for z in outputs))))

if __name__ == '__main__': main()
