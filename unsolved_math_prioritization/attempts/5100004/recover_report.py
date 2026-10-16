"""Retrieve one prior report by bounded byte ranges at the immutable revision."""
import json,re,urllib.request,pathlib,hashlib
ROOT=pathlib.Path(__file__).resolve().parent
URL='https://huggingface.co/datasets/ulamai/UnsolvedMath/resolve/37e53eabe540fb458758e198be61634bd02ee008/research_results.json'
lo,hi=0,80334822;target='AMR-050-0004';receipt=[]
def rank(x):return (0,x) if x.startswith('AMR-') else (1,x)
for i in range(16):
 start=max(0,(lo+hi)//2-65536);size=131072
 req=urllib.request.Request(URL,headers={'Range':f'bytes={start}-{start+size-1}'})
 with urllib.request.urlopen(req,timeout=90) as f:
  raw=f.read(size+1)
  if len(raw)>size:raise RuntimeError('Range not honored')
 recs=list(re.finditer(rb'^ "([^"\n]+)": \{',raw,re.M))
 if not recs:raise RuntimeError('No record markers')
 ids=[m[1].decode() for m in recs];print(start,ids[0],ids[-1],flush=True)
 receipt.append({'start':start,'bytes':len(raw),'first_key':ids[0],'last_key':ids[-1]})
 if target in ids:
  m=recs[ids.index(target)];begin=raw.find(b'{',m.start());text=raw[begin:].decode('utf-8',errors='ignore')
  obj,end=json.JSONDecoder().raw_decode(text)
  (ROOT/'sources/pinned_report.json').write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
  (ROOT/'sources/pinned_report_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
  p=json.loads((ROOT/'sources/pinned_problem.json').read_text())
  h=hashlib.sha256(json.dumps([p,obj],sort_keys=True).encode()).hexdigest()
  print('REVIEW HASH',h);print(json.dumps(obj,indent=2,ensure_ascii=False),flush=True);break
 if rank(target)<rank(ids[0]):hi=start
 elif rank(target)>rank(ids[-1]):lo=start+len(raw)
 else:raise RuntimeError('Missing target inside range; ordering assumption invalid')
else:raise RuntimeError('Range search exhausted')
