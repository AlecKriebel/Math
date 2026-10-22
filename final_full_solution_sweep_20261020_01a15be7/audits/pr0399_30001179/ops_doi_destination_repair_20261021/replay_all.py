#!/usr/bin/env python3
"""Replay final DOI-destination and all1651 previous controls into new private custody."""
from pathlib import Path
import argparse,hashlib,io,json,sys,types
from contextlib import redirect_stdout
H=Path(__file__).resolve().parent;A=H.parent

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args();out=args.output
 if not out.is_absolute() or not out.is_relative_to(A.parents[1]/'private') or any(p.is_symlink() for p in [out,*out.parents]):raise RuntimeError('New absolute private output without symlinks required')
 out.mkdir(parents=True,exist_ok=False)
 for e in json.loads((H/'CURRENT_HELPER_BINDING.json').read_bytes())['files']:
  b=(A/e['path']).read_bytes()
  if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:raise RuntimeError('Current helper binding changed')
 if (H/'MANIFEST.json').exists():
  value=json.loads((H/'MANIFEST.json').read_bytes())
  for e in value['files']+value['immutable_inputs']:
   b=(A/e['path']).read_bytes()
   if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:raise RuntimeError('Frozen replay input changed')
 prior=sys.argv;sources=[]
 try:
  for name,directory in [('destination_controls.py','destination'),('replay_1651.py','previous')]:
   path=H/name;body=path.read_bytes();module=types.ModuleType('fresh_private_'+directory);module.__file__=str(path);sys.argv=[str(path),'--output',str(out/directory)]
   exec(compile(body,str(path),'exec'),module.__dict__)
   with redirect_stdout(io.StringIO()):module.main()
   sources.append({'path':name,'sha256':hashlib.sha256(body).hexdigest()})
 finally:sys.argv=prior
 current=json.loads((out/'destination/DESTINATION_CONTROLS.json').read_bytes());previous=json.loads((out/'previous/REPLAY_1651.json').read_bytes())
 if current['new_destination_controls']!=170 or current['review04_other_controls']!=55 or previous['all_previous_controls']!=1651 or not current['all_passed'] or not previous['all_passed'] or current['actual_provider_attempts'] or previous['actual_provider_attempts']:raise RuntimeError('Required final obligations not met')
 result={'optimization':sys.flags.optimize,'new_destination_controls':170,'review04_other_controls':55,'previous_controls':1651,'total_current_controls':1876,'all_passed':True,'actual_provider_attempts':0,'cached_rows_separate':176,'executed_programs':sources,'audit_outputs_written':False,'publication_ready':False}
 (out/'REPLAY_ALL.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
