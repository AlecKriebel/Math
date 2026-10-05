#!/usr/bin/env python3
"""Strict externally pinned integrity gate and portable mathematical replays."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
AUTHOR_PIN = '465c3840c518ad8b5abe6bc229e306f2059a211f64cdeb48f5cb0005d2b88ecb'
AUDIT_PIN = '1c371abcc317ad4920fe361d65172d8c172370309c2de0d2e46ff83a2ee18cfe'
MANIFEST = 'PUBLICATION_MANIFEST.json'

def need(ok, why):
    if not ok:
        raise ValueError(why)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def pairs(items):
    out = {}
    for key, value in items:
        need(key not in out, 'duplicate JSON key')
        out[key] = value
    return out

def read_json(raw):
    return json.loads(raw, object_pairs_hook=pairs)

def git_blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

def check_queue(root, queue):
    need(queue.is_file() and not queue.is_symlink(), 'queue not regular or symlink')
    q = read_json((root/'QUEUE_PATCH.json').read_bytes())
    raw = queue.read_bytes()
    need(len(raw) == q['updated_bytes'] and sha(raw) == q['updated_sha256'] and git_blob(raw) == q['updated_blob'], 'updated queue bytes')
    lines = raw.splitlines(keepends=True)
    rows = [i for i, line in enumerate(lines) if b'| 30004334 /' in line]
    need(rows == [q['line_number']-1], 'queue target uniqueness')
    i = rows[0]
    cells = lines[i].split(b'|')
    need(cells[1].strip() == b'747' and cells[8] == b' unsolved ' and cells[9] == b' 5/5 ', 'queue disposition')
    old = cells[:]
    old[8], old[9] = b' queued ', b' 0/5 '
    need([j for j, (a,b) in enumerate(zip(cells,old)) if a != b] == [8,9], 'two-cell patch')
    lines[i] = b'|'.join(old)
    base = b''.join(lines)
    need(len(base) == q['base_bytes'] and sha(base) == q['base_sha256'] and git_blob(base) == q['base_blob'], 'base queue bytes')
    need(q['changed_cells'] == ['Status','Turns'] and q['changed_indices'] == [8,9], 'queue metadata')
    return {'verified':True, 'changed_cells':['Status','Turns'], 'all_other_bytes_preserved':True}

def verify(root, pin, queue=None):
    need(root.is_dir() and not root.is_symlink(), 'package directory symlink or missing')
    f = root/MANIFEST
    need(f.is_file() and not f.is_symlink(), 'publication manifest symlink or missing')
    raw = f.read_bytes()
    need(re.fullmatch(r'[0-9a-f]{64}',pin) and sha(raw) == pin, 'external publication manifest pin')
    m = read_json(raw)
    need(m['schema'] == 'root-unity-publication-v1' and m['problem_id'] == '30004334', 'manifest schema')
    entries = {}
    for row in m['files']:
        name = row['path']
        p = PurePosixPath(name)
        need(isinstance(name,str) and re.fullmatch(r'[A-Za-z0-9_./-]+',name) and not p.is_absolute() and str(p) == name and '..' not in p.parts and name not in ('.',MANIFEST) and name not in entries, 'unsafe/duplicate path')
        need(type(row['bytes']) is int and row['bytes'] >= 0 and re.fullmatch(r'[0-9a-f]{64}',row['sha256']), 'invalid manifest metadata')
        entries[name] = row
    actual = set()
    directories = set()
    for p in root.rglob('*'):
        need(not p.is_symlink(), 'package symlink')
        name = p.relative_to(root).as_posix()
        if p.is_dir():
            directories.add(name)
            continue
        need(stat.S_ISREG(p.stat().st_mode), 'nonregular payload')
        actual.add(name)
    expected_dirs = {str(parent) for name in entries for parent in PurePosixPath(name).parents if str(parent) != '.'}
    need(directories == expected_dirs, 'directory inventory')
    need(actual == set(entries)|{MANIFEST}, 'file inventory')
    for name, row in entries.items():
        raw = (root/name).read_bytes()
        need(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'payload mismatch '+name)
    for folder, name, pin in [('author','AUTHOR_MANIFEST.json',AUTHOR_PIN),('audit','AUDIT_MANIFEST.json',AUDIT_PIN)]:
        raw = (root/folder/name).read_bytes()
        need(sha(raw) == pin, 'frozen inner manifest')
        inner = read_json(raw)
        names = [f['path'] for f in inner['files']]
        need(len(names) == len(set(names)), 'duplicate inner path')
        need({p.name for p in (root/folder).iterdir()} == set(names)|{name}, 'inner inventory')
        for row in inner['files']:
            data = (root/folder/row['path']).read_bytes()
            need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'inner payload')
    status = read_json((root/'PUBLICATION_STATUS.json').read_bytes())
    need(status['status'] == 'unsolved' and status['turns_used'] == status['turn_limit'] == 5, 'scope status')
    for key in ['general_fixed_complex_order_m_ge_4_resolved','complex_counterexample','novelty_claim','global_openness_claim','source_pdfs_extracts_raw_datasets_private_coordination_included']:
        need(status[key] is False, 'scope nonclaim '+key)
    need(read_json((root/'audit/AUDIT_STATUS.json').read_bytes())['verdict'] == 'PASS', 'audit verdict')
    result = {'status':'PASS_SCOPED_PARTIAL_RESULTS','package_files':len(actual),'author_manifest_sha256':AUTHOR_PIN,'audit_manifest_sha256':AUDIT_PIN,'queue':check_queue(root,queue) if queue is not None else 'not supplied'}
    return result

def replay(root):
    root = root.resolve()
    flags = ['-O'] if sys.flags.optimize else []
    env = dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='root unity publication working directory ') as cwd:
        def run(script, *args):
            p = subprocess.run([sys.executable,*flags,str(root/script),*map(str,args)],cwd=cwd,env=env,capture_output=True,text=True,timeout=900)
            need(p.returncode == 0, script+' failed: '+p.stderr)
            return read_json(p.stdout)
        author = run('author/verify.py','--self-test','--expected-manifest',AUTHOR_PIN)
        audit = run('audit/verify_audit.py','--author',root/'author','--expected-audit-manifest',AUDIT_PIN)
        suite = run('audit/replay_checks.py','--author',root/'author')
        need(suite == read_json((root/'audit/REPLAY_RESULTS.json').read_bytes()), 'recorded full replay result differs')
        need(len(suite['replays']) == 8 and len(suite['integrity_controls']) == 30, 'full replay/negative control counts')
        return {'author_negative_controls':author['negative_controls_rejected'],'independent_reconstruction':audit['independent_reconstruction'],'normal_optimized_original_relocated_replays':8,'integrity_controls':30,'author_freeze_unchanged':suite['author_freeze_unchanged']}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root',type=Path)
    ap.add_argument('expected_manifest')
    ap.add_argument('--queue',type=Path)
    ap.add_argument('--replay',action='store_true')
    args = ap.parse_args()
    result = verify(args.root,args.expected_manifest,args.queue)
    if args.replay:
        result['replay'] = replay(args.root)
        verify(args.root,args.expected_manifest,args.queue)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
