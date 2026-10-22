"""Caller-pinned READ ONLY integrity check; no project imports/replay/services/writes."""
from pathlib import Path
import hashlib,json,stat,sys,re
D=Path(__file__).resolve().parent
def need(v,m):
 if not v:raise RuntimeError(m)
def H(b):return hashlib.sha256(b).hexdigest()
def strict(b):
 def pairs(items):
  out={}
  for key,value in items:need(key not in out,'Duplicate JSON key');out[key]=value
  return out
 return json.loads(b,object_pairs_hook=pairs)
def snap(root,exclude=('MANIFEST.json',),nlinks=False):
 out={};groups={}
 for q in [root,*sorted(root.rglob('*'))]:
  name='.'if q==root else q.relative_to(root).as_posix()
  if name in exclude:continue
  st=q.lstat();need(not q.is_symlink(),'Symlink in closed namespace')
  entry={'kind':'directory'if stat.S_ISDIR(st.st_mode)else'file','mode':stat.S_IMODE(st.st_mode),'mtime_ns':st.st_mtime_ns}
  if nlinks:entry['nlink']=st.st_nlink
  if entry['kind']=='file':
   need(stat.S_ISREG(st.st_mode),'Nonregular file');b=q.read_bytes();entry.update(bytes=len(b),sha256=H(b));groups.setdefault((st.st_dev,st.st_ino),[]).append(name)
  out[name]=entry
 return out,sorted(sorted(v)for v in groups.values()if len(v)>1)
def external_inputs():
 capture=strict((D/'private/FINAL_INPUT_READBACK.json').read_bytes())
 for name,pin in capture['inventory'].items():
  q=Path(name);st=q.lstat();need(not q.is_symlink()and stat.S_ISREG(st.st_mode),'Changed external input type');raw=q.read_bytes()
  need({'bytes':len(raw),'sha256':H(raw),'mode':stat.S_IMODE(st.st_mode),'mtime_ns':st.st_mtime_ns}==pin,'Historical/scientific input changed: '+name)
 for folder,nlinks in [('operations16',False),('operations16_whole_review01',True)]:
  root=D.parent/folder;m=strict((root/'MANIFEST.json').read_bytes());actual,_=snap(root,nlinks=False)
  for name,pin in m['entries'].items():
   if 'nlink'in pin:actual[name]['nlink']=(root if name=='.'else root/name).stat().st_nlink
  need(actual==m['entries'],'Complete prior namespace/metadata changed: '+folder)
 f=strict((D/'source/SOURCE_FREEZE.json').read_bytes());old=D.parent/'operations'
 need({q.name for q in(old/'runtime').iterdir()}==set(f['prior_runtime_files']),'Original13-leaf runtime changed')
 need(not(old/'runtime/ROOT_OPERATIONAL_CLEARANCE.json').exists(),'Revoked authority revived')
 for phase in range(6,18):need(not(D.parent/('operations'+str(phase).zfill(2))/'runtime').exists(),'Held/uncleared production runtime appeared')
 need(H((old/'proposed/preprint/zenodo-deposit.json').read_bytes())=='0ca12e07eee0ed88da4f94b82a2404eed4341aaa1f08f9100ecb630014fed6fe','Canonical original manifest changed')
 return len(capture['inventory'])
def main():
 need(sys.flags.optimize==0 and sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode,'Use optimize0 -I -S -B')
 need(len(sys.argv)==3 and sys.argv[1]=='--manifest-sha256'and re.fullmatch('[0-9a-f]{64}',sys.argv[2]),'Exact caller manifest SHA required')
 raw=(D/'MANIFEST.json').read_bytes();need(H(raw)==sys.argv[2],'Caller manifest pin mismatch')
 m=strict(raw);need(m['exclusions']==['MANIFEST.json']and m['publication_ready']is False and m['root_action_accepted']is False,'Integrity is not readiness/authority')
 actual,groups=snap(D);need(actual==m['entries']and groups==sorted(sorted(v)for v in m['hardlink_groups']),'Complete packet bytes/modes/nsmtime/namespace changed')
 src=D/'source';b=(src/'SOURCE_MANIFEST.json').read_bytes();need(H(b)==m['source_manifest_sha256'],'Source manifest changed');pins=strict(b)
 need({q.name for q in src.iterdir()}==set(pins)|{'SOURCE_MANIFEST.json'},'Source namespace changed')
 for name,pin in pins.items():
  data=(src/name).read_bytes();need(pin=={'bytes':len(data),'sha256':H(data)},'Source member changed')
 need(H((src/'bootstrap17.py').read_bytes())==m['bootstrap_sha256'],'Bootstrap changed')
 count=external_inputs()
 print(json.dumps({'status':'PASS_INTEGRITY_ONLY','files':m['files'],'directories':m['directories'],'input_records':count,'caller_pin':sys.argv[2],'publication_ready':False,'root_action_authority':False,'project_imports_replays_service_requests_writes':0},sort_keys=True))
if __name__=='__main__':main()
