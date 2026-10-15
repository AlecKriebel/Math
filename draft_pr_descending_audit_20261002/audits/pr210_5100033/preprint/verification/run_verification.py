#!/usr/bin/env python3
"""Portable nine-job replay, with strict integrity and scientific JSON equality."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,copy,hashlib,json,os,shutil,subprocess,sys,tempfile,time
from integrity import BASE,digest,verify
from validate_payloads import archive_checks,result_checks,PRIMARY_HASHES

# Only top-level non-scientific metadata may differ. No recursive/key-name filter.
EXCLUSIONS={
 'source_domain':{'python':'interpreter version only'},
 'meromorphic_divisor':{'utc_start':'wall-clock timestamp','utc_end':'wall-clock timestamp','runtime':'absolute interpreter path','python':'interpreter build/version only'},
 'priority_author':{'utc':'wall-clock timestamp'},
 'priority_classical':{'python':'interpreter build/version only'},
}
JOBS={
 'author':('original_submission/verify.py','original_submission/verification.json','stdout'),
 'inherited':('original_submission/independent_review/independent_check.py','original_submission/independent_review/INDEPENDENT_CHECKS.json','stdout'),
 'source_domain':('audits/source_domain_adversary_01/fresh_control.py','audits/source_domain_adversary_01/FRESH_CONTROL.json','stdout'),
 'physical_geometry':('audits/physical_geometry_adversary_01/physical_geometry_check.py','audits/physical_geometry_adversary_01/results.json','stdout'),
 'meromorphic_divisor':('audits/meromorphic_divisor_adversary_01/check_meromorphic.py','audits/meromorphic_divisor_adversary_01/results.json','meromorphic'),
 'priority_author':('audits/priority_author_updates_01/exact_pedal_inverse_control.py','audits/priority_author_updates_01/EXACT_CONTROL_RESULTS.json','EXACT_CONTROL_RESULTS.json'),
 'priority_classical':('audits/priority_classical_general_01/check_controls.py','audits/priority_classical_general_01/CONTROL_RESULTS.json','CONTROL_RESULTS.json'),
 'root_exact_geometry':('scope_controls/root_exact_geometry_controls.py','scope_controls/ROOT_EXACT_GEOMETRY_CONTROLS.json','stdout'),
 'root_projective':('scope_controls/root_priority_projective_control.py','scope_controls/ROOT_PRIORITY_PROJECTIVE_CONTROL.json','stdout'),
}

def utc():return datetime.now(timezone.utc).isoformat()
def copy_input(source,target):
    target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    if digest(source)!=digest(target):raise ValueError('Input copy changed bytes')
def normalize(data,job):
    out=copy.deepcopy(data)
    for key in EXCLUSIONS.get(job,{}):
        if key not in out:raise ValueError('Missing explicitly excluded metadata: '+key)
        del out[key]
    return out

def differences(a,b,path='$'):
    if type(a) is not type(b):return [path+' (type)']
    if isinstance(a,dict):
        if set(a)!=set(b):return [path+' (keys)']
        return [x for k in sorted(a) for x in differences(a[k],b[k],path+'.'+k)]
    if isinstance(a,list):
        if len(a)!=len(b):return [path+' (length)']
        return [x for i,(aa,bb) in enumerate(zip(a,b)) for x in differences(aa,bb,path+'['+str(i)+']')]
    return [] if a==b else [path]

def replay(job,primary_dir):
    source,frozen,output=JOBS[job];start=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='pr210-'+job+'-') as name:
        work=Path(name);script=work/Path(source).name
        primary_mode='not applicable';substituted={}
        if job=='meromorphic_divisor':
            mirror=work/'audits/pr210_5100033/initial_review_20261015'
            script=mirror/'meromorphic_divisor_adversary_01/check_meromorphic.py'
            copy_input(BASE/'audit_receipts/INTAKE.json',mirror/'INTAKE.json')
            native=Path('submitted/unsolved_math_prioritization/attempts/5100033')
            for rel in ['PROOF.md','SOURCES.md','source_manifest.json']:
                copy_input(BASE/'original_submission'/rel,mirror/native/rel)
            out=work/'fresh_meromorphic.json'
            if primary_dir:
                primary_mode='genuine external primary files freshly hashed; unchanged script executed directly'
                pdfs=work/'audits/pr211_5100063/initial_review_20261015/private_reading'
                for rel,expected in PRIMARY_HASHES.items():
                    path=primary_dir/rel
                    if digest(path)!=expected:raise ValueError('Primary PDF hash mismatch: '+rel)
                    copy_input(path,pdfs/rel)
                command=[sys.executable,'-B',str(script),'--output',str(out)]
            else:
                primary_mode='attested PDF hash preflight; no fresh external PDF hashing'
                substituted=dict(PRIMARY_HASHES)
                adapter=work/'meromorphic_source_preflight.py'
                copy_input(BASE/'meromorphic_source_preflight.py',adapter)
                command=[sys.executable,'-B',str(adapter),str(script),str(out)]
        else:
            command=[sys.executable,'-B',str(script)]
            out=work/output if output!='stdout' else None
        copy_input(BASE/source,script)
        if job=='author':copy_input(BASE/'original_submission/PROOF.md',work/'PROOF.md')
        env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
        completed=subprocess.run(command,cwd=work,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if completed.returncode:
            raise RuntimeError(job+' exited '+str(completed.returncode)+'\n'+completed.stderr.decode(errors='replace')[-6000:])
        raw=completed.stdout if output=='stdout' else out.read_bytes()
        actual=json.loads(raw);expected_raw=(BASE/frozen).read_bytes();expected=json.loads(expected_raw)
        mismatch=differences(normalize(expected,job),normalize(actual,job))
        if mismatch:raise ValueError(job+' scientific mismatch at '+', '.join(mismatch[:12]))
        rows=result_checks(job,actual)
        data=json.dumps(normalize(actual,job),sort_keys=True,separators=(',',':')).encode()
        return {'job':job,'program_sha256':digest(BASE/source),'frozen_result_sha256':digest(BASE/frozen),'replay_raw_sha256':hashlib.sha256(raw).hexdigest(),'raw_byte_equal':raw==expected_raw,'scientific_JSON_exact_equal':True,'scientific_canonical_sha256':hashlib.sha256(data).hexdigest(),'excluded_top_level_fields':EXCLUSIONS.get(job,{}),'metadata_differences':{k:{'frozen':expected[k],'replay':actual[k]} for k in EXCLUSIONS.get(job,{}) if expected[k]!=actual[k]},'row_validation':rows,'primary_mode':primary_mode,'attested_primary_hash_substitution_count':len(substituted),'attested_primary_hash_substitutions':substituted,'elapsed_seconds':round(time.monotonic()-start,3)}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--list',action='store_true')
    p.add_argument('--integrity-only',action='store_true')
    p.add_argument('--run',choices=['all']+list(JOBS),default='all')
    p.add_argument('--primary-dir',type=Path,help='reader-supplied directory with the three exact PDFs; never downloaded')
    p.add_argument('--receipt',type=Path,help='optional result receipt OUTSIDE this sealed folder')
    p.add_argument('--manifest',type=Path,help='trial inventory outside folder; default sealed MANIFEST.json')
    args=p.parse_args()
    if not __debug__ or sys.flags.optimize:raise RuntimeError('Refusing -O/-OO: assertions must be enabled')
    if args.receipt and (args.receipt.resolve()==BASE or BASE in args.receipt.resolve().parents):raise ValueError('Receipt must be outside sealed package')
    before=verify(args.manifest);archives=archive_checks()
    if args.list:
        for name,(script,frozen,_) in JOBS.items():print(name+'\t'+script+'\t'+frozen)
        return
    if args.integrity_only:
        print(json.dumps({'integrity':before,'archives':archives},indent=2));return
    import sympy,mpmath
    if sympy.__version__!='1.14.0' or mpmath.__version__!='1.3.0':raise RuntimeError('Requires exactly SymPy 1.14.0 and mpmath 1.3.0')
    selected=list(JOBS) if args.run=='all' else [args.run]
    receipt={'schema':'PR210-portable-reproduction-v1','utc_start':utc(),'python':sys.version,'runtime':sys.executable,'sympy':sympy.__version__,'mpmath':mpmath.__version__,'integrity_before':before,'archive_validation':archives,'jobs':[]}
    try:
        for job in selected:
            print('Running '+job+' ...',flush=True)
            row=replay(job,args.primary_dir);receipt['jobs'].append(row)
            print('PASS '+job+'; exact scientific JSON; raw bytes equal='+str(row['raw_byte_equal']),flush=True)
    finally:
        after=verify(args.manifest)
        if after!=before:raise ValueError('Frozen inventory changed during replay')
    receipt.update({'utc_end':utc(),'integrity_after':after,'all_selected_jobs_passed':True,'all_scientific_fields_compared_exactly':True,'no_interval_certification':True,'whole_manuscript_review':False})
    if args.receipt:args.receipt.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'jobs_passed':len(receipt['jobs']),'integrity_before_and_after_equal':True,'receipt':str(args.receipt) if args.receipt else None},indent=2))
if __name__=='__main__':main()
