"""Caller-pinned, read-only closed WHOLE02 review and complete custody verifier."""
from pathlib import Path
import argparse,json,hashlib,stat,lzma,io,tarfile,re,sys
D=Path(__file__).resolve().parent
P=D.parent/'publication_postpublish_preview_init_recovery_preparation02'
def need(x,m):
 if not x:raise RuntimeError(m)
def H(b):return hashlib.sha256(b).hexdigest()
def J(b):
 def pairs(xs):
  z={}
  for k,v in xs:need(k not in z,'Duplicate JSON key');z[k]=v
  return z
 return json.loads(b,object_pairs_hook=pairs)
def pin(b):return {'bytes':len(b),'sha256':H(b)}
def namespace(root,exclude):
 out={}
 for p in [root,*sorted(root.rglob('*'))]:
  n='.'if p==root else p.relative_to(root).as_posix()
  if n in exclude:continue
  s=p.lstat();need(not p.is_symlink(),'Symlink in closed review')
  e={'kind':'directory'if stat.S_ISDIR(s.st_mode)else'file','mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns,'nlink':s.st_nlink}
  if e['kind']=='file':need(stat.S_ISREG(s.st_mode),'Nonregular review file');e.update(pin(p.read_bytes()))
  out[n]=e
 return out
def main():
 need(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode and sys.flags.optimize==0,'Use CPython -I -S -B optimize0')
 a=argparse.ArgumentParser();a.add_argument('--manifest-sha256',required=True);args=a.parse_args()
 need(re.fullmatch('[a-f0-9]{64}',args.manifest_sha256),'Caller hash required')
 raw=(D/'MANIFEST.json').read_bytes();need(H(raw)==args.manifest_sha256,'Externally pinned review changed');m=J(raw)
 need(m['exclude_exactly']==['MANIFEST.json']and m['readiness']is False and m['root_action_authority']is False,'Integrity is not action authority')
 need(namespace(D,m['exclude_exactly'])==m['entries'],'Complete review namespace/bytes/modes/nsmtime/nlinks changed')
 need(H((P/'RECOVERY_MANIFEST.json').read_bytes())=='013dd485c0956ca50965a6dff8324b521d07844c027f9ca382e9c9f071f7fefc','Frozen preparation seal changed')
 prep=J((P/'RECOVERY_MANIFEST.json').read_bytes());need({p.relative_to(P).as_posix()for p in P.rglob('*')if p.is_file()}=={e['path']for e in prep['files']}|{'RECOVERY_MANIFEST.json','RECOVERY_MANIFEST.sha256'},'Frozen preparation file namespace')
 need({p.relative_to(P).as_posix()for p in P.rglob('*')if p.is_dir()}=={e['path']for e in prep['directories']},'Frozen preparation directory namespace')
 for e in prep['files']+prep['directories']:
  p=P/e['path'];s=p.lstat();need(not p.is_symlink()and stat.S_IMODE(s.st_mode)==e['mode']and s.st_mtime_ns==e['mtime_ns']and s.st_nlink==e['nlink'],'Frozen preparation metadata changed')
  if 'sha256'in e:need(pin(p.read_bytes())=={k:e[k]for k in ['bytes','sha256']},'Frozen preparation bytes changed')
 need(H((P/'SOURCE_MANIFEST.json').read_bytes())=='b788049646d45487d4883c8bb7f7418c9170ef4ae8bba8a5095e2e8913de9984','Runtime source changed')
 binds=J((P/'INPUT_BINDINGS.json').read_bytes())
 for name,e in binds['refs'].items():
  p=Path(name);need(not any(q.is_symlink()for q in[p,*p.parents])and pin(p.read_bytes())==e,'External runtime/authority/evidence changed')
 prefix=J((P/'private/CURRENT_CASE_PREFIX.json').read_bytes());case=Path(prefix['case_path']);files=0
 for e in prefix['entries']:
  p=case if e['path']=='.'else case/e['path'];s=p.lstat();need(not p.is_symlink()and s.st_dev==e['device']and s.st_ino==e['inode']and stat.S_IMODE(s.st_mode)==e['mode'],'Original CASE prefix identity changed')
  if e['kind']=='file':
   need(s.st_nlink==e['nlink']and s.st_mtime_ns==e['mtime_ns']and pin(p.read_bytes())=={k:e[k]for k in ['bytes','sha256']},'Original CASE file changed');files+=1
  else:need(p.is_dir(),'Original CASE directory changed')
 # Later legitimate CASE appends are permitted; original prefix never rebaselined.
 counts={'archives':0,'files':0,'dirs':0,'bytes':0}
 for p in sorted((D/'private').rglob('*.custody.json.xz')):
  inv=J(lzma.decompress(p.read_bytes()));store=p.parent/'WORLD_CUSTODY.store'
  with store.open('rb')as f:f.seek(inv['offset']);body=f.read(inv['compressed_bytes'])
  need(len(body)==inv['compressed_bytes']and H(body)==inv['compressed_sha256'],'Owned world segment changed')
  with tarfile.open(fileobj=io.BytesIO(body),mode='r:xz')as t:
   ms=t.getmembers();need(len(ms)==len(inv['entries'])and len({x.name for x in ms})==len(ms),'Owned full archive namespace')
   for n,e in zip(ms,inv['entries']):
    need(n.name==e['path']and n.mode==e['mode']and int(n.pax_headers['custody_mtime_ns'])==e['mtime_ns'],'Owned world metadata')
    if e['kind']=='file':
     need(n.isfile()and pin(t.extractfile(n).read())=={k:e[k]for k in ['bytes','sha256']},'Owned complete member bytes');counts['files']+=1;counts['bytes']+=e['bytes']
    else:need(n.isdir(),'Owned world directory');counts['dirs']+=1
   counts['archives']+=1
 need(counts=={'archives':11,'files':5786,'dirs':66,'bytes':5631982},'Complete custody count changed')
 c=J((D/'CONTROL_RECONCILIATION.json').read_bytes());need(len(c['successful_cases'])==9 and len({r['case']for r in c['successful_cases']})==9 and len(c['incomplete_not_counted_as_pass'])==2,'Scoped successful/control count')
 r=J((D/'REVIEW_RECEIPT.json').read_bytes());need(r=={'schema':'pr1208-postpublish-preview-init-review-v2','pr':1208,'record':23578142,'source_sha256':'b788049646d45487d4883c8bb7f7418c9170ef4ae8bba8a5095e2e8913de9984','status':'PASS','fresh_independent_review':True,'unresolved_findings':[]},'Review receipt changed')
 print(json.dumps({'status':'PASS_READ_ONLY_CLOSED_REVIEW','review_files':sum(v['kind']=='file'for v in m['entries'].values()),'review_dirs':sum(v['kind']=='directory'for v in m['entries'].values()),'original_CASE_prefix_files':files,'owned_complete_custody':counts,'successful_exact_predicate_worlds':9,'incomplete_resource_worlds_excluded':2,'service_calls':0,'production_CASE_changes':0,'action_authority':False,'readiness':False},sort_keys=True))
if __name__=='__main__':main()
