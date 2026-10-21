from pathlib import Path
import urllib.request,json,hashlib,datetime
root=Path(__file__).resolve().parent
url='https://api.github.com/repos/AlecKriebel/Math/pulls/200/files?per_page=100'
def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Independent-Publication-Audit/1.0','Accept':'application/json'})
    with urllib.request.urlopen(req,timeout=15) as r:
        data=r.read(1024*1024+1)
        if len(data)>1024*1024:raise RuntimeError('byte ceiling')
    return data
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':url}
try:
    data=get(url);files=json.loads(data)
    candidates=[f['filename'] for f in files if f['filename'].endswith('/PROOF.md')]
    result['proof_candidates']=candidates
    if len(candidates)!=1:raise RuntimeError('not exactly one proof')
    raw='https://raw.githubusercontent.com/AlecKriebel/Math/379a959609958f1e28f68f1ab6e42970ca9d1641/'+candidates[0]
    proof=get(raw);retained=(root.parent/'publication_package_v1/materials/history/ORIGINAL_POSITIVE_PROOF_20261001.md').read_bytes()
    result.update(raw_url=raw,bytes=len(proof),sha256=hashlib.sha256(proof).hexdigest(),exact_historical_payload_identity=proof==retained)
    result['status']='PASS' if proof==retained else 'FAIL'
except Exception as e:result.update(status='UNAVAILABLE',error=str(e))
(root/'ORIGINAL_SOURCE_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
