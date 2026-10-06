#!/usr/bin/env python3
import datetime,hashlib,json,os,pathlib
D=pathlib.Path(__file__).resolve().parent
A=D.parent
def record(path):
    body=path.read_bytes()
    return {'path':str(path.relative_to(D)) if path.is_relative_to(D) else str(path),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
def dump(filename,value):
    (D/filename).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
sources=[
('laclair_2304.13299v1.pdf','https://arxiv.org/pdf/2304.13299v1','2023-04-26T05:46:23Z',['Introduction','Theorem2.12/Remark2.13','equation8','complete Proposition3.12/Lemma3.13 proof','Corollary3.14/Remark3.15']),
('laclair_published_2025.pdf','https://link.springer.com/content/pdf/10.1007/s10801-025-01439-x.pdf','2025-07-15',['Introduction','physical9 Theorem2.12/Remark2.13','physical12 equation8','physical15-18 complete Proposition3.12/Lemma3.13 proof','physical18 Corollary3.14/Remark3.15']),
('blanco_encinas_1405.3942v1.pdf','https://arxiv.org/pdf/1405.3942v1','2014-05-15T18:51:02Z',['Introduction','complete Example5.6 physical/printed26-27']),
('blanco_encinas_1405.3942v5.pdf','https://arxiv.org/pdf/1405.3942v5','2017-02-11T11:53:49Z',['Introduction','Definition5.3/Remark5.4','Example5.5','complete Theorem5.10/5.11 proof','complete Example6.6 physical/printed34-35']),
('takagi2013_official.pdf','https://msp.org/ant/2013/7-4/ant-v7-n4-p06-s.pdf','2013',['Title/DOI/front matter','augmented matrix printed937 physical22','complete Remark4.3 printed939 physical24','complete Example4.4 printed940 physical25']),
]
entries=[]
for name,url,date,reads in sources:
    v=record(D/'private_sources'/name);v.update(url=url,publication_or_repository_date=date,actual_read_locations=reads,body_private_ignored=True);entries.append(v)
for name,url,reads in [('laclair_2304.13299v2.pdf','https://arxiv.org/pdf/2304.13299v2',['Introduction','Theorem2.12/Remark2.13','equation8','complete Proposition3.12/Lemma3.13 proof','Corollary3.14/Remark3.15']),('shibuta_takagi_0810.1278v3.pdf','https://arxiv.org/pdf/0810.1278v3',['complete Proposition2.1 proof and Question2.2 pp6-8'])]:
    v=record(A/'primary_source_scope_adversary_20261006/private_sources'/name);v.update(url=url,actual_read_locations=reads,body_private_ignored=True);entries.append(v)
render_names=['blanco_v1-26.png','blanco_v1-27.png','blanco_v5-34.png','blanco_v5-35.png','laclair_published-18.png','takagi2013-22.png','takagi2013-24.png','takagi2013-25.png']
dump('SOURCE_MANIFEST.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'sources':entries,'actually_visually_inspected_renders':[record(D/'private_renders'/name) for name in render_names],'copyrighted_bodies_not_redistributed':True,'access_boundaries':['Blanco subscription publisher PDF unavailable: HTML redirect not PDF','Blanco Valladolid repository timed out','Publisher metadata online2017/issue2018 read; journal body identity not claimed'],'search_limit':'Bounded primary-source search through2026-10-06; no-hit searches never priority proof'})
checkpoint=json.loads((D/'INDEPENDENCE_CHECKPOINT.json').read_text())
if record(D/checkpoint['checkpoint_path'])['sha256']!=checkpoint['sha256']:raise ValueError('Independent checkpoint changed')
candidate=A/'original_head_authentication_20261006/original_attempt/CANDIDATE.md'
if record(candidate)['sha256']!='1409e8ad35d34f3cc4a9bb14f7e42318c1dd1e0446ecba525c655fad8c978cdf':raise ValueError('Immutable candidate changed')
controls=json.loads((D/'CONTROL_PROCESS_RECEIPT.json').read_text())
if controls['status']!='PASS' or any(r['summary']['guard_count']!=1210 for r in controls['runs'][:2]):raise ValueError('Incomplete effective controls')
result={'schema':'pr117-later-binomial-priority-audit/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_seal_PID':os.getpid(),'PR':117,'problem_id':30001234,'immutable_head':'8163ee0dc7a0f944570925984cef2dc0fb291ad8','candidate':record(candidate),'original_attempts':'1/5','new_central_candidate_proof_search_turns':0,'math_status':'valid','priority_disposition_recommendation':'already_solved','decisive_prior':'Takagi2013 Example4.4 same ideal and augmented-image hypothesis','explicit_prior_same_example':True,'original_open_problem_novel_resolution_supported':False,'substantive_novel_contribution_established':False,'current_proof_and_verification_details_useful':True,'unresolved_priority_mapping_concerns':[],'originals_caches_preserved':True,'global_native_Git_service_mutations':False,'family_completion_percent':100,'report':record(D/'REPORT.md'),'independent_checkpoint':checkpoint,'control_receipt':record(D/'CONTROL_PROCESS_RECEIPT.json'),'effective_guard_counts':{'normal':1210,'optimized':1210},'deliberate_false_controls_rejected':2,'private_source_body_count':len(entries),'root_disposition_and_global_corrections_pending':True}
dump('RESULT.json',result)
members=[]
for path in sorted(D.iterdir()):
    if path.is_dir():continue
    if path.name in ['OUTPUT_MANIFEST.json','SHA256SUMS']:continue
    if path.suffix in ['.pdf','.png','.html']:raise ValueError('Copyright/private media leaked into public root')
    members.append(record(path))
manifest={'schema':'public-safe-output-manifest/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_seal_PID':os.getpid(),'members':members,'excludes':['private_sources/','private_renders/','__pycache__/','OUTPUT_MANIFEST.json','SHA256SUMS'],'private_bodies_excluded':True}
dump('OUTPUT_MANIFEST.json',manifest)
(D/'SHA256SUMS').write_text(''.join(r['sha256']+'  '+r['path']+'\n' for r in members))
for r in members:
    if record(D/r['path'])!=r:raise ValueError('Sealed member changed')
print(json.dumps({'actual_seal_PID':os.getpid(),'members':len(members),'RESULT':record(D/'RESULT.json'),'REPORT':record(D/'REPORT.md'),'MANIFEST':record(D/'OUTPUT_MANIFEST.json'),'status':'SEALED','family_completion_percent':100},indent=2,sort_keys=True))
