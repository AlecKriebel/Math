from pathlib import Path
import hashlib,json,datetime,subprocess,zipfile,sys
OWN=Path(__file__).resolve().parent;BASE=OWN.parent;ROOT=OWN/'extracted';REPO=Path('/Users/alec/Documents/Math');HEAD='e9c5d10978764db2cf25fa7d49cf4bd14a82d604';sha=lambda b:hashlib.sha256(b).hexdigest()
original=ROOT/'original_submission';prefix='unsolved_math_prioritization/attempts/30004630/'
native=subprocess.run(['git','ls-tree','-r','--name-only',HEAD,'--',prefix],cwd=REPO,capture_output=True,text=True,check=True).stdout.splitlines()
packaged=sorted(str(f.relative_to(original)) for f in original.rglob('*') if f.is_file())
assert sorted(p[len(prefix):] for p in native)==packaged
assert len(packaged)==19
comp=[]
for name in packaged:
 b=subprocess.run(['git','show',HEAD+':'+prefix+name],cwd=REPO,capture_output=True,check=True).stdout
 p=(original/name).read_bytes();assert b==p,name
 comp.append({'path':name,'bytes':len(p),'sha256':sha(p),'git_blob_sha1':hashlib.sha1(b'blob '+str(len(p)).encode()+b'\0'+p).hexdigest(),'exact_native_original_match':True})
meta=json.loads((BASE/'metadata.json').read_text());d=json.loads((BASE/'deposit.json').read_text())
assert d['metadata']==meta
assert (ROOT/'metadata.json').read_bytes()==(BASE/'metadata.json').read_bytes()
assert (ROOT/'manuscript/critical_wave_growth.tex').read_bytes()==(BASE/'critical_wave_growth.tex').read_bytes()
current=BASE/'verification_package';payloadcomp=[]
for f in sorted(ROOT.rglob('*')):
 if f.is_file():
  rel=f.relative_to(ROOT);assert f.read_bytes()==(current/rel).read_bytes(),rel
  payloadcomp.append(str(rel))
assert {str(p.relative_to(current)) for p in current.rglob('*') if p.is_file()}==set(payloadcomp)
with zipfile.ZipFile(BASE/'output/critical_wave_verification.zip') as z:
 entries=z.infolist();assert len(entries)==len(set(x.filename for x in entries))==113
 assert {x.filename for x in entries}==set(payloadcomp)
 for x in entries:
  assert not Path(x.filename).is_absolute() and '..' not in Path(x.filename).parts
  assert z.read(x)==(ROOT/x.filename).read_bytes()
  assert (x.external_attr>>16)&0o170000 in (0,0o100000)
replay=json.loads((OWN/'FROZEN_ARCHIVE_REPLAY.json').read_text());counts=[]
for c in replay['checksets']:
 q=c['receipt'];reported=q.get('assertions',q.get('exact_assertions',q.get('exact_checks')))
 diag=q.get('categories',{}).get('threshold_high_precision_sanity',0)
 counts.append({'checkset':c['name'],'reported':reported,'noncertified_diagnostic_assertions':diag,'exact_assertions':reported-diag})
assert sum(c['exact_assertions'] for c in counts)==5603
assert sum(c['noncertified_diagnostic_assertions'] for c in counts)==5
import sympy,mpmath
assert sympy.__version__=='1.14.0' and mpmath.__version__=='1.3.0'
assert sys.version_info>=(3,11)
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_head':HEAD,'all_19_original_byte_equal_native_git':True,'original_files':comp,'candidate_archive_current_payload_exact_equality':True,'archive_files':len(payloadcomp),'file_manifest_entries':112,'file_manifest_excludes_self':True,'metadata_archive_byte_equal':True,'deposit_metadata_object_equal':True,'manuscript_archive_byte_equal':True,'deposit_file_list':d['files'],'assertion_count_derivation':counts,'total_exact':5603,'total_noncertified_diagnostics':5,'runtime':sys.version,'sympy':sympy.__version__,'mpmath':mpmath.__version__,'receipt_normalization':'Only top-level utc/python informational fields removed; dependency strings, counts, scientific values, categories, diagnostic values and limitation statements compare exactly. Emitted-file receipt contents compared; stdout output path is informational, and when emitted stdout includes receipt SHA256 it was validated.'}
(OWN/'INTEGRITY_AND_COUNT_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('original_files','assertion_count_derivation')},indent=2))
