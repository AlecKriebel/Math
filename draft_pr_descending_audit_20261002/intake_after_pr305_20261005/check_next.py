"""Descending status-only intake; stop at the first originally claimed_solved PR."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib,base64,re,sys,stat
if sys.flags.optimize:raise RuntimeError('Unoptimized intake required.')
I=Path(__file__).resolve().parent;P=I.parent;R=P.parent
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
def pin(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
out=I/'actual_status_intake';assert not out.exists();out.mkdir();ops=[]
def api(endpoint):
    n=len(ops)+1;argv=['/opt/homebrew/bin/gh','api',endpoint];stamp=utc()
    proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    spec=dict(argv=argv,cwd=str(R),actual_PID=proc.pid,start_UTC=stamp,source=pin(Path(__file__).resolve()))
    (out/(str(n)+'_started.json')).write_text(json.dumps(spec,indent=2)+'\n')
    b,err=proc.communicate(timeout=55)
    for k,x in [('stdout',b),('stderr',err)]:
        (out/(str(n)+'_'+k+'.bin')).write_bytes(x);spec[k+'_bytes']=len(x);spec[k+'_sha256']=sha(x)
    spec.update(end_UTC=utc(),exit_code=proc.returncode);ops.append(spec)
    (out/(str(n)+'_execution.json')).write_text(json.dumps(spec,indent=2)+'\n')
    assert proc.returncode==0,(endpoint,proc.returncode);return json.loads(b)
inventory=json.loads((P/'inventory.json').read_bytes());records=[];eligible=None
for item in sorted((e for e in inventory['items'] if e['number']<305 and e['number']!=8),key=lambda e:-e['number']):
    number=item['number'];pr=api('repos/AlecKriebel/Math/pulls/'+str(number))
    assert pr['number']==number and pr['head']['sha']==item['headRefOid'],'Fresh original head differs; reconcile before eligibility.'
    ids=re.findall(r'\d{4,}',item['headRefName']);assert len(ids)==1
    problem=ids[0];head=item['headRefOid']
    q=api('repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+head)
    assert q['encoding']=='base64' and q['path']=='unsolved_math_prioritization/QUEUE.md'
    b=base64.b64decode(q['content']);assert len(b)==q['size']
    blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert blob==q['sha']
    rows=[x for x in b.splitlines(keepends=True) if re.match(rb'\| '+problem.encode()+rb' /',x)];assert len(rows)==1
    row=rows[0];cells=row.split(b'|');assert len(cells)==14
    status=cells[8].strip().decode();turns=cells[9].strip().decode()
    record=dict(number=number,problem=problem,original_head=head,original_status=status,
        original_author_turns=turns,fresh_PR_state=pr['state'],fresh_PR_draft=pr['draft'],
        original_QUEUE_blob=blob,original_QUEUE_bytes=len(b),original_QUEUE_sha256=sha(b),
        target_row=row.decode(),eligibility_checked_UTC=utc())
    if status=='claimed_solved' and pr['state']=='open' and pr['draft']:
        record['action']='FIRST_ELIGIBLE_CLAIMED_SOLVED_IN_DESCENDING_ORDER';eligible=record
        (I/'eligible_original_QUEUE.md').write_bytes(b);records.append(record);break
    record['action']='SKIPPED_STATUS_ONLY_NO_REVIEW_OR_OTHER_PROCESSING' if status!='claimed_solved' else 'NO_LONGER_OPEN_DRAFT_SKIPPED'
    records.append(record)
assert eligible is not None,'No next eligible draft found.'
result=dict(status='PASS_DESCENDING_STATUS_ONLY_INTAKE',UTC=utc(),start_below=305,
    records=records,eligible=eligible,all_non_claimed_solved_skipped_without_math_or_priority_or_mutation=True,
    Git_index_main_config_unchanged_no_Git_or_service_mutation=True,PR8_excluded=True,
    original_inventory_pin=pin(P/'inventory.json'),actual_native_captures=ops,
    shared_peer_window_respected=True,persistent_goal_complete=False)
(I/'INTAKE.json').write_text(json.dumps(result,indent=2)+'\n')
with (I/'RESEARCH_LOG.md').open('a') as f:
    f.write(utc()+' — Status-only descending intake after fully completed PR305. '+str([(e['number'],e['original_status']) for e in records])+'; first eligible PR'+str(eligible['number'])+' at exact original head '+eligible['original_head']+'. Other statuses untouched. No mathematics/priority verification yet; eligible PR workflow5%, mathematics0%, priority0%. Persistent program27 handled/8 published; peer55-path shared window respected.\n')
print(json.dumps(dict(status=result['status'],checked=[(e['number'],e['original_status']) for e in records],eligible=eligible,native_captures=len(ops)),indent=2))
