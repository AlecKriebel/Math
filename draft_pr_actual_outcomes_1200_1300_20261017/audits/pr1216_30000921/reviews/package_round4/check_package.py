#!/usr/bin/env python3
"""Round 4: review-copy artifact checks and fully offline entrypoint exercises."""
from pathlib import Path
import contextlib, copy, datetime, hashlib, importlib.util, io, json, shutil, subprocess, sys, types, zipfile

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
PUB=BASE/'publication'
FIX=HERE/'fixtures'
RESULT={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def need(c,m):
    if not c:raise RuntimeError(m)
def quiet(f):
    with contextlib.redirect_stdout(io.StringIO()) as s:f()
    return s.getvalue()
def load(name,root=PUB):
    spec=importlib.util.spec_from_file_location('r4_'+name.replace('/','_'),root/(name+'.py'))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def fails(f,label):
    try:quiet(f)
    except (RuntimeError,ValueError,FileNotFoundError,KeyError,StopIteration) as e:return {'case':label,'error':str(e)}
    raise RuntimeError('Expected refusal: '+label)
def fixture(name):
    root=FIX/name
    if root.exists():shutil.rmtree(root)
    root.mkdir()
    for directory in ['submitted','current_edition','priority']:
        shutil.copytree(BASE/directory,root/directory,ignore=shutil.ignore_patterns('sources','_local','__pycache__'))
    (root/'reviews').mkdir()
    for directory in ['source_question_family','analytic_source_adversary','annular_baire_adversary','nikula_corollary_adversary']:
        shutil.copytree(BASE/'reviews'/directory,root/'reviews'/directory,ignore=shutil.ignore_patterns('sources','_local','__pycache__'))
    for p in BASE.iterdir():
        if p.is_file() and p.suffix in {'.json','.md','.py'}:shutil.copyfile(p,root/p.name)
    shutil.copytree(PUB,root/'publication',ignore=shutil.ignore_patterns('__pycache__','FIRST_REVIEW_FIXES*','SECOND_REVIEW_FIXES*','THIRD_REVIEW_FIXES*'))
    return root/'publication'

def artifacts():
    build=json.loads((PUB/'BUILD_RECEIPT.json').read_text())
    checks={k:{'path':build[k]['path'],'bytes':(PUB/build[k]['path']).stat().st_size,'sha256':sha(PUB/build[k]['path'])} for k in ['pdf','verification_zip']}
    for k,x in checks.items():need(x==build[k],'build binding '+k)
    need((PUB/'output/pdf/main.pdf').read_bytes()==(PUB/build['pdf']['path']).read_bytes(),'PDF release mismatch')
    local=FIX/'zip_replay';local.mkdir(exist_ok=True)
    with zipfile.ZipFile(PUB/build['verification_zip']['path']) as z:
        need(len(z.namelist())==len(set(z.namelist()))==build['archive_members'],'ZIP inventory')
        for name in z.namelist():
            need(z.read(name)==(PUB/'verification'/name).read_bytes(),'ZIP source drift '+name)
        z.extractall(local)
    runs=[]
    for flags in [[],['-O'],['-OO']]:
        r=subprocess.run([sys.executable,'-B',*flags,str(local/'verify.py')],capture_output=True,text=True)
        need(r.returncode==0,r.stderr);o=json.loads(r.stdout);need(o==build['verification_run'],'saved replay differs');runs.append({'flags':flags,'result':o})
    # Corruption of each kind is applied to the archive copy, never reviewed files.
    rejected=[]
    for label,path in [('payload','current_edition/PROOF.md'),('nested_manifest','priority/independent/cross_freeze_20261017T183513Z/MANIFEST.json'),('source_freeze','reviews/source_question_family/freeze_20261017T182054Z/REPORT.md')]:
        p=local/path;old=p.read_bytes();p.write_bytes(old+b'\ncorrupt')
        r=subprocess.run([sys.executable,'-B',str(local/'verify.py')],capture_output=True,text=True);need(r.returncode!=0,'corruption passed '+label);rejected.append(label);p.write_bytes(old)
    extra=local/'unlisted.txt';extra.write_text('stale');r=subprocess.run([sys.executable,'-B',str(local/'verify.py')],capture_output=True,text=True);need(r.returncode!=0,'unlisted passed');extra.unlink();rejected.append('unlisted')
    RESULT['artifacts']={'checks':checks,'source_sha256':sha(PUB/'manuscript/main.tex'),'metadata_sha256':sha(PUB/'zenodo-deposit.json'),'verify_modes':runs,'negative_controls_rejected':rejected}

def build_and_prepare():
    root=fixture('build')
    b=load('build_package',root)
    quiet(b.main)
    need((root/'BUILD_RECEIPT.json').read_bytes()==(PUB/'BUILD_RECEIPT.json').read_bytes(),'rebuild receipt differs')
    need((root/'Polynomial_Multipliers_Verification_v1.0.zip').read_bytes()==(PUB/'Polynomial_Multipliers_Verification_v1.0.zip').read_bytes(),'rebuild ZIP differs')
    # Actual build entrypoint rejects ordinary stale/missing/corrupt document inputs.
    refused=[]
    for path,change in [('manuscript/main.tex',b'\n% source changed'),('output/pdf/main.pdf',b'\nchanged'),('COMPILE_RECEIPT.json',None),('LAYOUT_VERIFICATION.json',None)]:
        p=root/path;old=p.read_bytes()
        if change is None:p.unlink()
        else:p.write_bytes(old+change)
        refused.append(fails(b.main,path));p.write_bytes(old)
    p=root/'LAYOUT_VERIFICATION.json';old=p.read_bytes();x=json.loads(old);x['all_pages_visually_inspected']=False;save(p,x);refused.append(fails(b.main,'partial layout QA'));p.write_bytes(old)
    RESULT['build_prepare_main']={'deterministic_exact_rebuild':True,'refusals':refused}

def compile_mock():
    root=fixture('compile');m=load('compile_note',root)
    compiler=root/'mock-tectonic';compiler.write_bytes(b'compiler fixture')
    m.shutil=types.SimpleNamespace(which=lambda _:str(compiler))
    def compile_call(args,**kw):
        need(args[0]==str(compiler),'unexpected compiler command')
        (root/'output/pdf/main.pdf').write_bytes(b'%PDF-mocked-compiled')
        return types.SimpleNamespace(returncode=0,stdout='mocked compiler',stderr='')
    m.subprocess=types.SimpleNamespace(check_output=lambda *a,**kw:'Tectonic MOCK',run=compile_call)
    quiet(m.main);receipt=json.loads((root/'COMPILE_RECEIPT.json').read_text());need(receipt['source_sha256']==sha(root/'manuscript/main.tex'),'mock compile source binding');need(receipt['pdf_sha256']==sha(root/'output/pdf/main.pdf'),'mock compile PDF binding')
    def drifting(*a,**kw):
        p=root/'manuscript/main.tex';p.write_bytes(p.read_bytes()+b'\nchanged during compile');return types.SimpleNamespace(returncode=0,stdout='',stderr='')
    m.subprocess.run=drifting
    refusal=fails(m.main,'source changed during compile')
    RESULT['compile_main']={'mock_success_source_pdf_coupling':True,'refusal':refusal,'limit':'Compiler process mocked; this is not a new real compilation.'}

def pub_fixture(root):
    build=json.loads((root/'BUILD_RECEIPT.json').read_text());meta=json.loads((root/'zenodo-deposit.json').read_text())['metadata']
    pub={'environment':'production','state':'published','metadata_normalizations':[],'id':123456,'doi':'10.5281/zenodo.123456','doi_url':'https://doi.org/10.5281/zenodo.123456','record_url':'https://zenodo.org/records/123456','url':'https://doi.org/10.5281/zenodo.123456','title':meta['title'],'files':[{'name':build[k]['path'],'size':build[k]['bytes'],'sha256':build[k]['sha256']} for k in ['pdf','verification_zip']]}
    save(root/'PUBLICATION_RECEIPT.json',pub)
    return pub,meta,build

def tracker_main():
    root=fixture('tracker');m=load('append_tracker',root);pub,meta,_=pub_fixture(root);row=m.expected_row(pub,meta['title']);header=['Original Problem','Solution Chat URL','DOI','Notes'];state={'rows':[header],'appends':0,'lost':False,'badheader':False,'renamed':False}
    def fake(parts,params,body=None):
        if parts==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':m.GID,'title':'Other' if state['renamed'] else 'Math Puzzles'}}]}
        if parts==['spreadsheets','values','get']:
            if params['range']=="'Math Puzzles'!A:D":return {'values':[['wrong']] if state['badheader'] else copy.deepcopy(state['rows'])}
            return {'values':[copy.deepcopy(state['rows'][-1])]}
        if parts==['spreadsheets','values','append']:
            state['appends']+=1;state['rows'].append(copy.deepcopy(body['values'][0]))
            if state['lost']:raise RuntimeError('simulated lost append response')
            return {'updates':{'updatedRows':1,'updatedColumns':4,'updatedRange':"'Math Puzzles'!A2:D2"}}
        raise RuntimeError('Unmocked GWS call '+repr(parts))
    m.call=fake
    for key in ['badheader','renamed']:
        state[key]=True;fails(m.main,key);state[key]=False
    need(state['appends']==0,'tracker mutated before refusal')
    quiet(m.main);quiet(m.main);need(state['appends']==1,'duplicate append')
    shutil.rmtree(root/'tracker');state['rows']=[header];state['lost']=True;fails(m.main,'lost append response');need(state['appends']==2,'lost response not exercised');state['lost']=False;quiet(m.main);need(state['appends']==2,'append repeated after loss')
    state['rows'].append(copy.deepcopy(row));fails(m.main,'duplicate existing DOI rows');state['rows'].pop();state['rows'][-1][1]='must remain blank';fails(m.main,'existing mismatched problem row')
    RESULT['tracker_main']={'first_append_and_idempotent_retry':True,'lost_response_reconciled_without_reappend':True,'badheader_renamed_duplicate_mismatched_rejected':True,'all_GWS_operations_mocked':True}

def public_main():
    root=fixture('public');m=load('check_public_downloads',root);pub,meta,build=pub_fixture(root)
    publicmeta=copy.deepcopy(meta);publicmeta['resource_type']={'type':publicmeta.pop('upload_type'),'subtype':publicmeta.pop('publication_type')};publicmeta['license']={'id':publicmeta['license']};publicmeta['doi']=pub['doi']
    actual={'id':pub['id'],'doi':pub['doi'],'metadata':publicmeta,'files':[{'key':build[k]['path'],'links':{'self':'https://zenodo.org/api/records/123456/files/'+build[k]['path']+'/content'}} for k in ['pdf','verification_zip']]}
    state={'corruptfile':False}
    def fake(url,limit):
        if url=='https://zenodo.org/api/records/123456':return json.dumps(actual).encode()
        name=url.split('/')[-2];need(name in [build[k]['path'] for k in ['pdf','verification_zip']],'unknown public download');return b'corrupt' if state['corruptfile'] else (root/name).read_bytes()
    m.fetch=fake
    quiet(m.main);receipt=json.loads((root/'PUBLIC_DOWNLOAD_VERIFICATION.json').read_text());need(receipt['metadata_fields_verified']==sorted(meta),'metadata keys incomplete')
    refused=[]
    for key in meta:
        old=copy.deepcopy(actual['metadata'])
        if key in ['upload_type','publication_type']:actual['metadata']['resource_type']['type' if key=='upload_type' else 'subtype']='wrong'
        elif key=='license':actual['metadata']['license']['id']='wrong'
        else:actual['metadata'][key]=None
        refused.append(fails(m.main,'public metadata '+key));actual['metadata']=old
    state['corruptfile']=True;refused.append(fails(m.main,'public corrupt file'));state['corruptfile']=False
    actual['files'].append(copy.deepcopy(actual['files'][0]));refused.append(fails(m.main,'public duplicate file inventory'))
    RESULT['public_main']={'positive':True,'refusals':refused,'all_HTTP_fetches_mocked':True}

def updater_main():
    root=fixture('updater');m=load('update_pr_publication',root);pub,meta,build=pub_fixture(root);t=load('append_tracker',root)
    tracker={'spreadsheetId':t.SID,'gid':t.GID,'row':t.expected_row(pub,meta['title']),'updatedRange':"'Math Puzzles'!A2:D2",'readback_verified':True};(root/'tracker').mkdir(exist_ok=True);save(root/'tracker/TRACKER_RECEIPT.json',tracker)
    public={'public_record_identity_verified':True,'all_supplied_metadata_exact':True,'metadata_manifest_sha256':sha(root/'zenodo-deposit.json'),'doi':pub['doi'],'id':pub['id'],'doi_url':pub['doi_url'],'record_url':pub['record_url'],'metadata_fields_verified':sorted(meta),'files':[{'name':build[k]['path'],'bytes':build[k]['bytes'],'sha256':build[k]['sha256']} for k in ['pdf','verification_zip']]};save(root/'PUBLIC_DOWNLOAD_VERIFICATION.json',public)
    review=root.parent/'reviews/offline_clean';review.mkdir();(review/'REPORT.md').write_text('Offline test clean fixture, not a real publication review');save(review/'VERDICT.json',{'status':'CLEAN'})
    gate={'schema':'math-preprint-final-review-gate-v1','pr':1216,'problem_id':30000921,'original_head':m.ORIGINAL,'status':'pass','workflow':{n:sha(root/n) for n in m.REQUIRED_WORKFLOW},'latest_review':{'status':'CLEAN','report':'../reviews/offline_clean/REPORT.md','report_sha256':sha(review/'REPORT.md'),'verdict':'../reviews/offline_clean/VERDICT.json','verdict_sha256':sha(review/'VERDICT.json')},'pdf_sha256':build['pdf']['sha256'],'verification_zip_sha256':build['verification_zip']['sha256'],'metadata_sha256':sha(root/'zenodo-deposit.json')};save(root/'FINAL_REVIEW_GATE.json',gate)
    snapshot=json.loads((root.parent/'SUBMITTED_SNAPSHOT.json').read_text());origbody=(BASE/'PR_BODY.md').read_text();need(hashlib.sha256(origbody.encode()).hexdigest()==snapshot['body_sha256'],'original body fixture')
    state={'headRefOid':m.ORIGINAL,'headRefName':m.BRANCH,'state':'OPEN','isDraft':True,'body':origbody};remote={'head':m.ORIGINAL};actions=[];objects={};trees={};commit='c'*40;stored={}
    # Git object/database calls, remote operations, and gh all use this in-memory model.
    def fakegit(*a,data=None):
        if a==('branch','--show-current'):return b'main\n'
        if a[0]=='rev-parse':return (next(x['blob'] for x in snapshot['files'] if x['path']==a[1].split(':',1)[1])+'\n').encode()
        if a[0]=='ls-tree':return b''.join(e+b'\0' for e in trees.get(a[-1],[]))
        if a[0]=='hash-object':
            oid=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();objects[oid]=data;return (oid+'\n').encode()
        if a[0]=='mktree':
            oid=hashlib.sha1(data).hexdigest();trees[oid]=[x for x in data.split(b'\0') if x];return (oid+'\n').encode()
        if a[0]=='commit-tree':
            def flatten(oid,prefix=''):
                for e in trees[oid]:
                    mode,kind,child=e.split(b'\t')[0].decode().split();name=e.split(b'\t')[1].decode()
                    if kind=='tree':flatten(child,prefix+name+'/')
                    else:stored[prefix+name]=objects[child]
            flatten(a[1]);return (commit+'\n').encode()
        if a[0]=='update-ref':actions.append('local audit ref');return b''
        if a[0]=='rev-list':return (commit+' '+m.ORIGINAL+'\n').encode()
        if a[0]=='diff-tree':return ('\n'.join(sorted(stored))+'\n').encode()
        if a[0]=='show':return stored[a[1].split(':',1)[1]]
        if a[0]=='ls-remote':return (remote['head']+' refs/heads/'+m.BRANCH+'\n').encode()
        if a[0]=='push':actions.append('push');remote['head']=commit;state['headRefOid']=commit;return b''
        raise RuntimeError('Unmocked Git operation '+repr(a))
    def fakecmd(args,**kw):
        need(args[:3]==['gh','pr','edit'],'Unmocked command');actions.append('body edit');state['body']=(root/'PR_BODY_FINAL.md').read_text();return types.SimpleNamespace(returncode=0,stdout='',stderr='')
    m.git=fakegit;m.pr=lambda:copy.deepcopy(state);m.subprocess=types.SimpleNamespace(run=fakecmd)
    # Negative states must fail before any mutation; same actual main entrypoint.
    refused=[]
    for name,mutate in [('stale_metadata',lambda x:x.update(metadata_sha256='0'*64)),('missing_workflow',lambda x:x['workflow'].pop('append_tracker.py')),('wrong_head_gate',lambda x:x.update(original_head='0'*40)),('nonclean_gate',lambda x:x['latest_review'].update(status='CHANGES_REQUIRED'))]:
        bad=copy.deepcopy(gate);mutate(bad);save(root/'FINAL_REVIEW_GATE.json',bad);refused.append(fails(m.main,name));need(not actions,'mutation before gate refusal')
    save(root/'FINAL_REVIEW_GATE.json',gate)
    old=tracker['row'][1];tracker['row'][1]='nonblank';save(root/'tracker/TRACKER_RECEIPT.json',tracker);refused.append(fails(m.main,'nonblank tracker cell B'));tracker['row'][1]=old;save(root/'tracker/TRACKER_RECEIPT.json',tracker)
    public['all_supplied_metadata_exact']=False;save(root/'PUBLIC_DOWNLOAD_VERIFICATION.json',public);refused.append(fails(m.main,'unverified public metadata'));public['all_supplied_metadata_exact']=True;save(root/'PUBLIC_DOWNLOAD_VERIFICATION.json',public)
    quiet(m.main);need(len(stored)==13,'wrong updater paths');need(actions==['local audit ref','push','body edit'],'wrong update action trace');first=copy.deepcopy(actions);quiet(m.main);need(actions==first,'completed retry mutated')
    receipt=json.loads((root/'PR_BRANCH_RECEIPT.json').read_text());need(receipt['body_readback_verified'] and receipt['remote_readback_verified'],'incomplete final receipt')
    intent=root/'PR_BRANCH_INTENT.json';old=intent.read_bytes();obj=json.loads(old);obj['doi']='10.5281/zenodo.999';save(intent,obj);refused.append(fails(m.main,'stale saved intent on completed retry'));intent.write_bytes(old)
    RESULT['update_main']={'fresh_exact13paths_and_body':True,'idempotent_completed_retry':True,'mutation_trace':actions,'refusals':refused,'all_Git_GitHub_operations_mocked':True,'limit':'Synthetic object store exercises put/tree/main control flow; no repository writes or actual remote calls.'}

def regression_main():
    root=fixture('regression');r=subprocess.run([sys.executable,'-B',str(root/'workflow_regression.py')],capture_output=True,text=True);need(r.returncode==0,r.stderr);result=json.loads(r.stdout);need(result['all_modes_identical'],'regression modes');RESULT['supplied_regression_main']={'all_modes_identical':True,'runs':len(result['runs']),'program_sha256':result['program_sha256']}

if __name__=='__main__':
    for f in [artifacts,build_and_prepare,compile_mock,tracker_main,public_main,updater_main,regression_main]:
        f();print('PASS',f.__name__,flush=True)
    RESULT['at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save(HERE/'CHECK_RECEIPT.json',RESULT)
