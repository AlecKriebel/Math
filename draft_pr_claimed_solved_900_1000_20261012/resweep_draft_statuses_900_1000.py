#!/usr/bin/env python3
"""Read-only final scope sweep: PR metadata and exact immutable-head QUEUE status.

No proof, source intake, artifact, comment, merge, close, or publication action.
Run after the ascending work, and retain the receipt before goal completion.
A second metadata snapshot detects head/draft/state/base changes during the scan.
"""
import argparse,concurrent.futures,hashlib,json,re,subprocess,os
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
P=Path(__file__).resolve().parent;ROOT=P.parent
FIELDS='number state isDraft headRefOid headRefName baseRefName url'
def need(ok,label):
 if not ok:raise RuntimeError(label)
def run(args):return subprocess.run(args,cwd=ROOT,check=True,capture_output=True,text=True,timeout=60).stdout
def strict_json(raw):
 def pairs(items):
  result={}
  for k,v in items:need(k not in result,'Duplicate JSON key');result[k]=v
  return result
 def bad(value):raise RuntimeError('Nonfinite JSON constant')
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)
def graphql(query,variables=None):
 args=['gh','api','graphql','-f','query='+query]
 for k,v in (variables or {}).items():
  need(type(v) in (str,int),'GraphQL variable type');args+=['-F' if type(v) is int else '-f',k+'='+str(v)]
 reply=strict_json(run(args));need(type(reply) is dict and not reply.get('errors'),'GraphQL read incomplete');return reply['data']['repository']
def safe(path):
 return type(path) is str and bool(path) and '\\' not in path and '\0' not in path and not PurePosixPath(path).is_absolute() and PurePosixPath(path).as_posix()==path and all(x not in ('','.','..') for x in path.split('/'))
def metadata():
 fields=' '.join(f'p{n}:pullRequest(number:{n}){{{FIELDS}}}' for n in range(900,1001));query='query { repository(owner:"AlecKriebel",name:"Math") {'+fields+'} }';repo=graphql(query);need(set(repo)=={f'p{n}' for n in range(900,1001)},'Metadata range differs');return {n:repo[f'p{n}'] for n in range(900,1001)}
def changed_paths(pr):
 need(type(pr.get('number')) is int and 900<=pr['number']<=1000,'Changed-head PR number')
 query='query($number:Int!,$cursor:String){repository(owner:"AlecKriebel",name:"Math"){pullRequest(number:$number){'+FIELDS+' changedFiles files(first:100,after:$cursor){nodes{path}pageInfo{hasNextPage endCursor}}}}}'
 paths=[];cursor=None;cursors=set();declared=None
 for page in range(30):
  variables={'number':pr['number']}
  if cursor is not None:variables['cursor']=cursor
  node=graphql(query,variables).get('pullRequest')
  need(type(node) is dict and all(type(node.get(k)) is type(pr.get(k)) and node.get(k)==pr.get(k) for k in FIELDS.split()),'Changed-file page PR metadata drift')
  count=node.get('changedFiles');need(type(count) is int and 1<=count<=3000 and (declared is None or count==declared),'Bounded stable complete changed-file count');declared=count
  conn=node.get('files');need(type(conn) is dict and type(conn.get('nodes')) is list and 1<=len(conn['nodes'])<=100,'Changed-file connection/count')
  for item in conn['nodes']:
   need(type(item) is dict and set(item)=={'path'} and safe(item['path']),'Canonical changed filename required');paths.append(item['path'])
  need(len(paths)<=declared and len(paths)==len(set(paths)),'Duplicate or excess changed filenames')
  info=conn.get('pageInfo');need(type(info) is dict and type(info.get('hasNextPage')) is bool,'Pagination schema')
  if not info['hasNextPage']:
   need(len(paths)==declared,'Incomplete changed-file list');return paths
  cursor=info.get('endCursor');need(type(cursor) is str and bool(cursor) and cursor not in cursors,'Missing or repeated cursor');cursors.add(cursor)
 raise RuntimeError('Changed filename page bound exceeded')
def immutable_queue(head):
 need(type(head) is str and re.fullmatch('[0-9a-f]{40}',head) is not None,'Immutable queue commit')
 query='query($expr:String!){repository(owner:"AlecKriebel",name:"Math"){object(expression:$expr){__typename ...on Blob{text isBinary byteSize oid}}}}'
 node=graphql(query,{'expr':head+':unsolved_math_prioritization/QUEUE.md'}).get('object')
 need(type(node) is dict and node.get('__typename')=='Blob' and node.get('isBinary') is False and type(node.get('text')) is str,'Immutable queue text blob')
 raw=node['text'].encode();need(type(node.get('byteSize')) is int and len(raw)==node['byteSize'] and 0<len(raw)<=2*1024**2,'Immutable queue bounded byte size')
 oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();need(node.get('oid')==oid,'Immutable queue Git blob authentication');return node['text']
def target_status(queue,key):
 need(type(key) is str and re.fullmatch('[0-9]+',key) is not None,'Unexpected target ID');rows=[]
 for line in queue.splitlines():
  cells=line.split('|')
  if line.startswith('|') and len(cells)>9 and cells[2].strip().split(' / ',1)[0]==key:rows.append((line,cells))
 need(len(rows)==1,'Ambiguous/missing target QUEUE row '+key);line,cells=rows[0];return {'status':cells[8].strip(),'turns':cells[9].strip(),'queue_row_sha256':hashlib.sha256(line.encode()).hexdigest()}
def current_identity(pr,initial):
 # Reuse the original identity only for the exact same immutable head.
 # Changed heads require current filename metadata, never mathematical bodies.
 if pr['headRefOid']==initial['headRefOid']:
  keys=[str(x['id']) for x in initial['entries']]
  method='initial_identity_at_exact_unchanged_head'
 else:
  paths=changed_paths(pr)
  keys=sorted({match.group(1) for path in paths if (match:=re.fullmatch(r'unsolved_math_prioritization/attempts/([0-9]+)/.+',path))})
  method='complete_GraphQL_filename_metadata_after_head_change'
 if len(keys)!=1 or re.fullmatch('[0-9]+',keys[0]) is None:
  return {'identity_method':method,'identity_reconciled':False,'candidate_problem_ids':keys}
 return {'identity_method':method,'identity_reconciled':True,'problem_id':keys[0]}
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--receipt-name',required=True);args=ap.parse_args();need(re.fullmatch('[A-Za-z0-9_.-]+[.]json',args.receipt_name) is not None,'Receipt must be a simple JSON filename');out=P/args.receipt_name;need(not out.exists(),'Receipt exists; preserve prior snapshot and select a new name')
 started=datetime.now(timezone.utc).isoformat();old={r['number']:r for r in json.loads((P/'inventory.json').read_text())};need(set(range(900,1001))<=set(old),'Initial metadata inventory incomplete');first=metadata();rows=[];jobs=[]
 for number,pr in first.items():
  need(pr is not None and pr['number']==number,'Missing numbered PR metadata');base={'pr':number,'original_metadata_head':pr['headRefOid'],'state':pr['state'],'isDraft':pr['isDraft'],'baseRefName':pr['baseRefName'],'math_or_source_or_artifact_read':False,'remote_mutation':False}
  if pr['state']!='OPEN' or pr['isDraft'] is not True:base['action']='SKIP_NOT_OPEN_DRAFT';rows.append(base);continue
  jobs.append((base,pr,old[number]))
 def inspect(job):
  record,pr,initial=job
  try:
   record.update(current_identity(pr,initial))
   if not record['identity_reconciled']:record['action']='UNRESOLVED_IDENTITY';return record
   key=record['problem_id'];head=record['original_metadata_head'];queue=immutable_queue(head);record.update(**target_status(queue,key));record['action']='ELIGIBLE_REQUIRES_PROCESSING' if record['status']=='claimed_solved' else 'SKIP_STATUS_ONLY'
  except Exception as error:record.update(action='UNRESOLVED_READ',read_error=str(error),completion_scope_clear=False)
  return record
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows.extend(pool.map(inspect,jobs))
 second=metadata();unstable=[]
 for number in first:
  if first[number]!=second[number]:unstable.append(number)
 rows.sort(key=lambda r:r['pr']);eligible=[r for r in rows if r['action']=='ELIGIBLE_REQUIRES_PROCESSING'];unresolved=[r for r in rows if r['action'].startswith('UNRESOLVED_')];result={'started_utc':started,'completed_utc':datetime.now(timezone.utc).isoformat(),'scope':'All numbered PR900 through1000 inclusive; metadata and authenticated immutable-head QUEUE status only.','ordering':'ascending','pr_count':len(rows),'actions':dict(Counter(r['action'] for r in rows)),'all_non_claimed_solved_skipped_without_math_processing':True,'metadata_stable_across_scan':not unstable,'changed_during_scan':unstable,'eligible_remaining':eligible,'unresolved_identities':unresolved,'completion_scope_clear':not unstable and not eligible and not unresolved,'rows':rows,'source_math_artifact_reads_or_remote_mutations':False,'transport':'Read-only GraphQL. Complete bounded changed-filename pagination and Git-blob/size authentication of immutable QUEUE; no REST, checkout/index/HEAD/object/cache writes.'}
 with out.open('x') as f:f.write(json.dumps(result,indent=2)+'\n');f.flush();os.fsync(f.fileno())
 print(json.dumps({k:result[k] for k in ['completed_utc','pr_count','actions','metadata_stable_across_scan','eligible_remaining','unresolved_identities','completion_scope_clear']},indent=2))
if __name__=='__main__':main()
