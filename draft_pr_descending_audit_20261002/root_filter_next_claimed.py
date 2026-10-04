"""Status-only descending eligibility filter. No mathematical review of excluded PRs."""
from pathlib import Path
import base64,datetime,hashlib,json,re,subprocess
P=Path(__file__).resolve().parent;R=P.parent
def sha(b):return hashlib.sha256(b).hexdigest()
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f')
D=P/('private_status_filter_'+stamp);D.mkdir(exist_ok=False)
captures=[]
def run(args):
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(args,cwd=R,capture_output=True);i=len(captures)
 (D/f'{i:03}.stdout').write_bytes(p.stdout);(D/f'{i:03}.stderr').write_bytes(p.stderr)
 e={'argv':args,'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),'stderr_bytes':len(p.stderr),'stderr_sha256':sha(p.stderr)};captures.append(e);(D/f'{i:03}.receipt.json').write_text(json.dumps(e,indent=2)+'\n');assert p.returncode==0,(args,p.returncode,p.stderr.decode(errors='replace'));return p.stdout
inv=json.loads((P/'inventory.json').read_bytes());initial={x['number']:x for x in inv['items']};cursor=364
if (P/'STATUS_FILTER_LEDGER.json').exists():
 old=json.loads((P/'STATUS_FILTER_LEDGER.json').read_bytes());entries=old['entries'];cursor=old.get('next_eligible',{}).get('number',cursor) if old.get('next_eligible') else cursor
else:entries=[]
live=json.loads(run(['gh','pr','list','--state','open','--limit','500','--json','number,title,isDraft,headRefOid,headRefName,baseRefName,url']))
remaining=sorted([x for x in live if x['number'] in initial and x['number']<cursor and x['number']!=8 and x['isDraft']],key=lambda x:-x['number'])
eligible=None
for item in remaining:
 n=item['number'];head=item['headRefOid']
 branch_ids=set(re.findall(r'(?<!\d)\d+(?!\d)',item['headRefName']))
 first_title_id=re.search(r'\d+',item['title'])
 if len(branch_ids)==1:problem=next(iter(branch_ids))
 elif first_title_id and (not branch_ids or first_title_id.group() in branch_ids):problem=first_title_id.group()
 else:raise AssertionError(('Cannot authenticate one primary target ID from branch/title',n,branch_ids,item['title']))
 obj=json.loads(run(['gh','api','-X','GET','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md','-f','ref='+head]));assert obj['encoding']=='base64' and obj['type']=='file'
 b=base64.b64decode(obj['content']);assert len(b)==obj['size'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==obj['sha']
 rows=[(i+1,x) for i,x in enumerate(b.decode().splitlines()) if len(x.split('|'))>11 and x.split('|')[2].strip().split(' / ')[0]==problem];assert len(rows)==1,(n,problem,len(rows))
 line,row=rows[0];status=row.split('|')[8].strip();turns=row.split('|')[9].strip()
 pr=json.loads(run(['gh','pr','view',str(n),'--json','state,isDraft,headRefOid']));assert pr['state']=='OPEN' and pr['isDraft'] and pr['headRefOid']==head,'Head/state changed during status-only filter; repeat only reads.'
 rec={'number':n,'title':item['title'],'problem_id':problem,'head':head,'queue_git_blob_sha':obj['sha'],'queue_bytes':len(b),'queue_sha256':sha(b),'queue_physical_line':line,'submitted_status':status,'submitted_turns':turns,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'decision':'eligible_claimed_solved' if status=='claimed_solved' else 'skipped_status_only_no_processing','capture_directory':str(D)}
 entries.append(rec);print(json.dumps(rec),flush=True)
 x=initial[n];x.update(submitted_status=status,eligibility_checked_head=head,eligibility_checked_utc=rec['checked_utc'])
 if status!='claimed_solved':x.update(disposition='skipped_excluded_status_without_processing')
 else:eligible={**item,'problem_id':problem,'submitted_status':status,'submitted_turns':turns};break
ledger={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'NEXT_ELIGIBLE_FOUND' if eligible else 'NO_MORE_INITIAL_LOWER_DRAFTS_FOUND','scope':'Only submitted QUEUE.md status exactly claimed_solved; other statuses skipped without review, audit, repair, merge, close, comment or paper. Initial inventory and descending cursor; PR8 excluded.','entries':entries,'next_eligible':eligible,'native_capture_directory':str(D),'native_capture_count':len(captures),'tracker_364_login_pending':364 in inv.get('claimed_solved_tracker_pending_by_descending',[])}
(P/'STATUS_FILTER_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n');(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write(f"\n{ledger['utc']}: Submitted-status-only descending filter inspected {len(remaining) if eligible is None else len([e for e in entries if e['capture_directory']==str(D)])} current draft statuses until the next eligible claim. Next eligible: {eligible['number'] if eligible else 'none in initial lower inventory'}. No excluded-status mathematical work or PR mutation occurred. PR364 tracker pending: {364 in inv.get('claimed_solved_tracker_pending_by_descending',[])}; total eligible goal percentage remains unauthenticated.\n")
print(json.dumps({'status':ledger['status'],'next_eligible':eligible,'status_only_entries':len(entries)},indent=2))
