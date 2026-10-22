"""Read-only independent review02 manifest/ZIP/current/history binding audit."""
import hashlib,json,zipfile,stat,importlib.util,subprocess,sys,ast
from pathlib import Path,PurePosixPath
OUT=Path(__file__).parent
CASE=OUT.parent.parent
F=CASE/'preprint/history/review02_frozen';N=F/'pr_update/5100063';V=F/'verification'
sha=lambda b:hashlib.sha256(b).hexdigest()
def pincheck(base,row):
    p=base/row['path'];assert p.is_file() and not p.is_symlink(),str(p)
    data=p.read_bytes();assert len(data)==row['bytes'] and sha(data)==row['sha256'],str(p)
def read(p):return json.loads(p.read_text())
S=read(F/'SOURCE_MANIFEST.json');rows=S['files'];names=[r['path'] for r in rows]
assert len(names)==len(set(names))==150
for r in rows:pincheck(F,r)
P=read(F/'PACKAGE_MANIFEST.json')
for r in [P['source_manifest'],P['manuscript_source'],P['metadata'],*P['submission_files']]:pincheck(F,r)
D=read(F/'deposit.json');assert D['metadata']==read(F/'metadata.json')
assert D['files']==[{'path':'manuscript.pdf','name':'k904a-outer-focal-inverse-areas.pdf'},{'path':'k904a-source-verification.zip','name':'k904a-source-verification.zip'}]
prefix='k904a_outer_focal_inverse_product/'
with zipfile.ZipFile(F/'k904a-source-verification.zip') as z:
    zs=z.infolist();assert len(zs)==151 and len({i.filename for i in zs})==151
    assert set(z.namelist())=={prefix+n for n in names+['SOURCE_MANIFEST.json']}
    for i in zs:
        p=PurePosixPath(i.filename);assert not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename
        assert not set(p.parts)&{'private','private_reading','private_transport','__pycache__'}
        assert stat.S_IFMT(i.external_attr>>16)==stat.S_IFREG
        assert z.read(i.filename)==(F/i.filename[len(prefix):]).read_bytes()
        assert i.date_time==(2026,10,15,0,0,0)
    assert z.testzip() is None
# All selected files have authored formats, with the sole own manuscript PDF.
assert [n for n in names if n.lower().endswith(('.pdf','.png','.jpg','.html','.gz'))]==['manuscript.pdf']
counts={}
for base,name in [(V,'MANIFEST.json'),(N,'MANIFEST.json'),(N,'PUBLICATION_MANIFEST.json'),(N,'CURRENT_PACKET_MANIFEST.json')]:
    M=read(base/name)
    for r in M['files']:pincheck(base,r)
    counts[str(base.relative_to(F)/name)]=len(M['files'])
vm={r['path'] for r in read(V/'MANIFEST.json')['files']}
assert vm=={p.relative_to(V).as_posix() for p in V.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}|{p.relative_to(V).as_posix() for p in V.rglob('MANIFEST.json') if p!=V/'MANIFEST.json'}
# Current top-level manifests intentionally do not cover nested history; complete seal does.
assert read(N/'MANIFEST.json')==read(N/'PUBLICATION_MANIFEST.json')
assert {r['path'] for r in read(N/'CURRENT_PACKET_MANIFEST.json')['files']}=={p.relative_to(N).as_posix() for p in N.rglob('*') if p.is_file() and p!=N/'CURRENT_PACKET_MANIFEST.json'}
intake=OUT.parent/'submitted/unsolved_math_prioritization/attempts/5100063'
originals=sorted(p for p in intake.rglob('*') if p.is_file());assert len(originals)==19
for p in originals:
    rel=p.relative_to(intake)
    for b in [V/'original_submission',N/'history/original_submission_20261015']:assert p.read_bytes()==(b/rel).read_bytes(),str(rel)
prov=read(V/'PROVENANCE.json')
for r in prov['original_files']:pincheck(V,r)
# Family manifests retain original bases. Strip only the documented family prefix.
families=[]
for fam in prov['audit_families']:
    folder=V/'audits'/fam['family'];mpath=folder/('MANIFEST.json' if fam['family']=='priority_classical_general_01' else 'AUTHORED_MANIFEST.json')
    assert sha(mpath.read_bytes())==fam['original_manifest_sha256']
    M=read(mpath);rr=M.get('files',M.get('entries'))
    for r in rr:
        r=r.copy();r['path']=r.get('path',r.get('relative_path'));path=PurePosixPath(r['path'])
        if path.parts[0]==fam['family']:r['path']=str(PurePosixPath(*path.parts[1:]))
        pincheck(folder,r)
    assert len(rr)==fam['authored_files'];families.append({'family':fam['family'],'rows':len(rr)})
# Historical reviewer seal and root resolution duplicated consistently.
old=F/'manuscript_reviews/review01';M=read(old/'AUTHORED_MANIFEST.json')
for r in M['files']:pincheck(old,r)
assert (F/'REVIEW01_RESOLUTION.json').read_bytes()==(old/'REVIEW01_RESOLUTION.json').read_bytes()
res=read(F/'REVIEW01_RESOLUTION.json');assert sha((old/'REPORT.md').read_bytes())==res['review_report_sha256']
oldF=CASE/'preprint/history/review01_frozen'
oldproof=(oldF/'pr_update/5100063/PROOF.md').read_text();newproof=(N/'PROOF.md').read_text()
extract=lambda s:s[s.index('## 1.'):s.index('## 8.')]
assert extract(oldproof)==extract(newproof)
# Active receipt explicitly binds its archived proof, rather than falsely binding revised proof.
rv=read(N/'verification.json');assert rv['proof_sha256']==sha((V/'original_submission/PROOF.md').read_bytes())
assert rv['proof_sha256']!=sha((N/'PROOF.md').read_bytes()) and 'Historical' in rv['record_scope']
legacy=read(N/'independent_review/FROZEN_INPUT_VERIFICATION.json')
assert legacy['proof_sha256']==sha((V/'original_submission/PROOF.md').read_bytes())
assert legacy['manifest_sha256']==sha((V/'original_submission/MANIFEST.json').read_bytes())
for r in legacy['files']:assert sha((V/'original_submission'/r['file']).read_bytes())==r['sha256']
for name,digest in read(N/'independent_review/REVIEW_SHA256SUMS.json').items():assert sha((N/'independent_review'/name).read_bytes())==digest
for p in (V/'original_submission/independent_review').iterdir():
    if p.is_file():assert p.read_bytes()==(N/'independent_review'/p.name).read_bytes()
for pname in ['invariants_v11.pdf','invariants_final.pdf','stachel_published.pdf']:
    row=next(r for r in read(N/'source_manifest.json')['sources'] if r['file']==pname)
    assert sha((OUT.parent/'private_reading'/pname).read_bytes())==row['sha256']
# Importing harness defines functions only; no replay/mutation until explicit main.
spec=importlib.util.spec_from_file_location('review02_harness',V/'run_verification.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
harness=mod.verify_integrity();assert len(mod.JOBS)==10
# Syntax checks; no bytecode or program execution.
for p in F.rglob('*.py'):ast.parse(p.read_text(),filename=str(p))
report={'status':'PASS','source_manifest_rows':len(rows),'archive_entries':151,'native_and_portable_manifest_rows':counts,'intake_files_matching_each_archive':len(originals),'original_intake_bytes':sum(p.stat().st_size for p in originals),'family_manifests':families,'historical_review01_seal_rows':len(M['files']),'proof_sections_1_through_7_unchanged':True,'all_primary_pins_match':True,'metadata_exact_deposit_equal':True,'portable_harness_integrity':harness,'frozen_pins':{n:sha((F/n).read_bytes()) for n in ['manuscript.tex','manuscript.pdf','k904a-source-verification.zip','SOURCE_MANIFEST.json','PACKAGE_MANIFEST.json','metadata.json']},'limitations':'Manifest equality checks byte/provenance consistency, not mathematical truth. Review01 utility is historical fixed133-frame and was not run on current151-frame.'}
(OUT/'PACKAGE_AUDIT_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
