#!/usr/bin/env python3
"""Own acquisition helper; preserves complete native bodies/ordered transport.
Does not read manuscript or archived review bodies and executes no deposited code.
"""
from pathlib import Path
from datetime import datetime,timezone
import urllib.request,urllib.error,urllib.parse,json,hashlib,sys,time
RID=sys.argv[1];ROOT=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');P=ROOT/'papers'/RID;S=P/'sources';A=P/'acquisition'
now=lambda:datetime.now(timezone.utc).isoformat()
receipts=[]
def fetch(url,name):
    out=S/name
    if out.exists():raise RuntimeError('refusing overwrite '+str(out))
    start=now();req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req,timeout=45) as response:
            data=response.read();status=response.status;final=response.url;headers=list(response.headers.raw_items())
        if status!=200:raise RuntimeError('non200 status '+str(status))
        out.write_bytes(data)
        receipts.append({'requested_url':url,'started_UTC':start,'completed_UTC':now(),'HTTP_status':status,'final_url':final,'response_headers_in_received_order':headers,'body':{'path':str(out),'bytes':len(data),'SHA256':hashlib.sha256(data).hexdigest()},'fresh_ordinary_HTTPS':True})
        return json.loads(data)
    except Exception as exc:
        receipts.append({'requested_url':url,'started_UTC':start,'completed_UTC':now(),'error_type':type(exc).__name__,'error':str(exc),'successful_body':False})
        raise
try:
 record=fetch('https://zenodo.org/api/records/'+RID,'record.raw.json')
 if str(record['id'])!=RID or record.get('status')!='published':raise RuntimeError('not exact published record')
 latest=fetch('https://zenodo.org/api/records/'+RID+'/versions/latest','latest.raw.json')
 versions=fetch('https://zenodo.org/api/records/'+RID+'/versions','versions.page-001.raw.json')
 pages=[versions];nexturl=versions.get('links',{}).get('next')
 while nexturl:
  v=fetch(nexturl,'versions.page-'+str(len(pages)+1).zfill(3)+'.raw.json');pages.append(v);nexturl=v.get('links',{}).get('next')
 files=fetch('https://zenodo.org/api/records/'+RID+'/files','files.raw.json')
 summary={'record_id':RID,'title':record['metadata']['title'],'version_field_present':'version' in record['metadata'],'version':record['metadata'].get('version'),'publication_date_declared':record['metadata']['publication_date'],'record_created':record['created'],'record_updated':record.get('updated',record.get('modified')),'DOI':record['doi'],'latest_record_id':latest['id'],'all_versions_total_native':pages[0]['hits']['total'],'actual_versions_pages_acquired':len(pages),'asset_objects':record['files'],'total_native_asset_bytes':sum(a['size'] for a in record['files']),'source_description_encountered_only_as_machine_metadata':True,'source_scientifically_read':False}
 (A/'METADATA_INTAKE.json').write_text(json.dumps(summary,indent=2)+'\n')
 with (A/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — 25% source acquisition: exact published record, native latest, every versions page and files endpoint acquired whole; original objects and ordered headers retained. Asset authentication and archive custody pending.\n')
 print(json.dumps({k:v for k,v in summary.items() if k!='asset_objects'},indent=2))
 print(json.dumps(record['files'],indent=2))
finally:
 (S/'metadata.transport.json').write_text(json.dumps(receipts,indent=2)+'\n')
