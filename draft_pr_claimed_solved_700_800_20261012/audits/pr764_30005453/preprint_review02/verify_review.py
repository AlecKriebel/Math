"""Read-only closure verifier for this exact review; no replay or artifact writes."""
from pathlib import Path,PurePosixPath
import hashlib,json,stat
ROOT=Path(__file__).resolve().parent
def need(ok,msg):
 if not ok:raise ValueError(msg)
def decode(raw):
 def pairs(items):
  out={}
  for k,v in items:
   need(k not in out,'Duplicate JSON key');out[k]=v
  return out
 return json.loads(raw,object_pairs_hook=pairs)
def ident(raw):
 return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def main():
 m=decode((ROOT/'MANIFEST.json').read_bytes())
 listed={}
 for e in m['authored_files']:
  n=e['path'];p=PurePosixPath(n)
  need(n not in listed and n!='MANIFEST.json' and not p.is_absolute() and '..' not in p.parts,'Bad authored path')
  listed[n]={k:e[k] for k in ('bytes','sha256')}
 frozen=m['permitted_frozen_inputs'];bound=decode((ROOT/'INPUT_BINDING.json').read_bytes())
 need(frozen==[{'path':'frozen/'+e['path'],**{k:e[k] for k in ('bytes','sha256')}} for e in bound['frozen_publication_files']],'Frozen binding mismatch')
 expected=set(listed)|{'MANIFEST.json'}|{e['path'] for e in frozen}
 files={};dirs=set()
 for p in ROOT.rglob('*'):
  need(not p.is_symlink(),'Symlink in review')
  n=p.relative_to(ROOT).as_posix()
  if p.is_dir():dirs.add(n)
  else:
   need(stat.S_ISREG(p.stat().st_mode),'Nonregular review file')
   files[n]=p.read_bytes()
 need(set(files)==expected,'Review file inventory differs')
 need(dirs=={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'},'Review directory inventory differs')
 for n,e in listed.items():need(ident(files[n])==e,'Authored bytes changed: '+n)
 for e in frozen:
  need(ident(files[e['path']])=={k:e[k] for k in ('bytes','sha256')},'Frozen bytes changed')
  need((ROOT/e['path']).stat().st_nlink==1,'Frozen input unexpectedly hardlinked')
 for n,raw in files.items():
  if n.endswith('.json'):decode(raw)
 verdict=decode(files['VERDICT.json'])
 need(verdict['result']=='PASS' and verdict['actionable_issue_count']==0 and not verdict['issues'] and not verdict['repairs_required'],'Verdict scope changed')
 need(verdict['publication_pins']==bound['frozen_publication_files'],'Verdict pin mismatch')
 need(decode(files['REPRODUCTION_RECEIPT.json'])['result']=='PASS','Missing reproduction')
 need(all(x['equals_frozen_render'] for x in decode(files['VISUAL_RECEIPT.json'])['compiled_render_comparison']),'Visual comparison')
 print(json.dumps({'result':'PASS','authored_files':len(listed),'permitted_frozen_inputs':len(frozen),'closed_regular_files':len(files),'read_only':True},sort_keys=True))
if __name__=='__main__':main()
