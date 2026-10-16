#!/usr/bin/env python3
"""Bind the exact reviewed inputs and this review's final records."""
import datetime
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import zipfile

HERE=Path(__file__).absolute().parent
A=HERE.parents[1]
REPO=A.parents[2]
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda data:hashlib.sha256(data).hexdigest()
def pin(path):
    if not stat.S_ISREG(path.lstat().st_mode):raise ValueError('nonregular input '+str(path))
    data=path.read_bytes();return {'bytes':len(data),'sha256':sha(data)}
def write(name,value):
    (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
pre=json.loads((A/'PRE_REVIEW_PACKET_INPUTS.json').read_bytes())
records={}
for name,record in pre['files'].items():
    if pin(A/name)!=record:raise ValueError('pre-review scientific input drift: '+name)
    records[name]=record
records['PRE_REVIEW_PACKET_INPUTS.json']=pin(A/'PRE_REVIEW_PACKET_INPUTS.json')
ops_path=A/'reviews/operations_author_01/FINAL_FREEZE.json'
if sha(ops_path.read_bytes())!='1c5919ed21e193c369a95388170da3a65e8c3e11a002e9c8febbc262415efa58':raise ValueError('operational freeze drift')
ops=json.loads(ops_path.read_bytes())
for name,record in ops['files'].items():
    if pin(A/name)!=record:raise ValueError('operational input drift: '+name)
    records[name]=record
records['reviews/operations_author_01/FINAL_FREEZE.json']=pin(ops_path)
with zipfile.ZipFile(A/'publication/real_schlicht_verification.zip') as archive:
    manifest=json.loads(archive.read('PACKAGE_MANIFEST.json'))
    pubnames={n for n in pre['files'] if n.startswith('publication/')}
    for row in manifest['files']:
        name=row['path'];mapped='publication/PACKAGE_README.md' if name=='README.md' else (
            'publication/'+name if 'publication/'+name in pubnames else name)
        record={'bytes':row['bytes'],'sha256':row['sha256']}
        if pin(A/mapped)!=record:raise ValueError('actual archived input drift: '+mapped)
        records[mapped]=record
source_paths={
    'Hayman–Lingham 2018 v2':A/'reviews/covariance_source_01/tmp/1809.07200v2.pdf',
    'Koepf 1986':A/'reviews/classical_priority_01/tmp/koepf1986.pdf',
    'Jenkins 1962':A/'reviews/classical_priority_01/tmp/jenkins1962_provided_primary.pdf',
    'Rodemich 1979 issue':A/'reviews/classical_priority_01/tmp/rodemich1979_recovered_primary.pdf',
}
sources={title:{'local_read_only_input':str(path),'pin':pin(path)} for title,path in source_paths.items()}
rendered={p.name:pin(p) for p in sorted((HERE/'tmp/rendered').glob('*.png'))}
write('SOURCE_CHECKS.json',{'utc':now(),'source_inputs':sources,'rendered_pages':rendered,
    'visually_read_complete_pages':['paper 1','paper 2','paper 3','paper 4','paper 5','H–L printed114','H–L printed147','Koepf printed578','Jenkins1962 printed7','Rodemich printedA-68'],
    'read_full_koepf_five_page_text':True,'third_party_fulltexts_in_review_release':False,
    'Jenkins1960_original_obtained':False,'Aleksandrov_Popova1973_original_obtained':False,
    'no_historical_firstness_or_current_openness_certification':True})
kit=REPO/'zenodo_deposit_tool/zenodo.py'
if pin(kit)['sha256']!='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca':raise ValueError('shared kit identity drift')
external_read_only_files={str(kit):pin(kit)}
live=json.loads(subprocess.check_output(['gh','pr','view','662','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,url'],cwd=REPO))
head='e31701151c331a6eed9224fb37a75a374ea1043e'
if not(live['number']==662 and live['state']=='OPEN' and live['isDraft'] is True and live['headRefOid']==head and live['baseRefName']=='main'):
    raise ValueError('live scope gate drift')
queue=subprocess.check_output(['git','show',head+':unsolved_math_prioritization/QUEUE.md'],cwd=REPO)
rows=[line for line in queue.decode().splitlines() if len(line.split('|'))>2 and line.split('|')[2].strip()=='2306086 / AMR-022-6086']
snapshot=json.loads((A/'SCOPE_AND_SNAPSHOT.json').read_bytes())
if rows!=[snapshot['queue_row']] or rows[0].split('|')[8].strip()!='claimed_solved':raise ValueError('exact claimed_solved row drift')
write('LIVE_PR_SCOPE_RECHECK.json',{'utc':now(),'pr':live,'queue_row':rows[0],'exact_status':'claimed_solved','no_other_pr_contents_read':True})
normal=json.loads((HERE/'INDEPENDENT_CHECKS.normal.json').read_bytes())
optimized=json.loads((HERE/'INDEPENDENT_CHECKS.optimized.json').read_bytes())
opn=json.loads((HERE/'OPERATIONAL_CHECKS.normal.json').read_bytes())
opo=json.loads((HERE/'OPERATIONAL_CHECKS.optimized.json').read_bytes())
for report,expected in ((normal,180),(optimized,180),(opn,76),(opo,76)):
    if report['status']!='PASS' or report['checks']!=expected:raise ValueError('review controls incomplete')
if normal['results']!=optimized['results'] or opn['results']!=opo['results']:raise ValueError('own ordinary/optimized disagreement')
inputs={'schema':'pr662-round2-input-pins-v1','utc':now(),'relative_to':'audits/pr662_2306086',
    'files':records,'external_read_only_files':external_read_only_files,
    'shared_kit_pin_is_provenance_only_no_unprepared_transport_approval':True,
    'science_pre_review_packet_unchanged':True,'operational_author_freeze_unchanged':True}
write('INPUT_PINS.json',inputs)
verdict={'schema':'pr662-whole-package-review-verdict-v1','reviewer_id':'/root/pr662_package_round2',
    'utc':now(),'pr':662,'problem_id':'2306086','original_head':head,
    'verdict':'PASS_SCOPED_QUALITATIVE_PREPRINT_AND_FROZEN_OPERATIONS',
    'mandatory_findings':0,'optional_findings':0,'findings':[],
    'subtask_completion_estimate_percent':100,'qualitative_scope_only':True,
    'historical_firstness_certified':False,'present_openness_certified':False,'sharp_radius_determined':False,
    'human_peer_review':False,'AI_tools_used_extensively':True,
    'paper_pdf':pin(A/'publication/real_schlicht_preschwarzian.pdf'),
    'verification_zip':pin(A/'publication/real_schlicht_verification.zip'),
    'independent_math_integrity_tamper_rebuild_checks_per_mode':180,
    'independent_operational_checks_per_mode':76,'frozen_author_operational_controls_per_mode':147,
    'actual_proposed_layout_replayed':True,'optional_numerical_replayed_uncertified':True,
    'all_input_pins_sha256':pin(HERE/'INPUT_PINS.json')['sha256'],
    'findings_sha256':pin(HERE/'FINDINGS.md')['sha256'],
    'no_target_files_modified':True,'no_live_mutations_or_external_outreach':True,
    'future_live_metadata_publication_doi_tracker_head_and_merge_checks_remain_required':True,
    'unprepared_future_transport_adapters_approved':False}
write('VERDICT.json',verdict)
checked=[]
for name,record in records.items():
    if pin(A/name)!=record:raise ValueError('final input drift: '+name)
    checked.append(name)
for name,record in external_read_only_files.items():
    if pin(Path(name))!=record:raise ValueError('external read-only input drift: '+name)
write('FINAL_INPUT_RECHECK.json',{'utc':now(),'status':'PASS','inputs_checked':len(checked),
    'all_original_science_and_frozen_operations_unchanged':True,'input_pins_sha256':pin(HERE/'INPUT_PINS.json')['sha256'],
    'ordinary_optimized_own_control_results_identical':True,'live_original_draft_and_exact_claimed_solved_row_confirmed':True,
    'source_pdf_inputs_are_read_only_and_excluded_from_release':True})
with (HERE/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n- '+now()+' — Final scientific/operational pins and exact live scope rechecked; all unchanged. PASS, zero mandatory and zero optional findings. Completion estimate: 100% of this bounded review. No novelty, current-openness, sharp-radius, numerical certification, or actual-publication assertion.\n')
own={p.name:pin(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='FINAL_FREEZE.json'}
write('FINAL_FREEZE.json',{'schema':'pr662-round2-final-freeze-v1','utc':now(),
    'reviewer_id':'/root/pr662_package_round2','subtask_completion_estimate_percent':100,
    'files':own,'excludes':['tmp/**','FINAL_FREEZE.json'],'immutable_after_checkpoint':True})
print(json.dumps({'status':'PASS','mandatory_findings':0,'optional_findings':0,
    'input_files':len(records),'review_files':len(own),'verdict':pin(HERE/'VERDICT.json'),
    'final_freeze':pin(HERE/'FINAL_FREEZE.json')},indent=2))

if __name__!='__main__':raise ValueError('execute directly')
