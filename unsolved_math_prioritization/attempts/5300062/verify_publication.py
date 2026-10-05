#!/usr/bin/env python3
"""Strict portable publication replay; no network and no source inputs required."""
import argparse,base64,hashlib,io,json,os,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent

def require(ok,why):
 if not ok:raise RuntimeError(why)
def meta(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def expected_dirs(names):return {str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.'}
def inventory(root):
 require(not root.is_symlink(),'Symlink root');files=set();dirs=set()
 for p in root.rglob('*'):
  n=p.relative_to(root).as_posix();require(not p.is_symlink(),'Symlink entry')
  if p.is_dir():dirs.add(n)
  else:require(p.is_file(),'Nonregular entry');files.add(n)
 return files,dirs
def check_manifest(root,name,anchor):
 raw=(root/name).read_bytes();require(meta(raw)['sha256']==anchor,'External manifest anchor: '+name)
 rows=json.loads(raw)['files'];names={r['path'] for r in rows};require(len(names)==len(rows),'Duplicate manifest path')
 require(name not in names,'Self-referential manifest');want=names|{name}
 require(inventory(root)==(want,expected_dirs(want)),'Strict recursive inventory: '+str(root.name))
 for r in rows:
  p=PurePosixPath(r['path']);require(not p.is_absolute() and '..' not in p.parts and str(p)==r['path'],'Unsafe path')
  require(meta((root/r['path']).read_bytes())=={k:r[k] for k in ('bytes','sha256')},'Content mismatch: '+r['path'])
 return want
def integrity(root,anchor):
 require(sys.flags.optimize==0,'Optimized Python is unsupported')
 want=check_manifest(root,'PUBLICATION_MANIFEST.json',anchor)
 specs=json.loads((root/'FREEZE_BINDINGS.json').read_bytes())['archives'];require(len(specs)==4,'Four freezes required')
 for s in specs:
  sub=root/s['directory'];names=check_manifest(sub,'MANIFEST.json',s['manifest_sha256']);require(len(names)==s['files'],'Frozen file count')
  enc=(root/'frozen_archives'/(s['archive']+'.b64')).read_bytes();raw=base64.b64decode(enc.strip(),validate=True)
  require(base64.b64encode(raw)+b'\n'==enc,'Noncanonical archive encoding')
  require(meta(raw)=={k:s[k] for k in ('bytes','sha256')},'ZIP external anchor')
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   members=z.infolist();require(len(members)==len(names) and {m.filename for m in members}==names,'ZIP exact inventory');require(z.testzip() is None,'ZIP CRC')
   for m in members:
    p=PurePosixPath(m.filename);require(not p.is_absolute() and '..' not in p.parts and str(p)==m.filename,'Unsafe ZIP path')
    require(not m.is_dir() and not stat.S_ISLNK(m.external_attr>>16) and not m.flag_bits&1,'Unsafe ZIP member')
    require(z.read(m)==(sub/m.filename).read_bytes(),'ZIP/directory byte mismatch')
 return {'publication_manifest_sha256':anchor,'packet_files':len(want),'all_four_archives_and_manifests':'PASS','strict_recursive_inventory':'PASS'}
def run(script,*args):
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 return subprocess.check_output([sys.executable,'-B',str(script),*map(str,args)],env=env,timeout=150)
def queue_check(root,before,after):
 d=json.loads((root/'QUEUE_DELTA.json').read_bytes());b=Path(before).read_bytes();a=Path(after).read_bytes()
 require(meta(b)==d['before'] and meta(a)==d['after'],'Full queue identity')
 lines=b.splitlines(True);ix=[i for i,l in enumerate(lines) if b'| 5300062 / AMR-052-0062 |' in l];require(len(ix)==1,'Unique target row')
 i=ix[0];fields=lines[i].split(b'|');require(fields[8:10]==[b' queued ',b' 0/5 '],'Old fields')
 fields[8:10]=[b' unsolved ',b' 5/5 '];lines[i]=b'|'.join(fields);require(b''.join(lines)==a,'Only Status and Turns may change')
 return 'PASS_EXACT_FULL_BYTES'
def verify(root,anchor,before=None,after=None,integrity_only=False):
 root=Path(root).resolve();result=integrity(root,anchor);require((before is None)==(after is None),'Supply both queue inputs')
 result['queue_delta']=queue_check(root,before,after) if before else 'NOT_RUN_EXTERNAL_QUEUE_INPUTS_REQUIRED'
 if integrity_only:return result
 specs=json.loads((root/'FREEZE_BINDINGS.json').read_bytes())['archives'];replays={}
 for s in specs:
  replays[s['directory']]=json.loads(run(root/s['directory']/'verify.py','--expected-manifest',s['manifest_sha256']))
 with tempfile.TemporaryDirectory(prefix='hairs-publication-inputs-') as td:
  inputs={}
  for s in specs:
   p=Path(td)/s['archive'];p.write_bytes(base64.b64decode((root/'frozen_archives'/(s['archive']+'.b64')).read_bytes()));inputs[s['directory']]=p
  acceptance=json.loads(run(root/'v2_acceptance/verify.py','--expected-manifest',specs[3]['manifest_sha256'],'--original',inputs['author_v1'],'--v2',inputs['author_v2'],'--audit',inputs['audit_v1']))
 require(acceptance['bounded_delta_replay']=='EXACT_RESULT_BYTES' and acceptance['verdict']=='ACCEPT_SCOPED_PARTIAL_V2' and acceptance['general_problem_status']=='UNSOLVED','Exact accepted scope')
 require(replays['audit_v1']['mathematical_verdict']=='REPAIR_REQUIRED_V1','Historical verdict must remain')
 acceptance_controls=run(root/'v2_acceptance/code/test_verifier.py')
 require(acceptance_controls==(root/'v2_acceptance/results/integrity_controls.json').read_bytes(),'Acceptance integrity-control replay')
 require(integrity(root,anchor)=={k:result[k] for k in ['publication_manifest_sha256','packet_files','all_four_archives_and_manifests','strict_recursive_inventory']},'Replay modified packet')
 result.update(status='PASS',problem_id=5300062,general_status='UNSOLVED',approaches_used='5/5',verdict='ACCEPT_SCOPED_PARTIAL_V2',historical_verdict_preserved='REPAIR_REQUIRED_V1',replays=replays,bounded_delta=acceptance,acceptance_integrity_controls='EXACT_RESULT_BYTES',numerical_controls_interval_certified=False,formal_proof_claim=False,novelty_claim=False,human_peer_review_claim=False,hosted_ci_pass_claimed=False)
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--expected-manifest',required=True);p.add_argument('--queue-before');p.add_argument('--queue-after');p.add_argument('--integrity-only',action='store_true');a=p.parse_args()
 print(json.dumps(verify(ROOT,a.expected_manifest,a.queue_before,a.queue_after,a.integrity_only),indent=2,sort_keys=True))
