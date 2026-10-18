#!/usr/bin/env python3
"""Read-only final PR1200–1300 metadata capture; never infer mathematical scope."""
from pathlib import Path
import argparse,datetime,hashlib,json,subprocess
ROOT=Path(__file__).resolve().parent
def sha(body):return hashlib.sha256(body).hexdigest()
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default='final_scope_refresh',help='New program-relative capture directory')
    args=parser.parse_args();out=(ROOT/args.output).resolve()
    if not out.is_relative_to(ROOT) or out==ROOT or out.exists():raise RuntimeError('New dedicated program-local capture folder required')
    oldpath=ROOT/'PR_OUTCOME_METADATA.json';old=json.loads(oldpath.read_text())['data']['repository']
    fields='number title url body state isDraft headRefOid headRefName baseRefName updatedAt mergedAt mergeCommit { oid }'
    query='query { repository(owner:"AlecKriebel",name:"Math") { '+ ' '.join('p'+str(n)+': pullRequest(number:'+str(n)+') { '+fields+' }' for n in range(1200,1301))+' } }'
    request=json.dumps({'query':query}).encode()
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    run=subprocess.run(['gh','api','graphql','--input','-'],input=request,capture_output=True,timeout=120)
    if run.returncode:raise RuntimeError('Metadata capture failed: '+run.stderr.decode())
    data=json.loads(run.stdout)
    if data.get('errors') or set(data.get('data',{}).get('repository',{}))!={'p'+str(n) for n in range(1200,1301)}:raise RuntimeError('Incomplete GraphQL metadata capture')
    rows=[]
    for n in range(1200,1301):
        current=data['data']['repository']['p'+str(n)];previous=old['p'+str(n)]
        if not isinstance(current,dict) or current.get('number')!=n or current.get('url')!='https://github.com/AlecKriebel/Math/pull/'+str(n) or not isinstance(current.get('body'),str):raise RuntimeError('Wrong actual PR identity '+str(n))
        rows.append({'pr':n,'state':current['state'],'isDraft':current['isDraft'],'baseRefName':current['baseRefName'],'body_unchanged':current['body']==previous['body'],'head_unchanged':current['headRefOid']==previous['headRefOid'],'original_body_sha256':sha(previous['body'].encode()),'current_body_sha256':sha(current['body'].encode()),'original_head':previous['headRefOid'],'current_head':current['headRefOid'],'scope':'Metadata comparison only; changed outcome declarations require human-agent semantic reading before scope disposition. No mathematical review, publication or PR mutation.'})
    completed=datetime.datetime.now(datetime.timezone.utc).isoformat();out.mkdir()
    (out/'FINAL_LIVE_METADATA.json').write_bytes(run.stdout)
    (out/'FINAL_METADATA_COMPARISON.json').write_text(json.dumps({'started_at_utc':started,'completed_at_utc':completed,'schema':'math-pr1200-1300-final-metadata-comparison-v1','original_metadata_sha256':sha(oldpath.read_bytes()),'live_metadata_sha256':sha(run.stdout),'records':rows,'count':101,'changed_body_prs':[r['pr'] for r in rows if not r['body_unchanged']],'changed_head_prs':[r['pr'] for r in rows if not r['head_unchanged']],'scope':'Read-only actual outcome metadata, not proof retrieval or scope adjudication.'},indent=2)+'\n')
    print(json.dumps({'output':str(out),'count':101,'changed_body_prs':[r['pr'] for r in rows if not r['body_unchanged']],'changed_head_prs':[r['pr'] for r in rows if not r['head_unchanged']]},indent=2))
if __name__=='__main__':main()
