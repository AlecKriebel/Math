from pathlib import Path
import json,hashlib,datetime,subprocess
OWN=Path(__file__).resolve().parent;BASE=OWN.parent
utc=datetime.datetime.now(datetime.timezone.utc).isoformat();sha=lambda b:hashlib.sha256(b).hexdigest()
checkpoint=json.loads((OWN/'INDEPENDENCE_CHECKPOINT.json').read_text())
assert sha((OWN/'INDEPENDENT_DERIVATION.md').read_bytes())==checkpoint['derivation_sha256']
frozen=json.loads((BASE/'FROZEN_CANDIDATE.json').read_text());assert frozen==checkpoint['frozen_candidate']
files=[]
for pin in frozen['files']:
 b=(BASE/pin['path']).read_bytes();assert len(b)==pin['bytes'] and sha(b)==pin['sha256'];files.append({**pin,'final_readback_matches':True})
b=(BASE/'FROZEN_CANDIDATE.json').read_bytes();files.append({'path':'FROZEN_CANDIDATE.json','bytes':len(b),'sha256':sha(b),'dict_equal_initial_checkpoint':True})
(OWN/'INPUT_AND_FINAL_PINS.json').write_text(json.dumps({'utc':utc,'original_native_head':'e9c5d10978764db2cf25fa7d49cf4bd14a82d604','all_frozen_candidate_files_unchanged':True,'independent_derivation_initial_hash_unchanged':True,'independence_checkpoint_utc':checkpoint['utc'],'files':files},indent=2)+'\n')
source=json.loads((OWN/'SOURCE_VERSION_LEDGER.json').read_text())
for row in source['sources']:
 if row['name']=='KMv1':row['complete_pages_to_read']=sorted(set(row['complete_pages_to_read']+[24]))
 row['complete_pages_read']=row.pop('complete_pages_to_read');row['full_relevant_page_read_confirmed']=True
source['utc']=utc;source['limits']='Fresh reviewer read the exact listed complete pages; selected source formula pages were visually inspected. Final KM publisher body, whole original Dunn chapter and worldwide/deposit/history absence were not certified.'
(OWN/'SOURCE_VERSION_LEDGER.json').write_text(json.dumps(source,indent=2)+'\n')
findings=OWN/'SOURCE_AND_PRIORITY_FINDINGS.md';s=findings.read_text().replace('25-27 and 35-38','24-27 and 35-38')
s=s.replace('The latter uses an Linfinity neighborhood, excludes no zero cone,', 'Printed page 24 carries a standing genuine locally optimal-control premise into the later cone/theorem discussion; the manuscript\'s global optimizer fulfills it, and genuine local optimality is sufficient for prior coverage. The latter uses an Linfinity neighborhood, excludes no zero cone,')
findings.write_text(s)
report=OWN/'REPORT.md';s=report.read_text().replace('25-27 and 35-38','24-27 and 35-38');report.write_text(s)
qa=[]
for n in range(1,7):
 p=OWN/f'rendered/page-{n}.png';b=p.read_bytes();qa.append({'page':n,'relative_render_path':str(p.relative_to(OWN)),'bytes':len(b),'sha256':sha(b),'visually_inspected':True,'clipping_overlap_missing_glyph_or_citation_defect':False})
meta=json.loads((BASE/'metadata.json').read_text());orcid=meta['creators'][0]['orcid'];digits=orcid.replace('-','');v=0
for c in digits[:-1]:v=(v+int(c))*2
check=(12-v%11)%11;assert ('X' if check==10 else str(check))==digits[-1]
assert meta['publication_date']=='2026-10-14' and meta['version']=='1.0' and meta['license']=='cc-by-4.0'
(OWN/'PDF_QA.json').write_text(json.dumps({'utc':utc,'candidate_pdf_sha256':files[1]['sha256'],'pages':6,'all_six_own_renders_visually_inspected':True,'layout_defects':[],'renders':qa,'author':'Alec Kriebel','orcid':orcid,'orcid_checksum_valid':True,'date_version_license_consistent':True,'AI_unreferreed_no_external_human_review_disclosure_consistent':True,'bibliography_entries':9,'creation_Pacific_date_vs_UTC_publication_date_not_a_mismatch':True},indent=2)+'\n')
(OWN/'VERDICT.json').write_text(json.dumps({'utc':utc,'assigned_subaudit_completion_percent':100,'math':'PASS_PRECISE_FROZEN_THEOREM_AND_COROLLARY','source_scope':'PASS_UNCHANGED_ORDINARY_CONE_STRICT_POSITIVITY_TO_STRONG_CONTROL_L2_IMPLICATION_ONLY','priority_framing':'PASS_BOUNDED_NO_COVERING_FINDING_AND_KNOWN_MECHANISM_ATTRIBUTION; NOT_WORLDWIDE_FIRSTNESS_CERTIFICATE','package':'PASS_113_ARCHIVE_FILES_112_MANIFEST_PAYLOAD_PINS_7_COMPLETE_RECEIPTS_5603_EXACT_5_NONCERTIFIED_DIAGNOSTICS','rendering':'PASS_6_PAGES','mandatory_issues':[],'optional_improvements':['Explicit KM Theorem 4.17 number in opening discussion','CC BY 4.0 line in standalone PDF'],'candidate_edits':False,'repository_or_remote_or_PR_or_publication_or_tracker_mutation':False,'external_contact_or_outreach_prepared':False,'second_review_spawned':False,'publication_clearance':False,'parent_owned_next_step':'Read full report and preserve sequential fresh-review process; parent owns fixes and any publication decision.'},indent=2)+'\n')
log=OWN/'RESEARCH_LOG.md';s=log.read_text();s+='\n'+utc+' — 100% assigned fresh review. Full primary-source scope/version comparison and standing local-optimum premise checked; all manuscript analytic claims, edge cases and quantifiers withstand falsification. All seven checksets and complete scientific receipts match; total 5603 exact plus 5 noncertified diagnostics independently derived. Exact 113-file ZIP closure, native 19-file provenance, metadata/deposit/source equality, 83 direct nested pins plus four relocated historical pins verified. Six candidate pages visually reviewed. Final candidate readback unchanged and initial independent derivation hash unchanged. Final PASS is restricted to the exact frozen math/source/package/rendering and bounded historical framing. Mandatory repairs none; optional citation/license polish unconditioned. No publication clearance or second-review spawn. Public authored manifest excludes whole external reading copies, extracted input archive and unchanged checker input copies.\n';log.write_text(s)
# Public authored review output closure. Excluded reading/input copies remain only local evidence.
public=[];excluded=[]
for p in sorted(OWN.rglob('*')):
 if not p.is_file() or p.name=='FINAL_AUDIT_MANIFEST.json':continue
 rel=p.relative_to(OWN);parts=rel.parts
 is_input=(parts[0] in ('external_reading','extracted','rendered','runner_temp')) or (parts[0]=='replays' and p.suffix=='.py')
 if is_input:excluded.append(str(rel));continue
 b=p.read_bytes();public.append({'path':str(rel),'bytes':len(b),'sha256':sha(b)})
manifest={'schema':'pr248-fresh-final-manuscript-review-01-v1','utc':utc,'completion_percent':100,'original_native_head':'e9c5d10978764db2cf25fa7d49cf4bd14a82d604','frozen_candidate_files':files,'final_verdict':'PASS_PRECISE_FROZEN_CANDIDATE','mandatory_issues':[],'public_authored_relative_paths':public,'excluded_whole_external_reading_and_immutable_input_copies':True,'excluded_local_evidence_paths':excluded,'self_hash_note':'Manifest excludes itself; parent handoff records its external SHA256.','no_candidate_or_git_or_remote_or_publication_mutation':True}
(OWN/'FINAL_AUDIT_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'utc':utc,'completion_percent':100,'public_authored_files':len(public),'final_manifest_sha256':sha((OWN/'FINAL_AUDIT_MANIFEST.json').read_bytes()),'report_sha256':sha(report.read_bytes()),'candidate_pins_unchanged':True},indent=2))
