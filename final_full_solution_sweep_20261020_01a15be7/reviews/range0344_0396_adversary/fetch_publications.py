from pathlib import Path
import urllib.request,json,hashlib,datetime,concurrent.futures
E=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7');O=E/'reviews/range0344_0396_adversary';P=E/'private/pr0344_0396_review'
TARGETS={344:23133607,356:23130727,359:23129302,364:23127646,367:23124601}
def read(url):
 req=urllib.request.Request(url,headers={'User-Agent':'Independent-research-readonly-audit/1.0'})
 with urllib.request.urlopen(req,timeout=90) as r:return r.read(),r.status,r.url

def run(item):
 pr,record=item;dest=P/f'pr{pr:04d}_public';dest.mkdir(exist_ok=True)
 data,status,url=read(f'https://zenodo.org/api/records/{record}');(dest/'record.json').write_bytes(data);obj=json.loads(data)
 out={'pr':pr,'record':record,'queried_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'record_http_status':status,'record_final_url':url,'record_json_sha256':hashlib.sha256(data).hexdigest(),'doi':obj.get('doi'),'record_id_matches':obj.get('id')==record,'published':obj.get('is_published',obj.get('state')=='done'),'files':[]}
 _,status,final=read('https://doi.org/'+obj['doi']);out['doi_resolution']={'status':status,'final_url':final,'correct_record':str(record) in final}
 for f in obj['files']:
  name=f.get('key',f.get('filename'));link=f['links'].get('self',f['links'].get('content'))
  data,status,url=read(link);(dest/name).write_bytes(data)
  out['files'].append({'name':name,'url':link,'final_url':url,'status':status,'declared_size':f['size'],'actual_size':len(data),'size_matches':len(data)==f['size'],'declared_checksum':f['checksum'],'actual_md5':'md5:'+hashlib.md5(data).hexdigest(),'checksum_matches':'md5:'+hashlib.md5(data).hexdigest()==f['checksum'],'sha256':hashlib.sha256(data).hexdigest()})
 return out
result=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 futures={pool.submit(run,item):item for item in TARGETS.items()}
 for f in concurrent.futures.as_completed(futures):
  try:result.append(f.result());print('downloaded',result[-1]['pr'],flush=True)
  except Exception as e: result.append({'pr':futures[f][0],'record':futures[f][1],'error':repr(e)});print('error',result[-1],flush=True)
(O/'public_download_evidence.json').write_text(json.dumps({'scope':'Existing publication identity and custody only, no proof or priority audit','results':sorted(result,key=lambda r:r['pr'])},indent=2)+'\n')
