#!/usr/bin/env python3
"""Read-only final scope sweep: PR metadata and exact immutable-head QUEUE status.

No proof, source intake, artifact, comment, merge, close, or publication action.
Run after the ascending work, and retain the receipt before goal completion.
A second metadata snapshot detects head/draft/state/base changes during the scan.
"""
import argparse,concurrent.futures,hashlib,json,re,subprocess
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent
FIELDS='number state isDraft headRefOid headRefName baseRefName url'
def need(ok,label):
 if not ok:raise RuntimeError(label)
def run(args):return subprocess.run(args,cwd=ROOT,check=True,capture_output=True,text=True).stdout
def metadata():
 fields=' '.join(f'p{n}:pullRequest(number:{n}){{{FIELDS}}}' for n in range(900,1001));query='query { repository(owner:"AlecKriebel",name:"Math") {'+fields+'} }';response=json.loads(run(['gh','api','graphql','-f','query='+query]));need(not response.get('errors'),'Incomplete GraphQL metadata');repo=response['data']['repository'];need(set(repo)=={f'p{n}' for n in range(900,1001)},'Metadata range differs');return {n:repo[f'p{n}'] for n in range(900,1001)}
def target_status(queue,key):
 need(type(key) is str and re.fullmatch('[0-9]+',key) is not None,'Unexpected target ID');rows=[]
 for line in queue.splitlines():
  cells=line.split('|')
  if line.startswith('|') and len(cells)>9 and cells[2].strip().split(' / ',1)[0]==key:rows.append((line,cells))
 need(len(rows)==1,'Ambiguous/missing target QUEUE row '+key);line,cells=rows[0];return {'status':cells[8].strip(),'turns':cells[9].strip(),'queue_row_sha256':hashlib.sha256(line.encode()).hexdigest()}
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--receipt-name',required=True);args=ap.parse_args();need(re.fullmatch('[A-Za-z0-9_.-]+[.]json',args.receipt_name) is not None,'Receipt must be a simple JSON filename');out=P/args.receipt_name;need(not out.exists(),'Receipt exists; preserve prior snapshot and select a new name')
 started=datetime.now(timezone.utc).isoformat();old={r['number']:r for r in json.loads((P/'inventory.json').read_text())};need(set(range(900,1001))<=set(old),'Initial metadata inventory incomplete');first=metadata();rows=[];jobs=[]
 for number,pr in first.items():
  need(pr is not None and pr['number']==number,'Missing numbered PR metadata');base={'pr':number,'original_metadata_head':pr['headRefOid'],'state':pr['state'],'isDraft':pr['isDraft'],'baseRefName':pr['baseRefName'],'math_or_source_or_artifact_read':False,'remote_mutation':False}
  if pr['state']!='OPEN' or pr['isDraft'] is not True:base['action']='SKIP_NOT_OPEN_DRAFT';rows.append(base);continue
  keys=[str(x['id']) for x in old[number]['entries']];need(len(keys)==1,'Multiple target metadata needs narrow reconciliation');jobs.append((base,keys[0]))
 def inspect(job):
  record,key=job;head=record['original_metadata_head'];queue=run(['gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+head,'-H','Accept: application/vnd.github.raw+json']);record.update(problem_id=key,**target_status(queue,key));record['action']='ELIGIBLE_REQUIRES_PROCESSING' if record['status']=='claimed_solved' else 'SKIP_STATUS_ONLY';return record
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows.extend(pool.map(inspect,jobs))
 second=metadata();unstable=[]
 for number in first:
  if first[number]!=second[number]:unstable.append(number)
 rows.sort(key=lambda r:r['pr']);eligible=[r for r in rows if r['action']=='ELIGIBLE_REQUIRES_PROCESSING'];result={'started_utc':started,'completed_utc':datetime.now(timezone.utc).isoformat(),'scope':'All numbered PR900 through1000 inclusive; metadata and immutable-head QUEUE status only.','ordering':'ascending','pr_count':len(rows),'actions':dict(Counter(r['action'] for r in rows)),'all_non_claimed_solved_skipped_without_math_processing':True,'metadata_stable_across_scan':not unstable,'changed_during_scan':unstable,'eligible_remaining':eligible,'completion_scope_clear':not unstable and not eligible,'rows':rows,'source_math_artifact_reads_or_remote_mutations':False};out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['completed_utc','pr_count','actions','metadata_stable_across_scan','eligible_remaining','completion_scope_clear']},indent=2))
if __name__=='__main__':main()
