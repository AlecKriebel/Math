"""Caller-pinned read-only closed review and complete external-input verifier.

Use Python -B, --seal-sha256 EXTERNAL_PIN. No replay, network, Git or writes.
"""
from pathlib import Path
import argparse, hashlib, json, stat

def need(x,m):
    if not x:raise RuntimeError(m)

def record(p):
    s=p.lstat();need(not stat.S_ISLNK(s.st_mode),'symlink forbidden')
    d=stat.S_ISDIR(s.st_mode);need(d or stat.S_ISREG(s.st_mode),'nonregular entry')
    x={'kind':'directory' if d else 'file','mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns,'nlink':s.st_nlink}
    if not d:
        b=p.read_bytes();x.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
    return x

def snapshot(root,exclude=()):
    return {p.relative_to(root).as_posix():record(p) for p in [root,*sorted(root.rglob('*'))] if p.relative_to(root).as_posix() not in exclude}

def main():
    a=argparse.ArgumentParser();a.add_argument('--seal-sha256',required=True);pin=a.parse_args().seal_sha256
    r=Path(__file__).resolve().parent;b=(r/'CLOSED_REVIEW_SEAL.json').read_bytes()
    need(hashlib.sha256(b).hexdigest()==pin,'caller-pinned seal mismatch')
    x=json.loads(b);need(set(x)=={'schema','excluded_exact_paths','entries'},'seal keys')
    need(x['schema']=='pr1332-preparation03-whole-review02-closed-v1','seal schema')
    need(x['excluded_exact_paths']==['CLOSED_REVIEW_SEAL.json'],'seal exclusions')
    actual=snapshot(r,x['excluded_exact_paths']);need(actual==x['entries'],'own complete namespace/bytes/mode/nsmtime/nlink mismatch')
    base=json.loads((r/'EXTERNAL_INPUT_BASELINE.json').read_text());need(set(base)=={'roots','entries'},'external baseline keys')
    need(len(base['roots'])==17 and len(set(base['roots']))==17,'complete17externalroots')
    external={}
    for name in base['roots']:
        need('/' not in name and name not in {'.','..'},'unsafe external root')
        q=r.parent/name
        for p in ([q,*sorted(q.rglob('*'))] if q.is_dir() else [q]):external[p.relative_to(r.parent).as_posix()]=record(p)
    need(external==base['entries'],'frozen external namespace/bytes/mode/nsmtime/nlink mismatch')
    p=r.parent/'publication_preparation_03'
    need(hashlib.sha256((p/'CLOSED_DIRECTORY_SEAL.json').read_bytes()).hexdigest()=='eb2dd4976c896fb32d6287904d38ac26ce486e6eadaa3546c255ed140a7ed891','preparation seal external pin')
    need(hashlib.sha256((p/'verify_preparation.py').read_bytes()).hexdigest()=='e6631fae7944a7691f80dbee3bae7123923a73a497c7cfd9205761535aac8ea2','preparation verifier external pin')
    need(json.loads((r/'DECISION.json').read_text())['publication_ready'] is False,'not publication authority')
    print(json.dumps({'status':'PASS','seal_sha256':pin,'payload_files':sum(v['kind']=='file' for v in actual.values()),'directories':sum(v['kind']=='directory' for v in actual.values()),'all_closed_namespace_bytes_modes_nsmtimes_nlinks_exact':True,'all17externalroots_1147entries_preserved':len(external)==1147,'publication_ready':False,'network_actions':0,'service_writes':0,'Git_operations':0,'filesystem_writes':0},sort_keys=True))

if __name__=='__main__':main()
