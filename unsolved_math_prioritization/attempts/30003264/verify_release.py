#!/usr/bin/env python3
"""Offline publication integrity and scoped finite-control replay.

Trust requires the external publication manifest hash and frozen ZIP hashes.
Neither a self-modifiable verifier nor a finite test proves the primary problem.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parent
ARCHIVES={
 'author':('PREBLOCH_30003264_AUTHOR_PACKET.zip',23595,'7e96c5992aa3d18ae6a00a78dd9bb373126410fa6b3fabba6280bb3e20cd0c2b','00d7c6e2159fc100af50d28f933eb0be886af80551e02119bd4fca8c63275ecd'),
 'audit':('PREBLOCH_30003264_INDEPENDENT_AUDIT.zip',19427,'7031913b0e66e3fd3b4a9fd5ea87aadbfd83d6917f8bdc554fb34abf0a50f6a2','6170c9ef8f7989fbda11d935a55cda605ea4083417a923522f9b6a81331c8bdf')}
AUTHOR_REPLAY_SHA='bb63ccf7603b1f40a705e9383813f2eb01a0064136843e9637b1356251b38cde'
def need(value,message):
 if not value: raise ValueError(message)
def sha(b): return hashlib.sha256(b).hexdigest()
def unique(pairs):
 obj={}
 for k,v in pairs:
  need(k not in obj,'duplicate JSON key'); obj[k]=v
 return obj
def parse(path): return json.loads(path.read_text(),object_pairs_hook=unique)
def meta(path):
 b=path.read_bytes(); return {'bytes':len(b),'sha256':sha(b)}
def inventory():
 manifest=parse(ROOT/'PUBLICATION_MANIFEST.json')
 need(set(manifest)=={'format','problem_id','files'},'manifest schema')
 need(type(manifest['format']) is int and manifest['format']==1,'manifest version')
 need(type(manifest['problem_id']) is int and manifest['problem_id']==30003264,'problem identity')
 files=manifest['files']
 paths=list(ROOT.rglob('*'))
 need(not any(p.is_symlink() for p in paths),'symlink')
 need({p.relative_to(ROOT).as_posix() for p in paths if p.is_dir()}=={'author','audit'},'directory inventory')
 need({p.relative_to(ROOT).as_posix() for p in paths if p.is_file()}==set(files)|{'PUBLICATION_MANIFEST.json'},'file inventory')
 for name,expected in files.items():
  need(not Path(name).is_absolute() and '..' not in Path(name).parts,'unsafe manifest path')
  need(meta(ROOT/name)==expected,'publication bytes: '+name)
 for folder,(name,size,digest,manifest_hash) in ARCHIVES.items():
  archive=ROOT/name; need(meta(archive)=={'bytes':size,'sha256':digest},'frozen archive')
  need(sha((ROOT/folder/'MANIFEST.json').read_bytes())==manifest_hash,'frozen manifest')
  actual={p.name for p in (ROOT/folder).iterdir()}
  with zipfile.ZipFile(archive) as z:
   names=z.namelist();need(len(names)==len(set(names)) and set(names)==actual,'archive member inventory')
   for item in names:
    need(Path(item).name==item,'unsafe archive member')
    need(z.read(item)==(ROOT/folder/item).read_bytes(),'frozen directory: '+item)
  fm=parse(ROOT/folder/'MANIFEST.json')
  need(set(fm['files'])==actual-{'MANIFEST.json'},'frozen manifest file inventory')
  for item,expected in fm['files'].items(): need(meta(ROOT/folder/item)==expected,'frozen manifest bytes')
 status=parse(ROOT/'release_status.json')
 need(status['problem_id']==30003264 and status['rank']==733,'disposition identity')
 need(status['status']=='unsolved' and status['turns']=='5/5' and status['substantive_approaches_used']==5,'disposition budget')
 need(status['independent_audit']=='PASS_SCOPED_PRIMARY_UNRESOLVED','audit scope')
 need(status['frozen_packet_corrections_required']==[],'frozen correction state')
 need(all(status[k] is False for k in ['primary_problem_solved','primary_problem_disproved','novelty_or_priority_certified','human_peer_review']),'overstated disposition')
 verdict=parse(ROOT/'audit/VERDICT.json')
 need(verdict['primary_problem_status']=='UNRESOLVED' and verdict['substantive_approaches_used']==5 and verdict['verdict']=='PASS','frozen verdict')
 return len(files)+1
def run(script,optimized,args=()):
 r=subprocess.run([sys.executable,'-I','-B',*(['-O'] if optimized else []),str(script),*map(str,args)],cwd=ROOT,capture_output=True,timeout=180)
 need(r.returncode==0 and r.stderr==b'','replay failed: '+script.name)
 return r.stdout
def main():
 count=inventory()
 author=[];audit=[]
 for optimized in [False,True]:
  a=run(ROOT/'author/verify.py',optimized)
  need(sha(a)==AUTHOR_REPLAY_SHA,'author replay bytes');author.append(a)
  b=run(ROOT/'audit/independent_verify.py',optimized,[ROOT/ARCHIVES['author'][0]])
  need(b==(ROOT/'audit/INDEPENDENT_VERIFICATION.json').read_bytes(),'independent replay bytes');audit.append(b)
 need(author[0]==author[1] and audit[0]==audit[1],'optimization independence')
 controls=json.loads(audit[0])
 print(json.dumps({'problem_id':30003264,'status':'unsolved','turns':'5/5','file_count':count,'frozen_author_and_audit_preserved':True,'author_and_independent_normal_optimized_replays':'byte-identical','author_damage_controls':controls['author_damage_controls_rejected'],'independent_archive_mutations':controls['archive_mutations_rejected'],'independent_package_mutations':len(controls['mutations']['independent_envelope_mutations_rejected']),'arithmetic_mutations_both_modes':len(controls['mutations']['arithmetic_mutations_rejected_in_both_modes']),'scope':'Integrity and exact finite controls; primary question unresolved; no novelty certification.'},indent=2,sort_keys=True))
if __name__=='__main__': main()
