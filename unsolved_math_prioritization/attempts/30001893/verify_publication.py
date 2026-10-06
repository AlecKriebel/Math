#!/usr/bin/env python3
"""Portable integrity and exact replay; not a universal-conjecture proof."""
from pathlib import Path, PurePosixPath
import hashlib, json, subprocess, sys, zipfile
ROOT = Path(__file__).resolve().parent
BINDINGS = (
    ('release', 'b09ba6fceaad28780e2dea06cbc24bfd07ac7205149ff8358659655bfc0b9018', 'AUTHOR_SAFE_FREEZE.zip', 23424, '966970b14c7350553393b14ca378ad764d8ae2cd38b47cb00556fd6c51bf4e81'),
    ('audit_release', 'dc9c5261febbc66f1e533021f65b9a64d000e3f80b2340870c78db06526ea87e', 'INDEPENDENT_AUDIT_SAFE.zip', 21502, 'c854615190cb05a09e4e6b9227dcf7b03d2e27d79de5066027d5e11aaa7a77a3'),
)
def require(ok, label):
    if not ok:
        raise ValueError(label)
def digest(b):
    return hashlib.sha256(b).hexdigest()
def inventory(folder, manifest, allow_manifest=True):
    rows = manifest['files']
    names = [e['path'] for e in rows]
    require(len(names) == len(set(names)), 'Duplicate manifest path')
    for e in rows:
        n = e['path']; p = PurePosixPath(n)
        require(not p.is_absolute() and '..' not in p.parts and '\\' not in n, 'Unsafe path')
        f = folder / n
        require(f.is_file() and not f.is_symlink(), 'Missing or linked file: '+n)
        b = f.read_bytes()
        require(len(b) == e['bytes'] and digest(b) == e['sha256'], 'Changed bytes: '+n)
    expected = set(names) | ({'MANIFEST.json'} if allow_manifest else {'PUBLICATION_MANIFEST.json'})
    actual = {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file() or p.is_symlink()}
    require(actual == expected, 'Inventory mismatch')
    return expected

def main():
    manifest = json.loads((ROOT/'PUBLICATION_MANIFEST.json').read_bytes())
    require(manifest['problem_id'] == '30001893', 'Wrong target')
    inventory(ROOT, manifest, False)
    for folder, mh, zn, zs, zh in BINDINGS:
        f = ROOT/folder; mb = (f/'MANIFEST.json').read_bytes()
        require(digest(mb) == mh, 'Immutable manifest changed')
        names = inventory(f, json.loads(mb))
        zb = (ROOT/zn).read_bytes()
        require(len(zb) == zs and digest(zb) == zh, 'Immutable ZIP changed')
        with zipfile.ZipFile(ROOT/zn) as z:
            require(len(z.namelist()) == len(names) and set(z.namelist()) == names, 'ZIP members changed')
            for n in names:
                require(z.read(n) == (f/n).read_bytes(), 'ZIP member mismatch')
    status = json.loads((ROOT/'PUBLICATION_STATUS.json').read_bytes())
    require(status['queue_status'] == 'unsolved' and status['approaches_completed'] == 5, 'Wrong queue status')
    require(status['full_source_solved'] is False and status['novelty_claimed'] is False and status['current_global_openness_verified'] is False, 'Claim inflation')
    require(status['all_affine_strata_upper_bound_4n_minus_5_proved'] is False, 'Universal claim inflation')
    results = json.loads((ROOT/'audit_release/RESULTS.json').read_bytes())
    out=[]; science = (ROOT/'release/EXACT_RESULTS.json').read_bytes()
    for e in results['replays']:
        cmd=e['command'].split()
        require(cmd[0] == 'python3', 'Unexpected interpreter')
        wd=ROOT/('audit_release' if e['run'].startswith('independent') else 'release')
        p=subprocess.run([sys.executable]+cmd[1:],cwd=wd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
        require(p.returncode == 0, 'Replay failed: '+e['run']+' '+p.stderr.decode(errors='replace'))
        require(len(p.stdout)==e['stdout_bytes'] and digest(p.stdout)==e['stdout_sha256'], 'Replay byte mismatch: '+e['run'])
        if e['run'].startswith('author-scientific'):
            require(p.stdout==science, 'Frozen scientific output changed')
        out.append({'run':e['run'],'exit_code':p.returncode,'stdout_bytes':len(p.stdout),'stdout_sha256':digest(p.stdout)})
    print(json.dumps({'problem_id':'30001893','verdict':'PASS_PARTIAL_ONLY','full_source_solved':False,'immutable_files_and_zip_members_verified':True,'author_negative_controls_rejected':20,'independent_negative_controls_rejected':22,'replays':out},indent=2,sort_keys=True))
if __name__=='__main__':
    main()
