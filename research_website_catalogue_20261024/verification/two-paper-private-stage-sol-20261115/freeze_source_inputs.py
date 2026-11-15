"""Freeze only final two editorial/native input packets; no public baseline yet."""
from two_common import *
from datetime import datetime,timezone
LAYOUTS={'23385145':{'seal':'reviews/editorial/SEAL.json','seal_sha256':'4e90ed60d057b57c30eb9f86d0116828174baf9caae6cdf34aaa93e2201bb9a4','bib':'reviews/editorial/citation.bib','source_html':'reviews/editorial/candidate/index.html'},'22983513':{'seal':'reviews/editorial/SEAL.json','seal_sha256':'129b27d351a22734ab11b58025089f54ac6f4ea67dbc91e1cf73b41feb55e31d','bib':'reviews/editorial/CITATION.bib','metadata':'reviews/editorial/SCHOLARLY_METADATA.json'}}
def freeze():
 need(not (OWN/'SOURCE_INPUT_SEAL.json').exists(),'one_source_freeze_only');paths=set();records={}
 for rid in IDS:
  paper=PROGRAMME/'papers'/rid;layout=LAYOUTS[rid];ready=load(paper/'sources/SOURCE_READY.json');science=root_authority(rid,SCIENCE);editorial=root_authority(rid,EDITORIAL)
  need(bind(paper/layout['seal'])['sha256']==layout['seal_sha256'],'exact_frozen_final_editorial_seal:'+rid)
  objects={a['role']:{'binding_original':a,'whole_original_object':load(contained(paper,a['path']))} for a in ready['whole_native_API_objects']}
  transport_path=contained(paper,ready['actual_transport_receipt_path']);transport=load(transport_path)
  records[rid]={'layout':layout,'whole_SOURCE_READY_original':ready,'whole_native_API_objects_original':objects,'whole_native_transport_aggregate_original':transport,'whole_publication_original':load(paper/'publication.json'),'whole_promotion_original':load(paper/'promotion.json'),'whole_public_sections_original':load(paper/'reviews/editorial/public-sections.json'),'whole_requirements_original':load(paper/'reviews/editorial/PUBLICATION_REQUIREMENTS.json'),'whole_editorial_seal_original':load(paper/layout['seal']),'whole_scientific_root_authority_original':science,'whole_editorial_root_authority_original':editorial}
  paths.update(p for folder in [paper/'sources',paper/'reviews/editorial'] for p in folder.rglob('*') if p.is_file());paths.update([paper/'publication.json',paper/'promotion.json'])
  for table in [SCIENCE,EDITORIAL]:paths.add(PROGRAMME/'verification'/table[rid][0])
  # Bound actual peer verdict/seal/report originals by the already literal
  # scientific authorities and editorial protected-input snapshots, without
  # importing or executing their proofs/programs.
  protected=load(paper/'reviews/editorial/PROTECTED_INPUTS.json')
  def visit(x):
   if isinstance(x,dict):
    if isinstance(x.get('path'),str):
     q=Path(x['path']);q=q if q.is_absolute() else PROGRAMME/q
     if q.is_file() and q.resolve().is_relative_to(paper.resolve()):paths.add(q)
    for y in x.values():visit(y)
   elif isinstance(x,list):
    for y in x:visit(y)
  visit(protected)
 paths.add(Path('/Users/alec/Documents/Math/AGENTS.md'))
 reference=PROGRAMME/'verification/five-paper-private-stage-sol-20261115'
 for name in ['FINAL_SEAL.json','OWNED_MANIFEST.json','CANDIDATE_CODE_MANIFEST.json','five_common.py','five_markup.py','build_private.py','five_contract.py','verify_stage_read_only.py']:paths.add(reference/name)
 need(all(p.is_file() and not p.is_symlink() for p in paths),'only_regular_source_input_files')
 now=datetime.now(timezone.utc).isoformat();data={'UTC':now,'records':records,'input_files':[{'path':str(p),**bind(p)} for p in sorted(paths)],'public_baseline_frozen':False,'public_index_sitemap_built':False,'source_or_five_packet_mutation':False,'whole_literal_custom_verdicts_retained_in_root_and_editorial_objects':True}
 (OWN/'SOURCE_INPUTS.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
 seal={'UTC':now,'source_inputs_sha256':bind(OWN/'SOURCE_INPUTS.json')['sha256'],'policy_sha256':bind(OWN/'PRIVATE_POLICY.json')['sha256'],'input_files':len(paths),'public_baseline_frozen':False,'public_build_authorized':False,'AA':None,'canonical_assignment':None};(OWN/'SOURCE_INPUT_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n');print(json.dumps(seal,indent=2))
if __name__=='__main__':freeze()
