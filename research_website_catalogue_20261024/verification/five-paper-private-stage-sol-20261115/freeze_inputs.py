"""One fresh five-target input freeze, only after all five final editorials exist."""
from five_common import *
from datetime import datetime,timezone
import re
def freeze():
 need(not (OWN/'INPUT_FREEZE_SEAL.json').exists(),'one_new_input_freeze_only')
 layouts=load(OWN/'RECORD_LAYOUTS.json');need(list(layouts)==list(IDS),'five_explicit_layouts_in_native_row_order')
 records={};paths=set()
 for rid in IDS:
  paper=PROGRAMME/'papers'/rid;layout=layouts[rid];editorial=paper/'reviews/editorial'
  sealpath=contained(paper,layout['editorial_seal'])
  need(bind(sealpath)['sha256']==layout['editorial_seal_sha256'],'exact_final_editorial_seal:'+rid)
  rootname,rootsha=CLEARANCES[rid];authority=PROGRAMME/'verification'/rootname
  need(bind(authority)['sha256']==rootsha,'exact_root_science_authority:'+rid)
  config=contained(paper,layout['config']);promotion=contained(paper,layout['promotion'])
  ready=load(paper/'sources/SOURCE_READY.json')
  recordpath=Path(ready['native_record_body_path']) if rid in {'23430498','23149775'} else paper/'sources/record.raw.json'
  record=load(contained(paper,recordpath))
  source_objects={p.name:load(p) for p in sorted((paper/'sources').glob('*.json'))}
  if recordpath.name not in source_objects:source_objects[recordpath.name]=record
  reviews={lane:load(contained(paper,'reviews/'+lane+'/VERDICT.json')) for lane in ['scope','analytic','adversarial']}
  paths.update(p for p in (paper/'sources').rglob('*') if p.is_file())
  paths.update(p for p in editorial.rglob('*') if p.is_file())
  if layout['kind']=='html':paths.update(p for p in config.parent.rglob('*') if p.is_file())
  else:paths.update([config,promotion])
  paths.add(authority)
  for lane in ['scope','analytic','adversarial']:
   folder=paper/'reviews'/lane
   # Final seal/manifests/reports/verdicts are bound without executing a review.
   for name in ['VERDICT.json','REPORT.md','SEAL.json','FINAL_SEAL.json','OWNED_MANIFEST.json','FINAL_MANIFEST.json']:
    if (folder/name).is_file():paths.add(folder/name)
  records[rid]={'layout':layout,'source_ready_original':ready,'native_record_original':record,
   'whole_native_root_JSON_objects':source_objects,'editorial_seal_original':load(sealpath),
   'whole_config_original':load(config),'whole_promotion_original':load(promotion),
   'whole_root_scientific_authority':load(authority),'whole_three_custom_verdicts':reviews}
 # Immutable earlier-stage code/proposal are references, never campaigns.
 reference=PROGRAMME/'verification/six-paper-private-stage-sol-20261114'
 for name in ['FINAL_SEAL.json','REPORT.md','six_common.py','simple_dom.py','six_presentation.py','build_private.py','six_body_contract.py','six_source.py','verify_stage_read_only.py']:
  paths.add(reference/name)
 proposal=PROGRAMME/'verification/dlab-notebook-link-resolution-sol-20261114'
 for p in proposal.iterdir():
  if p.is_file() and p.suffix in {'.json','.md','.py'}:paths.add(p)
 paths.update([Path('/Users/alec/Documents/Math/AGENTS.md'),Path('/Users/alec/.codex/attachments/90621d13-992e-4dc9-b897-1e6237f7c667/goal-objective.md')])
 for p in paths:need(p.is_file() and not p.is_symlink(),'regular_frozen_input')
 now=datetime.now(timezone.utc).isoformat()
 frozen={'UTC':now,'records':records,'input_files':[{'path':str(p),**bind(p)} for p in sorted(paths)],
  'root_editorial_copy_config_helper_stage_adoption_pending':True,'independent_code_audit_pending':True,
  'historical_false_null_flags_not_rewritten':True,'scientific_programs_or_old_campaigns_replayed':False}
 (OWN/'FROZEN_INPUT_SET.json').write_text(json.dumps(frozen,indent=2,ensure_ascii=False)+'\n')
 s={'UTC':now,'frozen_inputs_sha256':bind(OWN/'FROZEN_INPUT_SET.json')['sha256'],
  'baseline_sha256':bind(OWN/'FRESH_BASELINE.json')['sha256'],'policy_sha256':bind(OWN/'PRIVATE_STAGE_POLICY.json')['sha256'],
  'record_layouts_sha256':bind(OWN/'RECORD_LAYOUTS.json')['sha256'],'all_five_editorials_final_before_integration':True,
  'production_install_authorized':False,'AA':None,'canonical_url':None}
 (OWN/'INPUT_FREEZE_SEAL.json').write_text(json.dumps(s,indent=2)+'\n')
 return {'records':list(IDS),'input_files':len(paths),'root_editorial_adoption_pending':True,'publication_authority':False}
if __name__=='__main__':print(json.dumps(freeze(),indent=2))
