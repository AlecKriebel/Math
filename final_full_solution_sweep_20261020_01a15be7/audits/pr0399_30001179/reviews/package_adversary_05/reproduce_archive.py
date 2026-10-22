#!/usr/bin/env python3
"""Fresh extracted archive replay and independent semantic mutation attacks."""
import hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
O=Path(__file__).resolve().parent;A=O.parents[1];P=A.parents[1]/'private/pr0399_package05';bundle=P/'archive/free-product-tensor-core-verification'
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v:raise RuntimeError(m)
def run(program,arguments=(),optimized=False,inherited=False):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
    if inherited:env['PYTHONOPTIMIZE']='2'
    command=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(program)]+list(map(str,arguments))
    r=subprocess.run(command,cwd=P,env=env,capture_output=True,text=True)
    return {'command':command,'inherited_optimization':inherited,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'stdout_sha256':sha(r.stdout.encode())}
def rehash(root):
    p=root/'FILES.json';m=json.loads(p.read_bytes())
    for e in m['files']:
        b=(root/e['path']).read_bytes();e.update(bytes=len(b),sha256=sha(b))
    p.write_text(json.dumps(m,indent=2)+'\n')
def main():
    results={'archive_baselines':[],'archive_negative_suite':[],'semantic_mutants':[],'independent_analytic':[],'independent_analytic_mutants':[]}
    for optimized,inherited in [(False,False),(False,True),(True,True)]:
        r=run(bundle/'tools/reproduce.py',[bundle],optimized,inherited);require(r['returncode']==0,'archive baseline');results['archive_baselines'].append(r)
    require(len({r['stdout_sha256'] for r in results['archive_baselines']})==1,'baseline outputs identical')
    for optimized in [False,True]:
        r=run(bundle/'tools/test_integrity_controls.py',[P/'negative_temp'],optimized,True);require(r['returncode']==0,'27 integrity controls');value=json.loads(r['stdout']);require(value['rejected_mutations']==27 and value['positive_fixtures']==2,'counts');results['archive_negative_suite'].append(r)
        r=run(O/'analytic_checks.py',optimized=optimized);require(r['returncode']==0,'independent analytic baseline');results['independent_analytic'].append(r)
        for mutation in ['drop-prefix','wrong-scale','reverse-core','wrong-adjoint']:
            r=run(O/'analytic_checks.py',['--mutant',mutation],optimized);require(r['returncode']!=0,'independent mutant accepted');results['independent_analytic_mutants'].append(r)
        for mutation in ['historical_assertion','family_semantic_type']:
            root=P/('archive_mutant_'+mutation+('_optimized' if optimized else '_normal'));shutil.copytree(bundle,root)
            if mutation=='historical_assertion':
                p=root/'original/check_density_chain.py';p.write_text(p.read_text()+"\nassert False, 'PACKAGE05_NESTED_SENTINEL'\n")
                p0=root/'original/PUBLIC_PACKET_MANIFEST.json';m=json.loads(p0.read_bytes());b=p.read_bytes();m['files']['check_density_chain.py'].update(bytes=len(b),sha256=sha(b));p0.write_text(json.dumps(m,indent=2)+'\n')
            else:
                p=root/'reviews/measure_ordinal/independent_controls.py';body=p.read_text();needle='"exact_finite_checks": checks';require(needle in body,'exact mutant insertion point');p.write_text(body.replace(needle,'"exact_finite_checks": float(checks)',1))
            rehash(root)
            integrity=run(root/'tools/integrity.py',[root],optimized,True);require(integrity['returncode']==0,'mutant must pass byte integrity')
            r=run(root/'tools/reproduce.py',[root],optimized,True);require(r['returncode']!=0,'semantic mutant accepted')
            if mutation=='historical_assertion':require('PACKAGE05_NESTED_SENTINEL' in r['stderr'],'nested historical assertion actually executes')
            results['semantic_mutants'].append({'mutation':mutation,'integrity':integrity,'replay':r})
    require(results['independent_analytic'][0]['stdout']==results['independent_analytic'][1]['stdout'],'own analytic normal/O identical')
    (O/'ARCHIVE_AND_ANALYTIC_REPRODUCTION.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps({'archive_baselines':len(results['archive_baselines']),'baseline_stdout_sha256':results['archive_baselines'][0]['stdout_sha256'],'integrity_negative_cases_per_mode':27,'positive_fixtures_per_mode':2,'semantic_mutants_rejected':len(results['semantic_mutants']),'independent_analytic_mutants_rejected':len(results['independent_analytic_mutants'])},indent=2))
if __name__=='__main__':main()
