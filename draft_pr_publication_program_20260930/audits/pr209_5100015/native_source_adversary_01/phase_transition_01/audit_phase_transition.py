"""Offline actual-load_inputs phase-marker controls; synthetic in-memory bindings only."""
from pathlib import Path
import hashlib,json,sys,types
from datetime import datetime,timezone
BASE=Path(__file__).absolute().parent
RESULTS=[]

def enc(value):return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def check(name,condition,detail=None):
    if not condition:raise RuntimeError('Independent marker control failed: '+name+'; '+str(detail))
    RESULTS.append({'name':name,'observed':detail})

def model(version):
    folder='historical_20261017_source_freeze' if version=='historical' else ('pre_stem_source_freeze' if version=='pre_stem' else 'source_freeze')
    freeze='HISTORICAL_SOURCE_FREEZE.json' if version=='historical' else ('PRE_STEM_SOURCE_FREEZE.json' if version=='pre_stem' else 'SOURCE_FREEZE.json')
    expected=json.loads((BASE/freeze).read_bytes())['files']
    rows={name:(BASE/folder/name).read_bytes() for name in expected}
    for name,raw in rows.items():
        if pin(raw)!=expected[name]:raise RuntimeError('Source pin drift '+name)
    h=types.ModuleType('synthetic_marker_'+version);h.__file__=str(BASE/folder/'native209_model.py')
    exec(compile(rows['native209_model.py'],h.__file__,'exec'),h.__dict__)
    return h,rows

def marker(h,phase):return ('<!-- PR209_NATIVE_PHASE_FACTS '+h.compact(h.phase_facts(phase))+' -->').encode()

def fixture(version,phase,change=None,seeds=None):
    h,sources=model(version);facts=h.phase_facts(phase);files={};own={};original=[]
    for i in range(23):
        path=h.ATTEMPT+'original_'+str(i)+'.txt';raw=('synthetic preserved author body '+str(i)+'\n').encode();own[path]=raw
        original.append({'path':path,'mode':'100644','type':'blob','git_object':h.native('blob',raw)})
        own[h.ATTEMPT+'history/original_submission_20261016/'+path[len(h.ATTEMPT):]]=raw
    for i in range(8):own[h.ATTEMPT+'revised_'+str(i)+'.txt']=('synthetic revised '+str(i)+'\n').encode()
    final=h.ATTEMPT+'revised_7.txt';own[final]=b'x'*(205547-sum(len(raw) for path,raw in own.items() if path!=final))
    if len(own)!=54 or sum(map(len,own.values()))!=205547:raise RuntimeError('Synthetic own54 fixture')
    baseline_raw=(BASE/'BASELINE_REFERENCE.json').read_bytes()
    if pin(baseline_raw)!=h.BASELINE_PIN:raise RuntimeError('Actual fixed baseline metadata pin')
    baseline=h.decode(baseline_raw);files['BASELINE_MEMBERSHIP.json']=baseline_raw
    def progress(which):
        obj={**h.phase_facts(which),'dated_eligible_total':99,'fully_completed_eligible_PRs':baseline['fully_completed_eligible_PRs']+([209] if which=='completion100' else []),'published_PRs':baseline['published_PRs']+[209]}
        return enc(obj)
    seed_case=b'# Synthetic case research log\n\nExisting local-only intake history.\n'
    seed_program=b'# Synthetic program research log\n\nImmutable earlier program history.\n'
    if seeds is not None:seed_case,seed_program=seeds
    before95={h.VIEWS[0]:None,h.VIEWS[1]:seed_case,h.VIEWS[2]:baseline_raw,h.VIEWS[3]:b'# Prior progress\n',h.VIEWS[4]:seed_program}
    phase95={h.VIEWS[0]:enc(h.phase_facts('merge95')),h.VIEWS[1]:seed_case+b'\nActual phase95 checkpoint fixture.\n'+marker(h,'merge95')+b'\n',h.VIEWS[2]:progress('merge95'),h.VIEWS[3]:b'# Current phase95\n'+marker(h,'merge95')+b'\n',h.VIEWS[4]:seed_program+b'\nActual phase95 checkpoint fixture.\n'+marker(h,'merge95')+b'\n'}
    current=phase95 if phase=='merge95' else {h.VIEWS[0]:enc(facts),h.VIEWS[1]:phase95[h.VIEWS[1]]+b'\nActual completion100 checkpoint fixture.\n'+marker(h,'completion100')+b'\n',h.VIEWS[2]:progress('completion100'),h.VIEWS[3]:b'# Current completion100\n'+marker(h,'completion100')+b'\n',h.VIEWS[4]:phase95[h.VIEWS[4]]+b'\nActual completion100 checkpoint fixture.\n'+marker(h,'completion100')+b'\n'}
    local=before95 if phase=='merge95' else phase95
    overlay={**own,**current,h.QUEUE:json.loads((BASE/'QUEUE_ROWS.json').read_bytes())['revised'].encode(),h.CASE+'synthetic_evidence.json':b'{"synthetic_evidence":true}\n'}
    if change is not None:change(h,overlay,local)
    revised=[{'path':path,'mode':'100644','type':'blob','git_object':h.native('blob',raw)} for path,raw in sorted(own.items())]
    refs={'ORIGINAL_NATIVE_REFERENCE.json':{'leaf_count':23,'root_tree':h.ORIGINAL_TREE,'leaves':original},'REVISED_NATIVE_REFERENCE.json':{'leaf_count':54,'root_tree':h.PREPARED_TREE,'leaves':revised},'QUEUE_REFERENCE.json':{},'CUSTODY_BODY_IDENTITIES.json':{'inventories':{'revised':[{'path':path,**pin(raw)} for path,raw in sorted(own.items())],'original':[{'path':r['path'],**pin(own[r['path']])} for r in original]}}}
    reused=[{'path':h.SHARED+'/synthetic_science/'+str(i)+'.txt','bytes':len(('synthetic '+str(i)).encode()),'sha256':hashlib.sha256(('synthetic '+str(i)).encode()).hexdigest(),'git_blob':h.native('blob',('synthetic '+str(i)).encode())} for i in range(228)]
    refs['EXISTING_SHARED_BODY_IDENTITIES.json']={'files':reused}
    # The source's closed input and marker checks are real. Synthetic reference pins
    # isolate them from actual authors' bytes and confer no actual custody/authority.
    h.REFERENCE_PINS={}
    for name,obj in refs.items():files[name]=enc(obj);h.REFERENCE_PINS[name]=pin(files[name])
    files.update(sources)
    rows=[]
    for i,(path,raw) in enumerate(sorted(overlay.items())):
        name='synthetic_selected_'+str(i);files[name]=raw
        native_before=local.get(path)
        if phase=='merge95' and path==h.VIEWS[1]:native_before=None # Case log was local only before95.
        pre=None if native_before is None else {'mode':'100644','type':'blob','sha':h.native('blob',native_before)}
        rows.append({'path':path,'source':name,**pin(raw),'git_blob':h.native('blob',raw),'preimage':pre})
    local_rows=[]
    for i,path in enumerate(h.VIEWS):
        raw=local[path];name=None if raw is None else 'synthetic_local_pre_'+str(i)
        if name is not None:files[name]=raw
        local_rows.append({'path':path,'preimage':None if raw is None else pin(raw),'source':name})
    m={'schema':'pr209-native-conditional-inputs-v1','PR':209,'problem_id':'5100015','phase':phase,'helper_pin':pin(sources['native209_model.py']),'core_pin':h.CORE_PIN,'executor_pin':pin(sources['native209_future_executor.py']),'expected_parent':'1'*40,'expected_parent_tree':'2'*40,'facts':facts,'files':rows,'reused_blobs':reused,'reused_trees':[{'path':h.SHARED,'mode':'040000','type':'tree','sha':h.SHARED_TREE}],'local_views':local_rows,'commit_message':'Synthetic marker fixture\n','commit_author':{'name':'Synthetic Auditor','email':'fixture@example.invalid','date':'2026-10-17T00:00:00Z'},'commit_committer':{'name':'Synthetic Auditor','email':'fixture@example.invalid','date':'2026-10-17T00:00:00Z'},'candidate_journal':'synthetic_candidate','writer_lock':h.WRITER_LOCK_REFERENCE,'total_files':len(rows),'total_bytes':sum(map(len,overlay.values())),'baseline_pin':h.BASELINE_PIN}
    files['synthetic_manifest']=enc(m);mpin=pin(files['synthetic_manifest'])
    roles={'scientific','priority','whole_package_one','whole_package_two','existing_publication','existing_tracker','custody','PR208_status_skip'}
    if phase=='completion100':roles|={'actual_merge95_acceptance','actual_original_PR_merge','actual_merge95_five_sync'}
    audits=[]
    for i in range(2):
        name='synthetic_source_audit_'+str(i);files[name]=b'Synthetic audit, no Root authority.\n';audits.append({'path':name,**pin(files[name]),'Root_accepted':True,'helper_pin':m['helper_pin'],'executor_pin':m['executor_pin'],'manifest_pin':mpin})
    evidence=h.CASE+'synthetic_evidence.json'
    a={'schema':'pr209-root-native-conditional-model-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':209,'phase':phase,'accepted':True,'manifest_pin':mpin,'helper_pin':m['helper_pin'],'core_pin':h.CORE_PIN,'executor_pin':m['executor_pin'],'facts':facts,'scientific_accepted':True,'priority_accepted':True,'whole_package_reviews_accepted':True,'existing_publication_verified':True,'existing_tracker_verified':True,'native_custody_accepted':True,'no_new_publication_or_tracker_action':True,'original_head':h.ORIGINAL,'prepared_head':h.PREPARED,'prepared_tree':h.PREPARED_TREE,'native_audits':audits,'receipts':{role:{'path':evidence,**pin(overlay[evidence])} for role in roles}}
    files['synthetic_acceptance']=enc(a)
    def synthetic_sealed(name,expected):
        h.rel(name);raw=files[name]
        if pin(raw)!=h.bytepin(expected):raise RuntimeError('Synthetic sealed input pin mismatch')
        return raw
    h.sealed=synthetic_sealed
    try:
        result=h.load_inputs('synthetic_manifest',mpin,'synthetic_acceptance',pin(files['synthetic_acceptance']))
        return {'accepted':True,'error':None,'files':len(result[2]),'logs_keep_local_prefix':all(overlay[p].startswith(local[p]) for p in (h.VIEWS[1],h.VIEWS[4])),'logs_keep_native_prefix':all(overlay[r['path']].startswith(local[r['path']]) for r in rows if r['path'] in (h.VIEWS[1],h.VIEWS[4]) and r['preimage'] is not None)}
    except (RuntimeError,ValueError,KeyError,TypeError,OSError) as error:return {'accepted':False,'error':str(error)}

def run(version):
    good95=fixture(version,'merge95');check(version+'_full_load_phase95',good95['accepted'],good95)
    full100=fixture(version,'completion100')
    if version=='historical':
        check('historical_preserved_95_then_100_refused',not full100['accepted'] and full100['error']=='Exact markdown phase marker',full100)
        def remove_old_marker(h,o,l):
            for p in (h.VIEWS[1],h.VIEWS[4]):o[p]=o[p].replace(marker(h,'merge95')+b'\n',b'')
        no95=fixture(version,'completion100',remove_old_marker)
        check('historical_replace_95_breaks_prefix',not no95['accepted'] and no95['error']=='Research log historical local prefix changed',no95)
        return
    check('repaired_full_load_append95_then100',full100['accepted'] and full100['logs_keep_local_prefix'] and full100['logs_keep_native_prefix'],full100)
    # Every mutable body is tested separately so a failure in another view cannot mask it.
    paths=lambda h:(h.VIEWS[1],h.VIEWS[3],h.VIEWS[4])
    variants={
        'stale95_only':lambda h,raw:raw[:raw.rfind(marker(h,'completion100'))],
        'duplicate100':lambda h,raw:raw+marker(h,'completion100')+b'\n',
        'reordered100_then95':lambda h,raw:raw+marker(h,'merge95')+b'\n',
        'content_after_current':lambda h,raw:raw+b'Later contradictory checkpoint prose.\n',
        'malformed_latest_JSON':lambda h,raw:raw.replace(marker(h,'completion100'),b'<!-- PR209_NATIVE_PHASE_FACTS {bad json} -->'),
        'unknown_latest_fact':lambda h,raw:raw.replace(marker(h,'completion100'),b'<!-- PR209_NATIVE_PHASE_FACTS '+h.compact({**h.phase_facts('completion100'),'unexpected':1}).encode()+b' -->'),
        'float_current_percent':lambda h,raw:raw.replace(marker(h,'completion100'),b'<!-- PR209_NATIVE_PHASE_FACTS '+h.compact({**h.phase_facts('completion100'),'case_workflow_estimate_percent':100.0}).encode()+b' -->'),
        'midline_current':lambda h,raw:raw.replace(marker(h,'completion100'),b'prefix '+marker(h,'completion100')),
        'unknown_phase_facts':lambda h,raw:raw.replace(marker(h,'completion100'),b'<!-- PR209_NATIVE_PHASE_FACTS '+h.compact({**h.phase_facts('completion100'),'case_workflow_estimate_percent':99}).encode()+b' -->'),
        'duplicate_historical95':lambda h,raw:marker(h,'merge95')+b'\n'+(marker(h,'merge95')+b'\n' if marker(h,'merge95') not in raw else b'')+raw,
        'malformed_historical95':lambda h,raw:raw.replace(marker(h,'merge95'),b'<!-- PR209_NATIVE_PHASE_FACTS {bad historical json} -->'),
        'unknown_marker_token':lambda h,raw:raw+b'<!-- PR209_NATIVE_PHASE_FACTS_MALFORMED -->\n',
        'missing_separator_lookalike':lambda h,raw:raw.replace(marker(h,'completion100'),b'<!-- PR209_NATIVE_PHASE_FACTS{bad} -->\n'+marker(h,'completion100')),
        'tab_separator_lookalike':lambda h,raw:raw.replace(marker(h,'completion100'),b'<!-- PR209_NATIVE_PHASE_FACTS\t{bad} -->\n'+marker(h,'completion100')),
        'unknown_stem_suffix_lookalike':lambda h,raw:raw.replace(marker(h,'completion100'),b'<!-- PR209_NATIVE_PHASE_FACTS_MALFORMED -->\n'+marker(h,'completion100')),
    }
    # Case/program logs have95 history; progress can use either one current marker or95→100.
    def progress_history(h,o,l):o[h.VIEWS[3]]=l[h.VIEWS[3]]+b'Completion progress.\n'+marker(h,'completion100')+b'\n'
    check('progress_MD_history95_100_allowed',fixture(version,'completion100',progress_history)['accepted'])
    def trailing(h,o,l):
        for p in paths(h):o[p]+=b'\n\n'
    check('terminal_marker_trailing_empty_lines_allowed',fixture(version,'completion100',trailing)['accepted'])
    for which in range(3):
        for label,mutate in variants.items():
            if label=='malformed_historical95' and which==1:continue
            def change(h,o,l,which=which,mutate=mutate):
                path=paths(h)[which];o[path]=mutate(h,o[path])
            result=fixture(version,'completion100',change)
            check('repaired_'+str(which)+'_'+label+'_refused',not result['accepted'],result)
    for which in (0,2):
        def drop95(h,o,l,which=which):
            path=paths(h)[which];o[path]=o[path].replace(marker(h,'merge95')+b'\n',b'')
        check('append_only_log_'+str(which)+'_historical_marker_not_removable',not fixture(version,'completion100',drop95)['accepted'])
    for which in range(3):
        for label in ('duplicate95','premature100','malformed95','content_after95'):
            def change(h,o,l,which=which,label=label):
                path=paths(h)[which]
                if label=='duplicate95':o[path]+=marker(h,'merge95')+b'\n'
                elif label=='premature100':o[path]+=marker(h,'completion100')+b'\n'
                elif label=='malformed95':o[path]=o[path].replace(marker(h,'merge95'),b'<!-- PR209_NATIVE_PHASE_FACTS {bad} -->')
                else:o[path]+=b'Stale content after active95.\n'
            result=fixture(version,'merge95',change)
            check('merge95_'+str(which)+'_'+label+'_refused',not result['accepted'],result)

if __name__=='__main__':
    if not(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path):raise RuntimeError('Use Python -E -S -B -P')
    run('historical')
    if len(sys.argv)>1 and sys.argv[1]=='historical-only':status='REPRODUCED_HISTORICAL_PHASE_TRANSITION_DEFECT'
    else:run('repaired');status='PASS_SOURCE_ONLY_CONDITIONAL'
    output={'schema':'pr209-independent-phase-transition-source-controls-v1','UTC':datetime.now(timezone.utc).isoformat(),'status':status,'test_count':len(RESULTS),'results':RESULTS,'actual_load_inputs_exercised':True,'synthetic_reference_inputs_and_envelopes_only':True,'external_calls':0,'production_mutations':0,'actual_phase_manifest_created':False}
    dest=BASE/('HISTORICAL_REPRODUCTION.json' if status.startswith('REPRODUCED') else 'PHASE_TRANSITION_RESULTS.json')
    if dest.exists():
        import tempfile,os
        descriptor,name=tempfile.mkstemp(prefix='REPLAY_'+dest.stem+'_',suffix='.json',dir=BASE)
        with os.fdopen(descriptor,'wb') as replay:replay.write(enc(output))
    else:dest.write_bytes(enc(output))
    print(json.dumps({'status':status,'checks':len(RESULTS)},sort_keys=True))
