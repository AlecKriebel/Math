"""Final native whole-evidence authentication; no repeated scientific suite."""
from pathlib import Path
from datetime import datetime
import gzip, json, os, stat
from capture import HERE,pin,write,now,digest
A=HERE.parent;F=A/'preprint_package_v02'
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def match(row,mode=True):
 p=Path(row['path']);need(p.is_file(),'Missing input '+str(p));g=pin(p)
 need(all(g[k]==row[k]for k in (('bytes','sha256','mode')if mode else('bytes','sha256'))),'Pin differs '+str(p));return p
def stream(row):
 b=gzip.decompress(match(row['stored']).read_bytes());need(len(b)==row['logical_bytes']and digest(b)==row['logical_sha256'],'Stream logical digest');return b
def main():
 need(__import__('sys').flags.optimize==0,'Optimization')
 doc=json.loads((F/'SECOND_CANDIDATE_MANIFEST.json').read_text());need(pin(F/'SECOND_CANDIDATE_MANIFEST.json')['sha256']=='b38a09c6768e11c2954892cdaa345a485557082c464d950f573a945f48b5ec71','Candidate identity')
 for r in doc['files']:need(pin(r['path'])['mode']==0o444,'Public not frozen');match(r)
 need(len(doc['files'])==23,'Public count')
 index=json.loads((HERE/'SOURCE_ARCHIVE_INDEX.json').read_text());need(index['all_requested_primary_bodies_included'],'Primary archive incomplete')
 for r in index['complete_body_copies']:
  original=match(r['original']);copy=match(r['complete_copy']);b=gzip.decompress(copy.read_bytes())
  need(len(b)==r['logical_bytes']and digest(b)==r['logical_sha256']and b==original.read_bytes(),'Archived complete body differs')
 for r in index['unredistributed_external_binary_anchors']:match(r['input'])
 parent_runs=[]
 for label in ['fresh_portable_replay','pdf_text','package_evidence_crosscheck','package_evidence_crosscheck_v02']:
  folder=HERE/'process_evidence'/label;run=json.loads((folder/'execution.json').read_text());request=json.loads((folder/'request.json').read_text());start=json.loads((folder/'started.json').read_text())
  need(run['actual_child_PID']==start['actual_child_PID']and run['argv']==start['argv']and run['cwd']==start['cwd'],'Actual start identity')
  for k,v in request.items():need(run[k]==v,'Request differs')
  need(datetime.fromisoformat(run['requested_UTC'])<=datetime.fromisoformat(run['started_UTC'])<=datetime.fromisoformat(run['completed_UTC']),'Times')
  match(run['interpreter']);match(run['recorder_source'])
  for r in run['sources_before']:
   original=match(r['original']);copy=match(r['stored']);b=gzip.decompress(copy.read_bytes());need(b==original.read_bytes()and len(b)==r['logical_bytes']and digest(b)==r['logical_sha256'],'Actual prelaunch source')
  out=stream(run['stdout']);err=stream(run['stderr']);expected_exit=1 if label=='package_evidence_crosscheck'else 0
  need(run['exit_code']==expected_exit,'Historical native exit differs')
  if expected_exit==0:need(not err,'Successful native stderr')
  else:need(b'Pin differs' in err and b'close_second_candidate.py' in err,'Failed checker full genuine traceback')
  parent_runs.append(dict(label=label,actual_child_PID=run['actual_child_PID'],actual_launcher_PID=run['actual_launcher_PID'],exit_code=run['exit_code'],argv=run['argv'],cwd=run['cwd'],UTC_interval=[run['started_UTC'],run['completed_UTC']],sources=len(run['sources_before']),stdout_logical_bytes=len(out),stderr_logical_bytes=len(err)))
 auth=json.loads((HERE/'AUTHENTICATION_AND_REPLAY.json').read_text());receipt=json.loads((HERE/'fresh_replay/REPLAY_RECEIPT.json').read_text())
 match(auth['actual_runner_receipt']);need(receipt['actual_launcher_PID']==45361 and len(receipt['native_executions'])==8,'Actual 8suite runner')
 children=[]
 for e in receipt['native_executions']:
  r=e['native_execution'];native=json.loads((Path(e['scientific_output']['path']).parent/'execution.json').read_text());need(native==r,'Child full receipt binding')
  need(r['actual_launcher_PID']==45361 and r['exit_code']==0 and r['runtime']['optimization']==0,'Child actual status')
  match(r['runtime']['executable']);source=match(r['source']);original=match(r['original_source']);match(r['runner_source']);need(source.read_bytes()==original.read_bytes(),'Executed child/original full body')
  stream(r['stdout']);need(not stream(r['stderr']),'Child stderr');match(e['scientific_output'])
  need(datetime.fromisoformat(r['started_UTC'])<=datetime.fromisoformat(r['completed_UTC']),'Child timing')
  children.append(dict(label=e['label'],PID=r['actual_child_PID'],exit_code=0))
 need([r['PID']for r in children]==[45375,45394,45397,45406,45407,45414,45524,45535],'Child actual PID inventory')
 for r in auth['members']:match(r['unpacked'])
 cross=json.loads((HERE/'EVIDENCE_CROSSCHECK.json').read_text());need(len(cross['full_byte_checked_pins'])==293,'Crosscheck count')
 for r in cross['full_byte_checked_pins']:match(r)
 need((HERE/'rendered_note.txt').read_bytes()==(F/'private_build_01/full_pdf_text.txt').read_bytes(),'PDF exact text')
 checkpoint=json.loads((HERE/'INDEPENDENT_RECONSTRUCTION_CHECKPOINT.json').read_text());r=json.loads((HERE/'DERIVATION_EDITORIAL_RECONCILIATION.json').read_text());need(checkpoint['derivation']['sha256']==r['literal_preserved_original']['sha256'],'Independent proof history');match(r['literal_preserved_original']);match(r['current_derivation'])
 verdict=json.loads((HERE/'VERDICT.json').read_text());need(not verdict['mandatory_unresolved_issues']and not verdict['new_nonmandatory_suggestions']and not verdict['publication_clearance'],'Verdict authority/issues')
 for k in ['candidate_manifest','PDF','ZIP','record_metadata','independent_derivation','historical_independence_checkpoint','report','reading_ledger','correction_history']:match(verdict[k])
 files=[];dirs=[]
 for p in HERE.rglob('*'):
  need(not p.is_symlink(),'Review symlink')
  if p.is_file():files.append(p)
  elif p.is_dir():dirs.append(p)
  else:raise RuntimeError('Nonregular review member')
 size=sum(p.stat().st_size for p in files);physical=sum(p.stat().st_blocks*512 for p in files)+sum(p.stat().st_blocks*512 for p in dirs)+HERE.stat().st_blocks*512
 need(size<20_000_000 and physical<20_000_000,'Own namespace exceeds20MB')
 write(HERE/'PRESEAL_CHECK.json',dict(status='PASS_FINAL_FULL_EVIDENCE_AUTHENTICATION_WITHOUT_SCIENCE_RERUN',UTC=now(),actual_checker_PID=os.getpid(),executed_source=pin(__file__),public_files=23,complete_source_archives=len(index['complete_body_copies']),external_binary_anchors=len(index['unredistributed_external_binary_anchors']),actual_parent_records=parent_runs,actual_eight_children=children,full_crosschecked_pins=293,original_blobs=29,first_archived_public_files=23,floating_comparison='Existing independent actual comparison4077exact+19floating diagnostics retained; no scientific rerun here.',stored_bytes=size,physical_bytes=physical,literal_files_before_this_check_output=len(files),mode_epoch='All reviewer receipts describe actual prefreeze modes. Final local custody freeze changes own files to0444/directories0555 and is a later distinct epoch.',candidate_modified=False,authority=False))
 print(json.dumps(dict(status='PASS_FINAL_FULL_EVIDENCE_AUTHENTICATION',actual_checker_PID=os.getpid(),source_archives=len(index['complete_body_copies']),historical_parent_PIDs=[r['actual_child_PID']for r in parent_runs],control_PIDs=[r['PID']for r in children],current_stored_bytes=size,current_physical_bytes=physical)))
if __name__=='__main__':main()
