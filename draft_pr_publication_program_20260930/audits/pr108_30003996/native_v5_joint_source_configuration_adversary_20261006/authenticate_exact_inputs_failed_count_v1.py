"""Read-only exact V5 source, actual frozen inputs and actual root process custody.
Never runs Git/services/native/resources or reads private configuration semantically.
"""
from pathlib import Path
import ast,collections,datetime,difflib,hashlib,json,os,shutil,stat,sys
O=Path(__file__).absolute().parent;A=O.parent;C=A.parents[2];D=A/'native_publication_integration_plan_20261006/corrected_v5';V4=D.parent/'corrected_v4';B=A/'native_actual_input_preparation_v2_20261006/draft_dfe3e71993e3bd99'
R=Path('/Users/alec/Documents/Math');reads={};checks=[]
def ck(n,v):
 if not v:raise ValueError(n)
 checks.append(n)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 p=Path(p).absolute();s=p.stat();ck('regular '+str(p),stat.S_ISREG(s.st_mode) and not any(q.is_symlink() for q in [p,*p.parents]));b=p.read_bytes();t=p.stat();ck('stable read '+str(p),(s.st_size,s.st_mtime_ns)==(t.st_size,t.st_mtime_ns));reads[str(p)]={'path':str(p),'bytes':len(b),'sha256':sha(b),'mode':format(stat.S_IMODE(t.st_mode),'04o'),'body_retained':False};return b
def opaque(p,expected):
 p=Path(p).absolute();s=p.stat();ck('opaque regular '+str(p),stat.S_ISREG(s.st_mode) and not any(q.is_symlink() for q in [p,*p.parents]));h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 t=p.stat();pin={'bytes':t.st_size,'sha256':h.hexdigest()};ck('opaque exact stable '+str(p),(s.st_size,s.st_mtime_ns)==(t.st_size,t.st_mtime_ns) and pin=={k:expected[k] for k in ['bytes','sha256']});reads[str(p)]={'path':str(p),**pin,'mode':format(stat.S_IMODE(t.st_mode),'04o'),'body_retained':False,'metadata_only_opaque_digest':True};return pin
def j(p):return json.loads(read(p))
def pin(p,v):b=read(p);ck('exact byte pin '+str(p),len(b)==v['bytes'] and sha(b)==v['sha256']);return b
# Exact sealed source inventory and narrow full regenerated diff.
manifest=j(D/'OUTPUT_MANIFEST.json');ck('known V5 source seal SHA',sha((D/'OUTPUT_MANIFEST.json').read_bytes())=='97520bba53dda8830db2e11762e0e52abdc6f6ec11eea60bad95e70473c74645');seal=j(D/'SEAL_RECEIPT.json')
ck('seal count111 and bytes',manifest['file_count']==111 and len(manifest['files'])==111 and sum(v['bytes'] for v in manifest['files'])==manifest['total_bytes']==1453854)
for v in manifest['files']:
 pin(D/v['relative_path'],v);ck('source mode '+v['relative_path'],reads[str(D/v['relative_path'])]['mode']==v['mode'])
ck('sealer actual source identity',seal['actual_sealer_PID']==manifest['actual_sealer_PID']==52864 and seal['sealed'] is True and seal['allfiles_including_manifest_and_receipt']==113)
sys.path.insert(0,str(D));import v3_guards as g
family=j(D/'CORE_FAMILY_MANIFEST.json');ck('known core family',family['code_family_sha256']=='f0e5185cda10f88894dfc7c94146d7943de3e329b08d0700335c9a486c5a08e2')
diff=[];changed=[]
for name in g.PROGRAMS:
 old=read(V4/name);new=pin(D/name,family['program_files'][name])
 if old!=new:changed.append(name);diff.extend(difflib.unified_diff(old.decode().splitlines(True),new.decode().splitlines(True),fromfile='sealed_corrected_v4/'+name,tofile='corrected_v5/'+name))
ck('only actual guards changed',changed==['v3_guards.py']);ck('full source diff independently regenerated',read(D/'CORE_SOURCE_DIFF.patch')==''.join(diff).encode())
pred=j(D/'PREDECESSOR_UNCHANGED_INPUT_PINS.json')
for v in pred['files']:pin(v['path'],v)
pred_counts=dict(collections.Counter(v['group'] for v in pred['files']))
# Authenticate original35-test actual custody, never rerun sealed-folder fixture suites.
pj=j(D/'execution_receipts/PROCESS_JOURNAL.json');ck('two sealed fixture processes',len(pj['records'])==2)
for mode,r in zip(['NORMAL','OPTIMIZED'],pj['records']):
 t=j(D/(mode+'_FIXTURE_RESULTS.json'));ck('35 exact successful fixture tests '+mode,t['tests']==35 and t['all_passed'] is True and t['actual_PID']==r['PID'] and t['argv']==r['argv'] and t['exit_code']==r['exit_code']==0 and t['UTC_start']==r['UTC_start'] and t['UTC_end']==r['UTC_end'] and r['child_reaped'] is True and r['termination_reason'] is None)
 for stream in ['stdout','stderr']:
  b=pin(t[stream]['path'],t[stream]);q=r[stream];ck('sealed fixture stream observed '+mode+stream,len(b)==q['bytes_observed'] and sha(b)==q['sha256_observed']);ret=read(D/'execution_receipts'/q['retained_path']);ck('sealed fixture retained exact '+mode+stream,ret==b[:4096] and len(ret)==q['retained_bytes'] and sha(ret)==q['retained_sha256'])
 ck('sealed fixture terminal OK '+mode,read(t['stderr']['path']).endswith(b'OK\n'))
# Frozen actual V5 input; only source selector/body hash changes from historical V4.
f=D/'EXECUTION_INPUTS_FROZEN_20261006.json';data=read(f);x=g.loads(data);g.validate_execution_manifest(x,data);cfg=x['effective'];ck('frozen0444 precise SHA',sha(data)=='dfe3e71993e3bd99afb9c11e54f4fe4c9117c770849ffac54c7bc2b17e6bd76a' and reads[str(f)]['mode']=='0444' and len(data)==69303)
old=g.loads(read(V4/'EXECUTION_INPUTS_FROZEN_20261006.json'));ck('all20 effective unchanged',x['effective']==old['effective'] and len(cfg)==20);ck('all180 non-gate pins unchanged',x['input_files']==old['input_files'] and len(x['input_files'])==180 and sum(p['bytes'] for p in x['input_files'])==1846309)
ck('program map frozen exact',len(x['program_files'])==5 and all(v['path']==str((D/Path(v['path']).name).relative_to(C)) and {k:v[k] for k in ['bytes','sha256']}==family['program_files'][Path(v['path']).name] for v in x['program_files']))
packet=j(B/'PACKET_MANIFEST.json');ck('inert packet8payload',len(packet['files'])==8)
for v in packet['files']:pin(B/v['relative_path'],v)
ck('packet frozen equality',read(B/'EXECUTION_INPUTS_DRAFT.json')==data)
for v in x['input_files']:pin(C/v['path'],v)
usage=j(B/'EXACT_INPUT_USAGE.json');gates=j(B/'PROPOSED_GATE_CHECKED_ARTIFACT_USAGE.json');registry={v['path']:v for v in x['input_files']}
ck('all usage nonempty and exact180',set(usage)==set(registry) and all(usage.values()))
for path,names in usage.items():
 for name in names:
  if name.startswith('gate_checked_artifact:'):ck('gate registry correspondent '+path,registry[path] in gates[name.split(':',1)[1]])
ck('no future report/root gate self-cycle',not any('native_v5_joint_source_configuration_adversary_20261006' in p or '/gates/' in p for p in registry))
# Complete capacity independently regenerated and counted, without native entry points.
cp=j(B/'CAPACITY_PLAN_WITH_RESERVED_GATES.json');ap=cfg['original_authentication_pins'];np=cfg['native_baseline_pins'];pack=g.loads(read(C/cfg['package']['manifest']['path']));package={v['relative_path']:read(C/cfg['package']['root']/v['relative_path']) for v in pack['files']}
copies=[('bundle/'+g.N+'publication/authenticated_inputs/'+str((C/v['path']).relative_to(A)),v['bytes']) for v in x['input_files']]
orig=A/'original_source_authentication_20261006/original_attempt'
copies += [('bundle/'+g.N+'historical_original/'+str((C/v['path']).relative_to(orig)),v['bytes']) for v in ap['original_files']]
for v in cfg['effective_diagnostics_pins']:
 name=str((C/v['path']).relative_to(A/'repaired_diagnostics_v1'));copies.append(('bundle/'+g.N+('EFFECTIVE_DIAGNOSTICS_README.md' if name=='README.md' else name),v['bytes']))
sr=next(v for v in ap['original_files'] if v['path'].endswith('/source_record.json'));copies += [('bundle/'+g.N+'source_record.json',sr['bytes']),('bundle/'+g.N+'prior_imported_report.json',ap['selected_prior']['bytes']),('bundle/'+g.N+'publication/EXECUTION_INPUTS.json',len(data))]
actual=g.capacity_inventory(np,copies,{role:{'bytes':65536} for role in g.GATE_ROLES},package,cfg['capacity_policy'],cfg['process_policy'])
ck('every capacity entry/formula matches',all(cp[k]==v for k,v in actual.items()))
mutable={'catalog.json','assessments.json','state.json','history.jsonl','assessment_history.jsonl','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md'}
native=sum(v['bytes']+(524288 if Path(v['path']).name in mutable else 0) for v in np);globalcopies=sum(v['bytes']+524288 for v in np if Path(v['path']).name in mutable)
independent=native+globalcopies+sum(n for _,n in copies)+7*65536+sum(map(len,package.values()))+9*131072+7*65536+128*4096+max(v['bytes']+524288 for v in np if Path(v['path']).name in {'catalog.json','assessments.json','state.json','summary.json'})
ck('independent135358232 and427 slots',independent==actual['max_materialized_bytes']==135358232 and len(actual['entries'])==426 and actual['file_count_cap']==427)
ck('independent194078488 reserve envelope',actual['required_free_bytes']==independent+16*1024**2+32*1024**2+8*1024**2==194078488)
free=shutil.disk_usage(D).free;ck('present snapshot capacity sufficient',free>=actual['required_free_bytes'])
privacy=j(B/'PRIVATE_EXPORT_EXCLUSIONS.json');expected_exclusions={g.N+'publication/authenticated_inputs/actual_operations/tracker_postpub_metadata/stdout.bin',g.N+'publication/authenticated_inputs/actual_operations/tracker_postpub_DOI_dedup/stdout.bin'}
ck('exact two private Sheetbody exclusions',len(privacy['exclusions'])==2 and {v['candidate_affected_path'] for v in privacy['exclusions']}==expected_exclusions and all(registry[v['input_pin']['path']]==v['input_pin'] for v in privacy['exclusions']))
runtime=cfg['runtime'];ck('exact Python version/executable',str(Path(sys.executable).resolve())==runtime['python_executable'] and sys.version==runtime['python_version'])
for role in ['python','git','gh']:opaque(runtime[role+'_executable'],runtime[role+'_binary'])
private=cfg['environment_policy']['git']['repository_config_pins']+cfg['environment_policy']['git']['repository_location_pins']+cfg['environment_policy']['gh']['config_pins']
for v in private:opaque(v['path'],v)
ck('private bodies absent registry',not set(registry)&{str(Path(v['path']).relative_to(C)) for v in private if Path(v['path']).is_relative_to(C)})
for name,v in cfg['raw_source_pins'].items():opaque(R/'unsolved_math_prioritization/cache'/name,v)
opaque(R/'unsolved_math_prioritization/cache/catalog.sqlite',cfg['source_cache_pin']);ck('SQL no sidecar',not any(Path(str(R/'unsolved_math_prioritization/cache/catalog.sqlite')+s).exists() for s in ['-wal','-shm','-journal']))
# All12 native baseline bindings use actual prior local Git read custody; no new Git invocation.
journal=j(B/'READ_ONLY_GIT_PROCESS_JOURNAL.json');ck('inert builder16 actual reads',len(journal['records'])==16)
for r in journal['records']:ck('inert clean local read custody '+str(r['PID']),r['exit_code']==0 and r['cwd']==str(C) and r['environment']==cfg['environment_policy']['git']['environment'] and r['ambient_inherited'] is False)
for v in np:
 matches=[r for r in journal['records'] if r['argv'][1:]==['show',cfg['main_parent']+':'+v['path']]];ck('native actual blob custody '+v['path'],len(matches)==1 and matches[0]['stdout_bytes']==v['bytes'] and matches[0]['stdout_sha256']==v['sha256'])
 p=C/v['path']
 if p.exists():opaque(p,v)
# Root actual clean-runtime source, outer exit and three complete retained actual reads.
probe=A/'root_native_runtime_read_probe_v5_20261006';root=j(probe/'ROOT_RECEIPT.json');pj=j(probe/'PROCESS_JOURNAL.json');outer=j(A/'actual_operations/root_clean_native_V5_runtime_account_PR_probe/execution.json');pin(A/'root_native_runtime_read_probe_v5.py',{'bytes':4703,'sha256':'c341a59dce311849e553082dc365658021c30d5e93f3cba63b082da7f80157ae'})
ck('actual root probe PID/hash/exit',root['actual_operator_PID']==pj['actual_operator_PID']==outer['PID']==54847 and root['actual_receipt'] is True and root['fixture'] is False and root['execution_inputs_sha256']==sha(data) and root['main_parent']==cfg['main_parent'] and outer['exit_code']==0)
ck('three exact child PIDs/custody',len(pj['records'])==3 and root['actual_process_PIDs']==[v['PID'] for v in pj['records']])
for i,r in enumerate(pj['records']):
 ck('root probe actual success '+str(i),r['actual_process_record'] is True and r['fixture'] is False and r['exit_code']==0 and r['termination_reason'] is None and r['child_reaped'] is True and r['output_complete'] is True and r['cwd']==str(C) and r['ambient_environment_inherited'] is False and r['effective_nonsecret_environment']==cfg['environment_policy'][r['executable_role']]['environment'])
 for s in ['stdout','stderr']:
  q=r[s];body=read(probe/q['retained_path']);ck('root complete stream '+str(i)+s,len(body)==q['bytes_observed']==q['retained_bytes'] and sha(body)==q['sha256_observed']==q['retained_sha256'])
ck('root account Alec actually read',read(probe/pj['records'][0]['stdout']['retained_path']).strip()==b'AlecKriebel')
ck('root actual PR equals frozen',j(probe/pj['records'][1]['stdout']['retained_path'])=={'baseRefName':'main','headRefName':'dot/math-30003996','headRefOid':g.HEAD,'isDraft':True,'number':108,'state':'OPEN'})
ck('root actual remote f36',read(probe/pj['records'][2]['stdout']['retained_path']).decode().split()==[cfg['main_parent'],'refs/heads/main'])
ck('root private metadata same pins only',root['private_configuration_validated_metadata_only_in_output']==[{'role':'git' if v in cfg['environment_policy']['git']['repository_config_pins'] else 'gh',**v,'body_retained_or_disclosed':False} for v in private] and root['private_body_contents_logged_or_copied'] is False)
ck('no root native/config/gates',root['native_prepare_assess_or_export_called'] is False and root['thin_config_or_review_gates_created'] is False and root['new_central_proof_search_turns']==0)
# Input-level proof provenance counts; mathematical contents are not re-reviewed.
auth=j(C/ap['blob_manifest']['path']);sp=j(C/ap['sourcepair']['path']);qauth=j(C/ap['queue_projection']['path'])
ck('original15 exact and historical2of5',auth['incoming_body_count']==15 and auth['literal_status']=='claimed_solved' and auth['original_author_effort']=='2/5' and qauth['original_budget']=='2/5' and len(ap['original_files'])==15)
ck('absent original structured ledgers',not any(Path(v['path']).name in ['status.json','turns.jsonl'] for v in ap['original_files']))
ck('source pair empty report preserved',j(C/ap['selected_prior']['path'])=={} and sp['authenticated_no_join_prior_report'] is True and sp['submitted_prior_equals_raw_and_SQL'] is False)
ck('published46 exact source binding',len(package)==46 and pack['original_head']==g.HEAD and pack['imported_prior_report']=={} and pack['effective_proof_sha256']=='2818eab189445649ae1ba98d55e3da3e5fab918de88f1779de86962ba99a3393')
read(A/'NATIVE_INTEGRATION_AND_MERGE_PLAN_20261006.md');read(A/'scoped_checkpoint_bounded.py');read(A/'ROOT_BOUNDED_CHECKPOINT_PREPARATION_20261006.json')
now=datetime.datetime.now(datetime.timezone.utc).isoformat();result={'schema':'pr108-joint-V5-exact-source-config-authentication/v1','UTC':now,'actual_operator_PID':os.getpid(),'checks_passed':len(checks),'check_names':checks,'execution_inputs_sha256':sha(data),'source_manifest_sha256':sha((D/'OUTPUT_MANIFEST.json').read_bytes()),'source111payload113sealed_files_checked':True,'predecessor_group_counts':pred_counts,'source_fixture_tests_per_mode':35,'independent_tests_per_mode':458,'input_files':180,'input_bytes':1846309,'capacity_exact_slots':427,'capacity_max_materialized_bytes':135358232,'required_free_bytes':194078488,'observed_free_bytes':free,'free_space_timestamp':now,'runtime_private_metadata_pins_checked':True,'private_configuration_body_semantic_inspection_by_auditor':False,'root_actual_private_validation_process_authenticated':True,'native_or_SQL_execution_service_Git_commands_by_auditor':0,'present_capacity_is_snapshot_recheck_required_before_actual_candidate':True}
(O/'EXACT_INPUT_AUTHENTICATION.json').write_bytes(g.canonical(result));(O/'READ_SCOPE_MANIFEST.json').write_bytes(g.canonical({'schema':'pr108-joint-V5-read-scope/v1','UTC':now,'actual_operator_PID':os.getpid(),'files':sorted(reads.values(),key=lambda v:v['path']),'body_copies_written':False}));print(json.dumps({k:v for k,v in result.items() if k not in ['check_names','predecessor_group_counts']}))
