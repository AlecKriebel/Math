#!/usr/bin/env python3
"""Unauthenticated GET-only reconciliation; payloads/expanded sources remain in memory."""
from pathlib import Path,PurePosixPath
import ast,datetime,gzip,hashlib,html,io,json,re,shutil,stat,subprocess,urllib.request,zipfile
O=Path(__file__).resolve().parent;R=O.parent.parent
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
H=lambda b:hashlib.sha256(b).hexdigest();M=lambda b:hashlib.md5(b).hexdigest()
def guard(n=0):
 assert sum(p.lstat().st_blocks*512 for p in O.rglob('*')if p.is_file())+n<6*1024**2
 assert shutil.disk_usage(O).free-n>=150*1024**2
def save(n,a):
 b=gzip.compress(json.dumps(a,ensure_ascii=False).encode(),mtime=0);guard(len(b));p=O/'private'/n;assert not p.exists();p.write_bytes(b)
def get(u,accept='application/json'):
 req=urllib.request.Request(u,headers={'Accept':accept,'User-Agent':'completed-eleven-publications-readonly-reconciliation'})
 with urllib.request.urlopen(req,timeout=45)as q:b=q.read();info={'requested_url':u,'final_url':q.url,'status':q.status,'bytes':len(b),'sha256':H(b)};assert q.status==200
 return b,info
S=json.loads(gzip.decompress((O/'private/STATE.json.gz').read_bytes()));root=json.loads(gzip.decompress((O/'private/ROOT_VERIFICATION_RECEIPTS.json.gz').read_bytes()));results=[];support={}
folders={1329:'pr1329_30003208',1337:'pr1337_30004534',1391:'pr1391_30005740',1348:'pr1348_10000037'}
def localjson(p):
 b=(R/p).read_bytes();support[p]={'bytes':len(b),'sha256':H(b),'text':b.decode()};return json.loads(b)
for item in S['completed_publications']:
 started=now();pr=item['pr'];v=json.loads(root[item['verification']]['text']);expected=v.get('files')or v.get('public_unauthenticated_payloads')or v.get('public_download_payloads')
 if not expected:
  p=f"audits/{folders[pr]}/root_publication_action0{2 if pr==1348 else 1}/PUBLIC_PAYLOADS_VERIFIED.json";a=localjson(p);expected=a.get('payloads',a.get('two_public_payloads'))
 exp={x['name']:x for x in expected};record=item['record'];base=f'https://zenodo.org/api/records/{record}';b,li=get(base);legacy=json.loads(b);b,ni=get(base,'application/vnd.inveniordm.v1+json');native=json.loads(b);b,fi=get(base+'/files');finalized=json.loads(b)
 save(f'pr{pr}_public_views.json.gz',{'legacy':legacy,'native':native,'finalized':finalized,'GET_receipts':[li,ni,fi]})
 assert str(legacy['id'])==native['id']==str(record);assert legacy['doi']==item['doi']==native['pids']['doi']['identifier'];concept=str(legacy['conceptrecid']);assert concept==native['parent']['id'];assert legacy['conceptdoi']==native['parent']['pids']['doi']['identifier']=='10.5281/zenodo.'+concept
 assert legacy['state']=='done'and legacy['submitted']is True and native['is_published']is True and native['is_draft']is False
 owners=sorted(str(x['id'])for x in legacy['owners']);assert owners==[str(native['parent']['access']['owned_by']['user'])]==['1789874']
 assert native['access']['record']==native['access']['files']=='public'
 lf={x['key']:x for x in legacy['files']};nf=native['files']['entries'];ff={x['key']:x for x in finalized['entries']};assert set(lf)==set(nf)==set(ff)==set(exp);assert len(exp)==2
 payloads={};checks=[];zipfacts=[];paperfacts=[]
 for name,e in exp.items():
  l,n,f=lf[name],nf[name],ff[name];assert l['id']==n['id']==f['file_id'];assert l['size']==n['size']==f['size'];assert l['checksum']==n['checksum']==f['checksum'];assert f['status']=='completed'and n['access']['hidden']is False
  url=f'{base}/files/{name}/content';assert n['links']['content']==f['links']['content']==url
  b,info=get(url);assert len(b)==l['size']==e.get('bytes',e.get('size'));assert H(b)==e['sha256'];assert 'md5:'+M(b)==l['checksum'];assert M(b)==e.get('md5',e.get('checksum','').replace('md5:',''));payloads[name]=b;checks.append(dict(info,name=name,md5=M(b),root_sha256_match=True,file_UUID=l['id']))
 pdfnames=[n for n in payloads if n.endswith('.pdf')];assert len(pdfnames)==1;pdf=payloads[pdfnames[0]];assert pdf.startswith(b'%PDF-')
 process=subprocess.run(['/opt/homebrew/bin/pdftotext','-','-'],input=pdf,capture_output=True,timeout=30);assert process.returncode==0,process.stderr.decode();text=process.stdout.decode();low=text.lower();paperfacts={'pdf_name':pdfnames[0],'text_sha256':H(process.stdout),'text_bytes':len(process.stdout),'pages_formfeed_count':text.count('\f'),'AI_mentions':bool(re.search(r'\bAI\b|artificial intelligence',text,re.I)),'unrefereed_or_not_peer_reviewed':bool(re.search(r'unrefereed|not.{0,90}(human|peer).{0,40}review|no.{0,40}(human|peer).{0,40}review',text,re.I|re.S)),'ORCID_present':'0009-0001-9320-500X'in text,'author_present':'Alec Kriebel'in text}
 for name,b in payloads.items():
  if not name.endswith('.zip'):continue
  z=zipfile.ZipFile(io.BytesIO(b));infos=z.infolist();names=[x.filename for x in infos];assert len(names)==len(set(names));assert z.testzip()is None
  assert all(not PurePosixPath(n).is_absolute()and'..'not in PurePosixPath(n).parts and'\\'not in n for n in names)
  assert all(not stat.S_ISLNK(x.external_attr>>16)for x in infos)
  members=[];jsons={};meta={};science=[];code=[];embedded=[];manifests={}
  for zi in infos:
   if zi.is_dir():continue
   content=z.read(zi);n=zi.filename;members.append({'path':n,'bytes':len(content),'sha256':H(content),'md5':M(content),'CRC32':zi.CRC,'unix_mode':(zi.external_attr>>16)&0xffff})
   if n.lower().endswith('.pdf')and H(content)==H(pdf):embedded.append(n)
   if n.lower().endswith(('.tex','.md','.py','.json','.txt')):
    try:t=content.decode('utf-8')
    except UnicodeDecodeError:continue
    if n.endswith('.py'):
     try:ast.parse(t,filename=n);code.append({'path':n,'syntax':'PASS'})
     except SyntaxError as ex:code.append({'path':n,'syntax':'FAIL','line':ex.lineno,'message':ex.msg})
    if n.endswith('.tex'):science.append({'path':n,'bytes':len(content),'AI_text':bool(re.search(r'\bAI\b|artificial intelligence',t,re.I)),'unrefereed_or_human_limit':bool(re.search(r'unrefereed|not.{0,90}(human|peer).{0,40}review',t,re.I|re.S))})
    if n.lower().endswith('.json'):
     try:a=json.loads(t)
     except ValueError:continue
     jsons[n]=a
     if'manifest'in PurePosixPath(n).name.lower()or PurePosixPath(n).name=='FILES.json':manifests[n]=a
     if isinstance(a,dict)and'title'in a and'description'in a and any(k in a for k in ['creators','metadata']):meta[n]=a
     if isinstance(a,dict)and isinstance(a.get('metadata'),dict)and'title'in a['metadata']and'description'in a['metadata']:meta[n]=a['metadata']
  mindepth=min((len(PurePosixPath(n).parts)for n in manifests),default=0);top={n:a for n,a in manifests.items()if len(PurePosixPath(n).parts)==mindepth}
  zipfacts.append({'name':name,'member_count':len(members),'directory_entries':len(names)-len(members),'safe_unique_no_symlinks':True,'CRC_all_pass':True,'total_uncompressed_bytes':sum(m['bytes']for m in members),'members':members,'top_manifests':top,'all_manifest_names':list(manifests),'metadata_carriers':meta,'embedded_same_public_PDF':embedded,'TeX_sources':science,'python_syntax':code,'no_code_executed':True})
 # DOI HTML is not retained; only the completed redirect target and byte identity.
 db,di=get('https://doi.org/'+item['doi'],'text/html');assert di['final_url'].rstrip('/')==f'https://zenodo.org/records/{record}'
 result={'pr':pr,'problem_id':item['problem_id'],'record':record,'concept_record':int(concept),'doi':item['doi'],'started':started,'completed':now(),'root_receipt':item['verification'],'title':legacy['metadata']['title'],'version':legacy['metadata'].get('version'),'owners':owners,'public_record_identity_PASS':True,'all_three_file_views_exact':True,'public_payloads':checks,'PDF_text_observation':paperfacts,'ZIP_observations':zipfacts,'DOI_resolution':di,'no_service_writes':True,'proofs_reaudited':False}
 results.append(result);save(f'pr{pr}_scientific_observation.json.gz',result);print(json.dumps({'pr':pr,'public_files':len(checks),'PDF_disclosures':paperfacts,'zip_members':[(x['member_count'],list(x['top_manifests']),list(x['metadata_carriers']))for x in zipfacts]},ensure_ascii=False),flush=True)
 del payloads,pdf,b,db,text
save('SUPPORT_RECEIPTS.json.gz',support)
(O/'PUBLIC_COLLECTION_SUMMARY.json').write_text(json.dumps({'at':now(),'count':len(results),'PRs':[x['pr']for x in results],'actual_payloads':sum(len(x['public_payloads'])for x in results),'downloaded_bytes':sum(y['bytes']for x in results for y in x['public_payloads']),'payload_binaries_retained':False,'expanded_source_bodies_retained':False,'code_executed':False,'service_writes':0},indent=2)+'\n');print('ALL_ELEVEN_PUBLIC_GET_COLLECTION_COMPLETE',flush=True)
