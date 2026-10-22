"""Replay four baselines and targeted file/identity/convention gate controls."""
import argparse, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path

def sha(b):
    return hashlib.sha256(b).hexdigest()

def run(a):
    W = Path(a.packet).absolute()
    D = Path(a.scratch).absolute()
    D.mkdir(parents=True, exist_ok=False)
    MF = sha((W / 'MANIFEST.json').read_bytes())
    CP = sha((W / 'verify_packet.py').read_bytes())
    mf = json.loads((W / 'MANIFEST.json').read_text())

    def clone(name):
        p = D / name
        p.mkdir()
        for row in mf['files']:
            rel = row['path']
            d = p / rel
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(W / rel, d)
        shutil.copyfile(W / 'MANIFEST.json', p / 'MANIFEST.json')
        return p

    def command(p, python=sys.executable, opt=False, mfpin=MF, cppin=CP, ir=None, sr=None, entry=None):
        cmd = [python, '-I', '-B'] + (['-O'] if opt else []) + [str(entry or p / 'verify_packet.py'), '--packet-root', str(p), '--expected-manifest-sha256', mfpin, '--expected-checker-sha256', cppin]
        if ir:
            cmd += ['--input-root', str(ir)]
        if sr:
            cmd += ['--source-root', str(sr)]
        cmd += ['--replay']
        return subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=90)
    positives = []
    negatives = []
    relocated = clone('relocated packet with spaces')
    for py in [sys.executable, a.other_python]:
        for opt in [False, True]:
            r = command(relocated, python=py, opt=opt, ir=a.input_root, sr=a.source_root)
            if r.returncode:
                raise RuntimeError(r.stdout + r.stderr)
            out = json.loads(r.stdout)
            if not (out['result'] == 'PASS' and out['bound_inputs_checked'] == 62 and (out['primary_files_checked'] == 20) and out['diagnostics_replayed']):
                raise AssertionError('exact diagnostic failed')
            positives.append({'mode': 'optimized' if opt else 'normal', 'interpreter': 'primary' if py == sys.executable else 'secondary', 'result': 'PASS', 'bound_inputs': 62, 'primary_files': 20})

    def bad(name, p=None, **kwargs):
        r = command(p or W, **kwargs)
        if r.returncode == 0:
            raise AssertionError('negative accepted: ' + name)
        negatives.append({'name': name, 'result': 'REJECTED'})
    bad('wrong-external-manifest-pin', mfpin='0' * 64)
    bad('wrong-external-checker-pin', cppin='0' * 64)
    p = clone('alter-report')
    f = p / 'CANDIDATE_COMPARISON.md'
    f.write_text(f.read_text() + '\nmutated\n')
    bad('changed-authored-report', p)
    p = clone('extra-file')
    (p / 'EXTRA').write_text('x')
    bad('unexpected-file', p)
    p = clone('empty-dir')
    (p / 'empty').mkdir()
    bad('unexpected-empty-directory', p)
    p = clone('symlink-file')
    f = p / 'VERDICT.json'
    f.unlink()
    f.symlink_to(W / 'VERDICT.json')
    bad('symlinked-authored-file', p)
    p = clone('hardlink-file')
    f = p / 'VERDICT.json'
    f.unlink()
    os.link(W / 'VERDICT.json', f)
    try:
        bad('hardlinked-authored-file', p)
    finally:
        f.unlink()
    p = clone('fifo-file')
    f = p / 'VERDICT.json'
    f.unlink()
    os.mkfifo(f)
    bad('fifo-authored-file', p)
    p = clone('missing-file')
    (p / 'VERDICT.json').unlink()
    bad('missing-authored-file', p)
    p = D / 'root-link'
    p.symlink_to(W, target_is_directory=True)
    bad('symlinked-packet-root', p)
    p = D / 'invoked-checker-link.py'
    p.symlink_to(W / 'verify_packet.py')
    bad('symlinked-invocation-entrypoint', entry=p)
    p = D / 'ancestor-link'
    p.symlink_to(W.parent, target_is_directory=True)
    bad('symlinked-root-ancestor', p / W.name)

    def copyinputs(name):
        p = D / name
        p.mkdir()
        for row in json.loads((W / 'INPUT_BINDINGS.json').read_text())['records']:
            q = p / row['path']
            q.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(Path(a.input_root) / row['path'], q)
        return p
    p = copyinputs('altered-input')
    f = p / 'original/unsolved_math_prioritization/attempts/30001478/author/certificate.json'
    f.write_text(f.read_text().replace('"X"', '"Y"', 1))
    bad('altered-source-certificate', ir=p)
    p = copyinputs('extra-original')
    (p / 'original/unsolved_math_prioritization/attempts/30001478/EXTRA').write_text('x')
    bad('extra-original-input', ir=p)
    p = D / 'altered-primary'
    shutil.copytree(a.source_root, p, ignore=shutil.ignore_patterns('control*'))
    f = p / 'OWR2010_22.pdf'
    f.write_bytes(f.read_bytes() + b'x')
    bad('altered-primary-PDF', sr=p)
    p = clone('duplicate-json')
    b = b'{"format":"bad","format":"pr789-source-geometry-v1","files":[]}'
    (p / 'MANIFEST.json').write_bytes(b)
    bad('duplicate-JSON-key', p, mfpin=sha(b))
    p = clone('unsafe-row')
    m = json.loads((p / 'MANIFEST.json').read_text())
    m['files'][0]['path'] = '../escape'
    b = json.dumps(m).encode()
    (p / 'MANIFEST.json').write_bytes(b)
    bad('unsafe-manifest-path', p, mfpin=sha(b))
    p = clone('duplicate-row')
    m = json.loads((p / 'MANIFEST.json').read_text())
    m['files'].append(m['files'][0])
    b = json.dumps(m).encode()
    (p / 'MANIFEST.json').write_bytes(b)
    bad('duplicate-manifest-file-row', p, mfpin=sha(b))
    return {'result': 'PASS', 'positive_count': len(positives), 'negative_count': len(negatives), 'positives': positives, 'negative_controls': negatives, 'scope': 'Four independent-executable normal/optimized baselines with full62 input and20 primary-file checks;18 targeted custody controls. No candidate executable replay or priority certification.'}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--packet', required=True)
    ap.add_argument('--scratch', required=True)
    ap.add_argument('--input-root', required=True)
    ap.add_argument('--source-root', required=True)
    ap.add_argument('--other-python', required=True)
    ap.add_argument('--output', required=True)
    a = ap.parse_args()
    result = run(a)
    Path(a.output).write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'result': result['result'], 'positive_count': result['positive_count'], 'negative_count': result['negative_count']}))
if __name__ == '__main__':
    main()
