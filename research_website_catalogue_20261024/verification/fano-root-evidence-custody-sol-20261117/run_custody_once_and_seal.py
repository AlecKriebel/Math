"""One saved main custody invocation; retain administrative history and seal own only."""
from pathlib import Path
import datetime,hashlib,json,stat,subprocess,sys,time
if not __debug__:raise RuntimeError('Assertions required')
OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/fano-root-evidence-custody-sol-20261117')
def pin(p):
 a=p.lstat();assert stat.S_ISREG(a.st_mode) and not p.is_symlink();b=p.read_bytes();z=p.lstat()
 assert (a.st_dev,a.st_ino,a.st_mode,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
 return dict(bytes=len(b),SHA256=hashlib.sha256(b).hexdigest(),mode=format(stat.S_IMODE(z.st_mode),'04o'))
for n in ['MAIN_EXECUTION.json','main.stdout','main.stderr','DATA_AUTHENTICATION.json','REPORT.md','MANIFEST.json','FINAL.json']:assert not (OWN/n).exists(),n
retained_names=['schema_discovery_v1_failed.py','SCHEMA_DISCOVERY_FAILURE.stderr','SCHEMA_DISCOVERY_FAILURE.json','RESEARCH_LOG.md'];retained={n:pin(OWN/n) for n in retained_names}
assert json.loads((OWN/'SCHEMA_DISCOVERY_FAILURE.json').read_bytes())['actual_exit_code']==1
assert json.loads((OWN/'SCHEMA_DISCOVERY_V2_EXECUTION.json').read_bytes())['exit_code']==0
sources={n:pin(OWN/n) for n in ['custody_once.py','run_custody_once_and_seal.py']}
argv=[sys.executable,'-B',str(OWN/'custody_once.py')];start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();r=subprocess.run(argv,cwd=OWN,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
for n,b in [('main.stdout',r.stdout),('main.stderr',r.stderr)]:
 with (OWN/n).open('xb') as f:f.write(b)
receipt=dict(started_UTC=start,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.monotonic()-t,argv=argv,exit_code=r.returncode,main_custody_checker_invocations=1,no_automatic_retry=True,literal_stdout=pin(OWN/'main.stdout'),literal_stderr=pin(OWN/'main.stderr'),full_saved_sources_personally_read_before_invocation=sources,original_administrative_failure_artifacts_preserved=retained,V1_stdout_not_separately_captured=True)
with (OWN/'MAIN_EXECUTION.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
assert retained=={n:pin(OWN/n) for n in retained_names} and sources=={n:pin(OWN/n) for n in sources}
if r.returncode:
 print(r.stdout.decode(errors='replace'));print(r.stderr.decode(errors='replace'),file=sys.stderr);raise SystemExit(r.returncode)
d=json.loads((OWN/'DATA_AUTHENTICATION.json').read_bytes());assert d['fixed_extent']==dict(files=334,child_directories=29,roots=4) and d['whole_before_after_equal']
report='''# Fano fixed-evidence custody

Authenticated all334files and29childdirectories across native source196/21, frozen rootINITIAL18/1, adversarial67/3 and scope53/4. All hidden, ignored and empty objects, whole bytes, filesystem modes, mtimes, ctimes and topology match before/after. Twelve external control/stream pins authenticate. The source194 payload rows, rootINITIAL16 hashes plus two explicitly marked terminal entries, adversarial65 payload rows plus exact two terminals, and scope51 hashes plus two explicit marked terminal rows were checked against actual bytes and individually declared metadata. Original terminal hash exclusions were honored by exact paths; no null hashes or blanket mode assumptions were introduced. Both family INITIAL subsets and their historical exposure declarations authenticate against current fixed payloads. Reports and scientific findings were hashed without semantic review.

The original scope native receipt remains one recorded attempt, exit1, empty stdout and720-byte stderr ending in the missing-SymPy error. Its148-line launcher was read as text only and all three recorded native-code byte/line pins match source. The literal traceback reaches replay line118; static control flow places integrity/edition calls before replay and the failing lazy import before temporary layout and any child subprocess. Native-tmp is empty, recorded positive children are0, and no positive replay/result is claimed. ADV declares0 scientific program executions. This task did not rerun, repair, install, import, compile or execute any scientific/native/production helper and creates no mathematical, formal, human or publication certificate.

Administrative history is retained: the original preparatory discovery reader exited1 on an integer files field. Its exact source, literal traceback, receipt and original log remain unchanged. Original discovery stdout was not separately captured; it survives only in the tool transcript, so full-stream custody is not claimed for that attempt. Root explicitly authorized a distinct saved/full-read typed V2 discovery, which exited0 once, and then this distinct saved/full-read main custody checker, which exited0 once. No failure was erased or reinterpreted as a scientific defect. The original native exit1 remains unchanged.

Finite data-custody task100% complete. Unrelated root continuation, primary, raster, progress and challenge work was outside the fixed guards. The research programme remains active and incomplete; no new scientific verdict is given.
'''
with (OWN/'REPORT.md').open('x') as f:f.write(report)
with (OWN/'CONTINUATION_LOG.md').open('a') as f:f.write('\n'+receipt['finished_UTC']+' — Distinct fully saved/read main custody checker invoked once, exit0;334/29 fixed whole inputs and all twelve external controls authenticated. Historical native1/exit1/child0 retained, ADV scientific0; no new scientific execution or verdict. Original discovery1 and authorized V2discovery0 preserved. Finite custody100%; programme active/incomplete.\n')
for n in ['MANIFEST.json','FINAL.json']:
 with (OWN/n).open('x') as f:f.write('{}\n')
files={}
for p in sorted(OWN.rglob('*')):
 assert p.is_file() and not p.is_symlink()
 if p.name not in ['MANIFEST.json','FINAL.json']:files[p.relative_to(OWN).as_posix()]=pin(p)
manifest=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),root=str(OWN),root_mode=format(stat.S_IMODE(OWN.stat().st_mode),'04o'),regular_files=len(files)+2,child_directories=0,payload_files=[dict(path=n,**p,empty=p['bytes']==0,hidden=any(x.startswith('.') for x in Path(n).parts)) for n,p in files.items()],exact_existing_terminal_recursive_hash_exclusions=['MANIFEST.json','FINAL.json'],terminal_modes={n:format(stat.S_IMODE((OWN/n).stat().st_mode),'04o') for n in ['MANIFEST.json','FINAL.json']},other_exclusions=[])
(OWN/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
final=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='DATA_CUSTODY_AUTHENTICATED',protected_extent=d['fixed_extent'],own_files=manifest['regular_files'],own_child_directories=0,manifest=pin(OWN/'MANIFEST.json'),data_authentication=pin(OWN/'DATA_AUTHENTICATION.json'),main_custody_exit=0,original_administrative_discovery_exit=1,V1_stdout_not_separately_captured=True,distinct_authorized_V2_discovery_exit=0,historical_scope_native_attempts=1,historical_scope_native_exit=1,positive_native_children=0,historical_ADV_scientific_executions=0,new_scientific_executions=0,new_mathematical_verdict=False,completion_percent=100,programme_goal_active_incomplete=True)
(OWN/'FINAL.json').write_text(json.dumps(final,indent=2)+'\n')
for n,p in files.items():assert pin(OWN/n)==p,n
assert retained=={n:pin(OWN/n) for n in retained_names} and pin(OWN/'MANIFEST.json')==final['manifest'] and {p.relative_to(OWN).as_posix() for p in OWN.rglob('*')}==set(files)|{'MANIFEST.json','FINAL.json'}
print(json.dumps(final))
