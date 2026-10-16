"""Reproduce all newly authored finite controls in private, immutable copies."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,subprocess
A=Path(__file__).resolve().parent
PY=A.parents[1]/'audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
PRIVATE=A/'tmp/root_family_controls';PRIVATE.mkdir(parents=True,exist_ok=True)
STREAMS=A/'root_family_control_streams';STREAMS.mkdir(exist_ok=True)
specs=[('hyperbolic','hyperbolic_arithmetic_review','hyperbolic_family_controls.py','replay_artifacts/hyperbolic_family_controls.stdout.txt',3988),
       ('surgery','surface_surgery_review','geometric_controls.py','GEOMETRIC_CONTROL_RECEIPT.json',3775),
       ('combinatorial','combinatorial_metric_review','independent_controls.py','outputs/independent_controls.json',None),
       ('whole','clean_final_adversary','independent_controls.py','INDEPENDENT_CONTROLS.json',38179)]
def sha(b):return hashlib.sha256(b).hexdigest()
def run(spec):
    label,family,code,expected_name,count=spec
    raw=(A/family/code).read_bytes();dest=PRIVATE/label;dest.mkdir(exist_ok=True)
    (dest/code).write_bytes(raw)
    r=subprocess.run([str(PY),code],cwd=dest,capture_output=True)
    (STREAMS/(label+'.stdout')).write_bytes(r.stdout)
    (STREAMS/(label+'.stderr')).write_bytes(r.stderr)
    assert r.returncode==0 and r.stderr==b'',(label,r.returncode,r.stderr)
    actual=json.loads(r.stdout);expected=json.loads((A/family/expected_name).read_bytes())
    ignored=[]
    if label=='surgery':
        ignored=['completed_utc']
        assert actual['completed_utc']!=expected['completed_utc']
        ac={k:v for k,v in actual.items() if k not in ignored}
        ex={k:v for k,v in expected.items() if k not in ignored}
    else:ac,ex=actual,expected
    assert ac==ex,label
    if count is not None:assert actual['assertions']==count
    assert actual['status']=='PASS'
    return {'family':label,'program':family+'/'+code,'program_bytes':len(raw),'program_sha256':sha(raw),
            'exit':r.returncode,'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),
            'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr),'complete_parsed_stdout':actual,
            'complete_expected_json':expected,'all_mathematical_and_scope_fields_equal':True,
            'only_excluded_fields':ignored,'historical_source_hashes_recertified':False}
rows=list(concurrent.futures.ThreadPoolExecutor(4).map(run,specs))
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS',
     'replays':rows,'new_control_assertions':sum(r['complete_parsed_stdout']['assertions'] for r in rows),
     'universal_proofs_audited_before_programs':True,
     'scope':'Finite exact controls supplement separately sealed universal proofs; they do not prove novelty or answer original Question 4.'}
(A/'root_family_control_reproduction.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','families':[(r['family'],r['complete_parsed_stdout']['assertions']) for r in rows],
                  'total':out['new_control_assertions'],'all_full_json_equal_except_one_utc':True},indent=2))
