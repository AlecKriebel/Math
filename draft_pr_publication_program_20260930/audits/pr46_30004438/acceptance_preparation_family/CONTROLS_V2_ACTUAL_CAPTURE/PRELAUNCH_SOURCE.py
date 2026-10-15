"""Handwritten private controls. Proposed production is never imported or compiled."""
from pathlib import Path, PurePosixPath
import copy, ctypes, datetime as dt, hashlib, io, json, math, os, re, stat, subprocess, sys, tokenize
H = Path(__file__).resolve().parent; A = H.parent; R = A.parents[2]; C = A/'reviewed_candidate'
def sha(b): return hashlib.sha256(b).hexdigest()
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def put(p, b):
    with p.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
def enc(o): return (json.dumps(o,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()
def same(a,b):
    return type(a) is type(b) and (set(a)==set(b) and all(same(a[k],b[k]) for k in a) if type(a) is dict else len(a)==len(b) and all(same(x,y) for x,y in zip(a,b)) if type(a) is list else a==b)
def parse(raw):
    def pairs(items):
        d={}
        for k,v in items:
            if k in d: raise ValueError('Duplicate key')
            d[k]=v
        return d
    def floating(v):
        x=float(v)
        if not math.isfinite(x): raise ValueError('Nonfinite')
        return x
    return json.loads(raw,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda v:(_ for _ in ()).throw(ValueError('Nonfinite')))
def relative(value):
    if type(value) is not str or not value or value=='.' or '\\' in value or '\0' in value: raise ValueError('Path')
    p=PurePosixPath(value)
    if p.is_absolute() or p.as_posix()!=value or {'.','..','.git','__pycache__'}&set(p.parts): raise ValueError('Path')
    return p
READS=[]; CHECKS=[]; GITS=[]
def read(p, expected=None, frozen=False):
    if p.is_symlink() or not p.is_file() or any(x.is_symlink() for x in p.parents):raise ValueError('Unsafe input')
    body=p.read_bytes();mode=stat.S_IMODE(p.stat().st_mode)
    if expected is not None:
        assert type(expected['bytes']) is int and len(body)==expected['bytes'] and sha(body)==expected['sha256']
    if frozen:assert mode==0o444
    READS.append({'path':str(p),'bytes':len(body),'sha256':sha(body),'full_mode':mode})
    return body
def check(name, ok):
    assert type(ok) is bool and ok,name
    CHECKS.append({'name':name,'passed':True})
def rejected(name, f):
    try:f()
    except (ValueError,TypeError,KeyError,AssertionError,FileNotFoundError,FileExistsError):check(name,True)
    else:raise AssertionError('Accepted mutant '+name)
def git(name, *tail):
    root=H/'OWN_READONLY_GIT_V2';root.mkdir(exist_ok=True);d=root/name;d.mkdir();operator=Path(__file__).read_bytes()
    argv=['git',*tail];pre={'argv':argv,'cwd':str(R),'source_sha256':sha(operator),'operator_pid':os.getpid(),'created_utc':now(),'stdin_supplied':False}
    put(d/'PRELAUNCH_SOURCE.py',operator);put(d/'PRELAUNCH.json',enc(pre));start=now();child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'));out,err=child.communicate();finish=now()
    capture={**pre,'actual_execution':True,'completed':True,'pid':child.pid,'exit_code':child.returncode,'started_utc':start,'finished_utc':finish,'source_unchanged':Path(__file__).read_bytes()==operator}
    for n,b in [('stdout',out),('stderr',err)]:put(d/(n+'.bin'),b);capture[n]={'path':n+'.bin','bytes':len(b),'sha256':sha(b)}
    put(d/'CAPTURE.json',enc(capture));GITS.append(capture);assert child.returncode==0 and capture['source_unchanged'];return out
def native():
    obj=parse((C/'CURRENT_DEPENDENCIES.json').read_bytes());rows=[]
    for z in obj['current_native13']:
        p=R/z['path'];b=read(p);rows.append({'path':z['path'],'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)})
    return rows
def inspect_manifest(p, count):
    body=read(p,frozen=True);o=parse(body);assert o['self_excluded']==[p.name] and type(o['files_count']) is int and o['files_count']==count
    rows=o['files'];assert len(rows)==count and len({z['path'] for z in rows})==count
    names={p.name};dirs=set()
    for z in rows:
        relative(z['path']);names.add(z['path']);dirs|={d.as_posix() for d in PurePosixPath(z['path']).parents if d.as_posix()!='.'};raw=read(p.parent/z['path'],z,frozen=True)
        if p.parent==C and z['path'].endswith('.json') and raw:parse(raw)
        if p.parent==C and z['path'].endswith('.jsonl'):
            assert not raw or raw.endswith(b'\n')
            if z['path'] in {'original_preparation_archive/original_native_selected/assessment_history.jsonl','original_preparation_archive/original_native_selected/history.jsonl'}:parse(raw)
            else:
                for line in raw.splitlines():parse(line)
    actual_files=set();actual_dirs=set()
    for q in p.parent.rglob('*'):
        assert not q.is_symlink() and (q.is_dir() or q.is_file());n=q.relative_to(p.parent).as_posix();relative(n)
        (actual_dirs if q.is_dir() else actual_files).add(n)
    assert actual_files==names and actual_dirs==dirs
    check('entire candidate'+str(count)+' strict bodies modes topology',True);return o
def strict_ledger(body,used,limit):
    assert type(used) is int and type(limit) is int and used==0 and limit==5
    actual=parse(body);expected=parse((H/'EXPECTED_ORIGINAL_LEDGER.json').read_bytes())
    assert same(actual,expected) and body==(A/'source_snapshot/turns.json').read_bytes()
def source_text(p):
    raw=read(p);tokens=list(tokenize.tokenize(io.BytesIO(raw).readline));stack=[];closing={')':'(',']':'[','}':'{'}
    for token in tokens:
        if token.type==tokenize.OP:
            if token.string in closing:assert stack and stack.pop()==closing[token.string]
            elif token.string in '([{':stack.append(token.string)
    assert not stack;check('lexical delimiter scan '+p.name+' (no code objects)',True);return raw.decode()
def main():
    assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
    assert not (H/'OWN_CONTROL_RESULTS.json').exists()
    main_before=git('main_before','rev-parse','HEAD').decode().strip();check('actual main branch',git('branch','branch','--show-current')==b'main\n');native_before=native()
    candidate=inspect_manifest(C/'MANIFEST.json',946);check('exact reviewed candidate manifest SHA',sha((C/'MANIFEST.json').read_bytes())=='66239699390b279235c4064208e63134049a5804884818de9176d377476a189d')
    deps=parse(read(C/'CURRENT_DEPENDENCIES.json'));check('complete826 dependency rows',len(deps['files'])==826)
    for z in deps['files']:relative(z['path']);read(A/z['path'],z)
    freeze=parse(read(A/'ROOT_ACTUAL_CURRENT_FREEZE_INSPECTION.json'));check('complete frozen original43 vs final45',freeze['frozen_inner_prefix_commands']==43 and freeze['final_original_inner_commands']==45)
    for z in freeze['complete_stream_members']:read(A/z['path'],z)
    for z in parse(read(A/'snapshot_manifest.json'))['files']:
        b=read(A/'source_snapshot'/z['relative_path'],z,frozen=True);check('original13 current archive '+z['relative_path'],b==read(C/'original_archive'/z['relative_path']))
    immutable={'SOURCE_STATUS.md','independent_review/REVIEW.md','independent_review/independent_checks.py','independent_review/independent_results.json','independent_review/review_summary.json','provenance.json','source_record.json','turns.json','verification.json','verify.py'}
    for n in sorted(immutable):check('immutable10 full body '+n,read(C/n)==read(A/'source_snapshot'/n))
    ledger=(C/'turns.json').read_bytes();strict_ledger(ledger,0,5);check('exact zero substantive object budget with response1',True)
    for n,b,u,l in [('empty',b'',0,5),('whitespace_only',b'\n',0,5),('invented_object',b'{"substantive_turns_used":0}\n',0,5),('bool_used',ledger,False,5),('wrong_used',ledger,1,5),('wrong_limit',ledger,0,4)]:rejected('private ledger '+n,lambda b=b,u=u,l=l:strict_ledger(b,u,l))
    for n in ['DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FINAL_PLAN.json']:
        o=parse(read(H/n))
        for k,v in o.items():
            if k.startswith('root_') and k.endswith('_completed'):check('unfabricated pending '+n+' '+k,v is False)
        check('new whole pending '+n,o['independent_whole_current_pass'] is False)
    inputs=parse(read(H/'INPUT_BINDINGS.json'));check('genuine now completed whole binding',inputs['whole_binding_completed'] is True and inputs['closed_whole_manifest']['sha256']=='be3fa099c6a080d5f9cddcf42f39ac51b51c8f89cd76d09fb5d360a99d1990e2' and inputs['closed_root_whole_inspection']['sha256']=='ed0cc07fd852881a0b9a9893e6c2ec7f25e6e6d2f3d1bfb26bfa88a7a0b17b54');inspect_manifest(A/'current_whole_adversary_family/MANIFEST.json',245)
    for z in inputs['external_input_rows']:
        b=read(Path(z['path']),z);check('normalized actual external full mode '+z['path'],stat.S_IMODE(Path(z['path']).stat().st_mode)==z['full_mode'])
    for z in inputs['pins'].values():read(R/z['path'],z)
    prior=parse(read(R/inputs['previous_mirror']['path'],inputs['previous_mirror']));check('all35 earlier primary membership',len(prior['entries'])==35 and sorted(e['pr'] for e in prior['entries'])==prior['required_completed_prs'] and 46 not in prior['required_completed_prs'])
    for e in prior['entries']:
        for k in ['acceptance','audit_acceptance','remote','accepted_source','canonical_acceptance_text','canonical_manifest','artifact']:
            b=read(R/e[k]['path']);assert sha(b)==e[k]['sha256']
        b=read(R/e['budget']['ledger']['path']);assert sha(b)==e['budget']['ledger']['sha256'];check('typed actual prior budget '+str(e['pr']),type(e['budget']['used']) is int and type(e['budget']['limit']) is int)
    post=parse(read(R/inputs['previous_post']['path'],inputs['previous_post']));rootpost=parse(read(R/inputs['previous_root_post']['path'],inputs['previous_root_post']));check('complete genuine PR45 ROOT entire_post equality',same(post,rootpost['entire_post']) and rootpost['schema']=='pr45-root-complete-actual-post-inspection/v1' and rootpost['completed_primary_prs']==35)
    production=['pr46_guards.py','seal_final_evidence.py','capture_root_final_operation.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py'];texts={n:source_text(H/n) for n in production}
    check('proposed explicit ROOT authority gates in source text',"root_binding_input" in texts['pr46_guards.py'] and "g.require(a.execute" in texts['seal_final_evidence.py'] and "g.args(p)" in texts['verify_post_acceptance.py'])
    check('original14-path diff guard text',"splitlines())==14,'Original14 changed paths'" in texts['pr46_guards.py'])
    check('explicit object zero-turn native guard text',"'kind':'pr46_exact_original_zero_turn_object'" in texts['state_mirror_reconciliation.py'] and "'turns_used':0" in texts['verify_post_acceptance.py'])
    # This required private check catches the inherited empty-JSON parse trap before
    # any proposed sealer executes. Literal failed stdout must remain an exact archive.
    check('literal empty failed JSON receipt production qualification',"family_evidence/projective_algebra_family/failed01_run_stdout.json" in texts['pr46_guards.py'] and 'Historical literal empty failed stdout is preserved' in texts['pr46_guards.py'])
    for b in [b'{"x":0,"x":1}',b'{"x":NaN}',b'{"x":Infinity}',b'{"x":1e999}']:rejected('strict duplicate/nonfinite JSON '+b.decode(),lambda b=b:parse(b))
    check('typed false distinct zero',not same(False,0));check('typed one distinct floating one',not same(1,1.0))
    for value in ['', '.', '/x','a/../b','a//b','a/./b','a/','a\\b','a\0b','.git/x','__pycache__/x']:rejected('canonical path '+repr(value),lambda value=value:relative(value))
    for value in ['a','a/b','a.b/c-d']:check('valid canonical '+value,relative(value).as_posix()==value)
    scratch=H/'OWN_PRIVATE_MODE_PROBES';scratch.mkdir();file=scratch/'full_mode';put(file,b'private mode probe\n')
    for mode in range(0o10000):file.chmod(mode);check('actual full chmod mode '+oct(mode),stat.S_IMODE(file.stat().st_mode)==mode);check('only literal0444 mode accepted '+oct(mode),(mode==0o444)==(stat.S_IMODE(file.stat().st_mode)==0o444))
    file.chmod(0o644)
    original=file.read_bytes();rejected('exclusive same file publication',lambda:put(file,b'overwrite'));check('exclusive preserves whole existing body',file.read_bytes()==original)
    alias=scratch/'FULL_MODE'
    try:put(alias,b'case probe\n');case_insensitive=False
    except FileExistsError:case_insensitive=True
    case={'case_insensitive_filesystem':case_insensitive,'existing_full_body_preserved':file.read_bytes()==original};check('case alias preserves original full body',case['existing_full_body_preserved'])
    link=scratch/'unsafe_symlink';link.symlink_to(file.name);rejected('symlink full read',lambda:read(link));link.unlink()
    fifo=scratch/'unsafe_fifo';os.mkfifo(fifo);rejected('FIFO full read',lambda:read(fifo));fifo.unlink()
    stage=scratch/'absent-stage';stage.mkdir();put(stage/'member',b'complete first-party absent publication\n');target=scratch/'absent-target';libc=ctypes.CDLL(None,use_errno=True);rename=libc.renamex_np;rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];rename.restype=ctypes.c_int
    check('actual macOS absent-only directory publication',rename(os.fsencode(stage),os.fsencode(target),4)==0 and (target/'member').read_bytes()==b'complete first-party absent publication\n')
    second=scratch/'second-stage';second.mkdir();put(second/'member',b'new collision source\n');check('actual absent-only rejects existing directory',rename(os.fsencode(second),os.fsencode(target),4)!=0 and (second/'member').read_bytes()==b'new collision source\n' and (target/'member').read_bytes()==b'complete first-party absent publication\n')
    native_after=native();main_after=git('main_after','rev-parse','HEAD').decode().strip();check('all13 live bytes/full modes unchanged',same(native_before,native_after));check('actual main unchanged throughout private controls',main_before==main_after)
    results={'schema':'pr46-acceptance-source-private-controls/v1','utc':now(),'operator_pid':os.getpid(),'status':'PASS_PRIVATE_CONTROLS_SOURCE_ONLY','assertions':len(CHECKS),'checks':CHECKS,'complete_input_reads':READS,'all_readonly_Git_captures':GITS,'actual_case_alias':case,'native13_before':native_before,'native13_after':native_after,'main_before':main_before,'main_after':main_after,'proposed_production_imported_compiled_executed':False,'foreign_raw_PDF_cache_SQL_body_copies':False,'future_ROOT_or_acceptance_approved':False,'original_substantive_attempts':0,'original_source_verification_responses':1,'new_substantive_attempts':0,'audit_turns':0}
    put(H/'OWN_CONTROL_RESULTS.json',enc(results));print(json.dumps({k:results[k] for k in ['status','assertions','proposed_production_imported_compiled_executed','future_ROOT_or_acceptance_approved']},sort_keys=True))
if __name__=='__main__':main()
