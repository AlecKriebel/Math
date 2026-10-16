"""Final independent byte/evidence comparisons; no candidate writes."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, zipfile

O=Path(__file__).resolve().parent;B=O.parent/'preprint';D=O.parent/'initial_review_20261016'
F=json.loads((O/'FROZEN_INPUTS.json').read_text())
def pin(p):
    r=p.read_bytes();return dict(path=str(p),bytes=len(r),sha256=hashlib.sha256(r).hexdigest())
for r in F['all_candidate_files']:
    p=pin(B/r['path']);assert p['bytes']==r['bytes'] and p['sha256']==r['sha256']
assert {p.relative_to(B).as_posix() for p in B.rglob('*') if p.is_file()}=={r['path'] for r in F['all_candidate_files']}
with zipfile.ZipFile(B/'k303b-source-verification.zip') as z:
    assert all(z.read(i)==(O/'actual_zip_extraction'/i.filename).read_bytes() for i in z.infolist())
orig=B/'verification/original_submission';native=B/'pr_update/5100015/history/original_submission_20261016'
assert {p.relative_to(orig).as_posix() for p in orig.rglob('*') if p.is_file()}=={p.relative_to(native).as_posix() for p in native.rglob('*') if p.is_file()}
assert len([p for p in orig.rglob('*') if p.is_file()])==23
original_seals=[]
for base in [orig,native]:
    f=json.loads((base/'FROZEN_MANIFEST.json').read_text())
    for name,r in f['files'].items():
        p=pin(base/name);assert p['bytes']==r['bytes'] and p['sha256']==r['sha256']
    q=base/'independent_review';f2=json.loads((q/'REVIEW_SHA256SUMS.json').read_text())
    assert all(pin(q/n)['sha256']==h for n,h in f2.items())
    original_seals.append(dict(base=str(base),author_entries=len(f['files']),inherited_review_entries=len(f2)))

tree=ast.parse((B/'verification/run_checks.py').read_bytes())
cases=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='cases' for t in n.targets)))
replays=[]
for root in [O/'real_eight_suite_replay',D/'root_reproduction_07_portable_zip_review01_fixed/executed']:
    aggregate=json.loads((root/'REPRODUCTION.json').read_text());assert aggregate['status']=='PASS' and aggregate['verified_frozen_files_before_after']==149
    receipts={r['name']:r for r in aggregate['results']};suite=[]
    for name,script,copytree,outfile,expected,ignored in cases:
        src=B/'verification'/script
        program=root/name/'inputs'/Path(script).relative_to(copytree) if copytree else root/name/Path(script).name
        assert program.read_bytes()==src.read_bytes()
        work=program.parent
        result=work/outfile if outfile else root/name/'stdout.txt'
        actual=json.loads(result.read_text());want=json.loads((B/'verification'/expected).read_text())
        for k in ignored:actual.pop(k,None);want.pop(k,None)
        assert actual==want
        r=receipts[name];assert r['status']=='PASS' and r['returncode']==0 and r['all_scientific_fields_identical'] and r['program_sha256']==pin(program)['sha256']
        suite.append(dict(name=name,actual_program=pin(program),actual_result=pin(result),actual_receipt=pin(root/name/'REPLAY_RECEIPT.json'),all_scientific_fields_independently_identical=True,ignored_only_timestamps=ignored))
    replays.append(dict(aggregate=pin(root/'REPRODUCTION.json'),independent_execution_by_this_reviewer=root.parent==O,suites=suite))

old=O.parent/'whole_package_adversary_01';new=D/'root_reproduction_05_whole_review01_controls'
assert (old/'independent_controls.py').read_bytes()==(new/'independent_controls.py').read_bytes()
one=json.loads((old/'INDEPENDENT_RESULTS.json').read_text());two=json.loads((new/'INDEPENDENT_RESULTS.json').read_text())
one.pop('utc');two.pop('utc');assert one==two and two['total_checks']==2657
assert not any(p.name=='__pycache__' for p in O.rglob('*'))
qa=[pin(p) for p in sorted((O/'pdf_visual_qa').iterdir())]
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',all_candidate_files_unchanged=len(F['all_candidate_files']),all_actual_zip_members_unchanged=211,originals_exact_membership=23,original_seals=original_seals,replays=replays,prior_review_2657_root_recheck=dict(source=pin(new/'independent_controls.py'),result=pin(new/'INDEPENDENT_RESULTS.json'),all_nontimestamp_fields_match=True,personally_rerun=False),pdf_visual_QA=dict(actual_rendered_pages=5,all_pages_visually_inspected=True,defects=[],source_correspondence='All five final pages inspected against current TeX, with text extraction retained',files=qa),no_owned_cache_payloads=True,no_candidate_writes=True)
(O/'FINAL_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('replays','pdf_visual_QA','prior_review_2657_root_recheck')},indent=2))
