#!/usr/bin/env python3
"""Read-only authentication of the exact selected original packet against Git."""
import argparse, hashlib, json, os, pathlib, subprocess
A = pathlib.Path(__file__).resolve().parents[2]
REPO = A.parents[2]
HEAD = 'c09ef9df8b1f4642be0396ba6343344be8fa25b0'
PREFIX = 'unsolved_math_prioritization/attempts/30003471/'
PIN = '6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415'
OUTER = 'd1b3a0528bf518640a117c2cfecff5bc81d21f58632f7b4f647ae998eb4dcedd'
def git(*args):
    return subprocess.check_output(['git','-C',str(REPO),*args])
def sha(b): return hashlib.sha256(b).hexdigest()
def authenticate():
    packet = json.loads((A/'ROOT_PACKET_AUTHENTICATION.json').read_text())
    if packet['original_head'] != HEAD: raise ValueError('head pin changed')
    records = packet['records']
    if len(records) != 29: raise ValueError('expected exactly 29 selected files')
    tree = git('ls-tree','-r','-z',HEAD,'--',PREFIX)
    actual = {}
    for row in tree.split(b'\0'):
        if not row: continue
        metadata, path = row.split(b'\t',1)
        mode, typ, oid = metadata.decode().split()
        if mode != '100644' or typ != 'blob': raise ValueError('nonregular original entry')
        actual[path.decode()] = oid
    if set(actual) != set(records): raise ValueError('selected Git tree differs from 29-file map')
    checked = {}
    for path, expected in records.items():
        diskpath = A/'original'/path
        if diskpath.is_symlink() or not diskpath.is_file(): raise ValueError('nonregular disk original')
        data = diskpath.read_bytes()
        obj = git('cat-file','blob',actual[path])
        found = {'bytes':len(data), 'sha256':sha(data)}
        if data != obj or found != expected: raise ValueError('authentication failure: '+path)
        checked[path] = found
    if checked[PREFIX+'public/PROOF.md']['sha256'] != PIN: raise ValueError('proof pin')
    if checked[PREFIX+'PUBLICATION_MANIFEST.json']['sha256'] != OUTER: raise ValueError('outer pin')
    branch = git('branch','--show-current').decode().strip()
    if branch != 'main': raise ValueError('shared branch changed')
    indexpath = pathlib.Path(git('rev-parse','--git-path','index').decode().strip())
    if not indexpath.is_absolute(): indexpath = REPO/indexpath
    return {'original_head':HEAD, 'proof_sha256':PIN, 'outer_manifest_sha256':OUTER,
            'original_count':len(checked), 'all_originals_match_actual_Git':True,
            'shared_head':git('rev-parse','HEAD').decode().strip(), 'shared_branch':branch,
            'shared_index_sha256':sha(indexpath.read_bytes()), 'selected_records':checked}
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=pathlib.Path)
    args = parser.parse_args()
    result = authenticate()
    from datetime import datetime, timezone
    result['utc'] = datetime.now(timezone.utc).isoformat()
    text = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')
