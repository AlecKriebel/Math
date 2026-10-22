from pathlib import Path
import json,urllib.request,hashlib,datetime,concurrent.futures
R=Path(__file__).resolve().parent;A=R.parents[1];head='e809a9c40f4ccdaced6f45f10b1dc8b7725a2119';d=json.loads((R/'sources/private/pr.json').read_text());rows=json.loads((A/'RETRIEVAL_RECEIPT.json').read_text())['files']
def check(x):
 url='https://raw.githubusercontent.com/AlecKriebel/Math/'+head+'/'+x['path'];row={'name':x['name'],'url':url,'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(url,timeout=30) as resp:b=resp.read();row['status']=resp.status
  (R/'sources/private'/('remote-'+x['name'])).write_bytes(b);row.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),git_blob_sha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),matches_live_input=b==(A/'inputs'/x['name']).read_bytes(),sha_present_in_live_pr_body=hashlib.sha256(b).hexdigest() in d['body'])
 except Exception as e:row['error']=str(e)
 return row
out=list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(check,rows));(R/'REMOTE_INPUT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
