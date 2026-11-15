#!/usr/bin/env python3
"""Default read-only exact14 preflight. --capture writes only this preparation namespace."""
import sys
sys.dont_write_bytecode=True
import argparse,json
from exact14_lib import O,S,BASE,STAGE_SEAL,need,now,sha,read,obj,stage_fences,website_git_state

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--capture',action='store_true');parser.add_argument('--installed',action='store_true');args=parser.parse_args()
 mode='installed'if args.installed else'baseline';overlay,summary=stage_fences(mode);raw,index,state=website_git_state(overlay)
 result={'UTC':now(),'status':'PASS_READ_ONLY_PREFLIGHT','website_mode':mode,'baseline_HEAD':BASE,'stage_final_seal_SHA256':STAGE_SEAL,'stage_and_website':summary,'Git':state,'website_or_Git_mutations':False,'stage_code_executed':False,'production_install_authorized':False}
 if args.capture:
  need(not args.installed,'capture records only original baseline')
  need(not(O/'PREFLIGHT_CAPTURE.json').exists(),'preserve existing preflight capture')
  protected=b'\0'.join(path+b'\t'+record.hex().encode()for path,record in index['protected'])+b'\0'
  need(sha(protected)==state['protected_raw_records_SHA256'],'actual complete protected record bytes')
  (O/'private/shared-index.before').write_bytes(raw);(O/'private/protected-index.raw-records').write_bytes(protected)
  need(read(Path(state['gitdir'])/'index')==raw,'shared index unchanged during capture')
  result['complete_protected_records_path']='private/protected-index.raw-records';result['whole_original_index_snapshot_path']='private/shared-index.before'
  (O/'PREFLIGHT_CAPTURE.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':
 from pathlib import Path
 main()
