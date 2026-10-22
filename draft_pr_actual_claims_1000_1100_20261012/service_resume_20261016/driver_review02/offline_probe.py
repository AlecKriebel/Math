"""Execute the frozen, unmodified driver in isolated child processes.

All service subprocesses are replaced with deterministic file-backed fakes.
Socket creation is also blocked. No credentials are read. Fixtures live here.
"""
from pathlib import Path
import datetime, hashlib, importlib.machinery, importlib.util, json, os
import shutil, socket, subprocess, sys, time, traceback
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
SOURCE = HERE/'REVIEWED_run_service.py.txt'

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2)+'\n')

def load(path): return json.loads(path.read_text())
def identity(path):
    b=path.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def setup(name, numbers=(1033,)):
    root=HERE/'fixtures'/name
    if root.exists():shutil.rmtree(root)
    d=root/'program';r=d/'service';r.mkdir(parents=True)
    configs={};prs={};publications={}
    for n in numbers:
        a=d/'audits'/f'pr{n}';a.mkdir(parents=True)
        manifest=a/'manifest.json';seal=a/'seal.json';asset=a/'asset'
        metadata={'title':f'Reviewed title {n}','description':'Reviewed description'}
        dump(manifest,{'metadata':metadata,'files':[{'path':'asset'}]})
        dump(seal,{'publication_ready':True});asset.write_bytes(b'reviewed bytes')
        cfg={'pr':n,'audit_folder':str(a.relative_to(d)),'manifest':str(manifest.relative_to(d)),
             'final_seal':str(seal.relative_to(d)),'manifest_identity':identity(manifest),
             'final_seal_identity':identity(seal),'files':[{'path':str(asset.relative_to(d)),**identity(asset)}],
             'metadata_sha256':hashlib.sha256(json.dumps(metadata,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
             'fresh_complete_reviews':2,'head':f'{n:040x}','title':metadata['title'],'problem_id':str(n),
             'accepted_scope':'Scoped claim','limitations':'Priority UNKNOWN',
             'pr_title':f'Accept {n}: '+metadata['title'],'tracker_original_problem':f'Problem {n}',
             'tracker_notes':'Reviewed notes'}
        dump(r/f'PR{n}_SERVICE_CONFIG.json',cfg);configs[str(n)]=cfg
        prs[str(n)]={'number':n,'head':{'sha':cfg['head']},'base':{'ref':'main','repo':{'full_name':'AlecKriebel/Math'}},
                     'state':'open','merged':False,'merge_commit_sha':None,'merged_at':None,
                     'draft':True,'title':'Original title','body':'Original description'}
        publications[str(n)]={'environment':'production','state':'ready_to_publish','title':cfg['title'],
                             'id':n,'doi':f'10.5281/zenodo.{n}','doi_url':f'https://doi.org/10.5281/zenodo.{n}',
                             'record_url':f'https://zenodo.org/records/{n}','doi_resolution':{'status':'resolved'}}
    dump(d/'STATE.json',{'next_pr':min(numbers),'completed_prs':[1001,1024,1025,1031],
                        'candidate_full_claim_prs':[1001,1024,1025,1031,*numbers,max(numbers)+1],
                        'accepted_results':[],'publications':[]})
    dump(d/'CLAIM_REGISTRY.json',{'records':[{'pr':n,'workflow_outcome':'PENDING'} for n in numbers]})
    (d/'README.md').write_text('Initial readme\n');(d/'RESEARCH_LOG.md').write_text('Initial log\n')
    dump(root/'remote.json',{'configs':configs,'prs':prs,'publications':publications,
                           'rows':[['Original Problem','Solution Chat URL','DOI','Notes']],
                           'merge_policy':'success'})
    return root

def receipt(root,n):return root/'program'/'audits'/f'pr{n}'/'service_receipts_20261016'

def ready_complete(root,n=1033):
    remote=load(root/'remote.json');cfg=remote['configs'][str(n)];pub=remote['publications'][str(n)]
    pub['state']='published';pr=remote['prs'][str(n)];pr.update({'merged':True,'state':'closed','draft':False,
                    'merge_commit_sha':f'{n+10000:040x}','merged_at':'2026-10-16T00:00:00Z'})
    remote['rows'].append([cfg['tracker_original_problem'],'',pub['doi_url'],cfg['tracker_notes']])
    dump(root/'remote.json',remote)
    dump(receipt(root,n)/'TRACKER_VERIFIED.json',{'doi':pub['doi'],'read_back_exact':True,'sheet_row':len(remote['rows'])})
    dump(receipt(root,n)/'MERGE_VERIFIED.json',{'head':cfg['head'],'merge_commit':pr['merge_commit_sha'],'merged_at':pr['merged_at']})

def child(root,n,step,fault):
    loader=importlib.machinery.SourceFileLoader('review_driver',str(SOURCE))
    spec=importlib.util.spec_from_loader(loader.name,loader);driver=importlib.util.module_from_spec(spec);loader.exec_module(driver)
    driver.D=root/'program';driver.R=driver.D/'service';driver.REPO=root
    socket.socket=lambda *a,**k: (_ for _ in ()).throw(AssertionError('Network forbidden'))
    def fake(argv,**kwargs):
        argv=list(map(str,argv));remote=load(root/'remote.json');cfg=remote['configs'][str(n)];pr=remote['prs'][str(n)];pub=remote['publications'][str(n)]
        action='unknown';result={};code=0;stderr=''
        if argv[0]==driver.GH:
            if 'PATCH' in argv:
                action='patch';pr.update(load(Path(argv[-1])));result=pr
            elif argv[1:3]==['pr','ready']:
                action='ready';pr['draft']=False;result=pr
            elif argv[1:3]==['pr','merge']:
                action='merge'
                if remote['merge_policy']=='reject':code=1;stderr='Offline policy rejection'
                else:pr.update({'merged':True,'state':'closed','merge_commit_sha':f'{n+10000:040x}','merged_at':'2026-10-16T00:00:00Z'})
            elif 'commits/' in argv[-1]:action='commit';result={'parents':[{'sha':cfg['head']},{'sha':'c'*40}]}
            elif argv[-1]==f'repos/AlecKriebel/Math/pulls/{n}':action='pr_read';result=pr
            else:raise AssertionError(argv)
        elif argv[0]==driver.GWS:
            if 'append' in argv:
                action='append';remote['rows'].extend(json.loads(argv[argv.index('--json')+1])['values']);result={'updates':{}}
            elif 'values' in argv:action='tracker_read';result={'values':remote['rows']}
            else:action='tabs';result={'sheets':[{'properties':{'sheetId':driver.GID,'title':"Tracker's tab"}}]}
        elif len(argv)>3 and argv[3] in {'check','stage','inspect','publish'}:
            action=argv[3]
            if action=='stage':
                if fault=='stage_no_id':code=1;stderr='Offline lost draft response'
                else:
                    key=hashlib.sha256(str(Path(argv[4]).resolve()).encode()).hexdigest()[:24]
                    dump(root/'.zenodo-state'/f'{key}-production.json',{'id':n})
            if action=='publish':pub['state']='published'
            result={**pub,'files':cfg['files']}
        else:raise AssertionError('Unexpected subprocess '+repr(argv))
        dump(root/'remote.json',remote)
        with (root/'SERVICE_CALLS.jsonl').open('a') as f:f.write(json.dumps({'step':step,'action':action,'argv':argv,'fault':fault})+'\n')
        if fault=='timeout_'+action:raise subprocess.TimeoutExpired(argv,1,output=b'Offline ambiguous timeout',stderr=b'')
        return SimpleNamespace(returncode=code,stdout=json.dumps(result),stderr=stderr)
    driver.subprocess.run=fake
    original_atomic=driver.atomic_text
    def atomic(path,value):
        if fault=='before_'+path.name:raise OSError('Offline write failure before '+path.name)
        original_atomic(path,value)
        if fault=='after_'+path.name:raise OSError('Offline write failure after '+path.name)
    driver.atomic_text=atomic
    original_read=driver.read
    def read(path):
        if fault=='hold_completion' and path.name=='STATE.json':
            (root/'HOLD_ENTERED').write_text('Completion lock held')
            deadline=time.monotonic()+20
            while not(root/'HOLD_RELEASE').exists():
                if time.monotonic()>deadline:raise RuntimeError('Offline barrier timeout')
                time.sleep(.02)
        return original_read(path)
    driver.read=read
    sys.argv=['run_service.py',str(n),step]
    try:driver.main()
    except BaseException as exc:
        print(json.dumps({'outcome':'raised','exception':type(exc).__name__,'message':str(exc)}))
        traceback.print_exc(file=sys.stderr);return 1
    return 0

def invoke(root,step,n=1033,fault=''):
    argv=[sys.executable,'-B',str(Path(__file__).resolve()),'child',str(root),str(n),step,fault]
    p=subprocess.run(argv,capture_output=True,text=True,timeout=30)
    row={'argv':argv,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    with (HERE/'COMMAND_RECEIPTS.jsonl').open('a')as f:f.write(json.dumps(row)+'\n')
    return row

def calls(root,action):
    p=root/'SERVICE_CALLS.jsonl';return [r for r in map(json.loads,p.read_text().splitlines()) if r['action']==action] if p.exists() else []

def assert_complete(root,n):
    d=root/'program';s=load(d/'STATE.json');marker=f'[EXTERNAL_COMPLETION_PR_{n}]'
    assert n in s['completed_prs']
    assert sum(r['pr']==n for r in s['accepted_results'])==1
    assert sum(r['pr']==n for r in s['publications'])==1
    assert next(r for r in load(d/'CLAIM_REGISTRY.json')['records']if r['pr']==n)['workflow_outcome']=='PUBLISHED_TRACKED_EXACT_HEAD_MERGED'
    assert (d/'RESEARCH_LOG.md').read_text().count(marker)==1
    assert (d/'README.md').read_text().count(marker)==1
    assert (receipt(root,n)/'COMPLETION_RECONCILED.json').exists()

def suite():
    results=[]
    root=setup('happy_full_workflow')
    for step in ['plan','stage','publish','track','merge','complete']:assert invoke(root,step)['exit']==0,step
    assert_complete(root,1033);results.append({'probe':'happy_full_workflow','pass':True})
    for target in ['CLAIM_REGISTRY.json','RESEARCH_LOG.md','README.md','STATE.json','COMPLETION_RECONCILED.json']:
        for when in ['before','after']:
            root=setup('completion_'+when+'_'+target);ready_complete(root)
            first=invoke(root,'complete',fault=when+'_'+target);assert first['exit']==1
            cursor_after_failure=load(root/'program'/'STATE.json')['next_pr']
            if target not in ['STATE.json','COMPLETION_RECONCILED.json'] or (target=='STATE.json'and when=='before'):assert cursor_after_failure==1033
            utc=load(receipt(root,1033)/'COMPLETION_EVENT.json')['utc']
            retry=invoke(root,'complete');assert retry['exit']==0;assert_complete(root,1033)
            assert load(receipt(root,1033)/'COMPLETION_EVENT.json')['utc']==utc
            results.append({'probe':'completion_write_failure_retry','target':target,'when':when,'cursor_after_failure':cursor_after_failure,'pass':True})
    root=setup('merge_rejection_retry');remote=load(root/'remote.json');remote['merge_policy']='reject';dump(root/'remote.json',remote)
    for step in ['stage','publish','track']:assert invoke(root,step)['exit']==0
    first=invoke(root,'merge');retry=invoke(root,'merge');remote=load(root/'remote.json')
    assert first['exit']==retry['exit']==1
    assert len(calls(root,'patch'))==len(calls(root,'ready'))==len(calls(root,'merge'))==1
    assert remote['prs']['1033']['body'].count('## Accepted result and published preprint')==1
    results.append({'probe':'merge_rejection_retry_no_mutation_or_nesting','pass':True})
    for action in ['publish','patch','ready','merge','append']:
        root=setup('ambiguous_'+action)
        steps=['stage','publish','track','merge']
        target_step={'publish':'publish','append':'track','patch':'merge','ready':'merge','merge':'merge'}[action]
        for step in steps[:steps.index(target_step)]:assert invoke(root,step)['exit']==0
        first=invoke(root,target_step,fault='timeout_'+action);assert first['exit']==1
        retry=invoke(root,target_step);assert retry['exit']==0,(action,retry)
        assert len(calls(root,action))==1
        results.append({'probe':'ambiguous_service_success_retry','action':action,'pass':True})
    root=setup('stage_no_id');first=invoke(root,'stage',fault='stage_no_id');retry=invoke(root,'stage');assert first['exit']==retry['exit']==1
    assert len(calls(root,'stage'))==1;results.append({'probe':'uncertain_stage_no_repeat','pass':True})
    for field,value in [('head',{'sha':'d'*40}),('base',{'ref':'other','repo':{'full_name':'AlecKriebel/Math'}}),('base',{'ref':'main','repo':{'full_name':'Other/Math'}}),('number',9999)]:
        root=setup('pr_identity_'+str(len(results)));remote=load(root/'remote.json');remote['prs']['1033'][field]=value;dump(root/'remote.json',remote)
        assert invoke(root,'stage')['exit']==1;assert not calls(root,'stage');results.append({'probe':'PR_identity_or_target_drift_block','field':field,'value':value,'pass':True})
    for step in ['merge','complete']:
        root=setup('stale_tracker_'+step);ready_complete(root)
        remote=load(root/'remote.json');remote['rows']=remote['rows'][:1]
        if step=='merge':remote['prs']['1033'].update({'state':'open','merged':False})
        dump(root/'remote.json',remote);assert invoke(root,step)['exit']==1
        assert not calls(root,'merge');assert load(root/'program'/'STATE.json')['next_pr']==1033
        results.append({'probe':'stale_tracker_blocks_'+step,'pass':True})
    root=setup('completion_global_lock',(1033,1034));ready_complete(root,1033);ready_complete(root,1034)
    s=load(root/'program'/'STATE.json');s['next_pr']=1034;s['completed_prs'].append(1033);dump(root/'program'/'STATE.json',s)
    argv=[sys.executable,'-B',str(Path(__file__).resolve()),'child',str(root),'1033','complete','hold_completion']
    p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    try:
        deadline=time.monotonic()+10
        while not(root/'HOLD_ENTERED').exists():
            assert time.monotonic()<deadline,'First child did not acquire completion lock';time.sleep(.02)
        second=invoke(root,'complete',n=1034);assert second['exit']==1 and 'BlockingIOError' in second['stdout']
        (root/'HOLD_RELEASE').write_text('Release')
        stdout,stderr=p.communicate(timeout=10);assert p.returncode==0,(stdout,stderr)
        with (HERE/'COMMAND_RECEIPTS.jsonl').open('a')as f:f.write(json.dumps({'argv':argv,'exit':p.returncode,'stdout':stdout,'stderr':stderr})+'\n')
        assert invoke(root,'complete',n=1034)['exit']==0;assert_complete(root,1033);assert_complete(root,1034)
        results.append({'probe':'global_completion_lock_serializes_old_retry_and_current_PR','pass':True})
    finally:
        if p.poll()is None:p.kill();p.communicate()
    report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_identity':identity(SOURCE),
            'all_service_subprocesses_mocked':True,'network_blocked':True,'all_probe_writes_under':str(HERE),
            'results':results,'status':'PASS'}
    dump(HERE/'PROBE_RESULTS.json',report);print(json.dumps({'status':'PASS','probes':len(results)}))

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='child':sys.exit(child(Path(sys.argv[2]),int(sys.argv[3]),sys.argv[4],sys.argv[5]))
    suite()
