#!/usr/bin/env python3
"""Read-only audit replay. Pass the original frozen packet as the sole argument.
Prints JSON only; writes no output files or bytecode. In-memory mutants are deliberate.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import stat
import subprocess
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def snapshot(path):
    return {p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                    'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')}
            for p in sorted(path.iterdir()) if p.is_file()}


def denied(path, existing):
    results=[]
    for kind,target,flags in [('new_file',path/'AUDIT_WRITE_PROBE_MUST_NOT_EXIST',os.O_WRONLY|os.O_CREAT|os.O_EXCL),
                              ('existing_file',path/existing,os.O_WRONLY|os.O_APPEND)]:
        try:
            fd=os.open(target,flags,0o600)
        except PermissionError as e:
            results.append({'probe':kind,'result':'DENIED','errno':e.errno,'exception':type(e).__name__})
        else:
            os.close(fd)
            raise RuntimeError('Readonly probe unexpectedly allowed: '+kind)
    return results


def run(flags, original, argv, label, expected_error=None):
    command=[sys.executable,*flags,*argv]
    r=subprocess.run(command,cwd=original,capture_output=True,text=True,
       env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},timeout=60)
    item={'label':label,'mode':'normal' if not flags else flags[0],
          'command':[Path(sys.executable).name,*flags,*(['-c','<in-memory semantic mutation>'] if argv[0]=='-c' else [Path(argv[0]).name])],
          'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
    if expected_error is None:
        require(r.returncode==0,'positive checker failed '+label)
        result=json.loads(r.stdout)
        require(result.get('result')=='PASS' and result.get('uid')==1000,'invalid positive result '+label)
        item['parsed_result']=result
    else:
        require(r.returncode!=0 and ('RuntimeError: '+expected_error) in r.stderr,'semantic mutant not rejected '+label)
        require('"result": "PASS"' not in r.stdout,'semantic mutant printed PASS '+label)
        item['expected_error']=expected_error
        item['semantic_rejection_verified']=True
    return item


def main():
    require(len(sys.argv)==2,'usage: replay_audit.py ORIGINAL_FROZEN_PACKET')
    original=Path(sys.argv[1]).resolve(); audit=Path(__file__).resolve().parent
    require(os.getuid()==1000,'actual UID must be 1000')
    before=snapshot(original); audit_before=snapshot(audit)
    for directory,files in ((original,before),(audit,audit_before)):
        require(stat.S_IMODE(directory.stat().st_mode)==0o555,'directory is not mode 0555')
        require(all(x['mode']=='0444' for x in files.values()),'file is not mode 0444')
    manifest=json.loads((original/'MANIFEST.json').read_text())
    require(set(manifest['files'])==set(before)-{'MANIFEST.json'},'manifest file set differs')
    for name,record in manifest['files'].items():
        require(all(before[name][k]==record[k] for k in ('bytes','sha256')),'original manifest mismatch '+name)
    probes={'original':denied(original,'check_identities.py'),'audit':denied(audit,'independent_checks.py')}
    code=(original/'check_identities.py').read_text()
    mutations=[
      ('reverse_reflection_normal','return dot(sub(x, y), x)/(R*d2) - a/R','return -dot(sub(x, y), x)/(R*d2) - a/R','boundary coefficient identity'),
      ('halve_radial_regulator_correction','return dot(sub(x, y), x)/(R*d2) - a/R','return dot(sub(x, y), x)/(R*d2) - a/(2*R)','boundary coefficient identity'),
      ('reverse_admissible_boundary_sign',"require(actual <= 0, 'boundary sign for a >= 1/2')", "require(actual >= 0, 'boundary sign for a >= 1/2')",'boundary sign for a >= 1/2'),
      ('wrong_inversion_radius_power','expected=R**4*d2*norm2(add(x,y))/(norm2(x)**2*norm2(y)**2)','expected=R**2*d2*norm2(add(x,y))/(norm2(x)**2*norm2(y)**2)','inversion factorization'),
      ('early_contracting_regulator','L_y=max(Q(0),t-Q(1,2));','L_y=max(Q(0),t-Q(1,4));','controlled contracting Y equation'),
      ('halve_circular_moment','integration_by_parts=-Q(2*m*comb(2*m,m),4**m)','integration_by_parts=-Q(m*comb(2*m,m),4**m)','even-power circular integral'),
      ('accept_product_stationarity',"require(mean_dx == 2 and mean_dx**2 == 4, 'product-uniform generator witness')", "require(mean_dx == 2 and mean_dx**2 == 0, 'product-uniform generator witness')",'product-uniform generator witness')]
    mutation_records=[]
    for name,old,new,error in mutations:
        require(code.count(old)==1,'mutation not unique '+name)
        changed=code.replace(old,new,1)
        mutation_records.append({'name':name,'original_fragment':old,'mutated_fragment':new,
          'mutated_sha256':hashlib.sha256(changed.encode()).hexdigest(),'expected_error':error})
    runs=[]; negative=[]
    for flags in ([],['-O'],['-OO']):
        runs.append(run(flags,original,[str(original/'check_identities.py')],'original_checker'))
        runs.append(run(flags,original,[str(audit/'independent_checks.py')],'independent_checker'))
        for (name,old,new,error),record in zip(mutations,mutation_records):
            changed=code.replace(old,new,1)
            script="exec(compile("+repr(changed)+", "+repr('<semantic-'+name+'>')+", 'exec'), {'__name__':'__main__'})"
            negative.append(run(flags,original,['-c',script],name,error))
    after=snapshot(original); audit_after=snapshot(audit)
    require(before==after,'original frozen bytes or modes changed')
    require(audit_before==audit_after,'audit bytes or modes changed during runs')
    print(json.dumps({'result':'PASS','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'actual_uid':os.getuid(),'actual_gid':os.getgid(),'python_version':sys.version,
      'directory_modes':{'original':'0555','audit':'0555'},'denied_write_probes':probes,
      'original_manifest_verified':True,'original_before':before,'original_after':after,
      'original_unchanged':True,'audit_before':audit_before,'audit_after':audit_after,'audit_unchanged_during_runs':True,
      'positive_runs':runs,'mutations':mutation_records,'semantic_negative_control_runs':negative,
      'summary':{'positive_runs':len(runs),'semantic_negative_runs':len(negative),'all_expected_results':True},
      'scope':'Finite exact algebra and mutation-sensitivity tests, not stochastic or global-proof certification.'},indent=2))


if __name__=='__main__':
    main()
