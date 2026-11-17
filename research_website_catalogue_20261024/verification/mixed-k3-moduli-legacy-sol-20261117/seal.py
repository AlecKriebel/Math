"""Finite passive identity closure; no source programs, old helpers, network or website access."""
import base64, datetime, hashlib, json, os, posixpath, stat, subprocess
from pathlib import Path

M=Path('/Users/alec/Documents/Math')
P=M/'research_website_catalogue_20261024'
OWN=P/'verification/mixed-k3-moduli-legacy-sol-20261117'
TERMINALS={'MANIFEST.json','FINAL.json'}
def read(n):return json.loads((OWN/n).read_bytes())
def write(n,data):
    with (OWN/n).open('x') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')
def pin(p):
    a=p.lstat();assert stat.S_ISREG(a.st_mode) and not p.is_symlink()
    raw=p.read_bytes();z=p.lstat()
    fields=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mode,s.st_mtime_ns,s.st_ctime_ns)
    assert fields(a)==fields(z) and len(raw)==z.st_size
    return dict(bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest(),MD5=hashlib.md5(raw).hexdigest(),mode=oct(stat.S_IMODE(a.st_mode)))
def census(root):
    files,dirs={},{'.':oct(stat.S_IMODE(root.lstat().st_mode))};pending=[root]
    while pending:
        here=pending.pop();a=here.lstat();assert stat.S_ISDIR(a.st_mode) and not here.is_symlink()
        for p in sorted(here.iterdir()):
            rel=p.relative_to(root).as_posix();s=p.lstat();assert not p.is_symlink()
            if stat.S_ISDIR(s.st_mode):dirs[rel]=oct(stat.S_IMODE(s.st_mode));pending.append(p)
            else:files[rel]=pin(p)
        z=here.lstat();assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_mtime_ns,z.st_ctime_ns)
    return dict(root=str(root),root_mode=dirs['.'],files=files,directories={n:m for n,m in dirs.items() if n!='.'},hidden_paths=[n for n in sorted(set(files)|set(dirs)) if n!='.' and any(x.startswith('.') for x in n.split('/'))],empty_files=[n for n,x in sorted(files.items()) if x['bytes']==0],empty_directories=[n for n in sorted(dirs) if n!='.' and not any(q.startswith(n+'/') for q in set(files)|set(dirs))])
assert not any((OWN/n).exists() for n in TERMINALS)
execution=read('EXECUTION.json');audit=read('AUDIT_RESULT.json')
assert execution['exit_code']==0 and execution['attempt']==1 and execution['stderr_bytes']==0
assert pin(OWN/'audit_identity.py')['SHA256']==execution['fully_read_saved_auditor_SHA256']
assert audit['no_W_access'] and audit['all_native_M_docs_source_writer_guards_exact']
assert all(n==0 for row in audit['all_exact_search_counts'].values() for n in row.values())
assert all(n==0 for row in audit['all_whole_target_asset_match_counts'].values() for n in row.values())
search=read('SEARCH_AND_ASSET_IDENTITIES.json');differences=read('SNAPSHOTS_AND_DIFFERENCES.json')
candidates=read('CANDIDATE_READING_LIST.json')['candidates']
reasons={
 'docs/papers/gamma-theta-order-13-k3/index.html':'Different citation title and source project gamma_theta_eternal_domination; k3 in its slug is not a K3-moduli identity.',
 'docs/papers/hadamard-668-repair-obstructions/index.html':'Different Hadamard citation title and explicit source path hadamard_668_search; moduli is only a shared word.',
 'docs/papers/k3p-theta-trinet-collision/index.html':'Different K3P citation title and explicit source project k2p_k3p_theta_trinet_collision; the letter sequence does not identify this K3-moduli note.',
 'docs/papers/s-tc-jc-sharp-boundary/index.html':'Different Jukes–Cantor citation title and explicit source path s_tc_jc_landmark_closure/s_tc_jc_sharp_boundary; its K3P mention does not identify this note.'}
assert {x['path'] for x in candidates}==set(reasons)
unique={};dispositions=[]
for row in candidates:
    actual=pin(OWN/row['saved_file']);assert actual['SHA256']==row['whole_article_SHA256'] and actual['bytes']==row['whole_article_bytes']
    assert not row['exact_identity_hits']
    unique.setdefault(actual['SHA256'],[]).append(row['saved_file'])
    local_assets={}
    records=search['views'][row['view']]['all_whole_file_identities']
    for link in row['asset_and_source_links']:
        if not link.startswith(('http:','https:','#','/')):
            path=posixpath.normpath(posixpath.join(posixpath.dirname(row['path']),link.split('#',1)[0]))
            if path in records:
                local_assets[path]=records[path]
                assert all(records[path]['SHA256']!=target['SHA256'] for target in search['target_whole_assets'].values())
    dispositions.append(dict(**row,personally_read_entire_distinct_body=True,duplicate_whole_body_identity_verified=True,genuine_correspondence=False,identity_reason=reasons[row['path']],linked_local_asset_identities=local_assets,explicit_source_links=[u for u in row['asset_and_source_links'] if u.startswith('https://github.com/')]))
assert len(unique)==4 and len(candidates)==11
write('CANDIDATE_DISPOSITIONS.json',dict(schema='whole-read-legacy-candidate-dispositions-v1',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),distinct_bodies_personally_read_in_full=4,occurrences=11,whole_body_equivalence_groups=unique,dispositions=dispositions,scope='Identity and association only; no scientific re-evaluation of these other works'))
before,after=read('GUARDS_BEFORE.json'),read('GUARDS_AFTER.json');assert before==after
final={k:census(Path(before[k]['root'])) for k in ('physical_docs','sources','writer')}
expected=before['native_M'];nativefiles={}
for n,value in expected['files'].items():
    p=Path(value['path']);fresh=dict(path=str(p),exists=p.exists())
    if p.exists():
        fresh.update(pin(p))
        if n=='HEAD':fresh['raw_base64']=base64.b64encode(p.read_bytes()).decode()
    assert fresh==value;nativefiles[n]=fresh
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
for n in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_COMMON_DIR','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES'):env.pop(n,None)
calls=[]
def git(*args):
    argv=['/usr/bin/git','--no-optional-locks','-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','gc.auto=0',*args]
    r=subprocess.run(argv,cwd=M,env=env,capture_output=True,check=False);name='raw/final-git-'+str(len(calls))
    for suffix,raw in (('stdout',r.stdout),('stderr',r.stderr)):
        with (OWN/(name+'.'+suffix+'.bin')).open('xb') as f:f.write(raw)
    calls.append(dict(argv=argv,exit_code=r.returncode,stdout=name+'.stdout.bin',stderr=name+'.stderr.bin'))
    assert r.returncode==0,r.stderr.decode(errors='replace')
    return r.stdout.decode()
native=dict(files=nativefiles,HEAD=git('rev-parse','HEAD').strip(),branch=git('branch','--show-current').strip(),logical_local_heads=git('for-each-ref','--format=%(refname)%00%(objectname)%00%(objecttype)','refs/heads'),loose_local_heads=census(Path(expected['loose_local_heads']['root'])))
final['native_M']=native;assert final==before
finalrefs=git('rev-parse','HEAD','refs/heads/main','refs/remotes/origin/main').splitlines()
write('GUARDS_FINAL.json',dict(guards=final,refs_observed_last=finalrefs,Git_calls=calls,exact_protected_boundary=True,remote_tracking_ref_is_observed_not_network_verified=True))
writerroot=Path(final['writer']['root']);wm=json.loads((writerroot/'MANIFEST.json').read_bytes())
payload={x['path']:{k:v for k,v in x.items() if k!='path'} for x in wm['payload_files']}
assert payload=={n:x for n,x in final['writer']['files'].items() if n not in ('MANIFEST.json','FINAL.json')}
assert {x['path']:x['mode'] for x in wm['directories']}==final['writer']['directories'] and wm['root_mode']==final['writer']['root_mode']
frozen_source=json.loads((writerroot/'SOURCE_GUARDS_FINAL.json').read_bytes())
assert frozen_source['files']==final['sources']['files'] and {n:v for n,v in frozen_source['directories'].items() if n!='.'}==final['sources']['directories']
assert frozen_source['directories']['.']==final['sources']['root_mode']
assert all(frozen_source[n]==final['sources'][n] for n in ('hidden_paths','empty_files','empty_directories'))
for n,value in audit['root_inputs'].items():assert pin(P/n)==value
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
diff_summary={k:dict(count=len(v),paths=[x['path'] for x in v]) for k,v in differences['differences'].items()}
write('FINAL_CHECKS.json',dict(UTC=utc,status='NO_GENUINE_CORRESPONDENCE_IDENTIFIED_IN_BOUNDED_VIEWS',record_id='23204176',exact_search_counts=audit['all_exact_search_counts'],whole_asset_match_counts=audit['all_whole_target_asset_match_counts'],candidate_occurrences=11,distinct_whole_articles_read=4,physical_docs_files_childdirs=[len(final['physical_docs']['files']),len(final['physical_docs']['directories'])],native_released_files=[audit['native_files'],audit['released_files']],native_M_index=final['native_M']['files']['index'],source_files_childdirs=[43,7],writer_files_childdirs=[28,1],all_guarded_bytes_modes_topology_exact=True,writer_manifest_all_payloads_exact=True,source_equal_frozen_writer_authenticated_full_source_guard=True,snapshot_differences=diff_summary,refs_before=audit['refs_before'],refs_after_audit=audit['refs_after'],refs_last=finalrefs,no_W_access=True,no_network=True,canonical_url=None,redirect_target=None,completion_percent=100))
report='''# Bounded legacy correspondence: record 23204176

No genuine corresponding legacy GitHub Pages article was identified in the three inspected views: current physical Math/docs, native main a4ce3c37dad209339e490d18dcced6c48cf912d2:docs, and root-supplied released commit 15482acd0ef864af280a864758b2ac6aa24dfbe8:docs. Native docs tree 6ccfd5ab446400dc7fb3933dcc2e374cb415fa90 and released docs tree e63ba1f227e5aa2f0e06fd6a52b36afa1531a4d0 differ intentionally; their complete finite difference maps are retained.

The physical census includes 257 files, including hidden entries; each Git snapshot has 254 blob leaves. Every body of the 260 unique Git blob objects was authenticated against its Git OID. Exact record/DOI/title/proposed-slug searches found zero matches in UTF-8 text and normalized HTML in all three views. Whole-file size/SHA256 comparison found no copy of either original native asset in any view: the 67,264-byte outer PDF, SHA256 483a6edff90202ef4d31560049a32ce946dcd1c6a999ab5b1f25b66a8f326612, or 135,014-byte source ZIP, SHA256 8f44cd5f9c447e40a97a07a3bcc62998accdb7aad4fce94b4020c5fe87f77ce0.

Eleven candidate occurrences comprise four distinct article bodies, all personally read completely. They have different citation titles, explicit other source-project associations and different linked asset identities. K3-containing filenames, K3P mentions and the shared word moduli are false identity matches. CANDIDATE_DISPOSITIONS.json retains each full candidate's identity, linked local-asset identities and explicit source links. Those other works were not scientifically rejudged.

The complete physical docs namespace, native M HEAD/index/config/config.worktree and logical/loose local branch heads, source 43 files/7 child directories, and frozen writer 28 files/1 child directory match before/after/final, including bytes, modes and hidden/empty topology. The writer's complete actual payload also matches its frozen manifest, and source bytes match its authenticated final source guard. Actual refs are recorded first and last. The released commit is supplied by root and matches the observed local remote-tracking ref; no network-fresh remote or live-site assertion is made. Literal passive invocation, streams, metadata Git streams, tree maps and all file identities are retained; the large cat-file blob stream is hash-bound rather than duplicated as a cache.

The checkpoint hold was honored before this new lane was created. This task made no W access, Git/source/writer mutation, network query, scientific-program import/execution, Sheet/status update, live verification, redirect, outreach or production action. The current private proposed slug remains a proposal. Canonical URL and redirect target remain null. This result is bounded correspondence evidence, not global historical or live absence. Scientific clearance is inherited without a new scientific adjudication.

Completion 100% of this bounded identity task. The own finite packet is frozen, with only its exact MANIFEST/FINAL terminal self-hash pair excluded from circular hashing. No follow-on action.
'''
with (OWN/'REPORT.md').open('x') as f:f.write(report)
with (OWN/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc+' — Four distinct complete candidate bodies read and rejected on identity/source/asset association; all eleven occurrences bound by exact whole-body hashes. Complete final native M/docs/source/writer guards and frozen manifest/source binding pass. Completion100% of bounded identity task; no W access; freeze and stop.\n')
write('SEAL_EXECUTION.json',dict(UTC=utc,full_saved_seal_personally_read_before_invocation=True,passive_auditor_attempts=1,passive_auditor_exit=0,failures=[],completion_percent=100))
payload_guard=census(OWN);assert not (set(payload_guard['files'])&TERMINALS)
names=sorted(set(payload_guard['files'])|TERMINALS)
manifest=dict(schema='finite-legacy-identity-manifest-v1',UTC=utc,root=str(OWN),root_mode=payload_guard['root_mode'],payload_files=[dict(path=n,**v) for n,v in sorted(payload_guard['files'].items())],directories=[dict(path=n,mode=m) for n,m in sorted(payload_guard['directories'].items())],actual_files=len(names),actual_childdirs=len(payload_guard['directories']),hidden_paths=payload_guard['hidden_paths'],empty_files=payload_guard['empty_files'],empty_directories=payload_guard['empty_directories'],terminal_controls=[dict(path=n,mode='0o644') for n in sorted(TERMINALS)],exact_terminal_self_hash_exclusions=sorted(TERMINALS),scope='Entire own finite namespace; no hidden/empty/ignored exclusions except exact named terminal circular/self-hash pair')
write('MANIFEST.json',manifest)
write('FINAL.json',dict(schema='bounded-legacy-identity-FINAL-v1',UTC=utc,status='NO_GENUINE_CORRESPONDENCE_IDENTIFIED_IN_BOUNDED_VIEWS',completion_percent=100,record_id='23204176',root=str(OWN),root_mode=payload_guard['root_mode'],manifest=pin(OWN/'MANIFEST.json'),actual_files=len(names),actual_childdirs=len(payload_guard['directories']),whole_file_names=names,directories=manifest['directories'],terminal_self_hash_exclusions=sorted(TERMINALS),native_commit=audit['native_commit'],released_commit=audit['released_commit'],native_docs_tree='6ccfd5ab446400dc7fb3933dcc2e374cb415fa90',released_docs_tree='e63ba1f227e5aa2f0e06fd6a52b36afa1531a4d0',physical_native_released_file_counts=[257,254,254],candidate_occurrences=11,distinct_whole_article_bodies_read=4,exact_identity_or_native_whole_asset_matches=0,all_actual_native_M_docs_sources_writer_guards_exact=True,no_W_access=True,no_network_or_mutation_or_scientific_execution=True,canonical_url=None,redirect_target=None,proposed_slug_not_live_verified='mixed-k3-moduli-hodge-classes',failures=[],limits=['Only current physical docs and the two exact existing Git snapshots, not global history','UTF-8/HTML identity text plus whole native asset identities; no general semantic PDF OCR census','Released commit supplied by root and existing local remote-tracking ref; no network freshness or live absence claim','No scientific re-adjudication, website access or redirect authority'],quiescent_stop=True))
actual=census(OWN)
assert set(actual['files'])==set(names) and actual['directories']==payload_guard['directories']
assert all(actual['files'][n]==v for n,v in payload_guard['files'].items())
assert actual['files']['MANIFEST.json']==read('FINAL.json')['manifest'] and all(actual['files'][n]['mode']=='0o644' for n in TERMINALS)
print(json.dumps(dict(status='FROZEN',files=len(names),childdirs=len(actual['directories']),snapshot_difference_counts={k:v['count'] for k,v in diff_summary.items()},MANIFEST=actual['files']['MANIFEST.json'],FINAL=actual['files']['FINAL.json'])))
