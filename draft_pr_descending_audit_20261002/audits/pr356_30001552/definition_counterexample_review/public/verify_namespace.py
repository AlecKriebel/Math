#!/usr/bin/env python3
"""Read-only namespace and retained-byte verifier. It never runs math programs."""
from pathlib import Path
from datetime import datetime
import argparse,hashlib,json,sys

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path): return json.loads(path.read_text())
def relative_files(base,prefix):
 folder=base/prefix
 return {str(p.relative_to(base)) for p in folder.rglob('*') if p.is_file()}

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parent.parent)
 ap.add_argument('--mode',choices=('auto','public','full'),default='auto')
 ap.add_argument('--candidate-root',type=Path,help='Optional full-mode frozen problem directory for actual candidate code pins; never executed.')
 args=ap.parse_args();root=args.root.resolve()
 mode=args.mode
 if mode=='auto': mode='full' if (root/'private/PRIVATE_MANIFEST.json').is_file() else 'public'
 errors=[];checks=[];limitations=[]
 def check(name,condition,detail=None):
  checks.append({'check':name,'pass':bool(condition),'detail':detail})
  if not condition: errors.append(name)
 def inventory(filename,scope,exclusions):
  path=root/filename
  if not path.is_file():
   check(filename+' present',False,'Package manifests are generated once after approval. Missing means unsealed/unavailable, not a mathematical failure.');return None
  data=load(path);records=data.get('files',[]);listed=set()
  for record in records:
   rel=record['path'];parts=Path(rel).parts
   safe=not Path(rel).is_absolute() and '..' not in parts and parts and parts[0]==scope
   check('safe manifest path '+rel,safe)
   if not safe:continue
   listed.add(rel);actual=root/rel
   check('retained file '+rel,actual.is_file() and not actual.is_symlink())
   if actual.is_file() and not actual.is_symlink():
    check('SHA256 '+rel,sha(actual)==record['sha256'])
    check('byte length '+rel,actual.stat().st_size==record['bytes'])
  actual=relative_files(root,scope)-set(exclusions)
  check(scope+' exact inventory',actual==listed,{'unexpected':sorted(actual-listed),'missing':sorted(listed-actual)})
  return data
 public=inventory('public/PUBLIC_MANIFEST.json','public',['public/PUBLIC_MANIFEST.json'])
 if public is None:
  print(json.dumps({'status':'UNSEALED_OR_MISSING','mode':mode,'checks':checks,'limitations':['No math program was run.'],'errors':errors},indent=2));return 2
 receipts=load(root/'public/REPLAY_RECEIPTS.json')
 for run in ('author','portable_public'):
  record=receipts[run];stream=root/'public/native_streams'/(run+'.stdout')
  check('public native stdout '+run,sha(stream)==record['stdout_sha256'])
  check('public native stdout byte length '+run,stream.stat().st_size==record['stdout_bytes'])
  check('recorded public expected-stream match '+run,record['exit_code']==0 and record['exact_expected_stream_equal'] is True)
 independent=receipts['independent_constraint_falsifiers']
 check('public independent saved stdout SHA256',sha(root/'public/EXPECTED_CHECKS.json')==independent['stdout_sha256'])
 check('public independent saved stdout length',(root/'public/EXPECTED_CHECKS.json').stat().st_size==independent['stdout_bytes'])
 check('public independent program pin',sha(root/'public/verify_constraints.py')==independent['program_sha256'])
 limitations.extend(['This verifies retained bytes, inventories and recorded execution metadata; it does not rerun or independently prove mathematics.','Saved stream equality is checked against retained receipt hashes; historical execution timing/provenance is not newly witnessed.','No novelty or priority claim is verified.'])
 if mode=='public':
  limitations.extend(['Public-only mode does not read or require private manifests, raw failed traces, source baseline, pre-execution records or private closure seal.','Actual frozen candidate code and private source5 bindings cannot be verified from the curated public files.','The optional original 68413 receipt remains unreproduced; public streams cover author526887 and portable68408.'])
  if args.candidate_root: limitations.append('--candidate-root is ignored in public-only mode.')
 else:
  private=inventory('private/PRIVATE_MANIFEST.json','private',['private/PRIVATE_MANIFEST.json','private/PACKAGE_SEAL.json','private/PACKAGE_SEAL.sha256'])
  if private is not None:
   for run in ('author','original_independent_literal','portable_public'):
    cap=root/'private/candidate_replays';before=load(cap/(run+'.before.json'));after=load(cap/(run+'.after.json'))
    for channel in ('stdout','stderr'):
     actual=cap/(run+'.'+channel)
     check('private native '+run+' '+channel+' SHA256',sha(actual)==after[channel+'_sha256'])
     check('private native '+run+' '+channel+' length',actual.stat().st_size==after[channel+'_bytes'])
    check('native receipt metadata '+run,after==receipts[run])
    check('candidate replay runner pin '+run,sha(root/'private/run_frozen_replays.py')==before['runner_sha256'])
    check('recorded before/after timestamps '+run,datetime.fromisoformat(before['timestamp_utc'])<=datetime.fromisoformat(after['timestamp_utc']))
    if args.candidate_root:
     for rel,value in before['packet_files_sha256'].items():
      actual=args.candidate_root/rel
      check('actual candidate pre-code pin '+run+' '+rel,actual.is_file() and sha(actual)==value)
    else: limitations.append('Actual candidate files for '+run+' were not supplied; retained pre-execution code pins are inventoried but no current candidate binding is claimed.')
   before=load(root/'private/independent_constraints.before.json');after=load(root/'private/independent_constraints.after.json')
   check('independent pre-execution code pin',sha(root/'private/independent_constraints.py')==before['program_sha256']==after['program_sha256'])
   check('independent public/private code identity',sha(root/'public/verify_constraints.py')==sha(root/'private/independent_constraints.py'))
   for channel in ('stdout','stderr'):
    actual=root/'private'/('independent_constraints.'+channel)
    check('independent native '+channel+' SHA256',sha(actual)==after[channel+'_sha256'])
    check('independent native '+channel+' length',actual.stat().st_size==after[channel+'_bytes'])
   check('independent recorded before/after timestamps',datetime.fromisoformat(before['timestamp_utc'])<=datetime.fromisoformat(after['timestamp_utc']))
   gate=load(root/'private/source_first_gate.json')
   for record in gate['files']:
    check('source-first baseline pin '+record['path'],sha(root/record['path'])==record['sha256'])
   check('source-first gate pin',sha(root/'private/source_first_gate.json')==(root/'private/source_first_gate.sha256').read_text().split()[0])
   seal_path=root/'private/PACKAGE_SEAL.json';seal_pin=root/'private/PACKAGE_SEAL.sha256'
   check('private one-time seal and pin present',seal_path.is_file() and seal_pin.is_file())
   if seal_path.is_file() and seal_pin.is_file():
    seal=load(seal_path)
    check('one-time closure seal SHA256',sha(seal_path)==seal_pin.read_text().split()[0])
    check('closure public-manifest pin',sha(root/'public/PUBLIC_MANIFEST.json')==seal['public_manifest_sha256'])
    check('closure private-manifest pin',sha(root/'private/PRIVATE_MANIFEST.json')==seal['private_manifest_sha256'])
   limitations.extend(['External historical original source bytes, repository history, API captures and local Git object binding are outside this namespace verifier.','The literal original independent checker failed before mathematical loops; its failure stream is retained, not converted to a successful68413 replay.'])
 print(json.dumps({'status':'PASS' if not errors else 'FAIL','mode':mode,'namespace_integrity_only':True,'implicit_math_reruns':False,'mutations':False,'checks':checks,'limitations':limitations,'errors':errors},indent=2))
 return 0 if not errors else 1

if __name__=='__main__':
 try: sys.exit(main())
 except (OSError,ValueError,KeyError,TypeError) as error:
  print(json.dumps({'status':'FAIL','namespace_integrity_only':True,'implicit_math_reruns':False,'mutations':False,'error_type':type(error).__name__,'error':str(error)},indent=2));sys.exit(1)
