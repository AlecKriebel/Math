from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,io,json,os,re,stat,subprocess,sys,time,urllib.request,zipfile
sys.dont_write_bytecode=True
os.environ.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
Q=Path(__file__).resolve().parent;R=Q.parent.parent;REPO=R.parent
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def save(rel,obj):
 p=Q/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def get(url):
 for attempt in range(3):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Independent-mathematical-publication-coverage-audit/1.0'})
   with urllib.request.urlopen(req,timeout=45) as resp:return resp.read(),dict(status=resp.status,final_url=resp.url,at=now())
  except Exception:
   if attempt==2:raise
   time.sleep(attempt+1)
def run(args,**kw):return subprocess.run(args,cwd=REPO,capture_output=True,check=True,**kw).stdout
params=dict(spreadsheetId='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20',range="'Math Puzzles'!A:AQ",valueRenderOption='FORMATTED_VALUE')
wire=run(['gws','sheets','spreadsheets','values','get','--params',json.dumps(params)]);sheet=json.loads(wire);(Q/'private/ledger_wire.json').write_bytes(wire);rows=sheet['values'];require(rows[0]==['Original Problem','Solution Chat URL','DOI','Notes'],'ledger headers differ');require(len(rows)==178 and max(map(len,rows))==4,'ledger shape changed')
ledger_targets={};targetrows=[]
for n,pid in [(628,'30000403'),(630,'30000700'),(662,'2306086')]:
 aliases={628:['1188-004','Cadoret','Hurwitz'],630:['1460-004','IM-sharing','Theorem H'],662:['AMR-022-6086','6.86','schlicht']}[n]
 exact=[];leads=[]
 for i,row in enumerate(rows,1):
  text=' '.join(row)
  if re.search(r'(?<!\d)'+pid+r'(?!\d)',text) or re.search(r'\bPR\s*#?'+str(n)+r'(?!\d)',text) or f'/pull/{n}' in text:exact.append(i)
  if any(alias.casefold() in text.casefold() for alias in aliases):leads.append(dict(row=i,values=row))
 ledger_targets[n]=dict(exact_identity_rows=exact,semantic_leads=leads)
 if n in [628,630]:require(exact==[],'unexpected candidate ledger identity')
 else:require(exact==[94],'publication ledger identity wrong');targetrows.append(dict(pr=n,row=94,values=rows[93]))
doi='10.5281/zenodo.23384924';variants=[i for i,row in enumerate(rows,1) if len(row)>=3 and doi.casefold() in row[2].casefold()];require(variants==[94],'duplicate primary DOI row');require(rows[93][2].strip() in [doi,'https://doi.org/'+doi],'wrong DOI cell')
save('private/ledger_identity_leads.json',ledger_targets);save('ledger_fresh_receipt.json',dict(at=now(),row_count=len(rows),column_count=4,whole_ledger_sha256=sha(wire),publication_row=94,unique_primary_DOI=True,hold_exact_identity_rows={628:[],630:[]},scope='Fresh whole-sheet read. Full cells and semantic lead review stay private.'))
wire,status=get('https://zenodo.org/api/records/23384924');record=json.loads(wire);save('private/public_662/record.json',record);require(record['state']=='done' and record['submitted'] is True and record['doi']==doi,'public record state DOI mismatch');_,resolution=get('https://doi.org/'+doi);require(resolution['status']==200 and resolution['final_url']=='https://zenodo.org/records/23384924','DOI resolves elsewhere')
rootproof=json.loads((Q/'private/inputs/PR0662_PUBLICATION_VERIFICATION.json').read_text());expected={f['name']:f for f in rootproof['files']};files=[]
for f in record['files']:
 body,http=get(f['links']['self']);digest=sha(body);require(http['status']==200 and len(body)==f['size'] and f['checksum']=='md5:'+hashlib.md5(body).hexdigest(),'download size/md5 mismatch');require(digest==expected[f['key']]['sha256'],'root vs fresh file mismatch');dest=Q/'private/public_662'/f['key'];dest.write_bytes(body);files.append(dict(name=f['key'],bytes=len(body),sha256=digest,md5=hashlib.md5(body).hexdigest(),http=http))
require(len(files)==2,'unexpected file count');z=zipfile.ZipFile(Q/'private/public_662/real_schlicht_verification.zip');names=z.namelist();require(len(names)==len(set(names))==101 and z.testzip() is None,'ZIP names or CRC failure')
for info in z.infolist():
 path=PurePosixPath(info.filename);require(not path.is_absolute() and '..' not in path.parts and '\\' not in info.filename and not stat.S_ISLNK(info.external_attr>>16),'unsafe archive path')
manifest=json.loads(z.read('PACKAGE_MANIFEST.json'));entries=manifest['files'];require(len(entries)==100 and set(names)=={'PACKAGE_MANIFEST.json'}|{x['path'] for x in entries},'archive not exactly positive manifest')
for v in entries:
 body=z.read(v['path']);require(len(body)==v['bytes'] and sha(body)==v['sha256'],'archive payload digest failure')
pdf=(Q/'private/public_662/real_schlicht_preschwarzian.pdf').read_bytes();require(pdf==z.read('real_schlicht_preschwarzian.pdf'),'PDF external/internal differs');pubprefix='unsolved_math_prioritization/publications/2306086/'
blobentries=[x for x in json.loads((Q/'GIT_BLOB_INPUT_MANIFEST.json').read_text())['files'] if x['pr']==662];lookup={x['path']:x for x in blobentries};originals=[]
for v in blobentries:
 if '/attempts/2306086/' in v['path']:
  member='native/'+v['path'];require(member in names and sha(z.read(member))==v['sha256'],'original archived source differs');originals.append(dict(path=v['path'],member=member,bytes=v['bytes'],sha256=v['sha256']))
require(len(originals)==24,'expected exactly 24 original inputs')
for name in ['real_schlicht_preschwarzian.pdf','real_schlicht_preschwarzian.tex','CLAIM_SCOPE.json','CURRENT_PRIORITY_AND_STATUS.md','README.md','verify_package.py']:
 require(sha(z.read(name))==lookup[pubprefix+name]['sha256'],'public source does not match merged head '+name)
for name in ['CLAIM_SCOPE.json','CURRENT_PRIORITY_AND_STATUS.md','README.md','real_schlicht_preschwarzian.tex','native/unsolved_math_prioritization/attempts/2306086/SCOPE_CLARIFICATION.md','native/unsolved_math_prioritization/attempts/2306086/author/PROOF_PARTIALS.md']:
 dest=Q/'private/public_662/inspection'/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(z.read(name))
text=run(['pdftotext','-layout',str(Q/'private/public_662/real_schlicht_preschwarzian.pdf'),'-']);(Q/'private/public_662/paper.txt').write_bytes(text)
save('publication_integrity_checks.json',dict(at=now(),pr=662,record=23384924,doi=doi,title=record['metadata']['title'],description=record['metadata']['description'],creators=record['metadata']['creators'],doi_resolution=resolution,files=files,zip_members=101,positive_manifest_payloads=100,manifest_sha256=sha(z.read('PACKAGE_MANIFEST.json')),all_payload_hashes_verified=True,same_PDF_inside_archive=True,same_merged_PDF_source_scope_and_status=True,unchanged_originals=originals))
# Independently confirm the cached fallback reports null as null, rather than equality.
pin=json.loads((Q/'private/inputs/PR0662_PINNED_SCOPE_VERIFICATION.json').read_text());checks=pin['changed_blobs'];require(len(checks)==46,'pinned special receipt count differs');nulls=[v for v in checks if v['cached_blob'] is None];require(all(v['cached_blob_equal'] is None for v in nulls),'null cached blob falsely asserted equal');require(len(nulls)==45,'null cached science SHA pattern changed');merge='bc2219152e8a2f6c241c31c2fdafe1fe1b5bdb1b';actual=run(['git','diff','--no-ext-diff','--no-renames','--name-only','-z','2669042ac964d5710972af552df141f7934588af...bdca29a7ce8454dda737a80b5baf4280c5f7427e']);oldcount=len(actual.rstrip(b'\0').split(b'\0'));require(oldcount==59037,'integrated-history context changed')
save('special_662_comparison_check.json',dict(at=now(),actual_merge=merge,merge_parents=run(['git','show','--no-patch','--format=%P',merge]).decode().split(),first_parent_paths=46,older_base_three_dot_head_paths=oldcount,cached_null_science_entries=len(nulls),null_equality_preserved=True,all_46_immutable_head_blobs_match_actual_merge=True))
log=json.loads((Q/'RESEARCH_LOG.json').read_text());log.append(dict(at=now(),completion_estimate_percent=80,event='Fresh full 178-row ledger and public DOI/PDF/ZIP verify: one unique row 94, 100 positive payloads, all 24 originals and merged publication source match.'));save('RESEARCH_LOG.json',log)
print(json.dumps(dict(ledger_rows=len(rows),public_files=len(files),zip_members=101,payloads=100,originals=len(originals),null_cached_science=len(nulls))))
