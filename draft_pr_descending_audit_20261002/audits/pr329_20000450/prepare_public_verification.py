"""Derive a portable public replay set from externally closed PR329 inputs.

No new mathematical formula or original author-turn mutation. Runtime guards
and a local expected-record path are the only exported program changes.
"""
from pathlib import Path
import hashlib,json,re
A=Path(__file__).resolve().parent; B=A/'preprint/verification_v01'
assert not B.exists(); (B/'programs').mkdir(parents=True); (B/'expected').mkdir()
sha=lambda b:hashlib.sha256(b).hexdigest()
guard='#!/usr/bin/env python3\n# Public export: optimization must not disable scientific assertions.\nimport sys\nif sys.flags.optimize:\n    raise SystemExit("Verification refuses Python optimization (-O/-OO).")\n'
items=[
 ('geometry_source',A/'geometry/independent_source_geometry.py','geometry_source_external001','text'),
 ('geometry_quotient',A/'geometry/independent_quotient_geometry.py','geometry_quotient_external001','text'),
 ('geometry',A/'geometry/validate_candidate_geometry.py','geometry_external001','text'),
 ('division_chord',A/'division_polynomial/independent_chord.py','division_chord_external001','json'),
 ('division_model',A/'division_polynomial/independent_model.py','division_model_external001','json'),
 ('division_finite',A/'division_polynomial/independent_finite.py','division_finite_external001','json'),
 ('division_quintic',A/'division_polynomial/independent_quintic_factors.py','division_quintic_external001','json'),
 ('arithmetic',A/'arithmetic/check_arithmetic.py','arithmetic_system_external001','json'),
 ('candidate',A/'snapshot/unsolved_math_prioritization/attempts/20000450/verify_turn1.py',None,'json')]
def science(b):
    lines=[]
    for line in b.decode().splitlines():
        if re.fullmatch(r'native_utc(?:_start|_end)? \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+\+00:00',line):continue
        line=re.sub(r' native_utc \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+\+00:00$','',line)
        lines.append(line)
    return ('\n'.join(lines)+'\n').encode()
records={}
for name,p,run,fmt in items:
    original=p.read_bytes(); s=original.decode(); assert '__future__' not in s
    if s.startswith('#!'):s=s.partition('\n')[2]
    changes=['Add explicit assertion-preserving optimization guard; original mathematical body unchanged.']
    if name=='division_quintic':
        old="Path(__file__).parent/'native/independent_generic_chord_final.stdout'"
        assert s.count(old)==1
        s=s.replace(old,"Path(__file__).parent.parent/'expected/division_chord.json'")
        changes.append('Bind independently derived coefficients to packaged expected/division_chord.json instead of the historical private native-record path.')
    exported=(guard+s).encode(); (B/'programs'/(name+'.py')).write_bytes(exported)
    if name=='candidate':
        out=(A/'root_replays_private/author001/stdout.bin').read_bytes()
    else:
        D=A/'root_runs_private'/run; j=json.loads((D/'execution.json').read_bytes())
        assert j['exit_code']==0 and (D/'stderr.bin').read_bytes()==b''
        out=(D/'stdout.bin').read_bytes(); assert sha(out)==j['stdout_sha256']
    if fmt=='json':
        q=json.loads(out)
        if name=='division_chord': assert 'interpreter' in q; del q['interpreter']
        payload=(json.dumps(q,indent=2,sort_keys=True)+'\n').encode()
    else:payload=science(out)
    (B/'expected'/(name+'.'+('json' if fmt=='json' else 'txt'))).write_bytes(payload)
    records[name]=dict(original_path=str(p.relative_to(A)),original_bytes=len(original),original_sha256=sha(original),
        exported_sha256=sha(exported),changes=changes,expected_format=fmt,
        output_comparison='Full mathematical JSON; only interpreter provenance omitted.' if name=='division_chord' else
        ('Complete text after only declared UTC metadata removal.' if fmt=='text' else 'Complete mathematical JSON, with no field omissions.'))
for mutant in ['drop_twist','wrong_radical','wrong_cyclotomic','wrong_norm_degree']:
    D=A/'root_runs_private'/('arithmetic_system_'+mutant+'_external001')
    j=json.loads((D/'execution.json').read_bytes()); assert j['exit_code']==1
    assert (D/'stderr.bin').read_bytes()==b''
    (B/'expected'/('mutant_'+mutant+'.json')).write_text(json.dumps(json.loads((D/'stdout.bin').read_bytes()),indent=2,sort_keys=True)+'\n')
(B/'PORTABILITY.json').write_text(json.dumps(dict(scope='Derived public exports of frozen original and independent audited programs; all original historical namespaces preserved.',programs=records,
    no_private_primary_redistribution=True,original_author_turn_count='1/5'),indent=2)+'\n')
(B/'requirements.txt').write_text('sympy==1.14.0\n')
print(json.dumps(dict(status='PREPARED_NOT_YET_REPLAYED',programs=len(records),bundle=str(B)),indent=2))
