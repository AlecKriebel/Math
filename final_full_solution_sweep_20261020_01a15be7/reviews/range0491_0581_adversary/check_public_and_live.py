from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,os,re,subprocess,sys,urllib.request,zipfile,io,time
sys.dont_write_bytecode=True
os.environ.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
Q=Path(__file__).resolve().parent;R=Q.parent.parent;REPO=R.parent
now=lambda:dt.datetime.now(dt.timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(n,d):
 p=Q/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(d if isinstance(d,bytes) else (json.dumps(d,indent=2)+'\n').encode())
def cmd(args):return subprocess.run(args,cwd=REPO,capture_output=True,check=True).stdout
def get(url):
 for attempt in range(4):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent-result-coverage-review/1.0'}),timeout=60) as f:return f.read(),dict(status=f.status,final_url=f.url,at=now())
  except Exception:
   if attempt==3:raise
   time.sleep(1)
query='query{repository(owner:"AlecKriebel",name:"Math"){'+''.join(f'p{n}:pullRequest(number:{n}){{number title state isDraft headRefOid baseRefOid updatedAt mergedAt mergeCommit{{oid}} body}}' for n in range(491,582))+'}}'
live=json.loads(cmd(['gh','api','graphql','-f','query='+query]));assert 'errors' not in live;save('private/prs_live.json',live);old={p['number']:p for p in json.loads((Q/'inputs/rest_inventory.json').read_text())['pull_requests']};changes=[]
for n in range(491,582):
 p=live['data']['repository']['p'+str(n)];assert p['number']==n
 diff={k:dict(old=old[n].get(k),live=p.get(k)) for k in p if p.get(k)!=old[n].get(k)}
 if diff:changes.append(dict(pr=n,differences=diff))
save('live_metadata_differences.json',changes);save('live_metadata_receipt.json',dict(at=now(),count=91,sha256=sha((Q/'private/prs_live.json').read_bytes()),changed_numbers=[x['pr'] for x in changes]))
comment=json.loads(cmd(['gh','api','repos/AlecKriebel/Math/issues/comments/6138397305']));save('private/pr0523_comment_live.json',comment);w=json.loads((Q/'inputs/PR0523_WITHDRAWAL_VERIFICATION.json').read_text());assert comment['id']==6138397305 and sha(comment['body'].encode())==w['closure_comment']['body_sha256'];p=live['data']['repository']['p523'];assert p['state']=='CLOSED' and p['mergedAt'] is None and p['headRefOid']==w['head'];cmd(['git','fetch','--no-write-fetch-head','origin',w['main']]);queue=cmd(['git','show',w['main']+':unsolved_math_prioritization/QUEUE.md']);assert sha(queue)==w['queue_sha256'];save('private/pr0523_corrected_QUEUE.md',queue);line=w['current_explicit_status']['source_line'];assert line in queue.decode().splitlines() and '| already_solved |' in line and '30004064' in line;save('withdrawal_verification.json',dict(at=now(),pr=523,live_closed_unmerged=True,exact_comment_body_sha256=sha(comment['body'].encode()),queue_commit=w['main'],queue_sha256=sha(queue),exact_current_negative_line=line,scope='Explicit administrative withdrawal only. Prior paper cited in comment remains a lead, not independently certified here.'))
params={'spreadsheetId':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','range':"'Math Puzzles'!A:AQ",'valueRenderOption':'FORMATTED_VALUE'}
ledger=json.loads(cmd(['gws','sheets','spreadsheets','values','get','--params',json.dumps(params)]));save('private/ledger_live.json',ledger);rows=ledger['values'];save('ledger_fresh_receipt.json',dict(at=now(),spreadsheet_id=params['spreadsheetId'],range=params['range'],rows=len(rows),sha256=sha((Q/'private/ledger_live.json').read_bytes()),method='Google Workspace CLI values get only'))
items=[(521,'30003571',23331080,67),(533,'30001182',23333353,78),(563,'2306072',23383961,90),(570,'30006605',23385145,95)];out=[]
for pr,problem,record,rownum in items:
 b,receipt=get('https://zenodo.org/api/records/'+str(record));d=json.loads(b);save(f'private/pr{pr:04d}/zenodo_record.json',d);doi='10.5281/zenodo.'+str(record);assert d['doi']==doi and d['state']=='done' and d['submitted'] is True;pdfs=[];archives=[];payloads=[]
 _,resolution=get('https://doi.org/'+doi);assert resolution['status']==200 and resolution['final_url']=='https://zenodo.org/records/'+str(record)
 row=rows[rownum-1];assert len(row)>=4 and problem in row[0] and row[2] in {doi,'https://doi.org/'+doi};same=[i+1 for i,v in enumerate(rows) if len(v)>2 and v[2] in {doi,'https://doi.org/'+doi}];assert same==[rownum]
 for f in d['files']:
  data,fetch=get(f['links']['self']);assert len(data)==f['size'] and 'md5:'+hashlib.md5(data).hexdigest()==f['checksum'];digest=sha(data);save(f'private/pr{pr:04d}/payload_{digest}.bin',data);e=dict(name=f['key'],bytes=len(data),sha256=digest,checksum=f['checksum'],download=fetch)
  root=json.loads((Q/f'inputs/PR{pr:04d}_PUBLICATION_LEADS.json').read_text());rf=next(x for x in next(x for x in root['records'] if x['record']==record)['files'] if x['name']==f['key']);assert rf['sha256']==digest
  if f['key'].endswith('.pdf'):pdfs.append(e)
  if f['key'].endswith('.zip'):
   z=zipfile.ZipFile(io.BytesIO(data));names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
   assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n and '\x00' not in n for n in names)
   mn=[n for n in names if n.endswith('/MANIFEST.json') and n.count('/')==1];assert len(mn)==1;prefix=mn[0].rsplit('/',1)[0]+'/';m=json.loads(z.read(mn[0]));save(f'private/pr{pr:04d}/MANIFEST.json',m)
   files=m['files'];assert isinstance(files,dict)
   for name,v in files.items():
    part=z.read(prefix+name);assert sha(part)==v['sha256'] and len(part)==v['bytes']
   assert set(names)=={mn[0]}|{prefix+n for n in files};assert str(m['problem_id'])==problem and m['pr']==pr
   # Inspect original authored problem/proof statements, current TeX, metadata and README without executing code.
   inspected=[]
   for name in names:
    rel=name[len(prefix):]
    if rel in ['README.md','metadata.json'] or (rel.endswith('.tex') and rel.count('/')<=2) or (rel.endswith('README.md') and rel.count('/')<=1) or ('original/' in rel and rel.endswith(('PROOF.md','STATEMENT_AND_SCOPE.md','SOURCE_GATE.md','README.md','STATUS.json'))):
     part=z.read(name);save(f'private/pr{pr:04d}/selected/'+rel,part);inspected.append(rel)
   md=d['metadata'];archived_metadata=prefix+'metadata.json' in names
   if archived_metadata:
    metadata=json.loads(z.read(prefix+'metadata.json'));amd=metadata.get('metadata',metadata);assert amd['title']==md['title']
    desc_match=amd['description']==md['description'];apostrophe_only=amd['description'].replace('’',"'")==md['description']
    assert desc_match or (pr==533 and apostrophe_only)
    save(f'archive_metadata_comparison_pr{pr:04d}.json',dict(title_equal=True,description_exact=desc_match,description_diff='U+2019 apostrophe replaced by ASCII apostrophe only' if not desc_match else None,scope='Punctuation-only difference preserves all mathematical wording, qualifiers and disclosure.'))
   links=md.get('related_identifiers',[]);assert any(x.get('identifier')=='https://github.com/AlecKriebel/Math/pull/'+str(pr) for x in links);assert any(n.endswith('.tex') for n in names) and any(n.endswith('.py') for n in names)
   e.update(archived_metadata_present=archived_metadata,members=len(names),manifest_payloads_verified=len(files),manifest_sha256=sha(z.read(mn[0])),manifest_identity={k:m.get(k) for k in ['pr','problem_id','head']},selected_texts=inspected);archives.append(e)
  payloads.append(e)
 assert pdfs and archives
 out.append(dict(pr=pr,problem_id=problem,record=record,doi=doi,title=d['metadata']['title'],published=True,doi_resolution=resolution,ledger_row=rownum,ledger_values=row[:4],unique_primary_DOI_rows=same,files=payloads,scope='Independent existing-publication file/metadata/ledger identity check, not proof or priority endorsement.'))
 save('publication_integrity_checks.json',out);print('verified',pr,record,rownum,flush=True)
save('RESEARCH_LOG.json',json.loads((Q/'RESEARCH_LOG.json').read_text())+[dict(at=now(),completion_estimate_percent=70,event='All91 actual pinned scopes/rows bound;91 live PR metadata compared;523 live closed/comment and pinned current negative row verified; four public records/eight files/strict ZIP manifests and fresh unique GWS rows independently checked. Manual mathematical identity reading remains.')])
