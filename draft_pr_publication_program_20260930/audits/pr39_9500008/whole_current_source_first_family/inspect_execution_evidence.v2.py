#!/usr/bin/env python3
"""Independent reader of retained evidence. Never imports or runs reviewed code."""
import collections
import copy
import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import sqlite3

OWN = Path(__file__).resolve().parent
A = OWN.parent
REPO = A.parents[2]
C = A/'reviewed_candidate'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def pairs(rows):
    out = {}
    for k,v in rows:
        if k in out: raise ValueError('duplicate key '+k)
        out[k] = v
    return out
def parse(raw): return json.loads(raw, object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
def load(path): return parse(Path(path).read_bytes())
def safe(path):
    p=Path(path)
    assert p.is_relative_to(A) and p.is_file()
    assert not any(x.is_symlink() for x in [p,*p.parents] if x.is_relative_to(A))
    return p
def record(row, base=A):
    p=Path(row['path'])
    if not p.is_absolute(): p=base/p
    raw=safe(p).read_bytes()
    assert len(raw)==row.get('size',row.get('bytes')) and sha(raw)==row['sha256'],str(p)
    return raw
inv=load(OWN/'WHOLE_BOUNDARY_INVENTORY.json')
reviewed_code={x['sha256'] for x in inv['unique_python_sources']}
r=load(A/'ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json')
assert r['status']=='PASS' and r['setup_completed'] is True and r['retention_errors']==[]
assert (r['original_substantive_turns'],r['turn_limit'],r['new_substantive_attempts'],r['audit_turns'])==(2,5,0,0)
assert r['full_problem_solved'] is False
detail={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'execution_rows':[],'structured_comparisons':[],'typed_attempts':[]}
def runrow(row,kind):
    assert row['launch_attempted'] is True and row['actual_execution'] is True and row['completed'] is True
    assert row['exit_code'] in (0,1) and row.get('error') is None and row.get('failure_type') is None
    assert datetime.datetime.fromisoformat(row['started_utc'])<=datetime.datetime.fromisoformat(row['ended_utc'])
    out,err=record(row['stdout']),record(row['stderr'])
    if 'prelaunch_source' in row:
        src=record(row['prelaunch_source']); assert sha(src)==row['script_sha256'] in reviewed_code
    if 'script' in row:
        s=row['script'];src=safe(s['retained_full_source']).read_bytes()
        assert len(src)==s['size'] and sha(src)==s['sha256'] in reviewed_code
    for item in row.get('generated_files',{}).get('created_or_changed',[]): record(item)
    capture=row['stdio_capture'];assert capture=={'kind':'complete_child_streams','stdout_available':True,'stderr_available':True}
    detail['execution_rows'].append({'kind':kind,'label':row.get('label',row.get('outer_label')),'index':row.get('nested_index'),
                                   'exit_code':row['exit_code'],'stdout_sha256':sha(out),'stderr_sha256':sha(err),
                                   'stdout_bytes':len(out),'stderr_bytes':len(err)})
    return out,err
assert [len(r[k]) for k in ['actual_outer_program_runs','actual_nested_program_runs','actual_administrative_command_runs']]==[14,88,2]
for row in r['actual_outer_program_runs']+r['actual_administrative_command_runs']: runrow(row,'outer_or_admin')
for row in r['actual_nested_program_runs']:runrow(row,'nested')
S=A/r['support_directory']
assert load(S/'outer_runs.json')==r['actual_outer_program_runs']
assert load(S/'administrative_runs.json')==r['actual_administrative_command_runs']
nested=[]
for p in sorted(S.glob('*_nested/nested_runs.json')):
    rows=load(p)
    nested.extend({'outer_label':p.parent.name[:-7],'nested_index':i,**x} for i,x in enumerate(rows))
    status=load(p.parent/'CAPTURE_STATUS.json')
    assert status['status']=='PASS' and status['original_failure'] is None and status['retention_errors']==[]
    assert status['nested_attempt_count']==len(rows) and status['helper_invocation']['helper_invocation_completed'] is True
assert nested==r['actual_nested_program_runs']
for row in r['original_replays']:
    expected=record(row['expected_receipt']);actual=record(row['actual_stdout']);generated=record(row['generated_receipt'])
    assert expected==actual==generated and not record(row['actual_stderr'])
    assert parse(generated)==row['complete_actual_result']
    assert sha((A/'source_snapshot'/row['program']).read_bytes())==row['program_sha256']
    candidates=[x for x in nested if x['outer_label']=='root_original_'+row['label']]
    # The original program is run as the instrumented outer helper. Its actual
    # file write is retained in outer_generated, separate from raw outer stdout.
    outer=load(S/('root_original_'+row['label']+'_nested/outer_generated_files.json'))
    assert any(record(x)==expected and x['original_relative_path']==Path(row['generated_receipt']['path']).name for x in outer['created_or_changed'])
assert [x['stdout_bytes'] for x in r['original_replays']]==[520,520,899]
failure=r['default_python314_actual_failure'];assert record(failure['actual_stdout'])==b''
assert b"ModuleNotFoundError: No module named 'sympy'" in record(failure['actual_stderr'])
assert failure['generated_result_absent'] is True and failure['exit_code']==1
policy=r['comparison_exclusion_policy'];assert policy['clock_keys']==['at','ended_utc','started_utc','time_utc','utc']
prefix=policy['single_private_path_prefix'];assert prefix['saved']==str(REPO)
def normalize(v):
    if isinstance(v,dict):return {k:normalize(x) for k,x in v.items() if k not in policy['clock_keys']}
    if isinstance(v,list):return [normalize(x) for x in v]
    if isinstance(v,str):return v.replace(prefix['actual'],prefix['saved'])
    return v
def diff(a,b,p='$'):
    if type(a)!=type(b):return [{'path':p,'actual':a,'saved':b}]
    if isinstance(a,dict):
        if set(a)!=set(b):return [{'path':p,'actual_keys':sorted(a),'saved_keys':sorted(b)}]
        return [x for k in a for x in diff(a[k],b[k],p+'/'+k)]
    if isinstance(a,list):
        if len(a)!=len(b):return [{'path':p,'actual_length':len(a),'saved_length':len(b)}]
        return [x for i in range(len(a)) for x in diff(a[i],b[i],p+'/'+str(i))]
    return [] if a==b else [{'path':p,'actual':a,'saved':b}]
assert len(r['full_structured_receipt_comparisons'])==4
for row in r['full_structured_receipt_comparisons']:
    a,b=record(row['actual']),record(row['saved']);delta=diff(normalize(parse(a)),normalize(parse(b)))
    assert delta==row['full_JSON_differences'] and (a==b)==row['complete_JSON_BYTE_equal']
    assert (not delta)==row['equal_after_explicit_clock_and_private_path_exclusions']
    q=row['precise_qualifications'];assert set(q)=={x['path'] for x in delta}
    for x in delta:
        item=q[x['path']];assert x==item['difference']
        sa,sb=record(item['actual_complete_stream']),record(item['saved_complete_stream'])
        assert normalize(sa.decode())==normalize(sb.decode())
        assert x['path'].endswith('/stderr_sha256') and x['actual']==sha(sa) and x['saved']==sha(sb)
    detail['structured_comparisons'].append({'label':row['label'],'full_differences':delta,'qualification_count':len(q)})
assert sum(x['qualification_count'] for x in detail['structured_comparisons'])==10
controls=S/'actual/final_partial_or_complete/reconstructed_controls'
assert load(controls/'PACKET_CONTROL_RESULTS.json')==r['real_packet_controls']
assert load(controls/'MANIFEST_CONTROL_RESULTS.json')==r['real_manifest_controls']
for row in r['real_packet_controls']+r['real_manifest_controls']:
    out=(controls/row['stdout']).read_bytes();err=(controls/row['stderr']).read_bytes()
    assert sha(out)==row['stdout_sha256'] and sha(err)==row['stderr_sha256']
    assert row['observed_expected'] is True and row['exit_code']==row['expected_exit']
    match=[x for x in nested if x['outer_label']=='root_reconstructed_packet_and_manifest_controls' and x['argv']==row['argv']]
    assert len(match)==1 and record(match[0]['stdout'])==out and record(match[0]['stderr'])==err
    if 'case' in row:
        assert row['strict_root_guard_pass']==(row['case']=='baseline')
        if row['case']!='baseline':assert row['expected_rejection_marker'].encode() in out+err
    elif 'expected_rejection_reason' in row:assert row['expected_rejection_reason'] in parse(out)['reason']
assert [len(r[k]) for k in ['real_packet_controls','real_manifest_controls']]==[6,28]
cases=load(A/'root_typed_entry_execution_revision/control_cases.json')
assert len(cases)==17
for suffix in ['', '_v2']:
    folder=A/('root_typed_entry_actual_capture'+suffix);receipt=load(folder/'TYPED_ENTRY_RECEIPT.json');rows=receipt['actual_runs']
    assert len(rows)==20 and load(folder/'RUNS.json')==rows and receipt['builder_invoked'] is True
    assert receipt['new_substantive_attempts']==receipt['audit_turns']==0
    for row in rows:
        src=record(row['source']);assert sha(src) in reviewed_code
        out,err=record(row['stdout']),record(row['stderr'])
        assert row['actual_execution'] is True and row['completed'] is True and row['launch_attempted'] is True
        assert row['stdin_supplied'] is False and row['stdio_kind']=='complete_child_streams'
        assert datetime.datetime.fromisoformat(row['started_utc'])<=datetime.datetime.fromisoformat(row['ended_utc'])
        if row['label'] in ['typed_baseline','typed_final_prebuild']:
            assert row['exit_code']==0 and not err and parse(out)=={'status':'ACCEPTED_TYPED_METADATA','entries':38,'isolated_control':False}
        elif row['label']!='unchanged_builder':
            case=next(x for x in cases if x['label']==row['label']);value=load(A/case['entry']);parent=value
            for k in case['path'][:-1]:parent=parent[k]
            k=case['path'][-1]
            if case['action']=='set':parent[k]=case['value']
            elif case['action']=='delete':del parent[k]
            elif case['action']=='duplicate_row':parent[k][1]=copy.deepcopy(parent[k][0])
            else:assert case['action']=='duplicate_key'
            raw=(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode()
            if case['action']=='duplicate_key':raw=(json.dumps(value)[:-1]+', '+json.dumps(str(k))+': '+json.dumps(parent[k])+'}\n').encode()
            assert (folder/'controls'/(case['label']+'.input.json')).read_bytes()==raw
            j=parse(out);assert row['exit_code']==1 and not err and j['status']=='REJECTED_TYPED_METADATA' and j['kind']==case['expected_kind']
        else:
            if not suffix:assert row['exit_code']==1 and b'Unreviewed retained capability' in err and receipt['status']=='FAIL'
            else:assert row['exit_code']==0 and not err and parse(out)==receipt['builder_result']
    outer=A/('root_current_typed_outer_capture'+suffix);cap=load(outer/'CAPTURE.json')
    assert cap['actual_execution'] is True and cap['completed'] is True and cap['exit_code']==(0 if suffix else 1)
    assert sha((outer/'prelaunch_source.py').read_bytes())==cap['source_sha256']
    for channel in ['stdout','stderr']:record(cap[channel],outer)
    detail['typed_attempts'].append({'suffix':suffix,'capture_sha256':sha((outer/'CAPTURE.json').read_bytes()),'receipt_sha256':sha((folder/'TYPED_ENTRY_RECEIPT.json').read_bytes()),'rows':len(rows),'rejected_mutants':17,'successful':bool(suffix)})
bad=inv['strict_json_failures'];qual=[]
for x in bad:
    raw=(A/x['path']).read_bytes()
    if raw==b'Undeclared first-party member must be rejected.\n':
        assert 'actual_manifest_controls/nested_manifest_same_basename/nested/PRIMARY_SCOPE_FAMILY_MANIFEST.json' in x['path']
        producer=A/'primary_scope_family/run_manifest_controls.py';assert b"write_text('Undeclared first-party member must be rejected.\\n')" in producer.read_bytes()
        results=load(A/'primary_scope_family/MANIFEST_NEGATIVE_CONTROL_RESULTS.json')
        assert any(y.get('control',y.get('name'))=='nested_manifest_same_basename' and y['returncode']==1 for y in results.get('controls',results.get('records',[])))
        mechanism='exact unlisted nested first-party member; original primary validator rejects membership'
    elif raw==b'Nested same-basename extra control.\n':
        assert 'actual_control_inputs/manifests/' in x['path'] and '/nested_manifest_extra/nested/' in x['path']
        family=x['path'].split('actual_control_inputs/manifests/')[1].split('/')[0]
        assert any(y['family']==family and y['case']=='nested_manifest_extra' and y['exit_code']==1 and y['strict_root_guard_pass'] is False for y in r['real_manifest_controls'])
        mechanism='exact root constructed nested member; original validator and strict root guard both reject'
    else:
        assert x['path'].endswith('/controls/duplicate_JSON_key.input.json') and len(raw)==1545 and sha(raw)=='8229604f25ce4cf93ac9b7f4bf5e4a05905b14f5cdd2afb28618727665977f2b'
        try:parse(raw)
        except ValueError as error:assert 'duplicate key status' in str(error)
        else:raise AssertionError('duplicate input incorrectly accepted')
        mechanism='exact duplicated status key reconstructed from original science card; typed guard rejects duplicate_key'
    qual.append({**x,'classification':'deliberate negative INPUT only, never proof or positive receipt','checked_provenance_and_rejection':mechanism})
detail['individual_malformed_qualification']=qual
assert len(qual)==14
# Whole source/prior and entire raw-to-SQL importer join, independent of queue imports.
native=REPO/'unsolved_math_prioritization';manifest=load(S/'native_preimages/unsolved_math_prioritization/manifest.json')
raw={}
for name,row in manifest['files'].items():
    b=(native/'cache'/name).read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'];raw[name]=parse(b)
problems,reports=raw['problems.json'],raw['research_results.json'];counts=collections.Counter(x['problem_number'] for x in problems)
expected={}
for x in problems:
    p=copy.deepcopy(x)
    if counts[p['problem_number']]>1 and p['problem_number'] in reports:p['_ambiguous_report']=True
    expected[str(p['id'])]=(p,{} if p.get('_ambiguous_report') else reports.get(p['problem_number'],{}))
assert len(expected)==len(problems)==15458 and len(reports)==6701
db=native/'cache/catalog.sqlite';conn=sqlite3.connect(db.as_uri()+'?mode=ro&immutable=1',uri=True);conn.execute('PRAGMA query_only=ON')
assert conn.execute('SELECT revision FROM metadata').fetchall()==[(manifest['revision'],)]
seen=set()
for key,p,prior in conn.execute('SELECT key,payload,report FROM records ORDER BY key'):
    assert key not in seen and (parse(p),parse(prior))==expected[key];seen.add(key)
conn.close();assert seen==set(expected)
p,prior=expected['9500008'];assert counts['AMR-094-0008']==1 and prior and 'AMR-094-0008' in reports
assert p==load(A/'source_snapshot/source_record.json')==r['provenance']['complete_flat_problem']
assert prior==load(A/'source_snapshot/prior_report.json')==r['provenance']['complete_actual_prior_report']
score=r['provenance']['pure_queue_score'];assert score['statement_hash']==sha(p['statement'].encode())
assert score['review_hash']==sha(json.dumps([p,prior],sort_keys=True).encode())
detail['source_prior_SQL']={'all_rows':len(seen),'raw_bytes':sum(x['bytes'] for x in manifest['files'].values()),'raw_key_present':True,'fallback_used':False,'whole_pair_equal':True,'statement_hash':score['statement_hash'],'review_hash':score['review_hash']}
# Exact original archive and scientific top-level preservation.
snap=load(A/'snapshot_manifest.json')
for row in snap['files']:assert record({'path':'source_snapshot/'+row['path'],'size':row['size'],'sha256':row['sha256']})==(C/'original_archive'/row['path']).read_bytes()
immut=[x['path'] for x in snap['files'] if x['path'] not in ['README.md','RESEARCH_LOG.md','review/REVIEW.md','review/verdict.json','review/runtime.json']]
for name in immut:assert (C/name).read_bytes()==(A/'source_snapshot'/name).read_bytes(),name
detail['original_archive']=len(snap['files']);detail['unchanged_scientific_top_level']=immut
pre=(C/'queue_proposal/QUEUE_PREIMAGE.md').read_text().splitlines(keepends=True)
post=(C/'queue_proposal/QUEUE_PROSPECTIVE.md').read_text().splitlines(keepends=True)
assert len(pre)==len(post);idx=[i for i in range(len(pre)) if pre[i]!=post[i]];assert len(idx)==1
i=idx[0];before=pre[i].split('|');after=post[i].split('|');assert len(before)==len(after)==14 and '9500008 / AMR-094-0008' in pre[i]
assert [j for j in range(14) if before[j]!=after[j]]==[7,8,12]
assert after[7].strip()=='unsolved' and after[8].strip()=='2/5'
detail['queue_named_cell_delta']={'line':i+1,'changed_cells':[7,8,12],'before':pre[i],'after':post[i],'scope':'complete preserved preimage/prospective comparison, no live native write'}
detail['status']='PASS_INDEPENDENT_WHOLE_RETAINED_EVIDENCE_INSPECTION'
(OWN/'INDEPENDENT_EXECUTION_EVIDENCE_INSPECTION.json').write_text(json.dumps(detail,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in detail.items() if k not in ['execution_rows','individual_malformed_qualification']},indent=2))
