"""One data-reader invocation, literal receipt, and own-only finite sealing."""
import datetime,hashlib,json,stat,subprocess,sys,time
from pathlib import Path
if not __debug__:
    raise RuntimeError('Custody assertions must remain enabled')
OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/pentagon-root-custody-sol-20261117')
def sha(body):return hashlib.sha256(body).hexdigest()
def pin(path):
    a=path.lstat();assert stat.S_ISREG(a.st_mode) and not path.is_symlink()
    body=path.read_bytes();z=path.lstat()
    assert (a.st_dev,a.st_ino,a.st_mode,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
    return dict(bytes=len(body),SHA256=sha(body),mode=format(stat.S_IMODE(z.st_mode),'04o'))
for name in ['EXECUTION.json','reader.stdout','reader.stderr','DATA_AUTHENTICATION.json','REPORT.md','MANIFEST.json','FINAL.json']:
    assert not (OWN/name).exists(),name
sources={n:pin(OWN/n) for n in ['data_reader.py','run_once_and_seal.py']}
argv=[sys.executable,'-B',str(OWN/'data_reader.py')]
started=datetime.datetime.now(datetime.timezone.utc).isoformat();tick=time.monotonic()
r=subprocess.run(argv,cwd=OWN,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
for name,body in [('reader.stdout',r.stdout),('reader.stderr',r.stderr)]:
    with (OWN/name).open('xb') as f:f.write(body)
receipt=dict(started_UTC=started,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-tick,argv=argv,exit_code=r.returncode,actual_data_reader_invocations=1,automatic_retry_forbidden=True,literal_stdout=pin(OWN/'reader.stdout'),literal_stderr=pin(OWN/'reader.stderr'),full_saved_sources_personally_read_before_first_invocation=sources,new_scientific_executions=0)
with (OWN/'EXECUTION.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
assert sources=={n:pin(OWN/n) for n in sources}
if r.returncode:
    print(r.stdout.decode(errors='replace'));print(r.stderr.decode(errors='replace'),file=sys.stderr)
    raise SystemExit(r.returncode)
d=json.loads((OWN/'DATA_AUTHENTICATION.json').read_bytes())
assert d['whole_before_after_equal'] is True and d['fixed_extent']==dict(files=242,child_directories=15,roots=4)
report='''# Frozen pentagon data custody

All four fixed namespaces authenticated: source97files/7childdirs, rootINITIAL17/1, adversarial47/4 and scope81/3, totaling242files/15childdirs. Every actual hidden, ignored and empty file, whole bytes, filesystem mode and directory topology was included; before/after snapshots are identical. All eight externally pinned controls and each original manifest format were checked. Original terminal recursion markers were honored exactly. Declared per-file modes, explicit scope-wide mode declarations and observed otherwise undeclared terminal/directory modes are distinguished in the data receipt.

The adversarial route has an8484-byte isolated arithmetic copy equal to the actual source. Its historical one-invocation/exit0 receipt and1669-byte stdout/empty stderr authenticate, and its entire parsed JSON equals the actual published arithmetic expectation. The scope route is recorded as direct-source geometry execution: actual source6420bytes, with no isolated geometry copy present or claimed. Its historical one-invocation/exit0 receipt and3177-byte stdout/empty stderr authenticate. Removing only anchored UTC metadata yields1715bytes exactly equal to the actual published geometry expectation. The recorded97-file source checksums and105 topology entries before/after agree with current source bytes and modes. Recorded commands and literal stream hashes are retained.

This is a passive custody check, not a scientific replay or new mathematical verdict. Only the two recorded routes are authenticated; no other scripts, variants or all-suite reproduction are claimed. Frozen original lookup/dependency/reading errors remain retained and are not described as clean probes. No source code was imported, parsed as an AST, compiled or executed. No current root continuation, progress, website, Git, Sheet, network or unfinished challenge was read or changed.

Finite custody task100% complete. Programme review remains144/203=70.935961%; the research programme remains active and incomplete.
'''
with (OWN/'REPORT.md').open('x') as f:f.write(report)
with (OWN/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+receipt['finished_UTC']+' — One fully saved/read passive datareader returned0; literal stdout/stderr retained. Fixed242/15 authenticated against eight external controls and heterogeneous manifests; before/after wholebytes/modes/topology exact. Historical arithmetic parsed output and geometry normalized1715-byte output match actual published expectations. Scope direct-source route qualified; no isolated copy fabricated. Finite custody100%; scientific review144/203=70.935961%, programme active/incomplete; no new scientific verdict.\n')
for name in ['MANIFEST.json','FINAL.json']:
    with (OWN/name).open('x') as f:f.write('{}\n')
files={};dirs={}
for path in sorted(OWN.rglob('*')):
    rel=path.relative_to(OWN).as_posix();assert not path.is_symlink()
    if path.is_dir():dirs[rel]=format(stat.S_IMODE(path.lstat().st_mode),'04o')
    elif rel not in ['MANIFEST.json','FINAL.json']:files[rel]=pin(path)
assert dirs=={}
manifest=dict(schema='finite-pentagon-data-custody-manifest-v1',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),root=str(OWN),root_mode=format(stat.S_IMODE(OWN.stat().st_mode),'04o'),regular_files=len(files)+2,child_directories=0,payload_files=[dict(path=n,**p,empty=p['bytes']==0,hidden=any(x.startswith('.') for x in Path(n).parts)) for n,p in sorted(files.items())],directories=[],exact_existing_terminal_recursive_hash_exclusions=['MANIFEST.json','FINAL.json'],terminal_modes={n:format(stat.S_IMODE((OWN/n).stat().st_mode),'04o') for n in ['MANIFEST.json','FINAL.json']},other_exclusions=[],all_hidden_empty_bytes_modes_topology_included=True)
(OWN/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
final=dict(schema='pentagon-root-custody-final-v1',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS_DATA_CUSTODY_ONLY',protected_extent=d['fixed_extent'],own_files=manifest['regular_files'],own_child_directories=0,manifest=pin(OWN/'MANIFEST.json'),data_authentication=pin(OWN/'DATA_AUTHENTICATION.json'),data_reader_exit=0,new_scientific_executions=0,new_scientific_verdict=False,completion_percent=100,programme_goal_active_incomplete=True)
(OWN/'FINAL.json').write_text(json.dumps(final,indent=2)+'\n')
assert {p.relative_to(OWN).as_posix() for p in OWN.rglob('*') if p.is_file()}==set(files)|{'MANIFEST.json','FINAL.json'}
for name,expected in files.items():assert pin(OWN/name)==expected,name
assert pin(OWN/'MANIFEST.json')==final['manifest']
print(json.dumps(final))
