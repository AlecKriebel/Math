#!/usr/bin/env python3
"""Authenticate all supplied public metadata and the publicly served artifacts."""
from pathlib import Path
import datetime,hashlib,json,runpy,urllib.request
ROOT=Path(__file__).resolve().parent

def fetch(url,limit):
    req=urllib.request.Request(url,headers={'User-Agent':'Math-Preprint-Public-Verification/1.0'})
    with urllib.request.urlopen(req,timeout=60) as response:data=response.read(limit+1)
    if len(data)>limit:raise RuntimeError('Public response exceeds size limit')
    return data

def verify_public_metadata(actual,wanted):
    """Compare EVERY supplied field, using only explicit public-schema mapping."""
    expected={'title','upload_type','publication_type','description','creators','access_right','license','version','publication_date','keywords','related_identifiers'}
    if set(wanted)!=expected:raise RuntimeError('Exactly eleven supplied public metadata fields required')
    checked=[]
    for key,value in wanted.items():
        if key=='upload_type':remote=actual.get('resource_type',{}).get('type')
        elif key=='publication_type':remote=actual.get('resource_type',{}).get('subtype')
        elif key=='license':remote=actual.get('license',{}).get('id')
        else:remote=actual.get(key)
        if remote!=value:raise RuntimeError('Public supplied metadata differs at '+key)
        checked.append(key)
    return sorted(checked)

def main():
    runpy.run_path(str(ROOT/'update_pr_publication.py'))['validate_workflow_gate'](json.loads((ROOT/'FINAL_REVIEW_GATE.json').read_text()))
    pub=json.loads((ROOT/'PUBLICATION_RECEIPT.json').read_text());build=json.loads((ROOT/'BUILD_RECEIPT.json').read_text())
    manifest=ROOT/'zenodo-deposit.json';wanted=json.loads(manifest.read_text())['metadata']
    shared=runpy.run_path(str(ROOT/'append_tracker.py'))
    identity=shared['validate_publication_identity'](pub,wanted['title'])
    raw=fetch('https://zenodo.org/api/records/'+str(pub['id']),1000000);actual=json.loads(raw)
    if int(actual['id'])!=pub['id'] or actual['doi']!=pub['doi'] or actual['metadata']['doi']!=pub['doi']:raise RuntimeError('Public record identity mismatch')
    checked=verify_public_metadata(actual['metadata'],wanted)
    expected={build[k]['path']:build[k] for k in ['pdf','verification_zip']}
    if set(f['key'] for f in actual['files'])!=set(expected) or len(actual['files'])!=len(expected):raise RuntimeError('Public file inventory mismatch')
    checks=[]
    for f in actual['files']:
        item=expected[f['key']];url=f['links']['self'];data=fetch(url,item['bytes']+1024);sha=hashlib.sha256(data).hexdigest()
        if len(data)!=item['bytes'] or sha!=item['sha256']:raise RuntimeError('Public artifact mismatch')
        checks.append({'name':f['key'],'url':url,'bytes':len(data),'sha256':sha,'matches_reviewed_artifact':True})
    report={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'doi':pub['doi'],'id':pub['id'],'doi_url':identity['doi_url'],'record_url':identity['record_url'],'public_record_identity_verified':True,'all_supplied_metadata_exact':True,'metadata_fields_verified':checked,'metadata_manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'metadata_comparison':'Every supplied field exactly equal after explicit legacy/public schema projection only; no content normalization accepted. Server-generated extra fields are not supplied metadata.','files':checks,'authentication':'No credentials; public HTTPS record/content endpoints.'}
    (ROOT/'PUBLIC_DOWNLOAD_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    local=ROOT.parent/'_local';local.mkdir(exist_ok=True);(local/'zenodo_public_record_api.json').write_bytes(raw)
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
