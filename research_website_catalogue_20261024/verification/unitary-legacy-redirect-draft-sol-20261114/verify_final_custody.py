"""Final additive custody; no Git, HTTP, JS execution or writes.
The initial strict-all-refs failure remains recorded and is not suppressed.
"""
from pathlib import Path
import json,hashlib,argparse
from redirect_contract import validate
E=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,s):
 if not ok:raise ValueError(s)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--current-local-core',action='store_true');args=ap.parse_args()
 inner=load(E/'SEAL.json');need(sha(E/'MANIFEST.json')==inner['manifest_sha256'],'original inner envelope preserved')
 for x in load(E/'MANIFEST.json')['files']:
  p=Path(x['path']);need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'unchanged inner artifact')
 candidate=Path(inner['candidate_path']);need(candidate.stat().st_size==913 and sha(candidate)==inner['candidate_sha256']=='7f6e34f571845066b420635fc4e32f2888a5be8f7da223dc4026b23f0ef04551','same concrete one-file draft');validate(candidate.read_text())
 drift=load(E/'LOCAL_DRIFT_QUALIFICATION.json');confirmation=load(E/'ROOT_CONCURRENCY_CONFIRMATION.json');changed=drift['changed_from_opening_snapshot']
 need(len(changed)==1 and changed[0]['before']['path']=='/Users/alec/Documents/Math/.git/refs/remotes/origin/main','exact recorded tracking-ref drift only')
 need(changed[0]['after_text'].strip()==confirmation['root_reported_checkpoint']=='e6a469bdf73880bdd179dd6bc5d02d4468510af6','root-confirmed concurrent checkpoint')
 need(confirmation['root_reported_parent']=='20d7666370d32b168c4468b62fe1c6a0df42d9c2' and confirmation['this_lane_draft_only_unchanged'] is True,'root confirmation scope')
 failures=load(E/'CLOSURE_QUALIFICATION_EXECUTIONS.json');need(failures['runs'][0]['exit_code']==0 and failures['runs'][1]['exit_code']==1,'successful pure custody and preserved fail-closed strict-ref guard')
 need(len(drift['unchanged_protected_local_files'])==8,'exact local core preserved set')
 if args.current_local_core:
  for x in drift['unchanged_protected_local_files']:
   p=Path(x['path']);need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'current localHEAD/index/main/article/core preservation')
 for x in load(E/'SOURCE_AND_IDENTITY_BINDINGS.json')['original_evidence_files']:
  p=Path(x['path']);need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'original source/authority evidence')
 tests=load(E/'URL_CONTROLS.json');need(len(tests['positive_cases'])==8 and len(tests['changed_script_controls_rejected'])==3 and len(load(E/'STATIC_CONTROLS.json')['rejected'])==3,'bounded exact-candidate controls')
 if (E/'FINAL_SEAL.json').exists():
  need(sha(E/'FINAL_MANIFEST.json')==load(E/'FINAL_SEAL.json')['manifest_sha256'],'final additive envelope')
  for x in load(E/'FINAL_MANIFEST.json')['files']:
   p=Path(x['path']);need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'sealed final additive artifact')
 print(json.dumps({'status':'PASS_DRAFT_ONLY_ADDITIVE_CUSTODY_WITH_ROOT_CONFIRMED_TRACKING_REF_UPDATE','candidate_bytes':913,'allowed_change_paths':1,'native_URL_cases':8,'URL_script_faults':3,'static_faults':3,'original_strict_ref_failure_retained':True,'root_checkpoint_origin_main_update_explicitly_recorded':True,'unchanged_local_core_files':8,'current_local_core_checked':args.current_local_core,'draft_applied':False,'this_lane_Git_or_site_mutations':0,'network_JS_or_campaign_replays':0},indent=2))
if __name__=='__main__':main()
