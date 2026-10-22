from pathlib import Path
import json, subprocess, concurrent.futures, base64, hashlib, datetime
ROOT=Path(__file__).resolve().parent
META=json.load(open(ROOT.parents[1]/'PR_OUTCOME_METADATA.json'))['data']['repository']
fields=[]
for n in range(1200,1251):
 fields.append(f'p{n}:pullRequest(number:{n}){{number state isDraft headRefOid updatedAt comments(first:100){{totalCount pageInfo{{hasNextPage endCursor}} nodes{{id body createdAt updatedAt url author{{login}}}}}} reviews(first:100){{totalCount pageInfo{{hasNextPage endCursor}} nodes{{id body state submittedAt url author{{login}}}}}}}}')
q='query {repository(owner:"AlecKriebel",name:"Math"){'+''.join(fields)+'}}'
p=subprocess.run(['gh','api','graphql','-f','query='+q],capture_output=True,text=True,check=True)
(ROOT/'latest_status_comments_reviews.json').write_text(p.stdout)
latest=json.loads(p.stdout)['data']['repository']
jobs=[]
for n in range(1200,1251):
 pr=META[f'p{n}']
 d=ROOT/f'pr_{n}'
 d.mkdir(exist_ok=True)
 (d/'BODY.md').write_text(pr['body'])
 for f in pr['files']['nodes']:
  if f['path'].endswith('/ACCEPTANCE.json') or f['path'].endswith('/README.md'):
   jobs.append((n,pr['headRefOid'],f['path']))
def work(job):
 n,head,path=job
 endpoint=f'repos/AlecKriebel/Math/contents/{path}?ref={head}'
 p=subprocess.run(['gh','api',endpoint],capture_output=True,text=True)
 if p.returncode:
  return {'pr':n,'path':path,'error':p.stderr,'code':p.returncode}
 obj=json.loads(p.stdout)
 content=base64.b64decode(obj['content'])
 d=ROOT/f'pr_{n}'
 (d/Path(path).name).write_bytes(content)
 (d/(Path(path).name+'.github.json')).write_text(json.dumps({k:v for k,v in obj.items() if k!='content'},indent=2)+'\n')
 return {'pr':n,'path':path,'ref':head,'github_blob_sha':obj['sha'],'sha256':hashlib.sha256(content).hexdigest(),'size':len(content)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 records=list(ex.map(work,jobs))
(ROOT/'immutable_file_receipts.json').write_text(json.dumps({'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':records},indent=2)+'\n')
print(json.dumps({'retrieved_files':len(records),'errors':[x for x in records if 'error' in x],'changed_heads':[n for n in range(1200,1251) if latest[f'p{n}']['headRefOid']!=META[f'p{n}']['headRefOid']],'comments':{n:latest[f'p{n}']['comments']['totalCount'] for n in range(1200,1251) if latest[f'p{n}']['comments']['totalCount']},'reviews':{n:latest[f'p{n}']['reviews']['totalCount'] for n in range(1200,1251) if latest[f'p{n}']['reviews']['totalCount']}},indent=2))
