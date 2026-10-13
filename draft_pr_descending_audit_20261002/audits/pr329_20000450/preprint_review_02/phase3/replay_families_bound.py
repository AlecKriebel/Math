#!/usr/bin/env python3
"""Read-only contemporary parent replay of independently written certificates."""
from pathlib import Path
import concurrent.futures,hashlib,json,os,stat,subprocess,time
N=Path(__file__).resolve().parent;F=N.parent/'families';R=N/'family_replay_receipts';R.mkdir(exist_ok=True)
SP='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr329_20000450/geometry/.runtime/bin/python'
sha=lambda b:hashlib.sha256(b).hexdigest()
def utc():return subprocess.run(['/bin/date','-u','+%Y-%m-%dT%H:%M:%SZ'],capture_output=True,check=True).stdout.decode().strip()
def inventory():
    records={}
    for p in sorted(F.rglob('*')):
        assert not p.is_symlink();rel=str(p.relative_to(F));mode=format(stat.S_IMODE(p.stat().st_mode),'04o')
        records[rel]={'mode':mode,'sha256':sha(p.read_bytes()) if p.is_file() else None}
    return records
before=inventory();env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0');env.pop('PYTHONOPTIMIZE',None)
names=['geometry/independent_geometry_v01.py','geometry/independent_boundary_v01.py','geometry/independent_tate_discriminant_v01.py',
       'kernel/direct_kernel_exact.py','kernel/map_boundary_exact.py','kernel/extra_exact_checks.py','kernel/finite_direct_control.py']
def run(name):
    script=F/name;label=name.replace('/','_').removesuffix('.py');argv=[SP,'-B',str(script)]
    assert not (R/(label+'.json')).exists()
    body=script.read_bytes();rec={'argv':argv,'cwd':str(N),'utc_start':utc(),'clock_argv':['/bin/date','-u','+%Y-%m-%dT%H:%M:%SZ'],
                               'executed_body_sha256_before':sha(body),'state':'started'}
    meta=R/(label+'.json');meta.write_text(json.dumps(rec,indent=2)+'\n');tm=time.monotonic_ns()
    with (R/(label+'.stdout')).open('wb') as out,(R/(label+'.stderr')).open('wb') as err:
        p=subprocess.run(argv,cwd=N,env=env,stdout=out,stderr=err,timeout=180,check=False)
    out=(R/(label+'.stdout')).read_bytes();err=(R/(label+'.stderr')).read_bytes()
    rec.update(utc_end=utc(),exit_status=p.returncode,state='completed',elapsed_monotonic_ns=time.monotonic_ns()-tm,
               stdout_bytes=len(out),stdout_sha256=sha(out),stderr_bytes=len(err),stderr_sha256=sha(err),
               executed_body_sha256_after=sha(script.read_bytes()))
    meta.write_text(json.dumps(rec,indent=2)+'\n')
    assert p.returncode==0 and not err,(name,p.returncode,err)
    assert rec['executed_body_sha256_before']==rec['executed_body_sha256_after']
    return {'program':name,**rec}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(run,names))
assert inventory()==before,'Held family mutation'
summary={'status':'PASS','utc_end':utc(),'fresh_family_scientific_programs':7,'all_full_streams_preserved':True,
         'all_held_family_bodies_modes_directories_unchanged':True,'results':results}
(N/'FAMILY_REPLAY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
