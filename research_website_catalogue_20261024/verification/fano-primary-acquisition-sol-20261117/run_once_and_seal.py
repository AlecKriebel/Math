"""One saved acquisition invocation, literal streams, own-only finite evidence seal."""
from pathlib import Path
import datetime,hashlib,json,stat,subprocess,sys,time
if not __debug__:raise RuntimeError('Assertions required')
OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/fano-primary-acquisition-sol-20261117')
def pin(p):
 a=p.lstat();assert stat.S_ISREG(a.st_mode) and not p.is_symlink();b=p.read_bytes();z=p.lstat()
 assert (a.st_dev,a.st_ino,a.st_mode,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_size,z.st_mtime_ns,z.st_ctime_ns)
 return dict(bytes=len(b),SHA256=hashlib.sha256(b).hexdigest(),mode=format(stat.S_IMODE(z.st_mode),'04o'))
for n in ['EXECUTION.json','acquisition.stdout','acquisition.stderr','SOURCE_EDITION_MAP.json','MANIFEST.json','FINAL.json','REPORT.md']:assert not (OWN/n).exists(),n
sources={n:pin(OWN/n) for n in ['acquire_once.py','run_once_and_seal.py']};argv=[sys.executable,'-B',str(OWN/'acquire_once.py')];start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
r=subprocess.run(argv,cwd=OWN,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
for n,b in [('acquisition.stdout',r.stdout),('acquisition.stderr',r.stderr)]:
 with (OWN/n).open('xb') as f:f.write(b)
receipt=dict(started_UTC=start,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.monotonic()-t,argv=argv,exit_code=r.returncode,one_invocation=True,no_automatic_retry=True,literal_stdout=pin(OWN/'acquisition.stdout'),literal_stderr=pin(OWN/'acquisition.stderr'),full_saved_sources_personally_read_before_execution=sources)
with (OWN/'EXECUTION.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
assert sources=={n:pin(OWN/n) for n in sources}
if r.returncode:
 print(r.stdout.decode(errors='replace'));print(r.stderr.decode(errors='replace'),file=sys.stderr);raise SystemExit(r.returncode)
d=json.loads((OWN/'SOURCE_EDITION_MAP.json').read_bytes());assert d['whole_native_source196files21dirs_and_ROOTINITIAL18files1dir_unchanged']
report='# Fano cited-primary acquisition custody\n\nStatus: '+d['status']+'. Seven whole cached PDFs were independently authenticated against declared bytes/SHA256 and copied into the root-authorized private ignored primary directory. No direct curl or fresh local HTTP download is claimed. Named primary URLs were browser-opened; the OWR and Wang-Zhu DOI resolver failures are retained, with publisher/author PDF fallback opens recorded separately.\n\n|ID|Pinned edition|PDF bytes|PDF pages|SHA256|\n|---|---|---:|---:|---|\n'
for x in d['records']:report+='|'+x['label']+'|'+x['declared_edition'].replace('|','/')+'|'+str(x['payload_pdf']['bytes'])+'|'+str(x.get('pdf_pages','unavailable'))+'|'+x['payload_pdf']['SHA256']+'|\n'
report+='\nThe edition map records full cache/payload paths, actual hashes and modes, observed arXiv stamps, literal Poppler command arguments/exits/stream hashes, text paths and label-only locator offsets. All PDF/text bodies remain only in the private ignored payload folder. Unversioned Han-Li generalized-soliton and Wang-Zhu author manuscripts are identified by their pinned whole bytes; no publisher version-of-record or current-HTTP-byte identity is inferred. In particular, the browser currently reports15PDFpages for the Wang-Zhu author URL; the actual pinned local pagecount is shown above, independently. Missing label matches are locator qualifications, not mathematical conclusions.\n\nWhole native Fano source196files/21childdirs and frozen rootINITIAL18/1, all hidden/ignored/empty bytes, modes, times and topology, match before/after. ROOTINITIAL remains files0444/directories0555 with its original seals exact. No source/helper code was imported, parsed as AST, compiled or executed, no mathematical verdict or peer report was read, and no Git/website/Sheet/global file was changed. Original browser lookup errors remain retained. Finite acquisition '+str(d['completion_percent'])+'% complete; programme remains active/incomplete.\n'
with (OWN/'REPORT.md').open('x') as f:f.write(report)
with (OWN/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+receipt['finished_UTC']+' — One fully saved/read acquisition script returned0; cache identities and protected whole guards authenticated. Actual status '+d['status']+';7cachedPDFs,14single Poppler invocations with literal histories retained; no source/scientific execution or directcurl. Private bodies only; unversioned edition limits explicit. Finite acquisition '+str(d['completion_percent'])+'%; programme active/incomplete.\n')
for n in ['MANIFEST.json','FINAL.json']:
 with (OWN/n).open('x') as f:f.write('{}\n')
files={}
for p in sorted(OWN.rglob('*')):
 assert p.is_file() and not p.is_symlink()
 if p.name not in ['MANIFEST.json','FINAL.json']:files[p.relative_to(OWN).as_posix()]=pin(p)
manifest=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),root=str(OWN),root_mode=format(stat.S_IMODE(OWN.stat().st_mode),'04o'),regular_files=len(files)+2,child_directories=0,payload_files=[dict(path=n,**p,empty=p['bytes']==0,hidden=any(x.startswith('.') for x in Path(n).parts)) for n,p in files.items()],exact_existing_terminal_recursive_hash_exclusions=['MANIFEST.json','FINAL.json'],terminal_modes={n:format(stat.S_IMODE((OWN/n).stat().st_mode),'04o') for n in ['MANIFEST.json','FINAL.json']},other_exclusions=[])
(OWN/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
final=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),status=d['status'],complete=d['complete'],own_files=manifest['regular_files'],own_child_directories=0,manifest=pin(OWN/'MANIFEST.json'),source_edition_map=pin(OWN/'SOURCE_EDITION_MAP.json'),protected_source_and_INITIAL_whole_guards_exact=True,actual_primary_PDFs=d['authenticated_cache_copies'],direct_curl_invocations=0,new_scientific_executions=0,new_mathematical_verdict=False,completion_percent=d['completion_percent'],programme_goal_active_incomplete=True)
(OWN/'FINAL.json').write_text(json.dumps(final,indent=2)+'\n')
for n,p in files.items():assert pin(OWN/n)==p,n
assert pin(OWN/'MANIFEST.json')==final['manifest'] and {p.relative_to(OWN).as_posix() for p in OWN.rglob('*')}==set(files)|{'MANIFEST.json','FINAL.json'}
print(json.dumps(final))
