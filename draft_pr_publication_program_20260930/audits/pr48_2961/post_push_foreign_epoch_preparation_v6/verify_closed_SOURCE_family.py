"""UNEXECUTED separate readonly V6 SOURCE reader; no candidate imports/compilation."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,stat
P=Path(__file__).absolute().parent
KEYS={'schema','source_only','self_excluded','files_count','files','file_modes','directory_modes'}
def need(v,m):
 if not v:raise ValueError(m)
def safe(n):
 need(type(n) is str and n and '\\' not in n and '\0' not in n,'Literal file');q=PurePosixPath(n);need(not q.is_absolute() and q.as_posix()==n and not {'.','..','.git','__pycache__'}.intersection(q.parts),'Canonical member');return n
def raw(q):need(q.is_file() and not q.is_symlink() and all(not a.is_symlink() for a in q.parents),'Regular nonsymlink source');return q.read_bytes()
def pairs(items):
 d={}
 for k,v in items:need(k not in d,'Duplicate key');d[k]=v
 return d
def main():
 p=argparse.ArgumentParser();p.add_argument('--source-manifest-sha256',required=True);a=p.parse_args();need(__debug__ and P.name=='post_push_foreign_epoch_preparation_v6','Exact V6 family');b=raw(P/'SOURCE_MANIFEST.json');need(hashlib.sha256(b).hexdigest()==a.source_manifest_sha256,'Exact actual closed self');v=json.loads(b,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)));need(type(v) is dict and set(v)==KEYS and v['schema']=='pr48-post-push-epoch-source-closure/v6' and v['source_only'] is True and v['self_excluded']==['SOURCE_MANIFEST.json'] and type(v['files_count']) is int and v['files_count']==len(v['files']),'Typed V6 closure schema');names={safe(z['path']) for z in v['files']};need(len(names)==v['files_count'],'Distinct exact payload');dirs={q.as_posix() for n in names for q in PurePosixPath(n).parents if q.as_posix()!='.'};need({q.relative_to(P).as_posix() for q in P.rglob('*') if q.is_file()}==names|{'SOURCE_MANIFEST.json'} and {q.relative_to(P).as_posix() for q in P.rglob('*') if q.is_dir()}==dirs and all(not q.is_symlink() and (q.is_file() or q.is_dir()) for q in P.rglob('*')),'Complete frozen topology');need(v['file_modes']==[dict(path=n,full_mode=0o444) for n in sorted(names|{'SOURCE_MANIFEST.json'})] and v['directory_modes']==[dict(path=d,full_mode=0o755) for d in sorted(dirs|{'.'})],'Complete separate fullmode domains')
 for z in v['files']:
  need(set(z)=={'path','bytes','sha256'} and type(z['bytes']) is int,'Original triple reference shape');x=raw(P/z['path']);need(len(x)==z['bytes'] and hashlib.sha256(x).hexdigest()==z['sha256'],'Whole closed payload body')
 for z in v['file_modes']:need(type(z['full_mode']) is int and stat.S_IMODE((P/z['path']).stat().st_mode)==z['full_mode'],'Typed actual closed payload/self mode')
 for z in v['directory_modes']:need(type(z['full_mode']) is int and stat.S_IMODE((P/z['path']).stat().st_mode)==z['full_mode'],'Typed complete0755 directories')
 print(json.dumps(dict(status='PASS_READONLY_SOURCE_V6_CLOSURE_ONLY',files_count=v['files_count'],source_manifest_sha256=a.source_manifest_sha256,fullmode_contract='pr48-source-operator-dependency-full07777/v6',production_executed=False,future_acceptance_approved=False)))
if __name__=='__main__':main()
