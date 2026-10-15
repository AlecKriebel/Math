"""Gate PR66 and authenticate initial immutable mathematical inputs; read-only."""
from pathlib import Path
import base64,datetime as dt,hashlib,json,os,subprocess,sys
A=Path(__file__).resolve().parent;R=A.parents[2]
F=A/'ROOT_initial_source_projection_20261004';F.mkdir(exist_ok=False)
D=Path('/Users/alec/.cache/codex-pr66-audit-20261004/initial_source_commands');D.mkdir(exist_ok=False)
(D/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
HEAD='78f4a7fadac0fd24e147a617956cb409eb6a579e';PREFIX='unsolved_math_prioritization/attempts/10400033/'
records=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def run(argv):
    start=dt.datetime.now(dt.timezone.utc).isoformat();c=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=c.communicate();n=str(len(records)+1)
    q={'argv':argv,'actual_child_pid':c.pid,'start_utc':start,'finish_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':c.returncode}
    for k,b in [('stdout',out),('stderr',err)]:
        p=D/(n+'.'+k);p.write_bytes(b);q[k]={'private_path':str(p),'bytes':len(b),'sha256':sha(b)}
    records.append(q);(F/'ACTUAL_COMMANDS.json').write_text(json.dumps(records,indent=2)+'\n')
    if c.returncode:raise RuntimeError('Source retrieval failed; inspect retained streams')
    return out
def api(path):return json.loads(run(['gh','api','repos/AlecKriebel/Math/'+path]))
if sys.flags.optimize or not sys.flags.ignore_environment or not sys.flags.dont_write_bytecode:raise RuntimeError('Invoke -E -B without optimization')
pr=json.loads(run(['gh','pr','view','66','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName']))
if not(pr['number']==66 and pr['state']=='OPEN' and pr['isDraft'] and pr['headRefOid']==HEAD and pr['baseRefName']=='main' and pr['headRefName']=='dot/math-10400033'):raise RuntimeError('Fresh exact-head gate failed')
queue=api('contents/unsolved_math_prioritization/QUEUE.md?ref='+HEAD);body=base64.b64decode(queue['content']);blob=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
rows=[s for s in body.decode().splitlines() if '| 10400033 /' in s]
if not(blob==queue['sha'] and len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved' and rows[0].split('|')[9].strip()=='1/5'):raise RuntimeError('Literal queue gate failed')
(F/'FRESH_LITERAL_GATE.json').write_text(json.dumps({'UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'PR':pr,'literal_status':'claimed_solved','original_budget':'1/5','whole_QUEUE_sha256':sha(body),'QUEUE_blob_SHA1':blob,'scientific_source_read_before_gate':False},indent=2)+'\n')
entries=api('contents/'+PREFIX+'?ref='+HEAD)
if not isinstance(entries,list):raise RuntimeError('Target attempt listing unavailable')
kept=[]
# Read original proof inputs before historical review opinions.
first=['CANDIDATE.md','source_record.json','status.json','turns.jsonl']
selected=[p for p in entries if p['type']=='file' and (p['name'] in first or (p['name'].endswith('.py') and 'review' not in p['name'].lower() and 'independent' not in p['name'].lower()))]
selected.sort(key=lambda p:(first.index(p['name']) if p['name'] in first else len(first),p['name']))
for e in selected:
    j=api('contents/'+e['path']+'?ref='+HEAD);b=base64.b64decode(j['content']);actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    if not(j['encoding']=='base64' and actual==j['sha']==e['sha'] and len(b)==j['size']):raise RuntimeError('Original blob mismatch')
    p=F/e['name'];p.open('xb').write(b);kept.append({'original_path':e['path'],'retained_path':e['name'],'bytes':len(b),'sha256':sha(b),'git_blob_SHA1':actual,'git_mode_not_yet_authenticated':True})
required={p['retained_path'] for p in kept}
if not set(first)<=required:raise RuntimeError('Required original bodies missing')
manifest={'UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_controller_pid':os.getpid(),'PR':66,'head':HEAD,'files':kept,'initial_input_projection_only':True,'full_tree_domain_mode_custody_pending_separate_agent':True,'historical_reviews_read':False,'science_executed':False,'native_Git_PR_or_publication_mutations':False}
(F/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
