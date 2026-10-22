#!/usr/bin/env python3
"""Offline scope/identity joins, writes only this unsealed review directory."""
from pathlib import Path,PurePosixPath
import collections,datetime,gzip,hashlib,html,json,re
O=Path(__file__).resolve().parent;R=O.parent.parent
Z=lambda n:json.loads(gzip.decompress((O/'private'/n).read_bytes()))
H=lambda b:hashlib.sha256(b).hexdigest();C=lambda a:json.dumps(a,ensure_ascii=False,sort_keys=True,separators=(',',':'))
S=Z('STATE.json.gz');rows=Z('opening_ledger.json.gz');roots=Z('ROOT_VERIFICATION_RECEIPTS.json.gz');extra=Z('EXTRA_PUBLICATION_AND_LEDGER_SOURCES.json.gz');support=Z('SUPPORT_RECEIPTS.json.gz');findings=[];matrix=[];sources={}
def original(p):
 b=(R/p).read_bytes();sources[p]={'bytes':len(b),'sha256':H(b),'text':b.decode()};return json.loads(b)
folders={292:'pr0292_30001608',397:'pr0397_9700002',399:'pr0399_30001179',280:'pr0280_30000156',1329:'pr1329_30003208',1337:'pr1337_30004534',1391:'pr1391_30005740',1348:'pr1348_10000037',1407:'pr1407_1200024',1372:'pr1372_30002726',1330:'pr1330_30003185'}
def metadata_normal(e,a):
 """Only API representation mapping; description characters handled separately."""
 mapped={}
 for k,v in e.items():
  if k=='upload_type':mapped['resource_type.type']=v
  elif k=='publication_type':mapped['resource_type.subtype']=v
  elif k=='license':mapped['license']=v.get('id')if isinstance(v,dict)else v
  elif k=='creators':mapped[k]=[{kk:vv for kk,vv in x.items()if not(kk=='affiliation'and vv in [None,''])}for x in v]
  elif k=='related_identifiers':mapped[k]=[dict(x,scheme=x.get('scheme','url'if x['identifier'].startswith('http')else'doi'))for x in v]
  else:mapped[k]=v
 actual={}
 for k in mapped:
  if k.startswith('resource_type.'):actual[k]=a['resource_type'][k.split('.')[1]]
  elif k=='license':actual[k]=a[k]['id']
  elif k=='creators':actual[k]=[{kk:vv for kk,vv in x.items()if not(kk=='affiliation'and vv in [None,''])}for x in a[k]]
  else:actual[k]=a.get(k)
 return mapped,actual
for item in S['completed_publications']:
 pr=item['pr'];v=json.loads(roots[item['verification']]['text']);obs=Z(f'pr{pr}_scientific_observation.json.gz');views=Z(f'pr{pr}_public_views.json.gz');legacy,native=views['legacy'],views['native'];manchecks=[];carriers={};syntax=[]
 for z in obs['ZIP_observations']:
  mem={x['path']:x for x in z['members']};manresults=[]
  for name,a in z['top_manifests'].items():
   fs=a.get('files');fs=[dict(v,path=k)for k,v in fs.items()]if isinstance(fs,dict)else fs;assert isinstance(fs,list),(pr,name,type(fs));prefix=str(PurePosixPath(name).parent);prefix=''if prefix=='.'else prefix+'/'
   target={prefix+x['path']:x for x in fs};missing=set(target)-set(mem);diff=[]
   for p,e in target.items():
    if p in mem and(e['sha256']!=mem[p]['sha256']or e.get('bytes',e.get('size'))!=mem[p]['bytes']):diff.append(p)
   uncovered=set(mem)-set(target)-{name}
   manresults.append({'manifest':name,'entries':len(fs),'missing':sorted(missing),'hash_or_size_mismatch':diff,'not_in_this_manifest':sorted(uncovered),'exact_self_excluded_closure':not(missing or diff or uncovered)})
  assert any(x['exact_self_excluded_closure']for x in manresults),(pr,manresults)
  manchecks+=manresults;carriers.update(z['metadata_carriers']);syntax+=z['python_syntax']
 if pr in [399,280]:
  path=f'audits/{folders[pr]}/preprint/publication/zenodo-deposit.json';a=json.loads(extra[path]['text']);carriers[path]=a.get('metadata',a)
 mismatches=[];allowed=[]
 for name,e in carriers.items():
  a,b=metadata_normal(e,legacy['metadata'])
  dif={k:{'intended':a[k],'actual':b[k]}for k in a if C(a[k])!=C(b[k])}
  if pr==1348 and set(dif)=={'description'}and a['description'].replace('’',"'")==b['description']:
   path='audits/pr1348_10000037/root_publication_action02/ROOT_COMPLETE_INITIAL_METADATA_NATIVE_UI_ADOPTION.json';ad=original(path);pair=ad['normalization_exact_pair'];assert H(a['description'].encode())==pair['intended_description_sha256']and H(b['description'].encode())==pair['remote_description_sha256'];allowed.append({'carrier':name,'field':'description','rule':'Exact root-adopted U+2019 to ASCII apostrophe only','affected_occurrences':a['description'].count('’'),'adoption':path});dif={}
  if pr==1337 and set(dif)=={'description'}:
   path='audits/pr1337_30004534/root_publication_action01/ROOT_EXACT_DESCRIPTION_SERIALIZATION_ADOPTION.json';ad=original(path)
   assert H(a['description'].encode())==ad['original_description_sha256']and H(b['description'].encode())==ad['server_description_sha256']
   assert a['description'].replace('n>=2','n&gt;=2').replace('’',"'")==b['description']
   allowed.append({'carrier':name,'field':'description','rule':'Exact root-adopted one n>=2 HTML escape plus two U+2019 apostrophes only','adoption':path});dif={}
  if pr==1330:
   allowed.append({'carrier':name,'field':'creators.affiliation','rule':'Intended omission maps to explicit legacy null and native/UI absence; all actual person/name/ORCID fields checked'})
  if dif:mismatches.append({'carrier':name,'differences':dif})
 if mismatches:findings.append({'pr':pr,'metadata_differences':mismatches})
 a=legacy['metadata'];nm=native['metadata'];ui=native['ui'];assert a['title']==nm['title']==ui.get('title',a['title']);assert a.get('version')==nm.get('version')==ui.get('version');assert a['description']==nm['description'];assert a['publication_date']==nm['publication_date'];assert a['resource_type']['subtype']=='preprint'and nm['resource_type']['id']=='publication-preprint'
 assert a.get('keywords',[])==[x['subject']for x in nm.get('subjects',[])];assert a.get('references',[])==[x['reference']for x in nm.get('references',[])];assert a['license']['id']==nm['rights'][0]['id'];assert a['language']==nm['languages'][0]['id']
 strip=lambda s:re.sub(r'\s+','',html.unescape(re.sub('<[^>]*>',' ',s)))
 assert strip(a['description'])==re.sub(r'\s+','',html.unescape(ui['description_stripped']))
 author=a['creators'];assert len(author)==1 and author[0]['name']=='Kriebel, Alec'and author[0]['orcid']=='0009-0001-9320-500X';person=nm['creators'][0]['person_or_org'];assert person['name']=='Kriebel, Alec'and {'identifier':'0009-0001-9320-500X','scheme':'orcid'}in person['identifiers']
 uc=ui['creators']['creators'];nc=nm['creators'];assert len(uc)==len(nc)==1 and uc[0]['person_or_org']==nc[0]['person_or_org']
 assert [x[1]for x in uc[0].get('affiliations',[])]==[x['name']for x in nc[0].get('affiliations',[])]
 assert a.get('related_identifiers',[])==[{'identifier':x['identifier'],'scheme':x['scheme'],'relation':next(y['relation']for y in a.get('related_identifiers',[])if y['identifier']==x['identifier']and y['relation'].lower()==x['relation_type']['id'])}for x in nm.get('related_identifiers',[])]
 if pr in [292,397,399,280]:expectedrow=json.loads(extra[f'audits/{folders[pr]}/LEDGER_PUBLICATION_VERIFICATION.json']['text'])['values']
 elif pr in [1329,1337,1391,1348]:expectedrow=json.loads(extra[f'audits/{folders[pr]}/root_ledger_action01/LITERAL_ROW.json']['text']);expectedrow=expectedrow.get('values',expectedrow.get('row',expectedrow))if isinstance(expectedrow,dict)else expectedrow
 else:expectedrow=v.get('four_literal_cells',v.get('ledger_new_four_literal_cells'))
 assert isinstance(expectedrow,list)and len(expectedrow)==4,(pr,type(expectedrow));assert rows[item['ledger_row']-1][:4]==expectedrow,(pr,'literal row differs')
 hits=[i+1 for i,row in enumerate(rows)if len(row)>2 and row[2].lower().replace('https://doi.org/','').strip()==item['doi'].lower()];assert hits==[item['ledger_row']]
 assert all(obs['PDF_text_observation'][k]for k in ['AI_mentions','unrefereed_or_not_peer_reviewed','ORCID_present','author_present']);assert all(x['syntax']=='PASS'for x in syntax)
 if pr in [292,397,399,280]:adoption=f'audits/{folders[pr]}/ROOT_PUBLICATION_CLEARANCE.json'
 elif pr==1348:adoption=f'audits/{folders[pr]}/ROOT_REPAIR02_SECOND_FRESH_WHOLE_REVIEW_AND_FINAL_PACKAGE_ADOPTION.json'
 elif pr in [1407,1372,1330]:adoption=f'audits/{folders[pr]}/ROOT_SECOND_FRESH_PUBLICATION_WHOLE_REVIEW_AND_FINAL_PACKAGE_ADOPTION.json'
 else:adoption=f'audits/{folders[pr]}/ROOT_FINAL_SCIENTIFIC_PUBLICATION_PACKAGE_ADOPTION.json'
 aa=original(adoption)
 matrix.append({'pr':pr,'problem_id':item['problem_id'],'doi':item['doi'],'record':item['record'],'concept_record':obs['concept_record'],'row':item['ledger_row'],'title':obs['title'],'version':obs['version'],'pages':obs['PDF_text_observation']['pages_formfeed_count'],'public_payloads':obs['public_payloads'],'root_receipt':item['verification'],'scientific_adoption':adoption,'scientific_adoption_sha256':sources[adoption]['sha256'],'expected_metadata_carriers':list(carriers),'metadata_mismatches':mismatches,'explicit_normalization_exceptions':allowed,'source_manifest_checks':manchecks,'ZIP_member_count':sum(x['member_count']for x in obs['ZIP_observations']),'ZIP_uncompressed_bytes':sum(x['total_uncompressed_bytes']for x in obs['ZIP_observations']),'python_syntax_count':len(syntax),'PDF_disclosures_author_ORCID_present':True,'native_legacy_UI_metadata_selected_complete_mapping_verified':True,'literal_four_cells':expectedrow,'current_unique_primary_C_DOIrow':hits[0],'identity_verdict':'HOLD'if mismatches else'PASS','mathematical_reaudit':False})
(O/'private/SCIENTIFIC_ADOPTION_SOURCES.json.gz').write_bytes(gzip.compress(json.dumps(sources,ensure_ascii=False).encode(),mtime=0));(O/'MATRIX.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Eleven completed publications at opening STATE; no pending or later publication assumed','items':matrix,'metadata_findings':findings},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'items':len(matrix),'metadata_findings':findings,'manifest_checks':[(x['pr'],[(y['manifest'],y['exact_self_excluded_closure'],len(y['not_in_this_manifest']))for y in x['source_manifest_checks']])for x in matrix]},ensure_ascii=False,indent=2))
