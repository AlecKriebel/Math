"""Own bounded SOURCE/text and already-completed capture inspection. No candidate import/compile/run."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat
F=Path(__file__).absolute().parent;A=F.parent;R=A.parents[2];S=A/'acceptance_preparation_family_v2';V=A/'acceptance_source_adversary_family_v2_fresh'
def need(q,m):
    if not q:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
checks=[];neg=[]
def positive(n,q):need(q,n);checks.append(n)
def rejects(n,f):
    try:f()
    except ValueError:neg.append(n)
    else:raise ValueError('Accepted private mutant '+n)
text=(F/'author_ROOT_acceptance.py').read_text();source=(F/'author_ROOT_acceptance.py').read_bytes()
for label,body in [('exact49_family',"H=A/'acceptance_preparation_family_v2'"),('exact_fresh_review',"F=A/'acceptance_source_adversary_family_v2_fresh'"),('exact49_prep','52795f5940b255fb25eb1dfc958de37dcc570dc21a411e83c40eba3dd71bc27c'),('exact54_fresh_review','1c9ec221a2679f490431c41cd653fe35748cc52cd80df427886f57a4fa0233a0'),('exact48V3','9c525f7b540068af07477e8f794e21596d93e69e49e8dbc52972d3196eb9fda4'),('actual48_RUNTIME_not_static_pin',"def predecessor():"),('six_ordered_roles',"phases=['preflight','overlay','prepush','finalize','mirror','post']"),('whole_ordered_argv',"need(eq(c['argv'],argv)"),('all_phase_before_after_modes',"for epoch in ['before','after']:"),('all_fixed_individual_tables',"[375,3229,154,148]"),('CAP_reference_retains_mode',"return dict(capture=ref(p,True)"),('originalSOURCE_science_counts',"science['original_source_response_count'] is None"),('fixed_only_plan_complete3229',"[triple(z) for z in rootwhole['normalized_complete_fixed_bindings']]"),('exact_foreign_log_exemption',"n==(PROGRAM/'RESEARCH_LOG.md').relative_to(R).as_posix()"),('clean_index',"Strict clean index before approval"),('timeout_full_capture_before_failure',"failures/timeout retain true PID/UTC/streams"),('no_optional_index_lock',"GIT_OPTIONAL_LOCKS='0'"),('explicit_source_attestation',"'--personally-read-complete-source'"),('missing_actual48_fails_before_runtime_creation',"previous,post,rp,previouscaps,root48cap=predecessor()")]:positive(label,body in text)
positive('only_standard_library_imports',all('pr49_guards' not in line and 'pr48_guards' not in line and 'importlib' not in line and 'exec(' not in line and 'compile(' not in line for line in text.splitlines() if line.startswith(('import ','from '))))
positive('initial_SOURCE_preserved',sha((F/'SOURCE_INITIAL_AUTHOR.py').read_bytes())==load(F/'PREPARATION_BINDINGS.json')['author']['sha256'])
sm=load(S/'PREPARATION_MANIFEST.json');vm=load(V/'SELF_MANIFEST.json');positive('actual129_SOURCE_schema',sm['schema']=='pr49-acceptance-source-closure/v2' and type(sm['files_count']) is int and sm['files_count']==129);positive('actual54_review_schema',vm['schema']=='pr49-fresh-acceptance-source-adversary-closure/v1' and vm['files_count']==54)
# Independent literal-row models expose the two actual template distinctions.
def frozen_mode(v):need((type(v) is int and v==0o444) or (type(v) is str and v=='0444'),'Exact closed permission representation')
for p in [A/'reviewed_candidate/MANIFEST.json',A/'current_whole_adversary_family/SELF_MANIFEST.json']:
    q=load(p)
    for z in q['files']:frozen_mode(z['full_mode'])
positive('current1544_andWHOLE127_literal_integer_modes',True)
for value in [True,False,0,420,0o1444,292.0,'444','292',None]:rejects('bad_frozen_mode_'+repr(value),lambda value=value:frozen_mode(value))
q=load(A/'current_whole_adversary_family/SELF_MANIFEST.json');dirs=set(q['directories']);rows=q['directory_full_modes'];positive('whole_root_dot_is_declared17th_mode',len(rows)==len(dirs)+1 and {z['path'] for z in rows}==dirs|{'.'})
def directory_domain(values):need(len(values)==len(dirs)+1 and {z['path'] for z in values}==dirs|{'.'},'Whole literal root plus all relative dirs')
rejects('whole_root_mode_omitted',lambda:directory_domain([z for z in rows if z['path']!='.']))
rejects('duplicate_whole_root_mode',lambda:directory_domain(rows+[next(z for z in rows if z['path']=='.')]))
captured=[]
groups=[(S,{'AUTHORING_ACTUAL_CAPTURE':1,'REPAIR_AUTHOR_ACTUAL_CAPTURE':0,'AUTHORING_V2_ACTUAL_CAPTURE':0,'PRIVATE_CONTROLS_ACTUAL_CAPTURE':0,'FINAL_PRIVATE_CONTROLS_ACTUAL_CAPTURE':0,'PREDECESSOR_DESIGN_BINDING_ACTUAL_CAPTURE':0,'FINAL_SOURCE_READINESS_ACTUAL_CAPTURE':0}),(V,{'independent_controls_actual':1,'independent_controls_v2_actual':1,'independent_controls_v3_actual':0,'fixed_source_custody_actual':0})]
for base,names in groups:
    for n,code in names.items():
        d=base/n;c=load(d/'CAPTURE.json');pre=c['prelaunch'];need(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and c['exit_code']==code and c['source_unchanged'] is True and c['operator_unchanged'] is True,'Actual original child flags')
        need(sha((d/'PRELAUNCH_SOURCE.py').read_bytes())==pre['source_sha256'] and sha((d/'PRELAUNCH_OPERATOR.py').read_bytes())==pre['operator_sha256'] and load(d/'PRELAUNCH.json')==pre,'Full actual prelaunch')
        for k in ['stdout','stderr']:
            z=c[k];b=(d/z['path']).read_bytes();need(len(b)==z['bytes'] and sha(b)==z['sha256'],'Whole actual stdout/stderr')
        need((d/'stderr.bin').read_bytes()==b'' if code==0 else bool((d/'stderr.bin').read_bytes()),'Exact failure/success stream disposition')
        captured.append(dict(path=str((d/'CAPTURE.json').relative_to(R)),pid=c['pid'],exit_code=code,full_mode=stat.S_IMODE((d/'CAPTURE.json').stat().st_mode)))
positive('all11_completed_preparer_and_fresh_review_success_fail_captures',len(captured)==11)
result=dict(schema='pr49-ROOT-author-bounded-SOURCE-consistency/v1',status='PASS_SOURCE_TEXT_AND_COMPLETED_CAPTURE_MODELS_ONLY',actual_private_reader_pid=os.getpid(),utc=dt.datetime.now(dt.timezone.utc).isoformat(),checks=checks,expected_private_rejections=neg,complete_completed_capture_bindings=captured,current_author=dict(path=str((F/'author_ROOT_acceptance.py').relative_to(R)),bytes=len(source),sha256=sha(source)),generated_author_imported_compiled_executed=False,proposed_or_historical_production_imported_compiled_executed=False,actual48_post_approved_or_pinned=False,ROOT_approval_created=False,native_Git_remote_write=False)
with (F/'SOURCE_CONSISTENCY_RESULT.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps(result))
