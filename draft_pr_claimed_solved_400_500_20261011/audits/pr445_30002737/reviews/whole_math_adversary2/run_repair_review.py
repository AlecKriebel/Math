#!/usr/bin/env python3
"""Independent actual subprocess review of the exact sealed supported interface.

Only own-folder writes. Foreign original/repair copies and mutants stay private.
Raw commands/stdout/stderr/return modes precede expectation assessment.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,os,shutil,subprocess,sys,tempfile,time

HERE=Path(__file__).resolve().parent
CASE=HERE.parents[1]
REPAIR=CASE/'verification_repair'
PINS={'verify.py':'1c99e09d1e5f13632a02851512e4fc97383fde43f0467a8dbbdbf1bb381954dc',
      'controls_exact.py':'83db2ecfa12dc2f28109b1ec4008c91bfa88f28c4748e23f075ce7fc01ccf581',
      'controls_deterministic.py':'849cfc6ea241317dc5bec94bdcf4af3edbf00b3432fcd2f8f81a08a1ee22ef5e',
      'SOURCE_MANIFEST.json':'e68e9b9338723c3c1c4a1ab8022d1bb6b04ea03a4d8f5d3dd9abbbd3b072a347'}

def require(condition,message):
    if not condition:raise ValueError(message)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2)+'\n')

def execute(name,script,args,optimized,cwd,envbase,out,expect_error=None,expect_false_pass=False):
    env=envbase.copy();env.pop('PYTHONOPTIMIZE',None)
    if optimized:env['PYTHONOPTIMIZE']='1'
    cmd=[sys.executable,str(script),*args];start=time.monotonic()
    r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True,timeout=180)
    value={'name':name,'command':cmd,'utc':datetime.now(timezone.utc).isoformat(),'cwd':str(cwd),
      'inherited_PYTHONOPTIMIZE':env.get('PYTHONOPTIMIZE'),'returncode':r.returncode,
      'stdout':r.stdout,'stderr':r.stderr,'seconds':time.monotonic()-start,'executed_sha256':sha(script),
      'expected_error':expect_error,'expected_historical_false_success':expect_false_pass}
    save(out/(name+'.json'),value)
    if expect_error:
        require(r.returncode!=0 and not r.stdout and expect_error in r.stderr,'incorrect rejection '+name)
    else:
        require(r.returncode==0,'unexpected failed baseline/expected history '+name)
        parsed=json.loads(r.stdout);require(parsed.get('status',parsed.get('verdict')) in ('pass','PASS'),'missing success '+name)
    print(name+': '+str(r.returncode),flush=True)
    return value

def main():
    out=HERE/'records/interface_review'
    require(not out.exists(),'preserve prior run records');out.mkdir(parents=True)
    for file,pin in PINS.items():require(sha(REPAIR/file)==pin,'reviewed pin changed '+file)
    before={str(p.relative_to(REPAIR)):sha(p) for p in REPAIR.rglob('*') if p.is_file() and 'private' not in p.parts and '__pycache__' not in p.parts}
    private=HERE/'private';private.mkdir(exist_ok=True)
    records=[]
    with tempfile.TemporaryDirectory(prefix='independent interface with spaces ',dir=private) as temp:
        work=Path(temp);pkg=work/'reviewed package with spaces';pkg.mkdir()
        for file in PINS:shutil.copyfile(REPAIR/file,pkg/file)
        shutil.copytree(REPAIR/'frozen_history',pkg/'frozen_history')
        cwd=work/'unrelated working directory';cwd.mkdir()
        trap=work/'PATH trap';trap.mkdir();fake=trap/'python3';fake.write_text('#!/bin/sh\nexit 93\n');fake.chmod(0o755)
        env=os.environ.copy();env['PATH']=str(trap)+os.pathsep+env.get('PATH','')
        faults={'marker':'Marker is ambiguous','correlation':'Occupancy coefficient differs','normalization':'normalization fails',
          'flow':'Floor-bin triangle fails','cocycle':'Suspension action cocycle fails','rs':'RS one-sided substitution/bit coding differs',
          'physical_pairs':'Physical direct/factored pair count differs','subdivision':'Subdivision/triangle section correlation differs',
          'saved_author_semantic':'Saved author result semantic mismatch','saved_independent_semantic':'Saved independent result semantic mismatch'}
        for optimized in (False,True):
            mode='optimized' if optimized else 'normal'
            records.append(execute('baseline_'+mode,pkg/'verify.py',[],optimized,cwd,env,out))
            for fault,reason in faults.items():
                records.append(execute(fault+'_'+mode,pkg/'verify.py',['--diagnostic-fault',fault],optimized,cwd,env,out,reason))
        # Independent fixtures: all inputs are exact copies except the declared bad bytes.
        for variant in ('same_length_proof','missing_result','extra_source','resealed_wrong_result','code_byte'):
            fixture=work/variant;shutil.copytree(pkg,fixture)
            if variant=='same_length_proof':
                f=fixture/'frozen_history/author/attempts/turn_01.md';b=f.read_bytes();f.write_bytes(b'X'+b[1:]);reason='Frozen source hash mismatch'
            elif variant=='missing_result':
                (fixture/'frozen_history/author/checks/verification_results.json').unlink();reason='exact file inventory mismatch'
            elif variant=='extra_source':
                (fixture/'frozen_history/extra.txt').write_text('extra\n');reason='exact file inventory mismatch'
            elif variant=='code_byte':
                f=fixture/'controls_deterministic.py';f.write_bytes(f.read_bytes()+b'\n');reason='Supported control literal hash mismatch'
            else:
                hist=fixture/'frozen_history';f=hist/'author/checks/verification_results.json';v=json.loads(f.read_text());v['density']='300';save(f,v)
                for manifest_file,anchor,isdict in [('author/MANIFEST.json',hist/'author',True),('RELEASE_MANIFEST.json',hist,False)]:
                    f=hist/manifest_file;v=json.loads(f.read_text());rows=v['files'].items() if isdict else ((r['path'],r) for r in v['files'])
                    for rel,row in rows:row.update(bytes=(anchor/rel).stat().st_size,sha256=sha(anchor/rel))
                    save(f,v)
                f=fixture/'SOURCE_MANIFEST.json';v=json.loads(f.read_text())
                for row in v['files']:row.update(bytes=(hist/row['path']).stat().st_size,sha256=sha(hist/row['path']))
                save(f,v);reason='Canonical source manifest literal hash mismatch'
            for optimized in (False,True):
                mode='optimized' if optimized else 'normal'
                records.append(execute(variant+'_'+mode,fixture/'verify.py',[],optimized,cwd,env,out,reason))
        # Genuine original marker failure, segregated from current interface outcomes.
        orig=work/'historical original marker.py';original=CASE/'source_snapshot/unsolved_math_prioritization/attempts/30002737/author/checks/verify_counterexample.py'
        text=original.read_text();old='E = (F(1, 10), F(1, 10))';require(text.count(old)==1,'original variant locator')
        orig.write_text(text.replace(old,'E = (F(1, 6), F(0))'))
        history=[]
        for optimized in (False,True):
            mode='optimized' if optimized else 'normal'
            history.append(execute('original_bad_marker_'+mode,orig,[],optimized,cwd,env,out,
                           None if optimized else 'AssertionError',optimized))
        # Guarded OWN mathematics, with real subprocess wrong variants.
        own=HERE/'controls/independent_whole_controls_guarded.py';ownrecords=[]
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(own.read_text()))),'own essential assert remains')
        for optimized in (False,True):
            mode='optimized' if optimized else 'normal'
            ownrecords.append(execute('own_baseline_'+mode,own,[],optimized,cwd,env,out))
            for fault in ('marker','physical_pairs','section'):
                ownrecords.append(execute('own_'+fault+'_'+mode,own,['--diagnostic-fault',fault],optimized,cwd,env,out,'ValueError'))
    baseline=[json.loads(r['stdout']) for r in records if r['name'].startswith('baseline')]
    for b in baseline:del b['runtime']
    require(baseline[0]==baseline[1],'current finite outputs differ')
    after={str(p.relative_to(REPAIR)):sha(p) for p in REPAIR.rglob('*') if p.is_file() and 'private' not in p.parts and '__pycache__' not in p.parts}
    require(before==after,'sealed repair changed')
    save(out/'SUMMARY.json',{'pr':445,'problem_id':30002737,'frozen_head':'3242c84e06db7e99012c7fe581adde5c3f89fc89',
       'reviewer':'/root/pr445_whole_math_adversary2','actual_current_baselines':2,'actual_current_negatives':30,
       'current_negatives_rejected_without_stdout':30,'normal_optimized_finite_results_identical':True,
       'diagnostic_math_and_parsed_semantic_negatives':20,'integrity_negatives':10,
       'historical_original_mutant_runs':2,'historical_normal_rejection':1,'historical_optimized_false_success':1,
       'own_guarded_baselines':2,'own_guarded_negatives_rejected_both_modes':6,
       'original_normal_only_diagnostic_preserved':True,'sealed_repair_files_unchanged':True,
       'current_code_pins':PINS,'raw_record_count':len(records)+len(history)+len(ownrecords),
       'python_executable':sys.executable,'python_version':sys.version,
       'limits':'New supported-interface and own finite-control evidence; never relabels original R1/RR1; no infinite proof or priority certificate'})
    print('Independent interface and owned guarded controls: all expected outcomes observed',flush=True)

if __name__=='__main__':main()
