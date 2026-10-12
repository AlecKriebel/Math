#!/usr/bin/env python3
"""Read-only parent verification of all three exact closed review namespaces."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,stat,subprocess,sys
A=Path(__file__).resolve().parent
RUN=A/'root_replay_private/family_closures_001'
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return datetime.now(timezone.utc).isoformat()
def inventory(p):
    out={}
    for q in sorted(p.rglob('*')):
        assert not q.is_symlink(),q
        mode=q.lstat().st_mode
        assert stat.S_ISREG(mode) or stat.S_ISDIR(mode)
        value={'type':'file' if q.is_file() else 'directory','mode':oct(stat.S_IMODE(mode))}
        if q.is_file():
            b=q.read_bytes();value.update(bytes=len(b),sha256=sha(b))
        out[str(q.relative_to(p))]=value
    return out
def main():
    tasks=[('algebra_certificate_review','public/verify_audit_package.py',
            ['--private-dir',str(A/'algebra_certificate_review/private')],'public/FINAL_SEAL.json'),
           ('topology_density_review','public/verify_review.py',
            ['--with-private','--snapshot',str(A/'snapshot')],'FINAL_CLOSURE.json'),
           ('backward_feedback_review','public/verify_audit.py',[],'SEAL.json')]
    assert all((A/family/seal).is_file() for family,code,args,seal in tasks),'Wait for all final seals.'
    assert not RUN.exists();RUN.mkdir(parents=True)
    results=[]
    for family,code,args,seal in tasks:
        p=A/family;before=inventory(p)
        start=utc();argv=[sys.executable,'-B',str(p/code)]+args
        result=subprocess.run(argv,cwd=A,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        end=utc()
        for name,b in [('stdout',result.stdout),('stderr',result.stderr)]:
            (RUN/(family+'.'+name)).write_bytes(b)
        rec={'argv':argv,'cwd':str(A),'started_utc':start,'completed_utc':end,'exit_code':result.returncode,
             'stdout_bytes':len(result.stdout),'stdout_sha256':sha(result.stdout),
             'stderr_bytes':len(result.stderr),'stderr_sha256':sha(result.stderr)}
        (RUN/(family+'.execution.json')).write_text(json.dumps(rec,indent=2)+'\n')
        assert result.returncode==0 and not result.stderr,rec
        parsed=json.loads(result.stdout)
        assert parsed['status'] in {'PASS','CLOSED_SCOPE_PASS'}
        after=inventory(p);assert before==after,'Closed family changed during parent verification.'
        (RUN/(family+'.whole_inventory.json')).write_text(json.dumps(before,indent=2)+'\n')
        results.append({'family':family,'whole_files':sum(e['type']=='file' for e in before.values()),
                        'whole_directories':sum(e['type']=='directory' for e in before.values()),
                        'whole_namespace_unchanged':True,'seal_path':seal,
                        'seal_sha256':sha((p/seal).read_bytes()),'native_run':rec,
                        'complete_verifier_result':parsed})
    out={'utc':utc(),'status':'PASS_ALL_THREE_CLOSED_FAMILIES_PARENT_VERIFIED',
         'families':results,'mandatory_mathematical_findings':0,
         'scope':'Parent independently read reports/control/verifier code and reproduced new controls. Full public/private native closure verified without modifying sealed namespaces. Priority and submission reviews remain pending.'}
    (A/'ROOT_FAMILY_CLOSURE_VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
