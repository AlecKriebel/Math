#!/usr/bin/env python3
"""Independent actual-code probes. Transport, gates, Git and services are mocked."""
import argparse,copy,hashlib,importlib.util,json,pathlib,tempfile,types
H=pathlib.Path(__file__).resolve().parent;A=H.parent.parent;P=A/'publication';PROGRAM=A.parents[1]
def load(p):
    s=importlib.util.spec_from_file_location('round4_probe_'+p.stem,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def need(v,m):
    if not v:raise RuntimeError(m)
def rejected(fn,errors):
    try:fn()
    except errors:return True
    raise RuntimeError('Invalid control accepted')
def repair_probes(root):
    suite=load(A/'reviews/draft_repair_tooling/offline_fault_checks.py');out=[]
    for case in ['inspect_old','already_new','delete_no_effect','delete_removes_PDF','delete_adds_extra','release_drift_after_DELETE','PDF_changed_after_PUT','metadata_changed_after_PUT','ZIP_changed_after_PUT','GET_failure_at_start']:
        f=suite.fixture(root/case);orig=f.client.request
        if case=='already_new':
            f.remote['files'][1].update(filesize=next(x['size'] for x in f.new if x['name']==f.r.ZIP),checksum=next(x['md5'] for x in f.new if x['name']==f.r.ZIP),id='11520f81-19a5-4096-a690-5c0acbfcf324')
        if case=='GET_failure_at_start':f.state['lose_read']=True
        def request(method,url,payload=None,file=None,accept='application/json'):
            if case=='delete_no_effect' and method=='DELETE':f.events.append('DELETE');return {'success_but_no_effect':True}
            r=orig(method,url,payload,file,accept)
            if method=='DELETE':
                if case=='delete_removes_PDF':f.remote['files']=[]
                elif case=='delete_adds_extra':f.remote['files'].append({'filename':'foreign','filesize':1,'checksum':'0'*32})
                elif case=='release_drift_after_DELETE':f.c.authenticate_release=lambda:(_ for _ in ()).throw(RuntimeError('Synthetic release drift'))
            if method=='PUT':
                if case=='PDF_changed_after_PUT':f.remote['files'][0]['id']='11520f81-19a5-4096-a690-5c0acbfcf325'
                elif case=='metadata_changed_after_PUT':f.remote['metadata']['description']+=' changed'
                elif case=='ZIP_changed_after_PUT':f.remote['files'][1]['checksum']='0'*32
            return r
        f.client.request=request
        if case=='inspect_old':
            result=suite.call(f,'inspect');need(result['status']=='recovery_required','old inspect recovery')
        elif case=='already_new':need(suite.call(f)['status']=='ready_to_publish','new package stage')
        elif case=='ZIP_changed_after_PUT':need(suite.call(f)['status']=='recovery_required','bad new ZIP no stage')
        else:rejected(lambda:suite.call(f),f.errors)
        d=f.events.count('DELETE');u=f.events.count('PUT')
        if case in ['inspect_old','already_new','GET_failure_at_start']:need(d==u==0,'read-only scenario mutation')
        elif case in ['PDF_changed_after_PUT','metadata_changed_after_PUT','ZIP_changed_after_PUT']:need(d==u==1,'one mutation each')
        else:need(d==1 and u==0,'bad deletion state uploaded')
        if case!='already_new':need(not (f.p/'STAGE_RECEIPT.json').exists(),'invalid stage receipt')
        out.append(dict(case=case,DELETE=d,PUT=u,stage_receipt=(f.p/'STAGE_RECEIPT.json').exists()))
    return out
def actual_publish_fields(root):
    root.mkdir(parents=True)
    c=load(PROGRAM/'publication_coordinators/pr1262.py');kit=c.load_exact_kit();kit.STATE_DIR=root/'kit-state';meta,files=kit.load_manifest(P/'zenodo-deposit.json');out=[]
    manifest=(P/'zenodo-deposit.json').resolve();place,_=kit.local_state(manifest,'production');kit.save_state(place,dict(manifest=str(manifest),environment='production',id=23443230))
    for field in sorted(meta):
        events=[];remote=dict(id=23443230,submitted=False,metadata=copy.deepcopy(meta),files=[dict(filename=f['name'],filesize=f['size'],checksum=f['md5']) for f in files])
        remote['metadata'][field]=None
        class Client:
            def get(self,n):need(n==23443230,'same ID');events.append('GET');return copy.deepcopy(remote)
            def publish(self,n):events.append('POST publish');raise RuntimeError('Forbidden POST reached')
        args=argparse.Namespace(command='publish',manifest=manifest,sandbox=False,confirm_id=23443230,check_doi=False)
        rejected(lambda:kit.run(args,client=Client()),(kit.DepositError,));need(events==['GET'],'metadata corrupt before actual kit publish POST')
        out.append(field)
    return out
def postmerge(root):
    m=load(PROGRAM/'publication_coordinators/verify_pr1262_merge.py');names=sorted([str(x.relative_to(A/'current_edition')) for x in (A/'current_edition').iterdir()]);base='unsolved_math_prioritization/attempts/30001248';files={base+'/'+n:(A/'current_edition'/n).read_bytes() for n in names}
    for n in ['Triangle_Modular_Threshold_Note_v1.0.pdf','Triangle_Modular_Threshold_Verification_v1.0.zip','zenodo-deposit.json']:files[base+'/publication_20261017/'+n]=(P/n).read_bytes()
    files[base+'/publication_20261017/PUBLICATION_RECEIPT.json']=b'SYNTHETIC MOCK PUBLICATION';files[base+'/publication_20261017/README.md']=b'SYNTHETIC MOCK README';need(len(files)==13,'actual 8 + 5')
    head='a'*40;merge='b'*40;parent='c'*40;body='SYNTHETIC REVIEWED FINAL BODY';row=['Problem 30001248','','https://doi.org/10.5281/zenodo.23443230','Synthetic notes'];mode={'case':None};out=[]
    pub=dict(id=23443230,doi='10.5281/zenodo.23443230',doi_url=row[2],record_url='https://zenodo.org/records/23443230',metadata_normalizations=[],doi_resolution=dict(status='resolved',http_status=200))
    tracker=dict(row=row,updatedRange="'Math Puzzles'!A2:D2")
    gate=dict(reviews=[],latest_review=dict(status='CLEAN'))
    context=dict(title='Synthetic',publication_text=dict(summary='Synthetic',priority_statement='Synthetic'),expected_pdf_pages=5)
    def git(*args,**kw):
        if args[0]=='branch':return b'main\n'
        if args[0] in ['fetch','update-ref']:return b''
        if args[0]=='rev-list':return (merge+' '+parent+' '+('d'*40 if mode['case']=='parent' else head)+'\n').encode()
        if args[0]=='show':
            name=args[1].split(':',1)[1];return b'CORRUPTED' if mode['case']=='blob_'+name else files[name]
        raise RuntimeError('Unexpected mocked Git '+repr(args))
    u=dict(git=git,validate_workflow_gate=lambda g:None,desired_files=lambda *args:(files,{},''),expected_identity=lambda *args:{},validate_saved=lambda *args:head,BRANCH='synthetic-branch',current_context=lambda:context)
    def call(*args,**kw):
        rows=[['Original Problem','Solution Chat URL','DOI','Notes'],row]
        if mode['case']=='row_blank_B':rows[1]=[row[0],'not blank',row[2],row[3]]
        if mode['case']=='duplicate_row':rows.append(row)
        return dict(values=rows)
    t=dict(validate_tracker_receipt=lambda *args:None,validate_publication_identity=lambda *args:None,call=call,SID='synthetic',GID=1)
    def live(*args,**kw):return json.dumps(dict(state='MERGED',headRefOid=head,headRefName=u['BRANCH'],body='wrong' if mode['case']=='body' else body,mergeCommit=dict(oid=merge),mergedAt='2026-10-17T23:00:00Z')).encode()
    m.runpy=types.SimpleNamespace(run_path=lambda path:u if path.endswith('update_pr_publication.py') else t);m.subprocess=types.SimpleNamespace(check_output=live)
    for case in ['valid']+['blob_'+n for n in files]+['parent','body','duplicate_row','row_blank_B','DOI_not_200']:
        mode['case']=case;m.PROGRAM=root/case.replace('/','_');m.A=m.PROGRAM/'audit';m.P=m.A/'publication';m.P.mkdir(parents=True);(m.P/'PR_BODY_FINAL.md').write_text(body);(m.P/'FINAL_REVIEW_GATE.json').write_text('{"synthetic_fixture_only":true}\n')
        for p in [m.PROGRAM/'RESEARCH_LOG.md',m.A/'RESEARCH_LOG.md']:p.write_text('Synthetic probe log\n')
        outputs={}
        def read(path):
            name=path.name
            if name=='FINAL_REVIEW_GATE.json':return gate
            if name=='PUBLICATION_RECEIPT.json':return {**pub,'doi_resolution':dict(status='resolved',http_status=201)} if case=='DOI_not_200' else pub
            if name=='DOI_INSPECT.json':return {**pub,'doi_resolution':dict(status='resolved',http_status=201)}
            if name=='TRACKER_RECEIPT.json':return tracker
            if name=='BUILD_RECEIPT.json':return dict(archive_members=203)
            if name=='SUBMITTED_SNAPSHOT.json':return {}
            if name=='PR_BRANCH_RECEIPT.json':return dict(body_readback_verified=True,remote_readback_verified=True)
            if name=='PUBLIC_DOWNLOAD_VERIFICATION.json':return dict(all_supplied_metadata_exact=True,public_record_identity_verified=True,doi=pub['doi'],id=pub['id'])
            if name=='zenodo-deposit.json':return dict(metadata=dict(title='Synthetic'))
            if name=='PROGRAM_STATE.json':return dict(current_pr=1262,completed_prs=[],publications=[],eligible_count=1)
            raise RuntimeError('Unexpected mocked input '+str(path))
        m.load=read;m.save=lambda path,obj:outputs.update({path.name:obj})
        if case=='valid':m.main();need('FINAL_DISPOSITION.json' in outputs and len(outputs['MERGE_RECEIPT.json']['files'])==13,'full postmerge result')
        else:rejected(m.main,(RuntimeError,));need('FINAL_DISPOSITION.json' not in outputs,'failed postmerge promoted')
        out.append(case)
    return out
def main():
    with tempfile.TemporaryDirectory(prefix='round4-extra-',dir=H/'_local') as d:
        r=pathlib.Path(d);j=dict(status='PASS',repair=repair_probes(r/'repair'),all11_actual_kit_publish_POST_fields=actual_publish_fields(r/'publish'),actual_postmerge=postmerge(r/'postmerge'),scope='Actual repair, strict kit publish path and postmerge main executed; all gates/services/transport/Git mocked, synthetic helper returns identified, own scratch only.')
    (H/'ADDITIONAL_CONTROLS.json').write_text(json.dumps(j,indent=2)+'\n')
if __name__=='__main__':main()
