"""Exact read-only namespace seal verification; requires caller-pinned hash."""
from pathlib import Path
import argparse,hashlib,json,stat
def item(p):
 s=p.lstat();v={'kind':'directory'if stat.S_ISDIR(s.st_mode)else'file'if stat.S_ISREG(s.st_mode)else'UNSUPPORTED','mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns,'nlink':s.st_nlink}
 if v['kind']=='file':b=p.read_bytes();v.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 return v
def verify(root,expected):
 s=root/'MANIFEST.json';raw=s.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=expected:raise RuntimeError('Caller-pinned manifest SHA256 mismatch')
 j=json.loads(raw);actual={'.'if p==root else str(p.relative_to(root)):item(p)for p in[root,*sorted(root.rglob('*'))]if p!=s}
 if actual!=j['entries']:raise RuntimeError('Exact complete namespace/bytes/mode/nsmtime/nlink mismatch')
 metadata=item(s)
 for k,v in j['manifest_metadata'].items():
  if metadata[k]!=v:raise RuntimeError('Manifest self metadata mismatch '+k)
 return {'status':'PASS','sha256':expected,'payload_files':sum(x['kind']=='file'for x in actual.values()),'pinned_directories':sum(x['kind']=='directory'for x in actual.values()),'manifest_additional_file_bound_by_external_sha256':True,'root_nlink':root.lstat().st_nlink,'all_bytes_modes_nsmtime_nlink_namespace':True,'action_authority':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--expected-sha256',required=True);a=p.parse_args();print(json.dumps(verify(Path(__file__).resolve().parent,a.expected_sha256),sort_keys=True))
