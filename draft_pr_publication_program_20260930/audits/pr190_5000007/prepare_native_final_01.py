"""Propagate actual gated publication facts; preserve reviewed scientific bytes."""
from pathlib import Path
import datetime,hashlib,json,shutil
A=Path(__file__).resolve().parent;I=A/'integration_preparation'
def require(x,msg):
 if not x:raise RuntimeError(msg)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p):return json.loads(p.read_text())
g=read(A/'ROOT_PUBLICATION_GATE.json');z=read(A/'ZENODO_PUBLICATION_READBACK.json');tr=read(A/'TRACKER_ACCEPTANCE.json')
require(g['status']=='READY_FOR_AUTHORIZED_PUBLICATION' and z['state']=='published','Publication not actually accepted')
require(tr['status']=='TRACKER_APPEND_AND_TWO_FRESH_READS_ACCEPTED' and tr['DOI']==z['doi'],'Tracker not actually accepted')
for n,x in g['payloads'].items():require(pin(A/g['package_name']/n)['sha256']==x['SHA256'],'Reviewed packet drift')
old=read(I/'CURRENT_TEMPLATE.json');require(old['current_template']=='native_template_pending_02','Wrong predecessor')
src=I/old['current_template'];T=I/'native_template_final_01';require(not T.exists(),'Final template already exists')
for n,x in old['files'].items():require(pin(src/n)==x,'Reviewed native bytes drift '+n)
shutil.copytree(src,T)
stamp=datetime.datetime.now(datetime.UTC).isoformat();changed=[]
def write(n,s):
 p=T/n
 if p.exists():p.chmod(0o644)
 p.write_text(s);p.chmod(0o444);changed.append(n)
def replace(n,a,b):
 s=(T/n).read_text();require(s.count(a)==1,'Nonunique factual text '+n);write(n,s.replace(a,b))
replace('README.md','It is prepared for the required successive NEW whole-package adversarial reviews. This native template makes no completed publication/merge/tracker claim.','The successive NEW whole-package review and global repair loop is complete; the final review found no required repairs. The exact reviewed note is published at '+z['doi_url']+' and tracker '+tr['range']+' was verified by two fresh reads. Original-head MAIN integration remains pending at this template preparation. PUBLICATION.json records these actual facts.')
replace('CANDIDATE_PROOF.md','Current core mathematics is independently audited; complete-package reviews and actual publication/disposition remain pending in this prepared native template.','Current core mathematics and the complete publication package have completed the successive fresh adversarial review loop. The exact reviewed note is actually published and tracked as stated in PUBLICATION.json; original-head MAIN disposition is pending at this template preparation.')
replace('independent_review/FINAL_REVIEW.md','Full publication-package reviews remain pending in this native preparation.','Completed whole-package reviews and the globally propagated DOI-file identity repair are bound in the Root publication gate. The last fresh reviewer found no required repairs. Actual Zenodo publication and tracker acceptance are recorded in ../PUBLICATION.json; original-head MAIN disposition is pending at this preparation.')
write('PUBLICATION_RECEIPT.md','# Actual publication and tracker acceptance\n\n'+stamp+' — Exact reviewed preprint '+z['doi_url']+' ('+z['record_url']+') is published. Tracker '+tr['range']+' was authenticated with two fresh row reads. Original PR190 head0c3346c8ebcb3b967a1d8bf9a283f027b44b738c is preserved; original-head MAIN integration remains pending at this preparation.\n\nThe earlier draft chronology remains: GitHub PR creation2026-10-01T04:03:35Z, initial artifact commit c9162a45d30120b10b42b1f79c50bab417ed287b, authenticated original V2 SHA256f96288e95c946731091989cea3eb087829c94cf966898dae792122567da3f16b. These records do not certify historical exact-byte public visibility, firstness, author awareness or independence. Current Ferudun DOI-version PDF/source identity was verified15October2026. Classical inputs and exact contemporaneous overlap are credited. Extensive AI; unrefereed; no conventional human peer review.\n\nThe immutable original draft-only receipt remains under historical_original/PUBLICATION_RECEIPT.md. Actual scientific, review, metadata and lifecycle receipts are in the case audit directory.\n')
pub={'UTC':stamp,'PR':190,'original_head':'0c3346c8ebcb3b967a1d8bf9a283f027b44b738c','state':'published','DOI':z['doi'],'doi_url':z['doi_url'],'record_url':z['record_url'],'tracker_range':tr['range'],'whole_package_reviews_complete':True,'last_review_no_required_repairs':True,'historical_priority_clearance':False,'DOI_file_identity_verified':True,'source_author_authenticated_erratum':False,'unique_author_intent_certified':False,'firstness_or_independence_certified':False,'original_PR_merge_pending_at_preparation':True,'current_paper_source_SHA256':g['payloads']['dodecahedron_endpoint.tex']['SHA256'],'publication_gate_SHA256':pin(A/'ROOT_PUBLICATION_GATE.json')['sha256']}
write('PUBLICATION.json',json.dumps(pub,indent=2)+'\n')
for n in ['source_interpretation.json','recovery_manifest.json']:
 j=read(T/n)
 if n=='source_interpretation.json':j['native_stage']='Reviewed note actually published and tracked; original-head MAIN integration pending'
 else:j['current_result']['native_stage']='Reviewed note actually published and tracked; original-head MAIN integration pending';j['UTC']=stamp
 j['current_publication']=pub;write(n,json.dumps(j,indent=2)+'\n')
j=read(T/'independent_review/reviewed_hashes.json');j.update(UTC=stamp,scope='Current explicitly qualified reviewed science; actual note published/tracked; original-head MAIN integration pending',whole_package_reviews_complete=True,publication_gate_SHA256=pub['publication_gate_SHA256']);write('independent_review/reviewed_hashes.json',json.dumps(j,indent=2)+'\n')
write('RESEARCH_LOG.md',(T/'RESEARCH_LOG.md').read_text()+'\n'+stamp+' — Workflow95%: successive fresh whole-package reviews complete, current DOI-file identity correction propagated, final review clean. Exact note '+z['doi_url']+' and tracker '+tr['range']+' actually accepted; original-head MAIN integration and factual completion pending. Original effort unknown/5(interrupted) retained.38completed/22published unchanged until factual acceptance.\n')
for n,x in old['files'].items():
 if n not in changed:require(pin(T/n)==x,'Unintended scientific/native change '+n)
original=read(A/'ORIGINAL_FILE_MANIFEST.json')
for x in original['files']:
 n=Path(x['path']).relative_to('unsolved_math_prioritization/attempts/5000007');require(pin(T/'historical_original'/n)=={'bytes':x['bytes'],'sha256':x['sha256']},'Original custody drift')
files={p.relative_to(T).as_posix():pin(p) for p in sorted(T.rglob('*')) if p.is_file()}
for n in files:(T/n).chmod(0o444)
cur={'UTC':stamp,'current_template':T.name,'status':'ACTUAL_PUBLISHED_TRACKED_NATIVE_TEMPLATE_MAIN_INTEGRATION_PENDING','original_head':pub['original_head'],'files':files,'package':g['package_name'],'publication_ready':True,'original_historical_files':22,'reviewed_scientific_bytes_unchanged':True,'only_factual_status_documents_changed':changed,'publication':pub,'MAIN_updated':False}
pointer=I/'CURRENT_TEMPLATE.json';pointer.chmod(0o644);pointer.write_text(json.dumps(cur,indent=2)+'\n');pointer.chmod(0o444)
archive=I/'NATIVE_TEMPLATE_FINAL_01_MANIFEST.json';require(not archive.exists(),'Manifest already exists');archive.write_bytes(pointer.read_bytes());archive.chmod(0o444)
case=read(A/'CURRENT_CASE_STATUS.json');case.update(UTC=stamp,status='NOTE_ACTUALLY_PUBLISHED_TRACKED_ORIGINAL_HEAD_MAIN_MERGE_PENDING',case_percent=95,publication_ready=True,whole_package_reviews_complete=True,whole_package_review01_complete=True,whole_package_review01_disposition='REPAIR_REQUIRED',required_review01_issue_globally_repaired=True,whole_package_review02_complete=True,whole_package_review02_disposition='PASS',Zenodo_published=True,DOI=z['doi'],tracker_updated=True,tracker_range=tr['range'],original_PR_merged=False,PR_closed=False,remaining_required_steps='Original-head two-parent MAIN merge, full selected current-tree acceptance and factual completion; only then original-status-only intake191.')
(A/'CURRENT_CASE_STATUS.json').write_text(json.dumps(case,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+stamp+' — Workflow95%: exact reviewed preprint '+z['doi_url']+' actually published, tracker '+tr['range']+' verified twice, native factual template prepared without scientific byte changes. Original-head MAIN integration/factual acceptance pending;38completed/22published unchanged. No historical firstness or independence certification.\n')
print(json.dumps({'status':cur['status'],'files':len(files),'only_factual_documents_changed':changed,'scientific_bytes_unchanged':True}))
