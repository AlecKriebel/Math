"""Independent offline custody/delta/chronology audit. No native or provider calls."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import ast, difflib, hashlib, io, json, os, stat, zipfile
P=Path("/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr214_30005244/preprint")
A=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr214_30005244/prior_package_history_adversary_01")
D=P.parent
READS={}
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p):
 p=Path(p)
 st=p.lstat()
 assert stat.S_ISREG(st.st_mode) and not stat.S_ISLNK(st.st_mode), str(p)
 b=p.read_bytes()
 assert (st.st_dev,st.st_ino,st.st_size,st.st_mode)==(p.lstat().st_dev,p.lstat().st_ino,p.lstat().st_size,p.lstat().st_mode)
 READS[str(p)]={'path':str(p),'bytes':len(b),'sha256':sha(b),'mode':oct(stat.S_IMODE(st.st_mode))}
 return b
def j(p): return json.loads(read(p))
def check_pin(b,row):
 assert len(b)==row['bytes'] and sha(b)==row['sha256'],row
def checked_zip(b):
 z=zipfile.ZipFile(io.BytesIO(b))
 infos=z.infolist(); names=[x.filename for x in infos]
 assert len(names)==len(set(names))
 for i in infos:
  n=PurePosixPath(i.filename)
  assert not n.is_absolute() and '..' not in n.parts and '\\' not in i.filename and not i.is_dir()
  assert stat.S_IFMT(i.external_attr>>16)==stat.S_IFREG
  assert stat.S_IMODE(i.external_attr>>16)==0o644
 assert z.testzip() is None
 m=json.loads(z.read('PACKAGE_FILES.json'))
 rows=m['files']
 assert len(rows)==len({r['path'] for r in rows})
 assert set(names)=={'PACKAGE_FILES.json'}|{r['path'] for r in rows}
 for r in rows: check_pin(z.read(r['path']),r)
 return z,m
finalraw=read(P/'output/dipole_spectrum_verification.zip')
assert len(finalraw)==764472 and sha(finalraw)=='5cbd35e7c4b30d3d7e90a953cffb689b03bc957e60c4aa6905b0a60e38c069d7'
z,m=checked_zip(finalraw)
assert len(z.infolist())==187 and len(m['files'])==186
assert z.read('PACKAGE_FILES.json')==read(P/'PACKAGE_FILES.json')
# Every package member with a direct local origin maps to that exact current origin.
localmatched=[]
for r in m['files']:
 n=r['path']; p=P/n
 if n.startswith('audits/fresh_review_'):
  p=P/n.removeprefix('audits/')
 elif n.startswith('audits/manuscript/'):
  p=P/Path(n).name
 elif n.startswith('audits/root_reproduction/'):
  p=D/'initial_review_20261015/root_reproduction'/n.removeprefix('audits/root_reproduction/')
 elif n.startswith('audits/root/'):
  p=D/'initial_review_20261015'/n.removeprefix('audits/root/')
 elif n.startswith('audits/'):
  p=D/'initial_review_20261015'/n.removeprefix('audits/')
 assert z.read(n)==read(p),str(p)
 localmatched.append(n)
# Historical frozen Review01 source, PDF, ZIP and helpers remain exact.
h=P/'history/review01_frozen'
hm=j(h/'HISTORY_MANIFEST.json')
for r in hm['files']: check_pin(read(h/r['path']),r)
f1=j(h/'FROZEN_INPUTS.json')
for r in f1['submission_files']: check_pin(read(h/r['path']),r)
z1,m1=checked_zip(read(h/'output/dipole_spectrum_verification.zip'))
assert len(z1.infolist())==136 and len(m1['files'])==135
assert z1.read('PACKAGE_FILES.json')==read(h/'PACKAGE_FILES.json')
# Reconstruct earlier second-review ZIP byte-for-byte using unchanged builder settings.
hs=P/'history/review02_manifest_snapshot'
oldmb=read(hs/'PACKAGE_FILES.json'); oldm=json.loads(oldmb)
assert len(oldm['files'])==167
oldnames={r['path'] for r in oldm['files']}
for r in oldm['files']: check_pin(z.read(r['path']),r)
out=io.BytesIO()
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as old:
 for n in sorted(oldnames|{'PACKAGE_FILES.json'}):
  zi=zipfile.ZipInfo(n,date_time=(2026,10,15,0,0,0))
  zi.compress_type=zipfile.ZIP_DEFLATED
  zi.external_attr=0o100644<<16
  old.writestr(zi,oldmb if n=='PACKAGE_FILES.json' else z.read(n))
oldraw=out.getvalue()
assert len(oldraw)==709382 and sha(oldraw)=='b78287495c9704bec1e71113aa0a2f285e0826ee5e01479b59fa0cd8aa4bdf9b'
z2,m2=checked_zip(oldraw)
assert len(z2.infolist())==168
delta=j(P/'FINAL_PACKAGE_DELTA_VALIDATION.json')
actual_added=sorted(set(z.namelist())-set(z2.namelist()))
assert actual_added==delta['added_administrative_members_only'] and len(actual_added)==19
assert not set(z2.namelist())-set(z.namelist())
assert [n for n in z2.namelist() if z.read(n)!=z2.read(n)]==['PACKAGE_FILES.json']
# Safely seal authentic authored review closures.
reviews=[]
for k in (1,2):
 r=P/f'fresh_review_0{k}'
 rm=j(r/'SAFE_AUTHORED_MANIFEST.json')
 assert len(rm['safe_authored_files'])==14
 for row in rm['safe_authored_files']:
  check_pin(read(r/row['path']),row)
  assert read(r/row['path'])==z.read(f'audits/fresh_review_0{k}/'+row['path'])
 reviews.append(rm)
v1=j(P/'fresh_review_01/REVIEW_VERDICT.json');v2=j(P/'fresh_review_02/REVIEW_VERDICT.json')
assert {r['id'] for r in v1['minor_documentary_fixes']}=={'D1','D2'} and v1['publication_cleared'] is False
assert v2['mandatory_findings']==v2['optional_findings']==[] and v2['publication_cleared'] is False
bindings=j(P/'fresh_review_02/INPUT_BINDINGS.json')['inputs']
# Historic frozen receipt replaces overwritten current FROZEN_INPUTS; ZIP reconstructs.
for row in bindings:
 if row['path']=='FROZEN_INPUTS.json': b=read(hs/'FROZEN_INPUTS.json')
 elif row['path']=='output/dipole_spectrum_verification.zip':b=oldraw
 else:b=read(P/row['path'])
 check_pin(b,row)
# All31 archived originals preserved independently of later active status.
original=j(P/'pr_update/30005244/ORIGINAL_SUBMISSION_MANIFEST.json')
assert len(original['files'])==31 and original['original_PR_head']=='36d5ef15098163e74bf14c2e696f560ce592affd'
for r in original['files']:
 b=read(P/'pr_update/30005244'/r['archive_path'])
 check_pin(b,r)
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['native_blob']
 assert b==z.read('pr_update/30005244/'+r['archive_path'])==z1.read('pr_update/30005244/'+r['archive_path'])
# Check global documentary repairs and code transformations without executing the generator.
active=read(P/'pr_update/30005244/CANDIDATE.md').decode()
oldactive=read(h/'pr_update/30005244/CANDIDATE.md').decode()
helper=read(P/'prepare_supporting_materials.py').decode()
oldhelper=read(h/'prepare_supporting_materials.py').decode()
assert '**Unreviewed.**' in oldactive and '**Unreviewed.**' not in active
assert 'Independent review and a broader novelty check remain required.' in oldactive
assert 'Independent review and a broader novelty check remain required.' not in active
assert 'Original analytical derivation. Current validation' in active
assert 'qualified_candidate = original_candidate.replace(old_status' in helper
assert 'qualified_candidate = qualified_candidate.replace(old_review' in helper
assert 'Python3.13' in oldhelper and 'Python3.13' not in helper
assert 'Python3.14.6 with NumPy2.3.4 and SymPy1.14.0' in helper
assert read(P/'verification/README.md')==read(h/'verification/README.md')
assert 'Python3.14.6' in read(P/'verification/README.md').decode()
# Metadata and exact publication identities.
metadata=j(P/'metadata.json'); deposit=j(P/'deposit.json')
assert metadata==deposit['metadata']==json.loads(z.read('metadata.json'))
assert deposit['files']==[{'path':'output/pdf/dipole_spectrum.pdf'},{'path':'output/dipole_spectrum_verification.zip'}]
finalf=j(P/'FROZEN_INPUTS.json'); clearance=j(P/'FINAL_CLEARANCE.json'); publication=j(P/'FINAL_PUBLICATION_AND_MERGE.json')
for row in finalf['submission_files']:check_pin(read(P/row['path']),row)
assert finalf['submission_files']==clearance['submission_files']
assert metadata==clearance['publication_metadata']==publication['publication']['metadata']
assert publication['publication']['id']==23390551 and publication['publication']['doi']=='10.5281/zenodo.23390551'
for r in publication['publication']['files']:
 check_pin(read(P/'output/pdf/dipole_spectrum.pdf' if r['name'].endswith('.pdf') else P/'output/dipole_spectrum_verification.zip'),dict(bytes=r['size'],sha256=r['sha256']))
assert publication['native_merge']['reviewed_head']=='95ba37055ebf1e7b4f9d76aa43816c9978c7bce8'
assert publication['native_merge']['merge_commit']=='4abf30daa991860a275b3d25745159852757ad35'
# Chronological documentary evidence, not independent clock/human proof.
b2=j(P/'fresh_review_02/INPUT_BINDINGS.json')
repair=j(P/'ROOT_REVIEW01_GLOBAL_REPAIR_ACCEPTANCE.json')
r2=j(P/'ROOT_REVIEW02_ACCEPTANCE.json')
times=[reviews[0]['utc'],repair['utc'],b2['utc'],reviews[1]['utc'],r2['utc'],delta['utc'],clearance['utc'],publication['publication']['utc']]
assert list(map(datetime.fromisoformat,times))==sorted(map(datetime.fromisoformat,times))
# Review coverage records: every11 page pair bound, real7 program results, source/report closures.
details=[]
for k in (1,2):
 rd=P/f'fresh_review_0{k}'
 render=j(rd/'RENDER_BINDING.json'); replay=j(rd/'PORTABLE_REPLAY.json'); controls=j(rd/'INDEPENDENT_CONTROLS_RESULT.json')
 assert replay['all_programs_passed'] and len(replay['programs'])==7 and controls['all_passed']
 details.append({'review':k,'render_keys':list(render),'replay_programs':len(replay['programs']),'controls_pin':READS[str(rd/'INDEPENDENT_CONTROLS_RESULT.json')]})
# Full changed text retained for direct read.
diffs={}
for n in ['dipole_spectrum.tex','pr_update/30005244/CANDIDATE.md','prepare_supporting_materials.py','build_submission_package.py','README.md']:
 diffs[n]=''.join(difflib.unified_diff(read(h/n).decode().splitlines(True),read(P/n).decode().splitlines(True),fromfile='review01/'+n,tofile='review02/'+n))
result={'utc':datetime.now(timezone.utc).isoformat(),'scope':'OFFLINE_PRIOR_REVIEW_HISTORY_ONLY','all_checked_assertions_passed':True,
 'final_archive':{'members':187,'manifest_rows':186,'bytes':len(finalraw),'sha256':sha(finalraw),'all_regular_mode_0644':True},
 'first_review_archive':{'members':136,'manifest_rows':135,'bytes':262286,'sha256':sha(read(h/'output/dipole_spectrum_verification.zip'))},
 'reconstructed_second_review_archive':{'members':168,'manifest_rows':167,'bytes':len(oldraw),'sha256':sha(oldraw),'reconstructed_in_memory':True},
 'preserved_second_review_payloads':167,'changed_earlier_members':['PACKAGE_FILES.json'],'added_members':actual_added,
 'final_members_matched_to_local_origins':len(localmatched),'authored_review_rows_verified':[14,14],'original31_bytes_SHA256_and_blobids_verified':True,
 'original_head':original['original_PR_head'],'later_integration_head':publication['native_merge']['reviewed_head'],'merge_commit':publication['native_merge']['merge_commit'],
 'chronological_record_timestamps':times,'review02_input_bindings_replayed':len(bindings),'coverage_receipt_details':details,
 'provider_actions':False,'native_or_git_actions':False,'new_publication_or_tracker_actions':False,
 'limits':['No raw original historical agent turn transcript was supplied; full source-reading/image-view/independence acts are supported by substantive preserved reports and artifacts, not independently observed in this audit.','Native-head bindings are checked offline from content-addressed preserved bodies and historical records; this audit performs no fresh provider or local Git reads.','No new mathematical/priority or entire-goal completion authority is asserted.']}
(A/'CHECK_RESULT.json').open('x').write(json.dumps(result,indent=2)+'\n')
(A/'INPUTS_VERIFIED.json').open('x').write(json.dumps({'files':list(READS.values())},indent=2)+'\n')
(A/'GLOBAL_REPAIR_DIFFS.json').open('x').write(json.dumps(diffs,indent=2)+'\n')
print(json.dumps(result,indent=2))
