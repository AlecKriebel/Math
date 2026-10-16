from pathlib import Path
import json,hashlib,datetime,ast
OWN=Path(__file__).resolve().parent;BASE=OWN.parent;OLD=BASE/'fresh_review_01';sha=lambda b:hashlib.sha256(b).hexdigest();utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
report=OWN/'REPORT.md';assert report.stat().st_size>6000 and report.read_text().rstrip().endswith('Publication and new complete full-review acceptance remain parent-owned.')
oldmf=OLD/'FINAL_AUDIT_MANIFEST.json';assert sha(oldmf.read_bytes())=='91158468546d72bcf01a292f2e092b80d09d82e1e730e9205e765f46f4a0ad14'
oldpins=json.loads(oldmf.read_text())
for pin in oldpins['public_authored_relative_paths']:
 b=(OLD/pin['path']).read_bytes();assert len(b)==pin['bytes'] and sha(b)==pin['sha256']
frozen=json.loads((BASE/'FROZEN_CANDIDATE.json').read_text());checkpoint=json.loads((OWN/'INPUT_AND_DELTA_CHECKPOINT.json').read_text());pins=[]
for pin in frozen['files']:
 b=(BASE/pin['path']).read_bytes();assert len(b)==pin['bytes'] and sha(b)==pin['sha256'];pins.append({**pin,'final_readback_matches':True})
assert [{k:q[k] for k in ('path','bytes','sha256')} for q in pins]==[{k:q[k] for k in ('path','bytes','sha256')} for q in checkpoint['current_frozen_files']]
script=BASE/'prepare_current_source_packet.py';b=script.read_bytes();planned=json.loads((OWN/'PLANNED_SCRIPT_REVIEW_AND_RESOLUTION.json').read_text());assert sha(b)==planned['current_sha256']=='0f76afa3fc623b57c25062ffcf181e484c203923d0afcf979d1304d52acdba8e'
tree=ast.parse(b.decode());oldbody=(OWN/'extracted/original_submission/COUNTEREXAMPLE.md').read_text();anchors=[]
for node in tree.body:
 if isinstance(node,ast.Assign) and any(isinstance(q,ast.Name) and q.id=='old' for q in node.targets):
  value=ast.literal_eval(node.value);assert oldbody.count(value)==1;anchors.append(value)
assert len(anchors)==4
(OWN/'FINAL_READBACK.json').write_text(json.dumps({'utc':utc,'current_frozen_inputs':pins,'old_full_review_manifest_sha256':sha(oldmf.read_bytes()),'all_51_old_full_review_public_records_unchanged':True,'planned_script_current_pin':{'path':str(script),'bytes':len(b),'sha256':sha(b),'AST_syntax_valid_without_execution':True,'all_four_original_body_replacement_anchors_exist_once':True},'planned_script_issues_resolved':True,'script_not_executed':True,'old_review_not_reclassified_as_new_full_review':True,'new_full_review_03_not_certified_by_this_addendum':True},indent=2)+'\n')
(OWN/'VERDICT.json').write_text(json.dumps({'utc':utc,'assigned_addendum_completion_percent':100,'delta':'PASS_EXACT_FOUR_EDITORIAL_REFINEMENTS','revised_package':'PASS_113_FILES_112_PINS_19_NATIVE_ORIGINALS_7_COMPLETE_RECEIPTS_AND_PORTABLE_RUNNER','assertions':{'exact':5603,'noncertified_diagnostics':5},'rendering':'PASS_ALL_SIX_REVISED_PAGES','planned_source_packet_static_review':'PASS_AFTER_PARENT_CORRECTED_AUTHOR_PAIR_AT_ZERO_QUALIFIER_AND_THREE_REVIEW_GUARD','mandatory_issues_remaining':[],'initial_findings_preserved_in':'PLANNED_SCRIPT_REVIEW_AND_RESOLUTION.json','candidate_and_old_review_mutations_by_reviewer':False,'publication_clearance':False,'planned_script_executed':False,'external_contact':False,'this_is_delta_and_payload_addendum_not_an_additional_NEW_full_review':True},indent=2)+'\n')
log=OWN/'RESEARCH_LOG.md';s=log.read_text();s+='\n'+utc+' — 100% assigned addendum. Final current candidate pins and corrected planned-script bytes unchanged at readback. Original review manifest and 51 public artifacts all unchanged. Corrected planned script parses without execution and every replacement anchor occurs once in the native original proof. Final scoped PASS for exact editorial delta, revised payload/receipts/metadata/provenance/rendering and corrected planned presentation; mandatory issues none. Earlier source-attribution findings plus parent resolution retained. First report write hit a transient full-filesystem error; no existing evidence or other directory was cleaned by this reviewer, and only failed local writing resumed after space recovery. Final public authored manifest excludes extracted immutable copies, renders and copied input scripts, while retaining their pins. No publication authorization, guarded-script execution or new full-review claim.\n';log.write_text(s)
public=[];excluded=[]
for p in sorted(OWN.rglob('*')):
 if not p.is_file() or p.name=='FINAL_AUDIT_MANIFEST.json':continue
 rel=p.relative_to(OWN);parts=rel.parts
 inp=parts[0] in ('extracted','rendered','runner_temp') or (parts[0]=='replays' and p.suffix=='.py') or p.name.startswith('planned_script_')
 if inp:excluded.append(str(rel));continue
 data=p.read_bytes();public.append({'path':str(rel),'bytes':len(data),'sha256':sha(data)})
m={'schema':'pr248-editorial-delta-review-01-v1','utc':utc,'completion_percent':100,'current_frozen_inputs':pins,'original_full_review_manifest':{'path':str(oldmf),'sha256':sha(oldmf.read_bytes()),'all_51_public_records_unchanged':True},'corrected_planned_source_packet_script':{'path':str(script),'bytes':len(b),'sha256':sha(b),'not_executed':True},'final_verdict':'PASS_DELTA_REVISED_PAYLOAD_AND_CORRECTED_PLANNED_SCRIPT_STATIC_REVIEW','mandatory_issues_remaining':[],'original_findings_and_resolutions':'PLANNED_SCRIPT_REVIEW_AND_RESOLUTION.json','this_addendum_is_not_a_new_independent_full_manuscript_review':True,'public_authored_relative_paths':public,'excluded_immutable_input_and_render_copy_paths':excluded,'external_whole_reading_copies_not_added':True,'self_hash_note':'Manifest excludes itself; parent handoff records its external SHA256.','no_candidate_old_review_git_PR_publication_tracker_or_other_directory_mutation':True}
(OWN/'FINAL_AUDIT_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
for pin in public:
 data=(OWN/pin['path']).read_bytes();assert len(data)==pin['bytes'] and sha(data)==pin['sha256']
print(json.dumps({'utc':utc,'completion_percent':100,'public_files':len(public),'report_bytes':report.stat().st_size,'report_sha256':sha(report.read_bytes()),'manifest_sha256':sha((OWN/'FINAL_AUDIT_MANIFEST.json').read_bytes()),'remaining_mandatory_issues':[]},indent=2))
