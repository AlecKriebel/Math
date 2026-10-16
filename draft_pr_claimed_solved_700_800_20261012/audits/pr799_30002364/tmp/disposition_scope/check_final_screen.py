"""Independent read-only final 101-number metadata and own QUEUE-row check.

No scientific candidate file is read. No production API mutation is issued.
"""
from pathlib import Path
import collections,datetime,hashlib,json,subprocess
W=Path(__file__).resolve().parent;T=W.parent;R=Path('/Users/alec/Documents/Math')
QUEUE='unsolved_math_prioritization/QUEUE.md';FIELDS='number title state isDraft merged headRefOid headRefName closedAt url mergeCommit { oid }'
MERGED=[718,742,764,765,778,781,786,788,789];CLOSED=[734,767,799]
def need(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def gql(q):
 need(q.startswith('query '),'Queries only')
 r=subprocess.run(['gh','api','graphql','--input','-'],input=json.dumps({'query':q}),text=True,capture_output=True,check=True)
 d=json.loads(r.stdout);need(not d.get('errors'),'GraphQL read errors');return d['data']['repository']
def capture():
 out=[];records=[]
 for start in range(700,801,25):
  ns=list(range(start,min(start+25,801)));q='query { repository(owner:"AlecKriebel",name:"Math") { '+' '.join(f'p{n}:pullRequest(number:{n}){{{FIELDS}}}' for n in ns)+' } }'
  d=gql(q);need(set(d)=={'p'+str(n) for n in ns},'Direct alias coverage');need(all(d['p'+str(n)] is not None for n in ns),'Existing PR numbers');out.extend(d['p'+str(n)] for n in ns);records.append({'query':q,'response':d})
 need([r['number'] for r in out]==list(range(700,801)),'Exactly every integer number');return out,records

def main():
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();root=json.loads((T/'root-receipts/ROOT_FINAL_RECONCILIATION.json').read_text())
 need(root['result']=='PASS' and [r['number'] for r in root['complete_rows']]==list(range(700,801)),'Root final certificate scope')
 before,braw=capture();opened=[r for r in before if r['state']=='OPEN' and r['isDraft']];old={r['number']:r for r in root['complete_rows']}
 bindings={};binding_records=[]
 for start in range(0,len(opened),20):
  group=opened[start:start+20];q='query { repository(owner:"AlecKriebel",name:"Math") { '+' '.join(f'q{r["number"]}:object(expression:"{r["headRefOid"]}:{QUEUE}"){{ ... on Blob {{ oid byteSize }} }}' for r in group)+' } }'
  d=gql(q);need(set(d)=={'q'+str(r['number']) for r in group},'All exact-head queue bindings');bindings.update({r['number']:d['q'+str(r['number'])] for r in group});binding_records.append({'query':q,'response':d})
 statuses=collections.Counter();own_rows=[]
 for r in before:
  n=r['number'];expect=old[n];need(all(expect.get(k)==v for k,v in r.items()),'Current metadata differs from root final record')
  if r['state']!='OPEN' or not r['isDraft']:
   need(expect['queue_inspected'] is False,'Closed/merged mathematical source not screened');continue
  need(expect['queue_inspected'] is True,'Missing own-row screen');problem=expect['problem']
  p=subprocess.run(['git','cat-file','blob',r['headRefOid']+':'+QUEUE],cwd=R,capture_output=True,check=True)
  raw=p.stdout;ident=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
  need(bindings[n]['oid']==ident and bindings[n]['byteSize']==len(raw),'Fresh authenticated queue blob identity')
  rows=[l.decode() for l in raw.splitlines() if l.startswith(b'| ') and (' '+problem+' / ').encode() in l];need(len(rows)==1,'Unique own queue row')
  cells=rows[0].split('|');need(len(cells)==14,'12-column QUEUE schema');status=cells[8].strip();turns=cells[9].strip()
  need(rows[0]==expect['own_row'] and status==expect['queue_status'] and turns==expect['turns'],'Own status/turn row differs')
  need(sha(raw)==expect['source']['blob_sha256'] and ident==expect['source']['blob_oid'],'Root immutable source pins')
  need(status!='claimed_solved' and expect['decision']=='skip_without_processing','Eligible PR remains')
  statuses[status]+=1;own_rows.append({'number':n,'head':r['headRefOid'],'problem':problem,'status':status,'turns':turns,'queue_blob_oid':ident,'queue_blob_sha256':sha(raw),'own_row_sha256':sha(rows[0].encode())})
 after,araw=capture();need(before==after,'Metadata changed across complete final captures')
 need([r['number'] for r in before if r['merged']]==MERGED,'Nine merged outcomes')
 need([r['number'] for r in before if r['state']=='CLOSED' and not r['merged']]==CLOSED,'Three closed-unmerged outcomes')
 need(len(opened)==89 and dict(statuses)=={'unsolved':80,'already_solved':9},'Exactly 89 excluded drafts')
 need(root['remaining_exact_claimed_solved']==[] and root['open_draft_status_counts']==dict(statuses),'Root final summary agrees')
 (W/'FINAL_METADATA_CAPTURES.json').write_text(json.dumps({'started_utc':started,'before':braw,'queue_bindings':binding_records,'after':araw},indent=2)+'\n')
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'started_utc':started,'result':'PASS','all_integer_numbers_queried_twice':101,'stable_before_after':True,'fresh_exact_head_queue_bindings':89,'immutable_source_blobs_replayed':89,'source_read_method':'read-only git cat-file; no object/ref/index/checkout writes','merged':MERGED,'closed_unmerged':CLOSED,'excluded_open_drafts':dict(statuses),'remaining_exact_claimed_solved':[],'only_metadata_and_own_queue_rows_read':True,'root_final_reconciliation_sha256':sha((T/'root-receipts/ROOT_FINAL_RECONCILIATION.json').read_bytes()),'capture_receipt_sha256':sha((W/'FINAL_METADATA_CAPTURES.json').read_bytes()),'own_rows':own_rows,'point_in_time_only':True}
 (W/'FINAL_SCREEN_READBACK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='own_rows'}))
if __name__=='__main__':main()
