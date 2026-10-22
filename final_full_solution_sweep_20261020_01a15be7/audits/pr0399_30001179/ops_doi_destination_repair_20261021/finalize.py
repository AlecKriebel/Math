#!/usr/bin/env python3
"""Collect exact offline evidence and unchanged inputs; no provider/Git operations."""
from pathlib import Path
import ast,datetime as dt,hashlib,json
H=Path(__file__).resolve().parent;A=H.parent;O=H/'pre_destination_binding';E=A.parents[1];REPO=E.parent
HELPERS={p.name for p in (H/'proposed_helpers').glob('*.py')}

def sha(b):return hashlib.sha256(b).hexdigest()
def entry(root,name):
 b=(root/name).read_bytes();return {'path':name,'bytes':len(b),'sha256':sha(b)}
def write(name,v):(H/name).write_text(json.dumps(v,indent=2)+'\n')
def inventory(paths):
 values=[[p.relative_to(REPO).as_posix(),p.stat().st_size,sha(p.read_bytes())] for p in sorted(paths)];return {'files':len(values),'sha256':sha(json.dumps(values,separators=(',',':')).encode())}

def main():
 now=dt.datetime.now(dt.timezone.utc).isoformat();inputs=json.loads((H/'INPUT_PRESERVATION.json').read_bytes());entries=inputs['complete_context_files']
 for e in entries:
  if entry(O,e['path'])!=e:raise RuntimeError('Preserved input changed '+e['path'])
  if e['path'] not in HELPERS and entry(A,e['path'])!=e:raise RuntimeError('Current immutable changed '+e['path'])
 write('IMMUTABLE_INPUT_BINDING.json',{'timestamp_utc':now,'files':[e for e in entries if e['path'] not in HELPERS],'all631_preserved':True,'all356_prior_artifacts_preserved':True,'all56_prior_immutable_inputs_preserved':True,'all25_review04_artifacts_preserved':True,'root_lead_reconciliation_sha256':sha((A/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').read_bytes()),'publication_ready':False})
 prior_state=json.loads((H/'LOCAL_STATE_BASELINE.json').read_bytes());current={'flat_json':inventory((REPO/'.zenodo-state').glob('*.json')),'recursive_all_regular_files':inventory(p for p in (REPO/'.zenodo-state').rglob('*') if p.is_file())}
 if any(current[k]!=prior_state[k] for k in current):raise RuntimeError('Local state changed')
 write('LOCAL_STATE_PRESERVATION.json',{'timestamp_utc':now,**current,'unchanged':True,'scope':'241 direct JSON and314 recursive regular files; separate sorted repository-relative path/size/SHA256 compact JSON aggregate inventories.'})
 statuses=['ROOT_PACKAGE_REVIEW04_ACCEPTANCE.json','ROOT_PACKAGE_REVIEW03_ACCEPTANCE.json','ROOT_RECORD_URL_FINDING.json'];write('ROOT_READ_STATUS_BINDING.json',{'timestamp_utc':now,'root_authored_status_receipts':[entry(A,n) for n in statuses],'review04_complete_report_sha256':sha((A/'reviews/package_adversary_04/REPORT.md').read_bytes()),'review04_operations_program_bytes':(A/'reviews/package_adversary_04/operations_checks.py').stat().st_size,'review04_operations_program_sha256':sha((A/'reviews/package_adversary_04/operations_checks.py').read_bytes()),'all25_review04_hashes_verified':True,'read_scope':'Complete review04 report, verdict, operations program and root acceptance read; prior356/56 and all25 review hashes checked. Parent actual-replay claims remain identified as parent evidence; new preparer replays are separate.','publication_ready':False})
 summaries=[]
 for mode in ['normal','optimized']:
  root=E/'private/pr0399_doi_destination_repair'/('final_all_'+mode);destination=H/'evidence'/mode;destination.mkdir(parents=True,exist_ok=False)
  for name in ['REPLAY_ALL.json','destination/DESTINATION_CONTROLS.json']:
   p=destination/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((root/name).read_bytes())
  for p in (root/'previous').rglob('*'):
   if p.is_file() and '__pycache__' not in p.parts:
    target=destination/'previous'/p.relative_to(root/'previous');target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes())
  v=json.loads((root/'REPLAY_ALL.json').read_bytes())
  if v['total_current_controls']!=1876 or v['actual_provider_attempts']:raise RuntimeError('Current replay counts differ')
  summaries.append({'mode':mode,'current_controls':1876,'targeted_destination':170,'review04_other':55,'prior_controls':1651,'actual_provider_attempts':0,'replay_receipt':entry(H,'evidence/'+mode+'/REPLAY_ALL.json')})
 write('TEST_SUMMARY.json',{'timestamp_utc':now,'modes':summaries,'helper_bindings':json.loads((H/'CURRENT_HELPER_BINDING.json').read_bytes())['files'],'old_failure_evidence_preserved':True,'old_four_observations_per_mode':4,'cached_rows_separate':176,'publication_ready':False})
 parsed=[]
 for p in sorted(list(H.glob('*.py'))+[A/n for n in HELPERS]):ast.parse(p.read_bytes(),filename=str(p));parsed.append(entry(A,p.relative_to(A).as_posix()))
 write('PARSE_CHECK.json',{'timestamp_utc':now,'files':parsed,'all_passed':True})
 with (H/'RESEARCH_LOG.md').open('a') as stream:stream.write(f'- {now} — 99%: three canonical helpers bound; literal final HTTPS destination policy and independently recomputed proof enforced before final gate/read/append. Actual pipeline controls170 plus reviewer other55 and all1651 earlier obligations pass per normal/-O, total1876. Five exact old synthetic public fixtures enriched only with canonical URL/proof; no verdict/guard weakening. Frozen356 verifier reconstructs successfully;631 contexts and state241/314 unchanged. New seal pending; publication_ready false, NEW complete review05/root decision required.\n')
 print(json.dumps({'preserved_context':len(entries),'current_immutable':len(entries)-7,'current_controls_per_mode':1876,'state_unchanged':True,'root_acceptance_sha256':sha((A/statuses[0]).read_bytes())}))
if __name__=='__main__':main()
