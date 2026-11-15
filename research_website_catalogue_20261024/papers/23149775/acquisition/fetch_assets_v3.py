#!/usr/bin/env python3
"""Additive asset retry with ordinary wildcard content negotiation.
Retains all earlier failure bodies/transport; no overwrite or deposited execution.
"""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import urllib.request,urllib.error,json,hashlib,sys
RID=sys.argv[1];ROOT=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');P=ROOT/'papers'/RID;S=P/'sources';A=P/'acquisition';CACHE=S/'cache/native-assets-attempt3';CACHE.mkdir(exist_ok=False);now=lambda:datetime.now(timezone.utc).isoformat();receipts=[]
record=json.loads((S/'record-attempt2.body').read_text());latest=json.loads((S/'latest.raw.json').read_text());versions=[json.loads(f.read_text()) for f in sorted(S.glob('versions.page-*.raw.json'))]
if (A/'NATIVE_INTAKE.json').exists() or (S/'asset.transport.v3.json').exists():raise RuntimeError('refusing existing final intake/transport')
try:
 actual=[]
 for original in record['files']:
  key=original['key'];parts=PurePosixPath(key).parts
  if key.startswith('/') or '..' in parts or '\\' in key:raise ValueError('unsafe native key')
  out=CACHE.joinpath(*parts);out.parent.mkdir(parents=True,exist_ok=True);start=now();url=original['links']['self'];req=urllib.request.Request(url,headers={'User-Agent':'curl/8.7.1','Accept':'*/*'})
  try:response=urllib.request.urlopen(req,timeout=45)
  except urllib.error.HTTPError as err:response=err
  with response:
   data=response.read();status=response.code;headers=list(response.headers.raw_items());final=response.url
  if out.exists():raise RuntimeError('refusing body overwrite')
  out.write_bytes(data)
  receipts.append({'requested_url':url,'started_UTC':start,'completed_UTC':now(),'HTTP_status':status,'final_url':final,'request_headers':dict(req.header_items()),'response_headers_in_received_order':headers,'body':{'path':str(out),'bytes':len(data),'SHA256':hashlib.sha256(data).hexdigest()},'fresh_ordinary_HTTPS':True})
  if status!=200:raise RuntimeError('HTTP '+str(status)+' retained at '+str(out))
  algorithm,expected=original['checksum'].split(':',1)
  if len(data)!=original['size'] or hashlib.new(algorithm,data).hexdigest().lower()!=expected.lower():raise RuntimeError('native size/checksum mismatch')
  actual.append({'original_api_file_object':original,'path':str(out),'bytes':len(data),'SHA256':hashlib.sha256(data).hexdigest(),'MD5':hashlib.md5(data).hexdigest(),'native_checksum_verified':True,'magic_prefix_hex':data[:16].hex()})
 intake={'UTC':now(),'record_id':int(RID),'native_record_body_path':str(S/'record-attempt2.body'),'native_record_body_SHA256':hashlib.sha256((S/'record-attempt2.body').read_bytes()).hexdigest(),'record_title':record['metadata']['title'],'version_field_present':'version' in record['metadata'],'version':record['metadata'].get('version'),'publication_date_declared':record['metadata']['publication_date'],'record_created':record['created'],'record_updated':record.get('updated',record.get('modified')),'DOI':record['doi'],'conceptrecid':record['conceptrecid'],'latest_record_id':latest['id'],'all_native_versions_total':versions[0]['hits']['total'],'all_native_versions_pages_acquired':len(versions),'all_assets_in_original_order':actual,'record_description_encountered_only_as_machine_metadata':True,'source_scientifically_read':False,'deposited_code_executed':False,'transport_boundary':'Initial Mozilla request403 retained as exception-only; subsequent successful native metadata requests have full transport. Explicit octet-stream Accept produced406 retained whole; successful wildcard content negotiation is ordinary unauthenticated HTTPS.'}
 (A/'NATIVE_INTAKE.json').write_text(json.dumps(intake,indent=2)+'\n')
 with (A/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — 55% source acquisition: native metadata and every original asset authenticated. Metadata ordinary curl-agent/JSON succeeded after403; explicit octet-stream406 bodies retained and wildcard content negotiation succeeded. Full successful transport/headers preserved; archive custody pending.\n')
 print(json.dumps({'record_id':RID,'version':intake['version'],'declared_date':intake['publication_date_declared'],'latest':latest['id'],'versions_total':intake['all_native_versions_total'],'assets':[{'key':x['original_api_file_object']['key'],'bytes':x['bytes'],'SHA256':x['SHA256']} for x in actual]},indent=2))
finally:
 (S/'asset.transport.v3.json').write_text(json.dumps(receipts,indent=2)+'\n')
