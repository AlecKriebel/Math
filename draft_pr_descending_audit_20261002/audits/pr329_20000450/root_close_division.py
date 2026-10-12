"""Root external scientific closure of the stable division-family namespace."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat
A=Path(__file__).resolve().parent; N=A/'division_polynomial'
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.now(timezone.utc).isoformat()
def pin(p):
    b=p.read_bytes(); return dict(bytes=len(b),sha256=sha(b),mode=f'{stat.S_IMODE(p.stat().st_mode):04o}')
def inventory():
    files={}; directories={}
    for p in sorted(N.rglob('*')):
        assert not p.is_symlink(),str(p)
        if p.is_file(): files[str(p.relative_to(N))]=pin(p)
        elif p.is_dir(): directories[str(p.relative_to(N))]=f'{stat.S_IMODE(p.stat().st_mode):04o}'
    return files,directories
assert not (A/'ROOT_DIVISION_CLOSURE.json').exists()
files,dirs=inventory(); assert len(files)==110
critical={'REPORT.md':'c6fd1861f12a0c3d02c152cab4b6ec79a62c5c329790968975dc75f60ce3666a',
 'verify_review.py':'447ebb62afe7ab62e56e2481063c1d5f26402c25897805966e8ffa34564f812a',
 'OWNED_NAMESPACE_MANIFEST.json':'1a84520309608052602faea9aba6429c627c59dcc6ed131da0f628a9d0cb7ad0',
 'FINAL_PINS.json':'b5d82b6d80de6b6d8653fd7441953664571a82d67647313ab85c73cba128b177'}
for k,h in critical.items(): assert files[k]['sha256']==h,k
owned=json.loads((N/'OWNED_NAMESPACE_MANIFEST.json').read_bytes())
assert {k:v for k,v in files.items() if k!='OWNED_NAMESPACE_MANIFEST.json'}=={
    k:{q:r[q] for q in ['bytes','sha256','mode']} for k,r in owned['files'].items()}
assert dirs==owned['directory_modes']
assert f'{stat.S_IMODE(N.stat().st_mode):04o}'==owned['root_mode']
def execution(name,wanted=0):
    D=A/'root_runs_private'/name; j=json.loads((D/'execution.json').read_bytes())
    assert j['exit_code']==wanted and (D/'stderr.bin').read_bytes()==b''
    for k in ['stdout','stderr']:
        b=(D/(k+'.bin')).read_bytes(); assert len(b)==j[k+'_bytes'] and sha(b)==j[k+'_sha256']
    return j,(D/'stdout.bin').read_bytes()
full,body=execution('division_full_external001'); result=json.loads(body)
assert result['status']=='PASS' and result['scope']=='full' and result['owned_files_checked']==109
assert result['candidate_files_checked']==21 and result['native_receipts_checked']==18
assert len(result['mathematical_replays'])==5
assert all(j['actual_exit']==0 and j['stderr_bytes']==0 and j['complete_mathematical_JSON_matches'] for j in result['mathematical_replays'])
external=[]
for program,rootname,oldstem in [
 ('independent_chord.py','division_chord_external001','independent_generic_chord_final'),
 ('independent_model.py','division_model_external001','independent_model_identities_final'),
 ('independent_finite.py','division_finite_external001','independent_finite_controls'),
 ('independent_quintic_factors.py','division_quintic_external001','independent_quintic_factor_final')]:
    j,b=execution(rootname)
    assert j['programs'][0]['sha256']==files[program]['sha256']
    assert b==(N/'native'/(oldstem+'.stdout')).read_bytes()
    external.append(dict(program=program,actual_execution=j,exact_native_scientific_stdout_equality=True))
M=A/'ROOT_DIVISION_NAMESPACE_MANIFEST.json'
M.write_text(json.dumps(dict(utc=utc(),namespace='division_polynomial',files=files,directories=dirs,
    root_mode=owned['root_mode'],excluded_namespace_files=[],whole_namespace_pinned=True,
    raw_primary_files_private_not_public_package=True),indent=2)+'\n')
j=dict(utc=utc(),status='PASS_ROOT_EXTERNALLY_CLOSED_DIVISION_FAMILY_ONLY',
    root_one_time_external_authorization='Root fully read the corrected final scientific report, source-only and first-assessment gates, primary read scopes, all four current mathematical programs and full native scientific outputs, current capture/verifier/manifest builder, final pins and log. Root independently replayed every scientific program and externally verified the whole stable namespace. Close this family only; no priority or publication approval.',
    namespace_manifest=dict(path=str(M.relative_to(A)),**pin(M)),
    root_full_scientific_reading=True,
    native_reading_limit='All scientific streams used in adjudication fully read. Every18 historical receipt and raw stream is integrity checked by the fully read read-only verifier, with complete110-file bodies and modes pinned; no claim that unrelated raw primary pages or all historical failed-program bodies were independently read for mathematical meaning.',
    full_native_external_execution=full,full_native_verifier_summary=result,
    independently_replayed_scientific_programs=external,
    geometry_prerequisite_externally_closed=pin(A/'ROOT_GEOMETRY_CLOSURE.json'),
    division_family_percent=100,
    strongest_verified_result='Generic chord derivation of every residual fifth-division coefficient; exact resultants, all25 distinct geometric points, all allowed specializations and inverse-chart denominators, actual Tate twist transport and arithmetic cover compatibility.',
    exact_remaining_division_gap='None within the stated normalized characteristic-zero family.',
    source_characterization_correction='Original remark(ii) motivates universal X_1(5) with marked point; full-level X(5) is a separate classical input. Corrected final report was fully read before closure; historical source-only freeze and core code unchanged.',
    entire_candidate_accepted=False,priority_complete=False,publication_ready=False,original_author_turn_count='1/5')
assert inventory()==(files,dirs)
(A/'ROOT_DIVISION_CLOSURE.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(dict(utc=j['utc'],status=j['status'],files=len(files),native_receipts=18,
    independent_programs=len(external),division_percent=100,publication_ready=False),indent=2))
