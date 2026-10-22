from pathlib import Path, PurePosixPath
import base64, datetime as dt, hashlib, json, os, re, stat, subprocess, sys, urllib.request, zipfile
sys.dont_write_bytecode=True
os.environ.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
Q=Path(__file__).resolve().parent; R=Q.parent.parent; REPO=R.parent
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def require(v,m):
 if not v: raise RuntimeError(m)
def save(rel,obj):
 p=Q/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def run(args,**kw):return subprocess.run(args,cwd=REPO,capture_output=True,check=True,**kw).stdout
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent-scope-custody-review/1.0'}),timeout=45) as r:
  return r.read(),dict(at=now(),requested_url=url,final_url=r.url,status=r.status,content_type=r.headers.get('Content-Type'))
params=dict(spreadsheetId='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20',range="'Math Puzzles'!A:AQ",valueRenderOption='FORMATTED_VALUE')
wire=run(['gws','sheets','spreadsheets','values','get','--params',json.dumps(params)])
(Q/'private/ledger_wire.json').write_bytes(wire);rows=json.loads(wire)['values']
require(rows[0]==['Original Problem','Solution Chat URL','DOI','Notes'],'Ledger header');require(len(rows)==178 and max(map(len,rows))==4,'Ledger shape changed')
identities={};leads={}
for n,pid,aliases in [(672,'6700060',['AMR-066-0060','mean-convex','dihedral','Gromov']), (681,'30003703',['Satoh','15987-013','Andreadakis']), (718,'30004324',['17296-007','Seshadri','Fulger']), (734,'2515',['KOU-21.6','Kourovka','21538908','De Caro'])]:
 exact=[];broad=[]
 for i,row in enumerate(rows,1):
  t=' '.join(row)
  if re.search(r'(?<!\d)'+pid+r'(?!\d)',t) or re.search(r'\bPR\s*#?'+str(n)+r'(?!\d)',t) or re.search(r'/pull/'+str(n)+r'(?!\d)',t):exact.append(i)
  if any(x.casefold() in t.casefold() for x in aliases):broad.append(dict(row=i,values=row))
 identities[n]=exact;leads[n]=broad
 require(exact==({681:[102],718:[71]}.get(n,[])),'Unexpected target identity rows '+str(n))
for record,rownum in [(23387442,102),(23331395,71)]:
 doi='10.5281/zenodo.'+str(record)
 require([i for i,row in enumerate(rows,1) if len(row)>2 and doi.lower() in row[2].lower()]==[rownum],'DOI duplicate')
 require(rows[rownum-1][2].strip() in [doi,'https://doi.org/'+doi],'DOI cell')
save('private/ledger_semantic_leads.json',dict(exact=identities,leads=leads))
save('ledger_fresh_receipt.json',dict(at=now(),row_count=len(rows),columns=4,wire_bytes=len(wire),wire_sha256=sha(wire),identity_rows=identities,unique_DOI_rows={23387442:102,23331395:71},full_cells_private=True,skill_shared_prerequisite='Absent; user prohibits generate-skills. Used explicitly authorized read-only raw Sheets values.get.'))
checks=[]
for n,record,member_count,payload_count,original_count in [(681,23387442,107,106,23),(718,23331395,78,77,49)]:
 p=Q/f'private/public_{n}';p.mkdir(parents=True,exist_ok=True)
 wire,http=get('https://zenodo.org/api/records/'+str(record));(p/'record_wire.json').write_bytes(wire);r=json.loads(wire)
 doi='10.5281/zenodo.'+str(record);require(r['state']=='done' and r['submitted'] is True and r['doi']==doi,'Public state/DOI')
 _,resolution=get('https://doi.org/'+doi);require(resolution['status']==200 and resolution['final_url']=='https://zenodo.org/records/'+str(record),'DOI resolution')
 expected=json.loads((R/f'PR{n:04d}_PUBLICATION_COVERAGE_DETAILS.json').read_text());expect={v['name']:v for v in expected['public_files']}
 require({v['key'] for v in r['files']}==set(expect),'Unexpected public files')
 files=[]
 for f in r['files']:
  b,fh=get(f['links']['self']);(p/f['key']).write_bytes(b)
  require(len(b)==f['size']==expect[f['key']]['bytes'] and f['checksum']=='md5:'+hashlib.md5(b).hexdigest() and sha(b)==expect[f['key']]['sha256'],'Public bytes mismatch')
  files.append(dict(name=f['key'],bytes=len(b),sha256=sha(b),md5=hashlib.md5(b).hexdigest(),http=fh))
 zipname=next(x['name'] for x in files if x['name'].endswith('.zip'));pdfname=next(x['name'] for x in files if x['name'].endswith('.pdf'))
 z=zipfile.ZipFile(p/zipname);names=z.namelist();require(len(names)==len(set(names))==member_count and z.testzip() is None,'ZIP counts/CRC')
 for i in z.infolist():
  path=PurePosixPath(i.filename);require(not path.is_absolute() and '..' not in path.parts and '\\' not in i.filename and not stat.S_ISLNK(i.external_attr>>16),'Unsafe ZIP path')
 manifest_name='PACKAGE_MANIFEST.json' if n==681 else 'MANIFEST.json';manifest=json.loads(z.read(manifest_name));entries=manifest['files']
 if isinstance(entries,dict): entries=[dict(path=k,**v) for k,v in entries.items()]
 require(len(entries)==payload_count and set(names)=={manifest_name}|{x['path'] for x in entries},'ZIP positive membership')
 for v in entries:
  b=z.read(v['path']);require(len(b)==v.get('bytes',v.get('size')) and sha(b)==v['sha256'],'Positive payload mismatch '+v['path'])
 head=json.loads((R/'rest_inventory.json').read_text());pr=next(x for x in head['pull_requests'] if x['number']==n);originals=[]
 for v in expected['unchanged_originals']:
  b=z.read(v['archive_member']);g=run(['git','show',pr['headRefOid']+':'+v['path']]);require(b==g and len(b)==v['bytes'] and sha(b)==v['sha256'],'Original Git binding '+v['path']);originals.append(v)
 require(len(originals)==original_count,'Original count')
 for name in (['CLAIM_SCOPE.json','CURRENT_PRIORITY_AND_STATUS.md','README.md','satoh_filtration_counterexamples.tex'] if n==681 else ['README.md','paper.tex','zenodo-metadata.json']):
  b=z.read(name);dest=p/'inspection'/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
 if n==681:
  require(z.read(pdfname)==(p/pdfname).read_bytes(),'Internal/external PDF')
  prefix='unsolved_math_prioritization/publications/30003703/'
  for name in ['CLAIM_SCOPE.json','CURRENT_PRIORITY_AND_STATUS.md','README.md','satoh_filtration_counterexamples.tex',pdfname]:require(z.read(name)==run(['git','show',pr['headRefOid']+':'+prefix+name]),'Merged publication identity '+name)
 else:require(pdfname not in names and 'paper.tex' in names,'Standalone PDF/source distinction')
 (p/'paper.txt').write_bytes(run(['pdftotext','-layout',str(p/pdfname),'-']))
 checks.append(dict(pr=n,record=record,doi=doi,title=r['metadata']['title'],description=r['metadata']['description'],record_http=http,record_wire_sha256=sha(wire),doi_resolution=resolution,files=files,archive_members=member_count,positive_payloads=payload_count,manifest_sha256=sha(z.read(manifest_name)),all_payloads_verified=True,originals=originals,PDF_inside_archive=n==681))
save('publication_integrity_checks.json',checks)
# Bind the later explicit withdrawal to current main and the exact existing correction.
wire=run(['gh','api','repos/AlecKriebel/Math/commits/main']);(Q/'private/withdrawal_main_wire.json').write_bytes(wire);commit=json.loads(wire)['sha']
contents=run(['gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+commit]);(Q/'private/withdrawal_queue_wire.json').write_bytes(contents);obj=json.loads(contents);queue=base64.b64decode(obj['content'])
(Q/'private/withdrawal_current_QUEUE.md').write_bytes(queue);require(hashlib.sha1(b'blob '+str(len(queue)).encode()+b'\0'+queue).hexdigest()==obj['sha'],'Current queue Git body')
target=[s for s in queue.decode().splitlines() if s.startswith('| 766 | 2515 / KOU-21.6 |')];require(len(target)==1 and '| already_solved |' in target[0] and 'PR#734 closed without merge' in target[0] and '21538908' in target[0],'Current explicit withdrawal row')
comment=run(['gh','api','repos/AlecKriebel/Math/issues/comments/6160164376']);(Q/'private/withdrawal_comment_wire.json').write_bytes(comment);c=json.loads(comment);require(c['issue_url'].endswith('/issues/734') and '21538908' in c['body'] and 'De Caro' in c['body'],'Wrong correction comment')
save('withdrawal_current_binding.json',dict(at=now(),main_commit=commit,queue_blob=obj['sha'],queue_bytes=len(queue),queue_sha256=sha(queue),source_line=target[0],correction_comment=c['html_url'],comment_sha256=sha(comment),historical_status='claimed_solved',current_status='already_solved',mathematics_or_external_priority_reaudited=False,third_party_ledger_append_required=False))
print(json.dumps(dict(status='PASS',ledger_rows=len(rows),public_files=4,payloads=sum(x['positive_payloads'] for x in checks),originals=sum(len(x['originals']) for x in checks),withdrawal_main=commit)))
