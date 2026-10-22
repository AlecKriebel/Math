"""Fresh outcome gate and exact original blob capture; no mathematical acceptance."""
from pathlib import Path
import datetime,hashlib,json,subprocess
T=Path(__file__).resolve().parent
A=T/'audits/pr1280_30003587'
def run(*args):return subprocess.check_output(args,cwd=T.parent)
def save(path,obj):path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
p=json.loads(run('gh','pr','view','1280','--repo','AlecKriebel/Math','--json','number,title,url,state,isDraft,headRefOid,headRefName,baseRefName,body,files,commits'))
head='f5085a4c954f814cde1bc3be0727ff30373aea95'
bodysha='6ab00d803d8a28f0ac3450dc33c69752561482d2f4bb37e29024707c2ef6c213'
evidence='every finite abelian diagonal quasi-free action is strongly approximately inner.'
if p['state']!='OPEN' or p['isDraft'] is not True or p['headRefOid']!=head or hashlib.sha256(p['body'].encode()).hexdigest()!=bodysha or evidence not in p['body']:
    raise RuntimeError('Actual full-target draft outcome/head changed; re-gate before mathematical work')
expected={'ACCEPTANCE.json','CHECK_RESULTS.json','EDITORIAL_CHANGE_MAP.json','INDEPENDENT_AUDIT.md','MANIFEST.json','PROOF.md','README.md','SOURCE_METADATA.json','SOURCE_VERIFICATION.md'}
base='attempts/30003587/'
if len(p['files'])!=9 or {f['path'] for f in p['files']}!={base+n for n in expected}:raise RuntimeError('Unexpected actual original file scope')
if run('git','branch','--show-current').strip()!=b'main':raise RuntimeError('Stay on main')
A.mkdir(parents=True,exist_ok=True)
(A/'_local').mkdir(exist_ok=True)
(A/'.gitignore').write_text('_local/\n__pycache__/\n')
save(A/'LIVE_PR_PREFLIGHT.json',p)
(A/'_local/ORIGINAL_PR_BODY.md').write_text(p['body'])
run('git','fetch','--no-auto-maintenance','--no-tags','--no-write-fetch-head','origin','refs/pull/1280/head:refs/math-audit/1200-1300-20261017/pr1280-original')
parents=run('git','show','-s','--format=%P',head).decode().split()
if parents!=['a72180cf68ed6c9c54360cfd61b7a6567f5a0a5f']:raise RuntimeError('Unexpected original parent')
rows=[]
for d in ['submitted','current_edition']:(A/d).mkdir(exist_ok=True)
for f in p['files']:
    path=f['path'];blob=run('git','rev-parse',head+':'+path).decode().strip();data=run('git','cat-file','blob',blob)
    if hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()!=blob:raise RuntimeError('Original Git blob mismatch')
    name=Path(path).name
    for d in ['submitted','current_edition']:
        dest=A/d/name
        if dest.exists() and dest.read_bytes()!=data:raise RuntimeError('Do not overwrite a different captured original')
        dest.write_bytes(data)
    rows.append({'path':path,'local_path':'submitted/'+name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'git_blob_sha1':blob})
if sum(r['bytes'] for r in rows)!=74387:raise RuntimeError('Original total bytes differ')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
snapshot={'at_utc':now,'pr':1280,'problem_id':30003587,'url':p['url'],'title':p['title'],'head':head,'branch':p['headRefName'],'parents':parents,'body_sha256':bodysha,'files':rows,'scope':'Exact nine original Git bodies. Historical acceptance/finite-check declarations are not current proof or priority certification.'}
save(A/'SUBMITTED_SNAPSHOT.json',snapshot)
save(A/'ELIGIBILITY_REVALIDATION.json',{'at_utc':now,'pr':1280,'problem_id':30003587,'head':head,'body_sha256':bodysha,'decision':'eligible_explicit_full_original_target_claim','evidence':evidence,'outcome_files_read_for_gate':['ACCEPTANCE.json','README.md'],'catalog_problem_status_observed':'partially_solved','policy':'Latest human rule uses actual explicit full-target recorded outcome. Generic no-novelty limits do not override it. No truth/priority acceptance inferred.'})
source=run('python3','unsolved_math_prioritization/queue.py','show','30003587');(A/'_local/ORIGINAL_PROBLEM_SHOW.json').write_bytes(source)
with (A/'RESEARCH_LOG.md').open('a') as stream:stream.write('\n## '+now+' — live full-target admission (5%)\n\nActual current draft/head/body revalidated. The PR explicitly claims the full finite-abelian strong approximate-innerness theorem; catalog partially-solved status is stale. Nine original Git blobs and their74387-byte total authenticated. Historical AI acceptance and finite checks are not current validation. Root and independent mathematical/priority reviews remain unstarted. Main checkout/index untouched.\n')
statepath=T/'PROGRAM_STATE.json';state=json.loads(statepath.read_text());state.update(current_pr=1280,current_pr_stage='independent_mathematical_review',current_pr_completion_estimate_percent=5,current_pr_math_gate_families={'pr':1280,'status':'pending'});save(statepath,state)
print(json.dumps({'at_utc':now,'head':head,'parents':parents,'files':rows},indent=2))
