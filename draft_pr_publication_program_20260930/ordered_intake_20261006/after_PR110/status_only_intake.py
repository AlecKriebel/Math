#!/usr/bin/env python3
"""Read immutable head QUEUE rows in numeric order; no mathematical intake of skipped statuses."""
from pathlib import Path
from datetime import datetime,timezone
import base64,hashlib,importlib.util,json,os,re,sys
D=Path(__file__).resolve().parent;P=D.parents[1];C=P.parent;A=P/'audits/pr110_5100032'
f=A/'native_post_assess_carryforward_v3_20261006/native_acceptance_actions_v4.py'
s=importlib.util.spec_from_file_location('bounded_readonly_runtime',f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
need=m.need
need(dict(os.environ)==m.START_ENV and sys.flags.ignore_environment and sys.flags.no_site and sys.flags.dont_write_bytecode and sys.flags.safe_path,'Exact clean physical startup')
release=m.loads(m.read(A/'FINAL_COMPLETION_OWNER_RELEASE_20261006.json',65536))
need(release['PR']==110 and release['writer_ownership_released'] is True and release['next_ordered_status_only_intake_authorized_now'] is True and release['remote_verified'] is True and release['GitHub_MERGED_confirmed'] is True,'Actual previous completion and explicit release')
packet=m.loads(m.read(A/'native_actual_input_preparation_20261006/root_fresh_native_preflight_20261006/EXECUTION_INPUTS.json',512*1024));rt=packet['runtime'];m.validate_runtime(rt)
capture=m.Capture(D/'actual_readonly_intake',whole_seconds=300)
registryraw=m.gh(capture,rt,'pr','list','--repo','AlecKriebel/Math','--state','open','--draft','--limit','1000','--json','number,title,headRefOid,headRefName,baseRefName,url,isDraft')
registry=m.loads(registryraw);need(isinstance(registry,list) and len(registry)<1000,'Complete bounded live registry')
m.atomic(D/'LIVE_DRAFT_REGISTRY.json',registryraw)
rows=[];chosen=None
for pr in sorted(registry,key=lambda x:x['number']):
    number=pr['number']
    if number<111 or number==8:continue
    need(pr['isDraft'] is True and pr['baseRefName']=='main' and re.fullmatch(r'[0-9a-f]{40}',pr['headRefOid']),'Draft immutable head identity')
    match=re.fullmatch(r'dot/math-([0-9]+)',pr['headRefName']);need(match is not None,'Expected math problem head branch')
    problem=int(match.group(1));head=pr['headRefOid'];path='unsolved_math_prioritization/QUEUE.md'
    raw=m.gh(capture,rt,'api','repos/AlecKriebel/Math/contents/'+path+'?ref='+head)
    response=m.loads(raw);need(response['type']=='file' and response['path']==path and response['encoding']=='base64','Full immutable QUEUE file response')
    body=base64.b64decode(response['content'],validate=False);need(len(body)==response['size'] and hashlib.sha1(('blob '+str(len(body))+'\0').encode()+body).hexdigest()==response['sha'],'Exact full authenticated Git blob')
    matches=[]
    for line in body.decode().splitlines():
        if not line.startswith('|'):continue
        cells=[x.strip() for x in line.split('|')[1:-1]]
        if len(cells)>=9 and cells[1].split('/')[0].strip()==str(problem):matches.append((line,cells))
    need(len(matches)==1,'Unique exact target QUEUE row')
    line,cells=matches[0];status=cells[7];eligible=status=='claimed_solved'
    m.atomic(D/('PR'+str(number)+'_AUTHENTICATED_HEAD_QUEUE.md'),body)
    row={'PR':number,'problem_id':problem,'head':head,'literal_status':status,'effort':cells[8],'eligible':eligible,'queue_bytes':len(body),'queue_sha256':hashlib.sha256(body).hexdigest(),'queue_Git_blob':response['sha'],'row':line,'math_review_or_remote_action_if_ineligible':False}
    rows.append(row)
    if eligible:
        verify=m.loads(m.gh(capture,rt,'pr','view',pr['url'],'--json','number,isDraft,state,headRefOid,headRefName,baseRefName,url,title'))
        need(verify['number']==number and verify['state']=='OPEN' and verify['isDraft'] is True and verify['headRefOid']==head and verify['headRefName']==pr['headRefName'] and verify['baseRefName']=='main','Selected immutable live draft reauthenticated')
        chosen={**row,'PR_metadata':verify};break
result={'schema':'ordered-literal-claimed-solved-intake/v1','UTC':m.now(),'actual_operator_PID':os.getpid(),'previous_PR110_completed_and_writer_released':True,'previous_actual_release_record':'audits/pr110_5100032/FINAL_COMPLETION_OWNER_RELEASE_20261006.json','previous_completed_metadata_main':release['completion_metadata_commit'],'ascending_status_only_rows':rows,'next_eligible_PR':None if chosen is None else chosen['PR'],'next_problem_id':None if chosen is None else chosen['problem_id'],'next_selected':chosen,'scope':'Only literal claimed_solved; all other statuses skipped after eligibility row authentication.','source_review_complete':False,'goal_complete':False,'Git_mutations':0,'service_writes':0}
m.save(D/'INTAKE_AFTER_PR110.json',result)
print(json.dumps({'actual_operator_PID':os.getpid(),'status_only_rows':[{'PR':x['PR'],'status':x['literal_status'],'eligible':x['eligible']} for x in rows],'next_eligible_PR':result['next_eligible_PR'],'next_problem_id':result['next_problem_id']}))
