#!/usr/bin/env python3
"""Read-only bounded capture. No imported sweep code is executed."""
from pathlib import Path
import datetime as dt,hashlib,json,subprocess,urllib.request,concurrent.futures,io,zipfile
HERE=Path(__file__).resolve().parent; P=HERE/'private'; ROOT=HERE.parents[1]; C='39e8a7e1f675baa98d4907e7831edcbf2bf53767'
def sha(b):return hashlib.sha256(b).hexdigest()
def run(args):return subprocess.run(args,capture_output=True,check=True).stdout
def save(path,data):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data);return {'bytes':len(data),'sha256':sha(data)}
def js(path,obj):return save(path,(json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode())
def git(*args):return run(['git',*args])
def remote(ref,name):
 req=urllib.request.Request(f'https://raw.githubusercontent.com/AlecKriebel/Math/{ref}/{name}',headers={'User-Agent':'bounded-independent-audit/1.0'})
 with urllib.request.urlopen(req,timeout=45) as r:return r.read()
def capture(n):
 d=P/f'pr{n}';d.mkdir(exist_ok=True)
 if (d/'CAPTURE.json').exists():
  cached=json.loads((d/'CAPTURE.json').read_text());return {k:v for k,v in cached.items() if k not in ['files','checkpoint_inputs']}
 prefix=str(ROOT.relative_to(Path.cwd()))
 disp=json.loads(remote(C,f'{prefix}/PR{n}_DISPOSITION.json'))
 saved={}
 for p in ROOT.glob(f'PR{n}_*.json'):
  b=remote(C,f'{prefix}/{p.name}');saved[p.name]=save(d/'checkpoint'/p.name,b)
 live=run(['gh','api',f'repos/AlecKriebel/Math/pulls/{n}']);save(d/'live_start.json',live);v=json.loads(live)
 comp=run(['gh','api',f'repos/AlecKriebel/Math/compare/{disp["inventory_base_sha"]}...{disp["inventory_head_sha"]}']);save(d/'compare.json',comp);cf=json.loads(comp)['files']
 files=run(['gh','api',f'repos/AlecKriebel/Math/pulls/{n}/files?per_page=100']);save(d/'live_files.json',files);lf=json.loads(files)
 bs=[]
 for f in cf:
  name=f['filename']; b=remote(disp['inventory_head_sha'],name);save(d/'head'/name,b)
  blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();bs.append({'path':name,'blob':blob,'api_blob':f['sha'],'equal':blob==f['sha'],'sha256':sha(b),'bytes':len(b)})
 summary={'number':n,'head':v['head']['sha'],'base':v['base']['sha'],'body_sha256':sha((v.get('body')or'').encode()),'state':v['state'],'merged':v['merged'],'draft':v['draft'],'all_metadata_bound':v['head']['sha']==disp['inventory_head_sha'] and v['base']['sha']==disp['inventory_base_sha'] and sha((v.get('body')or'').encode())==disp['inventory_body_sha256'],'live_equals_pinned_files':{f['filename']:f['sha'] for f in lf}=={f['filename']:f['sha'] for f in cf},'file_count':len(cf),'queue_files':[f['filename'] for f in cf if 'QUEUE' in f['filename']],'files':bs,'checkpoint_inputs':saved}
 js(d/'CAPTURE.json',summary);return {k:v for k,v in summary.items() if k not in ['files','checkpoint_inputs']}
def get(url):
 req=urllib.request.Request(url,headers={'User-Agent':'bounded-independent-audit/1.0'})
 with urllib.request.urlopen(req,timeout=45) as r:return r.read(),{'url':url,'final_url':r.url,'status':r.status}
def provider(n):
 d=P/f'record{n}';d.mkdir(exist_ok=True); b,receipt=get(f'https://zenodo.org/api/records/{n}');save(d/'record_start.json',b);r=json.loads(b); out={'record':n,'doi':r.get('doi'),'state':r.get('state'),'submitted':r.get('submitted'),'files':[]}
 for f in r.get('files',[]):
  data,rec=get(f['links']['self']); info=save(d/f['key'],data);info.update(name=f['key'],provider_size=f['size'],provider_checksum=f['checksum'],checksum_equal=f['checksum']=='md5:'+hashlib.md5(data).hexdigest(),size_equal=len(data)==f['size'],fetch=rec)
  if f['key'].endswith('.zip'):
   z=zipfile.ZipFile(io.BytesIO(data));info.update(entries=len(z.infolist()),payloads=sum(not x.is_dir() for x in z.infolist()),safe=len(z.namelist())==len(set(z.namelist())) and all(not x.startswith('/') and '..' not in Path(x).parts for x in z.namelist()),crc_ok=z.testzip() is None)
  out['files'].append(info)
 _,out['doi_resolution']=get('https://doi.org/'+r['doi']);js(d/'FETCH.json',out);return out
start={'at':dt.datetime.now(dt.timezone.utc).isoformat(),'checkpoint':C,'branch':git('branch','--show-current').decode().strip(),'git_head':git('rev-parse','HEAD').decode().strip(),'index_sha256':sha(Path('.git/index').read_bytes()),'status_porcelain':git('status','--porcelain').decode()}
js(P/'START_CUSTODY.json',start) if not (P/'START_CUSTODY.json').exists() else None
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:prs=list(ex.map(capture,range(1132,1141)))
params={'spreadsheetId':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','range':"'Math Puzzles'!A:AQ",'valueRenderOption':'FORMATTED_VALUE'}
save(P/'ledger_start.json',run(['gws','sheets','spreadsheets','values','get','--params',json.dumps(params)]))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:providers=list(ex.map(provider,[23063072,23372668,23442649,23443039]))
js(HERE/'CAPTURE_SUMMARY.json',{'started_at':start['at'],'ended_at':dt.datetime.now(dt.timezone.utc).isoformat(),'checkpoint':C,'prs':prs,'providers':providers,'ledger_rows':len(json.loads((P/'ledger_start.json').read_text())['values'])})
print(json.dumps({'prs':prs,'records':[x['record'] for x in providers],'rows':len(json.loads((P/'ledger_start.json').read_text())['values'])},indent=2))
