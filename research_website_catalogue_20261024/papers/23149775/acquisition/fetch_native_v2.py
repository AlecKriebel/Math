#!/usr/bin/env python3
"""Additive native metadata/asset custody. No supplied code or math read/run."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import urllib.request,urllib.error,urllib.parse,json,hashlib,sys
RID=sys.argv[1];ROOT=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');P=ROOT/'papers'/RID;S=P/'sources';A=P/'acquisition';CACHE=S/'cache/native-assets';CACHE.mkdir(exist_ok=True)
now=lambda:datetime.now(timezone.utc).isoformat()
receipts=[]
record_body=S/'record-attempt2.body';record=json.loads(record_body.read_text());record_receipt=json.loads((S/'record-attempt2.transport.json').read_text())
if record_receipt['HTTP_status']!=200 or str(record['id'])!=RID or record.get('status')!='published':raise RuntimeError('not exact authenticated published record')
if (S/'native.transport.v2.json').exists():raise RuntimeError('refusing overwrite transport')
def get(url,out,accept='application/json'):
    if out.exists():raise RuntimeError('refusing overwrite '+str(out))
    start=now();req=urllib.request.Request(url,headers={'User-Agent':'curl/8.7.1','Accept':accept})
    response=None
    try:
        try:response=urllib.request.urlopen(req,timeout=45)
        except urllib.error.HTTPError as err:response=err
        with response:
            status=response.code;final=response.url;headers=list(response.headers.raw_items());data=response.read()
        out.write_bytes(data)
        item={'requested_url':url,'started_UTC':start,'completed_UTC':now(),'HTTP_status':status,'final_url':final,'response_headers_in_received_order':headers,'request_headers':dict(req.header_items()),'body':{'path':str(out),'bytes':len(data),'SHA256':hashlib.sha256(data).hexdigest()},'fresh_ordinary_HTTPS':True};receipts.append(item)
        if status!=200:raise RuntimeError('HTTP '+str(status)+' retained at '+str(out))
        return data
    except Exception as exc:
        if response is None:receipts.append({'requested_url':url,'started_UTC':start,'completed_UTC':now(),'error_type':type(exc).__name__,'error':str(exc),'successful_body':False})
        raise
try:
 latest=json.loads(get('https://zenodo.org/api/records/'+RID+'/versions/latest',S/'latest.raw.json'))
 first=json.loads(get('https://zenodo.org/api/records/'+RID+'/versions',S/'versions.page-001.raw.json'));versions=[first];nexturl=first.get('links',{}).get('next')
 while nexturl:
    more=json.loads(get(nexturl,S/('versions.page-'+str(len(versions)+1).zfill(3)+'.raw.json')));versions.append(more);nexturl=more.get('links',{}).get('next')
 files=json.loads(get('https://zenodo.org/api/records/'+RID+'/files',S/'files.raw.json'))
 actual=[]
 for original in record['files']:
    key=original['key'];parts=PurePosixPath(key).parts
    if key.startswith('/') or '..' in parts or '\\' in key:raise RuntimeError('unsafe native asset key')
    out=CACHE/key;out.parent.mkdir(parents=True,exist_ok=True)
    data=get(original['links']['self'],out,'application/octet-stream')
    if len(data)!=original['size']:raise RuntimeError('native size mismatch')
    algorithm,expected=original['checksum'].split(':',1);digest=hashlib.new(algorithm,data).hexdigest()
    if digest.lower()!=expected.lower():raise RuntimeError('native checksum mismatch')
    actual.append({'original_api_file_object':original,'path':str(out),'bytes':len(data),'SHA256':hashlib.sha256(data).hexdigest(),'MD5':hashlib.md5(data).hexdigest(),'native_checksum_verified':True,'magic_prefix_hex':data[:16].hex()})
 intake={'UTC':now(),'record_id':int(RID),'native_record_body_path':str(record_body),'native_record_body_SHA256':hashlib.sha256(record_body.read_bytes()).hexdigest(),'record_title':record['metadata']['title'],'version_field_present':'version' in record['metadata'],'version':record['metadata'].get('version'),'publication_date_declared':record['metadata']['publication_date'],'record_created':record['created'],'record_updated':record.get('updated',record.get('modified')),'DOI':record['doi'],'conceptrecid':record['conceptrecid'],'latest_record_id':latest['id'],'all_native_versions_total':first['hits']['total'],'all_native_versions_pages_acquired':len(versions),'all_assets_in_original_order':actual,'record_description_encountered_only_as_machine_metadata':True,'source_scientifically_read':False,'deposited_code_executed':False}
 (A/'NATIVE_INTAKE.json').write_text(json.dumps(intake,indent=2)+'\n')
 with (A/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — 55% source acquisition: ordinary curl-agent/JSON requests succeeded after initial403. Native record/latest/all-version-pages/files and every original asset preserved; declared sizes/native checksums/SHA256 authenticated. Safe complete archive inventory/extraction and reader/TeX identification remain.\n')
 print(json.dumps({k:v for k,v in intake.items() if k not in ['all_assets_in_original_order']},indent=2))
 print(json.dumps([{'key':x['original_api_file_object']['key'],'bytes':x['bytes'],'SHA256':x['SHA256']} for x in actual],indent=2))
finally:
 (S/'native.transport.v2.json').write_text(json.dumps(receipts,indent=2)+'\n')
