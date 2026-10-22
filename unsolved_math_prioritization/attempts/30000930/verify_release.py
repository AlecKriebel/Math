#!/usr/bin/env python3
"""Network-free verification of the frozen crossingless release and audit."""
import hashlib,json,os,subprocess,sys,tempfile,zipfile
from pathlib import Path
if not __debug__:
    raise SystemExit('Run without -O: frozen verifiers use assertions.')
ROOT=Path(__file__).resolve().parent
ANCHORS={
 'continued-unsolved5.zip':(55541,'7d50dd95d9b3bb49b20b2218f2b865d1e75c0adad4c26a727c37ea572baf3846'),
 'continued-audit-portable.zip':(16019,'0b1c071bc5a8ee683ed2d1019e895fda402784bf31509861aeaaab53b8dc4c1e'),
 'audit/CLARIFICATIONS.md':(1279,'f0a3384230c84734e7a33d72d6e6292f21bc5f6d7c1b7b9c575de4d83a33dc7d'),
 'safe/history/audit/AUDIT.md':(9713,'dbb8a9e4593ec287b4e408e70ad9408604c1d3b18bcee5b68810f958b3524964'),
 'safe/history/author-packet.zip':(18021,'ae7427fca8dc6414d40b0a499fa58e2cd7056151f3c5a781170a96df72c0a3a1')}
def require(ok,message):
    if not ok:raise ValueError(message)
def identity(p):
    b=p.read_bytes();return len(b),hashlib.sha256(b).hexdigest()
def checked_path(name):
    p=Path(name);require(not p.is_absolute() and '..' not in p.parts and name not in ['', '.'],'unsafe path');return ROOT/p
def check_integrity():
    manifest=json.loads((ROOT/'RELEASE_MANIFEST.json').read_text());rows=manifest['files']
    require(len({r['path'] for r in rows})==len(rows),'duplicate manifest paths')
    actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
    require(actual=={r['path'] for r in rows}|{'RELEASE_MANIFEST.json'},'payload file-set mismatch')
    for r in rows:require(identity(checked_path(r['path']))==(r['bytes'],r['sha256']),'changed payload: '+r['path'])
    for name,expected in ANCHORS.items():require(identity(ROOT/name)==expected,'fixed anchor mismatch: '+name)
    archive_counts={}
    for name in ('continued-unsolved5.zip','continued-audit-portable.zip'):
        with zipfile.ZipFile(ROOT/name) as z:
            require(len(set(z.namelist()))==len(z.namelist()),'duplicate archive paths')
            for n in z.namelist():require(z.read(n)==checked_path(n).read_bytes(),'archive/extracted mismatch: '+n)
            archive_counts[name]=len(z.namelist())
    require(archive_counts=={'continued-unsolved5.zip':24,'continued-audit-portable.zip':8},'archive membership count')
    hb=json.loads((ROOT/'safe/HISTORY_BINDING.json').read_text())
    require(len(hb['files'])==7,'history membership count')
    for row in hb['files']:require(identity(ROOT/'safe'/row['path'])==(row['bytes'],row['sha256']),'history identity: '+row['path'])
    status=json.loads((ROOT/'safe/STATUS.json').read_text());require(status['status']=='unsolved' and status['turns_used']==status['turn_limit']==5,'status/turns')
    turns=[json.loads(x) for x in (ROOT/'safe/turns.jsonl').read_text().splitlines() if x.strip()];require(len(turns)==5,'five approaches')
    require('ordinary complex-oriented' in (ROOT/'safe/SOURCE_UPDATES.md').read_text(),'source correction missing')
    require('2026' in (ROOT/'README.md').read_text() and 'opposite' in (ROOT/'README.md').read_text(),'current scope missing')
    return {'files_verified':len(rows),'archive_members':archive_counts,'history_bindings':7,'frozen_author_members':24,'frozen_audit_members':8,'queue_status':'unsolved','turns':'5/5','assertions_enabled':True}
def main():
    result=check_integrity()
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td)
        with zipfile.ZipFile(ROOT/'continued-audit-portable.zip') as z:z.extractall(tmp)
        # replay_audit independently extracts the bound author archive into another temporary directory.
        out=subprocess.check_output([sys.executable,str(tmp/'audit/replay_audit.py'),str(ROOT/'continued-unsolved5.zip')],cwd=tmp,env=env)
        replay=json.loads(out);require(replay['status']=='PASS','audit replay')
    require(check_integrity()==result,'replay changed payload')
    result.update(status='PASS',full_resolution=False,clean_archive_replay=replay)
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
