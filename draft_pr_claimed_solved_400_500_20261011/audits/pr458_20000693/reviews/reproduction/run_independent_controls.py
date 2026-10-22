#!/usr/bin/env python3
"""Execute independent audit in both modes and actual mutated subprocesses."""
import concurrent.futures,hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CODE=(ROOT/'verify_independent.py').read_text()
PRIVATE=ROOT/'private_cases/independent_controls';PRIVATE.mkdir(parents=True,exist_ok=True)
MUTANTS=[
 ('primitive_collision',"require(exponent(CASES[2])==F(4),", "require(exponent(CASES[2])==F(2),"),
 ('conjugate_collision',"require(exponent(CASES[4])==F(34,16),", "require(exponent(CASES[4])==F(4),"),
 ('wrong_deletion',"==F(1,6),'deletion ratio'", "==F(1,5),'deletion ratio'"),
 ('separate_expectations',"==F(9,8),'correlated local expectation'", "==F(9,4),'correlated local expectation'"),
 ('wrong_Barnes',"mp.mpf(1)/12)<", "mp.mpf(1)/13)<"),
 ('theorem_scope_false_claim',"ASYMPTOTIC_PROVED=False", "ASYMPTOTIC_PROVED=True"),
 ('missing_restoration',"restored=[(actual(n,Q,p),a) for n,q,a in rows]+[(primitive(n,p),a) for n,q,a in rows if Q%p==0 and q%p!=0]", "restored=[(actual(n,Q,p),a) for n,q,a in rows]"),
 ('wrong_regularization_sign',"for n,a in g.items() for m,c in g.items()]", "for n,a in g.items() for m,c in g.items()]"),
 ('negative_weight',"('one',1,F(5,4)),('quad3',15,F(1,4))", "('one',1,F(-5,4)),('quad3',15,F(1,4))"),
]
# Give the regularization mutation an unambiguous genuinely different target.
MUTANTS[7]=('wrong_regularization_sign',"))),-a*c) for n,a", "))),a*c) for n,a")
def run(case,code,mode,positive):
 path=PRIVATE/(case+'_'+mode+'.py');path.write_text(code)
 env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 if mode=='optimized':env['PYTHONOPTIMIZE']='1'
 result=subprocess.run([sys.executable,str(path)],cwd=PRIVATE,env=env,capture_output=True,timeout=240)
 record={'case':case,'mode':mode,'returncode':result.returncode,'positive_baseline':positive,
 'expected_outcome_obtained':result.returncode==0 if positive else result.returncode!=0,
 'stdout_bytes':len(result.stdout),'stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),
 'stderr':result.stderr.decode(errors='replace'),'code_sha256':hashlib.sha256(code.encode()).hexdigest()}
 if positive and result.returncode==0:
  (ROOT/('INDEPENDENT_CHECKS_'+mode.upper()+'.json')).write_bytes(result.stdout)
  report=json.loads(result.stdout);record['total_cases']=report['total_cases'];record['counts_by_family']=report['counts_by_family']
 return record
jobs=[('baseline',CODE,m,True) for m in ('normal','optimized')]
for case,old,new in MUTANTS:
 if CODE.count(old)!=1 or old==new:raise RuntimeError('invalid mutation definition '+case)
 mutated=CODE.replace(old,new)
 jobs += [(case,mutated,m,False) for m in ('normal','optimized')]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(lambda a:run(*a),jobs))
positive=[r for r in records if r['positive_baseline']]
report={'reviewer':'/root/pr458_reproduction','pr':458,'problem_id':'20000693','frozen_head':'87a39f7b4e5ef81aacf98464f86586cc95684d7f',
 'suite_sha256':hashlib.sha256(CODE.encode()).hexdigest(),'positive_mode_outputs_byte_identical':len(positive)==2 and positive[0]['stdout_sha256']==positive[1]['stdout_sha256'],
 'negative_cases_per_mode':len(MUTANTS),'all_expected_outcomes_obtained':all(r['expected_outcome_obtained'] for r in records),
 'negative_rejected_normal':sum(r['returncode']!=0 for r in records if not r['positive_baseline'] and r['mode']=='normal'),
 'negative_rejected_optimized':sum(r['returncode']!=0 for r in records if not r['positive_baseline'] and r['mode']=='optimized'),'records':records}
(ROOT/'INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='records'},indent=2))
