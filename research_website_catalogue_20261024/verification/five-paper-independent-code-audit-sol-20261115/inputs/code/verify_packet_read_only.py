"""Terminal pure packet closure. Never builds files, installs, or replays science."""
from five_common import *
from five_source import load_bundles
from build_private import files_in_memory
from verify_stage_read_only import verify
from targeted_controls import run_controls
import argparse,sys,copy
EXCLUDED={'OWNED_MANIFEST.json','FINAL_SEAL.json'}
def verify_packet(*,current_base=False):
 before={str(p.relative_to(OWN)):bind(p) for p in OWN.rglob('*') if p.is_file()}
 need(not any(p.is_symlink() for p in OWN.rglob('*')),'owned_packet_no_symlinks')
 seal=load(OWN/'FINAL_SEAL.json');manifest=load(OWN/'OWNED_MANIFEST.json')
 need(bind(OWN/'OWNED_MANIFEST.json')['sha256']==seal['owned_manifest_sha256'],'exact_owned_manifest_seal')
 rows=manifest['files'];expected={r['path'] for r in rows};need(len(expected)==len(rows),'owned_unique_paths')
 need(set(before)==expected|EXCLUDED,'complete_owned_packet_namespace')
 for r in rows:need(bind(contained(OWN,r['path']))=={k:r[k] for k in ['bytes','sha256']},'owned_complete_bytes:'+r['path'])
 for key,name in [('report_sha256','REPORT.md'),('verdict_sha256','VERDICT.json'),('candidate_ready_sha256','CANDIDATE_READY.json'),('code_manifest_sha256','CANDIDATE_CODE_MANIFEST.json')]:need(bind(OWN/name)['sha256']==seal[key],'sealed_terminal_binding:'+name)
 need(seal['production_install_authorized'] is False and seal['AA'] is None and seal['canonical_URL_assignment'] is None,'terminal_no_install_or_native_authority')
 code=load(OWN/'CANDIDATE_CODE_MANIFEST.json')
 for r in code['files']:need(bind(OWN/r['path'])=={k:r[k] for k in ['bytes','sha256']},'exact_final_stage_code:'+r['path'])
 bundles=load_bundles();outputs=files_in_memory(bundles,'2026-11-15',dlab_homepage=True)
 for rel,data in outputs.items():
  for pair in ['candidate-a','candidate-b']:need((OWN/pair/'public'/rel).read_bytes()==data,'pure_memory_reproduction_all22_complete_bytes:'+pair+':'+rel)
 checked=[verify(OWN/pair/'public','2026-11-15',current_base=current_base,bundles=bundles) for pair in ['candidate-a','candidate-b']]
 controls=run_controls();held=load(OWN/'runs/targeted-normal.stdout.json');held['optimization']=sys.flags.optimize;need(same(controls,held),'complete_saved_28_fault_rejections_not_just_count')
 need({str(p.relative_to(OWN)):bind(p) for p in OWN.rglob('*') if p.is_file()}==before,'terminal_read_only_owned_bytes')
 return {'literal_custom_status':'SEALED_PRIVATE_FIVE_FULL_BYTES_REPRODUCIBLE_WITH_QUALIFIED_GATES_PENDING','owned_payloads':len(rows),'frozen_input_files':len(load(OWN/'FROZEN_INPUT_SET.json')['input_files']),'candidate_pair_paths_each':len(outputs),'new_only_fault_controls_per_mode':controls['faults_rejected'],'optimization':sys.flags.optimize,'complete_verifications':checked,'owned_packet_changed':False,'production_installed_or_native_AA_assigned':False,'network_or_writes':False,'source_or_legacy_campaign_replay':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--current-base',action='store_true');a=p.parse_args();print(json.dumps(verify_packet(current_base=a.current_base),indent=2))
