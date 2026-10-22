#!/usr/bin/env python3
"""Offline guard regressions: no Git/network/application mutations permitted."""
from pathlib import Path
import copy,datetime,hashlib,importlib.util,json,subprocess,sys,tempfile,types
ROOT=Path(__file__).resolve().parent

def load(name):
    spec=importlib.util.spec_from_file_location('offline_'+name.replace('/','_'),ROOT/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def need(c,m):
    if not c:raise RuntimeError(m)

def prepare_context_controls():
    p=load('prepare_package');rejected=[]
    with tempfile.TemporaryDirectory(prefix='pr1241-context-guards-') as tmp:
        audit=Path(tmp);p.AUDIT=audit;registry=[]
        for raw,(base,entries_key,path_key) in p.MINIMUM_FREEZES.items():
            path=audit/raw;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps({entries_key:[{path_key:'payload.md','bytes':1,'sha256':'0'*64}]}));registry.append({'path':raw,'base':base,'entries_key':entries_key,'path_key':path_key,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        context={'schema':'math-pr1241-current-context-v1','pr':1241,'problem_id':11000082,'original_head':p.ORIGINAL,'title':p.TITLE,'edition_text':{n:'Explicit fixture prose' for n in ['PROOF.md','AUDIT.md','README.md','ACCEPTANCE.md']},'acceptance':{'fixture':True},'sources':{'fixture':True},'verification':{'fixture':True},'authored_freezes':registry}
        priority={'novelty_clearance':False,'firstness_claim':False,'current_openness_claim':False,'new_existence_claim':False,'matching_publication_doi':p.MATCHING_DOI}
        cp=audit/'CURRENT_PR1241_CONTEXT.json';pp=audit/'PRIORITY_ADJUDICATION.json';mp=audit/'MATH_GATE.json';math_gate={'pr':1241,'problem_id':11000082,'original_head':p.ORIGINAL,'status':'PASS_fixture'}
        def restore():cp.write_text(json.dumps(context));pp.write_text(json.dumps(priority));mp.write_text(json.dumps(math_gate))
        restore();p.load_context()
        for key in ['missing_context','missing_priority','wrong_context_schema','wrong_context_pr','wrong_context_problem','wrong_context_head','wrong_context_title','missing_prose','extra_prose','empty_structured_record','missing_novelty_disclaimer','firstness_claim','wrong_matching_doi','wrong_math_gate','missing_required_freeze','wrong_freeze_schema','changed_freeze_anchor','duplicate_freeze','escaped_freeze_base']:
            restore();x=copy.deepcopy(context);y=copy.deepcopy(priority)
            if key=='missing_context':cp.unlink()
            elif key=='missing_priority':pp.unlink()
            elif key.startswith('wrong_context'):
                field={'schema':'schema','pr':'pr','problem':'problem_id','head':'original_head','title':'title'}[key[len('wrong_context_'):]];x[field]='wrong'
            elif key=='missing_prose':x['edition_text'].pop('PROOF.md')
            elif key=='extra_prose':x['edition_text']['OTHER.md']='wrong'
            elif key=='empty_structured_record':x['verification']={}
            elif key=='missing_novelty_disclaimer':y.pop('novelty_clearance')
            elif key=='firstness_claim':y['firstness_claim']=True
            elif key=='wrong_matching_doi':y['matching_publication_doi']='10.5281/zenodo.999'
            elif key=='wrong_math_gate':mp.write_text(json.dumps({**math_gate,'status':'PENDING'}))
            elif key=='missing_required_freeze':x['authored_freezes'].pop()
            elif key=='wrong_freeze_schema':x['authored_freezes'][0]['entries_key']='files'
            elif key=='changed_freeze_anchor':x['authored_freezes'][0]['sha256']='0'*64
            elif key=='duplicate_freeze':x['authored_freezes'].append(copy.deepcopy(x['authored_freezes'][0]))
            else:x['authored_freezes'][0]['base']='../../outside'
            if key!='missing_context':cp.write_text(json.dumps(x))
            if key!='missing_priority':pp.write_text(json.dumps(y))
            try:p.load_context()
            except (RuntimeError,FileNotFoundError):rejected.append(key)
            else:raise RuntimeError('Bad pre-authoring current context accepted '+key)
    return rejected

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
        if key.startswith('cell'):x['row'][int(key[-1])]='wrong11000082' if key=='cell0' else 'wrong'
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
        gate={'schema':'math-preprint-final-review-gate-v1','pr':int(u.NUMBER),'problem_id':11000082,'original_head':u.ORIGINAL,'status':'pass','workflow':{n:u.digest(root/n) for n in u.REQUIRED_WORKFLOW},'latest_review':{'status':'CLEAN','report':'../reviews/r3/REPORT.md','report_sha256':u.digest(review/'REPORT.md'),'verdict':'../reviews/r3/VERDICT.json','verdict_sha256':u.digest(review/'VERDICT.json')}}
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
        b.ROOT=root;b.pdf_pages=lambda path:7;(root.parent/'CURRENT_PR1241_CONTEXT.json').write_text(json.dumps({'expected_pdf_pages':7}));(root.parent/'PRIORITY_ADJUDICATION.json').write_text('{}');(root/'manuscript').mkdir(exist_ok=True);(root/'output/pdf').mkdir(parents=True);source=root/'manuscript/main.tex';pdf=root/'output/pdf/main.pdf';source.write_bytes(b'source v1');pdf.write_bytes(b'%PDF-fixture v1')
        compiled={'returncode':0,'source_date_epoch':'1792267200','source_sha256':b.binding(source)['sha256'],'pdf_sha256':b.binding(pdf)['sha256']};layout={**compiled,'status':'pass','pages':b.expected_pdf_pages(),'all_pages_visually_inspected':True,'page_indices_inspected':list(range(1,b.expected_pdf_pages()+1))}
        cp=root/'COMPILE_RECEIPT.json';lp=root/'LAYOUT_VERIFICATION.json'
        def restore():source.write_bytes(b'source v1');pdf.write_bytes(b'%PDF-fixture v1');cp.write_text(json.dumps(compiled));lp.write_text(json.dumps(layout))
        restore();b.document_bindings();baddoc=[]
        for key in ['stale_source','stale_pdf','missing_compile','missing_layout','wrong_build_stamp','failed_compile','wrong_compile_source','wrong_compile_pdf','wrong_layout_source','wrong_layout_pdf','wrong_pages','partial_visual_qa']:
            restore()
            if key=='stale_source':source.write_bytes(b'source v2')
            elif key=='stale_pdf':pdf.write_bytes(b'%PDF-fixture v2')
            elif key=='missing_compile':cp.unlink()
            elif key=='missing_layout':lp.unlink()
            elif key=='wrong_build_stamp':cp.write_text(json.dumps({**compiled,'source_date_epoch':'0'}))
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
        # Each real custom schema is exercised. Omitted-source inventories are
        # ordinary receipts and are deliberately absent from the registry.
        archive=root/'archive';archive.mkdir();registry=[];nested_schema_controls=[]
        for index,(entries_key,path_key) in enumerate([('entries','file'),('files','path'),('authored_files','path'),('all_authored_content_files','path_relative_to_authored_root')]):
            folder=archive/'priority'/('fixture'+str(index));folder.mkdir(parents=True);payload=folder/'CROSS.md';payload.write_bytes(b'frozen challenge');entry={path_key:'CROSS.md','bytes':len(payload.read_bytes()),'sha256':hashlib.sha256(payload.read_bytes()).hexdigest()};freeze=folder/'FREEZE_MANIFEST.json';freeze.write_text(json.dumps({entries_key:[entry]}));registry.append({'path':freeze.relative_to(archive).as_posix(),'base':folder.relative_to(archive).as_posix(),'entries_key':entries_key,'path_key':path_key,'sha256':hashlib.sha256(freeze.read_bytes()).hexdigest()})
        (archive/'RAW_SOURCE_INVENTORY.json').write_text(json.dumps({'files':[{'path':'omitted.pdf','bytes':100,'sha256':'0'*64}]}))
        need(len(v.authenticate_nested_manifests(archive,registry,require_complete=False))==4,'custom nested positive failed')
        for index,item in enumerate(registry):
            payload=archive/item['base']/'CROSS.md';payload.write_bytes(b'changed challenge');(archive/'MANIFEST.json').write_text(json.dumps({'files':[{'path':str(payload.relative_to(archive)),'bytes':len(payload.read_bytes()),'sha256':hashlib.sha256(payload.read_bytes()).hexdigest()}]}))
            try:v.authenticate_nested_manifests(archive,registry,require_complete=False)
            except ValueError:nested_schema_controls.append([item['entries_key'],item['path_key']])
            else:raise RuntimeError('Changed freeze escaped custom nested verification')
            payload.write_bytes(b'frozen challenge')
        nested_rejected=len(nested_schema_controls)==4
        bad_registry=copy.deepcopy(registry);bad_registry[0]['sha256']='0'*64
        try:v.authenticate_nested_manifests(archive,bad_registry,require_complete=False)
        except ValueError:pass
        else:raise RuntimeError('Changed outside freeze anchor accepted')
        bad_registry=copy.deepcopy(registry);bad_registry[0]['base']='../../outside'
        try:v.authenticate_nested_manifests(archive,bad_registry,require_complete=False)
        except ValueError:pass
        else:raise RuntimeError('Escaped registry base accepted')
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
    return {'canonical_publication_controls':badpub,'full_tracker_row_and_range_controls':badrow,'complete_review_gate_controls':badgate,'stale_document_controls':baddoc,'coupled_outer_change_nested_freeze_rejected':nested_rejected,'custom_nested_schemas':nested_schema_controls,'outside_freeze_anchor_and_base_escape_rejected':True,'omitted_raw_inventory_treated_as_receipt_only':True,'renamed_tracker_complete_main_zero_appends':True,'body_edit_readback_idempotence_lost_response_and_unknown_body':'PASS','scope':'Pure fixtures/mocks; document test checks hash/QA coupling, not real PDF rendering. No Git/network/application operation.'}

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
    meta_path=ROOT/'zenodo-deposit.json'
    if meta_path.exists():
        wanted_meta=json.loads(meta_path.read_text())['metadata'];metadata_scope='actual current local deposit metadata, compared offline'
    else:
        # Pure pre-authoring fixture; this is not a real paper/deposit metadata record.
        wanted_meta={'title':'Offline reviewed title fixture','upload_type':'publication','publication_type':'preprint','description':'Offline fixture','creators':[{'name':'Fixture author'}],'access_right':'open','license':'cc-by-4.0','version':'1.0','publication_date':'2026-10-17','keywords':['fixture'],'related_identifiers':[{'identifier':'10.5281/zenodo.23301731','relation':'references','scheme':'doi'}]};metadata_scope='11-field offline fixture only; real deposit metadata does not yet exist'

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
    return {'status':'PASS','explicit_current_context_controls':prepare_context_controls(),'additional_guards':additional_guards(),'valid_saved_identity_and_tree':True,'stale_saved_or_tree_controls_rejected':rejected,'metadata_fixture_scope':metadata_scope,'all_public_metadata_fields_exact_fixture':fields,'each_supplied_public_metadata_field_corruption_rejected':sorted(rejected_meta),'scope':'Tests saved-identity validator and full metadata projection with offline fixtures, not a live GitHub/Zenodo/GWS integration test. Publication main guards receive an additional independent whole-package review. No actual Git, network or application call is allowed.'}

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
