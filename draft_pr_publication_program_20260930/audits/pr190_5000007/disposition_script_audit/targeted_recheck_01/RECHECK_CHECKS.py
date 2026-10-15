"""Targeted AST/function and disposable-fixture checks; no production imports/APIs."""
from pathlib import Path
from contextlib import redirect_stdout
import ast,copy,datetime,hashlib,io,json,re,shutil,tempfile,types
D=Path(__file__).resolve().parent;A=D.parent.parent
PREFIX='draft_pr_publication_program_20260930/';CASE=PREFIX+'audits/pr190_5000007/';NATIVE='unsolved_math_prioritization/attempts/5000007/'
HEAD='0c3346c8ebcb3b967a1d8bf9a283f027b44b738c'
TARGETS=['campaign_aliases.py','prepare_final_scoped_merge.py','prepare_factual_completion.py','prepare_native_final_01.py','prepare_final_main_scope.py','prepare_publication_lifecycle_scripts_02.py','prepare_lifecycle_utilities_20261015.py','ROOT_DISPOSITION_REPAIR_01.json','ROOT_PUBLICATION_GATE.json']
def require(x,msg):
    if not x:raise RuntimeError(msg)
def pin(p):
    b=p.read_bytes();return bpin(b)
def bpin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def plainpin(p):return {k:v for k,v in pin(p).items() if k!='git_blob'}
def save(p,j):p.write_text(json.dumps(j,indent=2)+'\n')
def extract(name,func,env):
    node=next(n for n in ast.parse((A/name).read_text()).body if isinstance(n,ast.FunctionDef) and n.name==func)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[node],type_ignores=[])),str(A/name),'exec'),env)
    return env[func]
results={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'script_pins':{n:plainpin(A/n) for n in TARGETS},'remote_calls':0,'production_imports':0,'checks':[]}
def check(name,condition,detail=None):
    require(condition,'FAILED '+name)
    results['checks'].append({'name':name,'passed':True,**({'detail':detail} if detail is not None else {})})
for n in TARGETS:
    if n.endswith('.py'):ast.parse((A/n).read_text())
oldseal=json.loads((D.parent/'FINAL_SEAL.json').read_text())
check('prior_sealed_audit_unchanged',all(plainpin(D.parent/x['path'])=={'bytes':x['bytes'],'sha256':x['sha256']} for x in oldseal['manifest']))
repair=json.loads((A/'ROOT_DISPOSITION_REPAIR_01.json').read_text())
check('repair_record_matches_actual_lifecycle_code',all(plainpin(A/n)==v for n,v in repair['after'].items()) and plainpin(A/'campaign_aliases.py')==repair['normalization_helper'])
scope_constants={n.value for n in ast.walk(ast.parse((A/'prepare_final_main_scope.py').read_text())) if isinstance(n,ast.Constant) and isinstance(n.value,str)}
check('scope_includes_runtime_alias_helper_and_original_safe_audit',{'campaign_aliases.py','ROOT_DISPOSITION_REPAIR_01.json','repair_disposition_safeguards_01.py','disposition_script_audit/SAFE_AUTHORED_ALLOWLIST.json'}<=scope_constants)

# Extract the actual alias helper without importing a production module.
aliases={'copy':copy,'datetime':datetime,'CASE':'audits/pr190_5000007/','require':require}
normalize=extract('campaign_aliases.py','normalize',aliases)
obs=json.loads((D.parent/'LIVE_MAIN_ALIAS_OBSERVATION.json').read_text())
base={**copy.deepcopy(obs['top_level_scalars']),**copy.deepcopy(obs['selected_live_collections'])}
base['historical_completed_case_records']=[{'PR':177,'immutable_history':'sentinel for exact preservation'}]
old_history=copy.deepcopy(base['historical_completed_case_records'])
g={'package_name':'publication_package_v2','whole_package_reviews':['AUDIT-MOCK-R1','AUDIT-MOCK-R2']}
z={'state':'published','doi':'10.0000/AUDIT-MOCK','doi_url':'https://example.invalid/AUDIT-MOCK','record_url':'https://example.invalid/AUDIT-MOCK-RECORD'}
tr={'status':'TRACKER_APPEND_AND_TWO_FRESH_READS_ACCEPTED','DOI':z['doi'],'range':"'Math Puzzles'!A999:D999"}

# Execute actual phase95 update/normalize statements, excluding its save/API work.
tree=ast.parse((A/'prepare_final_scoped_merge.py').read_text())
prep=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='prepare')
phase95_statements=[]
for n in prep.body:
    if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call):
        f=n.value.func
        if isinstance(f,ast.Attribute) and isinstance(f.value,ast.Name) and ((f.value.id=='j' and f.attr=='update') or (f.value.id=='alias_module' and f.attr=='normalize')):phase95_statements.append(n)
env={'j':copy.deepcopy(base),'stamp':'AUDIT-MOCK','z':z,'tr':tr,'alias_module':types.SimpleNamespace(normalize=normalize)}
exec(compile(ast.fix_missing_locations(ast.Module(body=phase95_statements,type_ignores=[])),'actual-phase95-statements','exec'),env)
j95=env['j']
retired=['actual_factual_checkpoint_accepted','active_checkpoint_commit','last_completed_writer_operation_finished','read_only_next_case','next_intake_requires_actual_completion_receipt_and_explicit_writer_release']
check('phase95_actual_call_normalizes_counts_and_fraction',(j95['fully_completed_count'],j95['published_count'],j95['last_completed_PR'],j95['fully_completed_fraction_percent'],j95['workflow_estimate_percent'])==(38,22,184,38.38,38.38))
check('phase95_current_pending_original_head_merge',j95['current_PR']==190 and j95['current_original_PR_merged'] is False and j95['advance_to_next_PR_authorized_now'] is False and j95['current_original_budget']=='unknown/5 (interrupted)' and j95['next_numeric_intake_cursor']==191)
check('retired_aliases_removed_and_preserved',all(k not in j95 and j95['retired_stale_live_aliases_20261015']['values'][k]==base[k] for k in retired))
check('historical_records_unchanged_at95',j95['historical_completed_case_records']==old_history)
check('phase95_correct_receipt_intake_and_authority',j95['last_completed_actual_final_receipt']=='audits/pr184_10300044/ROOT_FINAL_FACTUAL_ACCEPTANCE.json' and j95['active_checkpoint_acceptance_receipt']=='audits/pr190_5000007/ROOT_ACTUAL_MERGE_ACCEPTANCE.json' and j95['last_actual_intake_checkpoint_commit']=='4c81b9a4eb4308842311e2658db41d9a961ab0d5' and j95['last_actual_intake_checkpoint_release']=='audits/pr190_5000007/INTAKE_CHECKPOINT_ACCEPTANCE.json' and j95['latest_ordered_intake_record']=='status_intakes_after_pr184/PR190_ORIGINAL_STATUS_INTAKE.json' and 'PR190' in j95['remaining_current_step'] and 'PR179' not in j95['remaining_current_step'] and '191' in j95['next_step'])
check('no_exclusive_window_or_self_commit_invented',j95['peer_pause_or_exclusive_writer_window_assumed'] is False and j95['next_intake_requires_explicit_writer_release'] is False and j95['next_intake_requires_actual_completion_receipt'] is True)
for phase,wrong in [(95,{**j95,'fully_completed_count':39}),(100,j95),(95,{**j95,'current_PR':191})]:
    try:normalize(copy.deepcopy(wrong),phase)
    except RuntimeError:results['checks'].append({'name':'alias_wrong_phase_or_census_rejected_'+str(len(results['checks'])),'passed':True})
    else:raise RuntimeError('Alias guard accepted wrong phase/census')

warm=types.SimpleNamespace(warm_selected_directories=lambda *a:None)
prior=types.SimpleNamespace(m=types.SimpleNamespace(h=warm))
core=[NATIVE+n for n in ['PROOF_V2.md','check_certificate.py','independent_review/reviewer_exact_check.py','source_record.json','prior_imported_report.json','check_half_turn.py']]
payloads=[CASE+'publication_package_v2/'+n for n in ['dodecahedron_endpoint.tex','zenodo-deposit.json','dodecahedron_endpoint.pdf','verification-package.zip']]
casepath=CASE+'CURRENT_CASE_STATUS.json';progress=PREFIX+'CURRENT_PROGRESS.json'
science=core+payloads
class MockGit:
    def __init__(self,root,mutation=None,factual=False):
        self.root=root;self.writes=[];self.reads=[];self.mutation=mutation
        self.content={n:('AUDIT-MOCK '+n+'\n').encode() for n in science+[CASE+'TRACKER_ACCEPTANCE.json']}
        self.content[progress]=(json.dumps(j95,indent=2)+'\n').encode()
        self.content[casepath]=(json.dumps({'PR':190,'whole_package_reviews_complete':True,'case_percent':95,'completed':38,'published':22},indent=2)+'\n').encode()
        self.selected={n:bpin(b) for n,b in self.content.items()}
        self.maps={'merge-tree':{n:('100644','blob',x['git_blob']) for n,x in self.selected.items()}}
        self.maps['actual-tree']=dict(self.maps['merge-tree']);self.maps['actual-tree']['foreign/unrelated.txt']=('100644','blob','b'*40)
        self.current_content=dict(self.content)
        self.commits={'merge-commit':{'tree':{'sha':'merge-tree'},'parents':[{'sha':'old-main'},{'sha':HEAD}]},'actual-main':{'tree':{'sha':'actual-tree'},'parents':[{'sha':'merge-commit'}]}}
        self.record={'commit':'merge-commit','tree':'merge-tree','expected_main':'old-main','parent_tree':'old-tree','selected_files':self.selected,'changed_paths':list(self.selected),'DOI':z['doi'],'tracker_range':tr['range']}
        save(root/'SCOPED_MERGE_PREPARATION.json',self.record)
        if mutation:
            name,kind=mutation
            if kind=='mode':self.maps['actual-tree'][name]=('100755','blob',self.selected[name]['git_blob'])
            elif kind=='delete':self.maps['actual-tree'].pop(name)
            else:
                self.current_content[name]=b'UNEXPECTED SCIENTIFIC CHANGE\n'
                if kind!='body_only':self.maps['actual-tree'][name]=('100644','blob',bpin(self.current_content[name])['git_blob'])
    def api(self,path,method=None,body=None):
        if method=='POST':
            self.writes.append(path)
            if path=='git/trees':
                table=dict(self.maps['actual-tree'])
                for entry in body['tree']:
                    table[entry['path']]=('100644','blob',bpin(entry['content'].encode())['git_blob'])
                self.maps['new-factual-tree']=table;return {'sha':'new-factual-tree'}
            if path=='git/commits':
                self.commits['new-factual-commit']={'tree':{'sha':body['tree']},'parents':[{'sha':x} for x in body['parents']]};return {'sha':'new-factual-commit'}
            raise RuntimeError('Unexpected mocked POST '+path)
        if path=='git/ref/heads/main':return {'object':{'sha':'actual-main'}}
        if path.startswith('git/commits/'):return self.commits[path.removeprefix('git/commits/')]
        if path.startswith('compare/'):return {'status':'ahead'}
        if path=='pulls/190':return {'merged':True,'state':'closed','head':{'sha':HEAD},'merge_commit_sha':'merge-commit'}
        raise RuntimeError('Unexpected mocked GET '+path)
    def lookup(self,t,n):return self.maps.get(t,{}).get(n)
    def changed(self,a,b):
        if a=='old-tree':return set(self.record['changed_paths'])
        before=self.maps[a];after=self.maps[b]
        return {n for n in set(before)|set(after) if before.get(n)!=after.get(n)}
    def body_at(self,n,ref):self.reads.append(n);return self.current_content[n]
    def merge_env(self):
        env={'A':self.root,'json':json,'hashlib':hashlib,'require':require,'api':self.api,'m':prior,'lookup':self.lookup,'changed_leaves':self.changed,'body_at':self.body_at,'gates':lambda:(g,z,tr),'save':save,'now':lambda:'AUDIT-MOCK','HEAD':HEAD,'NATIVE':NATIVE,'CASE':CASE}
        extract('prepare_final_scoped_merge.py','require_selected_at_main',env)
        return env
    def factual_module(self):
        env=self.merge_env()
        return types.SimpleNamespace(HEAD=HEAD,PREFIX=PREFIX,CASE=CASE,pin=pin,m=prior,gates=lambda:(g,z,tr),alias_module=types.SimpleNamespace(normalize=normalize),require_selected_at_main=env['require_selected_at_main'])
    def factual_env(self):return {'A':self.root,'json':json,'hashlib':hashlib,'re':re,'m':self.factual_module(),'api':self.api,'require':require,'save':save,'lookup':self.lookup,'changed_leaves':self.changed,'body_at':self.body_at,'now':lambda:'AUDIT-MOCK'}

def expect_reject(name,action,error_piece,root,acceptance_name=None):
    try:
        with redirect_stdout(io.StringIO()):action()
    except RuntimeError as error:
        check(name,error_piece in str(error),str(error))
        if acceptance_name:require(not (root/acceptance_name).exists(),'Rejected path wrote acceptance')
    else:raise RuntimeError('Expected rejection: '+name)

# Run the exact repaired merge accept(), including its actual new guard function.
for mutation in [None,(NATIVE+'check_half_turn.py','blob'),(payloads[2],'blob'),(payloads[3],'blob'),(core[0],'mode'),(core[0],'delete'),(payloads[2],'body_only'),(payloads[3],'body_only')]:
    with tempfile.TemporaryDirectory(prefix='merge_',dir=D) as temp:
        F=Path(temp);git=MockGit(F,mutation);env=git.merge_env();accept=extract('prepare_final_scoped_merge.py','accept',env)
        if mutation:
            name,kind=mutation
            expect_reject('merge_rejects_'+name.rsplit('/',1)[1]+'_'+kind,accept,'Fresh native body drift' if kind=='body_only' else 'Selected current MAIN identity drift',F,'ROOT_ACTUAL_MERGE_ACCEPTANCE.json')
        else:
            with redirect_stdout(io.StringIO()):accept()
            receipt=json.loads((F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').read_text())
            check('merge_accepts_unrelated_foreign_descendant',receipt['every_selected_identity_checked_at_actual_observed_MAIN'] is True)
            check('merge_directly_reads_pdf_and_zip',all(n in git.reads for n in payloads[2:]))

# Exact factual prepare: reject changed merged selections before postimage/API writes;
# run a clean complete fixture to test all case/census/normalization outputs.
for mutation in [None,(NATIVE+'check_half_turn.py','blob'),(payloads[2],'blob'),(payloads[3],'blob')]:
    with tempfile.TemporaryDirectory(prefix='factual_prepare_',dir=D) as temp:
        F=Path(temp);(F/'integration_preparation').mkdir();git=MockGit(F,mutation)
        save(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',{'PR_merged':True,'actual_native_scientific_and_metadata_bytes_accepted':True,'merge_commit':'merge-commit'})
        (F/'CURRENT_CASE_STATUS.json').write_bytes(git.content[casepath]);(F/'RESEARCH_LOG.md').write_text('AUDIT-MOCK LOG\n')
        shutil.copyfile(A/'prepare_factual_completion.py',F/'prepare_factual_completion.py')
        allowed=[CASE+n for n in ['SCOPED_MERGE_PREPARATION.json','ROOT_ACTUAL_MERGE_ACCEPTANCE.json','WORKFLOW_COMPLETION.json','CURRENT_CASE_STATUS.json','RESEARCH_LOG.md','prepare_factual_completion.py']]+[PREFIX+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']]
        save(F/'FINAL_MAIN_SCOPE.json',{'selected_MAIN_paths':allowed,'factual_receipt_additional_allowed_paths':[]})
        git.current_content[PREFIX+'CURRENT_PROGRESS.md']=b'AUDIT-MOCK PROGRESS\n';git.current_content[PREFIX+'RESEARCH_LOG.md']=b'AUDIT-MOCK PROGRAMME LOG\n'
        action=lambda:extract('prepare_factual_completion.py','prepare',git.factual_env())('factual_preparation_mock')
        if mutation:
            expect_reject('factual_prepare_rejects_'+mutation[0].rsplit('/',1)[1],action,'Selected current MAIN identity drift',F)
            check('factual_prepare_rejection_precedes_writes_'+mutation[0].rsplit('/',1)[1],not git.writes and not (F/'WORKFLOW_COMPLETION.json').exists())
        else:
            with redirect_stdout(io.StringIO()):action()
            j100=json.loads((F/'integration_preparation/factual_preparation_mock/CURRENT_PROGRESS.json').read_text());case100=json.loads((F/'CURRENT_CASE_STATUS.json').read_text())
            check('factual100_actual_prepare_counts_fraction_and_unique_arrays',(j100['fully_completed_count'],j100['published_count'],j100['last_completed_PR'],j100['fully_completed_fraction_percent'])==(39,23,190,39.39) and len(set(j100['fully_completed_eligible_PRs']))==39 and len(set(j100['published_PRs']))==23)
            check('factual100_live_aliases_and_history',j100['last_completed_actual_final_receipt']=='audits/pr190_5000007/ROOT_FINAL_FACTUAL_ACCEPTANCE.json' and j100['active_checkpoint_acceptance_receipt']==j100['last_completed_actual_final_receipt'] and all(k not in j100 for k in retired) and j100['historical_completed_case_records']==old_history and j100['retired_stale_live_aliases_20261015']==j95['retired_stale_live_aliases_20261015'])
            check('factual100_complete_case_and_conditional_intake',case100['whole_package_reviews_complete'] is True and case100['whole_package_review02_disposition']=='PASS' and case100['original_PR_merged'] is True and case100['case_completion_requires_actual_factual_postimage_acceptance'] is True and j100['advance_to_next_PR_authorized_now'] is True and j100['next_intake_requires_actual_completion_receipt'] is True and 'effective only after that acceptance' in j100['program_snapshot_authority_condition'] and j100['next_numeric_intake_cursor']==191 and j100['persistent_goal_complete'] is False)
            results['phase_alias_outputs']={str(phase):{k:j[k] for k in ['fully_completed_count','published_count','last_completed_PR','fully_completed_fraction_percent','last_completed_actual_final_receipt','active_checkpoint_acceptance_receipt','last_actual_intake_checkpoint_commit','latest_ordered_intake_record','remaining_current_step','next_step','program_snapshot_authority_condition']} for phase,j in [(95,j95),(100,j100)]}

# Exact factual acceptance with intended factual overrides plus foreign changes.
for mutation in [None,(NATIVE+'check_half_turn.py','blob'),(payloads[2],'blob'),(payloads[3],'blob')]:
    with tempfile.TemporaryDirectory(prefix='factual_accept_',dir=D) as temp:
        F=Path(temp);git=MockGit(F,mutation)
        changed_bodies={casepath:b'AUDIT-MOCK FACTUAL CASE100\n',progress:b'AUDIT-MOCK FACTUAL COUNTS39/23\n'}
        factual_pins={n:bpin(b) for n,b in changed_bodies.items()}
        git.maps['factual-tree']=dict(git.maps['merge-tree'])
        for n,x in factual_pins.items():
            value=('100644','blob',x['git_blob']);git.maps['factual-tree'][n]=value;git.maps['actual-tree'][n]=value;git.current_content[n]=changed_bodies[n]
        git.commits['factual-commit']={'tree':{'sha':'factual-tree'},'parents':[{'sha':'merge-commit'}]}
        r={'commit':'factual-commit','tree':'factual-tree','expected_main':'merge-commit','parent_tree':'merge-tree','selected_files':factual_pins,'changed_paths':list(factual_pins)}
        save(F/'FINAL_FACTUAL_PREPARATION.json',r)
        accept=extract('prepare_factual_completion.py','accept',git.factual_env())
        if mutation:expect_reject('factual_accept_rejects_'+mutation[0].rsplit('/',1)[1],accept,'Selected current MAIN identity drift',F,'ROOT_FINAL_FACTUAL_ACCEPTANCE.json')
        else:
            with redirect_stdout(io.StringIO()):accept()
            receipt=json.loads((F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').read_text())
            check('factual_accept_permits_intentional_overrides_and_foreign_changes',receipt['every_selected_identity_checked_at_actual_observed_MAIN'] and receipt['combined_expected_current_identities_checked']==len(git.selected))

# Actual native propagator in disposable local copy, with actual reviewed packet
# hashes but synthetic publication/tracker receipts. No external process runs.
cur=json.loads((A/'integration_preparation/CURRENT_TEMPLATE.json').read_text());native=A/'integration_preparation'/cur['current_template']
check('native_predecessor_still_pending02',cur['current_template']=='native_template_pending_02')
actual_gate=json.loads((A/'ROOT_PUBLICATION_GATE.json').read_text());packet=A/actual_gate['package_name']
packet_before={n:plainpin(packet/n) for n in actual_gate['payloads']}
with tempfile.TemporaryDirectory(prefix='native_',dir=D) as temp:
    F=Path(temp);(F/'integration_preparation').mkdir();shutil.copytree(native,F/'integration_preparation'/native.name)
    save(F/'integration_preparation/CURRENT_TEMPLATE.json',cur);shutil.copyfile(A/'ORIGINAL_FILE_MANIFEST.json',F/'ORIGINAL_FILE_MANIFEST.json')
    fixture_gate={**actual_gate,'package_name':str(packet)};save(F/'ROOT_PUBLICATION_GATE.json',fixture_gate)
    save(F/'ZENODO_PUBLICATION_READBACK.json',z);save(F/'TRACKER_ACCEPTANCE.json',tr)
    shutil.copyfile(A/'CURRENT_CASE_STATUS.json',F/'CURRENT_CASE_STATUS.json');(F/'RESEARCH_LOG.md').write_text('AUDIT-MOCK ROOT LOG\n')
    with redirect_stdout(io.StringIO()):exec(compile((A/'prepare_native_final_01.py').read_text(),str(A/'prepare_native_final_01.py'),'exec'),{'__file__':str(F/'prepare_native_final_01.py'),'__name__':'fixture_only'})
    final=F/'integration_preparation/native_template_final_01';newcur=json.loads((F/'integration_preparation/CURRENT_TEMPLATE.json').read_text());case95=json.loads((F/'CURRENT_CASE_STATUS.json').read_text())
    changes=[n for n,x in cur['files'].items() if plainpin(final/n)!=x]
    check('native_factual_only_changes',set(changes)=={'CANDIDATE_PROOF.md','PUBLICATION_RECEIPT.md','README.md','RESEARCH_LOG.md','independent_review/FINAL_REVIEW.md','independent_review/reviewed_hashes.json','recovery_manifest.json','source_interpretation.json'})
    original=json.loads((F/'ORIGINAL_FILE_MANIFEST.json').read_text())
    check('native_all22_originals_preserved',len(original['files'])==22 and all(plainpin(final/'historical_original'/Path(x['path']).relative_to('unsolved_math_prioritization/attempts/5000007'))=={'bytes':x['bytes'],'sha256':x['sha256']} for x in original['files']))
    check('native_scientific_files_and_packet_unchanged',all(plainpin(final/n)==x for n,x in cur['files'].items() if n not in changes) and all(plainpin(packet/n)==x for n,x in packet_before.items()))
    check('native_root_case95_truthful_publication_tracker_pending_merge',case95['case_percent']==95 and case95['whole_package_reviews_complete'] is True and case95['whole_package_review02_disposition']=='PASS' and case95['Zenodo_published'] is True and case95['tracker_updated'] is True and case95['DOI']==z['doi'] and case95['tracker_range']==tr['range'] and case95['original_PR_merged'] is False and case95['PR_closed'] is False and case95['completed']==38 and case95['published']==22)
    check('native_root_log_records_pending_scope','38completed/22published unchanged' in (F/'RESEARCH_LOG.md').read_text() and 'Original-head MAIN integration/factual acceptance pending' in (F/'RESEARCH_LOG.md').read_text())
    results['native_fixture']={'changed_existing':changes,'unchanged_existing':len(cur['files'])-len(changes),'historical_original_files':22,'new_files':sorted(set(newcur['files'])-set(cur['files']))}

# Run only the exact module prefix through each early canonical protection guard.
# Prefix ends at the guard, before imports of helpers or any mkdir/read/write/API.
for script,outputs in [('prepare_publication_lifecycle_scripts_02.py',['prepare_final_scoped_merge.py','prepare_factual_completion.py']),('prepare_lifecycle_utilities_20261015.py',['record_tracker.py'])]:
    tree=ast.parse((A/script).read_text());guard=next(n for n in tree.body if isinstance(n,ast.If) and any(isinstance(x,ast.Raise) for x in ast.walk(n)))
    prefix=ast.Module(body=[n for n in tree.body if n.lineno<=guard.lineno],type_ignores=[])
    for existing in outputs:
        with tempfile.TemporaryDirectory(prefix='generator_',dir=D) as temp:
            F=Path(temp);(F/existing).write_text('CANONICAL SENTINEL\n');before={p.name:pin(p) for p in F.iterdir()}
            try:exec(compile(ast.fix_missing_locations(prefix),str(A/script),'exec'),{'__file__':str(F/script)})
            except RuntimeError as error:check('generator_refuses_before_write_'+existing,'Historical generator retired' in str(error) and {p.name:pin(p) for p in F.iterdir()}==before)
            else:raise RuntimeError('Generator did not refuse existing '+existing)

check('target_code_and_packet_unchanged_after_checks',all(plainpin(A/n)==x for n,x in results['script_pins'].items()) and all(plainpin(packet/n)==x for n,x in packet_before.items()))
results['verdict']='PASS_TARGETED_REPAIRS';results['targeted_audit_percent']=100
save(D/'RECHECK_RESULTS.json',results)
print(json.dumps({'verdict':results['verdict'],'checks_passed':len(results['checks']),'remote_calls':0,'production_imports':0}))
