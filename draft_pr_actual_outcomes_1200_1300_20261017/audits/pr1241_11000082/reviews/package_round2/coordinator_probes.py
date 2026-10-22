"""Fresh offline coordinator probes. All filesystem mutations are on copies.

The actual coordinator source is executed with ONLY its absolute repository
constant redirected to an isolated copy. Subprocesses are intercepted. The real
reviewed generic kit's run() is exercised with a fake in-memory Zenodo client.
No credentials, API, Git objects/index/ref, or application calls occur.
"""
from pathlib import Path
import argparse, contextlib, copy, datetime, hashlib, importlib.util, io, json
import runpy, shutil, subprocess, sys, types
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parents[1]
REPO=Path('/Users/alec/Documents/Math')
REL=AUDIT.relative_to(REPO)
SOURCE=REPO/'draft_pr_actual_outcomes_1200_1300_20261017/_local/run_pr1241_deposit.py'
WORK=HERE/'scratch_local/coordinator_fixture'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def require(c,m):
    if not c: raise RuntimeError(m)
def write(p,d): p.write_text(json.dumps(d,indent=2)+'\n')

def setup():
    if WORK.exists(): shutil.rmtree(WORK)
    target=WORK/REL;target.mkdir(parents=True)
    freeze=json.loads((HERE/'INPUT_FREEZE.json').read_text())
    for e in freeze['files']:
        dst=target/e['path'];dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(AUDIT/e['path'],dst)
    review=target/'reviews/synthetic_latest';review.mkdir()
    (review/'REPORT.md').write_text('OFFLINE SYNTHETIC CLEAN EVIDENCE ONLY\n')
    write(review/'VERDICT.json',{'status':'CLEAN'})
    shutil.copyfile(HERE/'INPUT_FREEZE.json',review/'INPUT_FREEZE.json')
    p=target/'publication'
    gate={'schema':'math-preprint-final-review-gate-v1','pr':1241,'problem_id':11000082,
          'original_head':'493a764dec034b7b645be76a284c4e6edc0583eb','status':'pass',
          'workflow':{n:sha(p/n) for n in ['prepare_package.py','build_package.py','compile_note.py','verification/verify.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py']},
          'latest_review':{'status':'CLEAN','report':'../reviews/synthetic_latest/REPORT.md','report_sha256':sha(review/'REPORT.md'),'verdict':'../reviews/synthetic_latest/VERDICT.json','verdict_sha256':sha(review/'VERDICT.json'),'input_freeze_sha256':sha(review/'INPUT_FREEZE.json')}}
    for n,k in [('Johnson_Filtration_Multiplicity_Note_v1.0.pdf','pdf_sha256'),('Johnson_Filtration_Multiplicity_Verification_v1.0.zip','verification_zip_sha256'),('zenodo-deposit.json','metadata_sha256'),('manuscript/main.tex','source_sha256')]: gate[k]=sha(p/n)
    write(p/'FINAL_REVIEW_GATE.json',gate);write(p/'STAGE_RECEIPT.json',{'id':77,'state':'ready_to_publish','metadata_normalizations':[]})
    (target/'_local').mkdir(exist_ok=True)
    return target,p,review

spec=importlib.util.spec_from_file_location('readonly_kit_r2',REPO/'zenodo_deposit_tool/zenodo.py')
kit=importlib.util.module_from_spec(spec);spec.loader.exec_module(kit)
exact_source=SOURCE.read_text()
shutil.copyfile(SOURCE,HERE/'REVIEWED_COORDINATOR_READONLY.py')
require(sha(SOURCE)==sha(HERE/'REVIEWED_COORDINATOR_READONLY.py'),'Readonly provenance copy differs')
adapted=exact_source.replace("REPO=Path('/Users/alec/Documents/Math')",'REPO=Path('+repr(str(WORK))+')')
require(adapted!=exact_source,'Path adapter did not match')

def probe(name,mutate=None,normalized=False,action='publish',kit_failure=False,already_published=False):
    a,p,review=setup();live=json.loads((a/'LIVE_PR_PREFLIGHT.json').read_text());events=[];kit_outputs=[]
    if mutate: mutate(a,p,review,live)
    def out(args,**kwargs):
        if args[:3]==['gh','pr','view']:events.append('readonly_live_pr');return json.dumps(live)
        if args[:2]==['git','ls-remote']:events.append('readonly_branch');return live.get('mock_remote',live['headRefOid'])+' refs/heads/'+live['headRefName']+'\n'
        raise RuntimeError('Forbidden check_output '+repr(args))
    def run(args,**kwargs):
        if args[0]=='pdfinfo':return types.SimpleNamespace(returncode=0,stdout='Pages: 6\n',stderr='')
        if args[:2]==['gws','sheets']:
            events.append('readonly_tracker_'+args[2])
            params=json.loads(args[args.index('--params')+1])
            if args[2:4]==['spreadsheets','get']:data={'sheets':[{'properties':{'sheetId':live.get('mock_gid',1254632077),'title':live.get('mock_tab','Math Puzzles')}}]}
            elif args[2:5]==['spreadsheets','values','get']:
                require(params['range']=="'Math Puzzles'!A:D",'Incorrect preflight range')
                data={'values':live.get('mock_rows',[['Original Problem','Solution Chat URL','DOI','Notes']])}
            else:raise RuntimeError('Forbidden tracker write')
            return types.SimpleNamespace(returncode=0,stdout=json.dumps(data),stderr='')
        if len(args)>3 and str(args[2]).endswith('/zenodo_deposit_tool/zenodo.py'):
            events.append('kit_'+args[3]);require(args[3] in {'stage','inspect','publish'},'Unexpected kit action')
            if kit_failure:return types.SimpleNamespace(returncode=1,stdout='',stderr='uncertain mocked outcome')
            meta,files=kit.load_manifest(p/'zenodo-deposit.json')
            if args[3]=='publish':
                require(args[-2:]==['--confirm-id','77'],'Confirm id not exact known draft')
                class Client:
                    submitted=already_published
                    def get(self,record_id):
                        events.append('kit_GET_'+str(record_id));m=copy.deepcopy(meta)
                        if normalized:m['description']=m['description'].replace('\u2019',"'")
                        return {'id':77,'submitted':self.submitted,'metadata':m,'doi':'10.5281/zenodo.77','files':[{'filename':f['name'],'filesize':f['size'],'checksum':'md5:'+f['md5']} for f in files]}
                    def publish(self,record_id):
                        events.append('WOULD_POST_PUBLISH_'+str(record_id));self.submitted=True;return {'id':77,'submitted':True}
                state={'manifest':str((p/'zenodo-deposit.json').resolve()),'environment':'production','id':77}
                with patch.object(kit,'local_state',return_value=(p/'mock-state.json',state)),patch.object(kit,'save_state'),patch.object(kit,'doi_status',return_value={'status':'resolved'}):
                    data=kit.run(argparse.Namespace(command='publish',manifest=p/'zenodo-deposit.json',sandbox=False,confirm_id=77),client=Client())
            else:data={'id':77,'state':'ready_to_publish','metadata_normalizations':[]}
            kit_outputs.append({'id':data.get('id'),'state':data.get('state'),'metadata_normalizations':data.get('metadata_normalizations'),'already_published':data.get('already_published',False),'wanted_description_sha256':hashlib.sha256(meta['description'].encode()).hexdigest(),'normalized_description_sha256':hashlib.sha256(meta['description'].replace('\u2019',"'").encode()).hexdigest()})
            return types.SimpleNamespace(returncode=0,stdout=json.dumps(data),stderr='')
        raise RuntimeError('Forbidden subprocess '+repr(args))
    result={'case':name,'normalized_remote_before_publish':normalized,'events':events}
    try:
        with patch.object(sys,'argv',['copied_coordinator.py',action]),patch.object(subprocess,'check_output',side_effect=out),patch.object(subprocess,'run',side_effect=run),contextlib.redirect_stdout(io.StringIO()):
            exec(compile(adapted,'copied_coordinator.py','exec'),{'__name__':'__main__'})
    except Exception as e:result.update(completed=False,error=type(e).__name__+': '+str(e))
    else:result['completed']=True
    result.update(publish_posts=sum(x.startswith('WOULD_POST') for x in events),publication_receipt=(p/'PUBLICATION_RECEIPT.json').exists(),inspect_receipt_before_publish=(p/'STAGE_INSPECT.json').exists(),kit_outputs=kit_outputs)
    return result

results=[]
results.append(probe('positive_exact_publish_no_inspect_receipt'))
results.append(probe('F01_normalized_description_accepted_by_kit_and_published_before_coordinator_refusal',normalized=True))
results.append(probe('known_published_state_kit_readonly',already_published=True))
results.append(probe('uncertain_kit_failure_stops_no_receipt',kit_failure=True))
for n in ['prepare_package.py','build_package.py','compile_note.py','verification/verify.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py']:
    results.append(probe('workflow_drift_'+n,lambda a,p,r,l,n=n:(p/n).write_text((p/n).read_text()+'\n# copied corruption\n')))
results.append(probe('actually_nonclean_verdict_even_with_updated_digest',lambda a,p,r,l:(write(r/'VERDICT.json',{'status':'CHANGES_REQUIRED'}),write(p/'FINAL_REVIEW_GATE.json',{**json.loads((p/'FINAL_REVIEW_GATE.json').read_text()),'latest_review':{**json.loads((p/'FINAL_REVIEW_GATE.json').read_text())['latest_review'],'verdict_sha256':sha(r/'VERDICT.json')}}))))
for n in ['CURRENT_PR1241_CONTEXT.json','PRIORITY_ADJUDICATION.json','current_edition/PROOF.md','publication/COMPILE_RECEIPT.json','publication/LAYOUT_VERIFICATION.json','submitted/PROOF.md']:
    results.append(probe('latest_frozen_input_drift_'+n,lambda a,p,r,l,n=n:(a/n).write_bytes((a/n).read_bytes()+b' ')))
results.append(probe('kit_drift_in_latest_review_freeze',lambda a,p,r,l:(write(r/'INPUT_FREEZE.json',{**json.loads((r/'INPUT_FREEZE.json').read_text()),'external_readonly_inputs':[{**e,'sha256':'0'*64} if e['path'].endswith('/zenodo.py') else e for e in json.loads((r/'INPUT_FREEZE.json').read_text())['external_readonly_inputs']]}),write(p/'FINAL_REVIEW_GATE.json',{**json.loads((p/'FINAL_REVIEW_GATE.json').read_text()),'latest_review':{**json.loads((p/'FINAL_REVIEW_GATE.json').read_text())['latest_review'],'input_freeze_sha256':sha(r/'INPUT_FREEZE.json')}}))))
for key,value in [('isDraft',False),('state','CLOSED'),('headRefOid','b'*40),('headRefName','other'),('body','outside edit')]:results.append(probe('live_original_drift_'+key,lambda a,p,r,l,key=key,value=value:l.update({key:value})))
results.append(probe('known_local_publication_receipt_blocks_retry',lambda a,p,r,l:write(p/'PUBLICATION_RECEIPT.json',{'id':77})))
for key,value in [('mock_remote','f'*40),('mock_gid',0),('mock_tab','Renamed'),('mock_rows',[['Wrong','headers']]),('mock_rows',[['Original Problem','Solution Chat URL','DOI','Notes'],['11000082']]),('mock_rows',[['Original Problem','Solution Chat URL','DOI','Notes'],['AMR-109-0082']])]:
    results.append(probe('readonly_preflight_refusal_'+key+str(value),lambda a,p,r,l,key=key,value=value:l.update({key:value})))
require(results[0]['completed'] and results[0]['publish_posts']==1,'Positive publish control failed')
require(not results[1]['completed'] and results[1]['publish_posts']==1 and not results[1]['publication_receipt'],'F01 not reproduced')
for e in results[4:]:require(not e['completed'] and e['publish_posts']==0,'Corrupt precondition reached publication '+e['case'])
write(HERE/'COORDINATOR_RESULTS.json',{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'readonly_original_sha256':sha(SOURCE),'source_adapter':'Only absolute REPO constant redirected. All subprocesses intercepted. Kit run() used with in-memory fake client and patched state/DOI persistence. Positive review evidence and pdfinfo structural responses are explicitly synthetic; actual PDF separately recompiled/rendered.','results':results,'finding':'F01: exactness checked after generic kit publication, no mandatory exact inspect preflight. Existing curly apostrophes make the actual reviewed description a real accepted-normalization case.'})
print(json.dumps({'cases':len(results),'finding_reproduced':results[1],'all_other_corruptions_blocked':True},indent=2))
