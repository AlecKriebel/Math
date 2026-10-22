"""Documentary-only post-publication finalization of the frozen PR207 native packet.
No Git, network, ref, service, existing-view, or submitted-archive write.
"""
from pathlib import Path
import json, hashlib, datetime, difflib, os
A=Path(__file__).resolve().parent.parent
S=A/'native_revision_preparation_01'
OUT=A/'finalized_current_01'
NATIVE='unsolved_math_prioritization/attempts/5100044/'
CASE='draft_pr_publication_program_20260930/audits/pr207_5100044/'
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def jp(p):return json.loads(p.read_text())
def enc(v):return (json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
def check(name,want):
 b=(A/name).read_bytes();need(pin(b)==want,'Actual input changed: '+name);return jp(A/name)
gate=check('ROOT_PUBLICATION_GATE_01.json',{'bytes':3069,'sha256':'d194be8ac16c31ba8a91a6e9efdd515c1e65bb84708ae03cc0a5dab1693ce588'})
pub=check('ROOT_ACTUAL_PUBLICATION_01.json',{'bytes':3517,'sha256':'b185725e145968fa2cbee89df27a6280378ef5d50da4319cd62ce236a346ce9b'})
tracker=check('ROOT_ACTUAL_TRACKER_01.json',{'bytes':2311,'sha256':'4be14f01cb6dad4dcdfa1cf7f7512a1dcd29bdf1de1ff4f8510d6402d4254f70'})
need(gate['accepted'] and gate['new_distinct_reviewers']==2 and not gate['required_repairs'] and pub['published'] and pub['all_four_files_verified'] and pub['exact_intended_metadata_verified'] and tracker['native_readback_verified'] and tracker['appended_once'],'Actual completed event gates')
need(pub['doi']==tracker['doi']=='10.5281/zenodo.23428090','Actual own DOI')
need(not OUT.exists() and not OUT.is_symlink(),'Fresh finalization folder')
need(pin((S/'SEAL.json').read_bytes())=={'bytes':485,'sha256':'1aa225aa46e21f1a7b5aa391f1a18729ae37b2659bdb416f42b702c8d8a10b95'},'Frozen proposal seal')
m=jp(S/'NATIVE_ADOPTION_MAP.json');before={}
for row in m['operations']:
 b=(S/row['staged_path']).read_bytes();need(pin(b)==row['after'],'Frozen proposed current bytes')
 name=row['native_path'].removeprefix(NATIVE);need(NATIVE+name==row['native_path'],'Own native root')
 before[name]=b
need(len(before)==22 and sum(map(len,before.values()))==97450,'Original frozen native proposal')
after=dict(before);now=datetime.datetime.now(datetime.timezone.utc).isoformat();doi=pub['doi'];url=pub['doi_url']
rel='../../../'+CASE
review_sentence='Two new independent AI whole-package reviews were accepted by Root with no required repairs; this remains unrefereed and has no conventional human peer review or proof-assistant formalization.'
actual_sentence='Published verification note: ['+doi+']('+url+'). The exact four-file deposit and tracker '+tracker['range']+' were verified from actual service readbacks.'
def replace(name,old,new):
 text=after[name].decode();need(text.count(old)==1,'Exact documentary replacement occurrence: '+name+' / '+old[:65]);after[name]=text.replace(old,new).encode()
def jmodify(name,fn):
 o=json.loads(after[name]);fn(o);after[name]=enc(o)
# Only explicit publication/readiness sentences change; all mathematical assertions remain.
replace('PROOF.md','[telescoping preprint draft]','[published telescoping verification note source]')
replace('PROOF.md','Its final package seal remains pending.','Its frozen package is bound by PACKAGE_SEAL.json and the actual Root publication gate.')
replace('PROOF.md','Scoped mathematics has passed its dated audit; whole-package review and publication readiness remain pending.','Scoped mathematics and two new whole-package reviews have been accepted by Root. '+actual_sentence)
replace('PROOF.md','Whole-package adversarial review remains pending; this file alone does not authorize publication.',review_sentence+' Actual publication is recorded separately by the Root event receipt.')
replace('README.md','[telescoping preprint draft]','[published telescoping verification note source]')
replace('README.md','The latter is provisional and awaits its final package seal.',actual_sentence+' '+review_sentence)
replace('README.md','records the pending package review.','records the completed package reviews and verified publication.')
replace('PUBLICATION_STATUS.md','**Prospective correction prepared 16 October 2026. Publication ready: false. Whole-package adversarial review: pending.**','**Publication ready: true. Two new whole-package AI reviews accepted by Root; verified publication and tracker completion.**\n\nFinalized '+now+'. '+actual_sentence)
replace('PUBLICATION_STATUS.md','[telescoping manuscript draft]','[published telescoping manuscript source]')
replace('PUBLICATION_STATUS.md',"The draft's layout and final seal may still change.",'The reviewed PDF, TeX and ZIP are frozen by the published package seal; actual acceptance is in the Root publication gate.')
replace('PUBLICATION_STATUS.md','Our publication DOI is **pending and unassigned**. No DOI is invented or reserved by this proposal. Ferudun\'s cited DOI identifies his known-result preprint. No publication or tracker update has occurred in this staging task.',actual_sentence+' Ferudun\'s separate cited DOI identifies his known-result preprint. Repository integration and merge are documented by their own actual Root phase receipts.')
replace('SOURCES.md','Whole-package review remains pending.',review_sentence+' '+actual_sentence)
replace('WIP.md','an alternate telescoping preprint draft','the published alternate telescoping verification note')
replace('WIP.md',"Remaining work: settle the final manuscript seal, complete fresh whole-package adversarial review, obtain Root's read-through and adoption decision, and follow the authorized publication workflow. Our publication DOI is pending and unassigned. Publication ready: false.",actual_sentence+' '+review_sentence+' Publication ready: true. Repository integration and merge are documented by separate actual Root phase receipts.')
replace('WIP.md','Completion estimate: 100% of this bounded native/PR staging task after successful staged runs and consistency/pin checks; whole-package review and publication remain pending. No estimate of mathematical discovery priority.','Completion estimate: 100% of the bounded publication and current-presentation finalization task; repository integration and overall-case completion require separate actual receipts. No estimate of mathematical discovery priority.')
replace('independent_review/FINAL_REVIEW.md','The new native proposal and manuscript have **not** completed whole-package review.',review_sentence+' '+actual_sentence)
# Earlier dated research-log entries remain historical, followed by the actual later event.
after['RESEARCH_LOG.md']+=('\n- '+now+': Documentary finalization from real completed service events. '+review_sentence+' '+actual_sentence+' Mathematical/source/attribution statements, program bodies and prior computed runs are unchanged. Publication/current-presentation finalization100%; native integration and overall-case completion are recorded separately.\n').encode()
def common(o):
 o.update(publication_doi=doi,publication_doi_status='published_verified',publication_ready=True,whole_package_review='two_new_reviews_clean_Root_accepted',finalized_utc=now,publication_record_url=pub['record_url'],Root_publication_gate={'repository_path':CASE+'ROOT_PUBLICATION_GATE_01.json',**pin((A/'ROOT_PUBLICATION_GATE_01.json').read_bytes())},Root_publication_receipt={'repository_path':CASE+'ROOT_ACTUAL_PUBLICATION_01.json',**pin((A/'ROOT_ACTUAL_PUBLICATION_01.json').read_bytes())},Root_tracker_receipt={'repository_path':CASE+'ROOT_ACTUAL_TRACKER_01.json',**pin((A/'ROOT_ACTUAL_TRACKER_01.json').read_bytes())},package_seal={'repository_path':CASE+'publication_package_v1/PACKAGE_SEAL.json',**pin((A/'publication_package_v1/PACKAGE_SEAL.json').read_bytes())})
def metadata(o):common(o);o['schema']='pr207-current-metadata-v1'
jmodify('metadata.json',metadata)
jmodify('source_manifest.json',lambda o:o.update(publication_doi=doi))
# Inventories regenerated in dependency order; the execution record and programs remain byteexact.
rp=json.loads(after['independent_review/reviewed_hashes.json'])
rp.update(schema='pr207-current-pins-v1',created_utc=now,role='Current content inventory after documentary-only actual-event finalization; review acceptance is in the Root publication gate.',whole_package_review='two_new_reviews_clean_Root_accepted')
rp['files']={n:pin(after[n]) for n in rp['files']}
after['independent_review/reviewed_hashes.json']=enc(rp)
man=json.loads(after['MANIFEST.json']);man.update(created_utc=now,role='Current file inventory after documentary-only actual-event finalization, not a proof certificate.')
man['files']={n:pin(after[n]) for n in man['files']};after['MANIFEST.json']=enc(man)
pm=json.loads(after['PUBLICATION_MANIFEST.json']);common(pm);pm['schema']='pr207-current-publication-manifest-v1';pm['manifest']={'path':'MANIFEST.json',**pin(after['MANIFEST.json'])}
seal=jp(A/'publication_package_v1/PACKAGE_SEAL.json')
pm['manuscript'].update(role='Frozen published verification-note source; exact scientific assets and actual acceptance separately bound.',**seal['TeX'])
pm['PDF']={'repository_path':CASE+'publication_package_v1/focal_inversion_area.pdf',**seal['PDF']}
pm['verification_ZIP']={'repository_path':CASE+'publication_package_v1/verification_package.zip',**seal['ZIP']}
after['PUBLICATION_MANIFEST.json']=enc(pm)
# Check unchanged programs/run artifacts and all current dependency maps.
for name in ['verify.py','independent_review/independent_check.py','requirements.txt','verification.json','independent_review/independent_output.json','current_execution_receipt.json','source_record.json','prior_imported_report.json','independent_review/SOURCE_NOTES.md','independent_review/author_rerun_verification.json']:
 need(after[name]==before[name],'Forbidden non-documentary change: '+name)
for name in ['metadata.json','PUBLICATION_MANIFEST.json']:
 o=json.loads(after[name]);need(o['publication_ready'] is True and o['publication_doi']==doi and o['whole_package_review']=='two_new_reviews_clean_Root_accepted','Current factual aliases')
for name in ['MANIFEST.json','independent_review/reviewed_hashes.json']:
 for key,w in json.loads(after[name])['files'].items():need(pin(after[key])==w,'Dependent current pin')
body=(S/'PROPOSED_PR_BODY.md').read_text()
for old,new in [
 ('[telescoping preprint draft]','[published telescoping verification note source]'),
 ('remains provisional.','is frozen and published as ['+doi+']('+url+').'),
 ('**Whole-package review remains pending and publication ready is false.**',review_sentence+' **Publication ready: true.**'),
 ('Our publication DOI is **pending and unassigned**; the DOI above belongs to Ferudun. This body is prospective: no native file, branch, PR, QUEUE, publication, or tracker change was performed by this preparation.',actual_sentence+' The earlier DOI above belongs to Ferudun. Native adoption and PR merger are separately verified by actual Root receipts; this publication update alone makes no merger or overall-goal completion claim.')
]:
 need(body.count(old)==1,'Exact PR-body documentary replacement');body=body.replace(old,new)
OUT.mkdir(mode=0o700)
def write(path,b):
 path.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
 with path.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 path.chmod(0o444)
for n,b in sorted(after.items()):write(OUT/'payload'/NATIVE/n,b)
write(OUT/'FINAL_PR_BODY.md',body.encode())
meta=jp(S/'PROPOSED_PR_METADATA.json');meta.update(mode='actual_published_presentation_pending_native_adoption',retain_draft=False,publication_ready=True,publication_doi=doi,body_file='FINAL_PR_BODY.md')
write(OUT/'FINAL_PR_METADATA.json',enc(meta))
diff=''.join(''.join(difflib.unified_diff(before[n].decode().splitlines(True),after[n].decode().splitlines(True),fromfile='frozen/'+n,tofile='finalized/'+n)) for n in sorted(after) if after[n]!=before[n])
write(OUT/'DOCUMENTARY_FINALIZATION.diff',diff.encode())
rows=[{'native_path':NATIVE+n,'path':'payload/'+NATIVE+n,'before_frozen':pin(before[n]),'after':pin(after[n]),'changed':before[n]!=after[n]} for n in sorted(after)]
report={'schema':'pr207-documentary-current-finalization-v1','UTC':now,'PR':207,'state':'FINALIZED_OWNED_PACKET_ONLY_NOT_NATIVE_ADOPTION','frozen_scientific_package_unchanged':True,'frozen_native_proposal_unchanged':True,'all_code_and_computed_runs_unchanged':True,'mathematical_source_attribution_or_novelty_assertion_changed':False,'original_submitted_archive_unchanged':True,'actual_DOI':doi,'actual_tracker_range':tracker['range'],'payload_files':len(after),'payload_bytes':sum(map(len,after.values())),'changed_payload_files':sum(before[n]!=after[n] for n in after),'files':rows,'actual_inputs':{n:pin((A/n).read_bytes()) for n in ['ROOT_PUBLICATION_GATE_01.json','ROOT_ACTUAL_PUBLICATION_01.json','ROOT_ACTUAL_TRACKER_01.json']},'scope_contract':'Only actual DOI/record/tracker/review/ready/document-status fields and dependent pins, exactly per frozen whole-package review contract. No Git/API/local-current/QUEUE write performed.','case_integration_completion_not_asserted':True,'goal_complete':False}
write(OUT/'FINALIZATION_REPORT.json',enc(report))
files={p.relative_to(OUT).as_posix():pin(p.read_bytes()) for p in OUT.rglob('*') if p.is_file()}
manifest={'schema':'pr207-finalized-current-packet-manifest-v1','UTC':now,'files':files,'file_count':len(files),'total_bytes':sum(x['bytes'] for x in files.values()),'public_exact_allowlist':True}
write(OUT/'FINALIZATION_MANIFEST.json',enc(manifest))
write(OUT/'FINALIZATION_SEAL.json',enc({'schema':'pr207-finalized-current-packet-seal-v1','UTC':now,'manifest':pin((OUT/'FINALIZATION_MANIFEST.json').read_bytes()),'frozen_proposal_seal':pin((S/'SEAL.json').read_bytes()),'no_mathematical_source_attribution_or_novelty_changes':True,'actual_publication_verified':True,'actual_tracker_verified':True,'no_native_adoption_or_merge_performed':True,'goal_complete':False}))
print(json.dumps({'output':str(OUT),'payload_files':22,'payload_bytes':report['payload_bytes'],'changed_files':report['changed_payload_files'],'manifest':pin((OUT/'FINALIZATION_MANIFEST.json').read_bytes()),'seal':pin((OUT/'FINALIZATION_SEAL.json').read_bytes())}))
