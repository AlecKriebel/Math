"""Capture immutable final-package identities and verify release bytes."""
from capture import *

def getfile(path,ref):
    obj=json.loads(api(f'contents/{path}?ref={ref}'))
    data=base64.b64decode(obj['content'])
    if len(data)!=obj['size']:
        data=base64.b64decode(json.loads(api(f"git/blobs/{obj['sha']}"))['content'])
    assert hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()==obj['sha']
    rec=save(PRIVATE/'release'/str(ref)/path,data)
    rec.update(remote_path=path,ref=ref,git_blob_sha=obj['sha'])
    return rec
if __name__=='__main__':
    root=PRIVATE/'checkpoint'/HERE.parents[1].name
    result=[]
    for n,pid,rounds in [(1141,30006210,['package_01','package_02']),(1150,30003045,['package_04','package_05'])]:
        cov=json.loads((root/f'PR{n}_PUBLICATION_COVERAGE_DETAILS.json').read_text())
        ref=cov['postfreeze_commit']
        prefix=f'draft_pr_actual_claims_1100_1200_20261017/audits/pr{n}_{pid}'
        for path,pin in cov['all_six_release_assets'].items():
            rec=getfile(f'{prefix}/publication/{path}',ref)
            assert rec['bytes']==pin['bytes'] and rec['sha256']==pin['sha256']
            result.append(rec)
        files={1141:{'package_01':['REPORT.md','RECEIPT.json','END_PINS.json'], 'package_02':['REPORT.md','RECEIPT.json','END_CUSTODY.json','INPUT_END_AUTHENTICATION.json']},1150:{r:['REPORT.md','EXTERNAL_FINAL_RECEIPT.json','FINAL_CHECKS.json'] for r in rounds}}
        for r in rounds:
            for name in files[n][r]:result.append(getfile(f'{prefix}/reviews/{r}/{name}',ref))
    save(PRIVATE/'release_binding_captures.json',json.dumps(result,indent=2).encode())
    print(json.dumps({'immutable_release_assets':12,'review_artifacts':len(result)-12}))
