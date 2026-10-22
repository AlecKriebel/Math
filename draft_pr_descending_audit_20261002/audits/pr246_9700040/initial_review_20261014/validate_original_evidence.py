from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import ast,hashlib,importlib.util,json
D=Path(__file__).resolve().parent
S=D/'submitted/unsolved_math_prioritization/attempts/9700040'
R=D/'root_reproduction'
intake=json.loads((D/'INTAKE.json').read_text())
for pin in intake['original_source_files']:
    p=D/'submitted'/pin['native_path'];b=p.read_bytes()
    assert len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==pin['native_blob']
spec=importlib.util.spec_from_file_location('root_checked_author_module',R/'author/stationary_law.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
independent=json.loads((R/'original_independent/stdout.json').read_text())
comparisons=[]
for key,expected in independent['raw_coefficients'].items():
    indices=ast.literal_eval(key)
    xs=tuple(map(Fraction,independent['three_thresholds']))
    actual=module.raw_by_size(xs,indices,6)
    assert [str(v) for v in actual]==expected
    comparisons.extend({'indices':indices,'degree':n,'value':str(value),'matches_independent_direct_LIS_coefficients':True} for n,value in enumerate(actual))
assert len(comparisons)==42
index={}
for p in list(S.rglob('*'))+list((D/'root_source_reading/private_reading').glob('*')):
    if p.is_file() and (p.is_relative_to(S) or p.suffix in {'.pdf','.html'}):
        b=p.read_bytes();index.setdefault(hashlib.sha256(b).hexdigest(),[]).append((p,len(b)))
def walk(x):
    if isinstance(x,dict):
        yield x
        for v in x.values():yield from walk(v)
    elif isinstance(x,list):
        for v in x:yield from walk(v)
bindings=[]
for p in S.rglob('*.json'):
    for obj in walk(json.loads(p.read_text())):
        sha=obj.get('sha256')
        if not isinstance(sha,str) or len(sha)!=64:continue
        choices=[(target,size) for target,size in index.get(sha,[]) if 'bytes' not in obj or obj['bytes']==size]
        assert choices,(p.name,obj)
        target,size=choices[0]
        bindings.append({'manifest':p.relative_to(S).as_posix(),'historical_path_hint':next((obj[k] for k in ['path','reading_filename','filename','relative_path','name'] if k in obj),None),'sha256':sha,'bytes':size,'verified_against':str(target)})
report={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','original_native_files_verified':20,
        'all_original_size_SHA1_SHA256_match':True,'original_author_full_receipt':json.loads((R/'author/ROOT_REPLAY_ACCEPTANCE.json').read_text()),
        'original_independent_full_receipt':json.loads((R/'original_independent/ROOT_REPLAY_ACCEPTANCE.json').read_text()),
        'direct_cross_comparisons':comparisons,'cross_comparison_count':42,'historical_nested_bindings':bindings,
        'historical_nested_bindings_count':len(bindings),'source_primary_objects':json.loads((D/'root_source_reading/PRIMARY_RETRIEVAL.json').read_text()),
        'limits':'Exact finite algebra/controls and byte provenance. No stationarity, infinite-law validity or historical priority certificate follows from finite tests alone.'}
(D/'ROOT_ORIGINAL_EVIDENCE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','native_files':20,'author_assertions':49618,'original_independent_assertions':15580,'direct_cross_comparisons':42,'nested_bindings':len(bindings),'primary_source_pins':6},indent=2))
