#!/usr/bin/env python3
"""Read the public record and authenticate the two publicly served artifacts."""
from pathlib import Path
import datetime,hashlib,json,urllib.request
ROOT=Path(__file__).resolve().parent
def fetch(url,limit):
    req=urllib.request.Request(url,headers={'User-Agent':'Math-Preprint-Public-Verification/1.0'})
    with urllib.request.urlopen(req,timeout=60) as response:
        data=response.read(limit+1)
    if len(data)>limit:raise RuntimeError('Public response exceeds expected size limit')
    return data
def main():
    pub=json.loads((ROOT/'PUBLICATION_RECEIPT.json').read_text())
    build=json.loads((ROOT/'BUILD_RECEIPT.json').read_text())
    if pub['state']!='published':raise RuntimeError('Confirmed published record required')
    raw=fetch('https://zenodo.org/api/records/'+str(pub['id']),1000000)
    actual=json.loads(raw)
    if int(actual['id'])!=pub['id'] or actual['doi']!=pub['doi'] or actual['metadata']['title']!=pub['title']:raise RuntimeError('Public record identity mismatch')
    expected={build[k]['path']:build[k] for k in ['pdf','verification_zip']}
    if set(f['key'] for f in actual['files'])!=set(expected):raise RuntimeError('Public file inventory mismatch')
    checks=[]
    for f in actual['files']:
        item=expected[f['key']];url=f['links']['self'];data=fetch(url,item['bytes']+1024)
        sha=hashlib.sha256(data).hexdigest()
        if len(data)!=item['bytes'] or sha!=item['sha256']:raise RuntimeError('Public artifact mismatch')
        checks.append({'name':f['key'],'url':url,'bytes':len(data),'sha256':sha,'matches_reviewed_artifact':True})
    report={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'doi':pub['doi'],'public_record_identity_verified':True,'files':checks,'authentication':'No credentials; public HTTPS record and content endpoints.'}
    (ROOT/'PUBLIC_DOWNLOAD_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    local=ROOT.parent/'_local';local.mkdir(exist_ok=True);(local/'zenodo_public_record_api.json').write_bytes(raw)
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
