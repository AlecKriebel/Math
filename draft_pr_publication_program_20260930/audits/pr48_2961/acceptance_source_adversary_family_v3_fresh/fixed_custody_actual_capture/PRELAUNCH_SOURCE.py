"""Own readonly whole-body custody audit; no proposed source is imported."""
import datetime as dt,hashlib,json,math,re,stat
from pathlib import Path,PurePosixPath
F=Path(__file__).absolute().parent;R=F.parents[3];A=F.parent;V=A/'acceptance_preparation_family_v3'
def need(v,m):
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(rr):
        o={}
        for k,v in rr:need(k not in o,'Duplicate key');o[k]=v
        return o
    def fl(x):y=float(x);need(math.isfinite(y),'Nonfinite');return y
    return json.loads(b,object_pairs_hook=pairs,parse_float=fl,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def raw(p):
    need(p.is_file() and not p.is_symlink() and all(not d.is_symlink() for d in p.parents),'Regular no-symlink file')
    return p.read_bytes()
def typed(a,b):
    if type(a) is not type(b):return False
    return (a.keys()==b.keys() and all(typed(a[k],b[k]) for k in a)) if type(a) is dict else (len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))) if type(a) is list else a==b
def ref(p):
    b=raw(p);return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}
bindings={};groups={};total_bytes=0
def add(z,group):
    global total_bytes
    need(type(z) is dict and {'path','bytes','sha256','full_mode'}<=set(z),'Complete input binding')
    n=z['path'];pp=PurePosixPath(n)
    need(type(n) is str and n and not pp.is_absolute() and pp.as_posix()==n and not {'..','.git','__pycache__'}.intersection(pp.parts),'Canonical root-relative input')
    row={k:z[k] for k in ['path','bytes','sha256','full_mode']}
    need(type(row['bytes']) is int and row['bytes']>=0 and type(row['full_mode']) is int and 0<=row['full_mode']<=0o7777 and type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']),'Typed bytes/digest/mode')
    if n in bindings:need(typed(bindings[n],row),'Conflicting same-path live identity')
    else:
        body=raw(R/n);need(len(body)==row['bytes'] and sha(body)==row['sha256'] and stat.S_IMODE((R/n).stat().st_mode)==row['full_mode'],'Changed full input '+n)
        bindings[n]=row;total_bytes+=len(body)
    groups.setdefault(group,set()).add(n)
def check_family(base,name,pin=None):
    body=raw(base/name);need(pin is None or sha(body)==pin,'Exact family self pin');m=parse(body)
    need(m['self_excluded']==[name] and type(m['files_count']) is int and m['files_count']==len(m['files']),'Self-only typed family')
    expected={name};seen=set()
    for z in m['files']:
        n=z['path'];need(n not in seen and n!=name,'Unique payload');seen.add(n);p=base/n;need(len(raw(p))==z['bytes'] and sha(raw(p))==z['sha256'],'Full family body');add({**z,'path':p.relative_to(R).as_posix(),'full_mode':0o444},'closed_family_'+base.name);expected.add(n)
    files=set();dirs=set()
    for p in base.rglob('*'):
        need(not p.is_symlink() and (p.is_file() or p.is_dir()),'No special closure topology')
        (files if p.is_file() else dirs).add(p.relative_to(base).as_posix())
    expected_dirs={p.as_posix() for n in expected for p in PurePosixPath(n).parents if p.as_posix()!='.'}
    need(files==expected and dirs==expected_dirs,'Exact entire family files/directories');add(ref(base/name),'closed_self_'+base.name)
    need(stat.S_IMODE((base/name).stat().st_mode)==0o444,'Literal root self full444')
    return m
def capture(folder,group,expected_argv=None):
    c=parse(raw(folder/'CAPTURE.json'));add(ref(folder/'CAPTURE.json'),group)
    need(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and c['stdin_supplied'] is False,'Genuine successful actual capture')
    start=dt.datetime.fromisoformat(c['started_utc']);finish=dt.datetime.fromisoformat(c['finished_utc']);need(start.tzinfo is not None and start.utcoffset()==dt.timedelta(0) and finish.utcoffset()==dt.timedelta(0) and start<=finish<=dt.datetime.now(dt.timezone.utc),'Genuine capture chronology')
    if expected_argv is not None:need(c['argv']==expected_argv and c['cwd']==str(R),'Exact actual argv/cwd')
    for ch in ['stdout','stderr']:
        z=c[ch];need(set(z)=={'path','bytes','sha256'} and z['path']==ch+'.bin','Literal complete stream');b=raw(folder/z['path']);need(len(b)==z['bytes'] and sha(b)==z['sha256'],'Whole actual stream');add(ref(folder/z['path']),group)
    need(raw(folder/'stderr.bin')==b'','Whole successful stderr empty')
    for p in folder.iterdir():add(ref(p),group)
    return c
def main():
    m=check_family(V,'PREPARATION_MANIFEST.json');need(set(m)=={'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'} and m['schema']=='pr48-acceptance-source-closure/v3' and m['status']=='CLOSED_SOURCE_ONLY' and m['source_only'] is True and m['proposed_helpers_imported_compiled_executed'] is False and m['future_acceptance_or_ROOT_approval_claimed'] is False,'Exact closed V3 SOURCE-only schema')
    inputs=parse(raw(V/'INPUT_BINDINGS.json'));need(inputs['actual_predecessor_PR47_completed'] is True and inputs['future_native13_and_main_required'] is True and inputs['actual_predecessor_PR47_native4_dated_not_future_authority'] is True,'Actual47 does not approve48')
    need(len(inputs['external_input_rows'])==3912 and len({z['path'] for z in inputs['external_input_rows']})==3912,'All3912 fixed external identities')
    for z in list(inputs['pins'].values())+inputs['external_input_rows']+list(inputs['source_pattern_dated_references'].values())+[inputs['known_predecessor_source_contract'],inputs['known_predecessor_source_manifest']]+[inputs[k] for k in ['previous_mirror','previous_post','previous_root_post']]:add(z,'V3_current_inputs')
    for name in ['SUPERSEDED_SOURCE_BINDINGS.json','V2_M2_HISTORY_BINDINGS.json']:
        h=parse(raw(V/name))
        sections=['superseded_source','closed_adverse'] if name.startswith('SUPERSEDED') else ['superseded_V2','closed_M2_adverse']
        for key in sections:
            c=h[key];add(c['manifest'],'historical_closed_source');check_family((R/c['manifest']['path']).parent,Path(c['manifest']['path']).name,c['manifest']['sha256'])
            for z in c['individual_closed_members']:add(z,'historical_closed_source')
        for k in ['report','verdict']:add(h[k],'historical_reports')
        need(h['previous_PASS_transferred'] is False,'No historical PASS transfer')
        key='actual_source_and_adverse_closure_readback_captures' if name.startswith('SUPERSEDED') else 'actual_closure_and_readback_captures'
        for row in h[key]:
            add(row['capture'],'historical_actual_captures');cap=parse(raw(R/row['capture']['path']));need(typed(cap,row['complete_capture']),'Entire historical capture')
            capture((R/row['capture']['path']).parent,'historical_actual_captures')
            for z in row['complete_members']:add(z,'historical_actual_captures')
    p47=parse(raw(V/'ACTUAL47_PREDECESSOR_BINDINGS.json'))
    for n in ['root_post','verifier_post','mirror','original47_post_operator_source']:add(p47[n],'genuine_actual47')
    root=parse(raw(R/p47['root_post']['path']));post=parse(raw(R/p47['verifier_post']['path']));contract=parse(raw(R/inputs['known_predecessor_source_contract']['path']));mirror=parse(raw(R/p47['mirror']['path']))
    need(typed(root,p47['entire_ROOT22_post']) and typed(post,p47['entire_verifier_post']) and typed(root['entire_post'],post),'Whole actual47 ROOT22 and verifier')
    need(set(root)==set(contract['future47_required_ROOT_complete_keyset']) and len(root)==22,'Exact actual47 ROOT22')
    for k,v in contract['future47_required_completed_values'].items():need(k in root and typed(root[k],v),'Typed actual47 contracted value')
    for k,v in contract['future47_required_entire_post_values'].items():need(k in post and typed(post[k],v),'Typed entire actual47 verifier')
    need(post['targets']==38 and post['consumed_substantive_turns']==45 and post['primary_acceptances']==37 and post['program_completed_count']==37 and post['program_completion_estimate_percent']==37*100/180,'Actual47 dimensions')
    nums=[z['pr'] for z in mirror['entries']];need(len(nums)==len(set(nums))==37 and 46 in nums and 47 in nums and 48 not in nums and nums==mirror['required_completed_prs'] and len(mirror['duplicate_mirrors'])==1,'Genuine predecessor membership')
    rows=[p47['complete_actual_ROOT_post_capture']]+p47['complete_six_actual_phase_captures'];need(len(rows)==7,'One ROOT and six actual phases')
    roles=[]
    for row in rows:
        add(row['capture'],'genuine_actual47_captures');c=parse(raw(R/row['capture']['path']));need(typed(c,row['complete_capture']),'Whole actual47 CAP metadata');capture((R/row['capture']['path']).parent,'genuine_actual47_captures')
        for z in row['complete_members']:add(z,'genuine_actual47_captures')
        if 'phase' in c:roles.append(c['phase'])
    need(roles==['preflight','overlay','prepush','finalize','mirror','post'],'Actual distinct six phase roles checked independently')
    need(len(root['all_six_real_phase_captures'])==6 and [z['path'] for z in root['all_six_real_phase_captures']]==[z['capture']['path'] for z in rows[1:]],'ROOT actual six capture identities')
    # Operator's exact SOURCE body and actual-source declarations are connected
    # by CHANGE_MAP, not by an inherited control PASS.
    change=parse(raw(V/'CHANGE_MAP.json'))
    for z in change['helper_bodies']:
        old=raw(A/'acceptance_preparation_family_v2'/z['name']);new=raw(V/z['name']);need(sha(old)==z['old_sha256'] and sha(new)==z['new_sha256'] and (old==new) is z['unchanged'],'Whole old/new helper identity')
    for z in change['unchanged_scientific_and_ROOT_metadata']:need(sha(raw(V/z['name']))==z['sha256'] and raw(V/z['name'])==raw(A/'acceptance_preparation_family_v2'/z['name']),'Global scientific/draft metadata unchanged')
    old_guard=raw(A/'acceptance_preparation_family_v2/pr48_guards.py').decode();new_guard=raw(V/'pr48_guards.py').decode()
    for start,end in [('def write(','def dump('),('def fresh_check(','def native_git_snapshot(')]:need(old_guard[old_guard.index(start):old_guard.index(end)]==new_guard[new_guard.index(start):new_guard.index(end)],'M1 repair exact unchanged body')
    # Author private checks are read as evidence with explicit bounded scope.
    for name in ['private_path_controls_v3_actual_capture','private_readback_v3_actual_capture']:capture(V/name,'V3_author_private_captures')
    ready=parse(raw(V/'FINAL_READY_CHECK.json'))
    for n,z in ready['source_files'].items():need(len(raw(V/n))==z['bytes'] and sha(raw(V/n))==z['sha256'],'Exact final readiness member')
    science=parse(raw(V/'SCIENTIFIC_SCOPE.json'));need(science['full_problem_solved'] is False and science['novelty_claimed'] is False and science['paper_or_new_doi_or_tracker'] is False and science['original_substantive_attempts']==2 and science['new_substantive_attempts']==0 and science['audit_turns']==0 and science['related_problem_id']==30004403 and science['related_alias_native_entry_added'] is False,'Inherited exact unresolved shared2/5 scope')
    # Actual ROOT SOURCE closure/readback locations are supplied to this own
    # review by ROOT, never guessed or fabricated by a preparer.
    root_ops=parse(raw(F/'ROOT_SOURCE_OPERATIONS.json'));need(type(root_ops) is list and len(root_ops)==2,'Actual ROOT close then separate readonly')
    chronology=[]
    for z,role in zip(root_ops,['close_source.py','verify_closed_source.py']):
        folder=R/z['capture_path'];folder=folder.parent
        c=capture(folder,'actual_ROOT_V3_source_operations',z['argv']);need(Path(c['argv'][2])==V/role,'Actual ROOT role')
        chronology.extend([dt.datetime.fromisoformat(c['started_utc']),dt.datetime.fromisoformat(c['finished_utc'])]);out=parse(raw(folder/'stdout.bin'));need(out['manifest_sha256']==sha(raw(V/'PREPARATION_MANIFEST.json')),'Actual ROOT returned closure SHA')
        need(out['production_imported_compiled_executed'] is False and out['future_acceptance_approved'] is False,'Source-only ROOT operation')
    need(chronology==sorted(chronology),'Actual ROOT closure then readonly chronological order')
    check_family(V,'PREPARATION_MANIFEST.json',sha(raw(V/'PREPARATION_MANIFEST.json')))
    normalized=sorted(bindings.values(),key=lambda z:z['path']);out={'schema':'pr48-v3-fresh-source-complete-input-bindings/v1','preparation_manifest_sha256':sha(raw(V/'PREPARATION_MANIFEST.json')),'normalized_complete_external_input_bindings':normalized,'groups':{k:sorted(v) for k,v in sorted(groups.items())},'dated_native13_and_four_historical_rows_not_live_pins':True,'foreign_bodies_copied':False,'production_imported_compiled_executed':False,'future_acceptance_approved':False}
    with (F/'INPUT_BINDINGS.json').open('x') as h:json.dump(out,h,sort_keys=True,indent=2);h.write('\n')
    result={'schema':'pr48-v3-fresh-custody-result/v1','status':'PASS_ALL_FIXED_WHOLE_BODY_AND_FULLMODE_INPUTS','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'preparation_manifest_sha256':out['preparation_manifest_sha256'],'normalized_unique_fixed_inputs':len(normalized),'whole_bytes_checked_without_corpus_copy':total_bytes,'source_payload_files':m['files_count'],'actual47_distinct_roles':roles,'actual_ROOT_V3_source_operations':root_ops,'production_imported_compiled_executed':False,'future_acceptance_approved':False}
    with (F/'CUSTODY_RESULT.json').open('x') as h:json.dump(result,h,sort_keys=True,indent=2);h.write('\n')
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
