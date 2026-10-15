from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,zipfile
HERE=Path(__file__).resolve().parent;PRE=HERE.parent
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(HERE).as_posix() if p.is_relative_to(HERE) else str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
now=datetime.now(timezone.utc).isoformat()
freeze=json.loads((PRE/'FROZEN_CANDIDATE.json').read_text())
files=[]
for item in freeze['files']:
 p=PRE/item['path'];q=pin(p)
 assert q['bytes']==item['bytes'] and q['sha256']==item['sha256']
 files.append({'candidate_relative_path':item['path'],**q,'frozen_pin_match':True})
assert not freeze['upload_cleared']
assert json.loads((PRE/'deposit.json').read_text())['metadata']==json.loads((PRE/'metadata.json').read_text())
with zipfile.ZipFile(PRE/'output/critical_wave_verification.zip') as z:assert len(z.namelist())==113 and z.testzip() is None
proof=pin(HERE/'independent_reconstruction.md')
assert proof['bytes']==6707 and proof['sha256']=='bd83ebf28b688529da77beb4aaea64fbd367a05f9ecffe96271116bd8c3117dc'
replay=json.loads((HERE/'INDEPENDENT_REPLAY_AUDIT.json').read_text())
assert replay['status']=='PASS' and replay['independently_derived_exact_total']==5603 and replay['independently_derived_noncertified_diagnostics']==5
assert len(replay['checksets'])==7
for result in replay['checksets']:
 q=pin(Path(result['actual_receipt']['path']))
 assert q['bytes']==result['actual_receipt']['bytes'] and q['sha256']==result['actual_receipt']['sha256']
stress=json.loads((HERE/'INDEPENDENT_STRESS_RECEIPT.json').read_text());assert stress['status']=='PASS' and stress['assertions']==2274
evidence=json.loads((HERE/'EVIDENCE_PIN_READBACK.json').read_text())
assert evidence['archived_authored_manifest_bindings_checked']==105 and len(evidence['pdf_pages'])==6
write('FINAL_INPUT_READBACK.json',{'utc':now,'candidate_freeze_manifest':pin(PRE/'FROZEN_CANDIDATE.json'),'files':files,'all_frozen_pins_match':True,'upload_cleared_unchanged_false':True,'independent_first_proof_unchanged':proof,'native_head':'e9c5d10978764db2cf25fa7d49cf4bd14a82d604','metadata_deposit_exact_equal':True,'archive_crc_pass':True,'archive_regular_entries':113})
write('VERDICT.json',{'utc':now,'status':'PASS','scope':'Exact unchanged ordinary-cone implication at beta2=0; actual nonlinear source model, quantitative theorem/corollary, bounded priority framing, exact package and six-page PDF','mandatory_issues':[],'optional_refinements':[{'location':'critical_wave_growth.tex attribution paragraph','suggestion':'Change All analytic estimates to The wave estimates for sharper attribution.'},{'location':'portable archive README provenance paragraph','suggestion':'Explain historical_snapshot_01 shares four unchanged files in parent family.'}],'completion_percent_of_assigned_audit':100,'prior_source_covering_construction_authenticated':False,'worldwide_firstness_certified':False,'external_human_peer_review_claimed':False,'publication_clearance':False,'parent_owns_publication_and_edits':True,'frozen_candidate_unchanged':True,'checksets_replayed':7,'exact_assertions':5603,'noncertified_diagnostics':5,'own_extra_exact_controls':2274,'pdf_pages_individually_viewed':6})
log=HERE/'RESEARCH_LOG.md'
log.write_text(log.read_text()+f'\n{now} — All final gates complete: candidate five-file readback unchanged; CRC/count/native/source/metadata/package comparisons pass; seven complete replays and portable runner pass; 2274 own exact controls; all six pages inspected; primary scope/priority limitations recorded. Mandatory issues none; scoped PASS. Final public authored manifest excludes whole reading/input copies and self-hash. Completion estimate: 100% of assigned review, not parent goal/publication clearance.\n')
whitelist=['independent_reconstruction.md','RESEARCH_LOG.md','INDEPENDENCE_CHECKPOINT.json','INITIAL_INPUT_PINS.json','audit_package.py','audit_evidence.py','independent_stress_checks.py','finalize_review.py','PACKAGE_PIN_AUDIT.json','INDEPENDENT_REPLAY_AUDIT.json','INDEPENDENT_STRESS_RECEIPT.json','EVIDENCE_PIN_READBACK.json','SOURCE_PRIORITY_LEDGER.md','PDF_QA.md','REPORT.md','VERDICT.json','FINAL_INPUT_READBACK.json','portable_runner/VERIFICATION_RUN.json','portable_runner/stdout.txt','portable_runner/stderr.txt']
for work in (HERE/'independent_replays').iterdir():
 for p in work.iterdir():
  if p.name in ['stdout.txt','stderr.txt','ACTUAL_RECEIPT.json','INDEPENDENT_CONTROLS.json','CHECKS.json','INDEPENDENT_CHECK_RECEIPT.json']:
   whitelist.append(p.relative_to(HERE).as_posix())
authored=[pin(HERE/path) for path in sorted(whitelist)]
assert len(authored)==len({p['path'] for p in authored})
write('FINAL_AUDIT_MANIFEST.json',{'schema':'pr248-fresh-review02-authored-manifest-v1','utc':now,'review_completion_percent':100,'verdict':'PASS for exact frozen candidate; no mandatory issues','public_authored_relative_paths':authored,'self_hash_omitted_to_avoid_recursion':True,'excluded_directories':['extracted_archive/','external_reading/','private_tmp/'],'excluded_input_copies':['independent_replays/*/*.py','paper_page-*.png'],'exclusion_reason':'Whole third-party reading/provider records, candidate/archive inputs, copied input scripts and input-derived renders are not redistributed as authored review materials. Byte pins and own execution receipts remain public.','restrictions':{'candidate_changed':False,'git_index_or_refs_changed':False,'pr_tracker_publication_changed':False,'external_individual_communication':False,'other_shard_chat_communication':False,'third_reviewer_spawned':False},'initial_proof_sha256':proof['sha256'],'candidate_files':[{'path':x['candidate_relative_path'],'bytes':x['bytes'],'sha256':x['sha256']} for x in files]})
final=json.loads((HERE/'FINAL_AUDIT_MANIFEST.json').read_text())
for item in final['public_authored_relative_paths']:
 q=pin(HERE/item['path']);assert q==item
print(json.dumps({'status':'PASS','authored_files':len(authored),'completion_percent':100,'frozen_candidate_files_verified':len(files),'mandatory_issues':0,'report':str(HERE/'REPORT.md'),'manifest':str(HERE/'FINAL_AUDIT_MANIFEST.json')},indent=2))
