"""Fresh public record/assets only; preserve every actual transport and API object."""
from pathlib import Path
import urllib.request,urllib.error,datetime,hashlib,json
P=Path(__file__).resolve().parents[2];S=P/'sources';E=P/'reviews/scope'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
receipts=[]
def get(url,dest):
 start=utc();req=urllib.request.Request(url,headers={'User-Agent':'Independent-research-source-custody/1.0'})
 try:
  with urllib.request.urlopen(req,timeout=40) as r:data=r.read();status=r.status;headers=dict(r.headers.items());final=r.url
 except urllib.error.HTTPError as r:data=r.read();status=r.code;headers=dict(r.headers.items());final=r.url
 if dest.exists():raise RuntimeError('preserve_existing_original:'+str(dest))
 dest.write_bytes(data);receipts.append({'requested_url':url,'started_utc':start,'completed_utc':utc(),'status':status,'final_url':final,'headers':headers,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'path':str(dest)})
 (S/'api-and-file-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
 if status!=200:raise RuntimeError('non200_original_saved:'+str(status))
 return data
if (S/'record.raw.json').exists():raise RuntimeError('intake_already_started')
(E/'RESEARCH_LOG.md').write_text('* '+utc()+' — Fresh independent row105 intake started. No existing source/review packet present. Scope reconstruction will precede historical/reviewer opinions and foreign primary bodies. Completion estimate5%.\n')
a=json.loads(get('https://zenodo.org/api/records/23146753',S/'record.raw.json'))
print(json.dumps({'id':a['id'],'metadata':a['metadata'],'links':a['links'],'files':a['files']},ensure_ascii=False,indent=2))
# Follow actual supplied API links, without synthesizing an edition decision.
links=a['links'];latest_url=links.get('latest');versions_url=links.get('versions')
if not latest_url or not versions_url:raise RuntimeError('record_missing_actual_latest_or_versions_links')
latest=json.loads(get(latest_url,S/'latest.raw.json'));versions=json.loads(get(versions_url,S/'versions.raw.json'))
assets=[]
for item in a['files']:
 name=item['key']
 if Path(name).name!=name or name in ['.','..'] or '\\' in name:raise RuntimeError('unsafe_published_asset_key')
 data=get(item['links']['self'],S/name);md5=hashlib.md5(data).hexdigest()
 if len(data)!=item['size'] or item['checksum']!='md5:'+md5:raise RuntimeError('actual_API_size_or_MD5_mismatch')
 assets.append({'original_api_file_object':item,'path':str(S/name),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'md5':md5})
(S/'assets-acquired.json').write_text(json.dumps({'utc':utc(),'record_id':str(a['id']),'all_assets':assets},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'FRESH_ASSETS_ACQUIRED','latest_keys':list(latest),'version_keys':list(versions),'asset_names':[x['original_api_file_object']['key'] for x in assets]},indent=2))
