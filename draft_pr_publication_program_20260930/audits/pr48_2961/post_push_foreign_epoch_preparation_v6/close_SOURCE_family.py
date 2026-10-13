"""UNEXECUTED ROOT-only V6 closer. Only new SOURCE payload modes change to0444."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,stat
P=Path(__file__).absolute().parent
KEYS={'schema','source_only','self_excluded','files_count','files','file_modes','directory_modes'}
def need(v,m):
 if not v:raise ValueError(m)
def safe(n):
 need(type(n) is str and n and '\\' not in n and '\0' not in n,'Literal relative file');q=PurePosixPath(n);need(not q.is_absolute() and q.as_posix()==n and not {'.','..','.git','__pycache__'}.intersection(q.parts),'Canonical source member');return n
def raw(q):need(q.is_file() and not q.is_symlink() and all(not a.is_symlink() for a in q.parents),'Regular source');return q.read_bytes()
def pairs(items):
 d={}
 for k,v in items:need(k not in d,'Duplicate key');d[k]=v
 return d
def main():
 p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');p.add_argument('--personally-read-complete-source',action='store_true');p.add_argument('--source-ready-sha256',required=True);a=p.parse_args();need(a.execute and a.personally_read_complete_source and __debug__ and P.name=='post_push_foreign_epoch_preparation_v6','ROOT explicit V6 source read');need(not (P/'SOURCE_MANIFEST.json').exists(),'Absent own V6 self');b=raw(P/'SOURCE_READY.json');need(hashlib.sha256(b).hexdigest()==a.source_ready_sha256,'Exact SOURCE READY');v=json.loads(b,object_pairs_hook=pairs);need(v['schema']=='pr48-post-push-epoch-SOURCE-readiness/v6' and v['source_only'] is True and v['proposed_code_executed'] is False and v['actual_epoch_or_acceptance_approved'] is False,'Source only')
 names=[safe(n) for n in v['closure_payload_files']];need(names==sorted(set(names)) and len(names)==v['closure_payload_count'],'Declared distinct full payload');dirs={q.as_posix() for n in names for q in PurePosixPath(n).parents if q.as_posix()!='.'};need({q.relative_to(P).as_posix() for q in P.rglob('*') if q.is_file()}==set(names) and {q.relative_to(P).as_posix() for q in P.rglob('*') if q.is_dir()}==dirs and all(not q.is_symlink() and (q.is_file() or q.is_dir()) for q in P.rglob('*')),'Exact V6 source topology')
 for d in dirs|{'.'}:need(stat.S_IMODE((P/d).stat().st_mode)==0o755,'Full0755 SOURCE directories')
 rows=[]
 for n in names:
  f=P/n;need(stat.S_IMODE(f.stat().st_mode)==0o644,'Unclosed prepared body full0644 before controlled SOURCE freeze');x=raw(f);rows.append(dict(path=n,bytes=len(x),sha256=hashlib.sha256(x).hexdigest()))
 for z in v['source_files']:need(type(z) is dict and set(z)=={'path','bytes','sha256'} and any(z['path']==(P/q['path']).relative_to(P.parents[3]).as_posix() and z['bytes']==q['bytes'] and z['sha256']==q['sha256'] for q in rows),'Exact operative triple references')
 result=dict(schema='pr48-post-push-epoch-source-closure/v6',source_only=True,self_excluded=['SOURCE_MANIFEST.json'],files_count=len(rows),files=rows,file_modes=[dict(path=n,full_mode=0o444) for n in sorted(set(names)|{'SOURCE_MANIFEST.json'})],directory_modes=[dict(path=d,full_mode=0o755) for d in sorted(dirs|{'.'})]);need(set(result)==KEYS,'Seven-key V6 mode-bearing SOURCE schema');os.umask(0o022)
 with (P/'SOURCE_MANIFEST.json').open('xb') as f:f.write((json.dumps(result,indent=2,sort_keys=True)+'\n').encode());f.flush();os.fsync(f.fileno())
 for n in names+['SOURCE_MANIFEST.json']:(P/n).chmod(0o444)
 for z in rows:need(len(raw(P/z['path']))==z['bytes'] and hashlib.sha256(raw(P/z['path'])).hexdigest()==z['sha256'],'Whole source body unchanged by freeze')
 for z in result['file_modes']:need(stat.S_IMODE((P/z['path']).stat().st_mode)==z['full_mode'],'Every closed payload/self fullmode')
 for z in result['directory_modes']:need(stat.S_IMODE((P/z['path']).stat().st_mode)==z['full_mode'],'Every full directory mode')
 print(json.dumps(dict(status='PASS_SOURCE_V6_CLOSURE_ONLY',files_count=len(rows),source_manifest_sha256=hashlib.sha256(raw(P/'SOURCE_MANIFEST.json')).hexdigest(),fullmode_contract='pr48-source-operator-dependency-full07777/v6',future_acceptance_approved=False)))
if __name__=='__main__':main()
