"""Verify captured checkpoint evidence and seal own packet only after hold release."""
from pathlib import Path
import datetime,hashlib,json,stat
if not __debug__:raise RuntimeError('Assertions required')
OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/checkpoint-fanoPASS146-twoINITIALs-20261117')
def read(n):return json.loads((OWN/n).read_bytes())
def pin(p):
 a=p.lstat();assert stat.S_ISREG(a.st_mode) and not p.is_symlink();b=p.read_bytes();z=p.lstat();assert (a.st_dev,a.st_ino,a.st_mode,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
 return dict(bytes=len(b),SHA256=hashlib.sha256(b).hexdigest(),mode=format(stat.S_IMODE(z.st_mode),'04o'))
runs=read('RUNS.json');assert len(runs)==6 and all(x['exit_code']==0 for x in runs)
before,after=read('GUARDS_BEFORE.json'),read('GUARDS_AFTER.json')
for k in ['repositories','native_root_gitignore','public','immutable_packets']:assert before[k]==after[k],k
release=read('ROOT_RELEASE.json');dry,post=read('DRY_TREE_AUDIT.json'),read('POST_TREE_AUDIT.json');dr,pr=read('DRY_RUN.receipt.json'),read('PUSH.receipt.json');parent='436ec422f9ae291a365b9ff2814cb88bc15db8f3'
for mode in ['DRY_RUN','PUSH']:
 inv=read(mode+'.invocation.json');probe=read('PRE_'+mode+'_REMOTE_PARENT.invocation.json');assert inv['exit_code']==0 and inv['helper_unchanged'] and probe['exit_code']==0 and probe['expected_parent']==parent
 assert (OWN/probe['raw_stdout_file']).read_bytes().splitlines()==[(parent+'\trefs/heads/main').encode()]
assert dr['parent']==pr['parent']==post['parent']==release['expected_parent']==parent and post['commit']==pr['commit'] and post['tree']==pr['tree'] and post['fresh_actual_remote_main'].split()[0]==pr['commit']
assert dry['sibling_root_entries_preserved']==post['sibling_root_entries_preserved']==159 and dry['excluded_actual_paths']==post['excluded_actual_paths']
assert post['dry_to_push_tree_delta']==['research_website_catalogue_20261024/verification/checkpoint-subtree-dry-run-20261025.json'] and all(x['complete_current_nonignored_local_files_equal_committed_tree'] for x in post['durable_packet_and_source_closures'])
assert release['scientific_reviewed']==146 and release['native_Sheet_reviewed']==145 and release['scientific_passes']==138 and release['scientific_deferred']==8 and release['scientific_remaining']==57 and release['total']==203
assert release['programme_counts']==dict(verified=123,deployed=10,preparing=4,under_review=6,queued=50,holds=2,deferred=8)
assert release['new193_peer_mathematical_reports_derivations_mechanisms_not_semantically_read'] is True
closures={x['path']:x for x in post['durable_packet_and_source_closures']}
for rel,nf,nd in [('papers/23204810/reviews/adversarial-sol',38,1),('papers/23204810/reviews/scope-sol/INITIAL',28,1),('papers/23411227/reviews/mw-input-challenge-sol-20261117',23,1)]:
 c=closures[rel];assert c['all_local_regular_files']==nf and len(c['child_directories'])==nd
initials=[{k:closures[p][k] for k in ['path','root_mode','all_local_regular_files','child_directories','committed_regular_files','ignored_regular_files']} for p in ['papers/23204810/reviews/adversarial-sol','papers/23204810/reviews/scope-sol/INITIAL']]
now=datetime.datetime.now(datetime.timezone.utc).isoformat();percent=146/203*100
summary=dict(UTC=now,commit=pr['commit'],parent=parent,tree=pr['tree'],changed_paths=post['changed_paths'],status_counts=post['status_counts'],all159siblings_docs_exact=True,whole_changed_blobs_bytes_modes_verified=True,durable_closures=len(closures),key_files=len(post['key_actual_committed_files']),whole_native_and_public_guards_equal=True,native_root_gitignore=after['native_root_gitignore'],public_files=len(after['public']['files']),public_child_directories=len(after['public']['directories']),public_root_mode=after['public']['root_mode'],two193_original_INITIALs_opaque_metadata=initials,new193_scientific_findings_not_semantically_read=True,private_cache_actual_ignore_boundaries_preserved=True,original_Fano_auxiliary_native_exit1_no_positive_children_preserved=True,prior_administrative_reader_failure_and_history_preserved=True,excluded_actual_paths=post['excluded_actual_paths'],scientific_reviewed=146,native_Sheet_reviewed=145,scientific_passes=138,deferred=8,remaining=57,total=203,scientific_percent=percent,programme_counts=release['programme_counts'],checkpoint_completion_percent=100,programme_goal_active_incomplete=True)
with (OWN/'FINAL_CHECKS.json').open('x') as f:json.dump(summary,f,indent=2);f.write('\n')
report='# Fano PASS146 / native145 / two original INITIALs checkpoint\n\nVerified ordinary nonforce commit `'+pr['commit']+'`, parent `'+parent+'`, tree `'+pr['tree']+'`. One dry run, one actual push, and all six ordered guard/audit steps returned0. All '+str(post['changed_paths'])+' changed paths are programme-only. Every changed whole blob and Git mode, '+str(len(closures))+' durable closures and '+str(len(post['key_actual_committed_files']))+' key files authenticate. All159 untargeted remote root siblings, including released docs, remain exact. Native M/W HEAD, raw indexes, configs/config.worktree and logical/loose local heads, M-root ignore file and all803public files/387childdirs/root0750 whole bytes/modes/topology remain unchanged.\n\nThe Fano final root review14970bytes and clearance2273bytes, root adoption, full current fixed families/custody19/primary-acquisition14, actual112/15 root continuation, MW challenge23/1, original and corrected UNFIT production packets, V3source14/static10, prior checkpoint54 and root bookkeeping are included. Actual ignored primary42/PDF/PNG/runtime/journal bodies remain local with whole hashes bound in retained metadata; no force-add occurred. Original auxiliary native attempt remains exit1 with no positive child replay. The earlier data-reader discovery error and explicitly authorized continuation remain intact; no failure is erased.\n\nBoth new paper193 original-only INITIAL packets are included as opaque byte/mode evidence: ADV38files/1childdir and SCOPE INITIAL28/1, plus stable scope parent and source61/13. Their mathematical reports, derivations and mechanisms were not semantically read or assessed by this checkpoint task. Individual physical modes, all hidden/empty objects and actual ignore boundaries were retained; this checkpoint gives no new scientific verdict on193. Only the actual active Fano editorial directory and this own directory were excluded.\n\nScientific review146/203='+format(percent,'.6f')+'%,138PASS/8deferred/57remaining. Native Sheet remains145 pending the later root transition:123verified/10deployed/4preparing/6under review/50queued/2holds/8deferred. Programme active/incomplete; finite checkpoint100% complete. No production helper mode, scientific source, native index refresh/status/reset/checkout, website/Sheet operation, release or outside contact was executed.\n'
with (OWN/'REPORT.md').open('x') as f:f.write(report)
with (OWN/'CHECKPOINT_LOG.md').open('a') as f:f.write('\n'+now+' — Actual remote/parent/tree/changedblobs/modes/159siblings/docs/closures/nativepublic guards all0. Ownonly seal; checkpoint100%; scientific146/203='+format(percent,'.6f')+'%, native145; programme active/incomplete.\n')
for n in ['MANIFEST.json','FINAL.json']:
 with (OWN/n).open('x') as f:f.write('{}\n')
files={}
for p in sorted(OWN.rglob('*')):
 assert p.is_file() and not p.is_symlink()
 if p.name not in ['MANIFEST.json','FINAL.json']:files[p.relative_to(OWN).as_posix()]=pin(p)
manifest=dict(UTC=now,root=str(OWN),root_mode=format(stat.S_IMODE(OWN.stat().st_mode),'04o'),regular_files=len(files)+2,child_directories=0,payload_files=[dict(path=n,**p,empty=p['bytes']==0,hidden=any(x.startswith('.') for x in Path(n).parts)) for n,p in files.items()],exact_existing_terminal_recursive_hash_exclusions=['MANIFEST.json','FINAL.json'],terminal_modes={n:format(stat.S_IMODE((OWN/n).stat().st_mode),'04o') for n in ['MANIFEST.json','FINAL.json']},other_exclusions=[])
(OWN/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
final=dict(UTC=now,status='SCOPED_CHECKPOINT_PUSHED_VERIFIED',commit=pr['commit'],parent=parent,tree=pr['tree'],files=manifest['regular_files'],child_directories=0,manifest=pin(OWN/'MANIFEST.json'),all_payloads_verified=True,checkpoint_completion_percent=100,overall_scientific_review_percent=percent,native_Sheet_reviewed=145,programme_goal_active_incomplete=True,no_current_P_W_reads_by_sealer=True)
(OWN/'FINAL.json').write_text(json.dumps(final,indent=2)+'\n')
for n,p in files.items():assert pin(OWN/n)==p,n
assert pin(OWN/'MANIFEST.json')==final['manifest'] and {p.relative_to(OWN).as_posix() for p in OWN.rglob('*')}==set(files)|{'MANIFEST.json','FINAL.json'}
print(json.dumps(final))
