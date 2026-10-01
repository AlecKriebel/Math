"""Fetch a narrow pinned JSON byte range; never execute upstream content."""
import json,re,urllib.request,pathlib,hashlib
ROOT=pathlib.Path(__file__).resolve().parent
URL='https://huggingface.co/datasets/ulamai/UnsolvedMath/resolve/37e53eabe540fb458758e198be61634bd02ee008/'
def get(name,start,size=131072):
 req=urllib.request.Request(URL+name,headers={'Range':f'bytes={start}-{start+size-1}'})
 with urllib.request.urlopen(req,timeout=90) as f:
  raw=f.read(size+1)
  if len(raw)>size:raise RuntimeError('Range not honored')
  print(name,start,len(raw),flush=True)
  return raw
lo,hi=0,68931837;target=5100004;receipt=[]
for i in range(14):
 start=max(0,(lo+hi)//2-65536);raw=get('problems.json',start)
 recs=list(re.finditer(rb'^    "id": (\d+),',raw,re.M))
 if not recs:raise RuntimeError('No record markers')
 ids=[int(m[1]) for m in recs];print('IDs',ids[:2],ids[-2:],flush=True)
 receipt.append({'start':start,'bytes':len(raw),'first_id':ids[0],'last_id':ids[-1]})
 if target in ids:
  m=recs[ids.index(target)];begin=raw.rfind(b'  {',0,m.start());text=raw[begin:].decode('utf-8',errors='ignore')
  obj,end=json.JSONDecoder().raw_decode(text.lstrip());assert obj['id']==target
  (ROOT/'sources/pinned_problem.json').write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
  (ROOT/'sources/pinned_problem_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
  print('FOUND',json.dumps(obj,ensure_ascii=False),flush=True);break
 if target<ids[0]:hi=start
 elif target>ids[-1]:lo=start+len(raw)
 else:raise RuntimeError('Missing target inside range; ordering assumption invalid')
else:raise RuntimeError('Range search exhausted')
