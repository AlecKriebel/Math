"""Independent read-only acceptance predicates and exact diagnostic controls.

No foreign/candidate code is imported, compiled, evaluated or executed.
"""
from pathlib import Path, PurePosixPath
from fractions import Fraction as F
import collections, datetime, hashlib, json, math, os, sqlite3, stat

OWN = Path.cwd().resolve()
AUDIT = OWN.parent
REPO = AUDIT.parents[2]
C = AUDIT/'reviewed_candidate'
checks = []
started = datetime.datetime.now(datetime.timezone.utc).isoformat()

def ok(condition, name, detail=None):
    checks.append({'name':name, 'passed':bool(condition), 'detail':detail})
    if not condition: raise AssertionError(name)

def h(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def strict(raw):
    def pairs(items):
        d={}
        for k,v in items:
            if k in d: raise ValueError('duplicate key '+k)
            d[k]=v
        return d
    def constant(v): raise ValueError('nonfinite '+v)
    def floating(v):
        n=float(v)
        if not math.isfinite(n): raise ValueError('overflow float')
        return n
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=constant,parse_float=floating)

def j(p): return strict(Path(p).read_bytes())
def eq(a,b):
    return json.dumps(a,sort_keys=True,allow_nan=False,separators=(',',':')) == json.dumps(b,sort_keys=True,allow_nan=False,separators=(',',':'))

def time(s):
    t=datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
    if t.utcoffset()!=datetime.timedelta(0): raise ValueError('not UTC')
    return t

def identity(root,row):
    p=root/row['path']
    return p.is_file() and not p.is_symlink() and p.stat().st_size==row['bytes'] and h(p)==row['sha256']

ledger=j(OWN/'WHOLE_SOURCE_READ_LEDGER.json')
for r in ledger['reads']:
    p=Path(r['path'])
    ok(p.stat().st_size==r['bytes'] and h(p)==r['sha256'],'entire-read input remains same',r['path'])
    if p.suffix=='.json': j(p)
    if p.suffix=='.jsonl':
        for line in p.read_bytes().splitlines(): strict(line)
ok(True,'all individually read JSON/JSONL strict duplicate/finite parse')

m=j(C/'MANIFEST.json')
files={str(p.relative_to(C)) for p in C.rglob('*') if p.is_file()}
dirs={str(p.relative_to(C)) for p in C.rglob('*') if p.is_dir()}
required_dirs={str(p) for f in files for p in PurePosixPath(f).parents if str(p)!='.'}
ok(files=={r['path'] for r in m['files']}|{'MANIFEST.json'} and dirs==required_dirs,'candidate exact files and directories')
ok(all(not p.is_symlink() and stat.S_ISREG(p.stat().st_mode) and stat.S_IMODE(p.stat().st_mode)==0o444 for p in C.rglob('*') if p.is_file()),'candidate every exact full permission 0444')
snap=j(C/'original_snapshot_manifest.json')
ok(snap['head']=='86be0f85c7a37a5cad8d24abd16a32d8d1f27e62' and snap['base']=='60292bed09f59236aa192cb17aa138f7b4750e1a','original identity')
for r in snap['files']:
    p=C/'original_archive'/r['path']
    ok(p.read_bytes()==(AUDIT/'source_snapshot'/r['path']).read_bytes() and p.stat().st_size==r['size'] and h(p)==r['sha256'],'original16 whole archive exact',r['path'])
diff=(C/'original_diff.patch').read_bytes()
ok(len(diff)==54344 and len(diff.splitlines())==957 and diff.count(b'diff --git ')==17 and h(C/'original_diff.patch')==snap['diff_sha256'],'whole original957-line17-pathdiff')
immutable=['SOURCE_STATUS.md','check_normalization.py','check_results.json','source_record.json','source_checksums.json','turns.jsonl','review/author_replay/check_normalization.py','review/author_replay/check_results.json','review/independent_checks.py','review/independent_results.json']
for n in immutable: ok((C/n).read_bytes()==(C/'original_archive'/n).read_bytes(),'current immutable exact',n)
ok((C/'turns.jsonl').read_bytes()==b'','zero original and current turns ledger')
qual=(C/'SOURCE_PRECISION_QUALIFICATIONS.md').read_bytes()
for n,original in [('CURRENT_SOURCE_STATUS.md','SOURCE_STATUS.md'),('SOURCE_AUDIT.md','SOURCE_AUDIT.md'),('review/REVIEW.md','review/REVIEW.md')]:
    b=(C/n).read_bytes()
    ok(b.startswith(qual+b'\nHistorical literal body follows.') and b.endswith((C/'original_archive'/original).read_bytes()),'current proof/history wrapper full literal body',n)
ok(eq(j(C/'status.json'),j(C/'readiness.json')) and eq(j(C/'status.json'),j(C/'review/verdict.json')) and eq(j(C/'status.json'),j(C/'review/review_summary.json')),'all four current scopes exact typed equality')
state=j(C/'status.json')
ok(all(state[k] is None for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict']) and all(state[k] is False for k in ['full_problem_solved_by_project','novelty_claimed','historical_runtime_certified','historical_verdict_transferred','human_referee_review_claimed','paper_created','new_DOI_created','tracker_row_created']),'all current null/false fields precise')
ok(all(type(state[k]) is int and state[k]==0 for k in ['original_substantive_attempts','new_substantive_attempts','audit_turns']) and type(state['substantive_attempt_limit']) is int and state['substantive_attempt_limit']==5,'zero attempt accounting and typedfive')
ok(state['status']=='already_solved' and state['current_gate']=='PENDING_NEW_WHOLE_CURRENT_SOURCE_FIRST_ADVERSARY','historical frozen current gate remains pending')

repro=AUDIT/'root_original_actual_reproduction'
result=j(repro/'RESULT.json')
saved=j(C/'check_results.json'); ind=j(C/'review/independent_results.json')
ok(eq(result['entire_historical_author_result'],saved) and eq(result['entire_original_independent_result'],ind) and eq(result['entire_current_author_result'],dict(saved,source_status_sha256=h(C/'SOURCE_STATUS.md'))),'entire typed root reproductions match versioned originals')
old=(repro/'historical_source_status.md').read_bytes()
ok(old.count(b'Separate adversarial review of this identification is pending.')==1 and old.replace(b'Separate adversarial review of this identification is pending.',b'Separate adversarial AI review of this identification passed; see [the report](review/REVIEW.md).',1)==(C/'SOURCE_STATUS.md').read_bytes(),'exact one status sentence historical difference')
ok(type(saved['assertions']) is int and saved['assertions']==527 and type(ind['assertions']) is int and ind['assertions']==664 and all(type(v) is int for v in ind['checks'].values()) and sum(ind['checks'].values())==664,'every finite diagnostic count type')
for r in result['actual_outer_runs']:
    ok(r['actual_execution'] is True and r['completed'] is True and type(r['pid']) is int and r['pid']>0 and type(r['exit_code']) is int and r['exit_code']==0 and time(r['started_utc'])<=time(r['finished_utc']),'actual original process/clocks',r['pid'])
    for name in ['source','stdout','stderr','output_file']: ok(identity(repro,r[name]),'complete original capture member',r[name]['path'])
    ok((repro/r['stderr']['path']).read_bytes()==b'' and eq(j(repro/r['stdout']['path']),j(repro/r['output_file']['path'])),'complete actual stdout matches full result')
ok((repro/'historical_author_private/check_results.json').read_bytes()==(C/'check_results.json').read_bytes() and (repro/'original_independent_private/actual_capture/stdout.bin').read_bytes()==(C/'review/independent_results.json').read_bytes(),'historical author and independent full byte exact')

ref=j(C/'CURRENT_EXECUTION_REFERENCE.json')
outer=AUDIT/ref['audit_relative_outer_capture']; inner=AUDIT/ref['audit_relative_inner_attempt']
cap=j(outer/'CAPTURE.json'); pre=j(outer/'OPERATION_PRELAUNCH.json'); invocation=j(inner/'INVOCATION.json')
ok(cap['completed'] is True and cap['actual_execution'] is True and type(cap['exit_code']) is int and cap['exit_code']==0 and cap['pid']==invocation['pid']==ref['actual_builder_pid']==68759 and cap['operator_pid']==invocation['parent_pid']==ref['outer_parent_pid']==68758,'actual final current builder parent/child/exit')
ok(time(cap['started_utc'])<=time(invocation['utc'])<=time(cap['finished_utc']),'actual current nested clocks')
for channel in ['stdout','stderr']: ok(identity(outer,cap[channel]),'whole final current stream',channel)
ok((outer/'stderr.bin').read_bytes()==b'' and j(outer/'stdout.bin')['manifest_sha256']==h(C/'MANIFEST.json'),'final current stdout confirms exact frozen manifest')
ok(h(outer/'PRELAUNCH_BUILDER_SOURCE.py')==cap['builder_sha256']==h(C/'build/source_preparation/prepare_current_packet.py') and h(outer/'PRELAUNCH_OPERATOR.py')==cap['operator_sha256']==h(C/'build/source_preparation/capture_root_builder_operation.py'),'whole current prelaunch sources exact')
cmds=j(inner/'GIT_COMMANDS.json')
for r in cmds:
    ok(r['actual_execution'] is True and r['completed'] is True and type(r['pid']) is int and r['pid']>0 and type(r['exit_code']) is int and r['exit_code']==0 and time(cap['started_utc'])<=time(r['started_utc'])<=time(r['finished_utc'])<=time(cap['finished_utc']),'every final actual Git command complete',r['argv'])
    ok(r['argv'][0]=='git' and r['argv'][1] in ['branch','rev-parse','show','ls-tree','diff'],'current commands only read queries')
    for channel in ['stdout','stderr']: ok(identity(inner,r[channel]),'each full final Git stream',r[channel]['path'])
    ok((inner/r['stderr']['path']).read_bytes()==b'','each current Git stderr empty')
prefix=j(C/'build/actual_attempt_prepublication_prefix/GIT_COMMANDS.json')
ok(eq(prefix,cmds[:len(prefix)]) and len(prefix)<len(cmds),'packet command copy explicitly finite prepublication prefix',{'prefix':len(prefix),'final':len(cmds)})
ok((C/'build/actual_attempt_prepublication_prefix/GIT_COMMANDS.json').read_bytes()!= (inner/'GIT_COMMANDS.json').read_bytes(),'prefix not confused with complete final command record')
top=AUDIT/'root_current_freeze_operator_actual_capture'; tcap=j(top/'CAPTURE.json')
ok(tcap['completed'] is True and tcap['actual_execution'] is True and tcap['exit_code']==0 and tcap['pid']==cap['operator_pid'] and time(tcap['started_utc'])<=time(cap['started_utc'])<=time(cap['finished_utc'])<=time(tcap['finished_utc']),'outermost actual ROOT capture clocks')
for ch in ['stdout','stderr']: ok(identity(top,tcap[ch]),'outermost entire stream',ch)

deps=j(C/'CURRENT_DEPENDENCIES.json')
depnames={r['path'] for r in deps['files']}
foreign=[]
for family,manifest_name,ownkey,foreignkey in [('compactness_source_family','OWNERSHIP_MANIFEST.json','first_party_files','foreign_individually_excluded'),('probability_source_family','SELF_MANIFEST.json',None,None)]:
    f=AUDIT/family; fm=j(f/manifest_name)
    if ownkey:
        ownrows=fm[ownkey]; frows=fm[foreignkey]
    else:
        ownrows=[r for r in fm['files'] if r['classification']=='first_party_audit_artifact'];frows=[r for r in fm['files'] if r['classification']=='foreign_primary_or_access_evidence']
    actual={str(p.relative_to(f)) for p in f.rglob('*') if p.is_file()}
    ok(actual=={r['path'] for r in ownrows+frows}|{manifest_name},'each independent family exact closure',family)
    for r in ownrows: ok((C/'family_evidence'/family/r['path']).read_bytes()==(f/r['path']).read_bytes(),'authored family copy exact',family+'/'+r['path'])
    for r in frows:
        ok(family+'/'+r['path'] in depnames and not (C/'family_evidence'/family/r['path']).exists(),'foreign family individual exclusion and dependency',family+'/'+r['path'])
        foreign.append({'path':str((f/r['path']).resolve()),'bytes':r['bytes'],'sha256':r['sha256'],'role':'outside this family; foreign primary/derivative individually excluded'})
ok(len(foreign)==31,'all 8 plus23 individual source-family foreign exclusions')

qp=j(C/'CURRENT_QUEUE_PATCH.json')
before=(C/'queue_proposal/QUEUE_PREIMAGE.md').read_bytes(); after=(C/'queue_proposal/QUEUE_PROSPECTIVE.md').read_bytes()
ok(before==(REPO/'unsolved_math_prioritization/QUEUE.md').read_bytes() and before.count(qp['row_before'].encode())==1 and after==before.replace(qp['row_before'].encode(),qp['row_prospective'].encode(),1),'whole prospective queue only exact target row')
left=qp['row_before'].split('|');right=qp['row_prospective'].split('|')
ok(len(left)==len(right)==14 and all(a==b for i,(a,b) in enumerate(zip(left,right)) if i not in [8,9,11]),'only named Status Turns Findings; Chat DOI exact')

# Full read-only SQLite importer comparison, independently written here.
cache=REPO/'unsolved_math_prioritization/cache'
pb=(cache/'problems.json').read_bytes(); rb=(cache/'research_results.json').read_bytes()
problems=strict(pb); reports=strict(rb)
byid={str(p['id']):p for p in problems}; codes=collections.Counter(p['problem_number'] for p in problems)
conn=sqlite3.connect('file:'+str(cache/'catalog.sqlite')+'?mode=ro&immutable=1',uri=True)
conn.execute('PRAGMA query_only=ON')
sql=conn.execute('SELECT key,payload,report FROM records ORDER BY key').fetchall()
for key,payload,report in sql:
    expected=dict(byid[key]); code=expected['problem_number']
    if codes[code]>1 and code in reports: expected['_ambiguous_report']=True
    expected_report={} if expected.get('_ambiguous_report') else reports.get(code,{})
    if not eq(strict(payload),expected) or not eq(strict(report),expected_report): raise AssertionError('all SQL join '+key)
conn.close()
ok(len(pb)+len(rb)==149266659 and len(sql)==len(problems)==len(byid)==15458,'entire raw149266659 bytes and all15458SQL rows independently compare')
ok('OWR-17469-011' not in reports and eq(byid['30004386'],j(C/'source_record.json')) and eq(j(AUDIT/'pinned_prior_report.json'),{}),'raw prior key ABSENT and SQL fallback{} precise')

# New exact probes on the all-N construction, including zero, ties and norm one.
probe_count=0
for N in range(2,130):
    k=math.isqrt(N); r=N-k
    for q in [F(0),F(1,17),F(1,3),F(1)]:
        target=[q/F(2**i) for i in range(1,k+1)]
        filler=(1-sum(target,F(0)))/r
        sorted_sq=sorted(target+[filler]*r,reverse=True)
        if sum(sorted_sq,F(0))!=1: raise AssertionError('probe sphere normalization')
        for i,a in enumerate(target):
            if not a<=sorted_sq[i]<=max(a,filler): raise AssertionError('probe rank')
        if r*filler*filler>F(1,r): raise AssertionError('probe filler fourth-power')
        probe_count+=1
    for length in [1,2,3,5]:
        target=[F(1,length) if i<length else F(0) for i in range(k)]
        filler=(1-sum(target,F(0)))/r
        arranged=sorted(target+[filler]*r,reverse=True)
        if sum(arranged,F(0))!=1 or any(not a<=arranged[i]<=max(a,filler) for i,a in enumerate(target)): raise AssertionError('boundary/plateau probe')
        probe_count+=1
ok(True,'new exact zero/interior/plateau/finite-boundary rank and fourth-tail probes',probe_count)
ok(F(1,5)-3*F(1,3)**2==F(-2,15),'direct uniform fourth cumulant exact')

out={'schema':'NEW_WHOLE_CURRENT_INDEPENDENT_ACCEPTANCE_CONTROLS_v1','actual_pid':os.getpid(),
     'started_utc':started,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'candidate_manifest_sha256':h(C/'MANIFEST.json'),'checks':checks,'all_passed':True,
     'strict_entire_input_JSON_read':True,'SQL_rows_independently_compared':len(sql),
     'raw_bytes_independently_parsed':len(pb)+len(rb),'new_exact_probe_instances':probe_count,
     'foreign_helpers_executed':False,'native_git_remote_mutations':False,
     'scope':'Independent source/typed-provenance/capture/closure predicates plus finite exact construction diagnostics; mathematical derivation and source reads separately recorded. This is not ROOT approval or a future packet certificate.'}
(OWN/'INDEPENDENT_ACCEPTANCE_CONTROLS_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
print('Predicates:',len(checks),'Final actual command records:',len(cmds),'prefix:',len(prefix))
