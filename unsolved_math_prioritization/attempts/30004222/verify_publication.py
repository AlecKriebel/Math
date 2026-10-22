#!/usr/bin/env python3
"""Portable, read-only exact-byte release and corrected-delta replay."""
from pathlib import Path, PurePosixPath
import hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parent
ANCHORS={
 'release/MANIFEST.json':'975d9a7f2d13ab2564defe4d9965fb7e62586d71fa6f80760b4410047af243bb',
 'audit_20261005/safe/MANIFEST.json':'906f3c6b7831b6cb17f8c359361c800b573ad8896aecff75689d3e38c1e25380',
 'corrected_release_20261005/MANIFEST.json':'e4d60b6104abc8ad609d6b9ce5af8ca5796ba48c139b10a59f0181b560706914',
 'correction_binding_20261005/safe/MANIFEST.json':'a4bf90589135fd5453c62b58edef90e56396bbd477fadcd5cce36750d986793c',
 'delta_audit_20261005/safe/MANIFEST.json':'66fe28fb3da0574cd5917c4f7c0ad9d76dcb2fc77334963ee2f9713e57327628',
}
def require(ok,msg):
 if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
 out={}
 for k,v in pairs:
  require(k not in out,'duplicate JSON key: '+k);out[k]=v
 return out
def parse(p):return json.loads(p.read_bytes(),object_pairs_hook=unique)
def snapshot():
 return {p.relative_to(ROOT).as_posix():(p.stat().st_size,sha(p.read_bytes())) for p in ROOT.rglob('*') if p.is_file()}
def check():
 raw=(ROOT/'PUBLICATION_MANIFEST.json').read_bytes()
 if len(sys.argv)==2:require(sha(raw)==sys.argv[1],'external publication anchor mismatch')
 m=json.loads(raw,object_pairs_hook=unique)
 require(m['problem_id']=='30004222','problem identity')
 names=[x['path'] for x in m['files']]
 require(len(names)==len(set(names)),'duplicate manifest member')
 for name in names:
  p=PurePosixPath(name)
  require(name==p.as_posix() and not p.is_absolute() and '..' not in p.parts and name!='PUBLICATION_MANIFEST.json','unsafe manifest member')
 paths=list(ROOT.rglob('*'))
 require(not any(p.is_symlink() for p in paths),'symlink in package')
 require(all(p.is_file() or p.is_dir() for p in paths),'nonregular package member')
 now=snapshot()
 require(set(now)==set(names)|{'PUBLICATION_MANIFEST.json'},'exact publication file membership')
 dirs={str(p) for name in names for p in PurePosixPath(name).parents if str(p)!='.'}
 require({p.relative_to(ROOT).as_posix() for p in paths if p.is_dir()}==dirs,'exact publication directory membership')
 for x in m['files']:require(now[x['path']]==(x['bytes'],x['sha256']),'publication member hash: '+x['path'])
 for rel,anchor in ANCHORS.items():
  require(now[rel][1]==anchor,'frozen manifest anchor: '+rel)
  p=ROOT/rel;inner=parse(p)
  expected={x['path']:x for x in inner['files']}
  require(len(expected)==len(inner['files']),'duplicate frozen member')
  require({x.name for x in p.parent.iterdir()}==set(expected)|{'MANIFEST.json'},'frozen tree membership: '+rel)
  for name,r in expected.items():
   require(PurePosixPath(name).name==name,'unsafe frozen member')
   data=(p.parent/name).read_bytes()
   require((len(data),sha(data))==(r['bytes'],r['sha256']),'frozen member hash: '+rel+'/'+name)
 return raw,now
def main():
 require(len(sys.argv) in (1,2),'usage: verify_publication.py [external_manifest_sha256]')
 raw,before=check();d=parse(ROOT/'delta_audit_20261005/safe/DELTA_RESULTS.json')
 require(d['verdict']=='ACCEPTED_QUALIFIED_PRIOR_FORMULA' and d['remaining_blocking_defects']==[],'delta verdict')
 require(d['qualified_disposition']=='qualified_partial_prior_formula' and d['substantive_responses_used']==1 and not d['purely_combinatorial_resolution_certified'],'qualified disposition')
 require(d['accepted_corrected_manifest_sha256']==ANCHORS['corrected_release_20261005/MANIFEST.json'],'accepted corrected identity')
 require(d['original_frozen_verdict_unchanged']=='REVISE_REQUIRED','historical verdict')
 require(d['full_inventory']=={'added':3,'deleted':0,'modified':8,'paths':11},'complete delta inventory')
 env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 probe=subprocess.run([sys.executable,'-E','-B','-c','import sys; assert __debug__; print(sys.flags.optimize)'],env=env,check=True,capture_output=True,text=True)
 require(probe.stdout.strip()=='0' and not probe.stderr,'child assertions are disabled')
 commands=[('correction_binding',[ROOT/'correction_binding_20261005/safe/verify_binding.py',ROOT/'release',ROOT/'corrected_release_20261005']),('complete_delta',[ROOT/'delta_audit_20261005/safe/verify_delta.py','--root',ROOT])]
 results={}
 for name,args in commands:
  p=subprocess.run([sys.executable,'-E','-B',*map(str,args)],env=env,check=True,capture_output=True,text=True)
  require(not p.stderr,'unexpected verifier stderr: '+name)
  results[name]=json.loads(p.stdout,object_pairs_hook=unique)
  require(results[name]['status']=='PASS','verifier result: '+name)
 require(check()[1]==before,'input files changed during replay')
 print(json.dumps({'status':'PASS','problem_id':'30004222','queue_status':'unsolved','turns':'1/5','qualified_disposition':'qualified_partial_prior_formula','publication_manifest_sha256':sha(raw),'publication_files':len(before),'frozen_anchors_checked':len(ANCHORS),'child_assertions_enabled':True,'all_input_bytes_preserved':True,'external_publication_anchor_checked':len(sys.argv)==2,'replays':results},indent=2,sort_keys=True))
if __name__=='__main__':main()
