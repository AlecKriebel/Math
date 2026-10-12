"""Read-only numeric intake of immutable literal claimed_solved draft heads."""
from pathlib import Path
import base64,datetime,hashlib,json,os,re,subprocess
D=Path(__file__).resolve().parent
P=D.parents[1]
C=P.parent
A=P/'audits/pr111_4900006'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value,label):
    if not value:raise RuntimeError(label)
def dump(path,obj):path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def run(args):
    started=now();child=subprocess.Popen([GH,*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate(timeout=120)
    events.append({'argv':[GH,*args],'PID':child.pid,'start_UTC':started,'end_UTC':now(),'exit_code':child.returncode,
        'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),
        'stderr_sha256':hashlib.sha256(err).hexdigest()})
    dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
    require(child.returncode==0,err.decode('utf-8','replace')[:1000])
    return out
require(not (D/'INTAKE_AFTER_PR111.json').exists(),'Existing intake: inspect before retry')
release=json.loads((A/'FINAL_COMPLETION_OWNER_RELEASE_20261006.json').read_text())
require(release['PR']==111 and release['actual_remote_main_verified'] and release['actual_same_head_closed_without_merge']
    and release['writer_ownership_released'] and release['actual_release_API_accepted']
    and release['next_ordered_status_only_intake_authorized_now'],'Actual preceding completion/release')
registry=json.loads(run(['pr','list','--repo','AlecKriebel/Math','--state','open','--draft','--limit','1000',
    '--json','number,title,headRefOid,headRefName,baseRefName,url,isDraft']))
require(isinstance(registry,list) and len(registry)<1000,'Complete bounded registry')
dump(D/'LIVE_DRAFT_REGISTRY.json',registry)
rows=[];chosen=None
for pr in sorted(registry,key=lambda x:x['number']):
    number=pr['number']
    if number<112 or number==8:continue
    require(pr['isDraft'] and pr['baseRefName']=='main' and re.fullmatch(r'[0-9a-f]{40}',pr['headRefOid']),'Draft identity')
    match=re.fullmatch(r'dot/math-([0-9]+)',pr['headRefName'])
    require(match is not None,'Numeric problem branch')
    problem=int(match.group(1));head=pr['headRefOid'];path='unsolved_math_prioritization/QUEUE.md'
    response=json.loads(run(['api','repos/AlecKriebel/Math/contents/'+path+'?ref='+head]))
    require(response['type']=='file' and response['path']==path and response['encoding']=='base64','Immutable full QUEUE file')
    body=base64.b64decode(response['content'])
    require(len(body)==response['size'] and hashlib.sha1(('blob '+str(len(body))+'\0').encode()+body).hexdigest()==response['sha'],'Full Git blob authentication')
    matches=[]
    for line in body.decode().splitlines():
        if not line.startswith('|'):continue
        cells=[x.strip() for x in line.split('|')[1:-1]]
        if len(cells)>=9 and cells[1].split('/')[0].strip()==str(problem):matches.append((line,cells))
    require(len(matches)==1,'Unique exact target row')
    line,cells=matches[0];status=cells[7];eligible=status=='claimed_solved'
    (D/('PR'+str(number)+'_AUTHENTICATED_HEAD_QUEUE.md')).write_bytes(body)
    row={'PR':number,'problem_id':problem,'head':head,'literal_status':status,'effort':cells[8],'eligible':eligible,
        'queue_bytes':len(body),'queue_sha256':hashlib.sha256(body).hexdigest(),'queue_Git_blob':response['sha'],
        'row':line,'math_review_or_service_action_if_ineligible':False}
    rows.append(row)
    if eligible:
        live=json.loads(run(['pr','view',pr['url'],'--json','number,isDraft,state,headRefOid,headRefName,baseRefName,url,title']))
        require(live['number']==number and live['state']=='OPEN' and live['isDraft'] and live['headRefOid']==head
            and live['headRefName']==pr['headRefName'] and live['baseRefName']=='main','Selected immutable draft live readback')
        chosen={**row,'PR_metadata':live};break
record={'schema':'ordered-literal-claimed-solved-intake/v1','UTC':now(),'actual_operator_PID':os.getpid(),
    'previous_PR111_completed_and_writer_released':True,'previous_actual_release_record':'audits/pr111_4900006/FINAL_COMPLETION_OWNER_RELEASE_20261006.json',
    'previous_completed_metadata_main':release['completion_metadata_commit'],'ascending_status_only_rows':rows,
    'next_eligible_PR':None if chosen is None else chosen['PR'],'next_problem_id':None if chosen is None else chosen['problem_id'],
    'next_selected':chosen,'scope':'Only literal immutable-head claimed_solved; skip8 and all other statuses entirely.',
    'source_review_complete':False,'goal_complete':False,'Git_mutations':0,'service_writes':0,
    'program_completed_at_intake':19,'dated_eligible_total':99,'program_estimate_percent':19/99*100}
dump(D/'INTAKE_AFTER_PR111.json',record)
print(json.dumps({'actual_operator_PID':os.getpid(),'status_only_rows':[{'PR':x['PR'],'status':x['literal_status'],'eligible':x['eligible']} for x in rows],
    'next_eligible_PR':record['next_eligible_PR'],'next_problem_id':record['next_problem_id']}))
