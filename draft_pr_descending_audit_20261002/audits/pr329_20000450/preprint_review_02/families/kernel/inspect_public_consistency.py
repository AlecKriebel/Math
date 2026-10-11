"""Read-only exact portability, archive and independent coefficient comparison."""
from pathlib import Path
import datetime, difflib, hashlib, json
import sympy as S

audit=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr329_20000450')
root=Path(__file__).resolve().parent
archive=audit/'preprint_review_02/phase3/archive_replay'
pub=audit/'preprint/verification_v03'
sha=lambda b:hashlib.sha256(b).hexdigest()
guard='# Public export: optimization must not disable scientific assertions.\nimport sys\nif sys.flags.optimize:\n    raise SystemExit("Verification refuses Python optimization (-O/-OO).")\n'
records={};diffs={}
for name in ['division_chord','division_model','division_finite','division_quintic']:
    rec=json.loads((pub/'PORTABILITY.json').read_bytes())['programs'][name]
    original=(audit/rec['original_path']).read_bytes()
    exported=(pub/'programs'/f'{name}.py').read_bytes()
    archived=(archive/'programs'/f'{name}.py').read_bytes()
    assert sha(original)==rec['original_sha256'] and len(original)==rec['original_bytes']
    assert sha(exported)==rec['exported_sha256'] and archived==exported
    plain=exported.decode().replace(guard,'',1)
    diff=''.join(difflib.unified_diff(original.decode().splitlines(keepends=True),plain.splitlines(keepends=True),fromfile=rec['original_path'],tofile='export_after_guard_removal'))
    if name!='division_quintic':assert plain.encode()==original
    diffs[name]=diff
    records[name]={'original_sha256':sha(original),'exported_sha256':sha(exported),'archive_equal':True,
                   'guard_only':name!='division_quintic','declared_changes':rec['changes'],
                   'version_sha256':{v:sha((audit/f'preprint/verification_{v}/programs/{name}.py').read_bytes()) for v in ['v01','v02','v03']}}
# Two JSON records in our exact native stdout; second is complete algebra output.
raw=(root/'native/kernel_exact_v01/stdout.bin').read_text();dec=json.JSONDecoder()
first,n=dec.raw_decode(raw);second,_=dec.raw_decode(raw[n:].lstrip())
expected=json.loads((archive/'expected/division_chord.json').read_bytes())
x,beta=S.symbols('x beta')
for j,co in enumerate(expected['Tate_remainder_coefficients']):
    assert S.expand(S.sympify(co,locals={'beta':beta})-S.sympify(second['residual_coefficients'][str(10-j)],locals={'beta':beta}))==0
for key in ['third_from_chord','fourth_over_2v_from_chord']:
    assert key in expected
port1=json.loads((audit/'preprint/verification_v01/PORTABILITY.json').read_bytes())
port2=json.loads((audit/'preprint/verification_v02/PORTABILITY.json').read_bytes())
port3=json.loads((pub/'PORTABILITY.json').read_bytes())
assert all(port1['programs'][n]==port2['programs'][n]==port3['programs'][n] for n in records)
inputs=audit/'preprint/qualification_v03/inputs'
print(json.dumps({'status':'CONSISTENCY_PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'candidate_input_sha256':{n:sha((inputs/n).read_bytes()) for n in ['manuscript.tex','manuscript.pdf','zenodo-deposit.json','verification.zip']},
 'program_records':records,'public_derivative_diffs_after_guard_removal':diffs,
 'expected_R_coefficients_match_our_fresh_Vieta_derivation':True,
 'portability_entries_for_four_programs_unchanged_across_v01_v02_v03':True,
 'limits':'Static proof/code/record consistency. Parent conducts fresh program replay. Quintic checker is conditional on the packaged coefficient record; verify.py independently reconstructs and compares that record before quintic use.'},indent=2))
