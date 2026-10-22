#!/usr/bin/env python3
"""Offline, read-only evidence verifier. No network, archive execution or file writes."""
from pathlib import Path,PurePosixPath
import collections,copy,gzip,hashlib,html,json,re,shutil,stat,sys
O=Path(__file__).resolve().parent
H=lambda b:hashlib.sha256(b).hexdigest();C=lambda a:json.dumps(a,ensure_ascii=False,sort_keys=True,separators=(',',':'))
J=lambda p:json.loads((O/p).read_text());Z=lambda p:json.loads(gzip.decompress((O/'private'/p).read_bytes()))
def need(a,b):
 if not a:raise AssertionError(b)
def metadata(p):
 s=p.lstat();need(stat.S_ISDIR(s.st_mode)or stat.S_ISREG(s.st_mode),'special/link namespace member')
 a={'kind':'directory'if stat.S_ISDIR(s.st_mode)else'regular_file','mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns,'nlink':s.st_nlink}
 if stat.S_ISREG(s.st_mode):b=p.read_bytes();a.update(bytes=len(b),sha256=H(b))
 return a
def namespace():return{'.':metadata(O),**{p.relative_to(O).as_posix():metadata(p)for p in sorted(O.rglob('*'))if p.relative_to(O).as_posix()!='MANIFEST.json'}}
preseal=sys.argv[1:]==['--preseal'];need(preseal or not sys.argv[1:],'unsupported arguments')
if not preseal:need(C(namespace())==C(J('MANIFEST.json')['entries']),'exact self-excluded namespace/bytes/mode/nsmtime/nlink closure')
source={}
for n in ['ROOT_VERIFICATION_RECEIPTS.json.gz','EXTRA_PUBLICATION_AND_LEDGER_SOURCES.json.gz','SUPPORT_RECEIPTS.json.gz','SCIENTIFIC_ADOPTION_SOURCES.json.gz','HISTORICAL_DUPLICATE_CREDIT_SOURCES.json.gz','ROOT_FILE_IDENTITY_SOURCES.json.gz']:
 for p,a in Z(n).items():
  b=a['text'].encode();need(len(b)==a['bytes']and H(b)==a['sha256'],'source byte hash')
  if p in source:need(source[p]==a,'overlapping source disagreement')
  source[p]=a
idx=J('SOURCE_INDEX.json');need(len(idx)==47 and set(idx)==set(source),'all47exact source references')
for p,a in source.items():need(idx[p]=={k:a[k]for k in ['bytes','sha256']},'source index pin')
need(idx['PR1330_PUBLICATION_VERIFICATION.json']['sha256']=='897762e39abdeee8e62b91649a494fd193d5d3db89ef7a06dc49d313d98e53a5','parent exact1330 verification binding')
S=Z('STATE.json.gz');closing=Z('closing_STATE.json.gz');matrix=J('MATRIX.json');items=matrix['items'];need(len(items)==len(S['completed_publications'])==11 and not matrix['metadata_findings'],'eleven accepted identity outcomes')
need(len({x['doi']for x in items})==len({x['record']for x in items})==len({x['concept_record']for x in items})==11,'distinct11version/concept identities')
need({x['pr']for x in items}=={x['pr']for x in S['completed_publications']},'all opening completed publications')
need(all(x in closing['completed_publications']for x in S['completed_publications']),'closing preserves completed scope')
need(C(Z('opening_gws_raw0.json.gz'))==C(Z('closing_gws_raw0.json.gz')),'full metadata stable across both captures')
rows=Z('closing_ledger.json.gz');old=Z('opening_ledger.json.gz');need(len(rows)==len(old)==239 and C(rows)==C(old),'full239rowsalltypedcells stable')
for phase in ['opening','closing']:
 a=[Z(f'{phase}_gws_raw{i}.json.gz')for i in range(4)];need(C(a[0])==C(a[3])and C(a[1])==C(a[2]),'full typed metadata bracket and VALUE/FORMULA equality')
 v=a[1]['valueRanges'][0];need(v['valueRange']['values']==rows,'entire values raw envelope')
 grid=v['dataFilters'][0]['gridRange'];need(grid['sheetId']==1254632077 and grid['endColumnIndex']==43,'all43columns numericgid')
def one_row(sheet,doi):
 hits=[i+1 for i,r in enumerate(sheet)if len(r)>2 and r[2].lower().replace('https://doi.org/','').strip()==doi.lower()]
 need(len(hits)==1,'absent/duplicate primary DOI');return hits[0]
def root_file(pr,name):
 item=next(x for x in S['completed_publications']if x['pr']==pr);v=json.loads(source[item['verification']]['text']);fs=v.get('files')or v.get('public_unauthenticated_payloads')or v.get('public_download_payloads')
 if not fs:
  folders={1329:'pr1329_30003208',1337:'pr1337_30004534',1391:'pr1391_30005740',1348:'pr1348_10000037'};p=f"audits/{folders[pr]}/root_publication_action0{2 if pr==1348 else 1}/PUBLIC_PAYLOADS_VERIFIED.json";a=json.loads(source[p]['text']);fs=a.get('payloads',a.get('two_public_payloads'))
 return next(x for x in fs if x['name']==name)
def payload_match(pr,p):
 e=root_file(pr,p['name']);need(p['sha256']==e['sha256']and p['bytes']==e.get('bytes',e.get('size'))and p['md5']==e.get('md5',e.get('checksum','').replace('md5:','')),'payload differs from accepted scientific receipt')
def record_identity(a,item):
 l,n=a['legacy'],a['native'];record=str(item['record']);need(str(l['id'])==n['id']==record,'record identity')
 need(l['doi']==n['pids']['doi']['identifier']==item['doi'],'record DOI')
 need(str(l['conceptrecid'])==n['parent']['id']and l['conceptdoi']==n['parent']['pids']['doi']['identifier']=='10.5281/zenodo.'+n['parent']['id'],'concept identity')
 need([str(x['id'])for x in l['owners']]==[str(n['parent']['access']['owned_by']['user'])]==['1789874'],'owner identity')
 need(n['is_published']is True and n['is_draft']is False and l['state']=='done'and l['submitted']is True,'actually published')
 need(n['access']['record']==n['access']['files']=='public','public access')
 need(n['files']['count']==2 and n['files']['total_bytes']==sum(x['size']for x in l['files']),'native complete science file count/total')
def manifest_closed(z):
 members={x['path']:x for x in z['members']};need(len(members)==len(z['members']),'duplicate archive member');full=False
 for n,a in z['top_manifests'].items():
  fs=a['files'];fs=[dict(v,path=k)for k,v in fs.items()]if isinstance(fs,dict)else fs;parent=str(PurePosixPath(n).parent);prefix=''if parent=='.'else parent+'/';target={prefix+x['path']:x for x in fs}
  need(len(target)==len(fs),'duplicate manifest path')
  for p,e in target.items():need(p in members and e['sha256']==members[p]['sha256']and e.get('bytes',e.get('size'))==members[p]['bytes'],'manifest member hash/size/closure')
  if set(members)==set(target)|{n}:full=True
 need(full,'no full top-level self-excluded manifest')
 return len(members)
def intended_metadata(pr,o,a):
 carriers={k:v for z in o['ZIP_observations']for k,v in z['metadata_carriers'].items()}
 if pr in [399,280]:
  folder='pr0399_30001179'if pr==399 else'pr0280_30000156';p=f'audits/{folder}/preprint/publication/zenodo-deposit.json';v=json.loads(source[p]['text']);carriers[p]=v.get('metadata',v)
 actual=a['legacy']['metadata'];native=a['native']['metadata'];ui=a['native']['ui']
 need(bool(carriers),'no intended metadata source')
 for name,e in carriers.items():
  for k,v in e.items():
   if k=='upload_type':q=actual['resource_type']['type']
   elif k=='publication_type':q=actual['resource_type']['subtype']
   elif k=='license':v=v['id']if isinstance(v,dict)else v;q=actual[k]['id']
   elif k=='related_identifiers':v=[dict(x,scheme=x.get('scheme','url'if x['identifier'].startswith('http')else'doi'))for x in v];q=actual[k]
   elif k=='creators':
    clean=lambda xs:[{kk:vv for kk,vv in x.items()if not(kk=='affiliation'and vv in [None,''])}for x in xs];v=clean(v);q=clean(actual[k])
   else:q=actual.get(k)
   if k=='description'and v!=q and pr in [1337,1348]:
    if pr==1337:
     ad=json.loads(source['audits/pr1337_30004534/root_publication_action01/ROOT_EXACT_DESCRIPTION_SERIALIZATION_ADOPTION.json']['text']);need(H(v.encode())==ad['original_description_sha256']and H(q.encode())==ad['server_description_sha256']and v.replace('n>=2','n&gt;=2').replace('’',"'")==q,'exact1337serialized pair')
    else:
     ad=json.loads(source['audits/pr1348_10000037/root_publication_action02/ROOT_COMPLETE_INITIAL_METADATA_NATIVE_UI_ADOPTION.json']['text'])['normalization_exact_pair'];need(H(v.encode())==ad['intended_description_sha256']and H(q.encode())==ad['remote_description_sha256']and v.replace('’',"'")==q,'exact1348apostrophe pair')
   else:need(C(v)==C(q),'intended metadata field '+k)
 need(actual['title']==native['title']and actual['description']==native['description']and actual['version']==native['version']==ui['version']and actual['publication_date']==native['publication_date'],'native scientific text/version/date')
 plain=lambda s:re.sub(r'\s+','',html.unescape(s));need(plain(re.sub('<[^>]*>',' ',actual['description']))==plain(ui['description_stripped']),'UI mathematical plaintext exact')
 need(actual.get('keywords',[])==[x['subject']for x in native.get('subjects',[])]and actual.get('references',[])==[x['reference']for x in native.get('references',[])],'native keywords/references')
 need(actual['language']==native['languages'][0]['id']and actual['license']['id']==native['rights'][0]['id']and native['resource_type']['id']=='publication-preprint','language/license/type')
 need(len(actual['creators'])==len(native['creators'])==len(ui['creators']['creators'])==1,'single creator')
 creator=actual['creators'][0];person=native['creators'][0]['person_or_org'];up=ui['creators']['creators'][0];need(creator['name']==person['name']=='Kriebel, Alec'and creator['orcid']=='0009-0001-9320-500X'and {'identifier':creator['orcid'],'scheme':'orcid'}in person['identifiers']and up['person_or_org']==person,'author/ORCID native/UI')
 need([x[1]for x in up.get('affiliations',[])]==[x['name']for x in native['creators'][0].get('affiliations',[])],'UI indexed affiliations')
 need([(x['identifier'],x['scheme'],x['relation'].lower())for x in actual.get('related_identifiers',[])]==[(x['identifier'],x['scheme'],x['relation_type']['id'])for x in native.get('related_identifiers',[])],'native related identifiers')

payloads=members=python_count=0
for x in items:
 item=next(y for y in S['completed_publications']if y['pr']==x['pr']);a=Z(f"pr{x['pr']}_public_views.json.gz");o=Z(f"pr{x['pr']}_scientific_observation.json.gz");record_identity(a,item);intended_metadata(x['pr'],o,a);need(x['identity_verdict']=='PASS'and not x['metadata_mismatches'],'identity PASS only after exact specified exceptions')
 need(one_row(rows,x['doi'])==x['row']==item['ledger_row']and rows[x['row']-1][:4]==x['literal_four_cells'],'exact complete approved four strings')
 need(x['scientific_adoption_sha256']==source[x['scientific_adoption']]['sha256'],'scientific adoption binding')
 lf={z['key']:z for z in a['legacy']['files']};nf=a['native']['files']['entries'];ff={z['key']:z for z in a['finalized']['entries']};need(set(lf)==set(nf)==set(ff)=={z['name']for z in o['public_payloads']},'complete public file inventory')
 for sp,sv in source.items():
  sa=json.loads(sv['text']);sr=sa.get('record',sa.get('id'))if isinstance(sa,dict)else None
  if str(sr)!=str(item['record']):continue
  ec=sa.get('concept_record',sa.get('concept'))
  if ec is not None:need(str(ec)==str(a['legacy']['conceptrecid']),'root explicit concept PID')
  ids=sa.get('public_file_identities',sa.get('files',[]))
  if isinstance(ids,list):
   for ei in ids:
    if isinstance(ei,dict)and ei.get('id')and ei.get('name')in lf:need(lf[ei['name']]['id']==ei['id'],'explicit root file UUID identity')
 for p in o['public_payloads']:
  payload_match(x['pr'],p);payloads+=1;n=p['name'];need(p['file_UUID']==lf[n]['id']==nf[n]['id']==ff[n]['file_id'],'all file UUID aliases');need(p['bytes']==lf[n]['size']==nf[n]['size']==ff[n]['size'],'all file size aliases');need('md5:'+p['md5']==lf[n]['checksum']==nf[n]['checksum']==ff[n]['checksum'],'all file checksum aliases');need(p['status']==200 and p['final_url']==p['requested_url'],'actual public unauthenticated GET')
 for z in o['ZIP_observations']:
  need(z['safe_unique_no_symlinks']and z['CRC_all_pass']and z['no_code_executed'],'archive finite checks');members+=manifest_closed(z);python_count+=len(z['python_syntax']);need(all(q['syntax']=='PASS'for q in z['python_syntax']),'Python static syntax')
 need(all(o['PDF_text_observation'][k]for k in ['AI_mentions','unrefereed_or_not_peer_reviewed','ORCID_present','author_present']),'actual PDF disclosures/author')
 d=o['DOI_resolution'];need(d['status']==200 and d['final_url']==f"https://zenodo.org/records/{x['record']}",'DOI exact HTTP destination')
need(payloads==22 and members==491 and python_count==65,'observed totals')
sem=J('SEMANTIC_RECONCILIATION.json');need(sem['unique_matched_rows']==58 and sem['same_result_second_row_found_for_own_eleven']is False and sem['global_zero_duplicate_claim']is False,'bounded semantic distinction/historical credits')
need([x['pr']for x in sem['historical_external_same_theorem_overlaps_preserved']]==[1037,1135],'existing external overlaps not erased')
need(Z('closing_highest.json.gz')[0]['number']==J('CLOSING_SCOPE.json')['highest_PR']==1446,'latest discovered PR')
controls=[]
def reject(name,f):
 try:f()
 except (AssertionError,KeyError,StopIteration):controls.append(name)
 else:raise AssertionError('Corruption control accepted: '+name)
x=items[-1];o=Z('pr1330_scientific_observation.json.gz');a=Z('pr1330_public_views.json.gz');bad=copy.deepcopy(o['public_payloads'][0]);bad['sha256']='0'*64;reject('changed_payload_SHA',lambda:payload_match(1330,bad))
z=copy.deepcopy(o['ZIP_observations'][0]);z['members']=[v for v in z['members']if v['path']!='main.tex'];reject('omitted_editable_proof',lambda:manifest_closed(z))
reject('duplicate_primary_DOI',lambda:one_row(rows+[rows[238]],x['doi']))
bad=copy.deepcopy(a);bad['native']['parent']['id']='23576279';reject('wrong_concept_PID',lambda:record_identity(bad,S['completed_publications'][-1]))
bad=copy.deepcopy(a);bad['legacy']['metadata']['description']+=' Universal all-dimension theorem.';reject('scope_expansion_metadata',lambda:intended_metadata(1330,o,bad))
need(len(controls)==5,'all five meaningful negative controls')
allocation=sum(p.stat().st_blocks*512 for p in O.rglob('*')if p.is_file());free=shutil.disk_usage(O).free;need(allocation<=6*1024**2 and free>=150*1024**2,'physical custody/reserve')
print(json.dumps({'result':'UNSEALED_PREFLIGHT'if preseal else'PASS_ELEVEN_DATED_PUBLICATION_IDENTITIES_NOT_FINAL_CLEARANCE','completed_publications':11,'actual_payloads':payloads,'actual_archive_regular_members':members,'Python_files_statically_parsed':python_count,'raw_GWS_rows':len(rows),'raw_GWS_columns':43,'negative_controls_rejected':controls,'source_pins':len(idx),'own_physical_bytes':allocation,'free_bytes':free,'MANIFEST_sha256':None if preseal else H((O/'MANIFEST.json').read_bytes())},indent=2))
