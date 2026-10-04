"""ROOT alone may close this completed reviewer family, then separately verify it."""
from pathlib import Path,PurePosixPath
import argparse,datetime as dt,hashlib,json,os,stat,sys
F=Path(__file__).absolute().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def scan():
 fs=set();ds=set()
 assert F.is_dir() and not F.is_symlink()
 for p in F.rglob('*'):
  assert not p.is_symlink()
  n=p.relative_to(F).as_posix();assert n!='.' and not {'.','..','.git','__pycache__'}.intersection(PurePosixPath(n).parts)
  if stat.S_ISREG(p.stat().st_mode):fs.add(n)
  else:assert stat.S_ISDIR(p.stat().st_mode);ds.add(n)
 assert ds=={q.as_posix() for n in fs for q in PurePosixPath(n).parents if q.as_posix()!='.'}
 return fs,ds
assert __debug__ and not sys.flags.optimize
p=argparse.ArgumentParser();p.add_argument('--expected-report-sha256',required=True);a=p.parse_args()
assert not (F/'MANIFEST.json').exists() and not (F/'MANIFEST.json').is_symlink()
assert sha((F/'AUDIT.md').read_bytes())==a.expected_report_sha256
fs,ds=scan()
for n in fs:(F/n).chmod(0o444)
rows=[]
for n in sorted(fs):
 b=(F/n).read_bytes();assert stat.S_IMODE((F/n).stat().st_mode)==0o444
 rows.append({'path':n,'bytes':len(b),'sha256':sha(b),'full_mode':'0444'})
manifest={'schema':'pr47-whole-current-independent-self-only-closure/v1',
 'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_closing_pid':os.getpid(),
 'self_excluded':['MANIFEST.json'],'files_count':len(rows),'files':rows,
 'directories':sorted(ds),'full_permission_mode':'0444',
 'candidate_manifest_sha256':'a7d1acc9dbbf8cd5435d0bebd8f6b1a540ecb0f2aea8d0c616c46bc5bf6b4ea5',
 'verdict':'PASS_EXACT_CURRENT_CORRECTED_UNRESOLVED_PARTIAL_NO_MANDATORY_CORRECTION',
 'mandatory_corrections':[],'future_acceptance_approved':False,
 'closing_postchild_capture_inside_manifest_claimed':False,
 'historical_private_fixture_modes_restored_to_full0444_at_closure':True,
 'production_builder_or_operator_run':False,'foreign_source_raw_SQL_cache_bodies_copied':False}
b=(json.dumps(manifest,indent=2,allow_nan=False)+'\n').encode()
with (F/'MANIFEST.json').open('xb') as out:out.write(b);out.flush();os.fsync(out.fileno())
(F/'MANIFEST.json').chmod(0o444)
actual,actual_dirs=scan();assert actual==fs|{'MANIFEST.json'} and actual_dirs==ds
for row in rows:
 p=F/row['path'];b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
print(json.dumps({'status':'CLOSED_SELF_ONLY_WHOLE_CURRENT_INDEPENDENT_FAMILY','actual_closing_pid':os.getpid(),
 'files_count':len(rows),'directories_count':len(ds),'manifest_sha256':sha((F/'MANIFEST.json').read_bytes()),
 'future_acceptance_approved':False},indent=2))
