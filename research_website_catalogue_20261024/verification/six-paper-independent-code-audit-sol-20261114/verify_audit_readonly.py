"""Verify sealed independent audit evidence; never replay builders or faults.
Optional --current-base is appropriate only before production integration.
"""
from pathlib import Path
import json,hashlib,argparse
E=Path(__file__).resolve().parent;P=E.parents[1];W=P/'verification/six-paper-private-stage-sol-20261114'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,s):
 if not ok:raise ValueError(s)
def bind(p,n,h):need(p.stat().st_size==n and sha(p)==h,'binding '+str(p))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--current-base',action='store_true');args=ap.parse_args()
 need(sha(E/'PREFLIGHT_SEAL.json')=='bff849bcdb35b18313bee4dd26d75514dc8b00d0687df11308ad334d0ee12688','frozen independent preflight')
 need(sha(E/'PREFLIGHT_MANIFEST.json')==load(E/'PREFLIGHT_SEAL.json')['manifest_sha256'],'preflight envelope')
 for x in load(E/'PREFLIGHT_MANIFEST.json')['files']:bind(Path(x['path']),x['bytes'],x['sha256'])
 pins={'CANDIDATE_READY.json':'4fc89dc274a53c7bad55d4571f1b2e174f43d13218a662ee3c4302cd67de0e73','FINAL_SEAL.json':'8796f52a8dfa86cabf08507aff8120d39149b5e8ca8a2c2d01015dc68723fc93','OWNED_MANIFEST.json':'239bf60a4b7590c33389b75b64dba30d22f9080f3edefd5994958c05cec03912','CANDIDATE_CODE_MANIFEST.json':'97ce5b02ee63493e6dedfaee97e727d20b795b9de32b9de8b2745b937a6e66af'}
 for n,h in pins.items():need(sha(W/n)==h,'frozen candidate pin '+n)
 for x in load(W/'OWNED_MANIFEST.json')['files']:bind(W/x['path'],x['bytes'],x['sha256'])
 for x in load(W/'FROZEN_INPUT_SET.json')['files']:bind(Path(x['path']),x['bytes'],x['sha256'])
 for x in load(E/'ALL_PREFLIGHT_BINDINGS.json')['files']:bind(Path(x['path']),x['bytes'],x['sha256'])
 a=load(E/'INDEPENDENT_CANDIDATE_AUDIT.json');f=load(E/'FROZEN_FUNCTION_PROBES.json')
 need(a['all_preflight_blocks_accounted_for']==211 and len(a['independent_private_faults'])==60 and a['paired_complete_overlay_files']==26,'independent semantic evidence')
 need(f['whole_output_files_reproduced_in_memory']==26 and len(f['pure_negative_adapter_probes'])==30 and len(f['outside_private_namespace_output_paths_rejected'])==2,'independent final-code probes')
 need(f['all_original_frozen_input_bindings_unchanged']==1084 and f['candidate_owned_payloads_unchanged']==181,'post-probe custody')
 need((E/'INDEPENDENT_CANDIDATE_AUDIT.stderr').read_bytes()==b'' and (E/'FROZEN_FUNCTION_PROBES.stderr').read_bytes()==b'','empty actual errors')
 v=load(E/'FINAL_AUDIT_VERDICT.json');need(v['assessment']=='QUALIFIED_PASS_FROZEN_SIX_TARGET_CODE_AND_COMPLETE_SEMANTIC_CONTENT_WITH_EXPLICIT_PRESENTATION_MAPPINGS','literal independent audit verdict')
 need(v['blocking_defects']==[] and v['root_stage_adoption'] is False and v['production_install_authorized'] is False and v['AA'] is None,'withheld root/production/native gates')
 if (E/'FINAL_AUDIT_SEAL.json').exists():
  need(sha(E/'FINAL_AUDIT_MANIFEST.json')==load(E/'FINAL_AUDIT_SEAL.json')['manifest_sha256'],'final audit manifest/seal')
  for x in load(E/'FINAL_AUDIT_MANIFEST.json')['files']:bind(Path(x['path']),x['bytes'],x['sha256'])
 if args.current_base:
  public=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public');base=load(W/'FRESH_BASELINE.json');need({str(p.relative_to(public)) for p in public.rglob('*') if p.is_file()}=={x['path'] for x in base['public_files']},'current old public inventory')
  for x in base['public_files']:bind(public/x['path'],x['bytes'],x['sha256'])
  for x in base['installed_core_files']:bind(Path(x['path']),x['bytes'],x['sha256'])
 print(json.dumps({'status':'PASS_READONLY_INDEPENDENT_AUDIT_CUSTODY','candidate_payloads':181,'original_input_bindings':1084,'frozen_preflight_preserved':True,'independent_body_blocks_accounted_for':211,'independent_page_faults':60,'independent_native_authority_faults':30,'output_boundary_faults':2,'current_base_checked':args.current_base,'builder_source_campaign_or_fault_replays':0,'writes':0,'production_or_AA_clearance':False},indent=2))
if __name__=='__main__':main()
