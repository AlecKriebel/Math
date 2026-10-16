#!/usr/bin/python3
"""Read all fixed first-party bodies with four explicit actual closure schemas."""
import datetime,hashlib,json,math,pathlib,re,stat
F=pathlib.Path(__file__).resolve().parent;A=F.parent;R=A.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def full(p):return stat.S_IMODE(p.stat().st_mode)
def load(b):
    def pairs(xs):
        d={}
        for k,v in xs:
            if k in d:raise ValueError('Duplicate JSON key')
            d[k]=v
        return d
    def constant(v):raise ValueError('Nonfinite JSON')
    def floating(v):
        x=float(v)
        if not math.isfinite(x):raise ValueError('Nonfinite JSON')
        return x
    return json.loads(b,object_pairs_hook=pairs,parse_constant=constant,parse_float=floating)
fixed={};total=0
def bind(p):
    global total
    assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
    b=p.read_bytes();n=p.relative_to(R).as_posix();row={'path':n,'bytes':len(b),'sha256':sha(b),'full_mode':full(p)}
    if n in fixed:assert fixed[n]==row
    else:fixed[n]=row;total+=len(b)
    if p.suffix=='.json':load(b)
    elif p.suffix=='.jsonl' and b:
        try:load(b)
        except json.JSONDecodeError:
            for line in b.splitlines():assert line.strip();load(line)
    assert p.suffix.lower() not in {'.pdf','.png','.jpeg','.jpg','.sqlite','.db','.html'}
    return b,row
specs=[
 ('original','ORIGINAL_PREPARATION_MANIFEST.json','pr49-original-preparation-self-only-manifest/v1','2eecad772938f3b220936c3317f1266d9a98de0f9d9750a6efa725c665f63b4c',350),
 ('boundary','boundary_analysis_family/MANIFEST.json','pr49-boundary-independent-self-only-closure/v1','24543fa2de740787f3374e958cca7dc170ab92797f0c42f94b0b3c3f71fa756e',473),
 ('hyperbolic','hyperbolic_geometry_family/SELF_MANIFEST.json','pr49-hyperbolic-family-self-only/v1','07650b4164489112dbeb4668f9c08d9e87944a5d948c1dd33aa7549e42b239c6',107),
 ('ROOT','root_original_actual_reproduction/MANIFEST.json','pr49-root-original-complete-reproduction-self-only-closure/v1','6a0f39d01777401d85df104be5ba1489f107cf8707dc5151fdc6ebaff2d26796',192)]
closed={}
for key,name,schema,expected,count in specs:
    path=A/name;raw,mrow=bind(path);assert sha(raw)==expected and full(path)==0o444;m=load(raw);assert m['schema']==schema;root=path.parent
    if key=='original':
        payload=m['files'];assert m['files_count']==count and m['self_excluded']==[path.name]
        actual=set(m['authorship_root_files'])
        for n in m['authorship_directory_roots']:
            actual|={q.relative_to(root).as_posix() for q in (root/n).rglob('*') if q.is_file()}
        dirs=[{'path':'.','full_mode':m['authorship_root_full_mode']}]+m['owned_directory_bindings']
    elif key=='boundary':
        payload=m['members'];assert m['member_count']==count and m['self_excluded']==[path.name];dirs=m['directories']
        actual={q.relative_to(root).as_posix() for q in root.rglob('*') if q.is_file() and q!=path}
    elif key=='hyperbolic':
        payload=[dict(r,full_mode=int(r['mode'],8)) for r in m['payload_files']];assert m['manifest_self']['path']==path.name and m['manifest_self']['mode']=='0444'
        dirs=[{'path':'.','full_mode':full(root)}]+[{'path':r['path'],'full_mode':int(r['mode'],8)} for r in m['directories']]
        actual={q.relative_to(root).as_posix() for q in root.rglob('*') if q.is_file() and q!=path}
    else:
        payload=m['files'];assert m['files_count']==count and m['self_excluded']==[path.name]
        dirs=[{'path':'.','full_mode':full(root)}]+[{'path':n,'full_mode':full(root/n)} for n in m['directories']]
        actual={q.relative_to(root).as_posix() for q in root.rglob('*') if q.is_file() and q!=path}
    assert len(payload)==count and actual=={r['path'] for r in payload}
    members=[]
    for row in payload:
        b,r=bind(root/row['path']);assert len(b)==row['bytes'] and sha(b)==row['sha256'] and r['full_mode']==row['full_mode']==0o444;members.append(r)
    derived={'.'}|{p.as_posix() for n in actual for p in pathlib.PurePosixPath(n).parents if p.as_posix()!='.'}
    assert derived=={d['path'] for d in dirs}
    for d in dirs:assert full(root/d['path'])==d['full_mode']
    info={'root':root.relative_to(R).as_posix(),'schema':schema,'manifest':mrow,'self_name':path.name,'payload_count':count,'members':members,'directories':dirs}
    if key=='original':info.update(authorship_root_files=m['authorship_root_files'],authorship_directory_roots=m['authorship_directory_roots'])
    closed[key]=info
summary=load(bind(A/'root_original_actual_reproduction/ROOT_CURRENT_REPRODUCTION_SUMMARY.json')[0])
result=load(bind(A/'root_original_actual_reproduction/ROOT_REPRODUCTION_RESULT.json')[0]);raw=load(bind(A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json')[0])
assert summary['actual_completed_raw_PID']==raw['actual_pid']==62744 and summary['known_credited_full_target_only'] is True and summary['project_solved'] is False
assert result['actual_operator_pid']==60012 and len(result['complete_actual_Git_captures'])==33 and len(result['complete_actual_helper_captures'])==3
assert result['entire_replayed_results']['author']==result['complete_original_JSON_values']['verification.json']
assert result['entire_replayed_results']['identical_submitted']==result['entire_replayed_results']['author'] and result['identical_submitted_counted_independent'] is False
assert raw['full_raw_and_prior_bytes']==149266659 and raw['all_SQL_rows']==len(raw['complete_row_bindings'])==15458 and raw['selected_prior_key_present'] is False and raw['raw_null_present'] is False and raw['selected_prior_fallback']=={} and raw['SQLite_literal_fallback']=='{}' and raw['literal_original_prior_file_value'] is None
for r in summary['external_completed_first_party_bindings']:
    b,row=bind(R/r['path']);assert row==r
for name in ['root_pr49_original_preparation_closure_actual_capture','root_pr49_original_preparation_closed_readback_actual_capture','root_pr49_boundary_family_closure_actual_capture','root_pr49_boundary_family_closed_readback_actual_capture','root_pr49_hyperbolic_family_closure_actual_capture','root_pr49_hyperbolic_family_closed_readback_actual_capture','root_pr49_reproduction_closure_actual_capture','root_pr49_closed_reproduction_readback_actual_capture']:
    d=A.parent/'pr45_9900007'/name
    assert d.is_dir()
    c=load(bind(d/'CAPTURE.json')[0]);assert c['schema']=='root-explicit-command-capture/v1' and c['completed'] is True and c['exit_code']==0
    for p in d.iterdir():bind(p)
bind(A/'ROOT_MATHEMATICAL_REVIEW.md')
pins={'schema':'pr49-fixed-current-source-inputs/v1','status':'SOURCE_ONLY_ROOT_PREREQUISITES_PENDING','production_builder_executed':False,'future_acceptance_approved':False,'fixed_rows':sorted(fixed.values(),key=lambda x:x['path']),'closed_inputs':closed,'exact_literal_structured_exceptions':[],'historical_captured_full_modes_not_rewritten':True,'actual_closed_full_modes_bound_separately':True}
(F/'STATIC_INPUT_BINDINGS.json').write_text(json.dumps(pins,indent=2)+'\n')
out={'schema':'pr49-source-input-inspection/v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'unique_fixed_first_party_bodies':len(fixed),'all_bodies_read_bytes':total,'four_distinct_schemas_verified':True,'closed_payload_counts':{k:v['payload_count'] for k,v in closed.items()},'foreign_bodies_copied':False,'ROOT33Git_and3helpers_exact':True,'ROOT_raw_rows':15458,'ROOT_raw_full_bytes':149266659,'production_builder_imported_compiled_executed':False,'new_substantive_attempts':0,'audit_turns':0}
(F/'SOURCE_INPUT_INSPECTION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
