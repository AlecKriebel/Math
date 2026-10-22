"""Read-only integrity audit of the copied complete package."""
from pathlib import Path
import hashlib, json, stat, zipfile

HERE = Path(__file__).resolve().parent
HOME = HERE/'extracted/congestion-fragmentation-verification'
def sha(data): return hashlib.sha256(data).hexdigest()
def check_file(path, entry):
    data=path.read_bytes()
    assert len(data)==entry['bytes'], str(path)
    assert sha(data)==entry['sha256'], str(path)
    return len(data)

with zipfile.ZipFile(HERE/'bound/congestion-fragmentation-verification.zip') as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(set(z.namelist()))==138
    for info in z.infolist():
        p=Path(info.filename)
        assert not p.is_absolute() and '..' not in p.parts
        assert not stat.S_ISLNK(info.external_attr >>16)
        assert not info.is_dir()
manifest=json.loads((HOME/'MANIFEST.json').read_text())
actual={str(p.relative_to(HOME)) for p in HOME.rglob('*') if p.is_file()}
assert set(manifest['files'])==actual-{'MANIFEST.json'}
checks=[]
for name,entry in manifest['files'].items():
    check_file(HOME/name,entry)
checks.append({'manifest':'MANIFEST.json','verified_files':len(manifest['files']),'exact_payload_set':True})
for manifest_path in sorted(HOME.rglob('*MANIFEST.json')):
    if manifest_path==HOME/'MANIFEST.json':continue
    obj=json.loads(manifest_path.read_text());entries=obj.get('files')
    if not entries:continue
    rows=entries.items() if isinstance(entries,dict) else ((x['path'],x) for x in entries)
    count=0
    for name,entry in rows:
        check_file(manifest_path.parent/name,entry);count+=1
    checks.append({'manifest':str(manifest_path.relative_to(HOME)),'verified_files':count})
support=json.loads((HOME/'support-manifest.json').read_text())
for row in support['files']:check_file(HOME/row['path'],row)
checks.append({'manifest':'support-manifest.json','verified_files':len(support['files'])})
selection=json.loads((HOME/'PUBLICATION_FILES.json').read_text())['files']
assert set(selection)==set(x['path'] for x in support['files'])|{'support-manifest.json'}
assert (HOME/'paper/main.tex').read_bytes()==(HERE/'bound/congestion-fragmentation.tex').read_bytes()
assert (HOME/'publication-metadata.json').read_bytes()==(HERE/'bound/zenodo-deposit.json').read_bytes()
release=json.loads((HERE/'bound/RELEASE_FILES.json').read_text())
for row in release['files']:check_file(HERE/'bound'/row['path'],row)
assert len(release['files'])==5
binding=json.loads((HOME/'candidate-binding.json').read_text())
assert {x['path'] for x in binding['files']}=={str(p.relative_to(HOME/'candidate')) for p in (HOME/'candidate').rglob('*') if p.is_file()}
for row in binding['files']:check_file(HOME/'candidate'/row['path'],row)
policy=json.loads((HOME/'comparison-policy.json').read_text())
assert sum(len(x) for x in policy['float_tolerances'].values())==40
assert 'turn2' not in policy['float_tolerances'] or policy['float_tolerances']['turn2']=={}
for rules in policy['float_tolerances'].values():
    for rule in rules.values():
        assert rule['relative_tolerance']==0
        assert rule['absolute_tolerance']==4*rule['observed_absolute_difference']
for p in HOME.rglob('*'):
    if not p.is_file():continue
    p.read_text()  # Every archive payload is text; full bodies/PDFs are absent.
result={'all_assertions_passed':True,'zip_members':138,'hashed_payloads':137,
        'manifests':checks,'candidate_files':24,'permitted_float_paths':40,
        'all_archive_payloads_utf8_text':True,'source_and_metadata_copies_exact':True}
(HERE/'PACKAGE_INTEGRITY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
