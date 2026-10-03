"""Handwritten private V2 ownership/append models; production stays text only."""
from pathlib import Path, PurePosixPath
import copy, datetime as dt, hashlib, io, json, math, os, stat, tokenize, traceback
H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[2];V=A/'acceptance_preparation_family';C=A/'reviewed_candidate';W=A/'current_whole_adversary_family'
PROGRAM='draft_pr_publication_program_20260930/RESEARCH_LOG.md'
AUDIT=A.relative_to(R).as_posix();CANON='unsolved_math_prioritization/attempts/30004438'
READS=[];CHECKS=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def enc(o):return (json.dumps(o,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()
def put(p,b):
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def need(ok,msg):
    if not ok:raise ValueError(msg)
def check(msg,ok):
    need(type(ok) is bool and ok,msg);CHECKS.append({'name':msg,'passed':True})
def parse(b):
    def pairs(items):
        o={}
        for k,v in items:need(k not in o,'Duplicate key');o[k]=v
        return o
    def floating(v):
        f=float(v);need(math.isfinite(f),'Nonfinite');return f
    return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda v:(_ for _ in ()).throw(ValueError('Nonfinite')))
def same(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b
def read(p,z=None,mode=None):
    p=Path(p);need(not p.is_symlink() and stat.S_ISREG(p.lstat().st_mode) and all(not d.is_symlink() for d in p.parents),'Unsafe read');b=p.read_bytes();m=stat.S_IMODE(p.stat().st_mode)
    if z is not None:need(type(z['bytes']) is int and z['bytes']==len(b) and z['sha256']==sha(b),'Bound body')
    if mode is not None:need(type(mode) is int and m==mode,'Full mode')
    READS.append({'path':str(p),'bytes':len(b),'sha256':sha(b),'full_mode':m});return b
def rel(n):
    need(type(n) is str and n and n!='.' and '\\' not in n and '\0' not in n,'Bad path');p=PurePosixPath(n);need(not p.is_absolute() and p.as_posix()==n and not {'.','..','.git','__pycache__'}&set(p.parts),'Bad canonical');return p
def owned(n,v2=True):
    parts=rel(n).parts
    return n in NATIVE or (v2 and n==PROGRAM) or any(parts[:len(p)]==p and len(parts)>len(p) for p in [PurePosixPath(AUDIT).parts,PurePosixPath(CANON).parts])
def protect(names,v2=True):
    need(type(names) is list and all(type(n) is str for n in names) and names==sorted(set(names)),'Exact path list')
    for n in names:need(not owned(n,v2),'Owned cannot be foreign')
    return names
def rejected(name,fn):
    try:fn()
    except (ValueError,TypeError,KeyError,FileExistsError):check(name,True)
    else:raise ValueError('Accepted mutant '+name)
def closure(base,name,count,digest):
    raw=read(base/name,mode=0o444);need(sha(raw)==digest,'Manifest pin');o=parse(raw);need(type(o['files_count']) is int and o['files_count']==count and o['self_excluded']==[name],'Manifest schema/count');paths={name};dirs=set()
    for z in o['files']:
        rel(z['path']);need(z['path'] not in paths,'Duplicate member');paths.add(z['path']);read(base/z['path'],z,0o444);dirs|={p.as_posix() for p in PurePosixPath(z['path']).parents if p.as_posix()!='.'}
    actualfiles=set();actualdirs=set()
    for p in base.rglob('*'):
        need(not p.is_symlink() and (stat.S_ISREG(p.lstat().st_mode) or stat.S_ISDIR(p.lstat().st_mode)),'Unsafe member');(actualdirs if p.is_dir() else actualfiles).add(p.relative_to(base).as_posix())
    need(paths==actualfiles and dirs==actualdirs,'Exact self-only topology');check('Complete closed corpus '+str(base),True);return o
def lexical(name):
    raw=read(H/name);tokens=list(tokenize.tokenize(io.BytesIO(raw).readline));stack=[];pairs={')':'(',']':'[','}':'{'}
    for t in tokens:
        if t.type==tokenize.OP:
            if t.string in pairs:need(stack and stack.pop()==pairs[t.string],'Delimiter')
            elif t.string in '([{':stack.append(t.string)
    need(not stack,'Remaining delimiter')
    meaningful=[t for t in tokens if t.type not in {tokenize.ENCODING,tokenize.COMMENT,tokenize.NL,tokenize.NEWLINE,tokenize.INDENT,tokenize.DEDENT,tokenize.ENDMARKER}]
    if name=='pr46_guards.py':need(meaningful[0].type==tokenize.STRING and [t.string for t in meaningful[1:4]]==['from','__future__','import'],'Future import immediately follows sole module docstring')
    check('Literal production lexical source only '+name,True);return raw.decode()
def logreceipt(model,rows,note):
    expected=[AUDIT+'/ROOT_RESEARCH_LOG.md',PROGRAM];need(type(rows) is list and len(rows)==2,'Two exact logs')
    for row,n in zip(rows,expected):
        need(set(row)=={'path','before','after','before_mode','after_mode'} and row['path']==n and owned(n),'Exact owned log identity')
        p=model/rel(n);need(type(row['before']) is bytes and type(row['after']) is bytes and row['after']==row['before']+note and read(p)==row['after'],'Complete prefix plus append')
        need(type(row['before_mode']) is int and type(row['after_mode']) is int and row['before_mode']==row['after_mode']==stat.S_IMODE(p.stat().st_mode),'Full mode exact')
def native():
    rows=[]
    for z in DEPS['current_native13']:
        p=R/z['path'];raw=read(p);rows.append({'path':z['path'],'bytes':len(raw),'sha256':sha(raw),'full_mode':stat.S_IMODE(p.stat().st_mode)})
    return rows
def main():
    global DEPS,NATIVE
    need(__debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'Optimization')
    repair=parse(read(H/'SOURCE_REPAIR_BINDINGS.json'));completed=repair['closed_adverse_binding_completed']
    need(type(completed) is bool,'Typed completion status');result_name='OWN_CONTROL_RESULTS.json' if completed else 'OWN_PRELIMINARY_CONTROL_RESULTS.json';need(not (H/result_name).exists(),'Absent results')
    DEPS=parse(read(C/'CURRENT_DEPENDENCIES.json'));NATIVE={z['path'] for z in DEPS['current_native13']};before_native=native()
    closure(V,'PREPARATION_MANIFEST.json',166,'d97fb190b4b20a2566a1415130e4b7729cb1f8377f8b823e0fd0b263a3315dab')
    closure(C,'MANIFEST.json',946,'66239699390b279235c4064208e63134049a5804884818de9176d377476a189d');closure(W,'MANIFEST.json',245,'be3fa099c6a080d5f9cddcf42f39ac51b51c8f89cd76d09fb5d360a99d1990e2')
    need(len(DEPS['files'])==826,'Complete deps826')
    for z in DEPS['files']:read(A/z['path'],z)
    inp=parse(read(H/'INPUT_BINDINGS.json'))
    for z in inp['external_input_rows']:read(Path(z['path']),z,z['full_mode'])
    for z in inp['pins'].values():read(R/z['path'],z)
    if completed:
        for z in repair['complete_first_party_refs']:read(R/z['path'],z,z['full_mode'])
        am=repair['closed_adverse_manifest'];ao=parse(read(R/am['path'],am));closure((R/am['path']).parent,Path(am['path']).name,ao['files_count'],am['sha256'])
    else:check('Preliminary evidence does not pin unfinished adverse record',repair['status']=='PENDING_ACTUAL_CLOSED_ADVERSE_ROOT_BINDINGS' and repair['closed_adverse_manifest'] is None and repair['root_complete_adverse_inspection'] is None)
    for n in ['DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FINAL_PLAN.json']:
        o=parse(read(H/n));check('No fabricated future whole '+n,o['independent_whole_current_pass'] is False)
        for k,v in o.items():
            if k.startswith('root_') and k.endswith('_completed'):check('Pending '+n+' '+k,v is False)
    texts={n:lexical(n) for n in ['pr46_guards.py','seal_final_evidence.py','capture_root_final_operation.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']}
    g=texts['pr46_guards.py'];check('Fresh and capture and retained-preflight common ownership gate',g.count("protected_foreign_paths(fresh['protected_foreign_tracked_paths'])")==3)
    check('Exact sole additional owned program path literal',"ADDITIONAL_OWNED_MUTATION_PATHS = {PROGRAM_LOG.relative_to(R).as_posix()}" in g)
    check('No whole-program ownership prefix',"name.startswith(B.relative_to(R)" not in g)
    check('Post-append guard and mirror/post exact log check',"g.owned_log_append_check(pre)" in texts['integrate_reviewed_partial.py'] and "g.owned_log_append_check(pre)" in texts['state_mirror_reconciliation.py'] and "g.owned_log_append_check(pre)" in texts['verify_post_acceptance.py'])
    check('V2 operator anchor',"A / 'acceptance_preparation_family_v2'" in texts['capture_root_final_operation.py'] and "A / 'acceptance_preparation_family'" not in texts['capture_root_final_operation.py'])
    unrelated=['draft_pr_publication_program_20260930/another.md','draft_pr_publication_program_20260930/audits/pr45_9900007/ROOT_RESEARCH_LOG.md','draft_pr_publication_program_20260930/infrastructure/accepted_state_sync/RESEARCH_LOG.md','draft_pr_descending_audit_20261002/RESEARCH_LOG.md','README.md']
    for n in unrelated:check('Unrelated tracked body remains eligible '+n,protect([n])==[n])
    for n in sorted(NATIVE|{PROGRAM,AUDIT+'/ROOT_RESEARCH_LOG.md',CANON+'/acceptance.json'}):rejected('Owned rejected before mutation '+n,lambda n=n:protect([n]))
    for n in ['', '.', '/x',PROGRAM+'/',PROGRAM.replace('/RESEARCH','//RESEARCH'),PROGRAM.replace('/RESEARCH','/../RESEARCH')]:rejected('Noncanonical owned alias '+repr(n),lambda n=n:protect([n]))
    for names in [[PROGRAM,PROGRAM],['z','a'],[False],[PROGRAM,*unrelated]]:rejected('Malformed protected set '+repr(names),lambda names=names:protect(names))
    private=H/('PRIVATE_MODEL' if completed else 'PRIVATE_PRELIMINARY_MODEL');private.mkdir();physical={}
    for n in [PROGRAM,AUDIT+'/ROOT_RESEARCH_LOG.md',*unrelated]:
        p=private/rel(n);p.parent.mkdir(parents=True,exist_ok=True);put(p,('original private body '+n+'\n').encode());physical[n]=p
    old=read(physical[PROGRAM]);mode=stat.S_IMODE(physical[PROGRAM].stat().st_mode);start=now()
    # Reproduce S1 using the old ownership rule on a private first-party file.
    protect([PROGRAM],v2=False);physical[PROGRAM].write_bytes(old+b'private V1 append\n')
    try:need(read(physical[PROGRAM])==old,'S1 literal foreign body changed after finalization append')
    except ValueError:
        failure={'mechanism':'handwritten_private_V1_boundary_reproduction_not_production','actual_model_pid':os.getpid(),'started_utc':start,'finished_utc':now(),'exception':traceback.format_exc(),'logical_path':PROGRAM,'protected_before_sha256':sha(old),'after_append_sha256':sha(read(physical[PROGRAM])),'reproduced_S1':True,'production_executed':False}
    else:raise ValueError('V1 S1 not reproduced')
    put(H/('PRIVATE_V1_S1_FAILURE_REPRODUCTION.json' if completed else 'PRIVATE_PRELIMINARY_V1_S1_FAILURE_REPRODUCTION.json'),enc(failure));check('Actual private V1 preservation failure reproduced',True)
    # V2 rejects the claimed protection before any append; retain complete bytes.
    preserved=read(physical[PROGRAM]);rejected('V2 program rejected before any model append',lambda:protect([PROGRAM]));check('V2 rejection leaves complete bytes/mode',read(physical[PROGRAM])==preserved and stat.S_IMODE(physical[PROGRAM].stat().st_mode)==mode)
    for n in unrelated:check('Private unrelated preserved '+n,read(physical[n])==('original private body '+n+'\n').encode())
    protect(sorted(unrelated));before={n:read(physical[n]) for n in unrelated};note=b'private exact reviewed append\n';rows=[]
    for n in [AUDIT+'/ROOT_RESEARCH_LOG.md',PROGRAM]:
        p=physical[n];b=read(p);m=stat.S_IMODE(p.stat().st_mode);p.write_bytes(b+note);p.chmod(m);rows.append({'path':n,'before':b,'after':b+note,'before_mode':m,'after_mode':m})
    logreceipt(private,rows,note);check('Exact two owned model prefix/appends/modes',True);check('Whole unrelated body preservation after owned appends',all(read(physical[n])==before[n] for n in unrelated))
    for label,mutator in [('missing_log',lambda r:r.pop()),('extra_log',lambda r:r.append(copy.deepcopy(r[0]))),('wrong_destination',lambda r:r[1].update(path=unrelated[0])),('changed_prefix',lambda r:r[1].update(before=b'invented')),('changed_append',lambda r:r[1].update(after=r[1]['after']+b'extra')),('bool_mode',lambda r:r[1].update(after_mode=True)),('changed_mode',lambda r:r[1].update(after_mode=0o755))]:
        mutant=copy.deepcopy(rows);mutator(mutant);rejected('Owned receipt mutant '+label,lambda mutant=mutant:logreceipt(private,mutant,note))
    for b in [b'{"x":0,"x":1}',b'{"x":NaN}',b'{"x":1e999}']:rejected('Strict private JSON '+b.decode(),lambda b=b:parse(b))
    ledger=read(C/'turns.json');check('Exact original object0 response1',same(parse(ledger),parse(read(H/'EXPECTED_ORIGINAL_LEDGER.json'))))
    post=parse(read(H/'ROOT_POST_CONTRACT.json'));check('Exact new22-key complete ROOT post contract',len(post['required_ROOT_complete_keyset'])==22 and len(set(post['required_ROOT_complete_keyset']))==22 and post['required_completed_values']['owned_operational_log_appends_exact'] is True)
    inventory=parse(read(H/'OWNERSHIP_WRITE_INVENTORY.json'));check('One additional owned path; no whole-program exclusion',inventory['additional_owned_tracked_body_paths']==[PROGRAM] and inventory['complete_program_exclusion'] is False)
    after_native=native();check('Entire live13 bytes/full modes unchanged during own controls',same(before_native,after_native))
    result={'schema':'pr46-acceptance-source-v2-private-controls/v1','status':'PASS_PRIVATE_SOURCE_ONLY_S1_REPAIR_CONTROLS' if completed else 'PASS_PRELIMINARY_PRIVATE_S1_MODELS_PENDING_CLOSED_ADVERSE_BINDINGS','closed_adverse_binding_completed':completed,'utc':now(),'actual_pid':os.getpid(),'checks':CHECKS,'assertions':len(CHECKS),'complete_input_reads':READS,'native13_before':before_native,'native13_after':after_native,'private_V1_failure_reproduction':failure,'new_S1_boundary_rejection_before_mutation':True,'no_whole_program_exclusion':True,'unrelated_paths_preserved':True,'owned_log_full_prefix_append_mode_verified':True,'production_imported_compiled_executed':False,'future_acceptance_approved':False,'original_substantive_attempts':0,'original_source_verification_responses':1,'new_substantive_attempts':0,'audit_turns':0}
    put(H/result_name,enc(result));print(json.dumps({k:result[k] for k in ['status','actual_pid','assertions','closed_adverse_binding_completed','production_imported_compiled_executed','future_acceptance_approved']},sort_keys=True))
if __name__=='__main__':main()
