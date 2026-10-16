#!/usr/bin/env python3
"""Close the selected claimed_solved PR only after the pinned priority decision.

Default is read-only validation. No branch, index, original, queue, merge,
publication, DOI or spreadsheet mutation is performed by this helper.
"""
import argparse
from datetime import datetime,timezone,timedelta
import hashlib
import json
from pathlib import Path
import stat
import subprocess
from urllib.parse import quote

P=Path(__file__).resolve().parent
ROOT=P.parent
A=P/'audits/pr932_30003471'
HEAD='c09ef9df8b1f4642be0396ba6343344be8fa25b0'
PREFIX='unsolved_math_prioritization/attempts/30003471'
FAMILIES={'analytic_family','geometry_family','source_model_family','counterexample_family',
          'reproducibility_family','recent_priority_family','classical_priority_family','priority_falsifier'}

def need(condition,message):
    if not condition:raise RuntimeError(message)

def sha(raw):return hashlib.sha256(raw).hexdigest()

def run(args):return subprocess.run(args,cwd=ROOT,check=True,capture_output=True,text=True).stdout

def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n')

def classify(pr,status):
    if pr['state']!='OPEN' or not pr['isDraft']:return 'SKIP_NOT_OPEN_DRAFT'
    if status!='claimed_solved':return 'SKIP_STATUS_ONLY'
    need(pr['number']==932 and pr['headRefOid']==HEAD and pr['baseRefName']=='main','Selected immutable head/base changed')
    return 'ELIGIBLE'

def gate():
    pr=json.loads(run(['gh','pr','view','932','--repo','AlecKriebel/Math','--json',
                      'number,state,isDraft,headRefOid,baseRefName,url']))
    if pr['state']!='OPEN' or not pr['isDraft']:return {'action':'SKIP_NOT_OPEN_DRAFT','pr':pr}
    queue=run(['gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+pr['headRefOid'],
               '-H','Accept: application/vnd.github.raw+json'])
    rows=[r for r in queue.splitlines() if '| 30003471 /' in r]
    need(len(rows)==1,'Ambiguous target status row')
    status=rows[0].split('|')[8].strip()
    action=classify(pr,status)
    if action!='ELIGIBLE':return {'action':action,'status':status,'pr':pr,'math_source_read':False}
    need(rows[0].split('|')[9].strip()=='1/5','Original author accounting changed')
    return {'action':action,'status':status,'pr':pr,'queue_row_sha256':sha(rows[0].encode()),'utc':datetime.now(timezone.utc).isoformat()}

def verify_family(name,pin):
    folder=A/'reviews'/name;raw=(folder/'MANIFEST.json').read_bytes()
    need(sha(raw)==pin,'Changed sealed review map: '+name)
    manifest=json.loads(raw);records=manifest.get('files',manifest.get('records'))
    items=records.items() if isinstance(records,dict) else [(r['path'],r) for r in records]
    count=0
    for rel,record in items:
        path=Path(rel)
        need(not path.is_absolute() and '..' not in path.parts and not set(path.parts)&{'private','private_sources','tmp','__pycache__'},'Unsafe review member')
        file=folder/path;need(stat.S_ISREG(file.lstat().st_mode),'Nonregular review member')
        raw=file.read_bytes()
        need(len(raw)==record['bytes'] and sha(raw)==record['sha256'],'Changed review member: '+name+'/'+rel)
        count+=1
    return count

def originals():
    raw=subprocess.run(['git','ls-tree','-r','-z',HEAD,'--',PREFIX],cwd=ROOT,check=True,capture_output=True).stdout
    names=[]
    for item in raw.split(b'\0'):
        if not item:continue
        header,name=item.split(b'\t',1);mode,kind,oid=header.decode().split();name=name.decode()
        need(mode=='100644' and kind=='blob' and name.startswith(PREFIX+'/'),'Original Git mode/path')
        expected=subprocess.run(['git','cat-file','blob',oid],cwd=ROOT,check=True,capture_output=True).stdout
        path=A/'original'/name;need(stat.S_ISREG(path.lstat().st_mode) and path.read_bytes()==expected,'Original bytes changed')
        names.append(name)
    need(len(names)==29,'Original file count')
    base=A/'original'/PREFIX
    actual=[str(f.relative_to(A/'original')) for f in base.rglob('*') if not f.is_dir()]
    need(set(actual)==set(names),'Original closed inventory changed')

def preflight(external):
    state=json.loads((P/'CURRENT_STATE.json').read_text())
    need(state['active_pr']==932 and str(state['active_problem_id'])=='30003471','Not the selected active target')
    raw=(A/'PRIORITY_DISPOSITION.json').read_bytes();need(sha(raw)==external,'Priority decision anchor changed')
    decision=json.loads(raw)
    need(decision['pr']==932 and decision['problem_id']=='30003471' and decision['original_head']==HEAD and
         decision['disposition']=='CLOSE_WITHOUT_MERGE_ESTABLISHED_PRIORITY' and decision['fresh_priority_falsification_passed'] is True,
         'Priority closure decision absent')
    need(set(decision['review_manifest_sha256'])==FAMILIES,'Required independent families missing')
    counts={name:verify_family(name,pin) for name,pin in decision['review_manifest_sha256'].items()}
    need(counts==decision['curated_public_file_counts'],'Review counts changed')
    originals()
    body=(A/'CLOSURE_COMMENT_DRAFT.md').read_text()
    need(sha(body.encode())==decision['closure_comment_sha256']==decision['fresh_reviewer_approved_comment_sha256'],'Closure comment differs from reviewed version')
    replay=json.loads((A/'ROOT_REPRO_CURRENT_VERIFICATION.json').read_text())
    need(replay['pipeline_exit_code']==0 and replay['legacy_status']=='EXACT_LEGACY_RECEIPT_MISMATCH' and
         replay['actual_immutable_Git_files_authenticated']==29,'Reproduction evidence incomplete')
    parent=run(['git','ls-remote','origin','refs/heads/main']).split()[0]
    run(['git','fetch','--no-write-fetch-head','origin',parent])
    catalog=json.loads(run(['git','show',parent+':unsolved_math_prioritization/catalog.json']))
    rows=[v for v in catalog if str(v['id'])=='30003471'];need(len(rows)==1,'Current target identity ambiguous')
    old=json.loads((A/'TARGET_IDENTITY_PREFLIGHT.json').read_text());target=rows[0]
    need(target['present'] is True and target['holds']==[] and target['review_hash']==old['review_hash'] and
         target['statement_hash']==old['statement_hash'],'Current target source identity/readiness changed')
    return body,decision,{'remote_main':parent,'original_files':29,'review_counts':counts,'decision_sha256':external,
                           'closure_comment_sha256':sha(body.encode()),'new_author_proof_search_turns':0}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--disposition-sha256',required=True);parser.add_argument('--execute',action='store_true');args=parser.parse_args()
    eligible=gate()
    if eligible['action']!='ELIGIBLE':
        save(A/'PR932_SKIPPED_FINAL_GATE.json',eligible);print(json.dumps(eligible));return
    body,decision,verification=preflight(args.disposition_sha256)
    if not args.execute:
        save(A/'CLOSURE_PREFLIGHT.json',{'utc':datetime.now(timezone.utc).isoformat(),'eligible':eligible,**verification,'external_action_taken':False})
        print(json.dumps({'read_only_preflight':'PASS',**verification}));return
    fresh=gate();need(fresh['action']=='ELIGIBLE' and fresh['pr']['headRefOid']==HEAD,'Eligibility changed before comment')
    intent_path=A/'CLOSURE_INTENT.json'
    if intent_path.exists():
        intent=json.loads(intent_path.read_text());need(intent['decision_sha256']==args.disposition_sha256 and intent['closure_comment_sha256']==sha(body.encode()),'A different closure intent already exists')
    else:
        intent={'utc':datetime.now(timezone.utc).isoformat(),'pr':932,'problem_id':'30003471','original_head':HEAD,
                **verification,'gate':fresh};save(intent_path,intent)
    since=(datetime.fromisoformat(intent['utc'])-timedelta(seconds=60)).isoformat()
    comments=json.loads(run(['gh','api','repos/AlecKriebel/Math/issues/932/comments?per_page=100&since='+quote(since,safe='')]))
    need(len(comments)<100,'Comment recovery needs pagination; do not post blindly')
    matching=[c for c in comments if c['body']==body];need(len(matching)<=1,'Duplicate matching comments; inspect before continuing')
    if matching:comment=matching[0]
    else:
        request=A/'tmp/closure_comment_request.json';request.parent.mkdir(exist_ok=True);save(request,{'body':body})
        comment=json.loads(run(['gh','api','--method','POST','repos/AlecKriebel/Math/issues/932/comments','--input',str(request)]))
    readback=json.loads(run(['gh','api','repos/AlecKriebel/Math/issues/comments/'+str(comment['id'])]))
    need(readback['body']==body,'Comment exact readback failed')
    comment_receipt={'id':readback['id'],'url':readback['html_url'],'body_sha256':sha(body.encode()),'readback_exact':True}
    save(A/'CLOSURE_COMMENT_RECEIPT.json',comment_receipt)
    final_gate=gate();need(final_gate['action']=='ELIGIBLE','Eligibility changed before closing')
    request=A/'tmp/close_request.json';save(request,{'state':'closed'})
    run(['gh','api','--method','PATCH','repos/AlecKriebel/Math/pulls/932','--input',str(request)])
    result=json.loads(run(['gh','pr','view','932','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,closedAt,mergedAt,url']))
    need(result['state']=='CLOSED' and result['mergedAt'] is None and result['headRefOid']==HEAD,'Closure readback not exact')
    originals()
    receipt={'utc':datetime.now(timezone.utc).isoformat(),'outcome':'closed_without_merge_established_priority','pr':932,'problem_id':'30003471',
             'original_head':HEAD,'closed_pr':result,'comment':comment_receipt,**verification,'original_author_record':'1/5',
             'merge_performed':False,'preprint_or_DOI_or_sheet_entry_created':False,'native_queue_or_state_mutated':False}
    save(A/'CLOSURE_RECEIPT.json',receipt);print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
