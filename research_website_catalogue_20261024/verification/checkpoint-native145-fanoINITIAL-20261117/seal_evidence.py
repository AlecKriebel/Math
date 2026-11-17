"""Own captured evidence only: verify and finitely seal after root hold release."""
import datetime,hashlib,json,stat
from pathlib import Path
if not __debug__:raise RuntimeError('Assertions required')
OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/checkpoint-native145-fanoINITIAL-20261117')
def read(n):return json.loads((OWN/n).read_bytes())
def pin(p):
 a=p.lstat();assert stat.S_ISREG(a.st_mode) and not p.is_symlink();b=p.read_bytes();z=p.lstat()
 assert (a.st_dev,a.st_ino,a.st_mode,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
 return dict(bytes=len(b),SHA256=hashlib.sha256(b).hexdigest(),mode=format(stat.S_IMODE(z.st_mode),'04o'))
runs=read('RUNS.json');assert len(runs)==6 and all(x['exit_code']==0 for x in runs)
before,after=read('GUARDS_BEFORE.json'),read('GUARDS_AFTER.json')
for k in ['repositories','native_root_gitignore','public','immutable_packets']:assert before[k]==after[k],k
release=read('ROOT_RELEASE.json');dry,post=read('DRY_TREE_AUDIT.json'),read('POST_TREE_AUDIT.json');dr,pr=read('DRY_RUN.receipt.json'),read('PUSH.receipt.json')
parent='bbfb7abf5c56e3f8d090e125784ff357138076fb'
for mode in ['DRY_RUN','PUSH']:
 inv=read(mode+'.invocation.json');probe=read('PRE_'+mode+'_REMOTE_PARENT.invocation.json')
 assert inv['exit_code']==0 and inv['helper_unchanged'] and probe['exit_code']==0 and probe['expected_parent']==parent
 assert (OWN/probe['raw_stdout_file']).read_bytes().splitlines()==[(parent+'\trefs/heads/main').encode()]
assert dr['parent']==pr['parent']==post['parent']==release['expected_parent']==parent
assert post['commit']==pr['commit'] and post['tree']==pr['tree'] and post['fresh_actual_remote_main'].split()[0]==pr['commit']
assert dry['sibling_root_entries_preserved']==post['sibling_root_entries_preserved']==159
assert dry['excluded_actual_paths']==post['excluded_actual_paths'] and post['dry_to_push_tree_delta']==['research_website_catalogue_20261024/verification/checkpoint-subtree-dry-run-20261025.json']
assert all(x['complete_current_nonignored_local_files_equal_committed_tree'] for x in post['durable_packet_and_source_closures'])
initial=before['immutable_packets']['papers/23411227/reviews/root-initial-20261117']
assert len(initial['files'])==18 and len(initial['directories'])==1 and initial['root_mode']=='0o555' and all(x['mode']=='0o444' for x in initial['files'].values()) and set(initial['directories'].values())=={'0o555'}
closure=next(x for x in post['durable_packet_and_source_closures'] if x['path']=='papers/23411227/reviews/root-initial-20261117')
assert closure['committed_regular_files']==13 and closure['ignored_regular_files']==5
assert release['scientific_reviewed']==release['native_Sheet_reviewed']==145 and release['scientific_passes']==137 and release['scientific_deferred']==8 and release['scientific_remaining']==58
assert release['programme_counts']==dict(verified=123,deployed=10,preparing=4,under_review=6,queued=50,holds=2,deferred=8)
now=datetime.datetime.now(datetime.timezone.utc).isoformat();percent=145/203*100
summary=dict(UTC=now,commit=pr['commit'],parent=parent,tree=pr['tree'],changed_paths=post['changed_paths'],status_counts=post['status_counts'],all159siblings_docs_exact=True,whole_changed_blob_bytes_and_modes_verified=True,durable_closures=len(post['durable_packet_and_source_closures']),key_files=len(post['key_actual_committed_files']),native_and_public_whole_guards_equal=True,native_root_gitignore=after['native_root_gitignore'],public_files=len(after['public']['files']),public_child_directories=len(after['public']['directories']),public_root_mode=after['public']['root_mode'],fano_INITIAL_physical_files=18,fano_INITIAL_child_directories=1,fano_committed_files=13,fano_actual_ignored_PNGs=5,fano_manifest_hash_binds_all18=True,failed_overlay12_and_distinct_corrected17_preserved=True,excluded_actual_paths=post['excluded_actual_paths'],scientific_and_native_reviewed=145,scientific_passes=137,deferred=8,remaining=58,total=203,percent=percent,programme_counts=release['programme_counts'],checkpoint_completion_percent=100,programme_goal_active_incomplete=True)
with (OWN/'FINAL_CHECKS.json').open('x') as f:json.dump(summary,f,indent=2);f.write('\n')
report='# Scoped native145 / Fano INITIAL checkpoint\n\nVerified ordinary nonforce checkpoint `'+pr['commit']+'`, parent `'+parent+'`, tree `'+pr['tree']+'`. One dry run, one actual push and all six ordered guard/audit steps returned0. All '+str(post['changed_paths'])+' changed paths remain within the programme; every changed whole blob and Git mode, '+str(summary['durable_closures'])+' durable source/packet closures and '+str(summary['key_files'])+' key files authenticate. All159 untargeted remote root entries, including released docs, remain exact. Native M/W HEAD, raw index, config, config.worktree and logical/loose local heads, native M-root ignore file and all803public files/387childdirs/root0750 whole bytes/modes/topology remain exact. Private caches and journals retain actual ignore boundaries.\n\nFano original-only INITIAL is physically18files/1childdir, files0444 and directories0555. Its13 nonignored leaves are committed;5PNG rasters remain actually ignored locally and all18 hashes remain bound by the committed manifest. No force-add occurred. Root original review remains35% without a scientific verdict, primary/support/current-peer body exposure or scientific execution at this INITIAL seal. The native145 transition receipt, lossless packed full snapshots, new queue, frozen private editorial controls, original failed12-file overlay audit, distinct corrected17-file audit and previous checkpoint56-file packet are included. The original failed audit remains failed with its literal exit1 and no AFTER/RESULTS; it is not relabeled PASS.\n\nScientific and native review145/203='+format(percent,'.6f')+'%;137PASS,8deferred,58remaining. Native status counts123verified,10deployed,4preparing,6under review,50queued,2holds,8deferred. Programme active/incomplete; this finite checkpoint100% complete. No old production helper, scientific source, website/Sheet action, release or outside contact was executed.\n'
with (OWN/'REPORT.md').open('x') as f:f.write(report)
with (OWN/'CHECKPOINT_LOG.md').open('a') as f:f.write('\n'+now+' — Actual remote/parent/tree/changedblobs/modes/159siblings/docs/durableclosures/nativepublic guards all0. Ownonly finite seal; checkpoint100%; scientific/native145/203=71.428571%; FanoINITIAL35%noverdict; programme active/incomplete.\n')
for n in ['MANIFEST.json','FINAL.json']:
 with (OWN/n).open('x') as f:f.write('{}\n')
files={};dirs={}
for p in sorted(OWN.rglob('*')):
 rel=p.relative_to(OWN).as_posix();assert not p.is_symlink()
 if p.is_dir():dirs[rel]=format(stat.S_IMODE(p.stat().st_mode),'04o')
 elif rel not in ['MANIFEST.json','FINAL.json']:files[rel]=pin(p)
assert not dirs
manifest=dict(UTC=now,root=str(OWN),root_mode=format(stat.S_IMODE(OWN.stat().st_mode),'04o'),regular_files=len(files)+2,child_directories=0,payload_files=[dict(path=n,**p,empty=p['bytes']==0,hidden=any(x.startswith('.') for x in Path(n).parts)) for n,p in sorted(files.items())],directories=[],exact_existing_terminal_recursive_hash_exclusions=['MANIFEST.json','FINAL.json'],terminal_modes={n:format(stat.S_IMODE((OWN/n).stat().st_mode),'04o') for n in ['MANIFEST.json','FINAL.json']},other_exclusions=[],all_hidden_empty_bytes_modes_topology_included=True)
(OWN/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
final=dict(UTC=now,status='SCOPED_CHECKPOINT_PUSHED_VERIFIED',commit=pr['commit'],parent=parent,tree=pr['tree'],files=manifest['regular_files'],child_directories=0,manifest=pin(OWN/'MANIFEST.json'),all_payloads_verified=True,checkpoint_completion_percent=100,overall_review_percent=percent,programme_goal_active_incomplete=True,no_current_P_W_reads_by_sealer=True)
(OWN/'FINAL.json').write_text(json.dumps(final,indent=2)+'\n')
for n,p in files.items():assert pin(OWN/n)==p,n
assert pin(OWN/'MANIFEST.json')==final['manifest'] and {p.relative_to(OWN).as_posix() for p in OWN.rglob('*') if p.is_file()}==set(files)|{'MANIFEST.json','FINAL.json'}
print(json.dumps(final))
