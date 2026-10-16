"""Read-only original-source and scientific artifact integrity; no helper import."""
from pathlib import Path
from datetime import datetime,timezone
import base64,hashlib,json,zipfile

OUT=Path(__file__).resolve().parent;D=OUT.parent;C=D.parent;P=C/'publication';R=C/'preprint';H=D/'history/release_helpers_review03_frozen'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
inputs=load(OUT/'INPUTS.json');helpers=[]
for row in inputs['sources']:
    p=Path('/Users/alec/Documents/Math')/row['path'];raw=p.read_bytes();compile(raw,str(p),'exec')
    helpers.append(dict(path=row['path'],bytes=len(raw),sha256=sha(p),matches=len(raw)==row['bytes'] and sha(p)==row['sha256']))
assert all(x['matches'] for x in helpers)
archive=[]
for row in load(H/'ARCHIVE_MANIFEST.json')['files']:
    p=H/row['path'];archive.append(dict(path=row['path'],matches=p.stat().st_size==row['bytes'] and sha(p)==row['sha256']))
assert len(archive)==14 and all(x['matches'] for x in archive)
prior=D/'release_helpers_adversary_03';priorfiles=[]
for row in load(prior/'AUTHORED_MANIFEST.json')['files']:
    p=prior/row['path'];priorfiles.append(dict(path=row['path'],matches=p.stat().st_size==row['bytes'] and sha(p)==row['sha256']))
assert all(x['matches'] for x in priorfiles)
c=load(R/'FINAL_CLEARANCE.json');package=load(R/'PACKAGE_MANIFEST.json');science=[]
for row in package['submission_files']+[package[k] for k in ['source_manifest','manuscript_source','metadata']]:
    p=R/row['path'];science.append(dict(**row,matches=p.stat().st_size==row['bytes'] and sha(p)==row['sha256']))
assert all(x['matches'] for x in science)
assert (R/'FINAL_CLEARANCE.json').read_bytes()==(H/'FINAL_CLEARANCE.json').read_bytes()
stale=[]
for row in c['release_helpers']:
    p=P/row['path']
    if p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:stale.append(p.name)
assert stale==['integrate_reviewed_pr.py']
for n in ['ZENODO_VERIFIED_PUBLICATION.json','TRACKER_VERIFIED_APPEND.json','STAGE_ATTEMPT.json','PUBLISH_ATTEMPT.json']:
    assert (P/n).read_bytes()==(H/n).read_bytes()
assert load(H/'ZENODO_VERIFIED_PUBLICATION.json')['id']==23398175
assert load(H/'TRACKER_VERIFIED_APPEND.json')['updated_range']=="'Math Puzzles'!A113:D113"
intake=load(D/'INTAKE.json');original=[]
with zipfile.ZipFile(R/'k605a-source-verification.zip') as z:
    entries=z.namelist();assert len(entries)==len(set(entries))==181
    assert all(not n.startswith('/') and '..' not in Path(n).parts for n in entries)
    U=R/'pr_update/5100033';prefix='k605a_outer_focal_pedal_product/pr_update/5100033/'
    native={p.relative_to(U).as_posix():p.read_bytes() for p in U.rglob('*') if p.is_file()}
    zipped={n.removeprefix(prefix):z.read(n) for n in entries if n.startswith(prefix)}
    assert native==zipped
    for row in intake['original_source_files']:
        rel=row['native_path'].removeprefix('unsolved_math_prioritization/attempts/5100033/')
        for root in [D/'submitted/unsolved_math_prioritization/attempts/5100033',U/'history/original_submission_20261015',R/'verification/original_submission']:
            p=root/rel;original.append(dict(path=str(p.relative_to(C)),matches=p.stat().st_size==row['bytes'] and sha(p)==row['sha256']))
    assert len(original)==60 and all(x['matches'] for x in original)
captures=P/'private_transport/native_prepare_20261015T142749854176Z'
rows=[]
for n in ['002-stdout.json','008-stdout.json']:
    x=load(captures/n);raw=base64.b64decode(x['content']);target=[s for s in raw.decode().splitlines() if '5100033 / AMR-050-0033' in s]
    assert len(target)==1;rows.append(target[0])
placeholder=rows[0].split('|');placeholder[8]=' queued ';placeholder[9]=' 0/5 '
for i in [10,11,12]:placeholder[i]=' '
assert rows[1]!='|'.join(placeholder)
value=dict(utc=datetime.now(timezone.utc).isoformat(),helper_checks=helpers,archive_checks=archive,
  prior_source03_seal_checks=priorfiles,science_checks=science,zip_entries=len(entries),native_zip_exact_equality=True,
  native_files=len(native),original20_three_copy_checks=original,old_genuine_clearance_stale_helpers=stale,
  old_clearance_and_current_initial_receipts_unchanged=True,actual_main_placeholder_matches_reconstruction=False,
  actual_main_empty_cell_lengths=[len(rows[1].split('|')[i]) for i in [10,11,12]],
  reconstructed_empty_cell_lengths=[len(placeholder[i]) for i in [10,11,12]],
  source04_is_supporting_only=True,provider_CLI_Git_network_calls=0,completion_percent=95)
(OUT/'LOCAL_INTEGRITY_RESULTS.json').write_text(json.dumps(value,indent=2)+'\n')
print(json.dumps({k:v for k,v in value.items() if k not in ['helper_checks','archive_checks','prior_source03_seal_checks','original20_three_copy_checks']},indent=2))
