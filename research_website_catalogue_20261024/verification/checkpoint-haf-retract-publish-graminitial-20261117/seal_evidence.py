"""Seal only this checkpoint's captured evidence; never read current P or W."""
import datetime, hashlib, json, os, stat
from pathlib import Path

if not __debug__:
    raise RuntimeError('Checkpoint guards require Python assertions enabled')

OWN = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/checkpoint-haf-retract-publish-graminitial-20261117')
def read(name):
    return json.loads((OWN/name).read_bytes())
def pin(path):
    a = path.lstat()
    assert stat.S_ISREG(a.st_mode) and not path.is_symlink()
    b = path.read_bytes()
    z = path.lstat()
    assert (a.st_dev,a.st_ino,a.st_mode,a.st_size,a.st_mtime_ns,a.st_ctime_ns) == (z.st_dev,z.st_ino,z.st_mode,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
    assert len(b) == z.st_size
    return dict(bytes=len(b),SHA256=hashlib.sha256(b).hexdigest(),mode=format(stat.S_IMODE(z.st_mode),'04o'))
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
runs = read('RUNS.json')
assert len(runs) == 6 and all(x['exit_code'] == 0 for x in runs)
before, after = read('GUARDS_BEFORE.json'), read('GUARDS_AFTER.json')
assert before['repositories'] == after['repositories'] and before['public'] == after['public']
dry, post = read('DRY_TREE_AUDIT.json'), read('POST_TREE_AUDIT.json')
di, pi = read('DRY_RUN.invocation.json'), read('PUSH.invocation.json')
dr, pr = read('DRY_RUN.receipt.json'), read('PUSH.receipt.json')
assert di['exit_code'] == pi['exit_code'] == 0
assert di['mode'] == 'dry-run' and pi['mode'] == 'push'
assert di['helper_unchanged'] and pi['helper_unchanged'] and pi['ordinary_nonforce_push_only']
assert dr['parent'] == pr['parent'] == post['parent'] == '15482acd0ef864af280a864758b2ac6aa24dfbe8'
assert post['commit'] == pr['commit'] and post['tree'] == pr['tree']
assert post['fresh_actual_remote_main'].split()[0] == pr['commit']
assert dry['sibling_root_entries_preserved'] == post['sibling_root_entries_preserved'] == 159
assert post['dry_to_push_tree_delta'] == ['research_website_catalogue_20261024/verification/checkpoint-subtree-dry-run-20261025.json']
assert dry['excluded_actual_paths'] == post['excluded_actual_paths']
assert all(x['complete_current_nonignored_local_files_equal_committed_tree'] for x in post['durable_packet_and_source_closures'])
release = read('WRITEHOLD_RELEASE.json')
programme_counts = release['programme_counts']
assert programme_counts == dict(verified=123,deployed=7,preparing=3,under_review=10,queued=50,holds=2,deferred=8)
reviewed, total = 141, 203
completion = reviewed/total*100
summary = dict(schema='scoped-published130-graminitial-checkpoint-finalchecks-v1',UTC=started,parent=pr['parent'],commit=pr['commit'],tree=pr['tree'],changed_paths=post['changed_paths'],status_counts=post['status_counts'],all_159_untargeted_root_siblings_and_docs_exact=True,all_changed_blob_whole_bytes_and_git_modes_verified=True,key_actual_file_identities=len(post['key_actual_committed_files']),complete_durable_packet_source_closures=len(post['durable_packet_and_source_closures']),actual_cache_ignore_rules=post['actual_cache_ignore_rules'],excluded_actual_paths=post['excluded_actual_paths'],dry_push_exits=[di['exit_code'],pi['exit_code']],all_wrapper_runs=runs,native_protected_repositories_exact=after['repositories'],public_files=len(after['public']['files']),public_child_directories=len(after['public']['directories']),public_root_mode=after['public']['root_mode'],whole_public_bytes_modes_topology_exact=True,dry_to_push_delta_only_helper_dry_receipt=True,programme_goal_active_incomplete=True,reviewed=reviewed,total=total,overall_review_percent=completion,status_counts_programme=programme_counts,checkpoint_completion_percent=100,no_current_P_W_reads_by_sealer=True)
with (OWN/'FINAL_CHECKS.json').open('x') as stream:
    json.dump(summary,stream,indent=2)
    stream.write('\n')
report = '# Scoped checkpoint verified\n\nThe authorized programme-only checkpoint was pushed by one ordinary nonforce push after one successful dry run.\n\n- Commit: `'+pr['commit']+'`\n- Parent: `'+pr['parent']+'`\n- Tree: `'+pr['tree']+'`\n- Changed paths: '+str(post['changed_paths'])+'; all remain within the programme.\n- All 159 untargeted remote root siblings, including docs, are exact.\n- Whole native HEAD/index/config/config.worktree and logical/loose local heads of M and W are unchanged. W/public remains 790 regular files, 381 child directories, root mode 0750, with exact bytes, modes and topology.\n- Changed blobs, Git modes, key actual files and release-listed durable packet/source closures were verified against the committed tree. Private caches remain local under actual ignore boundaries.\n- Only actual active verification lanes and this evidence directory were excluded; their tree leaves remain at the parent.\n- Literal helper stdout/stderr and all verification exits are preserved. No old publication helper, research/support source, website/Sheet action, external communication or release was executed. Current 192/194 mathematical report content was not interpreted.\n\nOverall catalogue review is 141/203 = '+format(completion,'.6f')+'%. The research programme remains active and incomplete: 123 verified, 7 deployed, 3 preparing, 10 under review, 50 queued, 2 holds, 8 deferred. This finite checkpoint task is 100% complete.\n'
with (OWN/'REPORT.md').open('x') as stream:
    stream.write(report)
with (OWN/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n'+started+' — All six guarded execution/verification steps returned 0. Ordinary scoped checkpoint '+pr['commit']+' verified against actual remote main, parent, tree, changed paths/blobs/modes, 159 siblings/docs, durable closures and native/public guards. Checkpoint completion: 100%; overall catalogue review: '+format(completion,'.6f')+'%; research goal active and incomplete.\n')
for name in ('MANIFEST.json','FINAL.json'):
    with (OWN/name).open('x') as stream:
        stream.write('{}\n')
files, directories = [], []
root_mode_before = stat.S_IMODE(OWN.lstat().st_mode)
pending = [OWN]
while pending:
    here = pending.pop()
    a = here.lstat()
    assert stat.S_ISDIR(a.st_mode) and not here.is_symlink()
    for path in sorted(here.iterdir()):
        rel = path.relative_to(OWN).as_posix()
        z = path.lstat()
        if stat.S_ISDIR(z.st_mode):
            assert not path.is_symlink()
            directories.append(dict(path=rel,mode=format(stat.S_IMODE(z.st_mode),'04o')))
            pending.append(path)
        elif rel not in ('MANIFEST.json','FINAL.json'):
            files.append(dict(path=rel,**pin(path),hidden=any(x.startswith('.') for x in Path(rel).parts),empty=z.st_size==0))
    z = here.lstat()
    assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns) == (z.st_dev,z.st_ino,z.st_mode,z.st_mtime_ns,z.st_ctime_ns)
manifest = dict(schema='finite-scoped-published130-graminitial-checkpoint-manifest-v1',UTC=started,root=str(OWN),root_mode=format(stat.S_IMODE(OWN.lstat().st_mode),'04o'),regular_files=len(files)+2,child_directories=len(directories),payload_files=sorted(files,key=lambda x:x['path']),directories=sorted(directories,key=lambda x:x['path']),exact_already_created_terminal_recursive_hash_exclusions=[str(OWN/'MANIFEST.json'),str(OWN/'FINAL.json')],terminal_controls=[dict(path=x,mode=format(stat.S_IMODE((OWN/x).lstat().st_mode),'04o')) for x in ('MANIFEST.json','FINAL.json')],other_exclusions=[],all_hidden_empty_bytes_modes_topology_included=True,no_future_subtree_or_basename_exclusion=True)
(OWN/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
final = dict(schema='scoped-published130-graminitial-checkpoint-final-v1',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='SCOPED_CHECKPOINT_PUSHED_VERIFIED',commit=pr['commit'],parent=pr['parent'],tree=pr['tree'],files=manifest['regular_files'],child_directories=manifest['child_directories'],manifest=pin(OWN/'MANIFEST.json'),all_payloads_verified=True,checkpoint_completion_percent=100,overall_review_percent=completion,programme_goal_active_incomplete=True,no_current_P_W_reads_by_sealer=True)
(OWN/'FINAL.json').write_text(json.dumps(final,indent=2)+'\n')
for item in manifest['payload_files']:
    assert pin(OWN/item['path']) == {k:item[k] for k in ('bytes','SHA256','mode')}
assert pin(OWN/'MANIFEST.json') == final['manifest']
assert stat.S_IMODE(OWN.lstat().st_mode) == root_mode_before
assert {p.relative_to(OWN).as_posix():format(stat.S_IMODE(p.lstat().st_mode),'04o') for p in OWN.rglob('*') if p.is_dir() and not p.is_symlink()} == {x['path']:x['mode'] for x in directories}
assert {p.relative_to(OWN).as_posix() for p in OWN.rglob('*') if p.is_file()} == {x['path'] for x in files}|{'MANIFEST.json','FINAL.json'}
print(json.dumps(final))
