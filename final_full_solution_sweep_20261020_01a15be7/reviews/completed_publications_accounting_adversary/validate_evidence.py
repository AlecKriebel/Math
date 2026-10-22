#!/usr/bin/env python3
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,os,re,stat,subprocess,urllib.parse,zipfile
R=Path(__file__).resolve().parent;B=R.parents[1];REPO=B.parent;S=R/'inputs/effort'
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,d):(R/p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
inputs=json.loads((R/'INPUT_MANIFEST.json').read_text())
def capture_extra(p):
 p=B/p;b=p.read_bytes();q=Path('inputs/effort')/p.relative_to(B);t=R/q;t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(b);inputs['files'].append({'source':str(p),'captured_path':str(q),'captured_at':now(),'bytes':len(b),'sha256':sha(b)});return json.loads(b)
state=json.loads((S/'STATE.json').read_text());sheet=json.loads((R/'live/gws_fullsheet.stdout.json').read_text());rows=sheet['values'];ledger_results=[];public=[];source_results=[];env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
for own in state['completed_publications']:
 receipt=json.loads((S/own['verification']).read_text());pr=own['pr'];n=own['record'];base=R/'live'/f'zenodo_{n}';record=json.loads((base/'record.json').read_text());md=record['metadata'];audit=Path(receipt['evidence']['publication']).parent
 desired=capture_extra(audit/'preprint/publication/zenodo-deposit.json');desired=desired.get('metadata',desired)
 release=capture_extra(audit/'preprint/publication/RELEASE_FILES.json')
 metadata_comparison={k:md.get(k)==v for k,v in desired.items()};metadata_differences={k:{'intended':v,'public':md.get(k)} for k,v in desired.items() if md.get(k)!=v}
 landing=json.loads((base/'doi_landing.html.receipt.json').read_text());u=urllib.parse.urlsplit(landing['resolved_url']);dest_exact=u.scheme=='https' and u.netloc=='zenodo.org' and u.path==f'/records/{n}' and not u.query and not u.fragment
 root_ledger=json.loads((S/receipt['evidence']['ledger']).read_text());actual=rows[own['ledger_row']-1];actual=actual+['']*(4-len(actual));actual=actual[:4]
 tokens=[own['doi'],own['problem_id'],receipt['source_alias'],f'/pull/{pr}',receipt['title']]
 exacthits={t:[i+1 for i,row in enumerate(rows) if any(t.casefold() in str(c).casefold() for c in row)] for t in tokens}
 titleproblemhits=[i+1 for i,row in enumerate(rows) if own['problem_id'] in str(row[0] if row else '') or receipt['source_alias'].casefold() in str(row[0] if row else '').casefold()]
 ledger_results.append({'pr':pr,'expected_row':own['ledger_row'],'row_exact_A_D':actual==root_ledger['values'],'actual':actual,'expected_receipt':receipt['evidence']['ledger'],'token_rows':exacthits,'title_or_problem_first_column_rows':titleproblemhits,'unique_result_and_DOI':all(v==[own['ledger_row']] for v in exacthits.values()) and titleproblemhits==[own['ledger_row']]})
 files=[]
 for f in receipt['files']:
  path=base/f['name'];body=path.read_bytes();fetch=json.loads((base/(f['name']+'.receipt.json')).read_text());api=[x for x in record['files'] if x['key']==f['name']]
  found={'name':f['name'],'actual_bytes':len(body),'sha256':sha(body),'md5':hashlib.md5(body).hexdigest(),'http_200':fetch['status']==200,'size_exact':len(body)==f.get('size',f.get('bytes')),'sha256_exact':sha(body)==f['sha256'],'api_file_unique':len(api)==1,'api_size_exact':len(api)==1 and api[0]['size']==len(body),'api_md5_exact':len(api)==1 and api[0]['checksum']=='md5:'+hashlib.md5(body).hexdigest(),'root_md5_exact':f.get('checksum','md5:'+f.get('md5',''))=='md5:'+hashlib.md5(body).hexdigest()}
  if path.suffix=='.zip':
   with zipfile.ZipFile(path) as z:
    names=z.namelist();prefix=names[0].split('/')[0]+'/';manifest_name=prefix+('FILES.json' if pr==399 else 'MANIFEST.json');man=json.loads(z.read(manifest_name));listed=man['files'];listed={x['path']:x for x in listed} if isinstance(listed,list) else listed
    checks=[]
    for rel,v in listed.items():
     b=z.read(prefix+rel);checks.append({'path':rel,'bytes_exact':len(b)==v['bytes'],'sha256_exact':sha(b)==v['sha256']})
    safety=all(not x.startswith('/') and '..' not in PurePosixPath(x).parts and not stat.S_ISLNK(z.getinfo(x).external_attr>>16) for x in names)
    source_name=prefix+('provenance/SOURCE_SNAPSHOT.json' if pr==399 else 'SOURCE_SNAPSHOT.json');ss=json.loads(z.read(source_name));sourcechecks=[]
    for v in ss['files']:
     loc=v.get('copied_path',v.get('local',v.get('snapshot')));loc=('candidate/'+loc.removeprefix('original/')) if pr==397 else loc;archivebody=z.read(prefix+loc)
     obj=subprocess.run(['git','cat-file','blob',v['git_blob']],capture_output=True,cwd=REPO,env=env)
     sourcechecks.append({'archive_path':loc,'repository_path':v.get('original_path',v.get('repository_path',v.get('path'))),'blob':v['git_blob'],'archive_bytes':len(archivebody),'archive_sha256':sha(archivebody),'snapshot_size_exact':len(archivebody)==v['bytes'],'snapshot_sha256_exact':sha(archivebody)==v['sha256'],'immutable_git_blob_available':obj.returncode==0,'immutable_git_blob_exact':obj.returncode==0 and obj.stdout==archivebody})
    embedded_pdf=[x for x in names if x.endswith('.pdf')];externalpdf=next(x for x in receipt['files'] if x['name'].endswith('.pdf'));pdfmatches=[x for x in embedded_pdf if sha(z.read(x))==externalpdf['sha256']]
    found['zip']={'members':len(names),'crc_ok':z.testzip() is None,'unique_names':len(names)==len(set(names)),'safe_names_no_symlinks':safety,'manifest':manifest_name,'manifest_entries':len(listed),'manifest_exact_payload_coverage':set(prefix+x for x in listed)==set(names)-{manifest_name},'all_manifest_payloads_exact':all(c['bytes_exact'] and c['sha256_exact'] for c in checks),'manifest_checks':checks,'source_snapshot':source_name,'source_snapshot_pr_exact':ss['pr']==pr,'source_snapshot_head_exact':ss['head']==receipt['original_head'],'source_snapshot_originals':len(sourcechecks),'source_snapshot_all_exact':all(all(v for k,v in c.items() if k.endswith('_exact')) for c in sourcechecks),'embedded_pdf_matching_published_pdf':pdfmatches,'source_and_support_presence':{'editable_TeX':any(x.endswith('.tex') for x in names),'readme':prefix+'README.md' in names,'reproduction_code':any(x.endswith('.py') for x in names),'original_files':any('/original/' in x or '/candidate/' in x for x in names),'source_snapshot':source_name in names,'scoped_reviews':any('/reviews/' in x or '/historical_reviews/' in x for x in names)}}
    source_results.append({'pr':pr,'checks':sourcechecks})
  files.append(found)
 public.append({'pr':pr,'record':n,'doi':own['doi'],'state':record['state'],'status':record['status'],'submitted':record['submitted'],'record_and_doi_exact':record['id']==n and record['doi']==own['doi'] and md['doi']==own['doi'],'title_exact':md['title']==receipt['title'],'version':md.get('version'),'version_exact':md.get('version')==receipt.get('version','1.0'),'creator_exact':md['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'desired_metadata_fields':metadata_comparison,'metadata_differences':metadata_differences,'doi_landing_http_200':landing['status']==200,'doi_destination_exact':dest_exact,'resolved_url':landing['resolved_url'],'api_file_set_exact':{x['key'] for x in record['files']}=={x['name'] for x in receipt['files']},'files':files,'release_receipt':str(audit/'preprint/publication/RELEASE_FILES.json')})
# Broad ledger candidate searches are leads, adjudicated in report rather than assumed duplicates.
families={292:r'chunk|file.sharing|population process',397:r'congestion|fragmentation|aldous|spare.capacity',399:r'free product|tensor.core|skeide|30001178',280:r'birational|cycle.distribution|vivaldi|30000156'}
leads={str(pr):[{'row':i+1,'title':row[0] if row else '', 'text':' '.join(map(str,row))} for i,row in enumerate(rows) if re.search(pattern,' '.join(map(str,row)),re.I)] for pr,pattern in families.items()}
save('LEDGER_VALIDATION.json',{'completed_at':now(),'source':'live/gws_fullsheet.stdout.json','full_requested_range':sheet['range'],'rows_returned':len(rows),'four_rows':ledger_results,'all_exact_unique':all(x['row_exact_A_D'] and x['unique_result_and_DOI'] for x in ledger_results),'semantic_leads':leads})
save('PUBLIC_VALIDATION.json',{'completed_at':now(),'records':public});save('IMMUTABLE_SOURCE_VALIDATION.json',{'completed_at':now(),'environment_override':{'GIT_OPTIONAL_LOCKS':'0'},'command':'git cat-file blob <immutable object ID>; no index/ref writes','results':source_results});save('INPUT_MANIFEST.json',inputs)
print(json.dumps({'ledger_rows':len(rows),'ledger_four_exact_unique':all(x['row_exact_A_D'] and x['unique_result_and_DOI'] for x in ledger_results),'semantic_lead_rows':{k:[v['row'] for v in vals] for k,vals in leads.items()},'records':[{'pr':p['pr'],'record_doi_exact':p['record_and_doi_exact'],'metadata_differences':p['metadata_differences'],'files':[{'name':f['name'],'size_exact':f['size_exact'],'sha256_exact':f['sha256_exact'],'zip':{k:v for k,v in f.get('zip',{}).items() if k not in ['manifest_checks','embedded_pdf_matching_published_pdf']}} for f in p['files']]} for p in public]},indent=2))
