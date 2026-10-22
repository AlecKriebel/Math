"""Read-only external post-merge verification; own evidence and Git ref only."""
from pathlib import Path
import datetime, hashlib, json, runpy, subprocess
REPO=Path('/Users/alec/Documents/Math')
PROGRAM=Path(__file__).resolve().parents[1]
COMPLETED_BEFORE=[1205,1211,1216,1225,1241,1261,1262,1268]
ELIGIBLE=[1205,1211,1216,1225,1241,1261,1262,1268,1271,1274,1280,1283]
A=PROGRAM/'audits/pr1271_30003042'; P=A/'publication'
def need(value,message):
    if not value: raise RuntimeError(message)
def load(path): return json.loads(path.read_text())
def save(path,obj): path.write_text(json.dumps(obj,indent=2)+'\n')
def main():
    u=runpy.run_path(str(P/'update_pr_publication.py')); git=u['git']
    need(git('branch','--show-current').strip()==b'main','Stay on main')
    gate=load(P/'FINAL_REVIEW_GATE.json'); u['validate_workflow_gate'](gate)
    pub=load(P/'PUBLICATION_RECEIPT.json'); tracker=load(P/'tracker/TRACKER_RECEIPT.json')
    build=load(P/'BUILD_RECEIPT.json'); snapshot=load(A/'SUBMITTED_SNAPSHOT.json')
    files,_,_=u['desired_files'](build,pub,tracker,snapshot)
    need(len(files)==13,'Exactly thirteen final problem/publication files required')
    body=(P/'PR_BODY_FINAL.md').read_text()
    wanted=u['expected_identity'](pub,tracker,files,body)
    receipt=load(P/'PR_BRANCH_RECEIPT.json'); head=u['validate_saved'](receipt,wanted,files)
    need(receipt['body_readback_verified'] and receipt['remote_readback_verified'],'Incomplete branch/body receipt')
    live=json.loads(subprocess.check_output(['gh','pr','view','1271','--repo','AlecKriebel/Math','--json','state,headRefOid,headRefName,mergeCommit,mergedAt,body,url'],text=True))
    need(live['url']=='https://github.com/AlecKriebel/Math/pull/1271' and live['state']=='MERGED' and live['headRefOid']==head and live['headRefName']==u['BRANCH'] and live['body']==body,'Merged PR state/head/body differs')
    merge=live['mergeCommit']['oid']
    git('fetch','--no-auto-maintenance','--no-tags','--no-write-fetch-head','origin',merge)
    git('update-ref','refs/math-audit/1200-1300-20261017/merged-pr1271',merge)
    parents=git('rev-list','--parents','-n','1',merge).decode().split()[1:]
    need(len(parents)==2 and parents[1]==head,'Reviewed head is not expected merge parent')
    checks=[]
    for name,data in files.items():
        actual=git('show',merge+':'+name); need(actual==data,'Merged bytes differ '+name)
        checks.append({'path':name,'bytes':len(actual),'sha256':hashlib.sha256(actual).hexdigest(),'matches':True})
    title=load(P/'zenodo-deposit.json')['metadata']['title']
    t=runpy.run_path(str(P/'append_tracker.py')); t['validate_tracker_receipt'](tracker,pub,title)
    metadata=t['call'](['spreadsheets','get'],{'spreadsheetId':t['SID'],'fields':'sheets.properties'})
    tabs=[s['properties'] for s in metadata.get('sheets',[]) if s.get('properties',{}).get('sheetId')==t['GID']]
    need(len(tabs)==1 and tabs[0].get('title')=='Math Puzzles','Postmerge designated tracker sheet ID/title association differs')
    observed_tab={'sheetId':tabs[0]['sheetId'],'title':tabs[0]['title']}
    full="'"+observed_tab['title'].replace("'","''")+"'!A:D"
    rows=t['call'](['spreadsheets','values','get'],{'spreadsheetId':t['SID'],'range':full,'valueRenderOption':'UNFORMATTED_VALUE'}).get('values',[])
    need(rows and rows[0]==['Original Problem','Solution Chat URL','DOI','Notes'],'Postmerge tracker headers differ')
    matches=[(i+1,row) for i,row in enumerate(rows) if t['row_has_problem_identity'](row,pub)]
    need(len(matches)==1 and matches[0][1]==tracker['row'],'Missing/different/duplicate problem or DOI row')
    number=matches[0][0]
    need(tracker['updatedRange']==f"'Math Puzzles'!A{number}:D{number}",'Postmerge row range differs')
    public=load(P/'PUBLIC_DOWNLOAD_VERIFICATION.json')
    need(public['all_supplied_metadata_exact'] and public['public_record_identity_verified'] and public['doi']==pub['doi'] and public['id']==pub['id'],'Public verification differs')
    need(pub.get('metadata_normalizations')==[],'Publication metadata was normalized')
    doi=pub.get('doi_resolution')
    if not (isinstance(doi,dict) and doi.get('status')=='resolved' and doi.get('http_status')==200):
        inspected=load(P/'DOI_INSPECT.json')
        t['validate_publication_identity'](inspected,title)
        need(inspected['id']==pub['id'] and inspected['doi']==pub['doi'],'DOI inspection identity differs')
        doi=inspected.get('doi_resolution')
    need(isinstance(doi,dict) and doi.get('status')=='resolved' and doi.get('http_status')==200,'DOI has not resolved successfully')
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    save(P/'tracker/POSTMERGE_READBACK.json',{'at_utc':now,'spreadsheetId':t['SID'],'gid':observed_tab['sheetId'],'observed_sheet_properties':observed_tab,'range':tracker['updatedRange'],'values':[matches[0][1]],'readback_verified':True,'matching_problem_rows':1,'uniqueness_identifiers':['canonical DOI URL','bare DOI','numeric problem ID','OWR alias','PR URL']})
    merged={'at_utc':now,'pr':1271,'state':'MERGED','merged_at':live['mergedAt'],'merge_commit':merge,'reviewed_head':head,'parents':parents,'final_body_exact':True,'all13_merged_files_exact':True,'files':checks,'shared_index_modified':False,'checkout_branch':'main','method':'Expected-head merge; immutable merge object fetched into own ref, thirteen exact blobs and unique exact full tracker row checked.'}
    save(P/'MERGE_RECEIPT.json',merged)
    context=u['current_context']()
    disposition={'at_utc':now,'pr':1271,'problem_id':30003042,'outcome':'accepted_current_full_target_result_after_actual_review','doi':pub['doi'],'doi_url':pub['doi_url'],'record_url':pub['record_url'],'tracker_range':tracker['updatedRange'],'merged_at':live['mergedAt'],'merge_commit':merge,'reviewed_head':head,'math_review':context['publication_text']['summary'],'priority_scope':context['publication_text']['priority_statement'],'publication_review':{'final_gate_sha256':hashlib.sha256((P/'FINAL_REVIEW_GATE.json').read_bytes()).hexdigest(),'reviews':[{'reviewer_id':x['reviewer_id'],'status':x['status']} for x in gate['reviews']],'latest_status':gate['latest_review']['status'],'pages':context['expected_pdf_pages'],'archive_members':build['archive_members']},'public_downloads_exact':True,'all_supplied_metadata_exact':True,'doi_resolution':doi,'all13_merged_files_exact':True,'tracker_postmerge_readback_exact':True,'shared_index_modified':False,'completion_estimate_percent':100}
    save(A/'FINAL_DISPOSITION.json',disposition)
    state=load(PROGRAM/'PROGRAM_STATE.json')
    need(state['current_pr']==1271 and state['completed_prs']==COMPLETED_BEFORE and state['eligible_prs']==ELIGIBLE and state['eligible_count']==12 and [x['pr'] for x in state['publications']]==COMPLETED_BEFORE,'Program state no longer matches exact8 prior completions/12 eligible; reconcile before advancement')
    state['publications'].append(disposition); state['completed_prs'].append(1271)
    state.update(current_pr=1274,current_pr_stage='pending_live_full_solution_gate_revalidation',current_pr_completion_estimate_percent=0,completion_estimate_percent=round(100*len(state['completed_prs'])/state['eligible_count']),remaining_current_pr=['Revalidate explicit full original-target outcome and live head','Rigorous mathematics and independent adversaries, extensive priority audit','Preprint package and sequential fresh full-review/fix loop','Zenodo, exact tracker and expected-head merge'])
    save(PROGRAM/'PROGRAM_STATE.json',state)
    text=f'\n{now} — PR1271 COMPLETE100%. Published {pub["doi_url"]}; exact11metadata/two public artifacts, resolved DOI200, tracker {tracker["updatedRange"]}; expected-head merge {merge}, all13 immutable merged blobs/body/parents and unique full row verified. Actual reviewed attribution recorded; no firstness/current-openness claim. {len(state["completed_prs"])} eligible PRs complete; next1274. Program estimate{state["completion_estimate_percent"]}%. Shared checkout/index untouched.\n'
    for path in [PROGRAM/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
        with path.open('a') as stream: stream.write(text)
    print(json.dumps({k:disposition[k] for k in ['pr','doi_url','tracker_range','merge_commit','reviewed_head','all13_merged_files_exact','tracker_postmerge_readback_exact']},indent=2))
if __name__=='__main__':main()
