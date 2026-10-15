from pathlib import Path
import hashlib,json,datetime,zipfile,difflib
OWN=Path(__file__).resolve().parent;BASE=OWN.parent;HIST=BASE/'history/before_editorial_refinement_20261014T050605832144Z';OLD=BASE/'fresh_review_01';sha=lambda b:hashlib.sha256(b).hexdigest();utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
original_review_manifest=OLD/'FINAL_AUDIT_MANIFEST.json';assert sha(original_review_manifest.read_bytes())=='91158468546d72bcf01a292f2e092b80d09d82e1e730e9205e765f46f4a0ad14'
old_review=json.loads(original_review_manifest.read_text())
for p in old_review['public_authored_relative_paths']:
 b=(OLD/p['path']).read_bytes();assert len(b)==p['bytes'] and sha(b)==p['sha256'],p['path']
hist_manifest=json.loads((HIST/'PRESERVATION_MANIFEST.json').read_text())
for p in hist_manifest['original_draft_current_paths_before_editorial_refinement']:
 b=(HIST/p['path']).read_bytes();assert len(b)==p['bytes'] and sha(b)==p['sha256'],p['path']
frozen=json.loads((BASE/'FROZEN_CANDIDATE.json').read_text());inputs=[]
for p in frozen['files']:
 b=(BASE/p['path']).read_bytes();assert len(b)==p['bytes'] and sha(b)==p['sha256'];inputs.append({**p,'matches':True})
assert inputs[0]['sha256']=='bf4e13509ee738d1c5f73555e322ce77b9f2041b2306e4f80dfc588c98289584'
assert inputs[1]['sha256']=='a68d8d47dcf625f9ab8818924071200bff2b2280d67665e1e67dd7b83effe988'
assert inputs[2]['sha256']=='1da933750640177045808de748dd7f5732c33277377285b688a411f9f89771a0'
a=(HIST/'critical_wave_growth.tex').read_text();b=(BASE/'critical_wave_growth.tex').read_text()
subs=[(r"Kunisch--Meinlschmidt's wave-control analysis \cite{KM} proves strong",r"Kunisch--Meinlschmidt's wave-control analysis \cite[Theorem~4.17]{KM} proves strong"),('worldwide firstness. All analytic estimates used below are standard','worldwide firstness. The wave estimates used below are standard'),('its access limitations.\n\n\\begin{thebibliography}', 'its access limitations.\nThis note and its authored supporting materials are licensed under\n\\href{https://creativecommons.org/licenses/by/4.0/}{CC BY 4.0}.\n\n\\begin{thebibliography}')]
expected=a
for old,new in subs:assert expected.count(old)==1;expected=expected.replace(old,new)
assert expected==b,'Unexpected TeX change'
(OWN/'DRAFT_TO_CURRENT_TEX.diff').write_text(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='historical/critical_wave_growth.tex',tofile='current/critical_wave_growth.tex')))
with zipfile.ZipFile(HIST/'output/critical_wave_verification.zip') as oz,zipfile.ZipFile(BASE/'output/critical_wave_verification.zip') as nz:
 assert len(nz.infolist())==len({x.filename for x in nz.infolist()})==113
 assert set(oz.namelist())==set(nz.namelist())
 for info in nz.infolist():
  assert not Path(info.filename).is_absolute() and '..' not in Path(info.filename).parts
  assert (info.external_attr>>16)&0o170000 in (0,0o100000)
 nz.extractall(OWN/'extracted')
 changed=[];unchanged=[]
 for name in sorted(nz.namelist()):
  ob=oz.read(name);nb=nz.read(name)
  if ob!=nb:changed.append({'path':name,'historical_bytes':len(ob),'historical_sha256':sha(ob),'current_bytes':len(nb),'current_sha256':sha(nb)})
  else:unchanged.append(name)
 assert {p['path'] for p in changed}=={'README.md','manuscript/critical_wave_growth.tex','FILE_MANIFEST.json'}
 oldread=oz.read('README.md').decode();newread=nz.read('README.md').decode()
 ins='The relocated historical_snapshot_01 manifest shares four unchanged input/checker files with its parent audit-family directory; their exact preserved bytes remain in that parent directory. '
 assert oldread.count('Some audit-only paths refer to the original workspace;')==1
 assert oldread.replace('Some audit-only paths refer to the original workspace;',ins+'Some audit-only paths refer to the original workspace;')==newread
 (OWN/'DRAFT_TO_CURRENT_README.diff').write_text(''.join(difflib.unified_diff(oldread.splitlines(True),newread.splitlines(True),fromfile='historical/README.md',tofile='current/README.md')))
 om=json.loads(oz.read('FILE_MANIFEST.json'));nm=json.loads(nz.read('FILE_MANIFEST.json'))
 oldpins={p['path']:p for p in om['files']};newpins={p['path']:p for p in nm['files']};assert len(newpins)==112 and set(oldpins)==set(newpins)
 pinchanges=[name for name in oldpins if oldpins[name]!=newpins[name]];assert set(pinchanges)=={'README.md','manuscript/critical_wave_growth.tex'}
 topl=[{'key':key,'historical':om.get(key),'current':nm.get(key)} for key in set(om)|set(nm) if key!='files' and om.get(key)!=nm.get(key)]
 assert all(q['key'] in ('utc','created_utc','generated_utc','prepared_utc') for q in topl),topl
 (OWN/'DRAFT_TO_CURRENT_FILE_MANIFEST.diff').write_text(''.join(difflib.unified_diff(oz.read('FILE_MANIFEST.json').decode().splitlines(True),nz.read('FILE_MANIFEST.json').decode().splitlines(True),fromfile='historical/FILE_MANIFEST.json',tofile='current/FILE_MANIFEST.json')))
 (OWN/'ARCHIVE_DELTA.json').write_text(json.dumps({'utc':utc,'archive_files':113,'manifest_payload_pins':112,'archive_changed_files':changed,'archive_unchanged_files_count':len(unchanged),'archive_unchanged_files':unchanged,'manifest_changed_pins':pinchanges,'manifest_changed_top_level_informational_fields':topl,'exact_four_editorial_refinements_only':True,'all_checkers_receipts_proof_priority_records_originals_unchanged':True},indent=2)+'\n')
assert (BASE/'metadata.json').read_bytes()==(HIST/'metadata.json').read_bytes()
assert (BASE/'deposit.json').read_bytes()==(HIST/'deposit.json').read_bytes()
report={'utc':utc,'completion_percent':30,'current_frozen_files':inputs,'history_preservation_all_7_pins_match':True,'old_fresh_review_01_manifest_sha256':sha(original_review_manifest.read_bytes()),'old_fresh_review_01_public_records_unchanged':len(old_review['public_authored_relative_paths']),'exact_four_editorials_only':True,'metadata_deposit_unchanged':True,'scientific_equations_quantifiers_priority_claims_byte_unchanged_except_explicit_credit_wording_narrowing':True,'this_is_addendum_not_replacement_of_old_full_review':True}
(OWN/'INPUT_AND_DELTA_CHECKPOINT.json').write_text(json.dumps(report,indent=2)+'\n')
(OWN/'RESEARCH_LOG.md').write_text('# Editorial delta and revised final-payload review log\n\n'+utc+' — 30% assigned addendum. Exact three TeX replacements and single README insertion verified against preserved original draft; derived manifest changes only two payload pins and informational UTC. 110 archive files unchanged, all checkers/receipts/proof/priority/originals byte unchanged. Current input pins and historical 7 preservation pins verified. Original full-review manifest and all 51 public records remain unchanged. Metadata/deposit unchanged. Remaining: revised independent replays, original native provenance, metadata/current payload equality, all six revised PDF pages and final report/manifest.\n')
print(json.dumps({'utc':utc,'tex_replacements':3,'README_insertion':1,'archive_changed':[p['path'] for p in changed],'archive_unchanged':len(unchanged),'prior_full_review_records_unchanged':51},indent=2))
