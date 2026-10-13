"""Read-only candidate audit; all replay mutations stay in this review directory."""
from pathlib import Path, PurePosixPath
import sys, json, hashlib, zipfile, subprocess, os, datetime
A=Path(__file__).resolve().parent.parent
K=Path(__file__).resolve().parent
P=A/'publication_package_v2'
def require(c,m):
    if not c: raise RuntimeError(m)
def digest(b): return hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=digest(b))
prep=A/'PACKAGE_V2_PREPARATION.json'
require(digest(prep.read_bytes())=='d5e973f0731d490f49100659886d2de2a0f4a8897056ee5f3cca0e40deb45c9d','wrong preparation record')
pr=json.loads(prep.read_text());prep_checks=[]
for root,field in [(P,'package_files'),(A/'native_proposal_v2','native_files')]:
    for name,expected in pr[field].items():
        require(pin(root/name)==expected,'preparation identity mismatch '+str(root/name));prep_checks.append(str(root/name))
m=json.loads((P/'MANIFEST.json').read_text())
z=zipfile.ZipFile(P/'gram_locus_support.zip');names=z.namelist()
require(len(names)==len(set(names)),'duplicate ZIP member')
require(z.testzip() is None,'ZIP CRC failure')
require(set(names)==set(m['files'])|{'MANIFEST.json'},'archive/manifest path-set mismatch')
replay=K/'replay';replay.mkdir(exist_ok=True)
for n in names:
    q=PurePosixPath(n);require(not q.is_absolute() and '..' not in q.parts,'unsafe archive name')
    require(not (z.getinfo(n).external_attr>>16)&0o170000==0o120000,'archive symlink')
    b=z.read(n);require(b==(P/n).read_bytes(),'disk/archive mismatch '+n)
    if n!='MANIFEST.json':require(dict(bytes=len(b),sha256=digest(b))==m['files'][n],'manifest identity mismatch '+n)
    dst=replay/n;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
native=A/'native_proposal_v2'/'publication_package'
require({p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file()}=={p.relative_to(native).as_posix() for p in native.rglob('*') if p.is_file()},'native/package sets differ')
for p in P.rglob('*'):
    if p.is_file():require(p.read_bytes()==(native/p.relative_to(P)).read_bytes(),'native/package bytes differ')
cmd=[sys.executable,'-E','-S','-B','-P',str(replay/'verify_controls.py')]
run=subprocess.run(cmd,cwd=replay,capture_output=True,text=True,timeout=120)
require(run.returncode==0 and not run.stderr,'deposited driver failed')
for n in ['verification.normal.json','verification.optimized.json','negative_controls.json']:
    require((replay/n).read_bytes()==z.read(n),'deposited output replay differs '+n)
neg=json.loads((replay/'negative_controls.json').read_text())
require(len(neg['rejections'])==8 and all(i['rejected'] for i in neg['rejections']),'mutation control coverage')
native_runs=[]
for optimized in [False,True]:
    cmd=[sys.executable,'-E','-S','-B','-P']+(['-O'] if optimized else [])+[str(A/'native_proposal_v2'/'verify.py')]
    p=subprocess.run(cmd,cwd=K,capture_output=True,text=True,timeout=120)
    require(p.returncode==0 and not p.stderr,'active native wrapper failed')
    require(p.stdout.encode()==z.read('verification.normal.json'),'native checker output differs')
    native_runs.append(dict(optimized=optimized,returncode=p.returncode,stdout_sha256=digest(p.stdout.encode())))
rows=[]
for family in json.loads((P/'SUPPORT_INDEX.json').read_text())['families']:
    for n in family['included_paths']:require(n in names,'index advertises missing '+n)
    rows.append(dict(family=family['family'],all_advertised_present=True,count=len(family['included_paths'])))
for n in names:
    require('/private/' not in n and '/scratch/' not in n,'private member')
    require(not n.endswith(('.pdf','.png','.html')),'third-party body/render member')
out=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS',archive=pin(P/'gram_locus_support.zip'),manuscript_pdf=pin(P/'gram_locus_note.pdf'),preparation=pin(prep),preparation_identities_checked=len(prep_checks),ZIP_members=len(names),manifest_entries=len(m['files']),all_CRCs_pass=True,all_member_bytes_match_manifest_and_disk=True,native_publication_package_byte_identical=True,deposited_driver_stdout=run.stdout.strip(),same_deposited_outputs_reproduced_exactly=True,mutations=neg['rejections'],native_wrapper_runs=native_runs,support_index_families=rows,archive_member_names=names)
(K/'PACKAGE_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','ZIP_members','manifest_entries','preparation_identities_checked','same_deposited_outputs_reproduced_exactly','native_publication_package_byte_identical']}))
