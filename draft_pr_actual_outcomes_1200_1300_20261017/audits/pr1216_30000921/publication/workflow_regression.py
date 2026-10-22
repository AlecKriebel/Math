#!/usr/bin/env python3
"""Offline guard regressions: no Git/network/application mutations permitted."""
from pathlib import Path
import copy,datetime,hashlib,importlib.util,json,subprocess,sys,tempfile,types
ROOT=Path(__file__).resolve().parent

def load(name):
    spec=importlib.util.spec_from_file_location('offline_'+name.replace('/','_'),ROOT/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def need(c,m):
    if not c:raise RuntimeError(m)

def additional_guards():
    u=load('update_pr_publication');t=load('append_tracker');b=load('build_package');v=load('verification/verify')
    pub={'environment':'production','state':'published','metadata_normalizations':[],'id':123,'doi':'10.5281/zenodo.123','doi_url':'https://doi.org/10.5281/zenodo.123','record_url':'https://zenodo.org/records/123','url':'https://doi.org/10.5281/zenodo.123','title':'Reviewed title'}
    t.validate_publication_identity(pub,pub['title']);badpub=[]
    for key,value in [('id',True),('doi','10.5281/zenodo.999'),('doi_url','https://doi.org/10.5281/zenodo.999'),('record_url','https://zenodo.org/records/999'),('url','https://example.com'),('title','Wrong title'),('environment','sandbox'),('state','draft'),('metadata_normalizations',[{'field':'description'}])]:
        x=copy.deepcopy(pub);x[key]=value
        try:t.validate_publication_identity(x,pub['title'])
        except RuntimeError:badpub.append(key)
        else:raise RuntimeError('Bad production publication identity accepted '+key)
    tracker={'spreadsheetId':t.SID,'gid':t.GID,'row':t.expected_row(pub,pub['title']),'updatedRange':"'Math Puzzles'!A999:D999",'readback_verified':True}
    t.validate_tracker_receipt(tracker,pub,pub['title']);badrow=[]
    for key in ['cell0','cell1','cell2','cell3','wrong_tab','multirow','wrong_columns','header_row','wrong_gid','wrong_sid','unverified']:
        x=copy.deepcopy(tracker)
        if key.startswith('cell'):x['row'][int(key[-1])]='wrong30000921' if key=='cell0' else 'wrong'
        elif key=='wrong_tab':x['updatedRange']="'Other tab'!A999:D999"
        elif key=='multirow':x['updatedRange']="'Math Puzzles'!A999:D1000"
        elif key=='wrong_columns':x['updatedRange']="'Math Puzzles'!A999:C999"
        elif key=='header_row':x['updatedRange']="'Math Puzzles'!A1:D1"
        elif key=='wrong_gid':x['gid']=1
        elif key=='wrong_sid':x['spreadsheetId']='wrong'
        else:x['readback_verified']=False
        try:t.validate_tracker_receipt(x,pub,pub['title'])
        except RuntimeError:badrow.append(key)
        else:raise RuntimeError('Bad full tracker receipt accepted '+key)
    with tempfile.TemporaryDirectory(prefix='publication-guard-fixtures-') as tmp:
        root=Path(tmp)/'publication';root.mkdir();u.ROOT=root
        # Complete append main must reject a renamed designated gid before writes.
        tracker_root=Path(tmp)/'tracker-main';tracker_root.mkdir();t.ROOT=tracker_root
        (tracker_root/'PUBLICATION_RECEIPT.json').write_text(json.dumps(pub));(tracker_root/'zenodo-deposit.json').write_text(json.dumps({'metadata':{'title':pub['title']}}));append_calls=[]
        def renamed_call(parts,params,body=None):
            if parts==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':t.GID,'title':'Renamed Math Puzzles'}}]}
            if parts==['spreadsheets','values','append']:append_calls.append(body);raise RuntimeError('unexpected append after rename')
            raise RuntimeError('unexpected call before rename refusal '+repr(parts))
        t.call=renamed_call
        try:t.main()
        except RuntimeError as error:need(str(error)=='Tracker tab title changed; reconcile before append','rename test failed at wrong precondition')
        else:raise RuntimeError('Renamed tracker unexpectedly completed')
        need(append_calls==[],'Renamed tracker was mutated before rejection')
        for n in u.REQUIRED_WORKFLOW:
            f=root/n;f.parent.mkdir(parents=True,exist_ok=True);f.write_text('fixture workflow '+n)
        review=Path(tmp)/'reviews/r3';review.mkdir(parents=True);(review/'REPORT.md').write_text('clean fixture report');(review/'VERDICT.json').write_text('{"status":"CLEAN"}')
        gate={'schema':'math-preprint-final-review-gate-v1','pr':int(u.NUMBER),'problem_id':30000921,'original_head':u.ORIGINAL,'status':'pass','workflow':{n:u.digest(root/n) for n in u.REQUIRED_WORKFLOW},'latest_review':{'status':'CLEAN','report':'../reviews/r3/REPORT.md','report_sha256':u.digest(review/'REPORT.md'),'verdict':'../reviews/r3/VERDICT.json','verdict_sha256':u.digest(review/'VERDICT.json')}}
        u.validate_workflow_gate(gate);badgate=[]
        for key in ['empty_coverage','missing_script','extra_equivalent_script','wrong_script_digest','wrong_schema','wrong_pr','wrong_problem','wrong_head','nonclean_latest','report_digest','outside_report','actual_nonclean_verdict']:
            x=copy.deepcopy(gate)
            if key=='empty_coverage':x['workflow']={}
            elif key=='missing_script':x['workflow'].pop('append_tracker.py')
            elif key=='extra_equivalent_script':x['workflow']['./append_tracker.py']=x['workflow']['append_tracker.py']
            elif key=='wrong_script_digest':x['workflow']['append_tracker.py']='0'*64
            elif key=='wrong_schema':x['schema']='wrong'
            elif key=='wrong_pr':x['pr']=1
            elif key=='wrong_problem':x['problem_id']=1
            elif key=='wrong_head':x['original_head']='0'*40
            elif key=='nonclean_latest':x['latest_review']['status']='CHANGES_REQUIRED'
            elif key=='report_digest':x['latest_review']['report_sha256']='0'*64
            elif key=='outside_report':x['latest_review']['report']='../../outside.md'
            else:(review/'VERDICT.json').write_text('{"status":"CHANGES_REQUIRED"}');x['latest_review']['verdict_sha256']=u.digest(review/'VERDICT.json')
            try:u.validate_workflow_gate(x)
            except (RuntimeError,FileNotFoundError):badgate.append(key)
            else:raise RuntimeError('Bad review coverage/evidence accepted '+key)
            (review/'VERDICT.json').write_text('{"status":"CLEAN"}')
        # Source/PDF fixtures exercise byte coupling only; no fake rendering is claimed.
        b.ROOT=root;(root/'manuscript').mkdir(exist_ok=True);(root/'output/pdf').mkdir(parents=True);source=root/'manuscript/main.tex';pdf=root/'output/pdf/main.pdf';source.write_bytes(b'source v1');pdf.write_bytes(b'%PDF-fixture v1')
        compiled={'returncode':0,'source_sha256':b.binding(source)['sha256'],'pdf_sha256':b.binding(pdf)['sha256']};layout={**compiled,'status':'pass','pages':4,'all_pages_visually_inspected':True,'page_indices_inspected':[1,2,3,4]}
        cp=root/'COMPILE_RECEIPT.json';lp=root/'LAYOUT_VERIFICATION.json'
        def restore():source.write_bytes(b'source v1');pdf.write_bytes(b'%PDF-fixture v1');cp.write_text(json.dumps(compiled));lp.write_text(json.dumps(layout))
        restore();b.document_bindings();baddoc=[]
        for key in ['stale_source','stale_pdf','missing_compile','missing_layout','failed_compile','wrong_compile_source','wrong_compile_pdf','wrong_layout_source','wrong_layout_pdf','wrong_pages','partial_visual_qa']:
            restore()
            if key=='stale_source':source.write_bytes(b'source v2')
            elif key=='stale_pdf':pdf.write_bytes(b'%PDF-fixture v2')
            elif key=='missing_compile':cp.unlink()
            elif key=='missing_layout':lp.unlink()
            elif key.startswith('wrong_compile') or key=='failed_compile':
                x=copy.deepcopy(compiled);x['returncode' if key=='failed_compile' else 'source_sha256' if key.endswith('source') else 'pdf_sha256']=1 if key=='failed_compile' else '0'*64;cp.write_text(json.dumps(x))
            else:
                x=copy.deepcopy(layout)
                if key=='wrong_pages':x['pages']=1;x['page_indices_inspected']=[1]
                elif key=='partial_visual_qa':x['all_pages_visually_inspected']=False
                else:x['source_sha256' if key.endswith('source') else 'pdf_sha256']='0'*64
                lp.write_text(json.dumps(x))
            try:b.document_bindings()
            except (RuntimeError,FileNotFoundError):baddoc.append(key)
            else:raise RuntimeError('Stale/missing document assurance accepted '+key)
        # A coupled outer-manifest change must not hide a stale nested freeze.
        archive=root/'archive';nested=archive/'priority/independent/cross_freeze';nested.mkdir(parents=True);payload=nested/'CROSS.md';payload.write_bytes(b'frozen challenge');entry={'path':'CROSS.md','bytes':len(payload.read_bytes()),'sha256':hashlib.sha256(payload.read_bytes()).hexdigest()};(nested/'MANIFEST.json').write_text(json.dumps({'files':[entry]}));(archive/'MANIFEST.json').write_text('{"files":[]}');need(len(v.authenticate_nested_manifests(archive))==1,'nested positive failed');payload.write_bytes(b'changed challenge');(archive/'MANIFEST.json').write_text(json.dumps({'files':[{'path':'priority/independent/cross_freeze/CROSS.md','bytes':len(payload.read_bytes()),'sha256':hashlib.sha256(payload.read_bytes()).hexdigest()}]}))
        try:v.authenticate_nested_manifests(archive)
        except ValueError:nested_rejected=True
        else:raise RuntimeError('Changed cross-freeze escaped nested verification')
        # Full body step is mocked, including accepted write with lost response.
        state={'headRefOid':'a'*40,'headRefName':u.BRANCH,'state':'OPEN','body':'original body'};body='reviewed final body';(root/'PR_BODY_FINAL.md').write_text(body);(root/'FINAL_REVIEW_GATE.json').write_text('{}');calls=[];fail_once={'value':False}
        u.pr=lambda:copy.deepcopy(state)
        def body_git(*args,data=None):
            need(args==('ls-remote','origin','refs/heads/'+u.BRANCH),'body test unexpected Git operation');return (state['headRefOid']+' refs/heads/'+u.BRANCH+'\n').encode()
        u.git=body_git
        def edit(args,**kwargs):
            need(args[:3]==['gh','pr','edit'],'body test unexpected external command');calls.append(args);state['body']=body
            return types.SimpleNamespace(returncode=1 if fail_once['value'] else 0,stderr='simulated lost response' if fail_once['value'] else '',stdout='')
        u.subprocess=types.SimpleNamespace(run=edit);original=hashlib.sha256(b'original body').hexdigest()
        need(u.synchronize_pr_body('a'*40,body,original)['body_readback_verified'],'body readback failed');u.synchronize_pr_body('a'*40,body,original);need(len(calls)==1,'body idempotent retry wrote twice')
        state['body']='outside change'
        try:u.synchronize_pr_body('a'*40,body,original)
        except RuntimeError:pass
        else:raise RuntimeError('Unknown third-party body overwritten')
        state['body']='original body';fail_once['value']=True
        try:u.synchronize_pr_body('a'*40,body,original)
        except RuntimeError:pass
        else:raise RuntimeError('Lost body response falsely completed')
        fail_once['value']=False;u.synchronize_pr_body('a'*40,body,original);need(len(calls)==2,'lost-response recovery repeated idempotent body write')
    return {'canonical_publication_controls':badpub,'full_tracker_row_and_range_controls':badrow,'complete_review_gate_controls':badgate,'stale_document_controls':baddoc,'coupled_outer_change_nested_freeze_rejected':nested_rejected,'renamed_tracker_complete_main_zero_appends':True,'body_edit_readback_idempotence_lost_response_and_unknown_body':'PASS','scope':'Pure fixtures/mocks; document test checks hash/QA coupling, not real PDF rendering. No Git/network/application operation.'}

def worker():
    m=load('update_pr_publication');metadata=load('check_public_downloads')
    # The identity validator is exercised directly; its Git reads are synthetic,
    # and any call outside these read-only commands fails the test immediately.
    files={m.BASE+'/fixture-'+str(n):('reviewed-bytes-'+str(n)).encode() for n in range(13)}
    commit='a'*40;mode={'tree':'valid'};calls=[]
    def fake_git(*args,data=None):
        calls.append(args)
        if args[0]=='rev-list':return (commit+' '+('b'*40 if mode['tree']=='parent' else m.ORIGINAL)+'\n').encode()
        if args[0]=='diff-tree':return ('\n'.join(sorted(files)+( ['foreign/path'] if mode['tree']=='paths' else []))+'\n').encode()
        if args[0]=='show':
            ref,path=args[1].split(':',1);need(ref==commit,'unexpected test commit')
            return b'wrong' if mode['tree']=='bytes' else files[path]
        raise RuntimeError('Unexpected Git operation; offline test permits only mocked tree reads: '+repr(args))
    m.git=fake_git;m.digest=lambda p:hashlib.sha256(('current:'+p.name).encode()).hexdigest()
    wanted=m.expected_identity({'doi':'10.5281/zenodo.123','doi_url':'https://doi.org/10.5281/zenodo.123','record_url':'https://zenodo.org/records/123','id':123},{'updatedRange':"'Math Puzzles'!A999:D999"},files,'reviewed body')
    saved={**copy.deepcopy(wanted),'commit':commit}
    need(m.validate_saved(saved,wanted,files)==commit,'valid saved identity rejected')
    rejected=[]
    for key in ['pr','base','branch','paths','files','review_gate_sha256','metadata_sha256','doi','doi_url','record_url','deposit_id','tracker_range','tracker_receipt_sha256','public_verification_receipt_sha256','body_sha256','shared_index_modified']:
        bad=copy.deepcopy(saved)
        if key=='paths':bad[key].append('foreign/path')
        elif key=='files':bad[key][sorted(files)[0]]['sha256']='0'*64
        elif isinstance(bad[key],bool):bad[key]=not bad[key]
        elif isinstance(bad[key],int):bad[key]+=1
        else:bad[key]='stale:'+str(bad[key])
        try:m.validate_saved(bad,wanted,files)
        except RuntimeError:rejected.append(key)
        else:raise RuntimeError('Stale saved identity accepted at '+key)
    for kind in ['parent','paths','bytes']:
        mode['tree']=kind
        try:m.validate_saved(saved,wanted,files)
        except RuntimeError:rejected.append('actual_tree_'+kind)
        else:raise RuntimeError('Changed actual commit accepted: '+kind)
    mode['tree']='valid'
    bad={**saved,'commit':'not-a-commit'}
    try:m.validate_saved(bad,wanted,files)
    except RuntimeError:rejected.append('invalid_commit')
    else:raise RuntimeError('Invalid commit syntax accepted')
    wanted_meta=json.loads((ROOT/'zenodo-deposit.json').read_text())['metadata']
    public=copy.deepcopy(wanted_meta)
    public['resource_type']={'type':public.pop('upload_type'),'subtype':public.pop('publication_type'),'title':'Preprint'}
    public['license']={'id':public['license']};public['doi']='10.5281/zenodo.generated';public['relations']={'generated':True}
    fields=metadata.verify_public_metadata(public,wanted_meta);need(fields==sorted(wanted_meta),'not all supplied fields checked')
    rejected_meta=[]
    for key in wanted_meta:
        bad=copy.deepcopy(public)
        if key=='upload_type':bad['resource_type']['type']='wrong'
        elif key=='publication_type':bad['resource_type']['subtype']='wrong'
        elif key=='license':bad['license']['id']='wrong'
        else:bad[key]=None
        try:metadata.verify_public_metadata(bad,wanted_meta)
        except RuntimeError:rejected_meta.append(key)
        else:raise RuntimeError('Changed supplied public metadata accepted: '+key)
    return {'status':'PASS','additional_guards':additional_guards(),'valid_saved_identity_and_tree':True,'stale_saved_or_tree_controls_rejected':rejected,'all_public_metadata_fields_exact_fixture':fields,'each_supplied_public_metadata_field_corruption_rejected':sorted(rejected_meta),'scope':'Tests saved-identity validator and full metadata projection with offline fixtures, not a live GitHub/Zenodo/GWS integration test. Publication main guards receive an additional independent whole-package review. No actual Git, network or application call is allowed.'}

def main():
    if '--worker' in sys.argv:print(json.dumps(worker(),sort_keys=True));return
    runs=[]
    for flags in [[],['-O'],['-OO']]:
        r=subprocess.run([sys.executable,'-B',*flags,str(Path(__file__).resolve()),'--worker'],capture_output=True,text=True)
        need(r.returncode==0,r.stderr);runs.append({'flags':flags,'result':json.loads(r.stdout)})
    need(all(x['result']==runs[0]['result'] for x in runs),'mode-dependent regressions')
    receipt={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':runs,'all_modes_identical':True,'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'repaired_workflow_sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['prepare_package.py','build_package.py','compile_note.py','verification/verify.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py']}}
    (ROOT/'WORKFLOW_REGRESSION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
