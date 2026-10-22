#!/usr/bin/env python3
"""Read-only packet integrity and portable exact finite replay; standard library only."""
import argparse,base64,hashlib,io,json,os,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent
SPECS=[
 ('CODING_EFFICIENCY_30005026_AUTHOR_SAFE_FREEZE.zip','author','coding_efficiency_30005026',18242,'fab6977b8eb55254fc133e04341e435e45c4d22afa08070137afc58d74280eab','AUTHOR_MANIFEST.json','51e81798b0886a5434b893db4c91d13fde13f85588e8bba893bc2041f1c6f5d6',11),
 ('CODING_EFFICIENCY_30005026_INDEPENDENT_AUDIT_SAFE.zip','audit','coding_efficiency_30005026_audit',24431,'61bc2a273f9ba6960a01cbe3b42fd7aec4d1c8d349191e8783642e42878b6b97','MANIFEST.json','992a9e4f2f51baef9635c7f35e19e397bb2f5408711a553e3e04c43c891a0236',18)]
def require(ok,label):
 if not ok: raise ValueError(label)
def meta(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def expected_dirs(files): return {p.as_posix() for n in files for p in PurePosixPath(n).parents if p.as_posix()!='.'}
def inventory(root):
 require(not root.is_symlink(),'Symlink root')
 files,dirs=set(),set()
 for p in root.rglob('*'):
  n=p.relative_to(root).as_posix();require(not p.is_symlink(),'Symlink entry')
  if p.is_dir(): dirs.add(n)
  else: require(p.is_file(),'Nonregular entry');files.add(n)
 return files,dirs
def rows_check(root,rows,files):
 require(len(rows)==len({r['path'] for r in rows}),'Duplicate manifest entry')
 require({r['path'] for r in rows}==files,'Manifest file set')
 for r in rows:
  p=PurePosixPath(r['path']);require(not p.is_absolute() and '..' not in p.parts and p.as_posix()==r['path'],'Unsafe manifest path')
  require(meta((root/r['path']).read_bytes())=={k:r[k] for k in ('bytes','sha256')},'Changed member: '+r['path'])
def integrity(root,expected_manifest=None):
 root=Path(root);require(__debug__ and sys.flags.optimize==0,'Assertions must remain enabled; no -O or PYTHONOPTIMIZE')
 raw=(root/'PUBLICATION_MANIFEST.json').read_bytes();pin=meta(raw)['sha256']
 if expected_manifest: require(pin==expected_manifest,'External publication manifest pin')
 rows=json.loads(raw)['files'];want={r['path'] for r in rows}|{'PUBLICATION_MANIFEST.json'}
 require(inventory(root)==(want,expected_dirs(want)),'Exact recursive inventory')
 rows_check(root,rows,want-{'PUBLICATION_MANIFEST.json'})
 for name,folder,prefix,size,digest,mname,mpin,count in SPECS:
  frozen=root/folder;m=(frozen/mname).read_bytes();require(meta(m)['sha256']==mpin,'Frozen manifest pin')
  rows=json.loads(m)['files'];names={r['path'] for r in rows}|{mname}
  require(len(names)==count and inventory(frozen)==(names,expected_dirs(names)),'Frozen recursive inventory')
  rows_check(frozen,rows,names-{mname})
  enc=(root/'frozen_archives'/(name+'.b64')).read_bytes();data=base64.b64decode(enc.strip(),validate=True)
  require(base64.b64encode(data)+b'\n'==enc,'Canonical archive encoding');require(meta(data)=={'bytes':size,'sha256':digest},'Original ZIP identity')
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   entries=z.infolist();expected={prefix+'/'+n for n in names}
   require(len(entries)==count and {m.filename for m in entries}==expected,'ZIP exact member set');require(z.testzip() is None,'ZIP CRC')
   for member in entries:
    p=PurePosixPath(member.filename)
    require(len(p.parts)==2 and p.parts[0]==prefix and '..' not in p.parts and not p.is_absolute(),'Unsafe ZIP path')
    require(not member.is_dir() and not stat.S_ISLNK(member.external_attr>>16) and not member.flag_bits&1,'Unsafe ZIP member')
    require(z.read(member)==(frozen/p.name).read_bytes(),'ZIP/directory byte mismatch')
 require((root/'SOURCE_CORRECTIONS.md').read_bytes()==(root/'audit/CORRECTIONS.md').read_bytes(),'Source corrections addendum changed')
 return {'publication_manifest_sha256':pin,'packet_files':len(want)}
def run(script,*args):
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 return subprocess.check_output([sys.executable,'-B',str(script),*map(str,args)],env=env,timeout=120)
def queue_check(root,before,after):
 d=json.loads((root/'QUEUE_DELTA.json').read_bytes());b=Path(before).read_bytes();a=Path(after).read_bytes()
 require(meta(b)==d['before'] and meta(a)==d['after'],'Complete queue hashes')
 lines=b.splitlines(keepends=True);matches=[i for i,l in enumerate(lines) if b'| 30005026 / OWR-9790359-007 |' in l];require(len(matches)==1,'Exact queue target match')
 i=matches[0];fields=lines[i].split(b'|');require(fields[8:10]==[b' queued ',b' 0/5 '],'Queue old fields')
 fields[8:10]=[b' unsolved ',b' 5/5 '];lines[i]=b'|'.join(fields)
 require(b''.join(lines)==a,'Only Status and Turns may change; preserve every other byte')
 return 'PASS_EXACT_FULL_BYTES'
def verify(root=ROOT,expected_manifest=None,before=None,after=None):
 root=Path(root).resolve();result=integrity(root,expected_manifest)
 author=run(root/'author/verify.py');require(author==(root/'author/results.json').read_bytes(),'Author exact-byte replay')
 require(json.loads(author)==json.loads((root/'audit/AUTHOR_REPLAY.json').read_bytes()),'Audit author replay agreement')
 rebuilt=run(root/'audit/reconstruct_author_scope.py');require(rebuilt==(root/'audit/RECONSTRUCTED_RESULTS.json').read_bytes(),'Reconstruction exact-byte replay')
 independent=run(root/'audit/independent_controls.py');require(independent==(root/'audit/INDEPENDENT_RESULTS.json').read_bytes(),'Independent exact-byte replay')
 require(json.loads(author)['assertions']==141484 and json.loads(rebuilt)['assertions']==141484 and json.loads(independent)['assertions']==46913,'Exact assertion counts')
 with tempfile.TemporaryDirectory(prefix='coding-publication-') as tmp:
  name=SPECS[0][0];p=Path(tmp)/name;p.write_bytes(base64.b64decode((root/'frozen_archives'/(name+'.b64')).read_bytes(),validate=False))
  audit=json.loads(run(root/'audit/verify_audit.py',p))
 require(audit['status']=='PASS' and audit['author_assertions']==141484 and audit['independently_reconstructed_assertions']==141484 and audit['additional_independent_assertions']==46913,'Frozen audit replay')
 status=json.loads((root/'audit/STATUS.json').read_bytes())
 require(status['original_finite_valued_target']=='UNRESOLVED' and status['approaches_used']==5 and status['approach_limit']==5,'Original target scope')
 require(status['verdict']=='PASS_SCOPED_WITH_NONBLOCKING_SOURCE_ERRATA' and not status['external_theorems_independently_reproved'] and not status['novelty_claim'] and not status['journal_peer_review_claim'],'Qualified audit scope')
 independent=json.loads(independent);require(independent['finite_maps_exhausted']==6672 and len(independent['negative_controls_rejected'])==3 and all(independent['negative_controls_rejected'].values()),'Independent mathematical negative controls')
 require((before is None)==(after is None),'Supply both queue inputs or neither')
 queue=queue_check(root,before,after) if before else 'NOT_RUN_EXTERNAL_QUEUE_INPUTS_REQUIRED'
 require(integrity(root,expected_manifest)==result,'Replay altered packet')
 result.update(status='PASS',problem_id='30005026',assertions_enabled=True,author_assertions=141484,independently_reconstructed_assertions=141484,additional_independent_assertions=46913,independent_finite_maps=6672,mathematical_negative_controls=3,replays_byte_identical=True,both_frozen_archives_verified=True,source_corrections_addendum_verified=True,original_target='UNSOLVED',approaches_used='5/5',queue_delta=queue,external_source_metadata_replay='NOT_RUN_BY_THIS_COMMAND_EXTERNAL_INPUTS_REQUIRED',finite_checks_are_formal_proof=False,hosted_ci_pass_claimed=False)
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',default=str(ROOT));p.add_argument('--expected-manifest');p.add_argument('--queue-before');p.add_argument('--queue-after');a=p.parse_args()
 print(json.dumps(verify(a.root,a.expected_manifest,a.queue_before,a.queue_after),indent=2,sort_keys=True))
