from pathlib import Path
import urllib.request,json,hashlib,zipfile,io,datetime
out=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/reviews/range0400_0420_adversary');pub=out/'public';pub.mkdir(exist_ok=True)
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent-classification-review/1.0'}),timeout=45) as r:return r.read(),{'status':r.status,'final_url':r.url}
wire,receipt=get('https://zenodo.org/api/records/23331232');(pub/'record.json').write_bytes(wire);record=json.loads(wire);results=[]
for f in record['files']:
 data,res=get(f['links']['self']);(pub/f['key']).write_bytes(data)
 result={'name':f['key'],'bytes':len(data),'metadata_bytes':f['size'],'md5':hashlib.md5(data).hexdigest(),'expected_checksum':f['checksum'],'sha256':hashlib.sha256(data).hexdigest(),'download':res}
 if f['key'].endswith('.zip'):
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   result['zip_crc_error']=z.testzip();result['members']=z.namelist();manifest_names=[n for n in z.namelist() if n in ['SOURCE_MANIFEST.json','SUPPORT_MANIFEST.json']]
   for mn in manifest_names:
    b=z.read(mn);(pub/mn).write_bytes(b);result['manifest']=json.loads(b)
 results.append(result)
_,doi=get('https://doi.org/10.5281/zenodo.23331232')
(out/'public_recheck.json').write_text(json.dumps({'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'record_receipt':receipt,'record_sha256':hashlib.sha256(wire).hexdigest(),'state':record.get('state'),'submitted':record.get('submitted'),'doi':record['doi'],'metadata':record['metadata'],'files':results,'doi_resolution':doi},indent=2)+'\n')
print('record',record['doi'],record.get('state'),record.get('submitted'),'doi',doi)
for r in results:print(r['name'],r['bytes'],'checksum',r['expected_checksum']=='md5:'+r['md5'],'crc',r.get('zip_crc_error'),'members',len(r.get('members',[])),'manifestkeys',list(r.get('manifest',{})))
