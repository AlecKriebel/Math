from pathlib import Path
import json,math,hashlib,os
from datetime import datetime,timezone
F=Path(__file__).resolve().parent;R=F.parents[3];C=F.parent/'reviewed_candidate'
def pairs(v):
    d={}
    for k,x in v:
        assert k not in d,('duplicate JSON key',k)
        d[k]=x
    return d
def finite(v):
    x=float(v);assert math.isfinite(x);return x
def bad(v): raise ValueError('Nonfinite JSON constant '+v)
def load(b): return json.loads(b,object_pairs_hook=pairs,parse_float=finite,parse_constant=bad)
def typed_equal(a,b):
    assert type(a) is type(b),(type(a),type(b))
    if isinstance(a,dict):
        assert a.keys()==b.keys()
        for k in a:typed_equal(a[k],b[k])
    elif isinstance(a,list):
        assert len(a)==len(b)
        for x,y in zip(a,b):typed_equal(x,y)
    else: assert a==b
def ref(p):
    b=p.read_bytes();return dict(path=str(p.relative_to(R)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),full_mode=p.stat().st_mode&0o7777)
strict_json=0
for p in sorted(C.rglob('*')):
    if not p.is_file() or p.suffix not in ['.json','.jsonl']:continue
    b=p.read_bytes()
    if p.suffix=='.json':load(b);strict_json+=1
    elif b.strip():
        try:load(b);strict_json+=1
        except json.JSONDecodeError:
            for line in b.splitlines():
                if line.strip():load(line);strict_json+=1
cases=[]
for private,source,output,original,capture,count in [
 ('private_author','verify.py','verification.json','verification.json','AUTHOR_LITERAL_ACTUAL_CAPTURE',69),
 ('private_duplicate','submitted_verify.py','verification.json','review/verification.json','DUPLICATE_LITERAL_ACTUAL_CAPTURE',69),
 ('private_historical_independent','independent_checks.py','independent_results.json','review/independent_results.json','HISTORICAL_INDEPENDENT_LITERAL_ACTUAL_CAPTURE',187)]:
    cp=F/private/source;result=F/private/output; saved=C/original
    q=load((F/capture/'CAPTURE.json').read_bytes())
    assert q['exit_code']==0 and q['actual_execution'] is True and q['completed'] is True and q['source_unchanged'] is True
    original_source=C/('review/'+source if private!='private_author' else source)
    assert cp.read_bytes()==original_source.read_bytes()==(F/capture/'PRELAUNCH_SOURCE.py').read_bytes()
    assert result.read_bytes()==saved.read_bytes();typed_equal(load(result.read_bytes()),load(saved.read_bytes()))
    o=load(result.read_bytes());assert o['passed']==count and o['failed']==0
    cases.append(dict(actual_child=q['pid'],count=count,source=ref(cp),result=ref(result),saved=ref(saved),byte_exact=True,recursive_type_exact=True,independent_math=(private=='private_historical_independent')))
q=dict(schema='pr49-whole-literal-reproduction-and-strict-JSON/v1',status='PASS',actual_pid=os.getpid(),created_utc=datetime.now(timezone.utc).isoformat(),cases=cases,strict_current_JSON_objects=strict_json,originals_and_outputs_byte_type_exact=True,duplicate69_independent=False,no_new_substantive_attempts=True,no_native_writes=True,production_execution=False)
(F/'LITERAL_REPRODUCTION_RESULT.json').write_text(json.dumps(q,indent=2)+'\n')
print(json.dumps(dict(status='PASS',actual_pid=os.getpid(),literal_counts=[v['count'] for v in cases],strict_current_JSON_objects=strict_json)))
