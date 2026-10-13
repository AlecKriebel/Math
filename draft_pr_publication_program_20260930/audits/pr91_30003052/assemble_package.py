from pathlib import Path
import json,hashlib,zipfile,datetime,os
A=Path(__file__).resolve().parent;D=A/'publication_package_v1';P=D/'publicfiles'
def require(c,msg):
 if not c:raise RuntimeError(msg)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
R=json.loads((P/'verification/results.json').read_text())
require(R['status']=='PASS_FINITE_CONTROLS','finite receipt failed')
require(R['artifact']['sha256']==digest(P/'pr91_note.tex'),'stale manuscript identity')
require(len(R['runs'])==6 and all(x['exit_code']==0 for x in R['runs']),'bad child run')
require(R['unique_controls_per_mode']['total']==2720,'count')
for row in R['sources']:require(row['sha256']==digest(P/'verification'/row['file']),'stale supporting source')
members=['pr91_note.tex','README.md','PR91_PRIORITY_AUDIT.md','LICENSE.txt']
members+=['verification/'+n for n in ['verify.py','independent_checks.py','boundary_checks.py','run_all.py','SOURCE_PROVENANCE.json','results.json','VERIFY_README.md']]
Z=P/'pr91_support.zip'
with zipfile.ZipFile(Z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name in sorted(members):
  p=P/name;require(p.is_file() and not p.is_symlink(),'nonregular member')
  info=zipfile.ZipInfo(name,(2026,10,5,0,0,0));info.external_attr=0o100644<<16;info.create_system=3;info.compress_type=zipfile.ZIP_DEFLATED
  z.writestr(info,p.read_bytes())
with zipfile.ZipFile(Z) as z:
 require(sorted(z.namelist())==sorted(members),'archive scope')
 for n in members:require(z.read(n)==(P/n).read_bytes(),'archive body mismatch')
manifest=json.loads((D/'zenodo-deposit.json').read_text());payload=[D/x['path'] for x in manifest['files']]
(P/'SHA256SUMS.txt').write_text(''.join(digest(p)+'  '+str(p.relative_to(P))+'\n' for p in sorted(payload+[(P/n) for n in members]) if p.name!='SHA256SUMS.txt' and p in set(payload+[(P/n) for n in members])))
# Remove duplicate paths introduced by uploading source/readme separately from archive.
lines=(P/'SHA256SUMS.txt').read_text().splitlines();(P/'SHA256SUMS.txt').write_text('\n'.join(dict.fromkeys(lines))+'\n')
pins=[]
for p in payload:
 require(p.is_file() and not p.is_symlink(),'nonregular payload')
 b=p.read_bytes();pins.append({'file':str(p.relative_to(D)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'md5':hashlib.md5(b).hexdigest()})
snapshot={'schema':'pr91-public-package/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'metadata_sha256':digest(D/'zenodo-deposit.json'),'payloads':pins,'archive_members':[{'file':n,'sha256':digest(P/n),'bytes':(P/n).stat().st_size} for n in sorted(members)],'archive_byte_comparison':True,'third_party_PDFs_included':False,'private_audit_files_included':False,'digests_self_excluded':True,'publication_clearance':False}
(D/'private_notes/PUBLIC_PACKAGE_MANIFEST.json').write_text(json.dumps(snapshot,indent=2)+'\n')
print(json.dumps({'payloads':len(pins),'archive_members':len(members),'total_payload_bytes':sum(x['bytes'] for x in pins),'source_sha256':digest(P/'pr91_note.tex'),'actual_PID':os.getpid()}))
