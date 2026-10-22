"""Offline actual-kit and actual-postmerge probes. All writes stay in own scratch."""
from pathlib import Path
import argparse, contextlib, copy, importlib.util, io, json, os, tempfile, types
R=Path(__file__).resolve().parent; A=R.parents[1]; P=A/'publication'; REPO=A.parents[2]
def load(path):
    spec=importlib.util.spec_from_file_location('review_'+path.stem+'_'+str(id(path)),path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def save(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def require(value,msg):
    if not value:raise RuntimeError(msg)
def reject(fn,label):
    try:fn()
    except (RuntimeError,ValueError,KeyError):return label
    raise RuntimeError('Unexpected acceptance: '+label)

def actual_kit_checks(scratch):
    kit=load(REPO/'zenodo_deposit_tool/zenodo.py');c=load(A.parents[1]/'publication_coordinators/pr1262.py')
    c.install_exact_verifier(kit);kit.STATE_DIR=scratch/'kit_state';kit.doi_status=lambda _: {'status':'resolved','http_status':200}
    manifest=P/'zenodo-deposit.json';metadata,files=kit.load_manifest(manifest)
    place=kit.state_path(manifest,'production');kit.save_state(place,{'manifest':str(manifest),'environment':'production','id':123})
    clean={'id':123,'submitted':False,'metadata':copy.deepcopy(metadata),'files':[{'filename':f['name'],'filesize':f['size'],'checksum':f['md5']} for f in files]}
    class Client:
        def __init__(self,remote):self.remote=remote;self.events=[]
        def get(self,id):self.events.append('GET');return copy.deepcopy(self.remote)
        def publish(self,id):self.events.append('POST');self.remote['submitted']=True;self.remote['doi']='10.5281/zenodo.123'
    args=argparse.Namespace(command='publish',manifest=manifest,sandbox=False,confirm_id=123,check_doi=False)
    rejected=[]
    for field in metadata:
        remote=copy.deepcopy(clean);remote['metadata'][field]=None;client=Client(remote)
        try:kit.run(args,client=client)
        except kit.DepositError:rejected.append(field)
        else:raise RuntimeError('Metadata corruption accepted '+field)
        require(client.events==['GET'],'corruption reached publish POST')
    for field,value in [('id',124),('submitted','false')]:
        remote=copy.deepcopy(clean);remote[field]=value;client=Client(remote)
        try:kit.run(args,client=client)
        except kit.DepositError:pass
        else:raise RuntimeError('Identity/state corruption accepted')
        require('POST' not in client.events,'bad identity POST')
    client=Client(copy.deepcopy(clean));first=kit.run(args,client=client);second=kit.run(args,client=client)
    require(first['state']=='published' and second['already_published'] and client.events.count('POST')==1,'same-ID idempotence')
    # Directly show the actual wrapper refuses the generic kit's narrow permitted transform.
    plain=copy.deepcopy(metadata);plain['description']='A & B';remote=copy.deepcopy(clean);remote['metadata']=copy.deepcopy(plain);remote['metadata']['description']='A &amp; B'
    try:kit.verify(remote,plain,files)
    except kit.DepositError:normalization_rejected=True
    else:raise RuntimeError('Generic normalization reached PR1262 strict adapter')
    return {'actual_local_metadata_11_fields_rejected_before_POST':rejected,'wrong_ID_and_nonboolean_state_rejected_before_POST':True,'actual_kit_run_GET_POST_and_published_recovery':client.events,'generic_normalization_refused_by_actual_adapter':normalization_rejected,'services':'All actual shared-kit network client methods mocked.'}

def postmerge_checks(scratch):
    w=load(P/'workflow_regression.py');w.REPORT_ROOT=scratch
    f=w.fixture(scratch/'fixture');pub=f['pub'];audit=f['audit'];u=w.load(pub/'update_pr_publication.py')
    p,t,_=w.publication_and_tracker_controls(f);p['doi_resolution']={'status':'resolved','http_status':200};save(pub/'PUBLICATION_RECEIPT.json',p)
    files,_,note=u.desired_files(f['build'],p,t,f['snapshot']);body=note+'\nFinal synthetic fixture body.\n';(pub/'PR_BODY_FINAL.md').write_text(body)
    wanted=u.expected_identity(p,t,files,body);head='a'*40;merge='b'*40;parent='c'*40
    save(pub/'PR_BRANCH_RECEIPT.json',{**wanted,'commit':head,'body_readback_verified':True,'remote_readback_verified':True})
    live={'state':'MERGED','headRefOid':head,'headRefName':u.BRANCH,'body':body,'mergeCommit':{'oid':merge},'mergedAt':'2026-10-17T22:00:00Z','url':'https://fixture.invalid'}
    m=w.load(A.parents[1]/'publication_coordinators/verify_pr1262_merge.py');m.P=pub;m.A=audit;m.PROGRAM=audit.parents[1]
    tracker=w.load(pub/'append_tracker.py');mode={'bad':None};events=[]
    def git(*args,data=None):
        events.append(list(args))
        if args==('branch','--show-current'):return b'main\n'
        if args[0]=='rev-list':
            if args[-1]==head:return (head+' '+u.ORIGINAL+'\n').encode()
            parents=[parent,head] if mode['bad']!='parents' else [parent,'d'*40]
            return (merge+' '+' '.join(parents)+'\n').encode()
        if args[0]=='diff-tree':return ('\n'.join(files)+'\n').encode()
        if args[0]=='show':return b'wrong' if mode['bad']=='merged_blob' and args[1].startswith(merge+':') else files[args[1].split(':',1)[1]]
        if args[0] in {'fetch','update-ref'}:return b''
        raise RuntimeError('Unexpected Git request')
    u.git=git
    def call(parts,params,body=None):
        require(parts==['spreadsheets','values','get'],'unmocked tracker action')
        rows=[['Original Problem','Solution Chat URL','DOI','Notes'],t['row']]
        if mode['bad']=='duplicate_tracker':rows.append(t['row'])
        return {'values':rows}
    tracker.call=call
    m.runpy=types.SimpleNamespace(run_path=lambda path:u.__dict__ if Path(path).name=='update_pr_publication.py' else tracker.__dict__)
    def gh(*args,**kwargs):
        obj=copy.deepcopy(live)
        if mode['bad']=='state':obj['state']='OPEN'
        if mode['bad']=='head':obj['headRefOid']='d'*40
        if mode['bad']=='body':obj['body']='wrong'
        return json.dumps(obj)
    m.subprocess=types.SimpleNamespace(check_output=gh)
    def run():
        save(m.PROGRAM/'PROGRAM_STATE.json',{'current_pr':1262,'completed_prs':[],'publications':[],'eligible_count':2})
        with contextlib.redirect_stdout(io.StringIO()):m.main()
    run();require(json.loads((audit/'FINAL_DISPOSITION.json').read_text())['all13_merged_files_exact'],'complete postmerge fixture')
    rejected=[]
    for bad in ['state','head','body','parents','merged_blob','duplicate_tracker']:
        mode['bad']=bad;rejected.append(reject(run,bad))
    mode['bad']=None
    receipt=pub/'PUBLIC_DOWNLOAD_VERIFICATION.json';old=receipt.read_bytes();obj=json.loads(old);obj['all_supplied_metadata_exact']=False;save(receipt,obj);rejected.append(reject(run,'public_metadata_false'));receipt.write_bytes(old)
    old=(pub/'PUBLICATION_RECEIPT.json').read_bytes();obj=json.loads(old);obj['doi_resolution']={'status':'not_resolved','http_status':404};save(pub/'PUBLICATION_RECEIPT.json',obj)
    # Rebind the prospective commit fixture to this deliberately unresolved receipt.
    files2,_,_=u.desired_files(f['build'],obj,t,f['snapshot']);files.clear();files.update(files2)
    wanted=u.expected_identity(obj,t,files,body);save(pub/'PR_BRANCH_RECEIPT.json',{**wanted,'commit':head,'body_readback_verified':True,'remote_readback_verified':True})
    save(pub/'DOI_INSPECT.json',{**obj,'doi_resolution':{'status':'not_resolved','http_status':404}})
    rejected.append(reject(run,'DOI_unresolved'))
    return {'actual_postmerge_main_executed_with_mocks':True,'all13_exact_merge_blob_check_executed':True,'adversarial_rejections':rejected,'Git_service_compiler_calls':'Mocked; only own temporary fixture files and logs written.','no_actual_publication_or_approval':True}

with tempfile.TemporaryDirectory(prefix='independent-',dir=R/'_local') as temp:
    s=Path(temp);out={'actual_shared_kit':actual_kit_checks(s),'actual_postmerge':postmerge_checks(s)}
print(json.dumps(out,indent=2))
