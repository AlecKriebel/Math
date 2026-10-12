"""Independent scope/dated proposal inspection and bounded production-consistent slices.
No production import, compile or execution. Laboratory records are not approval.
"""
from pathlib import Path
import datetime as dt, hashlib, json, os, re, stat
R=Path('/Users/alec/Documents/Math');F=Path(__file__).absolute().parent;A=F.parent;S=A/'current_preparation_family';observed=dt.datetime.now(dt.timezone.utc);checks=[]
def need(v,n):
    if not v:raise ValueError(n)
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(p):need(not p.is_symlink() and stat.S_ISREG(p.stat().st_mode),'regular');return p.read_bytes()
def bind(p):
    b=raw(p);return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode))
def load(p):return json.loads(raw(p))
def utc(s):return dt.datetime.fromisoformat(s)
def cap_metadata(c,end):
    # Literal semantic shape of prepare_current_packet.py lines187-193, independently written.
    return c['schema']=='root-explicit-command-capture/v1' and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and c['operator_unchanged'] is True and utc(c['started_utc'])<utc(c['finished_utc'])<=end
def main():
    need(raw(A/'ROOT_CURRENT_SOURCE_CLOSURE_PRELAUNCH_SOURCE.py')==raw(S/'close_source_preparation.py'),'real ROOT closer prelaunch equal')
    prep=load(S/'PREPARATION_MANIFEST.json');need(prep['actual_closing_pid']==1200 and prep['source_only'] is True and prep['SOURCE_adversary_verdict'] is None and prep['production_builder_imported_compiled_executed'] is False and prep['production_operator_imported_compiled_executed'] is False and prep['future_acceptance_approved'] is False,'SOURCE null/false boundary')
    capture_rows=[]
    for entry in prep['retained_actual_nonproduction_captures']:
        d=S/entry['directory'];c=load(d/'CAPTURE.json');p=load(d/'PRELAUNCH.json');need(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']==entry['actual_pid'] and type(c['exit_code']) is int and c['exit_code']==entry['exit_code'] and c['operator_unchanged'] is True and c['source_unchanged'] is True and c['production_builder_or_ROOT_operator_executed'] is False and sha(raw(d/'CAPTURE.json'))==entry['capture_sha256'],'actual seven SOURCE children')
        need(all(c[k]==v for k,v in p.items() if k!='schema'),'genuine SOURCE prelaunch values');need(sha(raw(d/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256'] and sha(raw(d/'PRELAUNCH_SOURCE.py'))==c['source_sha256'] and sha(raw(Path(c['argv'][2])))==c['source_sha256'],'real unchanged preparer sources');need(utc(c['finished_utc'])<utc(prep['created_utc']),'completed before SOURCE close')
        for k in ['stdout','stderr']:x=c[k];b=raw(d/x['path']);need(type(x['bytes']) is int and len(b)==x['bytes'] and sha(b)==x['sha256'],'SOURCE complete typed streams')
        need(c['stderr']['bytes']==0 if entry['exit_code']==0 else b'Normative text RENAME_EXCL' in raw(d/'stderr.bin'),'real retained failure');capture_rows.append(dict(directory=entry['directory'],actual_pid=c['pid'],exit_code=c['exit_code'],capture=bind(d/'CAPTURE.json'),finished_utc=c['finished_utc']))
    need(len(capture_rows)==7,'complete preparer nonproduction seven')
    native=['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json'];dated_live=[];proposal_rows=[]
    for n in native:
        label=n.replace('/','__');pre=S/'native4_proposal/preimage'/label;post=S/'native4_proposal/prospective'/label;before=raw(pre);after=raw(post);proposal_rows.extend([bind(pre),bind(post)]);dated_live.append(dict(**bind(R/n),observed_utc=observed.isoformat(),classification='DATED_LIVE_OBSERVATION_NOT_FUTURE_IMMUTABLE_BINDING',matches_prepared_example_at_this_read=raw(R/n)==before))
        if not n.endswith('/QUEUE.md'):need(before==after,'other three prospective byte unchanged')
    before=raw(S/'native4_proposal/preimage/unsolved_math_prioritization__QUEUE.md');after=raw(S/'native4_proposal/prospective/unsolved_math_prioritization__QUEUE.md');bl=before.splitlines(keepends=True);al=after.splitlines(keepends=True);need(len(bl)==len(al),'whole proposal line count')
    diffs=[(i,b,a) for i,(b,a) in enumerate(zip(bl,al)) if b!=a];need(len(diffs)==1,'one target line only');index,b,a=diffs[0];bf=b.decode().split('|');af=a.decode().split('|');need(len(bf)==len(af)==14 and bf[2].strip()==af[2].strip()=='30000703 / OWR-1460-009' and {i for i,(x,y) in enumerate(zip(bf,af)) if x!=y}<={8,9,11} and bf[8].strip()=='queued' and af[8].strip()=='already_solved' and bf[9].strip()==af[9].strip()=='0/5' and bf[10]==af[10] and bf[12]==af[12],'named Status/Turns/Findings only; Chat and DOI preserved')
    status=load(S/'SOURCE_STATUS.json');need(status['current_SOURCE_verdict'] is None and status['production_builder_executed'] is False and status['production_operator_executed'] is False and status['future_acceptance_approved'] is False,'operative SOURCE status')
    # Metadata guard and complete-stream equality are not authorship authentication.
    source_cap=load(R/'draft_pr_publication_program_20260930/audits/pr45_9900007/root_pr49_current_source_closure_actual_capture/CAPTURE.json');end=observed;need(cap_metadata(source_cap,end),'genuine captured close metadata')
    wrong_role=dict(source_cap,argv=['/usr/bin/true']);need(cap_metadata(wrong_role,end),'metadata slice permits a different argv');checks.append(dict(name='CAP4_metadata_shape_does_not_authenticate_argv_role',accepted_by_metadata_slice=True,actual_source_modified=False,classification='OPTIONAL_HARDENING_GENUINE_ROOT_READING_REQUIRED'))
    empty=b'';bool_size=False;need(len(empty)==bool_size and type(bool_size) is not int,'literal production byte-count equality admits boolFalse for empty stream');checks.append(dict(name='CAP4_empty_stream_equality_does_not_enforce_exact_integer',accepted_by_equality_slice=True,actual_saved_stream_sizes_are_plain_integers=True,classification='OPTIONAL_EXPLICIT_TYPED_STREAM_CHECK'))
    need(len('')==0 and type(1200) is int and 1200>0,'wrapped PID is valid');checks.append(dict(name='positive_PID_shape_is_not_execution_authentication',actual_source_closing_pid=1200,actual_separate_readback_pid=1444,classification='REAL_CAPTURE_CHRONOLOGY_AND_SOURCE_REQUIRED'))
    result=dict(schema='pr49-current-source-adversary-scope-and-bounded-limits/v1',status='PASS_EXACT_SCOPE_PROPOSALS_AND_BOUNDED_GUARD_QUALIFICATIONS',actual_pid=os.getpid(),created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),ROOT_source_closer_prelaunch=bind(A/'ROOT_CURRENT_SOURCE_CLOSURE_PRELAUNCH_SOURCE.py'),actual_SOURCE_preparation_captures=capture_rows,dated_native4_observations=dated_live,prepared_proposal_bindings=proposal_rows,changed_proposal_line_one_based=index+1,other3_prospective_bytes_unchanged=True,whole_QUEUE_except_selected_named_cells_byte_unchanged=True,optional_limit_controls=checks,production_imported_compiled_executed=False,helpers_executed=False,future_acceptance_approved=False,mandatory_corrections=[],original_substantive_attempts=0,new_substantive_attempts=0,audit_turns=0)
    with (F/'SCOPE_AND_LIMITS_RESULT.json').open('xb') as h:h.write((json.dumps(result,indent=2,allow_nan=False)+'\n').encode())
    print(json.dumps({k:v for k,v in result.items() if k not in ('actual_SOURCE_preparation_captures','dated_native4_observations','prepared_proposal_bindings')},sort_keys=True))
if __name__=='__main__':main()
