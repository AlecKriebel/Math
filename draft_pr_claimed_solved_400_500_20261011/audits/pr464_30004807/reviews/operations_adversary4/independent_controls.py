#!/usr/bin/env python3
"""Fresh operations4 models. All fabricated state is private; no real services."""
import argparse,base64,contextlib,copy,hashlib,importlib.util,io,json,os,socket,stat,sys,tempfile,zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
sys.path.insert(0,str(AUDIT/'operations'))
import common as c
import zenodo_pr464 as z
import register_pr464_tracker as t
import integrate_pr464_publication as integ

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path); module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
prepared=load(AUDIT/'operations/check_operations.py','ops4_fixture_constructor')
kit=load(AUDIT.parents[2]/'zenodo_deposit_tool/zenodo.py','ops4_unchanged_kit')
RESULTS=[]
NATIVE_KIT=z.kit_cli

def require(ok,message):
    if not ok:raise RuntimeError(message)

def deny(*a,**k):raise RuntimeError('Real service boundary denied in operations4')
def jwrite(path,value):path.write_bytes(c.json_bytes(value))
def rejected(fn,needle):
    try:fn()
    except RuntimeError as exc:require(needle in str(exc),'Wrong guard: '+str(exc));return str(exc)
    raise RuntimeError('Expected guard absent: '+needle)

def snapshot(root):
    result={}
    for p in sorted(root.rglob('*')):
        key=p.relative_to(root).as_posix();info=p.lstat()
        if p.is_symlink():result[key]=['symlink',os.readlink(p)]
        elif stat.S_ISREG(info.st_mode):result[key]=['file',info.st_size,c.sha(p.read_bytes()),info.st_nlink]
        elif stat.S_ISDIR(info.st_mode):result[key]=['directory']
        else:result[key]=['special',stat.S_IFMT(info.st_mode)]
    return result

def case(name,fn):
    private=HERE/'private_cases';private.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='ops4_',dir=private) as tmp:
        f=prepared.Fixture(Path(tmp).resolve())
        with patch.multiple(c,AUDIT=f.audit,PACKAGE=f.package,REPOSITORY=f.repo),patch.object(t,'AUDIT',f.audit),\
             patch.object(c,'github',deny),patch.object(c,'gws',deny),patch.object(t,'gws',deny),\
             patch.object(c.subprocess,'run',side_effect=deny),patch.object(socket,'create_connection',deny):
            try:
                fn(f);RESULTS.append({'case':name,'passed':True,'real_external_calls':0})
            except Exception as exc:
                RESULTS.append({'case':name,'passed':False,'error':type(exc).__name__+': '+str(exc),'real_external_calls':0})

def unsafe_output(f,runner,name,kind):
    path=f.audit/name;path.unlink(missing_ok=True)
    target=f.repo/'independent-sentinel';target.write_bytes(b'KEEP\x00\xff\n')
    if kind=='symlink':path.symlink_to(target)
    elif kind=='dangling':path.symlink_to(f.repo/'no-target')
    elif kind=='hardlink':os.link(target,path)
    elif kind=='directory':path.mkdir()
    elif kind=='fifo':os.mkfifo(path)
    before=snapshot(f.repo);dispatch=[]
    def called(*a,**k):dispatch.append(a);raise RuntimeError('Unexpected service before output check')
    calls={'stage':lambda:z.run('stage',True),'publish':lambda:z.run('publish',True,123456),'inspect':lambda:z.run('inspect'),
           'tracker_default':lambda:t.run(False),'tracker_apply':lambda:t.run(True),
           'integration_default':lambda:integ.run(False),'integration_apply':lambda:integ.run(True),'integration_reconcile':integ.reconcile}
    with patch.object(c,'live_eligibility',called),patch.object(z,'kit_cli',called),patch.object(c,'confirm_live_publication',called),\
         patch.object(t,'confirm_live_publication',called),patch.object(c,'github',called),patch.object(t,'gws',called):
        rejected(calls[runner],'Unsafe receipt destination')
    require(not dispatch and snapshot(f.repo)==before,'Unsafe destination changed bytes or reached service')

def writer_failure(f,phase):
    name='PR_BODY_CURRENT.md';dest=f.audit/name;dest.write_bytes(b'previous approved text')
    before=snapshot(f.repo)
    if phase=='replace':
        with patch.object(c.os,'replace',side_effect=OSError('local replacement failure')):
            try:c.write_output(name,b'complete new text')
            except OSError:pass
            else:raise RuntimeError('Injected failure absent')
    elif phase=='recheck':
        original=c.output_destination;calls=[]
        def changed(n):
            calls.append(n)
            if len(calls)==2:raise RuntimeError('Unsafe receipt destination: injected second check failure')
            return original(n)
        with patch.object(c,'output_destination',changed):rejected(lambda:c.write_output(name,b'complete new text'),'Unsafe receipt destination')
    else:
        c.write_output(name,b'complete new text\x00\xff');require(dest.read_bytes()==b'complete new text\x00\xff','Ordinary overwrite failed')
        require(not list(f.audit.glob('.pr464-output-*')),'Temporary output leaked');return
    require(snapshot(f.repo)==before,'Failed individual replacement changed bytes or leaked temporary output')

def writer_alias(f,kind):
    name='REVIEW_OWNED.json'
    if kind=='internal':
        (f.audit/'link-parent').symlink_to(f.audit,target_is_directory=True);root=f.audit;name='link-parent/'+name
    elif kind=='root':
        root=f.repo/'alias';root.symlink_to(f.audit,target_is_directory=True)
    elif kind=='ancestor':
        link=f.repo/'ancestor';link.symlink_to(f.audit.parent,target_is_directory=True);root=link/f.audit.name
    elif kind=='dot':root=f.audit/'..'/f.audit.name
    else:root=f.audit;name='../'+name
    before=snapshot(f.repo)
    with patch.object(c,'AUDIT',root):
        rejected(lambda:c.write_output(name,b'complete'), 'Unsafe receipt destination' if kind!='escape' else 'canonical safe relative path')
    require(snapshot(f.repo)==before,'Alias failure changed filesystem')

class FakeZenodo:
    def __init__(self,f,scenario):self.f=f;self.scenario=scenario;self.record=None;self.writes=[];self.published=False;self.get_after_pub=0
    def create(self,metadata):
        self.writes.append('create');self.record={'id':123456,'submitted':False,'metadata':copy.deepcopy(metadata),'files':[],
                                                'links':{'bucket':'https://zenodo.org/fake-bucket','html':'https://zenodo.org/fake-draft'}}
        if self.scenario=='create_response_loss':raise kit.DepositError('Create reached fake service; response lost')
        return copy.deepcopy(self.record)
    def get(self,record_id):
        require(record_id==123456,'Wrong saved draft used')
        if self.published:
            self.get_after_pub+=1
            if self.scenario=='published_get_loss' and self.get_after_pub==1:raise kit.DepositError('Published read response lost')
        return copy.deepcopy(self.record)
    def upload(self,bucket,entry):
        self.writes.append('upload:'+entry['name'])
        self.record['files'].append({'filename':entry['name'],'filesize':entry['size'],'checksum':'md5:'+entry['md5']})
        if self.scenario=='upload_response_loss':raise kit.DepositError('Uploaded response lost')
        return {'id':123456}
    def update(self,record_id,metadata):
        self.writes.append('update');self.record['metadata']=copy.deepcopy(metadata)
        if self.scenario=='metadata_drift':self.record['metadata']['title']+=' changed by fake service'
        return copy.deepcopy(self.record)
    def publish(self,record_id):
        self.writes.append('publish');self.record.update(submitted=True,doi='10.5281/zenodo.123456');self.published=True
        if self.scenario=='publish_response_loss':raise kit.DepositError('Published response lost')
        return copy.deepcopy(self.record)

class PublicReply:
    status=200
    def __init__(self,data):self.buffer=io.BytesIO(data)
    def __enter__(self):return self
    def __exit__(self,*a):return False
    def read(self,n=-1):return self.buffer.read(n)

class PublicModel:
    def __init__(self,f,service,scenario):self.f=f;self.service=service;self.scenario=scenario;self.requests=[]
    def open(self,request,timeout):
        require('Authorization' not in dict(request.header_items()),'Public reader sent credentials')
        url=request.full_url;self.requests.append(url)
        if '/api/records/' in url:
            data=c.json_bytes({'id':123456,'doi':'10.5281/zenodo.123456','metadata':{'title':'OFFLINE FIXTURE ONLY'},
                              'files':[{'key':n} for n in c.UPLOADS]})
        else:
            name=url.split('/files/')[1].split('?')[0];data=(self.f.package/c.UPLOADS[name]).read_bytes()
            if self.scenario=='public_same_length_corruption' and name.endswith('.pdf'):data=bytes([data[0]^1])+data[1:]
            if self.scenario=='public_appended_byte' and name.endswith('.pdf'):data+=b'X'
        return PublicReply(data)

def zenodo_complete(f,scenario):
    # The constructor's minimal title-only metadata is sufficient for its gate tests,
    # but an actual kit invocation needs a complete synthetic publication manifest.
    metadata={'title':'OFFLINE FIXTURE ONLY','description':'<p>Private offline test only.</p>','upload_type':'publication','publication_type':'preprint','creators':[{'name':'OFFLINE MOCK','affiliation':'OFFLINE MOCK'}]}
    jwrite(f.package/'metadata.json',metadata)
    deposit=json.loads((f.package/'deposit.json').read_text());deposit['metadata']=metadata;jwrite(f.package/'deposit.json',deposit);f.seal()
    context=c.validate_gate();service=FakeZenodo(f,scenario);public=PublicModel(f,service,scenario)
    state=f.repo/'kit-state';state.mkdir()
    invocations=[]
    def invoke(args,**kw):
        require(args[1]==str(context['kit']) and args[3]==str(f.package/'deposit.json') and '--sandbox' not in args,'Wrong actual kit command')
        command=args[2];invocations.append(command)
        ns=SimpleNamespace(command=command,manifest=f.package/'deposit.json',sandbox=False,check_doi=False,
                           confirm_id=int(args[args.index('--confirm-id')+1]) if '--confirm-id' in args else None)
        try:value=kit.run(ns,client=service);return SimpleNamespace(returncode=0,stdout=json.dumps(value),stderr='')
        except kit.DepositError as exc:return SimpleNamespace(returncode=1,stdout='',stderr=str(exc))
    with patch.object(c,'live_eligibility',lambda:None),patch.object(z.subprocess,'run',invoke),patch.object(kit,'STATE_DIR',state),\
         patch.object(kit,'doi_status',lambda d:{'status':'not_checked_in_offline_review'}),patch.object(z,'build_opener',lambda *a:public):
        if scenario in {'create_response_loss','upload_response_loss','metadata_drift'}:
            rejected(lambda:z.run('stage',True),'Repository Zenodo kit did not confirm success')
            operation=json.loads((f.audit/'ZENODO_STAGE_OPERATION.json').read_text())
            require(operation['state']=='outcome_unconfirmed','Uncertain stage not durable')
            prior=list(service.writes);rejected(lambda:z.run('stage',True),'prior Zenodo write exists')
            require(service.writes==prior,'Uncertain stage repeated remote writes')
            if scenario=='create_response_loss':
                rejected(lambda:z.run('inspect'),'Repository Zenodo kit did not confirm success')
            else:rejected(lambda:z.run('inspect'),'Repository Zenodo kit did not confirm success')
            require(service.writes==prior,'Read-only inspect wrote remote state');return
        staged=z.run('stage',True);require(staged['state']=='ready_to_publish' and service.writes.count('create')==1,'Stage failed')
        if scenario=='wrong_confirmation':
            prior=list(service.writes);rejected(lambda:z.run('publish',True,123457),'Exact confirmed production draft')
            require(service.writes==prior,'Wrong confirmation wrote remote state');return
        if scenario=='published_get_loss':
            rejected(lambda:z.run('publish',True,123456),'Repository Zenodo kit did not confirm success')
            require(service.writes.count('publish')==1,'Publish repeated')
            prior=list(service.writes);rejected(lambda:z.run('publish',True,123456),'prior Zenodo write exists')
            recovered=z.run('inspect');require(recovered['state']=='published' and service.writes==prior,'Inspect failed recovery or wrote')
        elif scenario in {'public_same_length_corruption','public_appended_byte'}:
            rejected(lambda:z.run('publish',True,123456),'Actual public download differs' if scenario.endswith('corruption') else 'exceeds accepted size')
            require(service.writes.count('publish')==1,'Public failure repeated publish')
            require(not (f.audit/'ZENODO_PUBLIC_FILE_READBACK.json').exists(),'Invalid actual public bytes marked verified')
            prior=list(service.writes);rejected(lambda:z.run('publish',True,123456),'prior Zenodo write exists');require(service.writes==prior,'Public failure retried');return
        else:
            published=z.run('publish',True,123456);require(published['state']=='published','Publication incomplete')
        c.validate_publication(context)
        require(service.writes.count('publish')==1 and len([n for n in service.writes if n.startswith('upload:')])==2,'Wrong write counts')
        before=list(service.writes);z.run('inspect');require(service.writes==before,'Inspect performed a remote write')
        rejected(lambda:z.run('stage',True),'prior Zenodo write exists');rejected(lambda:z.run('publish',True,123456),'prior Zenodo write exists')
        require(service.writes==before,'Durable guard repeated a write')

class GitStore:
    """Native immutable hierarchical tree/blob model, distinct from earlier Reader mocks."""
    def __init__(self,f,scenario):
        self.f=f;self.scenario=scenario;self.main='a'*40;self.branch=c.ORIGINAL;self.commits={};self.trees={};self.blobs={};self.paths={};self.writes=[];self.patches=0;self.main_reads=0
        queue=(prepared.HEADER+f.receipt['selected_queue_row']+'\n').encode();f.receipt['queue_sha256']=c.sha(queue);jwrite(f.audit/'SOURCE_RECEIPT.json',f.receipt);f.seal()
        original={x['path']:(f.audit/'source_snapshot'/x['path']).read_bytes() for x in f.receipt['files']};original[c.QUEUE]=queue
        lines,i,cells,cols=c.queue_row(queue);cells[cols.index('Status')]=' queued ';cells[cols.index('Turns')]=' 0/5 ';lines[i]='|'+'|'.join(cells)+'|\n'
        self.main_files={c.QUEUE:(''.join(lines)+f.receipt['selected_queue_row'].replace(c.PROBLEM+' /','99999999 /')+'\n').encode(),
                         'unrelated/nested/binary.bin':b'keep nested\x00\xff', 'unrelated/normal.txt':b'keep text\n'}
        if scenario=='receipt_conflict':self.main_files[c.PREPRINT+'publication_receipts/SOURCE_RECEIPT.json']=b'conflicting independent main bytes'
        if scenario=='body_ordinary':(f.audit/'PR_BODY_CURRENT.md').write_bytes(b'authorized earlier body')
        self.add_commit(c.ORIGINAL,original,[]);self.add_commit(self.main,self.main_files,[])
    def tree_of(self,files):
        root={}
        for path,data in files.items():
            current=root;parts=path.split('/')
            for part in parts[:-1]:current=current.setdefault(part,{})
            blob=c.git_sha(data);self.blobs[blob]=data;current[parts[-1]]=blob
        def store(node):
            entries=[]
            for name,value in sorted(node.items()):
                entries.append({'path':name,'mode':'040000' if isinstance(value,dict) else '100644','type':'tree' if isinstance(value,dict) else 'blob','sha':store(value) if isinstance(value,dict) else value})
            tree=hashlib.sha1(c.json_bytes(entries)).hexdigest();self.trees[tree]=entries;return tree
        return store(root)
    def add_commit(self,revision,files,parents):
        tree=self.tree_of(files);self.paths[revision]=dict(files);self.commits[revision]={'sha':revision,'tree':{'sha':tree},'parents':[{'sha':p} for p in parents]};return tree
    def api(self,endpoint,payload=None,method=None):
        if payload is not None:self.writes.append(endpoint)
        if endpoint=='pulls/464':return {'number':464,'state':'open','draft':True,'changed_files':14,'head':{'sha':self.branch,'ref':c.BRANCH,'repo':{'full_name':c.REPO}},'base':{'ref':'main','repo':{'full_name':c.REPO}}}
        if endpoint.startswith('pulls/464/files'):return [{'filename':p,'status':'modified' if p==c.QUEUE else 'added'} for p in self.paths[c.ORIGINAL]]
        if endpoint=='git/ref/heads/'+c.BRANCH:return {'object':{'sha':self.branch}}
        if endpoint=='git/ref/heads/main':
            self.main_reads+=1;return {'object':{'sha':'f'*40 if self.scenario=='main_moves' and self.main_reads>1 else self.main}}
        if endpoint.startswith('git/commits/'):return copy.deepcopy(self.commits[endpoint.removeprefix('git/commits/')])
        if endpoint.startswith('git/trees/'):return {'sha':endpoint.removeprefix('git/trees/'),'truncated':False,'tree':copy.deepcopy(self.trees[endpoint.removeprefix('git/trees/')])}
        if endpoint.startswith('git/blobs/'):
            blob=endpoint.removeprefix('git/blobs/');data=self.blobs[blob]
            if self.scenario=='binary_read_corrupt' and hasattr(self,'candidate') and data==self.paths[self.candidate][c.PREPRINT+'manuscript.pdf']:data=bytes([data[0]^1])+data[1:]
            return {'sha':blob,'encoding':'base64','size':len(data),'content':base64.b64encode(data).decode()}
        if endpoint=='git/blobs':
            require(payload['encoding']=='base64','Wrong blob encoding');data=base64.b64decode(payload['content']);blob=c.git_sha(data);self.blobs[blob]=data
            if self.scenario=='head_moves':self.branch='e'*40
            return {'sha':blob}
        if endpoint=='git/trees':
            require(payload['base_tree']==self.commits[self.main]['tree']['sha'],'Tree lost captured main')
            self.new_files=dict(self.main_files)
            for item in payload['tree']:
                require(item['mode']=='100644' and item['type']=='blob','Unsafe creation mode');self.new_files[item['path']]=self.blobs[item['sha']]
            self.new_tree=self.tree_of(self.new_files);return {'sha':self.new_tree}
        if endpoint=='git/commits':
            self.candidate='b'*40;require(payload['tree']==self.new_tree and payload['parents']==[c.ORIGINAL,self.main],'Wrong tree/parents')
            self.add_commit(self.candidate,self.new_files,payload['parents']);return {'sha':self.candidate}
        if endpoint.startswith('compare/'):
            files=[{'filename':p,'status':'modified' if p in self.main_files else 'added'} for p,data in self.new_files.items() if self.main_files.get(p)!=data]
            if self.scenario=='compare_extra':files.append({'filename':'unrelated/deleted-file','status':'removed'})
            return {'base_commit':{'sha':self.main},'merge_base_commit':{'sha':self.main},'files':files}
        if endpoint=='git/refs/heads/'+c.BRANCH:
            self.patches+=1;require(payload=={'sha':self.candidate,'force':False} and method=='PATCH','Wrong patch request')
            saved=json.loads((self.f.audit/'BRANCH_INTEGRATION_OPERATION.json').read_text());require(saved['state']=='ref_update_attempted_once','Missing saved intent')
            if self.scenario=='ref_rejected':raise RuntimeError('Fake service rejects ref without applying')
            self.branch=self.candidate
            if self.scenario=='lost_ref_response':raise RuntimeError('Fake service applied ref but response lost')
            if self.scenario=='timeout_ref_response':raise c.subprocess.TimeoutExpired('fake ref',60)
            if self.scenario=='json_ref_response':raise json.JSONDecodeError('Fake malformed response','',0)
            return {'object':{'sha':self.candidate}}
        raise RuntimeError('Unexpected native mock Git endpoint '+endpoint)

def integration_complete(f,scenario):
    store=GitStore(f,scenario);context,pub=f.publication();values=c.tracker_values(context['metadata'],pub['doi_url'])
    jwrite(f.audit/'TRACKER_APPEND_RECEIPT.json',{'verified':True,'spreadsheet_id':c.SHEET,'sheet_id':c.TAB_ID,'tab':c.TAB,
            'values':values,'doi':pub['doi_url'],'updated_range':"'Math Puzzles'!A2:D2",'unique_doi_row_at_final_snapshot':True})
    checks=[]
    def pub_check(ctx):checks.append('publication');return pub
    def tracker_check(ctx,p):
        checks.append('tracker')
        if scenario=='tracker_drifts' and checks.count('tracker')>1:raise RuntimeError('Actual live tracker record is not exact and unique')
    with patch.object(c,'github',store.api),patch.object(c,'confirm_live_publication',pub_check),patch.object(c,'confirm_live_tracker',tracker_check):
        if scenario=='readonly':
            result=integ.run(False);require(result['state']=='read_only_preflight' and not store.writes,'Default made Git writes');return
        early={'receipt_conflict':'installation destination conflicts'}
        late={'main_moves':'Main advanced','head_moves':'PR identity','binary_read_corrupt':'Git blob content does not match immutable object',
              'compare_extra':'changed-file set differs','tracker_drifts':'Actual live tracker record','ref_rejected':'Branch write outcome unconfirmed'}
        if scenario in early|late:
            rejected(lambda:integ.run(True),(early|late)[scenario]);require(store.patches==(1 if scenario=='ref_rejected' else 0),'Rejected candidate patched branch')
            if scenario in early:require(not store.writes,'Conflict reached object writes')
            else:
                before=list(store.writes);rejected(lambda:integ.run(True),'Prior integration write exists');require(store.writes==before,'Failure blindly retried Git writes')
            return
        result=integ.run(True);require(result['state']=='branch_updated_verified' and store.patches==1,'Integration not verified exactly once')
        installed=store.paths[result['commit_sha']]
        for p,data in store.main_files.items():
            if p!=c.QUEUE:require(installed[p]==data,'Unrelated main bytes changed')
        before=store.main_files[c.QUEUE].splitlines(keepends=True);after=installed[c.QUEUE].splitlines(keepends=True)
        require(len(before)==len(after) and [n for n,(a,b) in enumerate(zip(before,after)) if a!=b]==[1],'Not exactly selected QUEUE row')
        receipt=json.loads((f.audit/'BRANCH_INTEGRATION_RECEIPT.json').read_text())
        for p,spec in receipt['files'].items():require(c.sha(installed[p])==spec['sha256'] and len(installed[p])==spec['bytes'],'Whole-file installed receipt drift')
        require((f.audit/'PR_BODY_CURRENT.md').read_text().find(pub['doi_url'])>=0,'Safe PR body absent/incorrect')
        writes=list(store.writes);rejected(lambda:integ.run(True),'Prior integration write exists');integ.reconcile()
        require(store.writes==writes and store.patches==1,'Read-only recovery repeated remote mutation')


def tracker_complete(f,scenario):
    context,pub=f.publication();values=c.tracker_values(context['metadata'],pub['doi_url']);rows=[['Original Problem','Solution Chat URL','DOI','Notes'],['UNRELATED','','https://doi.org/10.1/unrelated','preserve']];appends=[];reads=[]
    if scenario=='existing_token':
        existing=copy.deepcopy(values[0]);existing[2]=pub['doi_url'].removeprefix('https://doi.org/');rows.append(existing)
    if scenario=='existing_exact':rows.append(copy.deepcopy(values[0]))
    if scenario=='durable_missing':jwrite(f.audit/'TRACKER_APPEND_OPERATION.json',{'state':'append_attempted_once','doi':pub['doi_url'],'values':values})
    def read(name):
        reads.append(name)
        if name.endswith('A:D'):return {'values':copy.deepcopy(rows)}
        number=int(name.split('!A')[1].split(':')[0]);return {'values':copy.deepcopy(rows[number-1:number])}
    def append(action,params,body):
        require(action=='append' and params['spreadsheetId']==c.SHEET and params['valueInputOption']=='RAW' and body['values']==values,'Wrong native intended append')
        saved=json.loads((f.audit/'TRACKER_APPEND_OPERATION.json').read_text());require(saved['state']=='append_attempted_once','No append intent');appends.append(body)
        rows.append(copy.deepcopy(values[0]));target=f"'Math Puzzles'!A{len(rows)}:D{len(rows)}"
        if scenario=='lost_response':raise RuntimeError('fake append response lost')
        if scenario=='timeout_response':raise c.subprocess.TimeoutExpired('fake gws',60)
        if scenario=='malformed_response':return {'updates':{'updatedRows':True,'updatedColumns':4,'updatedCells':4,'updatedRange':target}}
        if scenario=='duplicate_after_append':rows.append(copy.deepcopy(values[0]))
        return {'updates':{'updatedRows':1,'updatedColumns':4,'updatedCells':4,'updatedRange':target}}
    with patch.multiple(t,validate_gate=lambda:context,confirm_live_publication=lambda ctx:pub,live_eligibility=lambda:None,
                        check_sheet=lambda:None,sheet_get=read,gws=append):
        if scenario=='durable_missing':
            before=snapshot(f.repo);rejected(lambda:t.run(True),'row was removed');require(not appends and snapshot(f.repo)==before,'Prior uncertain append repeated or erased');return
        if scenario=='existing_token':
            rejected(lambda:t.run(True),'unique and exact');require(not appends,'Token alias duplicated instead of rejection');return
        if scenario in {'malformed_response','duplicate_after_append'}:
            rejected(lambda:t.run(True),'Unexpected append size' if scenario=='malformed_response' else 'not unique and exact')
            require(len(appends)==1,'Bad response repeated append')
            if scenario=='malformed_response':
                result=t.run(True);require(result['state']=='existing_identical_registration' and len(appends)==1,'Malformed success did not reconcile without write')
            return
        result=t.run(True);require(result['verified'] is True and len(appends)==(0 if scenario=='existing_exact' else 1),'Tracker did not verify once')
        require(rows[1]==['UNRELATED','','https://doi.org/10.1/unrelated','preserve'],'Unrelated row changed')
        prior=len(appends);t.run(False);t.run(True);require(len(appends)==prior,'Verified repeat appended again')
        rows[:]=rows[:2];rejected(lambda:t.run(True),'row was removed');require(len(appends)==prior,'Deleted verified row repeated append')

builder=load(AUDIT/'build_preprint_package.py','ops4_builder')
def builder_fixture(f):
    (f.package/'CURRENT_PUBLICATION_NOTES.md').write_bytes(b'OFFLINE FIXTURE ONLY current note\n')
    (f.package/'review_evidence').mkdir(exist_ok=True)
    witness=f.package/'review_evidence/witness.md';witness.write_bytes(b'OFFLINE FIXTURE ONLY witness\n')
    jwrite(f.package/'REVIEW_EVIDENCE_SELECTION.json',{'positive_explicit_selection':True,'entries':[{'path':'review_evidence/witness.md','sha256':c.sha(witness.read_bytes()),'bytes':witness.stat().st_size}]})
    core=[]
    for name in sorted(f.payloads):
        if name.startswith('verification/'):
            p=f.package/name;core.append({'path':name.removeprefix('verification/'),'sha256':c.sha(p.read_bytes()),'bytes':p.stat().st_size})
    jwrite(f.package/'verification/PUBLIC_OUTPUT_WHITELIST.json',{'positive_whitelist_only':True,'public_files':core})

def invoke_builder(f,freeze=None,root=None,package=None):
    args=['offline-builder']+([] if freeze is None else ['--freeze',str(freeze)])
    with patch.multiple(builder,ROOT=root or f.audit,PACKAGE=package or f.package),patch.object(sys,'argv',args),contextlib.redirect_stdout(io.StringIO()):builder.main()

def builder_boundary(f,name,kind,freeze=False):
    builder_fixture(f);root=f.audit if name=='BRANCH_INSTALL_PLAN.json' or freeze else f.package;p=root/name;p.unlink(missing_ok=True)
    sentinel=f.repo/'builder-sentinel';sentinel.write_bytes(b'KEEP BUILDER\0\xff')
    if kind=='symlink':p.symlink_to(sentinel)
    elif kind=='dangling':p.symlink_to(f.repo/'nonexistent-builder-target')
    elif kind=='hardlink':os.link(sentinel,p)
    elif kind=='directory':p.mkdir()
    elif kind=='fifo':os.mkfifo(p)
    before=snapshot(f.repo)
    rejected(lambda:invoke_builder(f,3 if freeze else None),'Symlink' if kind in {'symlink','dangling'} else 'Never overwrite' if freeze else 'Unsafe existing output')
    require(snapshot(f.repo)==before,'Builder preflight changed any fixture bytes')

def builder_freeze(f,number):
    builder_fixture(f);before=snapshot(f.repo)
    rejected(lambda:invoke_builder(f,number),'Never overwrite' if number==2 else 'Invalid review round')
    require(snapshot(f.repo)==before,'Rejected freeze invalidated current files')

def builder_valid(f,existing):
    builder_fixture(f);older=(f.audit/'PACKAGE_REVIEW_INPUT_2.json').read_bytes()
    if not existing:
        for name in ['SHA256SUMS.json',c.ZIP_NAME,'ARCHIVE_RECEIPT.json','deposit.json']:(f.package/name).unlink(missing_ok=True)
        (f.audit/'BRANCH_INSTALL_PLAN.json').unlink(missing_ok=True)
    invoke_builder(f,3);freeze=json.loads((f.audit/'PACKAGE_REVIEW_INPUT_3.json').read_text())
    require((f.audit/'PACKAGE_REVIEW_INPUT_2.json').read_bytes()==older,'Prior freeze changed')
    for name,spec in freeze['files'].items():require(c.sha((f.package/name).read_bytes())==spec['sha256'] and (f.package/name).stat().st_size==spec['bytes'],'New frozen bytes wrong')
    plan=json.loads((f.audit/'BRANCH_INSTALL_PLAN.json').read_text());names=set()
    for e in plan['entries']:
        path=f.repo/e['local_program_path'];rel=path.relative_to(f.package).as_posix();names.add(rel)
        require(e['repository_destination']==c.PREPRINT+rel and c.sha(path.read_bytes())==e['sha256'] and path.stat().st_size==e['bytes'],'New plan mismatched')
    manifest=json.loads((f.package/'SHA256SUMS.json').read_text())['files']
    with zipfile.ZipFile(f.package/c.ZIP_NAME) as arc:
        require(arc.testzip() is None and len(arc.namelist())==len(set(arc.namelist())) and set(arc.namelist())==set(manifest)|{'SHA256SUMS.json'},'New archive invalid')
        for name,spec in manifest.items():require(arc.read(name)==(f.package/name).read_bytes() and c.sha(arc.read(name))==spec['sha256'] and len(arc.read(name))==spec['bytes'],'New ZIP payload drift')
        require(names==set(arc.namelist())|set(freeze['files']),'New exact union mismatch')
    for name,field in [('SOURCE_RECEIPT.json','source_receipt_sha256'),('MATHEMATICAL_ACCEPTANCE_GATE.json','mathematical_acceptance_gate_sha256'),('BRANCH_INSTALL_PLAN.json','branch_install_plan_sha256')]:require(freeze[field]==c.sha((f.audit/name).read_bytes()),'New freeze crossbinding drift')
    require(not [p for p in f.audit.rglob('*') if p.name.startswith('.pr464-output-') or p.name.startswith('.regular_zas')],'Partial output remains')


def main():
    groups=[(['stage','publish','inspect'],['ZENODO_STAGE_OPERATION.json','ZENODO_PUBLISH_OPERATION.json','ZENODO_STAGE_RECEIPT.json','ZENODO_PUBLISH_RECEIPT.json','ZENODO_PUBLIC_FILE_READBACK.json']),
            (['tracker_default','tracker_apply'],['TRACKER_APPEND_OPERATION.json','TRACKER_APPEND_RECEIPT.json','ZENODO_PUBLIC_FILE_READBACK.json']),
            (['integration_default','integration_apply','integration_reconcile'],['BRANCH_INTEGRATION_PREFLIGHT.json','BRANCH_INTEGRATION_OPERATION.json','BRANCH_INTEGRATION_RECEIPT.json','PR_BODY_CURRENT.md','ZENODO_PUBLIC_FILE_READBACK.json'])]
    for runners,names in groups:
        for runner in runners:
            for name in names:
                for kind in ['symlink','dangling','hardlink','directory','fifo']:case('fresh_output_'+runner+'_'+name+'_'+kind,lambda f,r=runner,n=name,k=kind:unsafe_output(f,r,n,k))
    for phase in ['replace','recheck','valid']:case('fresh_atomic_writer_'+phase,lambda f,p=phase:writer_failure(f,p))
    for kind in ['root','ancestor','internal','dot','escape']:case('fresh_alias_'+kind,lambda f,k=kind:writer_alias(f,k))
    for scenario in ['valid','create_response_loss','upload_response_loss','metadata_drift','wrong_confirmation','publish_response_loss','published_get_loss','public_same_length_corruption','public_appended_byte']:case('fresh_unchanged_kit_wrapper_'+scenario,lambda f,s=scenario:zenodo_complete(f,s))
    for scenario in ['valid','body_ordinary','readonly','lost_ref_response','timeout_ref_response','json_ref_response','receipt_conflict','main_moves','head_moves','binary_read_corrupt','compare_extra','tracker_drifts','ref_rejected']:case('fresh_native_hierarchical_git_'+scenario,lambda f,s=scenario:integration_complete(f,s))
    for scenario in ['valid','existing_exact','existing_token','durable_missing','lost_response','timeout_response','malformed_response','duplicate_after_append']:case('fresh_tracker_temporal_'+scenario,lambda f,s=scenario:tracker_complete(f,s))
    for name in ['SHA256SUMS.json',c.ZIP_NAME,'ARCHIVE_RECEIPT.json','deposit.json','BRANCH_INSTALL_PLAN.json']:
        for kind in ['symlink','dangling','hardlink','directory','fifo']:case('fresh_builder_output_'+name+'_'+kind,lambda f,n=name,k=kind:builder_boundary(f,n,k))
    for kind in ['symlink','dangling','hardlink','directory','fifo']:case('fresh_builder_new_freeze_'+kind,lambda f,k=kind:builder_boundary(f,'PACKAGE_REVIEW_INPUT_3.json',k,True))
    for number in [2,0,-1]:case('fresh_builder_immutable_freeze_'+str(number),lambda f,n=number:builder_freeze(f,n))
    for existing in [False,True]:case('fresh_builder_complete_existing_'+str(existing),lambda f,e=existing:builder_valid(f,e))
    summary={'reviewer':'/root/pr464_operations_adversary4','case_count':len(RESULTS),'passed_count':sum(x['passed'] for x in RESULTS),'failed_count':sum(not x['passed'] for x in RESULTS),'all_passed':all(x['passed'] for x in RESULTS),'real_external_calls':0,'cases':RESULTS}
    suffix='NORMAL' if __debug__ else 'OPTIMIZED';(HERE/('INDEPENDENT_CONTROLS_'+suffix+'.json')).write_bytes(c.json_bytes(summary));print(json.dumps({k:summary[k] for k in ['case_count','passed_count','failed_count','all_passed','real_external_calls']},sort_keys=True))
    for row in RESULTS:
        if not row['passed']:print(json.dumps(row,sort_keys=True))
if __name__=='__main__':main()
