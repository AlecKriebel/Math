from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
C=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr210_5100033');D=C/'initial_review_20261015';B=C/'preprint';O=Path(__file__).resolve().parent;P=C/'publication';P211=C.parent/'pr211_5100063/initial_review_20261015'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
rows=[]
def source(path,coverage,expected=None,visual=False):
 h=sha(path)
 if expected:assert h==expected,(str(path),h)
 rows.append({'path':str(path),'bytes':path.stat().st_size,'sha256':h,'coverage':coverage,'actually_visually_viewed':visual})
expected={'invariants_v11.pdf':'c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da','invariants_final.pdf':'c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42','stachel_published.pdf':'9121028d7295435740cebb25ec60abe1a0dcc4e96686c226b1b6533bd49515d8'}
for name,h in expected.items():source(D/'private_reading'/name,'Fresh hash; supplied directly to genuine-primary meromorphic replay. Relevant extracted passages separately read.',h)
for name,coverage in [('invariants_v11.txt','Section2 signed area; sections3.4/3.7 construction and original foci; Table7 p9 k605,a primed product.'),('invariants_final.txt','Section2 signed area; Table7 and Section3.7 p349 k606 primed outer-foot product, distinct unprimed k605.'),('stachel_published.txt','Printed1613-1614 canonical context, Theorem4.3 and Eq4.9 including coprime turning numbers; nearby erroneous dn sign is not used.')]:source(D/'private_reading'/name,coverage)
source(P211/'priority_author_updates_01/private_reading/invariants_v1.pdf','Fresh PDF hash; actual preserved PNG pages5-6 read visually for Section3.6/Table5 k604.', '085ecad4062dc55d4ae8053c693acb8121f928a992c3e850d943964b949810e7')
source(P211/'priority_author_updates_01/private_reading/euler62.pdf','Fresh six-page primary PDF hash; full extracted text read and actual page6 image viewed.','c7fbcc7e5a7b7746ad102cb7cf0f5e9eb6aa149009d88c3654fdbcc3484126c0')
source(P211/'priority_author_updates_01/private_reading/euler62.txt','Complete six-page primary text: theorem, vector poles, isotropic coefficients, order removal, reduced lattice/antiperiod, positivity, repeats/circle, exact controls and literal false square.')
source(D/'priority_author_updates_01/private_reading/ferudun14_v11.pdf','Fresh PDF hash; definitions/Theorems1-2 and parallel-residue/complementary-zero proof read in extracted text.')
source(D/'priority_author_updates_01/private_reading/ferudun14_v11.txt','Read definitions/Theorems1-2, canonical/outer identities, Lemma4 pole bound and Section5 zeros. Different parity/point observable; substantive methodological antecedent.')
source(D/'priority_classical_general_01/private_reading/ks_pramana_final_ias.txt','Read actual published-text copy: parameter m=k², periods, Eq7-9 p923, complete Section2.1 pp924-926, and odd summary Eq58 p931. Underlying PDF not freshly hashed because only extracted text retained here.','c37d396f97527c5c488202c3a4e96e7fbbf2d9d68be88f7dac6b4e4643516b36')
for name,coverage in [('root_v1_table5.png','Actual v1 printedp5 Section3.6 original-focus unprimed/primed definition.'),('root_v1_actual_table5.png','Actual v1 printedp6 Table5: k604 primed product, odd, date4/20, proof?.'),('root_final_table7.png','Actual publishedp349 Table7 k606 primed product and Section3.7 definition.'),('f62_page-6.png','Actual cited0062 printedp6 square coordinates; visually confirms the fixture typo isolated by current package.')]:source(D/'private_reading'/name,coverage,visual=True)
prior=[]
for name,h in [('whole_manuscript_adversary_01','acd3f1751af73a3902d0f6d31ecc6d9d9dcb8d60ed020ff86e99dd3ff203ea99'),('whole_manuscript_adversary_02','489aa49704fea4b99e6e3c1b2f63e9bbb0d486427fd30531547976c85e2bc2a3')]:
 f=D/name/'REPORT.md';assert sha(f)==h
 man=D/name/'AUTHORED_MANIFEST.json';mm=load(man);rs=mm.get('authored_files',mm.get('files'))
 for r in rs:
  p=man.parent/r['path'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
 prior.append({'family':name,'report_sha256':h,'manifest_sha256':sha(man),'manifest_payloads':len(rs)})
assert prior[1]['manifest_sha256']=='c6eb0e365bbfe98f48cdc29be608b398731fad98a82d0d81e30d707823a22632'
plan=load(B/'NATIVE_RELEASE_PLAN.json');policy=load(P/'CURRENT_RELEASE_POLICY.json')
assert plan['PR_reconciliation_parent_rule']==policy['PR_reconciliation_parents']==['2180d64b648b81ac660a792f7823d0b715f9cf12','freshly observed MAIN commit']
assert 'Sole-parent commits apply only to separate MAIN progress checkpoints' in plan['required_native_guard']
assert policy['MAIN_checkpoint_parents']=='one fresh MAIN parent' and policy['expected_head_branch']=='dot/math-5100033' and policy['expected_repository']=='AlecKriebel/Math'
code=(P/'integrate_reviewed_pr.py').read_text();assert "'parents': [OLD, main]" in code and "actual_commit['parents']] == [OLD,main]".replace(' == ','==') in code
root=load(D/'ROOT_PORTABLE_REPRODUCTION_RECEIPT_V4.json');assert sha(D/'ROOT_PORTABLE_REPRODUCTION_RECEIPT_V4.json')=='2c3cdbd0d53ccc1e2bf25caae91b3a3eb1b3a3b62b88bb2b690bea100d12ef04'
ours=load(O/'PORTABLE_REPLAY_RECEIPT.json');assert len(root['jobs'])==len(ours['jobs'])==10
assert {x['job']:x['scientific_canonical_sha256'] for x in root['jobs']}=={x['job']:x['scientific_canonical_sha256'] for x in ours['jobs']}
genuine=load(O/'GENUINE_PRIMARY_REPLAY_RECEIPT.json');assert genuine['jobs'][0]['attested_primary_hash_substitution_count']==0 and genuine['jobs'][0]['scientific_canonical_sha256']==next(x['scientific_canonical_sha256'] for x in ours['jobs'] if x['job']=='meromorphic_divisor')
(O/'SOURCE_AND_RELEASE_RECEIPT.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'sources':rows,'prior_whole_reviews_read_only_after_independent_freeze':prior,'resolutions':{s:sha(B/s) for s in ['REVIEW01_RESOLUTION.json','REVIEW02_RESOLUTION.json']},'release_plan':{'package_plan_sha256':sha(B/'NATIVE_RELEASE_PLAN.json'),'external_policy_sha256':sha(P/'CURRENT_RELEASE_POLICY.json'),'helper_readonly_sha256':sha(P/'integrate_reviewed_pr.py'),'parent_rules_agree':True,'helper_actions_imported_or_executed':False,'helper_clearance_is_separate':True,'local_FINAL_CLEARANCE_exists':(C/'FINAL_CLEARANCE.json').exists() or (D/'FINAL_CLEARANCE.json').exists()},'root_v4_scientific_hashes_agree':True,'genuine_and_offline_scientific_hashes_agree':True,'limits':['No exhaustive new priority search performed.','KS final underlying PDF hash is historical attestation; actual published extracted text was read and freshly hashed.','Source PDFs/texts/PNGs are not copied into authored outputs.','Stachel Triple full-text and complete final Talented comparison gaps remain.','No external/publication/native/tracker action or action-helper execution.']},indent=2)+'\n')
print('PASS source and release-plan audit;',len(rows),'source file receipts')
