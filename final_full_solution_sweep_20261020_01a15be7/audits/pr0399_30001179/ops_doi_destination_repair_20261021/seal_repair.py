#!/usr/bin/env python3
"""Seal/verify this exact local destination repair and preserved356 lineage."""
from pathlib import Path,PurePosixPath
import argparse,datetime as dt,hashlib,json,os
H=Path(__file__).resolve().parent;A=H.parent;O=H/'pre_destination_binding'
HELPERS={'ops_binding.py','prepublication_check.py','publication_live_gates.py','repository_integration.py','verify_published_files.py','publication_lifecycle.py','record_publication_ledger.py'}
OLD='151a3c3c1dffa10750fad0ba8fdb189ba27698c30c3d0d2c000c98dbc48e732b'

def sha(b):return hashlib.sha256(b).hexdigest()
def entry(root,name):
 if not isinstance(name,str) or not name or '\\' in name or ':' in name or '\0' in name or any(x in {'','.','..'} for x in name.split('/')):raise RuntimeError('Unsafe path')
 p=PurePosixPath(name)
 if p.is_absolute() or p.as_posix()!=name or root.is_symlink() or any(root.joinpath(*p.parts[:i]).is_symlink() for i in range(1,len(p.parts)+1)):raise RuntimeError('Unsafe/symlink path')
 b=(root/name).read_bytes();return {'path':name,'bytes':len(b),'sha256':sha(b)}
def verify(root,entries):
 if not isinstance(entries,list) or not entries:raise RuntimeError('Missing inventory')
 seen=set()
 for e in entries:
  if set(e)!={'path','bytes','sha256'} or type(e['bytes']) is not int or e['path'] in seen or entry(root,e['path'])!=e:raise RuntimeError('Changed/duplicate artifact '+str(e.get('path')))
  seen.add(e['path'])
 return seen

def preserved():
 old='ops_record_url_repair_20261021/MANIFEST.json'
 if sha((A/old).read_bytes())!=OLD or (A/old).read_bytes()!=(O/old).read_bytes():raise RuntimeError('Previous356 seal changed')
 if (A/'ops_record_url_repair_20261021/MANIFEST.sha256').read_text()!=OLD+'  MANIFEST.json\n':raise RuntimeError('Previous checksum changed')
 data=json.loads((H/'INPUT_PRESERVATION.json').read_bytes());entries=data['complete_context_files']
 if len(entries)!=631 or len(data['previous356_files'])!=356 or len(data['previous56_immutable_inputs'])!=56:raise RuntimeError('Prior inventory counts changed')
 verify(O,entries);verify(A,[e for e in entries if e['path'] not in HELPERS])
 inputs=json.loads((H/'IMMUTABLE_INPUT_BINDING.json').read_bytes())['files'];verify(A,inputs)
 if inputs!=[e for e in entries if e['path'] not in HELPERS]:raise RuntimeError('Immutable context differs')
 current=json.loads((H/'CURRENT_HELPER_BINDING.json').read_bytes())['files']
 if verify(A,current)!=HELPERS:raise RuntimeError('Seven-helper set differs')
 summary=json.loads((H/'TEST_SUMMARY.json').read_bytes())
 if summary['helper_bindings']!=current or any(m['current_controls']!=1876 or m['actual_provider_attempts'] for m in summary['modes']):raise RuntimeError('Current test binding differs')
 return inputs

def selection():
 inputs=preserved();all_paths=list(H.rglob('*'))
 if any(p.is_symlink() for p in all_paths):raise RuntimeError('Symlink authored artifact')
 excluded={H/'MANIFEST.json',H/'MANIFEST.sha256'};paths=[A/n for n in HELPERS]+[p for p in all_paths if p.is_file() and p not in excluded and '__pycache__' not in p.parts]
 if len(paths)!=len(set(paths)):raise RuntimeError('Duplicate authored inventory')
 return sorted(paths),inputs

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--verify',action='store_true');args=parser.parse_args();paths,inputs=selection();manifest=H/'MANIFEST.json';checksum=H/'MANIFEST.sha256'
 if args.verify:
  data=manifest.read_bytes();value=json.loads(data)
  if checksum.read_text()!=sha(data)+'  MANIFEST.json\n' or value['publication_ready'] is not False or value['immutable_inputs']!=inputs:raise RuntimeError('Manifest scope/checksum differs')
  if {e['path'] for e in value['files']}!={p.relative_to(A).as_posix() for p in paths}:raise RuntimeError('Authored inventory differs')
  verify(A,value['files']);verify(A,inputs);print(json.dumps({'verified':True,'artifacts':len(value['files']),'immutable_inputs':len(inputs),'manifest_sha256':sha(data),'preserved356':True,'current_controls_per_mode':1876,'publication_ready':False}));return
 if manifest.exists() or checksum.exists():raise RuntimeError('Never overwrite a frozen checkpoint')
 value={'schema':1,'timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'pr':399,'problem_id':'30001179','completion_estimate_percent':100,'publication_ready':False,'scope':'Bounded local DOI destination repair; NEW complete history-free review05 and root decision required. No provider/Git/state/ledger mutation or clearance.','previous356_manifest_sha256':OLD,'review04_manifest_sha256':'4822b258611ad2a7ddb57a5f4db2137ee1b8752883d9c50ef94923435f90d678','current_controls_per_mode':1876,'files':[entry(A,p.relative_to(A).as_posix()) for p in paths],'immutable_inputs':inputs}
 data=(json.dumps(value,indent=2)+'\n').encode()
 for p,b in [(manifest,data),(checksum,(sha(data)+'  MANIFEST.json\n').encode())]:
  with p.open('xb') as stream:stream.write(b);stream.flush();os.fsync(stream.fileno())
 print(json.dumps({'artifacts':len(value['files']),'immutable_inputs':len(inputs),'manifest_sha256':sha(data),'publication_ready':False}))
if __name__=='__main__':main()
