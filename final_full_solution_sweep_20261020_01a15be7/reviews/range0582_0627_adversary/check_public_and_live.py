from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,io,json,os,re,stat,subprocess,sys,time,urllib.request,zipfile
sys.dont_write_bytecode=True
os.environ.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
Q=Path(__file__).resolve().parent
R=Q.parent.parent
REPO=R.parent
PUB={582:('30004404',23386475,97),585:('30001232',23387814,101),618:('30004609',23331709,73),623:('30001184',23356540,88)}
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(rel,d):
 p=Q/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def get(url):
 for attempt in range(3):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Independent-mathematical-publication-coverage-audit/1.0'})
   with urllib.request.urlopen(req,timeout=45) as resp:return resp.read(),dict(status=resp.status,final_url=resp.url)
  except Exception:
   if attempt==2:raise
   time.sleep(1+attempt)
def run(args,**kwargs):return subprocess.run(args,cwd=REPO,capture_output=True,check=True,**kwargs).stdout
inv=json.loads((Q/'inputs/rest_inventory.json').read_text());prs={p['number']:p for p in inv['pull_requests']}
query='query { repository(owner:"AlecKriebel",name:"Math") {'+' '.join(f'p{n}:pullRequest(number:{n}){{number title body state isDraft mergedAt updatedAt headRefOid baseRefOid mergeCommit{{oid}}}}' for n in range(582,628))+'} }'
wire=run(['gh','api','--hostname','github.com','graphql','--input','-'],input=json.dumps({'query':query}).encode());live=json.loads(wire);save('private/live_prs.json',live);assert 'errors' not in live
differences=[]
for n in range(582,628):
 p=live['data']['repository'][f'p{n}'];old=prs[n];diff=[k for k in p if p[k]!=old.get(k)]
 if diff:differences.append(dict(pr=n,fields=diff))
save('live_metadata_differences.json',differences)
save('live_metadata_receipt.json',dict(at=now(),prs=46,raw_sha256=sha(wire),differences=differences,scope='Dated readonly provider snapshot, not protection against future changes.'))
params=dict(spreadsheetId='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20',range="'Math Puzzles'!A:AQ",valueRenderOption='FORMATTED_VALUE')
wire=run(['gws','sheets','spreadsheets','values','get','--params',json.dumps(params)]);ledger_wire=wire;sheet=json.loads(wire);save('private/ledger.json',sheet);(Q/'private/ledger_wire.json').write_bytes(ledger_wire);rows=sheet['values'];assert rows[0][:4]==['Original Problem','Solution Chat URL','DOI','Notes']
ledger=[];results=[];originals=[]
for n,(pid,rid,rown) in PUB.items():
 doi='10.5281/zenodo.'+str(rid);exact=[(i,row) for i,row in enumerate(rows,1) if len(row)>=3 and row[2].strip() in [doi,'https://doi.org/'+doi]];assert len(exact)==1 and exact[0][0]==rown
 row=exact[0][1];joined=' '.join(row);assert re.search(r'(?<!\d)'+pid+r'(?!\d)',joined);assert re.search(r'\bPR\s*#?'+str(n)+r'(?!\d)',joined) or f'/pull/{n}' in joined
 ledger.append(dict(pr=n,row=rown,values=row,unique_primary_DOI=True))
 wire,status=get('https://zenodo.org/api/records/'+str(rid));record=json.loads(wire);save(f'private/public_{n}/record.json',record);assert record['state']=='done' and record['submitted'] is True and record['doi']==doi
 _,resolution=get('https://doi.org/'+doi);assert resolution==dict(status=200,final_url='https://zenodo.org/records/'+str(rid))
 files=[];archive=None;pdfbytes=None
 rootproof=json.loads((Q/'inputs'/f'PR{n:04d}_PUBLICATION_VERIFICATION.json').read_text());expected={f['name']:f for f in rootproof['files']}
 for f in record['files']:
  body,fs=get(f['links']['self']);assert fs['status']==200 and len(body)==f['size'] and f['checksum']=='md5:'+hashlib.md5(body).hexdigest()
  digest=sha(body);assert expected[f['key']]['sha256']==digest
  kind='.pdf' if f['key'].endswith('.pdf') else '.zip';path=Q/f'private/public_{n}/payload_{digest}{kind}';path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(body)
  info=dict(name=f['key'],bytes=len(body),sha256=digest,md5=hashlib.md5(body).hexdigest(),download_http=fs['status'])
  if kind=='.pdf':pdfbytes=body;pdfpath=path
  else:archive=zipfile.ZipFile(io.BytesIO(body));zipinfo=info
  files.append(info)
 assert archive and pdfbytes
 names=archive.namelist();assert len(names)==len(set(names)) and not archive.testzip()
 for f in archive.infolist():
  p=PurePosixPath(f.filename);assert not p.is_absolute() and '..' not in p.parts and '\\' not in f.filename and not stat.S_ISLNK(f.external_attr>>16)
 if n in [582,585]:
  mn=next(x for x in names if x.endswith('/MANIFEST.json') and x.count('/')==1);prefix=mn.rsplit('/',1)[0]+'/';m=json.loads(archive.read(mn));assert m['pr']==n and m['problem_id']==int(pid);assert all(x.startswith(prefix) for x in names);entries=[dict(path=prefix+p,**v) for p,v in m['files'].items()]
 else:
  mn='PACKAGE_MANIFEST.json';prefix='';m=json.loads(archive.read(mn));entries=m['files'];assert len(entries)==m['file_count']
 assert set(names)=={mn}|{v['path'] for v in entries}
 for v in entries:
  body=archive.read(v['path']);assert len(body)==v['bytes'] and sha(body)==v['sha256']
 assert any(x.endswith('.tex') for x in names) and any(x.endswith('.py') for x in names)
 if n in [618,623]:
  internal=next(x for x in names if x.endswith('.pdf'));assert archive.read(internal)==pdfbytes
 pubtext=run(['pdftotext','-layout',str(pdfpath),'-']).decode();(Q/f'private/public_{n}/paper.txt').write_text(pubtext)
 excerpts=[]
 for name in names:
  if name in [prefix+'README.md',prefix+'metadata.json','CURRENT_PRIORITY_AND_STATUS.md'] or name.endswith('.tex') and name.count('/')<=1:
   data=archive.read(name);dest=Q/f'private/public_{n}/inspection'/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);excerpts.append(dict(path=name,bytes=len(data),sha256=sha(data)))
 science=[x for x in json.loads((Q/'GIT_BLOB_INPUT_MANIFEST.json').read_text())['files'] if x['pr']==n and not x['path'].endswith('/QUEUE.md')]
 matches=[];different=[]
 for v in science:
  relative=v['path'].split('/attempts/'+pid+'/',1)[1]
  candidates=[x for x in names if x.endswith('/original/'+v['path']) or x.endswith('/original/'+relative) or x.endswith('/original/unsolved_math_prioritization/attempts/'+pid+'/'+relative)]
  if n in [618,623]:candidates=['candidate/'+relative] if 'candidate/'+relative in names else []
  equal=[x for x in candidates if sha(archive.read(x))==v['sha256']]
  if equal:matches.append(dict(path=v['path'],archive_path=equal[0],sha256=v['sha256']))
  else:different.append(dict(path=v['path'],candidate_archive_paths=candidates,sha256=v['sha256']))
 if n in [582,585]:assert len(matches)==len(science) and not different
 if n==618:assert len(matches)==16 and len(different)==7
 if n==623:
  core=[v for v in matches if '/packet/' in v['path'] or '/audit/' in v['path']];assert len(core)==24
 originals.append(dict(pr=n,current_science_files=len(science),matches=matches,different_or_absent=different,scope='Current integration provenance files may intentionally differ from the archived historical candidate; core original proof/audit is separately verified.'))
 results.append(dict(pr=n,problem_id=pid,record=rid,doi=doi,title=record['metadata']['title'],description=record['metadata']['description'],related_identifiers=record['metadata'].get('related_identifiers'),creators=record['metadata']['creators'],doi_resolution=resolution,files=files,zip_members=len(names),manifest_payloads_verified=len(entries),all_positive_manifest_hashes_verified=True,TeX_and_code_present=True,publication_inspection_files=excerpts))
 print(json.dumps(dict(pr=n,files=len(files),members=len(names),payloads=len(entries),current_source_matches=len(matches),different=len(different))),flush=True)
save('ledger_fresh_receipt.json',dict(at=now(),rows=len(rows),whole_ledger_sha256=sha(ledger_wire),targets=ledger,scope='WholefourcolumnGWSCLIread; rawledgerkeptprivate'))
save('publication_integrity_checks.json',dict(at=now(),publications=results))
save('original_blob_comparisons.json',dict(at=now(),publications=originals))
save('public_inspection_index.json',dict(at=now(),note='Actual PDF text and archived current README/source/metadata retained privately for root scope comparison.'))
