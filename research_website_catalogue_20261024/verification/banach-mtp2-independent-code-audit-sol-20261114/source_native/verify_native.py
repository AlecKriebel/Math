#!/usr/bin/env python3
"""Read-only independent custody/authority audit for exactly two native records.

No mathematical programme, renderer, legacy campaign, network request or write
is performed. The only output is JSON on stdout. Python -O keeps all checks.
"""
from pathlib import Path,PurePosixPath
from io import BytesIO
from collections import Counter
import copy,hashlib,json,re,stat,sys,zipfile
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parents[3]
STAGE=P/'verification/local-banach-mtp2-stage-sol-20261025/resume'
sys.path[:0]=[str(STAGE),str(P/'scripts')]
from pypdf import PdfReader
import banach_mtp2_source as supplied
STATUSES={'23217863':'PASS_AT_DECLARED_EXTERNAL_THEOREM_LEVEL','23146753':'PASS_WITH_EXPLICIT_PRIMARY_AND_PRIORITY_LIMITS'}
PINS={
 '23217863':{'publication':'9015e779a369c918f6a08835cce384d9c20d9325060d7910300093367e45cc37','promotion':'155b5fbebb5ad89fce5f68838d3377ab8c9f07e37847c85c0eca67bed82fc2ea','science':'b8f379a432a6866d611b929b8c91a410312a36943b99051574edc135598b280a','editorial':'17ef2f58114a960f8d91ca358d129319beaaf7a4c1e3e4a637fa4b4bd82409cf','source_count':54,'members':41,'reader_pages':7,'embedded_pages':28,'date':'2026-10-07','order':['paper.pdf','source-and-verification.zip'],'version':None},
 '23146753':{'publication':'70d32cfac4132080a916373adeaa9bc0ccecdc276ab9985976f3dbdc4fab12f1','promotion':'68d9fc5e77fd6e701daa92315fb5dacafe45c4dff070b047a39eef9b5204dcdc','science':'9f03be990c7b547ebc341908662b241f84b77ffb9b26f9d834d72407d34b7860','editorial':'a217022c02f02f94e42a368a2c3ef684792de598b11293eb20121bb3a78fdfd9','source_count':27,'members':13,'reader_pages':5,'embedded_pages':5,'date':'2026-10-04','order':['mtp2-edge-closure-verification.zip','mtp2-edge-closure-note.pdf'],'version':'1.0'},
}
checks=Counter();faults=[];inputs={}
def ck(t,f):
 checks[f]+=1
 if not t:raise RuntimeError(f)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
 data=p.read_bytes();inputs[p.relative_to(P).as_posix()]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()};return data
def obj(p):return json.loads(read(p))
def eq(a,b):
 if type(a) is not type(b):return False
 if type(a) is dict:return list(a)==list(b) and all(eq(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b))
 return a==b
def path_under(base,name):
 q=PurePosixPath(name);ck(not q.is_absolute() and '..' not in q.parts and '\\' not in name,'safe relative path')
 p=base/name;ck(not p.is_symlink() and p.resolve().is_relative_to(base.resolve()) and p.is_file(),'regular contained file');return p
def negative(rid,name,fn):
 try:fn()
 except (ValueError,KeyError,TypeError) as e:faults.append({'rid':rid,'case':name,'rejected':True,'reason':str(e)})
 else:raise RuntimeError('undetected mutation '+rid+' '+name)
def audit(rid):
 pin=PINS[rid];paper=P/'papers'/rid;source=paper/'sources';c=obj(paper/'publication.json');g=obj(paper/'promotion.json')
 science_path=P/'verification'/('root-clearance-'+rid+'-20261025.json');editorial_path=P/'verification'/('root-editorial-'+rid+'-20261025.json')
 science,editorial=obj(science_path),obj(editorial_path);b=c['source_binding']
 for p,k in [(paper/'publication.json','publication'),(paper/'promotion.json','promotion'),(science_path,'science'),(editorial_path,'editorial')]:ck(sha(p)==pin[k],'exact separately declared authority pin')
 ck(eq(g['root_clearance_record'],science),'whole original scientific authority retained')
 ck(g['status']==science['status']==STATUSES[rid] and g['disposition_by']=='root','literal custom root status')
 ck(editorial['status']=='ROOT_EDITORIAL_ACCEPTED_FOR_PRIVATE_STAGE' and editorial['private_staging_authorized'] is True and editorial['production_integration_authorized'] is False and editorial['root_scientific_status_preserved_literal']==STATUSES[rid],'private staging authority only')
 ck(sha(paper/'publication.json')==g['publication_sha256']==editorial['publication_sha256'] and sha(paper/'promotion.json')==editorial['promotion_sha256'],'full config hash links')
 for q,h in editorial['editorial_objects'].items():ck(hashlib.sha256(read(P/q)).hexdigest()==h,'root editorial object binding')
 for key in ('root_review','root_custody_receipt'):ck(hashlib.sha256(read(P/science[key])).hexdigest()==science[key+'_sha256'],'root full evidence identity')
 ck(set(g['reviews'])==set(science['reviews'])=={'scope','analytic','adversarial'},'three actual family objects')
 family_status={}
 for family,item in g['reviews'].items():
  r=science['reviews'][family];v=obj(paper/item['verdict_file'])
  ck(eq(item['root_authority_entry'],r) and eq(item['verdict'],v) and eq(v,r['whole_original_custom_verdict']),'whole typed ordered original family objects')
  ck(sha(paper/item['verdict_file'])==item['verdict_sha256']==r['verdict_sha256'],'custom verdict byte binding')
  ck(hashlib.sha256(read(paper/item['report'])).hexdigest()==item['report_sha256']==r['report_sha256'],'family full report byte binding')
  family_status[family]={k:v[k] for k in ['status','assessment','mathematical_assessment','mathematical_verdict','mathematical_disposition'] if k in v}
 raw,meta,api,events,inv=[obj(paper/b[k+'_path']) for k in ['source_receipt','metadata','raw_record','transport_receipt','recursive_archive_inventory']]
 for k,o in [('source_receipt',raw),('metadata',meta),('raw_record',api),('transport_receipt',events),('recursive_archive_inventory',inv)]:
  ck(sha(paper/b[k+'_path'])==b[k+'_sha256'],'native original object byte pin')
  if k+'_original' in b:ck(eq(o,b[k+'_original']),'whole source binding original object')
  if k+'_original' in g:ck(eq(o,g[k+'_original']),'whole promotion original object')
 ck(eq(meta['metadata'],api['metadata']),'literal derivative nested metadata')
 ck(eq(raw['all_assets'],b['all_assets']) and eq(raw['all_assets'],g['all_assets']),'whole native ordered asset arrays')
 ck(eq(api['files'],b['published_file_objects']) and eq(api['files'],g['published_file_objects']) and eq(api['files'],[x['original_api_file_object'] for x in raw['all_assets']]),'whole original API file objects in actual order')
 ck([x['key'] for x in api['files']]==pin['order'],'record-specific PDF ZIP order')
 ck(raw['publication_date']==c['publication_date']==api['metadata']['publication_date']==b['zenodo_publication_date']==b['manuscript_date']==pin['date'],'declared date not transport creation update')
 ck(api['created']==raw['created']==meta['created']==b['record_created_utc'] and api['updated']==raw['updated']==meta['updated']==b['record_updated_utc'],'separate actual creation update times')
 ck(eq(c['version'],pin['version']) and eq(g['version'],pin['version']) and eq(b['zenodo_version'],pin['version']) and b['manuscript_version'] is None,'version values not synthesized')
 ck(('version' in api['metadata']) is (rid=='23146753') and c['version_field_present'] is (rid=='23146753'),'absent metadata key stays absent')
 if rid=='23146753':ck(api['metadata']['version']=='1.0' and b['manuscript_version_printed'] is False,'Zenodo edition not printed manuscript edition')
 for field in ['canonical_url','AA','follow_up']:ck(c[field] is None and g[field] is None,'unchanged null later authority')
 for field in ['rendered_public_copy_approved','local_http_verified','live_http_verified','browser_verified','native_sheet_publication_verified','public_page_published','root_editorial_clearance_received']:ck(g[field] is False and c['review_metadata'][field] is False,'unchanged false historical later gates')
 latest=obj(source/'latest.raw.json');versionlist=obj(source/'versions.raw.json');hits=versionlist['hits']['hits']
 ck(eq(latest,api) and len(hits)==1 and type(hits[0]['id']) is int and hits[0]['id']==int(rid),'genuine current sole record')
 expect=copy.deepcopy(api);expect['swh']=None;ck(api['swh']=={} and eq(expect,hits[0]),'native versions hit swh null distinction')
 ck(type(events) is list and len(events)==5,'five actual transport objects')
 ck([Path(x['path']).name for x in events]==['record.raw.json','latest.raw.json','versions.raw.json']+pin['order'],'original transport order')
 for event in events:
  payload=Path(event['path']);data=read(payload)
  ck(type(event['status']) is int and event['status']==200 and type(event['headers']) is dict,'literal transport status and header map')
  ck(type(event['bytes']) is int and len(data)==event['bytes'] and hashlib.sha256(data).hexdigest()==event['sha256'],'complete saved transport payload')
  ck(set(event)=={'requested_url','started_utc','completed_utc','status','final_url','headers','path','bytes','sha256'},'no invented transport md5 or file object')
 assets=[]
 for item in raw['all_assets']:
  a=item['original_api_file_object'];data=read(Path(item['path']));ck(type(item['bytes']) is int and item['bytes']==a['size']==len(data),'asset exact size')
  ck(a['checksum']=='md5:'+item['md5'] and re.fullmatch('[0-9a-f]{32}',item['md5']) and hashlib.md5(data).hexdigest()==item['md5'] and hashlib.sha256(data).hexdigest()==item['sha256'],'genuine full API MD5 and SHA256')
  event=next(x for x in events if Path(x['path']).name==a['key']);literal='MD5:afc4fd82272a87b678e0efce8beea0d' if rid=='23146753' and a['key'].endswith('.pdf') else 'MD5:'+item['md5']
  ck(event['headers']['oc-checksum']==literal,'opaque original header remains literal')
  assets.append({'name':a['key'],'bytes':len(data),'sha256':item['sha256'],'md5':item['md5'],'oc_checksum':event['headers']['oc-checksum']})
 finalname='SOURCE_FINAL_MANIFEST.json' if rid=='23217863' else 'SOURCE_MANIFEST.json';sealname='SOURCE_FINAL_SEAL.json' if rid=='23217863' else 'SOURCE_SEAL.json'
 final=obj(source/finalname);seal=obj(source/sealname);ready=obj(source/'SOURCE_READY_MANIFEST.json');readyseal=obj(source/'SOURCE_READY_SEAL.json')
 if rid=='23217863':ck(type(final['files']) is dict and len(final['files'])==52 and seal['manifest']['sha256']==sha(source/finalname),'native dictionary final manifest nested seal');rows=[dict(v,path=k) for k,v in final['files'].items()]
 else:ck(type(final['files']) is list and len(final['files'])==25 and seal['manifest_sha256']==sha(source/finalname),'native list final manifest flat seal');rows=final['files']
 ck(readyseal['manifest_sha256']==sha(source/'SOURCE_READY_MANIFEST.json') and readyseal['SOURCE_READY_sha256']==sha(source/'SOURCE_READY.json'),'unaltered original ready seal')
 for row in ready['files']+rows:
  path=path_under(source,row['path']);data=read(path);ck(type(row['bytes']) is int and len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'every original source binding')
 allfiles={x.relative_to(source).as_posix() for x in source.rglob('*') if x.is_file()}
 ck(allfiles=={x['path'] for x in rows}|{finalname,sealname} and len(allfiles)==pin['source_count'],'exact native source file set and count')
 ck(not {'receipt.json','record.json'}&allfiles and not ({'SOURCE_MANIFEST.json','SOURCE_SEAL.json'}&allfiles if rid=='23217863' else {'SOURCE_FINAL_MANIFEST.json','SOURCE_FINAL_SEAL.json'}&allfiles),'no persisted source aliases')
 zpath=source/c['supplement_filename'];z=zipfile.ZipFile(BytesIO(read(zpath)));table=inv['members'];entries=z.infolist();ck(len(entries)==len(table)==pin['members'],'full original complete ZIP member count')
 ck([x.filename for x in entries]==[x['member'] for x in table],'whole native ZIP inventory order')
 embedded=[]
 for ze,row in zip(entries,table):
  q=PurePosixPath(ze.filename);ck(not ze.is_dir() and not q.is_absolute() and '..' not in q.parts and stat.S_IFMT(ze.external_attr>>16) in [0,stat.S_IFREG] and not ze.flag_bits&1,'regular unencrypted ZIP member')
  data=z.read(ze);ck(len(data)==ze.file_size==row['bytes'] and ze.compress_size==row['compressed_bytes'] and f'{ze.CRC:08x}'==row['CRC32'] and hashlib.sha256(data).hexdigest()==row['sha256'],'every complete member CRC size and SHA256')
  ck(read(source/'published-source'/ze.filename)==data and row['extracted_path']==str(source/'published-source'/ze.filename),'exact unchanged extraction')
  if ze.filename.lower().endswith('.pdf'):embedded.append((ze.filename,data))
 ck(len(embedded)==1,'one embedded PDF role')
 pdf=source/c['pdf_filename'];selected=read(pdf);ck(len(PdfReader(BytesIO(selected)).pages)==pin['reader_pages'],'complete selected reader page count')
 ck(len(PdfReader(BytesIO(embedded[0][1])).pages)==pin['embedded_pages'] and (selected==embedded[0][1]) is (rid=='23146753'),'distinct 28 page support versus identical 5 page embedded reader')
 lic=source/'published-source'/('LICENSES.md' if rid=='23217863' else 'LICENSE.txt');lt=read(lic).decode();ck('Creative Commons Attribution 4.0' in lt,'original authored CC BY notice')
 if rid=='23217863':
  up=source/'published-source/sources/upstream';licence=read(up/'LICENSE').decode();at=read(up/'ATTRIBUTION.md').decode();rm=read(up/'Vanishing-of-higher-bounded-Hochschild-cohomology-September-23-2026/README.md').decode()
  ck('Apache License' in licence and 'Version 2.0' in licence and '4. Redistribution.' in licence and 'OpenAI' in at and 'adc7f1241b42e322a6451854ab7e4b4c146bf78a' in at and '**Author:** OpenAI' in rm and 'does not relicense' in lt,'complete original mixed license attribution and README citation')
 # Independent comparison of every editorial native custody copy to actual original.
 originals={p.name:p for p in (paper/'reviews/editorial/original-objects').iterdir() if p.is_file()}
 for name,path in originals.items():
  if name=='root-clearance.json':target=science_path
  elif name=='root-review.md':target=P/science['root_review']
  elif name in ['root-custody-recheck.json','root-custody.json']:target=P/science['root_custody_receipt']
  elif 'verdict' in name:
   family=next(k for k in g['reviews'] if k in name);target=paper/g['reviews'][family]['verdict_file']
  else:target=source/name
  ck(read(path)==read(target),'every full editorial original object byte copy')
 ck(len(originals)==17,'all seventeen raw original object copies')
 # Exercise current source helper positively, then with in-memory semantic faults.
 v=supplied.banach_mtp2_source_view(paper,c,g);ck(eq(v[0],raw) and [x['name'] for x in v[1]['files']]==pin['order'],'actual helper full source view pristine')
 for status in ['PASS',STATUSES[rid]+'_EXTRA',None]:
  bad=copy.deepcopy(g);bad['status']=status;negative(rid,'forged_or_generic_status_'+str(status),lambda bad=bad:supplied.banach_mtp2_source_view(paper,c,bad))
 bad=copy.deepcopy(g);bad['reviews']['analytic']['verdict']['invented_approval']=True;negative(rid,'custom_verdict_extra_field',lambda:supplied.banach_mtp2_source_view(paper,c,bad))
 bad=copy.deepcopy(raw);bad['all_assets'].reverse();negative(rid,'native_order_reversed',lambda:supplied.validate_bm_assets(paper,rid,bad,api))
 bad=copy.deepcopy(raw);bad['all_assets'][0]['bytes']=True;negative(rid,'boolean_asset_size',lambda:supplied.validate_bm_assets(paper,rid,bad,api))
 bad=copy.deepcopy(api)
 if rid=='23217863':bad['metadata']['version']=None
 else:bad['metadata'].pop('version')
 negative(rid,'absent_null_or_missing_version_alias',lambda:supplied.validate_bm_edition(rid,c,g,raw,meta,bad))
 bad=copy.deepcopy(events);bad[-1]['headers']['oc-checksum']='MD5:'+raw['all_assets'][-1]['md5'] if rid=='23146753' else 'MD5:0';negative(rid,'rewritten_header',lambda:supplied.validate_bm_transports(paper,rid,bad,raw,api))
 return {'status':STATUSES[rid],'publication_sha256':sha(paper/'publication.json'),'promotion_sha256':sha(paper/'promotion.json'),'root_science_sha256':sha(science_path),'root_editorial_sha256':sha(editorial_path),'source_files':len(allfiles),'archive_members':len(entries),'original_object_copies':len(originals),'assets':assets,'family_assessment_objects':family_status,'source_final_manifest_sha256':sha(source/finalname),'source_final_seal_sha256':sha(source/sealname)}
def main():
 ck(len(sys.argv)==1,'no overrides')
 result={rid:audit(rid) for rid in PINS}
 print(json.dumps({'status':'NATIVE_CUSTODY_AUTHORITY_AND_LICENSE_INTERFACES_SUPPORTED','records':result,'checks':dict(sorted(checks.items())),'check_count':sum(checks.values()),'in_memory_negative_controls':faults,'input_bindings':dict(sorted(inputs.items())),'helper_sha256':sha(STAGE/'banach_mtp2_source.py'),'scope':'Code/editorial native-custody audit only. No fresh mathematical review, renderer, legacy campaign, source modification or production authority.'},indent=2,ensure_ascii=False))
if __name__=='__main__':main()
