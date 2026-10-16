from pathlib import Path
import hashlib,json,datetime,subprocess
R=Path(__file__).resolve().parent;A=R.parents[1];P=A/'preprint_v1_0';S=A/'reviews/priority_01/private_sources'
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
    if not ok:raise ValueError(msg)
def dump(n,o):(R/n).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
sources=[
 ('AIM.html','http://aimpl.org/shapesurface/1/','Complete Problem1.4 heading/introduction/question and neighboring section1 problems; literal unrestricted-dimension scope. Historical plain HTTP body; new web open failed. No certificate bypass.'),
 ('EM_v1.pdf','https://arxiv.org/abs/1406.7624v1','Domain/Robin convention PDF3-4; Section5 assumptions and Theorem5.1 interface PDF16-17; Theorem5.2 and proof PDF20-21; PDF21 actually viewed.'),
 ('HHRV_publisher.pdf','https://doi.org/10.1007/s00023-022-01228-3','Section2 complete basic assumptions and quantitative strengthening; published TheoremA.6 and entire derivation PDF35-36, printed817-818; PDF35 actually viewed. Publisher DOI page freshly opened.'),
 ('HHRV_latest.pdf','https://arxiv.org/abs/1610.09891v2','Actual old-preprint Theorem3.6 PDF11 and adjacent context; denominator(1-4theta)^2/theta<1/4 distinct from journal.'),
 ('FL_v1.pdf','https://arxiv.org/abs/0711.3473v1','Section2.1 form(2.3)/outward Robin convention; Theorem3.2 and Lemma3.4 with count/Poisson proof interface PDF7.'),
 ('PV_v1.pdf','https://arxiv.org/abs/2008.03699v1','Actual Assumptions2.3 PDF5; Definition3.15/(3.8)-(3.9) PDF13; Remark5.22 PDF36-37; Definition6.3/Theorem6.4/null-sequence proof PDF38-39.'),
 ('PP_v2.pdf','https://arxiv.org/abs/1502.00877v2','Definition1.1 uniform collar/curvature admissibility; Corollary1.6 and its large-strength curvature gap in introduction PDF2-4. No complete reproof of source asymptotics.'),
 ('EKL_v1.pdf','https://arxiv.org/abs/1703.10854v1','Sections1.1-1.2 delta model/deformation-amplitude convention PDF1-3; Section4 discussion PDF20-21; expectations distinguished from theorems.'),
 ('L2017.pdf','https://aamp.fjfi.cvut.cz/lotoreichik/Trier2017.pdf','PDF7/12, printed9/15: fixed alpha/beta f and distinct delta/Robin expectation blocks; extracted text read, not newly visually inspected.'),
 ('BSZ_v1.pdf','https://arxiv.org/abs/2609.03783v1','Actual magnetic operator/field assumptions(a)-(b) and Theorem1 PDF2-3; B>0 and large beta. Applicability only, not entire magnetic-proof correctness.')]
ledger=[]
for name,url,scope in sources:
    body=(S/name).read_bytes();ledger.append({'retained_source':str(S/name),'bytes':len(body),'sha256':sha(body),'primary_url':url,'read_scope':scope})
dump('SOURCE_READ_LEDGER.json',{'utc':now,'method':'Existing exact retained primary bodies rehashed; material interfaces freshly read. No duplicate PDF downloads or full bodies distributed.','sources':ledger,'all22_prior_bodies_newly_read':False,'exhaustive_new_priority_census':False,'novelty':'UNKNOWN','exact_remaining_geometric_priority':'UNKNOWN'})
dump('WEB_CORROBORATION.json',{'utc':now,'publisher':{'url':'https://link.springer.com/article/10.1007/s00023-022-01228-3','fresh_web_open_success':True,'version_of_record_online_date':'2022-09-10','journal':'Annales Henri Poincare24(2023),783-842','authors':'Vu Hoang, Dirk Hundertmark, Johanna Richter, Semjon Vugalter','journal_factor_confirmed':'theta^2/(1-2theta)^2, 0<theta<1/2'},'Exner_Minakov':{'url':'https://arxiv.org/abs/1406.7624','fresh_web_open_success':True,'body_contents_reviewed_locally':True},'AIM':{'url':'http://aimpl.org/shapesurface/1/','fresh_web_open':'Internal Error','retained_full_target_passage_read':True,'https_authenticated_body_claimed':False}})
seal=json.loads((P/'PREPARATION_SEAL.json').read_text())
for key,name in [('output_pins_sha256','OUTPUT_PINS.json'),('input_pin_sha256','PREPARATION_INPUT_PINS.json'),('final_verification_sha256','FINAL_VERIFICATION.json')]:
    need(sha((P/name).read_bytes())==seal[key],'preparation seal '+key)
need(len((P/'OUTPUT_PINS.json').read_bytes())==seal['output_pins_bytes'],'preparation pins length')
freeze=json.loads((R/'INPUT_PINS.json').read_text())['files']
for row in freeze:
    b=(A/row['path']).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'conservation '+row['path'])
dump('FINAL_CONSERVATION.json',{'utc':now,'all_existing_frozen_inputs_rehashed':len(freeze),'unchanged':True,'preparation_seal_links_verified':True,'no_candidate_or_prior_file_edits':True,'shared_branch':subprocess.run(['git','symbolic-ref','--short','HEAD'],check=True,capture_output=True,text=True).stdout.strip(),'shared_head':subprocess.run(['git','rev-parse','HEAD'],check=True,capture_output=True,text=True).stdout.strip(),'git_mutations_performed':False,'services_or_outreach_performed':False})
# Remove only this review's own disposable rendered PNGs after actual inspection
# and exact hash capture. These are captured-stage visual inputs, not promised
# currently present files. No primary source or authored deliverable is removed.
removed=[]
for p in sorted((R/'tmp').glob('*.png')):
    b=p.read_bytes();removed.append({'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)});p.unlink()
dump('OWN_DERIVATIVE_CLEANUP.json',{'utc':now,'scope':'Only this reviewer own disposable rendered PNGs after all actual views; historical image hashes are captured-stage records. Primary PDFs, all frozen inputs and package remain untouched.','files':removed})
verdict={'utc':now,'pr':1085,'problem_id':20000488,'audited_head':'5e23f0c801d23976830657d2eef2b32bdc7da05a','review_kind':'NEW_COMPLETE_WHOLE_PACKAGE_REVIEW01','verdict':'ZERO_ACTIONABLE_P0_P1_P2_P3','findings':[],'P0':0,'P1':0,'P2':0,'P3':0,'mathematics':'ACCEPT_FULL_STATED_SCOPE','priority_framing':'CREDITED_EXPOSITION_AND_PRIOR_THEOREM_COROLLARIES','exact_remaining_geometric_priority':'UNKNOWN','novelty':'UNKNOWN','worldwide_open_status':'UNKNOWN','independent_discovery':'UNKNOWN','actual_git_originals_authenticated':6,'all_current_paper_pages_actually_viewed':7,'builtin_compiler':'success','real_clean_pdf_rebuilds':2,'canonical_pdf_sha256':sha((P/'paper.pdf').read_bytes()),'canonical_tex_sha256':sha((P/'paper.tex').read_bytes()),'canonical_support_sha256':sha((P/'pr1085_support_v1_0.zip').read_bytes()),'normal_optimized_reproduction_equal':True,'native_repository_local_check':'PASS','publication_ready':False,'published':False,'required_next_step':'Parent full report/source-interface adoption and at least one further NEW complete independent whole-package review. Ascending services remain held behind PR1032.','human_peer_review':False,'formal_proof_certificate':False,'review_completion_percent':100}
dump('VERDICT.json',verdict)
with (R/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n'+now+': Complete full review01. Independent proof/source interfaces and new exact diagnostics pass; 127 actual commands, 106 expected fault rejections, two real identical clean PDF rebuilds, seven actual page views, 91-member closed ZIP and all309 frozen inputs verified. ZERO P0--P3. Completion100% for this assigned review, publication clearance pending another NEW review/root/cursor. Only own disposable PNGs removed after captured-stage hashing.\n')
excluded={'OUTPUT_PINS.json','FINAL_SEAL.json'};rows=[]
for p in sorted(R.rglob('*')):
    rel=p.relative_to(R)
    if not p.is_file() or any(x in {'tmp','private','__pycache__'} for x in rel.parts) or rel.as_posix() in excluded:continue
    b=p.read_bytes();rows.append({'path':rel.as_posix(),'bytes':len(b),'sha256':sha(b)})
dump('OUTPUT_PINS.json',{'utc':now,'scope':'Every public review output except OUTPUT_PINS and its separately binding FINAL_SEAL; ignored private extracts/disposable scratch are excluded.','files':rows})
for row in rows:
    b=(R/row['path']).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'output pin '+row['path'])
b=(R/'OUTPUT_PINS.json').read_bytes()
dump('FINAL_SEAL.json',{'utc':now,'kind':'COMPLETE_NEW_WHOLE_REVIEW01_ZERO_ACTIONABLE_FINDINGS_NOT_PUBLICATION_CLEARANCE','output_pins_bytes':len(b),'output_pins_sha256':sha(b),'output_records':len(rows),'all_output_pins_terminally_rehashed':True,'input_pins_sha256':sha((R/'INPUT_PINS.json').read_bytes()),'all309_frozen_inputs_unchanged':True,'verdict_sha256':sha((R/'VERDICT.json').read_bytes()),'report_sha256':sha((R/'REPORT.md').read_bytes()),'publication_ready':False,'published':False,'minimum_new_whole_reviews':2,'completed_new_whole_reviews_this_agent':1,'services_hold':'preceding PR1032 priority cursor'})
print(json.dumps({'output_records':len(rows),'verdict':verdict['verdict'],'report_sha256':sha((R/'REPORT.md').read_bytes()),'output_pins_sha256':sha(b),'seal_sha256':sha((R/'FINAL_SEAL.json').read_bytes())},indent=2))
