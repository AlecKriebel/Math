#!/usr/bin/env python3
"""Independent read-only concrete-data audit; imports no integration helper."""
from pathlib import Path
import collections, copy, csv, datetime, hashlib, io, json, os, stat, subprocess, sys, time, zipfile

C = Path(__file__).resolve().parents[4]
A = Path(__file__).resolve().parent.parent
D = A / 'native_publication_integration_plan_20261006/corrected_v5'
Q = D / 'candidate_dfe3e71993e3bd99'
O = Path(__file__).resolve().parent
T = '30003996'
N = Path('unsolved_math_prioritization')
TARGET = N / 'attempts' / T
MAIN = 'f36cb1e34696d460b9cfb5b03425998de48c4669'
ESHA = 'dfe3e71993e3bd99afb9c11e54f4fe4c9117c770849ffac54c7bc2b17e6bd76a'
mode = 'optimized' if sys.flags.optimize else 'normal'
checks = collections.Counter()
readpins = {}
negative_controls = []
git_custody = []
started = datetime.datetime.now(datetime.timezone.utc).isoformat()

def ensure(v, label, group='binding'):
    checks[group] += 1
    if not v:
        raise RuntimeError(label)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def canon(x):
    return json.dumps(x, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(',', ':')).encode()

def control_bytes(x):
    return (json.dumps(x, sort_keys=True, ensure_ascii=False, allow_nan=False, indent=2)+'\n').encode()

def body(p):
    p = Path(p)
    ensure(p.is_file() and not p.is_symlink(), 'nonregular input ' + str(p), 'path')
    b = p.read_bytes()
    pin = {'path': str(p), 'bytes': len(b), 'sha256': sha(b)}
    old = readpins.get(str(p))
    ensure(old is None or old == pin, 'input changed while reviewing ' + str(p), 'custody')
    readpins[str(p)] = pin
    return b

def stream_pin(p):
    p = Path(p)
    ensure(p.is_file() and not p.is_symlink(), 'nonregular stream input', 'path')
    h = hashlib.sha256(); size = 0
    with p.open('rb') as f:
        while True:
            b = f.read(1024 * 1024)
            if not b: break
            size += len(b); h.update(b)
    pin = {'path': str(p), 'bytes': size, 'sha256': h.hexdigest()}
    old = readpins.get(str(p))
    ensure(old is None or old == pin, 'stream changed ' + str(p), 'custody')
    readpins[str(p)] = pin
    return pin

def load(p):
    def reject_duplicate(pairs):
        d = {}
        for k,v in pairs:
            if k in d: raise RuntimeError('duplicate JSON key')
            d[k] = v
        return d
    return json.loads(body(p), object_pairs_hook=reject_duplicate,
                      parse_constant=lambda x: (_ for _ in ()).throw(RuntimeError('nonfinite JSON')))

def match(p, pin):
    b = body(p)
    ensure(len(b) == pin['bytes'] and sha(b) == pin['sha256'], 'pin mismatch ' + str(p), 'pin')
    return b

def match_stream(p, pin):
    q = stream_pin(p)
    ensure(q['bytes'] == pin['bytes'] and q['sha256'] == pin['sha256'], 'stream pin mismatch', 'pin')

def same_except_target(b, a):
    return set(a) == set(b) | {T} and all(canon(b[k]) == canon(a[k]) for k in b if k != T)

def catalog_invariant(b, a):
    if len(b) != len(a): return False
    seen = set()
    for x,y in zip(b,a):
        k = x.get('id')
        if k in seen or k != y.get('id'): return False
        seen.add(k)
        if k != T and canon(x) != canon(y): return False
    x = next(r for r in b if r['id'] == T); y = next(r for r in a if r['id'] == T)
    e = copy.deepcopy(x); e.update(local_status='claimed_solved', turns_used=2, eligible=False, rank=None)
    return canon(e) == canon(y)

def physical_csv(b):
    """Scan physical CR/LF record boundaries independently of helper line logic."""
    records = []; start = 0; i = 0; quoted = False
    while i < len(b):
        c = b[i]
        if c == 34:
            if quoted and i+1 < len(b) and b[i+1] == 34:
                i += 2; continue
            quoted = not quoted
        elif c in (10,13) and not quoted:
            stop = i+1
            if c == 13 and stop < len(b) and b[stop] == 10: stop += 1
            records.append(b[start:stop]); start = stop; i = stop; continue
        i += 1
    if start < len(b): records.append(b[start:])
    if quoted: raise RuntimeError('unterminated quote in actual CSV')
    parsed = []
    for rec in records:
        r = list(csv.reader(io.StringIO(rec.decode('utf-8'), newline=''), strict=True))
        if len(r) != 1: raise RuntimeError('physical CSV scanner disagreement')
        parsed.append(r[0])
    return records, parsed

def csv_invariant(b, a):
    br,bp = physical_csv(b); ar,ap = physical_csv(a)
    if len(br) != len(ar) or br[0] != ar[0]: return False
    header = bp[0]; ids = header.index('id'); changed = set()
    for rb,ra,x,y in zip(br[1:],ar[1:],bp[1:],ap[1:]):
        if len(x) != len(header) or len(y) != len(header) or x[ids] != y[ids]: return False
        if x[ids] != T:
            if rb != ra: return False
        else:
            changed = {header[i] for i in range(len(header)) if x[i] != y[i]}
            expected = dict(zip(header,x)); expected.update(local_status='claimed_solved',turns_used='2',eligible='False',rank='')
            if dict(zip(header,y)) != expected: return False
    return changed == {'local_status','turns_used','eligible','rank'}

def negative(name, predicate, original, changed):
    ensure(predicate(*original), name + ' positive control', 'negative_control')
    ensure(not predicate(*changed), name + ' mutation was accepted', 'negative_control')
    negative_controls.append(name)

E = load(Q/'EXECUTION_INPUTS.json'); e = E['effective']
ensure(sha(body(Q/'EXECUTION_INPUTS.json')) == ESHA, 'actual E SHA')
ensure(body(Q/'EXECUTION_INPUTS.json') == body(D/'EXECUTION_INPUTS_FROZEN_20261006.json'), 'frozen E copy')
ensure(e['main_parent'] == MAIN and E['template_only'] is False, 'actual main binding')
ensure(len(E['input_files']) == 180 and len(E['program_files']) == 5, 'registry sizes')
ensure(len({p['path'] for p in E['input_files']}) == 180, 'registry uniqueness')
for pin in E['program_files']:
    match(C/pin['path'],pin)
for pin in E['input_files']:
    original = match(C/pin['path'],pin)
    suffix = Path(pin['path']).relative_to(A.relative_to(C))
    captured = Q/'bundle'/TARGET/'publication/authenticated_inputs'/suffix
    ensure(match(captured,pin) == original, 'captured registry body differs', 'capture')

cfg = load(Q/'CONFIG.json')
ensure(body(Q/'CONFIG.json') == body(D/'CONFIG_ACTUAL_ROOT_COMMISSIONED_20261006.json'), 'actual config copy')
match(C/cfg['execution_inputs']['path'],cfg['execution_inputs'])
ensure(cfg['template_only'] is False and cfg['commissioned_after_independent_review'] is True, 'commission flags')
gates = {}
registry = {p['path']:p for p in E['input_files']}
for role,pin in cfg['gates'].items():
    g = load(C/pin['path']); match(C/pin['path'],pin); gates[role] = g
    ensure(g['role'] == role and g['PR'] == 108 and g['problem_id'] == 30003996, 'gate role/id')
    ensure(g['execution_inputs_sha256'] == ESHA and g['main_parent'] == MAIN, 'gate E/main')
    for field,value in [('original_budget','2/5'),('new_central_proof_search_turns',0),('effective_proof_sha256','2818eab189445649ae1ba98d55e3da3e5fab918de88f1779de86962ba99a3393'),('package_manifest_sha256','61f08bd60185b6ef2382fb279fe77d59958974c07c4a44976cc7289eafca8c38')]:
        ensure(type(g[field]) is type(value) and g[field] == value, 'gate core field ' + field)
    for field in ['actual_root_review','clearance']: ensure(g[field] is True,'gate clearance')
    for field in ['fixture','simulated','dry_run']: ensure(g[field] is False,'synthetic gate')
    ensure(g['checked_artifacts'] and all(p == registry.get(p['path']) for p in g['checked_artifacts']), 'gate checked input declaration')
    for pin2 in g.get('separately_authenticated_review_evidence_outside_execution_manifest',[]): match(C/pin2['path'],pin2)
    ensure(datetime.datetime.fromisoformat(g['UTC']) < datetime.datetime.fromisoformat('2026-10-06T08:29:33.565117+00:00'),'gate chronology')
ensure(len(gates)==7 and len({g['exact_claim'] for g in gates.values()})==1,'seven common claims')
ensure(gates['final']['gate_sha256']=={r:cfg['gates'][r]['sha256'] for r in cfg['gates'] if r!='final'},'final gate antecedents')
ensure(gates['whole_package_R1']['reviewer_run_id'] != gates['whole_package_R2']['reviewer_run_id'],'independent review identities')
ensure('does not relabel the old R1 run as clean' in gates['whole_package_R1']['historical_R1_interpretation'],'R1 history honesty')

R = load(Q/'CANDIDATE_RECEIPT.json'); offers = R['affected_paths']
ensure(R['execution_inputs_sha256']==ESHA and R['main_parent']==MAIN,'receipt E/main')
ensure(R['actual_operator_PID']==62139 and R['native_worker_process_PID']==62294,'receipt PIDs')
ensure(R['native_assess_executed_in_private_backend'] is True,'native ran')
for field in ['native_export_executed','merge_executed','Git_index_branch_remote_or_service_mutated','publication_executed_by_helper']:
    ensure(R[field] is False,'candidate action boundary')
ensure(R['reviewed_program_sha256']=={Path(p['path']).name:p['sha256'] for p in E['program_files']},'executed program binding')
ensure(len(offers)==275 and len({r['path'] for r in offers})==275,'offered path count')
actual_paths = set()
for p in (Q/'bundle').rglob('*'):
    ensure(not p.is_symlink(),'bundle symlink','path')
    if p.is_file(): actual_paths.add(p.relative_to(Q/'bundle').as_posix())
ensure(actual_paths == {r['path'] for r in offers},'undeclared/absent bundle body')
for r in offers:
    rel=Path(r['path']); ensure(not rel.is_absolute() and '..' not in rel.parts,'unsafe offered path','path')
    match(Q/'bundle'/rel,r['after'])
    if r['before'] is not None: match(C/rel,r['before'])
    else: ensure(not (C/rel).exists(),'offered new file already present')
changed_globals={r['path'] for r in offers if not r['path'].startswith(str(TARGET)+'/')}
ensure(changed_globals == {str(N/n) for n in ['assessments.json','state.json','history.jsonl','assessment_history.jsonl','catalog.json','ranking.csv','summary.json','QUEUE.md']},'exact eight global changes')

baseline={}
for pin in e['native_baseline_pins']:
    p=C/pin['path']
    if p.exists(): baseline[Path(pin['path']).name]=match(p,pin)
    else:
        p=Q/'private_native_backend'/Path(pin['path']).name
        baseline[Path(pin['path']).name]=match(p,pin)
        # Independently retrieve only these three small missing Git blobs.
        argv=[e['runtime']['git_executable'],'show',MAIN+':'+pin['path']]
        st=datetime.datetime.now(datetime.timezone.utc).isoformat(); start=time.monotonic()
        proc=subprocess.Popen(argv,cwd=C,env=e['environment_policy']['git']['environment'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err=proc.communicate(timeout=30)
        ensure(proc.returncode==0 and len(out)<=32768 and len(err)<=4096,'bounded sparse Git read')
        ensure(out==baseline[Path(pin['path']).name],'sparse pinned Git body')
        git_custody.append({'actual_PID':proc.pid,'argv':argv,'cwd':str(C),'UTC_start':st,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':proc.returncode,'reaped':True,'elapsed_seconds':time.monotonic()-start,'stdout_bytes':len(out),'stdout_sha256':sha(out),'retained_stdout_prefix':out[:4096].decode('utf8'),'stderr_bytes':len(err),'stderr_sha256':sha(err)})

oldstate=json.loads(baseline['state.json']); newstate=load(Q/'bundle'/N/'state.json')
oldass=json.loads(baseline['assessments.json']); newass=load(Q/'bundle'/N/'assessments.json')
ensure(T not in oldstate and T in newstate,'target state introduction')
ensure(same_except_target(oldstate,newstate),'unrelated state map','native_map')
ensure(same_except_target(oldass,newass),'unrelated assessment map','native_map')
for k in oldass:
    if k!=T: ensure(canon(oldass[k])==canon(newass[k]),'unrelated full assessment','assessment_row')
for k in oldstate:
    ensure(canon(oldstate[k])==canon(newstate[k]),'unrelated full state','state_row')
for k,v in oldass[T].items(): ensure(canon(v)==canon(newass[T][k]),'historical desk field changed '+k,'target')
added=set(newass[T])-set(oldass[T]); ensure(added=={'clear_holds','reviewed_at','new_central_proof_search_turns','original_budget','original_structured_ledger_present','package_manifest_sha256','publication_DOI'},'assessment added fields')
ensure(newass[T]['clear_holds']=={} and type(newass[T]['clear_holds']) is dict,'clear_holds empty')
ensure(newass[T]['publication_DOI']=='10.5281/zenodo.23181280','target assessment DOI')
imported=load(Q/'bundle'/TARGET/'IMPORT_BASELINE.json')
ensure(canon(newstate[T])==canon(imported),'state/import baseline identity')
ensure(imported['status']=='claimed_solved' and type(imported['turns_used']) is int and imported['turns_used']==2,'target native status/effort')
ensure(imported['original_structured_ledger_present'] is False and imported['new_central_proof_search_turns']==0,'budget no extra search')
ensure('never recovered original event' in imported['original_effort_provenance'],'dated ledger truth')
for filename in ['history.jsonl','assessment_history.jsonl']:
    b=baseline[filename]; a=body(Q/'bundle'/N/filename)
    ensure(a.startswith(b),'historical ledger exact prefix','ledger')
    suffix=a[len(b):]; lines=suffix.splitlines()
    ensure(len(lines)==1 and suffix.endswith(b'\n'),'one append only','ledger')
    event=json.loads(lines[0]); ensure(event['id']==T,'target-only append','ledger')
    if filename=='history.jsonl':
        expected=dict(imported,event='dated_import_of_authenticated_historical_author_count')
        ensure(canon(event)==canon(expected),'history event exact','ledger')
    else: ensure(canon(event)==canon(newass[T]),'assessment event exact','ledger')
ensure(load(Q/'bundle'/TARGET/'HISTORICAL_DESK_ASSESSMENT.json')==oldass[T],'historical desk archive')
ensure(load(Q/'bundle'/TARGET/'assessment.json')==newass[T],'target current assessment')

oldcat=json.loads(baseline['catalog.json']);newcat=load(Q/'bundle'/N/'catalog.json')
ensure(catalog_invariant(oldcat,newcat),'catalog invariant','catalog')
for x,y in zip(oldcat,newcat):
    if x['id']!=T: ensure(canon(x)==canon(y),'unrelated complete catalog row','catalog_row')
ensure(len(oldcat)==15458 and len({r['id'] for r in oldcat})==15458,'catalog count/IDs')
drifts=R['unrelated_catalog_projection_drift_preserved']; projected=[]
for row in oldcat:
    if row['id']==T: continue
    st=oldstate.get(row['id'],{}); status=st.get('status',row['local_status']); turns=st.get('turns_used',0)
    eligible=not row['holds'] and status in ['queued','unreviewed','ready'] and turns<row['turn_limit']
    expected={'local_status':status,'turns_used':turns,'eligible':eligible}
    diff={k:{'before':row[k],'after':v} for k,v in expected.items() if type(row[k]) is not type(v) or row[k]!=v}
    if diff: projected.append((row['id'],diff,eligible))
ensure(len(drifts)==len(projected),'derive drift count rather than trusting 48')
ensure({r['id'] for r in drifts}=={r[0] for r in projected},'drift ID set')
for id_,diff,eligible in projected:
    r=next(r for r in drifts if r['id']==id_)
    ensure(r['difference']==diff and r['expected_eligible'] is eligible and r['baseline_preserved'] is True,'explained projection drift','drift')

oldcsv=baseline['ranking.csv'];newcsv=body(Q/'bundle'/N/'ranking.csv')
ensure(csv_invariant(oldcsv,newcsv),'all physical CSV records unchanged except target','csv')
pr,parsed=physical_csv(oldcsv);nr,nparsed=physical_csv(newcsv)
ensure(len(parsed)==15459 and len(nparsed)==15459,'CSV complete count')
idcol=parsed[0].index('id')
for rb,ra,x in zip(pr[1:],nr[1:],parsed[1:]):
    if x[idcol]!=T: ensure(rb==ra,'unrelated physical CSV span','csv_row')
oldqueue=baseline['QUEUE.md'].splitlines(keepends=True);newqueue=body(Q/'bundle'/N/'QUEUE.md').splitlines(keepends=True)
ensure(len(oldqueue)==len(newqueue),'campaign line count')
changed=[i for i,(b,a) in enumerate(zip(oldqueue,newqueue)) if b!=a]
ensure(len(changed)==1 and b'30003996 / OWR-16633-013' in oldqueue[changed[0]],'campaign target only')
before=oldqueue[changed[0]].decode().split('|');after=newqueue[changed[0]].decode().split('|')
ensure(len(before)==len(after)==14,'campaign columns')
diff={i for i,(b,a) in enumerate(zip(before,after)) if b!=a}
ensure(diff=={8,9,11,12},'campaign four selected cells')
ensure(after[8].strip()=='claimed_solved' and after[9].strip()=='2/5' and after[11].strip()==e['campaign_note'] and after[12].strip()=='https://doi.org/10.5281/zenodo.23181280','campaign exact values')
ensure(body(Q/'private_native_backend/SHORTLIST.md')==baseline['SHORTLIST.md'],'shortlist entire body')
ensure('SHORTLIST.md' not in {Path(r['path']).name for r in offers if r['before'] is not None},'unchanged shortlist not offered')
oldsummary=json.loads(baseline['summary.json']);newsummary=load(Q/'bundle'/N/'summary.json')
expected=copy.deepcopy(oldsummary);expected['eligible']-=1
ensure(canon(newsummary)==canon(expected),'scoped summary only eligible minus one')
ensure(newsummary['eligible']==sum(r['eligible'] for r in newcat),'summary eligibility actual full rows')
holdcounts=collections.Counter(h.split(':')[0] for r in newcat for h in r['holds'])
ensure(dict(holdcounts)==newsummary['holds'],'full hold tally')
ensure(newsummary['records']==len(newcat) and newsummary['assessed']==len(newass),'summary records/assessments')

orig=e['original_authentication_pins']; origroot=A/'original_source_authentication_20261006/original_attempt'
ensure(len(orig['original_files'])==15,'original 15 count')
for pin in orig['original_files']:
    original=match(C/pin['path'],pin);suffix=(C/pin['path']).relative_to(origroot)
    ensure(body(Q/'bundle'/TARGET/'historical_original'/suffix)==original,'original historical exact','original')
for pin in e['effective_diagnostics_pins']:
    original=match(C/pin['path'],pin);suffix=(C/pin['path']).relative_to(A/'repaired_diagnostics_v1')
    if suffix.as_posix() == 'README.md':
        wrapper=body(Q/'bundle'/TARGET/suffix).decode()
        ensure(all(text in wrapper for text in ['Literal status claimed_solved','historical author effort 2/5','No original status.json or turns.jsonl','New central proof-search turns: 0','Imported prior report remains {}','not a fresh global rerank','https://doi.org/10.5281/zenodo.23181280']),'current reviewed native README wrapper')
        captured=Q/'bundle'/TARGET/'publication/authenticated_inputs/repaired_diagnostics_v1/README.md'
        ensure(body(captured)==original,'superseded diagnostic README preserved exactly')
    else: ensure(body(Q/'bundle'/TARGET/suffix)==original,'effective diagnostic exact','diagnostic')
prior=load(Q/'bundle'/TARGET/'prior_imported_report.json')
ensure(type(prior) is dict and prior=={},'exact empty prior not null')
ensure(body(Q/'bundle'/TARGET/'prior_imported_report.json')==match(C/orig['selected_prior']['path'],orig['selected_prior']),'prior exact bytes')
for f in ['status.json','turns.jsonl']:
    ensure(not (Q/'bundle'/TARGET/f).exists() and not (Q/'bundle'/TARGET/'historical_original'/f).exists(),'invented original structured ledger')
pm=load(A/'publication_ready_package_v2/PACKAGE_MANIFEST.json')
ensure(len(pm['files'])==46,'published logical count')
for pin in pm['files']:
    rp=Path(pin['relative_path']); original=match(A/'publication_ready_package_v2'/rp,pin)
    ensure(body(Q/'bundle'/TARGET/'publication/package'/rp)==original,'published payload exact','package')
ensure(body(Q/'bundle'/TARGET/'publication/authenticated_inputs/publication_ready_package_v2/PACKAGE_MANIFEST.json')==body(A/'publication_ready_package_v2/PACKAGE_MANIFEST.json'),'candidate package manifest exact')
ensure(body(Q/'bundle'/TARGET/'publication/EXECUTION_INPUTS.json')==body(Q/'EXECUTION_INPUTS.json'),'native publication frozen manifest exact')
for role,pin in cfg['gates'].items():
    ensure(body(Q/'bundle'/TARGET/'publication/gates'/(role+'.json'))==match(C/pin['path'],pin),'archived concrete gate exact')
archives=list((A/'publication_ready_package_v2').glob('*.zip'));ensure(len(archives)==1,'one support ZIP')
zb=body(archives[0]);ensure(len(zb)==151513 and sha(zb)=='66f7d7e25370062e0f70b7fdce538dc90a5a264957557714f11d1ac42ebc14aa','published ZIP bytes')
with zipfile.ZipFile(io.BytesIO(zb)) as z:
    expected={r['relative_path'] for r in pm['files']}|{'PACKAGE_MANIFEST.json'}
    ensure(len(z.infolist())==47 and set(z.namelist())==expected,'ZIP exact members')
    for name in expected:
        expectedbody=body(A/'publication_ready_package_v2'/name)
        ensure(z.read(name)==expectedbody,'ZIP member unchanged','archive')

control=load(Q/'WORKER_CONTROL.json');result=load(Q/'WORKER_RESULT.json')
ensure(result['outcome']=='success' and result['native_function']=='queue.py:assess' and result['native_assess_returned_without_exception'] is True,'worker actual assess result')
ensure(result['actual_operator_PID']==62294 and result['execution_inputs_sha256']==ESHA,'worker PID/E')
ensure(result['validated_worker_control']==control,'returned full control')
ensure(result['worker_control_binding_sha256']==sha(control_bytes(control)),'canonical full control binding')
ensure(control['execution_inputs_sha256']==ESHA and control['worker_policy']==e['worker_policy'],'control frozen policy')
ensure(result['requested_resource_policy']==e['worker_policy'],'requested resource policy binding')
ensure(result['applied_limits']=={'RLIMIT_CPU':[90,90],'RLIMIT_FSIZE':[33554432,33554432],'RLIMIT_NOFILE':[32,32]},'actual exact enforceable limits')
ensure(result['hard_memory_limit_claimed'] is False and result['memory_policy']['hard_memory_limit_claimed'] is False and result['memory_policy']['RLIMIT_AS_enforcement_certified'] is False,'memory claim honest')
ensure(result['SQL_connection']=='mode=ro&immutable=1','read-only SQL result')
ensure(control['ROOT']==str(Q/'private_native_backend') and result['ROOT']==control['ROOT'],'worker private output')
ensure(control['queue_py_sha256']==e['queue_py_sha256']==result['queue_py_sha256'],'queue code pinned')
ensure(control['dataset_revision']=='37e53eabe540fb458758e198be61634bd02ee008' and control['record_count']==15458,'dataset scope')
caps={Path(r['path']).name:r['bytes']+(0 if Path(r['path']).name in ['queue.py','manifest.json','policy.json'] else 524288) for r in e['native_baseline_pins']};caps['assessment.json']=131072
ensure(control['backend_file_caps']==caps,'derived all native caps')
for p in (Q/'private_native_backend').iterdir():
    ensure(p.is_file() and not p.is_symlink() and p.name in caps and p.stat().st_size<=caps[p.name],'private backend declared cap','capacity')
for pin in e['native_baseline_pins']:
    name=Path(pin['path']).name
    if name not in ['queue.py','manifest.json','policy.json','SHORTLIST.md']:ensure(body(Q/'private_native_backend'/name)==body(Q/'bundle'/N/name),'private final native/candidate body','native_copy')

P=load(Q/'PROCESS_JOURNAL.json');records=P['records']
ensure(P['actual_operator_PID']==62139 and len(records)==40 and len({r['PID'] for r in records})==40,'actual journal PID/count')
worker=[r for r in records if r['executable_role']=='python'];ensure(len(worker)==1 and worker[0]['PID']==62294,'unique worker process')
for r in records:
    ensure(type(r['PID']) is int and r['PID']>1 and r['actual_process_record'] is True and r['fixture'] is False,'actual process type','process')
    ensure(r['exit_code']==0 and r['child_reaped'] is True and r['output_complete'] is True and r['termination_reason'] is None and r['SIGKILL_attempted'] is False,'actual process exit/reaping','process')
    start=datetime.datetime.fromisoformat(r['UTC_start']);end=datetime.datetime.fromisoformat(r['UTC_end'])
    ensure(0<=(end-start).total_seconds()<r['deadline_seconds'],'process deadline custody','process')
    role=r['executable_role'];ensure(role in ['git','gh','python'],'process role','process')
    ensure(r['ambient_environment_inherited'] is False and r['effective_nonsecret_environment']==e['environment_policy'][role]['environment'],'exact nonambient role environment','process')
    ensure(r['argv'][0]==e['runtime'][role+'_executable'] and r['cwd']==str(C),'process executable/cwd','process')
    for stream in ['stdout','stderr']:
        m=r[stream];raw=body(Q/m['retained_path']);ensure(len(raw)==m['retained_bytes'] and sha(raw)==m['retained_sha256'],'retained stream body','process')
        ensure(m['bytes_observed']<=r['stream_read_caps'][stream] and m['retained_bytes']==min(4096,m['bytes_observed']),'observed bounded stream','process')
        if m['bytes_observed']<=4096:ensure(m['sha256_observed']==sha(raw),'complete observed small stream SHA','process')
ensure(worker[0]['argv']==[e['runtime']['python_executable'],'-E','-S','-B',str(D/'native_assess_worker.py'),'--control',str(Q/'WORKER_CONTROL.json')],'worker exact clean argv')
ensure(worker[0]['deadline_seconds']==120 and e['worker_policy']['deadline_seconds']==120,'worker requested deadline')
ensure(datetime.datetime.fromisoformat(worker[0]['UTC_start'])<=datetime.datetime.fromisoformat(result['UTC_start'])<=datetime.datetime.fromisoformat(result['UTC_end'])<=datetime.datetime.fromisoformat(worker[0]['UTC_end']),'worker receipt nested actual process chronology')
for pin in e['native_baseline_pins']:
    records_for=[r for r in records if r['argv'][1:]==['show',MAIN+':'+pin['path']]]
    ensure(len(records_for)==1,'one pinned baseline Git body process')
    m=records_for[0]['stdout'];ensure(m['bytes_observed']==pin['bytes'] and m['sha256_observed']==pin['sha256'],'actual Git baseline fullstream count/SHA')
outer=A/'actual_operations/native_V5_actual_private_candidate'; outerreceipt=load(outer/'execution.json');outerstart=load(outer/'started.json')
ensure(outerreceipt['child_PID']==62139 and outerreceipt['exit_code']==0 and outerreceipt['cwd']==str(C),'outer actual PID/exit/cwd')
ensure(outerreceipt['argv']==['/usr/bin/env','-i','PATH=/usr/bin:/bin','LC_ALL=C','LANG=C','TZ=UTC','__CF_USER_TEXT_ENCODING=0x1F5:0x0:0x0','/bin/sh',str(D/'launch_review_bundle.sh'),e['runtime']['python_executable'],str(D/'CONFIG_ACTUAL_ROOT_COMMISSIONED_20261006.json')],'outer exact clean launcher')
ensure(outerstart['recorder_PID']==outerreceipt['recorder_PID'] and outerstart['argv']==outerreceipt['argv'] and outerstart['UTC_start']==outerreceipt['UTC_start'] and outerstart['cwd']==outerreceipt['cwd'],'outer started/final custody')
for stream in ['stdout','stderr']:match(outer/outerreceipt[stream]['path'],outerreceipt[stream])
ensure(datetime.datetime.fromisoformat(outerreceipt['UTC_start'])<datetime.datetime.fromisoformat(records[0]['UTC_start'])<datetime.datetime.fromisoformat(records[-1]['UTC_end'])<datetime.datetime.fromisoformat(outerreceipt['UTC_end']),'outer process chronology')

# Configuration and shared source bodies are streamed only; SQL is never opened.
for pin in e['environment_policy']['git']['repository_config_pins']+e['environment_policy']['gh']['config_pins']:match_stream(pin['path'],pin)
for role in ['python','git','gh']:match_stream(e['runtime'][role+'_executable'],e['runtime'][role+'_binary'])
cache=Path(control['SQL_cache']);match_stream(cache,e['source_cache_pin'])
for name,pin in e['raw_source_pins'].items():match_stream(cache.parent/name,pin)

plan=load(A/'ROOT_PROPOSED_NATIVE_EXPORT_PLAN_20261006.json');privacy=load(A/'native_actual_input_preparation_v2_20261006/draft_dfe3e71993e3bd99/PRIVATE_EXPORT_EXCLUSIONS.json')
excluded={r['candidate_affected_path'] for r in privacy['exclusions']}
expected_private={str(TARGET/'publication/authenticated_inputs/actual_operations'/label/'stdout.bin') for label in ['tracker_postpub_metadata','tracker_postpub_DOI_dedup']}
ensure(excluded==expected_private and len(excluded)==2,'exact two private exclusions')
ensure(plan['offers_to_export']==[r for r in offers if r['path'] not in excluded],'exact export offer subsequence')
ensure(len(plan['offers_to_export'])==273 and set(plan['private_offers_to_omit'])==excluded,'273 public offers')
ensure(plan['candidate_receipt_sha256']==sha(body(Q/'CANDIDATE_RECEIPT.json')) and plan['execution_inputs_sha256']==ESHA and plan['main_parent']==MAIN,'export candidate/E/main binding')
note=plan['added_operational_exclusions_note'];note_bytes=match(C/note['source_path'],note);note_data=json.loads(note_bytes)
ensure(note['target_path']==str(TARGET/'publication/PUBLIC_OPERATIONAL_BODY_EXCLUSIONS.json'),'single added note destination')
ensure(note_data['omitted_public_operational_bodies']==privacy['exclusions'] and note_data['execution_inputs_sha256']==ESHA,'operational note exact exclusions/E')
ensure(note_data['private_Git_GH_configuration_or_credential_bodies_published'] is False and 'authorized access' in note_data['operational_replay_limit'] and 'All46 published logical files' in note_data['scientific_package'],'explicit public replay limitation')
ensure(all(p['path'] not in {r['path'] for r in E['input_files']} for p in e['environment_policy']['gh']['config_pins']+e['environment_policy']['git']['repository_config_pins']),'no private runtimeconfig in offered registry')
ensure(all(not (Q/'bundle'/Path(r['path'])).exists() for r in e['environment_policy']['gh']['config_pins']),'credential config not bundled by absolutepath')
cap=load(Q/'CAPACITY_PLAN.json');entries={r['path']:r['max_bytes'] for r in cap['entries']}
ensure(len(entries)==len(cap['entries']),'capacity destinations unique')
actual_files=[p for p in Q.rglob('*') if p.is_file()]
ensure(all(not p.is_symlink() for p in actual_files),'candidate symlink free')
ensure(len(actual_files)<=cap['file_count_cap']==427,'actual file count cap')
for p in actual_files:
    rp=p.relative_to(Q).as_posix();ensure(rp in entries and p.stat().st_size<=entries[rp],'actual artifact declared cap '+rp,'capacity')
ensure(sum(p.stat().st_size for p in actual_files)<=cap['max_materialized_bytes'],'actual total materialized cap')
ensure(cap['required_free_bytes']==cap['max_materialized_bytes']+cap['headroom_bytes']+cap['future_commit_overhead_bytes']+cap['runtime_overhead_bytes'],'complete reserved capacity')

# Independent semantic and resource binding mutation controls, in both modes.
m=copy.deepcopy(newass);m[next(k for k in oldass if k!=T)]['impact']=999
negative('unrelated assessment field',same_except_target,(oldass,newass),(oldass,m))
m=copy.deepcopy(newstate);m[next(iter(oldstate))]['turns_used']=999
negative('unrelated state field',same_except_target,(oldstate,newstate),(oldstate,m))
m=copy.deepcopy(newcat);m[0]['rank']=987654
negative('unrelated rank field',catalog_invariant,(oldcat,newcat),(oldcat,m))
m=copy.deepcopy(newcat);m[0],m[1]=m[1],m[0]
negative('unrelated full row position',catalog_invariant,(oldcat,newcat),(oldcat,m))
m=copy.deepcopy(newcat);next(r for r in m if r['id']==T)['turns_used']=0
negative('original two turns cannot reset',catalog_invariant,(oldcat,newcat),(oldcat,m))
m=newcsv.replace(b'rank,id,',b'RANK,id,',1)
negative('CSV physical header',csv_invariant,(oldcsv,newcsv),(oldcsv,m))
m=newcsv.replace(b'Gradient-Path',b'Gradient_Path',1)
negative('CSV unrelated physical body',csv_invariant,(oldcsv,newcsv),(oldcsv,m))
def policybound(c,r):
    return canon(c['worker_policy'])==canon(e['worker_policy']) and canon(r['requested_resource_policy'])==canon(e['worker_policy']) and canon(r['validated_worker_control'])==canon(c) and r['worker_control_binding_sha256']==sha(control_bytes(c)) and r['execution_inputs_sha256']==ESHA and r['actual_operator_PID']==worker[0]['PID'] and r['applied_limits']=={'RLIMIT_CPU':[90,90],'RLIMIT_FSIZE':[33554432,33554432],'RLIMIT_NOFILE':[32,32]}
for field,value in [('cpu_seconds',2),('file_size_bytes',4096),('open_files',99)]:
    c=copy.deepcopy(control);c['worker_policy'][field]=value
    negative('control '+field,policybound,(control,result),(c,result))
r=copy.deepcopy(result);r['applied_limits']['RLIMIT_CPU']=[2,2]
negative('returned applied resource mismatch',policybound,(control,result),(control,r))
r=copy.deepcopy(result);r['execution_inputs_sha256']='0'*64
negative('returned frozen execution mismatch',policybound,(control,result),(control,r))
r=copy.deepcopy(result);r['actual_operator_PID']=1
negative('returned worker PID mismatch',policybound,(control,result),(control,r))

# Confirm materialized live native baseline has not changed during review.
for pin in e['native_baseline_pins']:
    if (C/pin['path']).exists(): match(C/pin['path'],pin)
for pin in E['program_files']+E['input_files']:match(C/pin['path'],pin)
receipt={'schema':'pr108-independent-actual-native-candidate-audit/v1','actual_operator_PID':os.getpid(),'python_optimized':bool(sys.flags.optimize),'mode':mode,'UTC_start':started,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate_receipt_sha256':sha(body(Q/'CANDIDATE_RECEIPT.json')),'execution_inputs_sha256':ESHA,'main_parent':MAIN,'check_count':sum(checks.values()),'checks_by_group':dict(checks),'all275_private_offers_verified':True,'exact273_plus_one_public_export_plan_verified':True,'unrelated_full_catalog_rows':15457,'physical_unrelated_CSV_records':15457,'original_historical_files':15,'published_logical_files':46,'support_ZIP_members':47,'captured_nongate_inputs':180,'actual_helper_PID':62139,'actual_worker_PID':62294,'actual_child_processes_verified':40,'independently_derived_projection_drifts':len(projected),'negative_controls':negative_controls,'native_or_service_or_Git_mutation':False,'helper_or_native_code_imported':False,'SQL_queries':0,'resource_application':False,'export_or_merge_cleared':False,'private_body_disclosure_or_copy':False}
(O/(mode+'_RECEIPT.json')).write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
(O/(mode+'_READ_PINS.json')).write_text(json.dumps(list(readpins.values()),indent=2,sort_keys=True)+'\n')
(O/(mode+'_READ_ONLY_GIT_CUSTODY.json')).write_text(json.dumps(git_custody,indent=2,sort_keys=True)+'\n')
print(json.dumps({'mode':mode,'actual_PID':os.getpid(),'checks':sum(checks.values()),'negative_controls':len(negative_controls),'verdict':'PASS','readpins':len(readpins)}))
