#!/usr/bin/env python3
"""Read-only PR/head/queue/current-main identity binding using GitHub GETs."""
from pathlib import Path
import base64,datetime,hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parents[1]
HEAD='a35667b1bb0bafed69916709997a4684223ecc93'
def need(ok,label):
 if not ok:raise RuntimeError(label)
def command(*a):return subprocess.check_output(a,text=True)
def main():
 phase=sys.argv[1]
 raw=command('gh','pr','view','908','--repo','AlecKriebel/Math','--json','number,url,title,state,isDraft,headRefOid,headRefName,baseRefName,body')
 (HERE/'private_sources'/f'live_pr_{phase}.json').write_text(raw)
 pr=json.loads(raw)
 need(pr['state']=='OPEN' and pr['isDraft'] is True and pr['headRefOid']==HEAD and pr['baseRefName']=='main','PR gate')
 body=pr['body'].encode();corrected=(AUDIT/'PR_DESCRIPTION_CORRECTED.md').read_bytes()
 need(body==corrected,'exact corrected live body')
 refraw=command('gh','api','repos/AlecKriebel/Math/git/ref/heads/main')
 (HERE/'private_sources'/f'main_ref_{phase}.json').write_text(refraw)
 mainsha=json.loads(refraw)['object']['sha']
 craw=command('gh','api','--method','GET','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/catalog.json','-f','ref='+mainsha)
 (HERE/'private_sources'/f'catalog_api_{phase}.json').write_text(craw)
 cm=json.loads(craw)
 if cm['encoding']=='base64':content=base64.b64decode(cm['content'])
 else:
  content=command('gh','api','--method','GET','-H','Accept: application/vnd.github.raw+json','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/catalog.json','-f','ref='+mainsha).encode()
 (HERE/'private_sources'/f'catalog_body_{phase}.json').write_bytes(content)
 target=[x for x in json.loads(content) if str(x['id'])=='30006191']
 need(len(target)==1,'unique target')
 t=target[0];expected=json.loads((AUDIT/'TARGET_IDENTITY_PREFLIGHT.json').read_text())
 need(t['present'] is True and t['holds']==[] and t['review_hash']==expected['review_hash'] and t['statement_hash']==expected['statement_hash'],'current-main source gate')
 queue=command('git','show',HEAD+':unsolved_math_prioritization/QUEUE.md')
 rows=[r for r in queue.splitlines() if r.startswith('|') and len(r.split('|'))>9 and r.split('|')[2].strip().split(' / ')[0]=='30006191']
 need(len(rows)==1,'head queue unique');cells=[x.strip() for x in rows[0].split('|')]
 need(cells[8]=='claimed_solved' and cells[9]=='1/5','exact status/count')
 source=json.loads((AUDIT/'source_record_private.txt').read_text())
 need(source['review_hash']==t['review_hash'],'raw source identity')
 statement=source['problem']['clean_statement']
 need(hashlib.sha256(statement.encode()).hexdigest()==t['statement_hash'],'raw statement fingerprint')
 result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':phase,
  'pr':{k:v for k,v in pr.items() if k!='body'},'live_body_sha256':hashlib.sha256(body).hexdigest(),
  'live_body_exact_current_corrected_text':True,'immutable_head_queue_status':cells[8],
  'immutable_head_queue_turns':cells[9],'current_main_sha':mainsha,
  'current_main_catalog_sha256':hashlib.sha256(content).hexdigest(),
  'source_present':t['present'],'holds':t['holds'],'review_hash':t['review_hash'],'statement_hash':t['statement_hash'],
  'mutations_performed':False}
 (HERE/f'LIVE_{phase}_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
