"""Read-only authentication of frozen choices plus pure guard/consumer/capacity tests."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import copy,datetime,hashlib,importlib.util,json,os,shutil,stat
D=Path(__file__).resolve().parent;A=D.parent;C=A.parents[2]
S=A/'native_publication_integration_plan_20261006/corrected_v4';B=A/'native_actual_input_preparation_20261006';Q=B/'draft_0dd29832e98382f5'
sys.path.insert(0,str(S))
import v3_guards as g
import prepare_review_bundle as helper
# Imports execute no entry point or resource-setup function.
M=S/'EXECUTION_INPUTS_FROZEN_20261006.json';mbytes=M.read_bytes();m=g.loads(mbytes);cfg=m['effective']
checks=[];pins=[];metadata=[]
def need(ok,message):
    if not ok:raise ValueError(message)
def checked(name,fn):
    fn();checks.append(name)
def rejection(name,fn):
    try:fn()
    except (ValueError,KeyError,TypeError):checks.append(name);return
    raise RuntimeError('Accepted challenge: '+name)
def streamed(path,private=False):
    before=g.regular(path);digest=hashlib.sha256();count=0
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):digest.update(block);count+=len(block)
    after=g.regular(path);need((before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns) and count==before.st_size,'metadata changed during hash')
    return {'path':str(path),'bytes':count,'sha256':digest.hexdigest(),'mode':format(stat.S_IMODE(after.st_mode),'04o'),'UID':after.st_uid,'private_opaque_hash_only':private,'body_retained_or_disclosed':False}
def pincheck(pin,absolute=False,private=False):
    path=Path(pin['path']) if absolute else C/g.relative(pin['path']);actual=streamed(path,private)
    need(actual['bytes']==pin['bytes'] and actual['sha256']==pin['sha256'],'exact pin mismatch: '+str(path));metadata.append(actual);return path
need(len(mbytes)==69303 and g.sha(mbytes)=='0dd29832e98382f5d73ddbc93b139e23d9f11d8cc2f60d53fe4050ce01b709bf' and stat.S_IMODE(M.stat().st_mode)==0o444,'final readonly frozen pin')
g.validate_execution_manifest(m,mbytes);g.validate_environment_policy(cfg['environment_policy']);helper.validate_process_policy(cfg['process_policy']);helper.validate_worker_policy(cfg['worker_policy'])
checked('exact canonical final manifest/environment/resource policies',lambda:need(cfg['main_parent']=='f36cb1e34696d460b9cfb5b03425998de48c4669','main parent'))
provisional=g.loads((B/'draft_0a8a86fd02ff1f8e/EXECUTION_INPUTS_DRAFT.json').read_bytes());p=copy.deepcopy(provisional);p['effective']['main_parent']=cfg['main_parent']
checked('only main parent differs from original authenticated provisional',lambda:need(g.canonical(p)==mbytes and g.canonical(m)==(Q/'EXECUTION_INPUTS_DRAFT.json').read_bytes(),'provisional/final drift'))
# All existing sealed bytes are preserved; a known future frozen data file is outside original94 inventory.
original=json.loads((S/'OUTPUT_MANIFEST.json').read_bytes());source_review=A/'native_v4_fresh_source_adversary_20261006';review_manifest=json.loads((source_review/'OUTPUT_MANIFEST.json').read_bytes());builder_manifest=json.loads((B/'OUTPUT_MANIFEST.json').read_bytes())
for root,manifest in [(S,original),(source_review,review_manifest),(B,builder_manifest)]:
    for pin in manifest['files']:
        path=root/pin['relative_path'];actual=streamed(path)
        need(actual['bytes']==pin['bytes'] and actual['sha256']==pin['sha256'],'sealed predecessor mutation')
    for name in ['OUTPUT_MANIFEST.json','SEAL_RECEIPT.json']:metadata.append(streamed(root/name))
checked('original V4 payload92/source-review payload23/builder payload15 preserved',lambda:need(original['file_count']==92 and review_manifest['file_count']==23 and len(builder_manifest['files'])==15,'sealed counts'))
for pin in m['program_files']:pincheck(pin)
family={Path(p['path']).name:{k:p[k] for k in ['bytes','sha256']} for p in m['program_files']}
checked('exact source-reviewed five-program family',lambda:need(g.sha(g.canonical(family))=='e57b078c27b6ea42080bc74d2bd91c3252a408f8a468de46ccb607c37a64c2e2','code family'))
for pin in m['input_files']:pincheck(pin)
checked('entire180 declared actual input inventory',lambda:need(len(m['input_files'])==180 and sum(p['bytes'] for p in m['input_files'])==1846309,'registry totals'))
packet=json.loads((Q/'PACKET_MANIFEST.json').read_bytes())
for pin in packet['files']:
    actual=streamed(Q/pin['relative_path']);need(actual['bytes']==pin['bytes'] and actual['sha256']==pin['sha256'],'final packet pin')
metadata.append(streamed(Q/'PACKET_MANIFEST.json'));metadata.append(streamed(M));metadata.append(streamed(A/'ROOT_FINAL_NATIVE_EXECUTION_INPUT_FREEZE_20261006.json'))
# Private files are never decoded, parsed, copied, inspected or printed.
env=cfg['environment_policy'];privates=env['git']['repository_location_pins']+env['git']['repository_config_pins']+env['gh']['config_pins']
need((C/'.git').is_dir() and not (C/'.git').is_symlink() and env['git']['repository_location_pins']==[] and not (C/'.git/commondir').exists() and not (C/'.git/config.worktree').exists(),'Git location configuration changed')
need({p['path'] for p in env['git']['repository_config_pins']}=={str(C/'.git/config')},'Git exact config inventory')
for pin in privates:
    path=pincheck(pin,True,True)
    if path.parent==Path(env['gh']['environment']['GH_CONFIG_DIR']):need(stat.S_IMODE(path.stat().st_mode)==0o600 and path.stat().st_uid==os.getuid(),'GH opaque mode/UID')
need({str(p) for p in Path(env['gh']['environment']['GH_CONFIG_DIR']).iterdir() if p.is_file()}=={p['path'] for p in env['gh']['config_pins']},'GH file inventory')
checked('private opaque config pins and locations without body inspection',lambda:need(not {p['path'] for p in privates}&{str(C/p['path']) for p in m['input_files']},'private body in registry'))
for role in ['python','git','gh']:
    path=Path(cfg['runtime'][role+'_executable']);actual=streamed(path);need({k:actual[k] for k in ['bytes','sha256']}==cfg['runtime'][role+'_binary'],'runtime binary pin');metadata.append(actual)
checked('current Python path/full version',lambda:need(str(Path(sys.executable).resolve())==cfg['runtime']['python_executable'] and sys.version==cfg['runtime']['python_version'],'Python runtime drift'))
readmeta=json.loads((Q/'READ_SCOPE_AND_RUNTIME_METADATA.json').read_bytes());shell=readmeta['runtime_shell_pin'];pincheck(shell,True)
for pin in cfg['native_baseline_pins']:pincheck(pin)
native_manifest=(C/'unsolved_math_prioritization/manifest.json').read_bytes();nm=g.loads(native_manifest)
sourcepair=g.loads((C/cfg['original_authentication_pins']['sourcepair']['path']).read_bytes());source_meta={p['path']:{k:p[k] for k in ['bytes','sha256']} for p in sourcepair['input_pins']}
for name,pin in cfg['raw_source_pins'].items():
    path=Path('/Users/alec/Documents/Math/unsolved_math_prioritization/cache')/name
    need(source_meta[str(path)]==pin and nm['files'][name]==pin,'raw/native/sourcepair correspondence');actual=streamed(path);need({k:actual[k] for k in ['bytes','sha256']}==pin,'raw opaque metadata drift');metadata.append(actual)
sql=Path('/Users/alec/Documents/Math/unsolved_math_prioritization/cache/catalog.sqlite');need(source_meta[str(sql)]==cfg['source_cache_pin'],'SQL original metadata correspondence');actual=streamed(sql);need({k:actual[k] for k in ['bytes','sha256']}==cfg['source_cache_pin'],'SQL opaque metadata drift');metadata.append(actual)
checked('immutable source/revision and absent SQL sidecars',lambda:need(nm['revision']==g.WORKER_DATASET_REVISION and not any(Path(str(sql)+s).exists() for s in ['-wal','-shm','-journal']),'source/sidecar'))
# Purely follow the exact helper direct-consumer and future-declared-gate registry routes.
reviewed=g.ReviewedInputs(m,C,A);read=reviewed.read;gate_usage=g.loads((Q/'PROPOSED_GATE_CHECKED_ARTIFACT_USAGE.json').read_bytes());expected_usage={}
def use(pin,label,root=None):
    path,body=read(pin,root);expected_usage.setdefault(pin['path'],set()).add(label);return path,body
package_root=C/cfg['package']['root'];_,package_bytes=use(cfg['package']['manifest'],'prepare:package_manifest');package=g.loads(package_bytes);package_files={}
for entry in package['files']:
    pin={'path':str((package_root/entry['relative_path']).relative_to(C)),'bytes':entry['bytes'],'sha256':entry['sha256']}
    _,body=use(pin,'prepare:logical_package_file',package_root);package_files[entry['relative_path']]=body
for role,pins in gate_usage.items():
    need(role in g.GATE_ROLES and pins,'declared future gate coverage')
    for pin in pins:use(pin,'gate_checked_artifact:'+role)
_,pubbytes=use(cfg['publication']['receipt'],'prepare:actual_publication_receipt');pub=g.loads(pubbytes)
use(pub['metadata_response'],'publication_check:metadata')
for item in pub['payload_readbacks']:
    use(item['downloaded_file'],'publication_check:logical_payload');use(item['HTTP_GET_receipt'],'publication_check:HTTP_custody')
    if item['transport']=='zip_member':use(item['archive_file'],'publication_check:archive')
actual_pub,doi=helper.publication_check(cfg,package_files,package_bytes,read)
_,sheetbytes=use(cfg['google_sheet']['receipt'],'prepare:actual_Sheet_receipt');sheet=g.loads(sheetbytes)
for role,rec in sheet['processes'].items():
    for field in ['stdout_pin','stderr_pin']:use(rec[field],'validate_sheet:'+role+':'+field)
    if role=='write':use(rec['request_body_pin'],'validate_sheet:append_body')
expected={'DOI':doi,'row_index':cfg['google_sheet']['row_index'],'values':cfg['google_sheet']['values'],'existing_chat_authorized':cfg['google_sheet']['existing_chat_authorized']}
sheet_checked=g.validate_sheet(sheet,expected,pub['UTC_end'],read)
original={}
for role,pin in cfg['original_authentication_pins'].items():
    if role!='original_files':original[role]=use(pin,'prepare:original_authentication:'+role)[1]
original_files={}
for pin in cfg['original_authentication_pins']['original_files']:
    path,body=use(pin,'prepare:original_file',A/'original_source_authentication_20261006/original_attempt');original_files[str(path.relative_to(A/'original_source_authentication_20261006/original_attempt'))]=body
for pin in cfg['effective_diagnostics_pins']:use(pin,'prepare:effective_diagnostics',A/'repaired_diagnostics_v1')
reviewed.finish()
usage=g.loads((Q/'EXACT_INPUT_USAGE.json').read_bytes())
checked('independently reconstructed exact direct/gate-only consumer map180 with no unused',lambda:need({p:sorted(c) for p,c in expected_usage.items()}==usage and set(usage)==set(reviewed.pins),'usage map mismatch'))
checked('unchanged46 logical package and actual31 blank B receipt contracts',lambda:need(len(package_files)==46 and g.sha(package_bytes)=='61f08bd60185b6ef2382fb279fe77d59958974c07c4a44976cc7289eafca8c38' and doi=='10.5281/zenodo.23181280' and sheet_checked['row_index']==31 and cfg['google_sheet']['values'][1]=='' and cfg['google_sheet']['existing_chat_authorized'] is False,'package/target Sheet drift'))
blob=g.loads(original['blob_manifest']);queue_auth=g.loads(original['queue_projection']);src=g.loads(original['sourcepair']);prior=original['selected_prior']
checked('original15/status2of5/empty prior/source-pair absence preserved',lambda:need(len(blob['files'])==15 and set(original_files)==g.ORIGINAL_NAMES and blob['literal_status']=='claimed_solved' and blob['original_author_effort']=='2/5' and queue_auth['literal_status']=='claimed_solved' and queue_auth['original_budget']=='2/5' and prior==b'{}\n' and src['submitted_source_equals_raw_and_SQL'] is True and src['submitted_prior_equals_raw_and_SQL'] is False,'historical provenance'))
checked('Sheet source URL and effective proof binding',lambda:need(g.loads(original_files['source_record.json'])['source_url']==cfg['google_sheet']['values'][0] and g.sha((A/'repaired_diagnostics_v1/PROOF.md').read_bytes())==helper.PROOF,'source/proof'))
oldass=g.loads((C/'unsolved_math_prioritization/assessments.json').read_bytes())[g.K];catalog=g.loads((C/'unsolved_math_prioritization/catalog.json').read_bytes());target=next(r for r in catalog if r['id']==g.K);state=g.loads((C/'unsolved_math_prioritization/state.json').read_bytes())
checked('exact historical desk assessment and target native baseline',lambda:need(g.canonical(oldass)==g.canonical(cfg['assessment']) and target['local_status']=='queued' and target['turns_used']==0 and g.K not in state and target['review_hash']==helper.REVIEW and target['statement_hash']==helper.STATEMENT,'native target baseline'))
del catalog,state,oldass
# Independent complete allocation formula: direct base/duplicate global + all exact copies/wrappers/metadata/streams/gates/package + one maximum atomic slot.
copies=[(g.N+'publication/authenticated_inputs/'+str((C/p).relative_to(A)),len(b)) for p,b in reviewed.captured.items()]
copies += [(g.N+'historical_original/'+n,len(b)) for n,b in original_files.items()]
copies += [(g.N+('EFFECTIVE_DIAGNOSTICS_README.md' if Path(p['path']).name=='README.md' else str((C/p['path']).relative_to(A/'repaired_diagnostics_v1'))),p['bytes']) for p in cfg['effective_diagnostics_pins']]
copies += [(g.N+'source_record.json',len(original_files['source_record.json'])),(g.N+'prior_imported_report.json',len(prior)),(g.N+'publication/EXECUTION_INPUTS.json',len(mbytes))]
capacity=g.capacity_inventory(cfg['native_baseline_pins'],[('bundle/'+p,n) for p,n in copies],{r:{'bytes':65536} for r in g.GATE_ROLES},package_files,cfg['capacity_policy'],cfg['process_policy'])
actual_cap=g.loads((Q/'CAPACITY_PLAN_WITH_RESERVED_GATES.json').read_bytes());checked('entire allocation exact against reviewed helper',lambda:need(all(actual_cap[k]==v for k,v in capacity.items()),'capacity packet mismatch'))
base_sum=sum(p['bytes']+(524288 if Path(p['path']).name in g.WORKER_MUTABLE_NAMES else 0) for p in cfg['native_baseline_pins']);globals_sum=sum(p['bytes']+524288 for p in cfg['native_baseline_pins'] if Path(p['path']).name in g.WORKER_MUTABLE_NAMES)
atomic=max(p['bytes']+524288 for p in cfg['native_baseline_pins'] if Path(p['path']).name in ['catalog.json','assessments.json','state.json','summary.json'])
oracle_total=base_sum+globals_sum+sum(n for _,n in copies)+7*65536+sum(len(b) for b in package_files.values())+9*131072+7*65536+128*4096+atomic
oracle_count=12+9+len(copies)+7+len(package_files)+9+7+128+1
checked('independent capacity arithmetic and distinct destinations',lambda:need(oracle_total==capacity['max_materialized_bytes']==135358232 and oracle_count==capacity['file_count_cap']==427 and len(capacity['entries'])==len({x['path'] for x in capacity['entries']})==426 and capacity['required_free_bytes']==194078488==oracle_total+56*1024*1024,'independent capacity oracle'))
privacy=g.loads((Q/'PRIVATE_EXPORT_EXCLUSIONS.json').read_bytes());expect_private=[sheet['processes']['metadata']['stdout_pin'],next(pin for pin in gate_usage['final'] if pin['path'].endswith('/tracker_postpub_DOI_dedup/stdout.bin'))]
checked('two exact public-export body exclusions',lambda:need([x['input_pin'] for x in privacy['exclusions']]==expect_private and all(x['candidate_affected_path']==g.N+'publication/authenticated_inputs/'+str((C/x['input_pin']['path']).relative_to(A)) for x in privacy['exclusions']) and privacy['private_runtime_configuration']==privates,'private export mismatch'))
# Pure returned derivation uses real frozen choices and byte-pinned native manifest but creates no WORKER_CONTROL file.
control=g.derive_worker_control(m,mbytes,S/('candidate_'+g.sha(mbytes)[:16]),native_manifest)
checked('actual frozen worker caps correspond complete capacity',lambda:need(control['backend_file_caps']=={Path(e['path']).name:e['max_bytes'] for e in capacity['entries'] if e['path'].startswith('private_native_backend/')},'derived caps'))
# Fresh report is later separate evidence: input->review->pre_execution/final; final->six antecedents, no path back into input.
nodes={'manifest':set(),'review':{'manifest'},'root_auth':{'review'},'pre_execution':{'manifest','review','root_auth'},'final':{'manifest','review','root_auth','pre_execution','mathematics','priority','package','R1','R2'},'mathematics':{'manifest'},'priority':{'manifest'},'package':{'manifest'},'R1':{'manifest'},'R2':{'manifest'}}
visiting=set();done=set()
def visit(n):
    need(n not in visiting,'evidence cycle')
    if n in done:return
    visiting.add(n)
    for dep in nodes[n]:visit(dep)
    visiting.remove(n);done.add(n)
for n in nodes:visit(n)
checked('separate pinned review evidence has no manifest/report cycle',lambda:need(not any('native_actual_configuration_adversary_20261006' in p['path'] for p in m['input_files']) and set(gate_usage)==set(g.GATE_ROLES),'future evidence cycle/role coverage'))
# Check exact future gate contract by synthetic in-memory dictionaries, never write or issue a gate.
programs={Path(p['path']).name:p['sha256'] for p in m['program_files']}
def synthetic_gate(role):
    x={'schema':'pr108-publication-root-gate/v3','role':role,'PR':108,'problem_id':30003996,'main_parent':cfg['main_parent'],'original_head':helper.HEAD,'review_hash':helper.REVIEW,'statement_hash':helper.STATEMENT,'effective_proof_sha256':helper.PROOF,'package_manifest_sha256':g.sha(package_bytes),'execution_inputs_sha256':g.sha(mbytes),'actual_root_review':True,'clearance':True,'new_central_proof_search_turns':0,'original_budget':'2/5','exact_claim':'Synthetic guard correspondence only; no gate issued.','checked_artifacts':gate_usage[role],'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewed_program_sha256':programs,'scoped_rank_interpretation':cfg['scoped_rank_interpretation']}
    flags={'mathematics':['mathematical_clearance'],'priority':['priority_clearance','bounded_substantive_resolution_note_clearance','attribution_checked','no_concrete_antecedent_in_recorded_search'],'package':['package_clearance','metadata_and_attribution_checked'],'whole_package_R1':['independent_whole_package_review','zero_blocking_findings'],'whole_package_R2':['independent_whole_package_review','zero_blocking_findings'],'pre_execution_adversary':['native_scope_and_invariants_checked'],'final':['mathematical_clearance','priority_clearance','package_clearance','whole_package_R1_clearance','whole_package_R2_clearance','native_integration_clearance','pre_execution_adversary_clearance','actual_Zenodo_service_authenticated','actual_Google_Sheet_service_authenticated']}
    for k in flags[role]:x[k]=True
    return x
for role in g.GATE_ROLES:
    x=synthetic_gate(role);helper.validate_gate(x,role,g.sha(package_bytes),g.sha(mbytes),programs,cfg['main_parent']);checks.append('synthetic exact '+role+' gate guard')
    for key,value in [('execution_inputs_sha256','0'*64),('main_parent','0'*40),('original_head','0'*40),('package_manifest_sha256','0'*64),('review_hash','0'*64),('effective_proof_sha256','0'*64)]:
        bad=copy.deepcopy(x);bad[key]=value;rejection(role+' rejects altered '+key,lambda bad=bad,role=role:helper.validate_gate(bad,role,g.sha(package_bytes),g.sha(mbytes),programs,cfg['main_parent']))
for role in ['pre_execution_adversary','final']:
    x=synthetic_gate(role);x['reviewed_program_sha256']['v3_guards.py']='0'*64
    rejection(role+' rejects different code family',lambda x=x,role=role:helper.validate_gate(x,role,g.sha(package_bytes),g.sha(mbytes),programs,cfg['main_parent']))
for name in ['CONFIG_TEMPLATE_DO_NOT_RUN.json','EXECUTION_INPUTS_TEMPLATE_DO_NOT_RUN.json']:
    t=g.loads((S/name).read_bytes());rejection(name+' remains inert',lambda t=t,name=name:g.validate_thin_config(t) if name.startswith('CONFIG') else g.validate_execution_manifest(t,g.canonical(t)))
# Provenance only; original R1 remains historical non-clean, correction and current R2 retain their meaning.
r1=g.loads((A/'ROOT_WHOLE_PACKAGE_R1_AUTHENTICATION_20261006.json').read_bytes());r2=g.loads((A/'ROOT_WHOLE_PACKAGE_R2_AUTHENTICATION_20261006.json').read_bytes())
checked('historical R1 F01 is preserved with globally repaired V2 and clean R2',lambda:need(r1['required_findings']==['F01'] and r2['required_findings']==[] and r2['R1_F01_globally_repaired_and_freshly_verified'] is True,'R1/R2 provenance'))
free=shutil.disk_usage(S).free
result={'schema':'pr108-fresh-actual-frozen-input-pure-review/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'optimized':not __debug__,'passed':True,'checks':len(checks),'check_names':checks,'execution_inputs_sha256':g.sha(mbytes),'main_parent':cfg['main_parent'],'core_family_sha256':g.sha(g.canonical(family)),'registry_files':len(m['input_files']),'registry_bytes':sum(p['bytes'] for p in m['input_files']),'direct_and_gate_consumer_map_exact':True,'package_logical_files':46,'publication_receipt_compatible':True,'actual_sheet_receipt_compatible':True,'sheet_target':sheet_checked,'private_config_opaque_pins_verified':len(privates),'private_body_inspection':False,'runtime_metadata_pins_verified':True,'shared_raw_SQL_metadata_verified_without_query_or_copy':True,'capacity':{k:v for k,v in capacity.items() if k!='entries'},'current_free_bytes_snapshot':free,'snapshot_capacity_sufficient':free>=capacity['required_free_bytes'],'privacy_exclusions':[x['candidate_affected_path'] for x in privacy['exclusions']],'evidence_dependencies':{k:sorted(v) for k,v in nodes.items()},'worker_control_derived_in_memory_only':True,'worker_control_binding_sha256':g.sha(g.canonical(control)),'private_body_validation_and_actual_clean_GH_probe_remain_root_boundaries':True,'native_prepare_worker_execute_assess_resource_setup_calls':0,'actual_config_gate_files_created':0,'services_Git_mutations_or_source_copies':0}
(D/('OPTIMIZED_PURE_REVIEW_RESULTS.json' if not __debug__ else 'NORMAL_PURE_REVIEW_RESULTS.json')).write_bytes(g.canonical(result))
if __debug__:
    (D/'AUTHENTICATED_INPUT_AND_RUNTIME_PINS.json').write_bytes(g.canonical({'schema':'pr108-actual-config-review-full-metadata-pins/v1','UTC':result['UTC'],'operator_PID':os.getpid(),'frozen_input':{'path':str(M),'bytes':len(mbytes),'sha256':g.sha(mbytes),'mode':'0444'},'registry_pins':m['input_files'],'program_pins':m['program_files'],'streamed_metadata':metadata,'no_private_body_inspection_retention_or_disclosure':True}))
print(json.dumps({k:v for k,v in result.items() if k not in ['check_names','evidence_dependencies','capacity','sheet_target']},sort_keys=True))
