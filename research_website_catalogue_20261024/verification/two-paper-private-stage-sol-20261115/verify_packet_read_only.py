"""Sealed two-candidate pure closure; never writes, installs or browses."""
from two_common import *
from two_source import load_bundles
from build_private import files_in_memory
from verify_stage_read_only import verify
from targeted_controls import run_controls
import sys,argparse
EXCLUDED={'OWNED_MANIFEST.json','FINAL_SEAL.json'}
def verify_packet(*,current_base=False):
 before={str(p.relative_to(OWN)):bind(p) for p in OWN.rglob('*') if p.is_file()};need(not any(p.is_symlink() for p in OWN.rglob('*')),'owned_packet_no_symlinks');seal=load(OWN/'FINAL_SEAL.json');manifest=load(OWN/'OWNED_MANIFEST.json');need(bind(OWN/'OWNED_MANIFEST.json')['sha256']==seal['owned_manifest_sha256'],'owned_manifest_seal');rows=manifest['files'];expected={r['path'] for r in rows};need(len(rows)==len(expected) and set(before)==expected|EXCLUDED,'complete_sealed_owned_namespace')
 for r in rows:need(bind(contained(OWN,r['path']))=={k:r[k] for k in ['bytes','sha256']},'complete_owned_bytes:'+r['path'])
 for key,name in [('report_sha256','REPORT.md'),('verdict_sha256','VERDICT.json'),('ready_sha256','CANDIDATE_READY.json'),('code_manifest_sha256','CODE_MANIFEST.json')]:need(bind(OWN/name)['sha256']==seal[key],'terminal_sealed_'+name)
 for r in load(OWN/'CODE_MANIFEST.json')['files']:need(bind(OWN/r['path'])=={k:r[k] for k in ['bytes','sha256']},'final_import_safe_helper_bytes:'+r['path'])
 need(seal['production_install_authorized'] is False and seal['AA'] is None and seal['canonical_assignment'] is None,'terminal_no_install_or_native_authority')
 bs=load_bundles();pure=files_in_memory(bs,'2026-11-15')
 for rel,data in pure.items():
  for pair in ['candidate-a','candidate-b']:need((OWN/pair/'public'/rel).read_bytes()==data,'pure_exact11_byte_reproduction:'+pair+':'+rel)
 positives=[verify(OWN/pair/'public','2026-11-15',current_base=current_base,bundles=bs) for pair in ['candidate-a','candidate-b']];controls=run_controls();held=load(OWN/'runs/controls-normal-recovered.stdout.json');held['optimization']=sys.flags.optimize;need(same(controls,held),'all24_full_saved_rejection_outcomes_not_just_count')
 need({str(p.relative_to(OWN)):bind(p) for p in OWN.rglob('*') if p.is_file()}==before,'terminal_owned_packet_read_only')
 return {'literal_custom_status':'SEALED_TWO_PRIVATE_FULL_COPY_ASSET_AND_BYTE_REPRODUCTION_VALIDATED_WITH_ROOT_STAGE_GATES_PENDING','owned_payloads':len(rows),'original_frozen_input_files':len(load(OWN/'SOURCE_INPUTS.json')['input_files']),'paired_overlay_files_each':len(pure),'optimization':sys.flags.optimize,'new_only_faults_rejected':controls['faults_rejected'],'full_positive_results':positives,'owned_bytes_changed':False,'network_browser_install_Sheet_Git_source_or_old_campaign_actions':False,'AA':None,'canonical_assignment':None}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--current-base',action='store_true');a=p.parse_args();print(json.dumps(verify_packet(current_base=a.current_base),indent=2))
