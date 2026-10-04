#!/usr/bin/env python3
"""Independent manually transcribed predicate experiments plus full fixed-body inspection.
No import, compilation or execution of production builder/operator or mathematical helpers.
"""
from pathlib import Path, PurePosixPath
import ctypes, datetime as dt, hashlib, json, math, os, re, stat, subprocess, sys
F=Path(__file__).absolute().parent; A=F.parent; R=A.parents[2]; P=A/'current_preparation_family'
assert __debug__ and not sys.flags.optimize and sys.platform=='darwin'
checks=[]; readback={}; node_types={}; git_records=[]
def ck(label,v):
    if not v: raise AssertionError(label)
    checks.append(label)
def sha(b): return hashlib.sha256(b).hexdigest()
def utc(): return dt.datetime.now(dt.timezone.utc).isoformat()
def enc(o): return (json.dumps(o,indent=2,allow_nan=False)+'\n').encode()
def need(v,m):
    if not v: raise ValueError(m)
def relative(v):
    need(type(v) is str and v and '\\' not in v and '\0' not in v,'path')
    p=PurePosixPath(v)
    need(not p.is_absolute() and str(p)==v and not {'.','..','.git','__pycache__'}.intersection(p.parts),'path')
    return v
def load(b):
    def pairs(items):
        d={}
        for k,v in items: need(k not in d,'duplicate'); d[k]=v
        return d
    def constant(v): raise ValueError(v)
    def floating(v):
        n=float(v); need(math.isfinite(n),'nonfinite'); return n
    return json.loads(b,object_pairs_hook=pairs,parse_constant=constant,parse_float=floating)
def equal(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict: return set(a)==set(b) and all(equal(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b
def rows(rs,mode=False):
    need(type(rs) is list,'rows'); seen=set()
    for r in rs:
        need(type(r) is dict and set(r)==({'path','bytes','sha256','full_mode'} if mode else {'path','bytes','sha256'}),'rowkeys')
        n=relative(r['path']); need(n not in seen,'duplicate row'); seen.add(n)
        need(type(r['bytes']) is int and r['bytes']>=0 and type(r['sha256']) is str and re.fullmatch('[0-9a-f]{64}',r['sha256']) is not None,'rowtype')
        if mode: need(type(r['full_mode']) is int and 0<=r['full_mode']<4096,'mode')
    return seen
def raw(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'regular')
    return p.read_bytes()
def topology(root):
    need(root.is_dir() and not root.is_symlink() and all(not q.is_symlink() for q in root.parents),'directory')
    fs=set(); ds=set()
    for p in root.rglob('*'):
        need(not p.is_symlink(),'symlink'); n=relative(p.relative_to(root).as_posix())
        if stat.S_ISREG(p.stat().st_mode): fs.add(n)
        else: need(stat.S_ISDIR(p.stat().st_mode),'special'); ds.add(n)
    need(ds=={q.as_posix() for n in fs for q in PurePosixPath(n).parents if str(q)!='.'},'extra directory')
    return fs,ds
def bad(label,fn):
    try: fn()
    except (ValueError,TypeError,FileNotFoundError,OSError): ck(label,True); return
    raise AssertionError('Did not reject '+label)
def tree_nodes(o):
    t=type(o).__name__; node_types[t]=node_types.get(t,0)+1
    if type(o) is dict:
        for k,v in o.items(): tree_nodes(k); tree_nodes(v)
    elif type(o) is list:
        for v in o: tree_nodes(v)
def inspect(p,expected=None,mode=None):
    b=raw(p); n=p.relative_to(R).as_posix(); sm=stat.S_IMODE(p.stat().st_mode)
    if expected: ck('full pinned bytes '+n,len(b)==expected['bytes'] and sha(b)==expected['sha256'])
    if mode is not None: ck('full mode '+n,sm==mode)
    row={'path':n,'bytes':len(b),'sha256':sha(b),'full_mode':sm}
    ck('repeated byte identity '+n,n not in readback or equal(row,readback[n])); readback[n]=row
    if p.suffix=='.json': tree_nodes(load(b))
    elif p.suffix=='.jsonl':
        # Original selected-history receipts use pretty JSON despite this suffix.
        try: o=load(b)
        except json.JSONDecodeError:
            for line in b.splitlines(): tree_nodes(load(line))
        else: tree_nodes(o)
    return b
def closure(root,name,pin,count,dirs):
    mb=inspect(root/name,mode=0o444); ck('manifest pin '+name,sha(mb)==pin); m=load(mb)
    ck('self-only '+name,m['self_excluded']==[name] and type(m['files_count']) is int and m['files_count']==len(m['files'])==count)
    rs=[{k:r[k] for k in ['path','bytes','sha256']} for r in m['files']]
    fs,ds=topology(root); ck('exact topology '+str(root),fs==rows(rs)|{name} and len(ds)==dirs)
    for r in rs: inspect(root/r['path'],r,0o444)
    return m
prep=closure(P,'PREPARATION_MANIFEST.json','cc29dc830448d8ddf232f3fc080e457c6a8a015428104bba2d4fc15f62f56631',157,25)
ck('production bytes personally reviewed',sha(raw(P/'prepare_current_packet.py'))=='a99e425fdd85864aced1d2bb26557d57af475d723d0c1191bb42a131ab598c6a' and sha(raw(P/'capture_root_builder_operation.py'))=='dcac0206d0136302065fc699ef8938b53795aaddf143b620eb6a402ac596f200')
pins=load(raw(P/'STATIC_INPUT_BINDINGS.json'))
for group,info in pins['groups'].items():
    mr=info['manifest']; mp=R/mr['path']; mb=inspect(mp,mr,0o444); m=load(mb)
    if group=='cover_algebra_family':
        ck('group self '+group,m['schema']=='pr47-cover-self-only-recursive-closure/v1' and m['sole_self_excluded_from_members']==mp.name and len(m['files'])==143)
    elif group=='gauge_geometry_family':
        ck('group self '+group,m['schema']=='pr47-gauge-family-self-only-closed-manifest/v1' and m['self_excluded']==mp.name and type(m['file_count_excluding_self']) is int and m['file_count_excluding_self']==len(m['files'])==71)
    else:
        ck('group self '+group,m['self_excluded']==[mp.name] and type(m['files_count']) is int and m['files_count']==len(m['files'])==301)
    expected={PurePosixPath(r['path']).relative_to(mp.parent.relative_to(R)).as_posix() for r in info['members']}
    ck('fixed members match actual manifest '+group,expected=={r['path'] for r in m['files']})
    if group=='original':
        fs=set(info['authorship_root_files']); ds=set()
        for n in info['authorship_directory_roots']:
            sub,sd=topology(A/n); fs|={n+'/'+s for s in sub}; ds|={n}|{n+'/'+s for s in sd}
        ck('scoped original ownership',fs==expected and ds=={r['path'] for r in info['directories']} and len(fs)==301 and len(ds)==55)
    else:
        fs,ds=topology(mp.parent); ck('closed family topology '+group,fs==expected|{mp.name} and ds=={r['path'] for r in info['directories']})
    for r in info['members']: inspect(R/r['path'],r,0o444)
    for r in info['directories']: ck('pinned directory mode '+group+'/'+r['path'],stat.S_IMODE((mp.parent/r['path']).stat().st_mode)==r['full_mode'])
for r in pins['separate_original_and_ROOT_actual_captures']: inspect(R/r['path'],r,r['full_mode'])
rf=load(raw(P/'ROOT_FIXED_EVIDENCE.json')); D=A/'root_original_actual_reproduction'
rm=closure(D,'MANIFEST.json','71109d8643eeff305b9e8200e2e7be0e62e79ad1cc7ad8a22b4456f5a108d278',219,46)
for r in rf['members']+rf['separate_actual_closure_members']: inspect(R/r['path'],r,r['full_mode'])
for name in ['ROOT_MATHEMATICAL_REVIEW.md','ROOT_COMPLETE_RAW_SQL_AUDIT.json']:
    ck('ROOT top evidence equals closed copy '+name,inspect(A/name)==raw(D/name))
rootresult=load(raw(D/'ROOT_REPRODUCTION_RESULT.json')); summary=load(raw(D/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json')); audit=load(raw(A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json'))
ck('full typed embedded ROOT reproduction',equal(summary['entire_reproduction_result'],rootresult))
original=load(raw(A/'snapshot_manifest.json')); ori={}
for r in original['files']:
    n=r['relative_path']; ori[n]=inspect(A/'source_snapshot'/n,r,0o444)
    ck('archive byte-exact '+n,ori[n]==raw(P/'original_archive'/n))
for n in ['verify.py','verification.json','source_checksums.json','source_record.json','turns.json','prior_report.json','review/independent_checks.py','review/independent_results.json','review/submitted_verify.py','review/submitted_results.json']:
    ck('operative immutable '+n,ori[n]==raw(P/'operative_proposal'/n))
author=load(ori['verification.json']); ind=load(ori['review/independent_results.json']); ledger=load(ori['turns.json'])
ck('full author and duplicate receipt',equal(rootresult['entire_author_result'],author) and equal(rootresult['entire_identical_submitted_copy_result'],author))
ck('full historical independent receipt',equal(rootresult['entire_historical_independent_result'],ind))
ck('complete ledger and typed accounting',equal(rootresult['complete_original_turns'],ledger) and type(ledger['count']) is int and ledger['count']==1 and len(ledger['attempts'])==1 and ori['prior_report.json']==b'null\n')
ck('114 duplicate not independent',author['passed'] is True and type(author['assertions']) is int and author['assertions']==len(author['checks'])==114 and type(ind['passed']) is int and ind['passed']==len(ind['checks'])==100 and rootresult['duplicate114_counted_independent'] is False)
for k,n in [('original_substantive_attempts',1),('turn_limit',5),('new_substantive_attempts',0),('audit_turns',0)]: ck('typed accounting '+k,type(rootresult[k]) is int and rootresult[k]==n)
ck('full SQL record semantics',audit['status']=='PASS_FULL_RAW_PRIOR_SQL_AND_ORIGINAL_PLAIN_SOURCE' and type(audit['full_raw_and_prior_bytes']) is int and audit['full_raw_and_prior_bytes']==149266659 and type(audit['all_SQL_rows']) is int and audit['all_SQL_rows']==15458 and len(audit['complete_row_bindings'])==15458)
keys=set()
for row in audit['complete_row_bindings']:
    ck('every distinct SQL typed witness '+row['key'],type(row['key']) is str and row['key'] not in keys and row['complete_payload_recursive_type_equal'] is True and row['complete_report_recursive_type_equal'] is True and row['ambiguous_code'] is False)
    keys.add(row['key'])
ck('plain source full typed equality',equal(audit['original_native_selected_read']['complete_selected_problem'],load(ori['source_record.json'])))
ck('null versus absent fallback',audit['selected_prior_key_present'] is False and equal(audit['selected_prior_fallback'],{}) and audit['raw_null_present'] is False and audit['literal_original_prior_file_value'] is None and audit['literal_original_prior_differs_from_upstream_absent_fallback'] is True)
for label,cap in [('helper',c) for c in rootresult['complete_actual_helper_captures']]+[('Git',c) for c in rootresult['complete_actual_Git_captures']]:
    ck('real ROOT '+label+' capture '+str(cap['pid']),cap['actual_execution'] is True and cap['completed'] is True and type(cap['pid']) is int and cap['pid']>0 and type(cap['exit_code']) is int and cap['exit_code']==0 and cap['stdin_supplied'] is False)
    for k in ['stdout','stderr']: inspect(R/cap[k]['path'],cap[k])
    if label=='helper':
        ck('helper source typed '+str(cap['pid']),type(cap['source']) is dict)
        inspect(R/cap['source']['path'],cap['source']); ck('unchanged source '+str(cap['pid']),cap['source_unchanged'] is True)
    else:
        ck('genuine readonly Git null source '+str(cap['pid']),cap['source'] is None and cap['source_unchanged'] is None and cap['argv'][0]=='git' and cap['argv'][1] in {'show','ls-tree','diff'})
        bad('original builder source-present branch rejects genuine Git '+str(cap['pid']),lambda cap=cap:rows([cap['source']]))
q=raw(P/'SOURCE_PRECISION_QUALIFICATIONS.md')
for n in ['README.md','PR_DRAFT.md','pr_body.md','CURRENT_CONTEXT.md','CURRENT_REVIEW_CONTEXT.md']:
    b=raw(P/'presentations'/n); ck('complete global qualification '+n,b.endswith(q) and b'unsolved' in b and b'known Seifert degeneracy has no I# computation' in b and b'no newly accepted verdict' in b)
ck('obsolete universal branch removed',b'either prove that every reducible' not in raw(P/'operative_proposal/OBSTRUCTION.md'))
for n in ['DRAFT_ROOT_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json']:
    d=load(raw(P/n)); ck('draft is not approval '+n,d['reading_completed'] is False and d['created_utc'] is None and all(v is False for v in d['root_flags'].values()))
ck('no actual current destination',not (A/'reviewed_candidate').exists() and not (A/'reviewed_candidate').is_symlink())
private=F/'private'; private.mkdir(exist_ok=False)
for v in ['',None,True,1,[],{},'/absolute','a//b','a/./b','a/../b','../a','a/','./a','a\\b','a\0b','.git/a','a/__pycache__/b']:
    bad('reject path '+repr(v),lambda v=v:relative(v))
ck('dot lexical limit honestly observed',relative('.')=='.')
for n in ['a','a/b','a b','a-b/c_1']: ck('valid path '+n,relative(n)==n)
for b in [b'{"x":1,"x":2}',b'{"a":{"x":1,"x":2}}',b'NaN',b'Infinity',b'-Infinity',b'1e9999',b'[1e9999]',b'{"x":1e9999}',b'{',b'\xff']:
    bad('reject bad JSON '+repr(b),lambda b=b:load(b))
for a,b in [(True,1),(False,0),(1,1.0),({'x':True},{'x':1}),([None],[{}]),(None,{}),({'a':1},{'a':1,'b':2})]: ck('recursive distinct '+repr((a,b)),not equal(a,b))
for a in [None,{},[],True,1,1.0,'x',{'a':[True,1,None,{}]}]: ck('typed self equality '+repr(a),equal(a,a))
row={'path':'member','bytes':0,'sha256':'a'*64,'full_mode':0o444}
for k,vals in [('bytes',[True,False,-1,1.0,'0',None]),('sha256',['A'*64,'a'*63,'g'*64,True,None]),('full_mode',[True,False,-1,4096,292.0,'0444',None]),('path',['../a','a//b',True,None])]:
    for v in vals: bad('reject typed row '+k+repr(v),lambda k=k,v=v:rows([dict(row,**{k:v})],True))
bad('reject extra row key',lambda:rows([dict(row,extra=True)],True)); bad('reject missing row key',lambda:rows([{k:v for k,v in row.items() if k!='bytes'}],True)); bad('reject duplicate rows',lambda:rows([row,row],True))
for mode in range(4096): ck('all4096 logical modes '+str(mode),rows([dict(row,full_mode=mode)],True)=={'member'})
fixture=private/'mode'; fixture.write_bytes(b'full-mode fixture\n')
for mode in range(4096):
    fixture.chmod(mode); actual=stat.S_IMODE(fixture.stat().st_mode)
    ck('all4096 actual chmod exact '+str(mode),actual==mode)
    ck('only full0444 accepted '+str(mode),(actual==0o444)==(mode==0o444))
fixture.chmod(0o644)
valid=private/'valid'; (valid/'nested').mkdir(parents=True); (valid/'nested/member').write_bytes(b'member')
ck('valid nested topology',topology(valid)==({'nested/member'},{'nested'}))
(valid/'empty').mkdir(); bad('reject extra empty directory',lambda:topology(valid)); (valid/'empty').rmdir()
bad('dot downstream raw rejects directory',lambda:raw(valid/relative('.')))
link=private/'link'; link.symlink_to(valid,target_is_directory=True); bad('reject symlink parent',lambda:raw(link/'nested/member')); bad('reject symlink root',lambda:topology(link)); link.unlink()
(valid/'linked').symlink_to(valid/'nested/member'); bad('reject symlink member',lambda:topology(valid)); (valid/'linked').unlink()
fifo=valid/'fifo'; os.mkfifo(fifo); bad('reject FIFO before read',lambda:raw(fifo)); bad('reject FIFO topology',lambda:topology(valid)); fifo.unlink()
lib=ctypes.CDLL(None,use_errno=True); rename=lib.renamex_np; rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint]; rename.restype=ctypes.c_int
src=private/'rename_source'; dst=private/'rename_destination'; src.mkdir(); (src/'member').write_bytes(b'one')
ck('actual exclusive absent rename',rename(os.fsencode(src),os.fsencode(dst),4)==0 and (dst/'member').read_bytes()==b'one')
src.mkdir(); (src/'member').write_bytes(b'two'); rc=rename(os.fsencode(src),os.fsencode(dst),4); ck('actual exclusive existing destination rejects',rc==-1 and (src/'member').read_bytes()==b'two' and (dst/'member').read_bytes()==b'one')
rc=rename(os.fsencode(src),os.fsencode(private/'RENAME_DESTINATION'),4)
case_insensitive=(private/'RENAME_DESTINATION').exists() and os.path.samefile(private/'RENAME_DESTINATION',dst)
ck('actual case alias existing rejects when aliased',not case_insensitive or rc==-1 and (src/'member').read_bytes()==b'two')
sentinel=private/'exclusive'; sentinel.write_bytes(b'first')
bad('exclusive create duplicate preserves',lambda:sentinel.open('xb')); ck('exclusive original bytes unchanged',sentinel.read_bytes()==b'first')
flags=load(raw(P/'DRAFT_ROOT_READ_LEDGER.json'))['root_flags']; required={k:True for k in flags}
ck('all exact reading flags accepted',equal(required,{k:True for k in flags}))
for k in flags:
    ck('false reading flag rejects '+k,not equal(dict(required,**{k:False}),required))
    ck('integer reading flag rejects '+k,not equal(dict(required,**{k:1}),required))
ck('missing and extra reading flags reject',not equal({k:v for k,v in required.items() if k!=next(iter(required))},required) and not equal(dict(required,extra=True),required))
science=load(raw(P/'DRAFT_ROOT_SCIENCE_CARD.json')); ck('runtime future remains null',all(science[k] is None for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict']) and science['new_whole_current_gate']=='PENDING')
ck('optional extra ledger key is not universal rejection',dict(science,future_merge_approved=True)['current_verdict'] is None)
out={'schema':'pr47-source-independent-private-controls/v1','created_utc':utc(),'pid':os.getpid(),'status':'COMPLETE_CONTROLS_MANDATORY_SOURCE_REPAIR','assertions':len(checks),'checks':checks,'unique_full_fixed_body_reads':len(readback),'full_fixed_body_read_bytes':sum(r['bytes'] for r in readback.values()),'complete_readback_rows':list(sorted(readback.values(),key=lambda r:r['path'])),'all_parsed_JSON_nodes_by_type':node_types,'all4096_actual_modes_tested':True,'production_import_compile_execute':False,'mathematical_helpers_run':False,'foreign_bodies_copied':False,'actual_case_insensitive_alias_observed':case_insensitive,'isolated_dot_lexical_acceptance_is_downstream_rejected':True,'reading_science_extra_key_general_allowlist_absent':True,'future_whole_current_acceptance_certified':False,'mandatory_corrections':[{'locator':'prepare_current_packet.py line164','issue':'Source-key membership treats33 genuine null-source Git captures as helper sources; checked(None) rejects fixed true ROOT evidence.','repair':'Require typed nonnull sources for actual helper records; distinguish and validate genuine readonly Git records with source null and source_unchanged null.'}]}
(F/'CONTROL_RESULTS.json').write_bytes(enc(out)); print(json.dumps({k:v for k,v in out.items() if k not in ['checks','complete_readback_rows']},indent=2))
