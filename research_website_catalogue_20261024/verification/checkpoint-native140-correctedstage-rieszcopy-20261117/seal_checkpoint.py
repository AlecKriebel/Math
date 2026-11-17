"""Finite report/seal after an actual scoped push and independent native/public guards."""
import datetime, hashlib, json
from pathlib import Path
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P/'verification/checkpoint-native140-correctedstage-rieszcopy-20261117'
TERMINALS = {'MANIFEST.json','FINAL.json'}
def read(name):
    return json.loads((OWN/name).read_bytes())
def pin(path):
    a = path.lstat()
    assert stat.S_ISREG(a.st_mode) and not path.is_symlink()
    raw = path.read_bytes()
    z = path.lstat()
    assert (a.st_dev,a.st_ino,a.st_size,a.st_mode,a.st_mtime_ns,a.st_ctime_ns) == (z.st_dev,z.st_ino,z.st_size,z.st_mode,z.st_mtime_ns,z.st_ctime_ns)
    return dict(bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest(),mode=oct(stat.S_IMODE(z.st_mode)))
def census():
    files,dirs = {},{}
    for p in sorted(OWN.rglob('*')):
        assert not p.is_symlink()
        rel = p.relative_to(OWN).as_posix()
        if p.is_dir():
            dirs[rel] = oct(stat.S_IMODE(p.stat().st_mode))
        else:
            files[rel] = pin(p)
    return files,dirs
def write(name,value):
    with (OWN/name).open('x') as stream:
        json.dump(value,stream,indent=2)
        stream.write('\n')

before,after = read('GUARDS_BEFORE.json'),read('GUARDS_AFTER.json')
assert before['repositories'] == after['repositories'] and before['public'] == after['public']
dry,post = read('DRY_TREE_AUDIT.json'),read('POST_TREE_AUDIT.json')
push = read('PUSH.receipt.json')
invoke = read('PUSH.invocation.json')
assert invoke['exit_code'] == 0 and invoke['stderr_bytes'] == 0 and invoke['helper_unchanged']
assert post['commit'] == push['commit'] == post['fresh_remote_main'].split()[0]
assert post['tree'] == push['tree'] and post['parent'] == push['parent'] == '386463ab847f283920e746a48f52079ac8b3d735'
assert post['sibling_root_entries_preserved'] == 159 and post['docs_entry']['OID'] == 'e63ba1f227e5aa2f0e06fd6a52b36afa1531a4d0'
assert all(x['current_file_whole_bytes_equal'] or x['known_helper_receipt_drift'] for x in post['all_changed_blob_whole_bytes_verified'])
assert post['excluded_subtree_leaves_exact_at_parent'] and all(x['committed_leaves']==0 for x in post['private_caches'])
assert not any(x['path'].startswith(P.name+'/verification/'+OWN.name+'/') for x in post['changes'])
assert pin(P/'scripts/checkpoint_subtree.py')['SHA256'] == invoke['helper']['SHA256'] == '405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0'
utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
write('FINAL_CHECKS.json',dict(schema='checkpoint-full-final-checks-v1',UTC=utc,commit=post['commit'],parent=post['parent'],tree=post['tree'],changed_paths=post['changed_paths'],status_counts=post['status_counts'],sibling_root_entries=159,docs_entry=post['docs_entry'],fresh_remote_main=post['fresh_remote_main'],native_M_W_full_protected_boundary_exact=True,public_files=len(after['public']['files']),public_childdirs=len(after['public']['directories']),public_root_mode=after['public']['root_mode'],whole_changed_blobs_modes_verified=len(post['all_changed_blob_whole_bytes_verified']),packet_committed_leaf_counts=post['packet_committed_leaf_counts'],actual_existing_push_exclusions=invoke['excluded_actual_directories'],dry_tree=dry['tree'],actual_push_tree_equals_dry=post['tree']==dry['tree'],important_committed_blob_identities=post['important_committed_blob_identities'],helper_full_source_read=True,helper_unchanged=True,dry_attempts=1,push_attempts=1,force_push=False,releases_or_Zenodo_actions=0,website_or_Sheet_or_science_actions=0,substantive_failures=[]))
report = '# Scoped programme checkpoint\n\nOrdinary push succeeded: commit '+post['commit']+', parent '+post['parent']+', tree '+post['tree']+'. The actual diff is '+str(post['changed_paths'])+' programme-only paths. It preserves every one of the159 sibling root entries, including docs tree e63ba1f227e5aa2f0e06fd6a52b36afa1531a4d0, with exact mode/type/OID equality. NativeM intentionally remains at its own earlier mainHEAD; preservation is against the remote parent for sibling trees, not a replacement by native docs.\n\nThe helper was personally read in full94lines, never invoked with --help or imported, and ran once dry and once for the ordinary nonforce push. Literal helper streams, argv, timings and exit codes are retained. Its internal programme index is distinct from the independently guarded actual25854746-byte M index. No externalGIT_DIR bootstrap was created. Successful helper Git subprocess streams are captured internally by the supplied helper; the retained outer streams are its literal complete stdout/stderr, not an invented per-command transcript.\n\nIndependent postchecks bind actual commit headers, one parent, author/committer Alec Kriebel <me@aleckriebel.com>, actual tree, fullpathlist, all changed blob contents/modes, fresh remote main, and important frozen packet/control identities. Riesz writer28, fact17 and legacy113 committed leaves, corrected-stage control files, native tracker140/reconciliation and the saved partial row191 state are included. Original row191 primary-reading/compiler caches and corrected-stage full website clones remain gitignored and absent from the commit; no papers subtree was excluded. The final push tree is reported as observed and is not assumed equal to the dry tree.\n\nEvery active exclusion was an actually existing ordinary directory immediately before its invocation. Root subsequently authorized the new production-audit lane; it already existed at the final namespace check, so this task created no content or directory there. The continuation audit and production audit were excluded from the push. Already-excluded frozen corrected-audit/production-preparation lanes were left at their parent state. Own evidence is also excluded, so this final audit packet itself is local and will need a later ordinary checkpoint if desired.\n\nFull nativeM/W HEAD/index/config/config.worktree and all logical/loose LOCAL branch heads match before/after. The entire actual W/public781files/377childdirs, including rootmode0750, hidden files, empty entries, bytes and all modes/topology, matches. FETCH_HEAD, remote-tracking refs and object database additions are expressly outside equality under the root clarification; they are normal helper fetch/push effects. No website installation/deployment, source-science execution, Sheet/AA change, release, Zenodo or external outreach occurred.\n\nCompletion100% of the authorized checkpoint task. This report makes no new scientific or live-publication claim. No autonomous follow-on action.\n'
with (OWN/'REPORT.md').open('x') as stream:
    stream.write(report)
with (OWN/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n'+utc+' — One ordinarypush and completepostchecks succeeded. Actualcommit'+post['commit']+', tree'+post['tree']+', '+str(post['changed_paths'])+'scopedpaths;159siblings/docs and allnativeM/W/localheads+completeWpublic exact. Completion100% ofcheckpoint; finalfinitepacket frozen; stop.\n')
write('READ_ATTESTATION.json',dict(schema='checkpoint-owned-and-helper-full-source-reads-v1',UTC=utc,full_actual_helper_personally_read=True,helper=pin(P/'scripts/checkpoint_subtree.py'),owned_scripts={p.name:pin(p) for p in sorted(OWN.glob('*.py'))},all_owned_sources_personally_read_before_their_invocations=True,run_helper_invoker_change_between_dry_push='Only named production-audit directory added to existing-directory discovery at explicit root instruction; helper unchanged; full invoker reread beforepush',no_substantive_failure_or_retry=True))
files,dirs = census()
assert not(set(files)&TERMINALS)
names = sorted(set(files)|TERMINALS)
manifest = dict(schema='finite-scoped-checkpoint-manifest-v1',UTC=utc,root=str(OWN),root_mode=oct(stat.S_IMODE(OWN.stat().st_mode)),payload_files=[dict(path=p,**v) for p,v in sorted(files.items())],directories=[dict(path=p,mode=m) for p,m in sorted(dirs.items())],actual_file_count=len(names),actual_child_directory_count=len(dirs),terminal_control_topology=[dict(path=p,mode='0o644') for p in sorted(TERMINALS)],exact_terminal_self_hash_exclusions=sorted(TERMINALS),hidden_paths=[p for p in sorted(set(files)|set(dirs)) if any(x.startswith('.') for x in p.split('/'))],empty_files=[p for p,v in sorted(files.items()) if v['bytes']==0],empty_directories=[p for p in sorted(dirs) if not any(q.startswith(p+'/') for q in set(files)|set(dirs))],scope='Complete finite own namespace, no hidden/empty/ignored exclusions; exact named terminal self/circular pair only')
write('MANIFEST.json',manifest)
write('FINAL.json',dict(schema='scoped-checkpoint-FINAL-v1',UTC=utc,status='PUSHED_AND_INDEPENDENTLY_POSTVERIFIED',completion_percent=100,commit=post['commit'],parent=post['parent'],tree=post['tree'],changed_paths=post['changed_paths'],siblings_preserved=159,docs_preserved=post['docs_entry'],native_M_W_local_HEAD_index_config_localheads_exact=True,complete_W_public_exact=True,website_files_dirs=[781,377],dry_run_exit=0,push_exit=0,ordinary_nonforce_push=True,fresh_remote_main=post['fresh_remote_main'],no_release_or_Zenodo=True,science_website_Sheet_actions=0,failures=[],own_packet_not_in_this_commit=True,root=str(OWN),root_mode=manifest['root_mode'],manifest=pin(OWN/'MANIFEST.json'),whole_namespace_files=names,directories=manifest['directories'],terminal_self_hash_exclusions=sorted(TERMINALS),scope_limits=['FETCH_HEAD/remote-tracking refs/object additions allowed helper effects, outside native protected equality','Own checkpoint packet excluded from this commit','No new scientific/live/deployment claim'],quiescent_stop=True))
actual,actual_dirs = census()
assert set(actual)==set(names) and actual_dirs==dirs
assert all(actual[p]==v for p,v in files.items())
assert actual['MANIFEST.json']==read('FINAL.json')['manifest']
print(json.dumps(dict(status='FROZEN',commit=post['commit'],tree=post['tree'],paths=post['changed_paths'],files=len(names),dirs=len(dirs),manifest=actual['MANIFEST.json'],FINAL=actual['FINAL.json'])))
