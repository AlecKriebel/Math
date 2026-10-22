"""Offline fault probes. All subprocess requests are mocked; all writes stay here."""
import contextlib, hashlib, importlib.util, io, json, pathlib, shutil, sys
from types import SimpleNamespace

HERE = pathlib.Path(__file__).resolve().parent
SOURCE = HERE.parent / 'run_service.py'
spec = importlib.util.spec_from_file_location('driver_under_review', SOURCE)
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)

def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n')

def fixture(name):
    root = HERE / name
    if root.exists():shutil.rmtree(root)
    d = root / 'program'; r = d / 'service'; a = d / 'audits' / 'pr1033'
    r.mkdir(parents=True, exist_ok=True); a.mkdir(parents=True, exist_ok=True)
    driver.D, driver.R, driver.REPO = d, r, root
    manifest = a / 'manifest.json'; seal = a / 'seal.json'; asset = a / 'asset'
    dump(manifest, {'metadata': {'title': 'Reviewed title', 'description': 'Reviewed description'}, 'files': []})
    dump(seal, {'publication_ready': True}); asset.write_text('reviewed bytes')
    metadata = json.loads(manifest.read_text())['metadata']
    cfg = {'pr': 1033, 'audit_folder': str(a.relative_to(d)), 'manifest': str(manifest.relative_to(d)),
           'final_seal': str(seal.relative_to(d)), 'manifest_identity': driver.ident(manifest),
           'final_seal_identity': driver.ident(seal),
           'files': [{'path': str(asset.relative_to(d)), **driver.ident(asset)}],
           'metadata_sha256': hashlib.sha256(json.dumps(metadata, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
           'fresh_complete_reviews': 2, 'head': 'a'*40, 'title': 'Reviewed title', 'problem_id': '100',
           'accepted_scope': 'Scoped claim', 'limitations': 'Priority UNKNOWN',
           'pr_title': 'Accept 100: Reviewed title', 'tracker_original_problem': 'Problem100', 'tracker_notes': 'Reviewed notes'}
    dump(r/'PR1033_SERVICE_CONFIG.json', cfg)
    dump(d/'STATE.json', {'next_pr':1033, 'completed_prs':[1001,1024,1025,1031],
                         'candidate_full_claim_prs':[1001,1024,1025,1031,1033,1034],
                         'accepted_results':[], 'publications':[]})
    dump(d/'CLAIM_REGISTRY.json', {'records':[{'pr':1033,'workflow_outcome':'PENDING'}]})
    (d/'README.md').write_text('Initial readme\n'); (d/'RESEARCH_LOG.md').write_text('Initial log\n')
    o=a/'service_receipts_20261016';o.mkdir(exist_ok=True)
    dump(o/'TRACKER_VERIFIED.json', {'doi':'10.5281/zenodo.1','read_back_exact':True,'sheet_row':100})
    dump(o/'MERGE_VERIFIED.json', {'head':cfg['head'],'merge_commit':'b'*40,'merged_at':'2026-10-16T00:00:00Z'})
    pub={'environment':'production','state':'published','title':cfg['title'],'doi':'10.5281/zenodo.1',
         'doi_url':'https://doi.org/10.5281/zenodo.1','record_url':'https://zenodo.org/records/1',
         'doi_resolution':{'status':'resolved'}}
    pr={'head':{'sha':cfg['head']},'state':'closed','merged':True,'merge_commit_sha':'b'*40,
        'merged_at':'2026-10-16T00:00:00Z','draft':False,'title':'Original title','body':'Original description'}
    calls=[]
    def fake(argv, **kwargs):
        argv=list(map(str,argv)); calls.append(argv)
        if 'inspect' in argv: result=pub
        elif argv[0]==driver.GH and argv[1:2]==['api'] and argv[-1].startswith('repos/AlecKriebel/Math/pulls/'): result=pr
        elif argv[0]==driver.GH and 'commits/' in argv[-1]:result={'parents':[{'sha':cfg['head']},{'sha':'c'*40}]}
        elif argv[0]==driver.GH and 'PATCH' in argv:
            update=json.loads(pathlib.Path(argv[-1]).read_text()); pr.update(update); result=pr
        elif argv[0]==driver.GH and argv[1:3]==['pr','merge']:
            return SimpleNamespace(returncode=1, stdout='', stderr='Mock merge rejected by policy')
        else: raise AssertionError('Unexpected external call: '+repr(argv))
        return SimpleNamespace(returncode=0, stdout=json.dumps(result), stderr='')
    driver.subprocess.run=fake
    return d,o,pr,calls

def invoke(step):
    sys.argv=['run_service.py','1033',step]
    out=io.StringIO()
    try:
        with contextlib.redirect_stdout(out):driver.main()
        return {'outcome':'returned','stdout':out.getvalue()}
    except Exception as e:
        return {'outcome':'raised','type':type(e).__name__,'message':str(e),'stdout':out.getvalue()}

results=[]
# Fault after STATE has been saved, before registry persistence.
d,o,pr,calls=fixture('checkpoint_interruption')
real_save=driver.save
def interrupted_save(path,value):
    if path.name=='CLAIM_REGISTRY.json':raise OSError('Mock disk failure after STATE commit')
    return real_save(path,value)
driver.save=interrupted_save
first=invoke('complete'); driver.save=real_save
second=invoke('complete')
results.append({'probe':'checkpoint_partial_then_retry','first':first,'retry':second,
                'state':json.loads((d/'STATE.json').read_text()),
                'registry':json.loads((d/'CLAIM_REGISTRY.json').read_text()),
                'research_log':(d/'RESEARCH_LOG.md').read_text()})
assert first['outcome']=='raised' and second['outcome']=='returned'
assert json.loads((d/'STATE.json').read_text())['next_pr']==1034
assert json.loads((d/'CLAIM_REGISTRY.json').read_text())['records'][0]['workflow_outcome']=='PENDING'
assert (d/'RESEARCH_LOG.md').read_text()=='Initial log\n'

# PATCH succeeds, merge is rejected; retry mutates body before refusing old merge intent.
d,o,pr,calls=fixture('merge_retry_body')
pr.update({'state':'open','merged':False})
first=invoke('merge'); body1=pr['body']; second=invoke('merge'); body2=pr['body']
results.append({'probe':'merge_retry_duplicates_body','first':first,'retry':second,
                'first_accepted_header_count':body1.count('## Accepted result and published preprint'),
                'retry_accepted_header_count':body2.count('## Accepted result and published preprint'),
                'patch_count':sum('PATCH' in c for c in calls),
                'merge_count':sum(c[1:3]==['pr','merge'] for c in calls)})
assert body1.count('## Accepted result and published preprint')==1
assert body2.count('## Accepted result and published preprint')==2
assert 'Previous mutation intent exists' in second['message']

# Merge uses a historic tracker receipt without asking Google Sheets for the current row.
d,o,pr,calls=fixture('stale_tracker')
pr.update({'state':'open','merged':False})
result=invoke('merge')
results.append({'probe':'merge_accepts_stale_tracker_receipt','result':result,
                'gws_calls':sum(c[0]==driver.GWS for c in calls),
                'merge_attempts':sum(c[1:3]==['pr','merge'] for c in calls),
                'fixture_condition':'Tracker receipt is old; real row may since have been edited/deleted. No current spreadsheet response is consumed.'})
assert sum(c[0]==driver.GWS for c in calls)==0
assert sum(c[1:3]==['pr','merge'] for c in calls)==1

# Same reviewed head, different base branch: no main-target guard exists.
d,o,pr,calls=fixture('retargeted_base')
pr.update({'state':'open','merged':False,'base':{'ref':'other-branch','repo':{'full_name':'AlecKriebel/Math'}}})
result=invoke('merge')
results.append({'probe':'same_head_other_base_merge_attempted','result':result,
                'base':pr['base'],'merge_attempts':sum(c[1:3]==['pr','merge'] for c in calls)})
assert sum(c[1:3]==['pr','merge'] for c in calls)==1

# Head drift blocks before any external publication action.
d,o,pr,calls=fixture('head_drift')
pr.update({'state':'open','merged':False,'head':{'sha':'d'*40}})
result=invoke('stage')
assert 'PR head changed' in result['message']
assert not (o/'STAGE_INTENT.json').exists()
results.append({'probe':'head_drift_blocks_stage','result':result,'external_mutation_attempts':0})

# An uncertain draft creation without a saved ID is never blindly repeated.
d,o,pr,calls=fixture('uncertain_stage')
pr.update({'state':'open','merged':False})
original_fake=driver.subprocess.run
def uncertain_stage(argv, **kwargs):
    argv=list(map(str,argv))
    if 'stage' in argv:
        calls.append(argv)
        return SimpleNamespace(returncode=1,stdout='',stderr='Mock lost draft creation response')
    return original_fake(argv,**kwargs)
driver.subprocess.run=uncertain_stage
first=invoke('stage');second=invoke('stage')
assert sum('stage' in c for c in calls)==1
assert 'do not restage' in first['message'] and 'Previous mutation intent exists' in second['message']
results.append({'probe':'uncertain_stage_no_duplicate','first':first,'retry':second,
                'native_stage_requests':sum('stage' in c for c in calls)})

# A failed append response is reconciled from the raw row; rerun does not append.
d,o,pr,calls=fixture('uncertain_append')
original_fake=driver.subprocess.run
remote_rows=[['Original Problem','Solution Chat URL','DOI','Notes']]
def uncertain_append(argv,**kwargs):
    argv=list(map(str,argv))
    if argv[0]!=driver.GWS:return original_fake(argv,**kwargs)
    calls.append(argv)
    if 'append' in argv:
        remote_rows.extend(json.loads(argv[argv.index('--json')+1])['values'])
        return SimpleNamespace(returncode=1,stdout='',stderr='Mock lost successful append response')
    result={'values':remote_rows} if 'values' in argv else {'sheets':[{'properties':{'sheetId':driver.GID,'title':'Tracker'}}]}
    return SimpleNamespace(returncode=0,stdout=json.dumps(result),stderr='')
driver.subprocess.run=uncertain_append
first=invoke('track');second=invoke('track')
assert first['outcome']==second['outcome']=='returned'
assert sum('append' in c for c in calls)==1
results.append({'probe':'uncertain_append_reconciles_no_duplicate','first':first,'retry':second,
                'append_requests':sum('append' in c for c in calls)})
dump(HERE/'PROBE_RESULTS.json',{'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                              'all_subprocess_calls_mocked':True,'all_writes_under_review_folder':True,'results':results})
print(json.dumps({'status':'PASS_FOUR_COUNTEREXAMPLES_THREE_POSITIVE_CONTROLS','probes':len(results)}))
