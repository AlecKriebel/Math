"""One strict passive Fano custody check; no scientific source execution/import."""
import datetime,hashlib,json,os,re,stat
from pathlib import Path
if not __debug__:raise RuntimeError('Assertions required')
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');B=P/'papers/23411227';OWN=P/'verification/fano-root-evidence-custody-sol-20261117'
ROOTS={'source':B/'sources','root_INITIAL':B/'reviews/root-initial-20261117','adversarial':B/'reviews/adversarial-sol','scope':B/'reviews/scope-sol'}
EXTENTS={'source':(196,21),'root_INITIAL':(18,1),'adversarial':(67,3),'scope':(53,4)}
def digest(b):return hashlib.sha256(b).hexdigest()
def raw(p):
 assert any(p==r or p.is_relative_to(r) for r in ROOTS.values()),str(p)
 a=p.lstat();assert stat.S_ISREG(a.st_mode) and not p.is_symlink(),str(p)
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  z=os.fstat(fd);assert (a.st_dev,a.st_ino)==(z.st_dev,z.st_ino)
  with os.fdopen(fd,'rb',closefd=False) as f:b=f.read()
  q=os.fstat(fd);assert (z.st_dev,z.st_ino,z.st_mode,z.st_size,z.st_mtime_ns,z.st_ctime_ns)==(q.st_dev,q.st_ino,q.st_mode,q.st_size,q.st_mtime_ns,q.st_ctime_ns)
  assert len(b)==q.st_size;return b
 finally:os.close(fd)
def load(p):return json.loads(raw(p))
def safe(text,root_allowed=False):
 p=Path(text);assert not p.is_absolute() and '..' not in p.parts,text
 if not root_allowed:assert str(p) not in ['','.'],text
 return p.as_posix()
def census(root):
 files={};dirs={};pending=[root]
 while pending:
  here=pending.pop();a=here.lstat();assert stat.S_ISDIR(a.st_mode) and not here.is_symlink()
  entries=sorted(here.iterdir());rel=here.relative_to(root).as_posix();dp=dict(mode=format(stat.S_IMODE(a.st_mode),'04o'),mtime_ns=a.st_mtime_ns,ctime_ns=a.st_ctime_ns,empty=not entries,hidden=any(x.startswith('.') for x in Path(rel).parts))
  if rel=='.':rootmeta=dp
  else:dirs[rel]=dp
  for p in entries:
   z=p.lstat();assert not p.is_symlink();name=p.relative_to(root).as_posix()
   if stat.S_ISDIR(z.st_mode):pending.append(p)
   else:
    b=raw(p);files[name]=dict(bytes=len(b),SHA256=digest(b),mode=format(stat.S_IMODE(z.st_mode),'04o'),mtime_ns=z.st_mtime_ns,ctime_ns=z.st_ctime_ns,empty=not b,hidden=any(x.startswith('.') for x in Path(name).parts))
  z=here.lstat();assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_mtime_ns,z.st_ctime_ns)
 return dict(root=str(root),root_metadata=rootmeta,files=files,directories=dirs)
started=datetime.datetime.now(datetime.timezone.utc).isoformat();before={n:census(r) for n,r in ROOTS.items()}
for n,(nf,nd) in EXTENTS.items():assert (len(before[n]['files']),len(before[n]['directories']))==(nf,nd),n
assert sum(len(x['files']) for x in before.values())==334 and sum(len(x['directories']) for x in before.values())==29
external=[('source','SOURCE_FINAL.json',910,'46a1f71e118fff3101c7f0af2158658847ad338172d7bd6d119ba041c8613886'),('source','SOURCE_MANIFEST.json',60052,'3bd41786837658193a0258d1f1a70dc719f0e321647ed885294e9947f64a1e7b'),('root_INITIAL','INITIAL_SEAL.json',944,'7d2c5575923b6b56ef4c4c77150a2d52a4e7ba82b71d85f2d68b13a704ce72f2'),('root_INITIAL','INITIAL_MANIFEST.json',5788,'ab3298ed377b33150f9b9fa8f4d2b5900298459bdff82c30c4d172cf7f528ea0'),('adversarial','FINAL.json',1688,'5c57c5d78e57cdc6d03c53840746bf7ec631e9d75fe488d595a6ec6d0bb77443'),('adversarial','OWNED_MANIFEST.json',12615,'13a06ca34d39c7eb60233a3f673c7fc06c74b497ff347ab12dd6e01c70b5ea52'),('adversarial','INITIAL_SEAL.json',1414,'144427db7537cfec5e3b4bb4e48ffb7d8c64e3e3b2190469e53abeff71399b5a'),('scope','FINAL.json',11903,'02c20c80c6e6ff9665693258e5358c2bfd54ff3adaf46bba6711ac1512a84b72'),('scope','OWNED_MANIFEST.json',12415,'a84e317b625ee55a4a75fb2c9bf0515d929b0c596d283d494686695f809cdba7'),('scope','INITIAL_SEAL.json',7353,'9824af712729e883f8871d54fe50d9fb616ccd8c06e57874047bd818b69962e9'),('scope','NATIVE_EXECUTION.json',1430,'c143af5fe4de50f950777d24e0797d5cd2e68e8600d88e90c8cca387780b166b'),('scope','native.stderr.txt',720,'f15489e27ecc022adeb77de99b33070a3e64e274d3b83ac02d9abb93d605a897')]
for label,rel,size,sha in external:assert (before[label]['files'][rel]['bytes'],before[label]['files'][rel]['SHA256'])==(size,sha),(label,rel)
def metadata(actual,row):
 if 'mode' in row:assert int(actual['mode'],8)==int(row['mode'],8),row
 for k in ['bytes','mtime_ns','ctime_ns','hidden','empty']:
  if k in row:assert actual[k]==row[k],(row.get('path','metadata'),k,actual[k],row[k])
def filepin(label,rel,row,hash_required=True):
 rel=safe(rel);actual=before[label]['files'][rel];metadata(actual,row)
 if hash_required:
  sha=row['SHA256'] if 'SHA256' in row else row['sha256'];assert isinstance(sha,str) and re.fullmatch('[0-9a-f]{64}',sha)
  assert actual['SHA256']==sha,(label,rel)
 return rel
def payload(label,rows):
 assert isinstance(rows,list);names=set()
 for row in rows:
  assert isinstance(row,dict);rel=filepin(label,row['path'],row);assert rel not in names;names.add(rel)
 return names
def directories(label,rows,complete=False):
 assert isinstance(rows,list);names=set()
 for row in rows:
  rel=safe(row['path'],True);actual=before[label]['root_metadata'] if rel=='.' else before[label]['directories'][rel];metadata(actual,row);assert rel not in names;names.add(rel)
 if complete:assert names==set(before[label]['directories'])|({'.'} if '.' in names else set())
 return names
def matching_links(label,row):
 sha=row['SHA256'] if 'SHA256' in row else row['sha256'];matches=[n for n,p in before[label]['files'].items() if p['SHA256']==sha and p['bytes']==row['bytes']]
 assert matches,(label,row)
 for rel in matches:filepin(label,rel,row)
 return sorted(matches)
checks=[]
sm=load(ROOTS['source']/'SOURCE_MANIFEST.json');sf=load(ROOTS['source']/'SOURCE_FINAL.json')
snames=payload('source',sm['files']);st=set(sm['root_controls_excluded_from_own_list'])
assert st=={'SOURCE_MANIFEST.json','SOURCE_FINAL.json'} and snames|st==set(before['source']['files']) and not snames&st
assert set(sm['actual_file_paths_including_controls'])==set(before['source']['files']) and sm['exact_controls_existed_before_enumeration'] is True
assert sm['ordinary_files_including_controls']==196 and sm['child_directory_count']==21 and int(sm['root_mode'],8)==int(before['source']['root_metadata']['mode'],8)
directories('source',sm['directories'],True);filepin('source','SOURCE_MANIFEST.json',sf['SOURCE_MANIFEST']);filepin('source','SOURCE_READY.json',sf['SOURCE_READY'])
checks.append(dict(namespace='source',payload_hash_rows=len(snames),exact_terminal_exclusions=sorted(st),all_declared_file_directory_metadata_checked=True,SOURCE_FINAL_undeclared_mode_observed=before['source']['files']['SOURCE_FINAL.json']['mode']))
rm=load(ROOTS['root_INITIAL']/'INITIAL_MANIFEST.json');rs=load(ROOTS['root_INITIAL']/'INITIAL_SEAL.json');rterm=set(rm['terminal_content_hash_exclusions_exact']);assert rterm=={'INITIAL_MANIFEST.json','INITIAL_SEAL.json'}
rfiles=set();rdirs=set();rhash=0
for row in rm['entries']:
 rel=safe(row['path'],True)
 if row['kind']=='directory':
  actual=before['root_INITIAL']['root_metadata'] if rel=='.' else before['root_INITIAL']['directories'][rel];metadata(actual,row);assert rel not in rdirs;rdirs.add(rel)
 else:
  assert row['kind']=='file' and rel not in rfiles;rfiles.add(rel)
  if rel in rterm:
   assert row['content_hash_exclusion']=='Exact already-created terminal pair only' and 'SHA256' not in row and 'sha256' not in row;filepin('root_INITIAL',rel,row,False)
  else:filepin('root_INITIAL',rel,row);rhash+=1
assert rfiles==set(before['root_INITIAL']['files']) and rdirs==set(before['root_INITIAL']['directories'])|{'.'} and rm['files']==18 and rm['child_directories']==1
assert before['root_INITIAL']['root_metadata']['mode']=='0555' and all(p['mode']=='0444' for p in before['root_INITIAL']['files'].values()) and set(p['mode'] for p in before['root_INITIAL']['directories'].values())=={'0555'}
assert rs['manifest_SHA256']==before['root_INITIAL']['files']['INITIAL_MANIFEST.json']['SHA256'] and rs['INITIAL_SHA256']==before['root_INITIAL']['files']['INITIAL.md']['SHA256']
assert rs['scientific_program_executions']==0 and rs['support_primary_current_peer_bodies_unread'] is True
checks.append(dict(namespace='root_INITIAL',payload_hash_rows=rhash,exact_terminal_exclusions=sorted(rterm),every_declared_mtime_mode_size_hidden_empty_value_checked=True,all_terminal_whole_hashes_externally_pinned=True))
am=load(ROOTS['adversarial']/'OWNED_MANIFEST.json');af=load(ROOTS['adversarial']/'FINAL.json');an=payload('adversarial',am['files']);at=set(am['exact_root_terminal_exclusions'])
assert at=={'FINAL.json','OWNED_MANIFEST.json'} and an|at==set(before['adversarial']['files']) and not an&at and am['ordinary_files_including_two_controls']==67 and am['child_directory_count']==3
assert int(am['root_mode'],8)==int(before['adversarial']['root_metadata']['mode'],8);directories('adversarial',am['directories'],True)
filepin('adversarial','OWNED_MANIFEST.json',af['manifest']);filepin('adversarial','INITIAL_SEAL.json',af['immutable_INITIAL_seal']);assert af['scientific_program_executions']==0
ai=load(ROOTS['adversarial']/'INITIAL_SEAL.json');aim=load(ROOTS['adversarial']/'INITIAL_MANIFEST.json');ain=payload('adversarial',aim['payloads']);ait=set(aim['exact_root_terminal_exclusions']);assert ait=={'INITIAL_MANIFEST.json','INITIAL_SEAL.json'} and not ain&ait and len(ain|ait)==aim['files_including_two_terminal_controls']==ai['actual_regular_files']==19
directories('adversarial',aim['directories']);assert ai['original_scientific_program_executions']==0 and ai['foreign_proof_support_archived_current_peer_root_bodies_opened'] is False
advlinks={k:matching_links('adversarial',ai[k]) for k in ['INITIAL','independent_results','manifest','source_pins']}
checks.append(dict(namespace='adversarial',payload_hash_rows=len(an),exact_terminal_exclusions=sorted(at),immutable_INITIAL_payload_hash_rows=len(ain),immutable_INITIAL_exact_terminal_exclusions=sorted(ait),INITIAL_metadata_links=advlinks,historical_scientific_executions=0,all_declared_file_directory_metadata_checked=True))
cm=load(ROOTS['scope']/'OWNED_MANIFEST.json');cf=load(ROOTS['scope']/'FINAL.json');ct={str(Path(n).relative_to(ROOTS['scope'])) for n in cm['exact_already_created_terminal_control_exclusions']};assert ct=={'FINAL.json','OWNED_MANIFEST.json'} and cm['other_exclusions']==[]
cn=set();chashes=0
for row in cm['files']:
 rel=safe(row['path']);assert rel not in cn;cn.add(rel);assert row['type']=='regular'
 if rel in ct:
  assert row['terminal_control'] is True and row['byte_hash_exclusion']=='Exact already-created control; circular hash omitted. FINAL binds this manifest by whole-byte pin.' and 'sha256' not in row and 'SHA256' not in row;filepin('scope',rel,row,False)
 else:filepin('scope',rel,row);chashes+=1
assert cn==set(before['scope']['files']) and cm['regular_file_count']==53 and cm['child_directory_count']==4 and cm['directory_count_including_root']==5
directories('scope',cm['directories'],True);filepin('scope','OWNED_MANIFEST.json',cf['finite_closure']['manifest']);assert cf['finite_closure']['payload_hash_rows']==chashes==51
ci=load(ROOTS['scope']/'INITIAL_SEAL.json');cin=payload('scope',ci['payloads']);self_control=Path(ci['only_exact_already_created_self_hash_exclusion']);assert self_control==ROOTS['scope']/'INITIAL_SEAL.json'
assert cin|{'INITIAL_SEAL.json'}=={x['path'] for x in ci['complete_file_extent']} and len(cin)==20 and ci['regular_files_including_self']==21 and ci['future_subtree_basename_exclusions'] is False
for row in ci['complete_file_extent']:filepin('scope',row['path'],row,False)
directories('scope',ci['directories']);assert ci['native_scientific_program_execution_count']==0 and ci['archived_support_opinion_results_program_bodies_semantically_read'] is False and ci['foreign_supporting_mathematical_body_read'] is False and ci['current_root_or_peer_findings_read'] is False
for row in ci['source_controls']:
 p=Path(row['path']);assert p.parent==ROOTS['source'];filepin('source',p.name,row)
for k in ['seal','reconstruction','results','read_receipts','research_log']:filepin('scope',cf['initial'][k]['path'],cf['initial'][k])
fc=cf['finite_closure'];assert fc['regular_files_including_both_terminal_controls']==53 and fc['child_directories']==4 and fc['directories_including_root']==5
assert all(int(x['mode'],8)==int(fc['all_regular_modes'],8) for x in before['scope']['files'].values())
assert all(int(x['mode'],8)==int(fc['all_directory_modes'],8) for x in before['scope']['directories'].values()) and int(before['scope']['root_metadata']['mode'],8)==int(fc['all_directory_modes'],8)
assert set(fc['terminal_controls_excluded_only_by_exact_already_created_absolute_path'])==set(cm['exact_already_created_terminal_control_exclusions']) and fc['no_other_exclusions'] is True
checks.append(dict(namespace='scope',extent_rows=len(cn),payload_hash_rows=chashes,exact_terminal_exclusions=sorted(ct),explicit_terminal_marker_and_modes_checked=True,immutable_INITIAL_payload_hash_rows=len(cin),immutable_INITIAL_exact_absolute_self_exclusion=str(self_control),all_declared_file_directory_metadata_checked=True))
ne=load(ROOTS['scope']/'NATIVE_EXECUTION.json');stderr=raw(ROOTS['scope']/'native.stderr.txt');stdout=raw(ROOTS['scope']/'native.stdout.json')
assert ne['native_entrypoint_attempts']==1 and ne['exit_status']==1 and ne['native_checker_child_processes_reached']==0 and ne['successful_native_result_object_or_positive_checker_outputs'] is False
assert ne['retry_install_download_runtime_change_optimized_variant_or_campaign'] is False and ne['outer_portable_wrapper_execution'] is False
for k in ['stdout','stderr']:filepin('scope',ne[k]['path'],ne[k])
assert stdout==b'' and len(stderr)==720 and stderr.endswith(b"ModuleNotFoundError: No module named 'sympy'\n") and before['scope']['directories']['native-tmp']['empty'] is True
code_read=load(ROOTS['scope']/'NATIVE_CODE_READ.json');program_root=ROOTS['source']/'published-source/container-001/tree'
codepins=[]
for row in code_read['entire_exact_current_bodies_personally_read']:
 p=program_root/row['path'];b=raw(p);assert len(b)==row['bytes'] and digest(b)==row['sha256'] and len(b.splitlines())==row['lines'];codepins.append(dict(path=str(p),bytes=len(b),SHA256=digest(b),lines=len(b.splitlines())))
launcher=program_root/'source/verify_publication.py';lines=raw(launcher).decode().splitlines();assert len(lines)==148 and lines[117]=='    import sympy'
position={fragment:next(i+1 for i,l in enumerate(lines) if fragment in l) for fragment in ["result = {'packet_files_verified': integrity(), **editions()}",'result.update(replay())','with tempfile.TemporaryDirectory(', 'run = subprocess.run(']}
assert position["result = {'packet_files_verified': integrity(), **editions()}"]==141 and position['result.update(replay())']==143 and 118<position['with tempfile.TemporaryDirectory(']<position['run = subprocess.run(']
assert b'line 143, in main' in stderr and b'line 118, in replay' in stderr and str(launcher) in ne['command']
native=dict(recorded_attempts=1,recorded_exit=1,positive_checker_children=0,positive_native_result_object=False,literal_stderr=stderr.decode(),literal_stderr_SHA256=digest(stderr),literal_stdout_bytes=0,literal_stdout_SHA256=digest(stdout),exact_recorded_command=ne['command'],native_temporary_directory_empty=True,code_pins_authenticated=codepins,static_launcher_lines=position,lazy_import_line=118,control_flow_inference='On the recorded straight-line traceback path, main integrity/edition functions returned before replay entered lazy SymPy import. The import precedes temporary layout and child subprocess creation. This authenticates recorded failure/control flow, not positive scientific replay or mathematical proof.',repair_retry_install_or_replay_by_this_task=False)
after={n:census(r) for n,r in ROOTS.items()};assert before==after
result=dict(schema='fano-four-fixed-trees-custody-v1',started_UTC=started,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='DATA_CUSTODY_AUTHENTICATED',fixed_extent=dict(files=334,child_directories=29,roots=4),external_controls=[dict(namespace=n,path=rel,bytes=size,SHA256=sha,actual_mode=before[n]['files'][rel]['mode']) for n,rel,size,sha in external],manifest_and_INITIAL_checks=checks,historical_scope_native_failure=native,historical_ADV_scientific_executions=0,before=before,after=after,whole_before_after_equal=True,all_hidden_ignored_empty_bytes_modes_mtimes_ctimes_topology_included=True,peer_mathematical_findings_not_interpreted=True,new_scientific_execution=0,new_mathematical_verdict=False,administrative_V1_discovery_failure_retained=True,administrative_V1_stdout_not_separately_captured=True,distinct_authorized_V2_discovery_exit=0,main_custody_checker_invocations=1,completion_percent=100,programme_goal_active_incomplete=True)
with (OWN/'DATA_AUTHENTICATION.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(dict(status=result['status'],files=334,child_directories=29,external_controls=len(external),manifest_hash_rows=[x['payload_hash_rows'] for x in checks],whole_before_after_equal=True,historical_native_attempts=1,historical_native_exit=1,positive_children=0,ADV_scientific_executions=0,new_scientific_executions=0,new_mathematical_verdict=False,custody_completion_percent=100)))
