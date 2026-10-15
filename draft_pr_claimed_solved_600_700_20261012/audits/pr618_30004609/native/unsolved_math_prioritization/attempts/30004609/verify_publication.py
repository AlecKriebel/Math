#!/usr/bin/env python3
"""Strict inventory/integrity validation and exact replay of the final package."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, subprocess, sys
ROOT=Path(__file__).resolve().parent
MANIFEST='PUBLICATION_MANIFEST.json'

def digest(data): return hashlib.sha256(data).hexdigest()

def verify():
    doc=json.loads((ROOT/MANIFEST).read_text())
    entries=doc['files']
    assert isinstance(entries,list) and entries, 'empty file inventory'
    assert doc['file_count']==len(entries), 'file count mismatch'
    names=[]
    for e in entries:
        name=e['path']; p=PurePosixPath(name)
        assert isinstance(name,str) and name and str(p)==name, 'noncanonical path'
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in name, 'unsafe path'
        assert name!=MANIFEST and name not in names, 'duplicate or self entry'
        assert isinstance(e['bytes'],int) and e['bytes']>=0, 'invalid byte count'
        assert len(e['sha256'])==64 and all(c in '0123456789abcdef' for c in e['sha256']), 'invalid digest'
        names.append(name)
    actual=set()
    for p in ROOT.rglob('*'):
        assert not p.is_symlink(), 'symlink prohibited'
        if p.is_file(): actual.add(p.relative_to(ROOT).as_posix())
    assert actual==set(names)|{MANIFEST}, ('exact inventory mismatch',sorted(actual-set(names)-{MANIFEST}),sorted(set(names)-actual))
    for e in entries:
        data=(ROOT/e['path']).read_bytes()
        assert len(data)==e['bytes'] and digest(data)==e['sha256'], ('file mismatch',e['path'])
    inputs=json.loads((ROOT/'independent-audit/AUDITED_INPUTS.json').read_text())
    prefix='unsolved_math_prioritization/attempts/30004609/'
    for e in inputs['files']:
        assert e['path'].startswith(prefix)
        data=(ROOT/e['path'][len(prefix):]).read_bytes()
        assert len(data)==e['bytes'] and digest(data)==e['sha256'], ('frozen author mismatch',e['path'])
    q=ROOT.parents[1]/'QUEUE.md'
    q_status='not present in standalone packet'
    if q.is_file():
        data=q.read_bytes()
        assert digest(data)==doc['queue_patch']['after_sha256'] and len(data)==doc['queue_patch']['after_bytes'], 'queue bytes mismatch'
        rows=data.decode().splitlines()
        hits=[l for l in rows if '| 644 | 30004609 /' in l]
        assert hits==[doc['queue_patch']['after_row']], 'queue row mismatch'
        q_status='PASS'
    return doc,q_status

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--integrity-only',action='store_true');args=ap.parse_args()
    doc,q_status=verify()
    out={'exact_packet_integrity':'PASS','manifested_files':doc['file_count'],'queue':q_status}
    if not args.integrity_only:
        author=subprocess.run([sys.executable,str(ROOT/'check.py')],cwd=ROOT,check=True,capture_output=True)
        assert author.stdout==(ROOT/'RESULTS.json').read_bytes(), 'final author output mismatch'
        audit=subprocess.run([sys.executable,str(ROOT/'independent-audit/verify_audit.py')],cwd=ROOT,check=True,capture_output=True)
        out['final_layout_author_checker']='PASS_BYTE_IDENTICAL'
        out['portable_independent_audit']=json.loads(audit.stdout)
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
