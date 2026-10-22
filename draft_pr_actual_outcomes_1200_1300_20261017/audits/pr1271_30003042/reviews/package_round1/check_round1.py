#!/usr/bin/env python3
"""Fresh review harness. Writes only this review's ignored scratch and evidence.

Actual operative modules are imported byte-for-byte. All publication, Google,
Git and HTTP operations in workflow tests are replaced by explicit mocks.
"""
from pathlib import Path
import contextlib, copy, datetime, hashlib, importlib.util, io, json, os
import shutil, subprocess, sys, tempfile, types

R=Path(__file__).resolve().parent
A=R.parents[1]
P=A/'publication'
L=R/'_local'
os.environ['TMPDIR']=str(L)
os.environ['PYTHONDONTWRITEBYTECODE']='1'
tempfile.tempdir=str(L)

def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def load(path):
    s=importlib.util.spec_from_file_location('round1_'+path.stem+str(id(path)),path)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def capture(fn):
    with contextlib.redirect_stdout(io.StringIO()):return fn()
def rejected(fn,label):
    try:fn()
    except (RuntimeError,ValueError,KeyError,FileNotFoundError) as e:return {'case':label,'exception':type(e).__name__,'reason':str(e)}
    raise RuntimeError('Corrupt case accepted: '+label)

def portable():
    root=L/('extracted-mode'+str(sys.flags.optimize))
    if root.exists():shutil.rmtree(root)
    shutil.copytree(L/'extracted',root)
    v=load(root/'verify.py');build=json.loads((P/'BUILD_RECEIPT.json').read_text())
    an=build['verification_anchors'];need(len(list(root.rglob('*')))>169,'extraction missing directories')
    args=[a for k,val in an.items() for a in ['--expected-'+k+'-sha256',val]]
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    run=subprocess.run([sys.executable,'-B',*flags,str(root/'verify.py'),*args],capture_output=True,text=True,timeout=180)
    need(run.returncode==0,run.stderr);actual=json.loads(run.stdout)
    need(actual['authenticated_members']==168 and len(actual['nested_manifests'])==13,'wrong actual inventory')
    matrix=[];manifest=root/'MANIFEST.json';raw=manifest.read_bytes()
    def check(anchor=None):return v.verify(root,anchor or an['manifest'],an['context'],an['snapshot'])
    def refresh():
        x=json.loads(raw)
        for row in x['files']:
            p=root/row['path'];row.update(bytes=p.stat().st_size,sha256=sha(p))
        save(manifest,x);return sha(manifest)
    payload=root/'reviews/chow_computation/REPORT.md';old=payload.read_bytes()
    try:
        payload.write_bytes(old+b'\nCORRUPTED\n');matrix.append(rejected(check,'nested_payload'))
        current=refresh();matrix.append(rejected(lambda:check(current),'nested_payload_coupled_outer_rewrite'))
    finally:payload.write_bytes(old);manifest.write_bytes(raw)
    nested=root/'reviews/chow_computation/MANIFEST.json';old=nested.read_bytes()
    try:
        x=json.loads(old);x['authored_files'][0]['sha256']='0'*64;save(nested,x)
        current=refresh();matrix.append(rejected(lambda:check(current),'nested_manifest_coupled_outer_rewrite'))
    finally:nested.write_bytes(old);manifest.write_bytes(raw)
    for label,mutate in [
        ('unsafe_parent',lambda x:x['files'][0].update(path='../escape')),
        ('absolute_path',lambda x:x['files'][0].update(path='/outside')),
        ('duplicate_path',lambda x:x['files'].append(copy.deepcopy(x['files'][0]))),
        ('case_path',lambda x:x['files'][0].update(path=x['files'][0]['path'].swapcase())),
    ]:
        try:
            x=json.loads(raw);mutate(x);save(manifest,x);matrix.append(rejected(lambda:check(sha(manifest)),label))
        finally:manifest.write_bytes(raw)
    extra=root/'unexpected.txt'
    try:extra.write_text('unlisted');matrix.append(rejected(check,'unlisted_file'))
    finally:extra.unlink()
    context=root/'provenance/CURRENT_PR1271_CONTEXT.json';old=context.read_bytes()
    try:
        x=json.loads(old);x['title']='CORRUPTED';save(context,x);current=refresh()
        matrix.append(rejected(lambda:check(current),'context_coupled_outer_rewrite_outside_context_anchor'))
    finally:context.write_bytes(old);manifest.write_bytes(raw)
    matrix.append(rejected(lambda:v.need(False,'guard survived optimization'),'explicit_guard'))
    return {'actual_archive_verification':actual,'tamper_controls':matrix,'flags':sys.flags.optimize}

def each_merged_blob(w):
    with tempfile.TemporaryDirectory(prefix='each-merged-blob-',dir=L) as tmp:
        f=w.fixture(Path(tmp)/'fixture');w.context_and_portable_controls(f)
        pubrec,tracker,_=w.publication_and_tracker_controls(f);w.update_controls(f,pubrec,tracker)
        pub=f['pub'];audit=f['audit'];program=audit.parents[1]
        u=load(pub/'update_pr_publication.py');t=load(pub/'append_tracker.py')
        m=load(program/'publication_coordinators/verify_pr1271_merge.py')
        files,_,_=u.desired_files(f['build'],pubrec,tracker,f['snapshot'])
        need(len(files)==13,'thirteen required');head='a'*40;merge='c'*40
        body=(pub/'PR_BODY_FINAL.md').read_text();wanted=u.expected_identity(pubrec,tracker,files,body)
        save(pub/'PR_BRANCH_RECEIPT.json',{**wanted,'commit':head,'body_readback_verified':True,'remote_readback_verified':True})
        live={'state':'MERGED','headRefOid':head,'headRefName':u.BRANCH,'mergeCommit':{'oid':merge},'mergedAt':'2026-10-17T21:00:00Z','body':body,'url':'https://github.com/AlecKriebel/Math/pull/1271'}
        mode={'corrupt':None};events=[]
        def git(*args,data=None):
            events.append(['git',*args])
            if args==('branch','--show-current'):return b'main\n'
            if args[0]=='rev-list':return ((merge+' '+'d'*40+' '+head if args[-1]==merge else head+' '+u.ORIGINAL)+'\n').encode()
            if args[0]=='diff-tree':return ('\n'.join(sorted(files))+'\n').encode()
            if args[0]=='show':
                commit,path=args[1].split(':',1)
                return b'CORRUPTED SINGLE MERGED BLOB' if commit==merge and path==mode['corrupt'] else files[path]
            if args[0] in {'fetch','update-ref'}:return b''
            raise RuntimeError('Forbidden unmocked Git operation '+repr(args))
        u.git=git
        rows=[['Original Problem','Solution Chat URL','DOI','Notes'],tracker['row']]
        def call(parts,params,body=None):
            events.append(['gws',*parts])
            if parts==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':t.GID,'title':'Math Puzzles'}}]}
            if parts==['spreadsheets','values','get']:return {'values':copy.deepcopy(rows)}
            raise RuntimeError('Forbidden service mutation')
        t.call=call
        def route(path):
            if Path(path).name=='update_pr_publication.py':return u.__dict__
            if Path(path).name=='append_tracker.py':return t.__dict__
            raise RuntimeError('Unexpected routed module')
        m.runpy=types.SimpleNamespace(run_path=route)
        m.subprocess=types.SimpleNamespace(check_output=lambda *a,**k:json.dumps(live))
        pubrec['doi_resolution']={'status':'resolved','http_status':200};save(pub/'PUBLICATION_RECEIPT.json',pubrec)
        # Publication bytes participate in the intended merge tree: recalculate
        # the receipt-bound desired files after adding the resolver evidence.
        files,_,_=u.desired_files(f['build'],pubrec,tracker,f['snapshot'])
        wanted=u.expected_identity(pubrec,tracker,files,body)
        save(pub/'PR_BRANCH_RECEIPT.json',{**wanted,'commit':head,'body_readback_verified':True,'remote_readback_verified':True})
        initial={'current_pr':1271,'completed_prs':copy.deepcopy(m.COMPLETED_BEFORE),'publications':[{'pr':n} for n in m.COMPLETED_BEFORE],'eligible_prs':copy.deepcopy(m.ELIGIBLE),'eligible_count':12}
        statepath=program/'PROGRAM_STATE.json';save(statepath,initial);capture(m.main)
        need(json.loads(statepath.read_text())['current_pr']==1274,'positive full-main did not advance')
        result=[]
        for path in sorted(files):
            save(statepath,initial);before=statepath.read_bytes();events.clear();mode['corrupt']=path
            row=rejected(m.main,'single_corrupt_merge_blob:'+path)
            need('Merged bytes differ '+path in row['reason'],'wrong rejection cause '+row['reason'])
            need(statepath.read_bytes()==before,'state advanced on corrupt blob')
            row.update(state_bytes_unchanged=True,actual_complete_postmerge_main=True)
            result.append(row)
        return {'positive_complete_main_advances_8_to_9':True,'individually_corrupted_blobs':result,'actual_postmerge_sha256':sha(program/'publication_coordinators/verify_pr1271_merge.py'),'all_external_operations_mocked':True}

def workflow():
    w=load(P/'workflow_regression.py');w.REPORT_ROOT=R
    whole=w.worker()
    # worker changes PATH only within this harness process; its generated
    # compiler and pdfinfo fixtures remain isolated under this review folder.
    return {'actual_current_regression':whole,'fresh_each13_blob_test':each_merged_blob(w),'flags':sys.flags.optimize}

if __name__=='__main__':
    mode=sys.argv[1]
    result=portable() if mode=='portable' else workflow()
    save(R/(mode+'_mode'+str(sys.flags.optimize)+'.json'),result)
    print(json.dumps({'mode':mode,'optimization':sys.flags.optimize,'status':'PASS'}))
