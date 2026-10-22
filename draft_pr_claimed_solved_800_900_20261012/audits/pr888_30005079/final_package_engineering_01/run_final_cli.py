"""Actual final CLI execution with raw private evidence and transparent path redaction."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys

HERE=Path(__file__).absolute().parent;A=HERE.parent;C=A/'candidate'
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def main():
    label=sys.argv[1];require=lambda ok,msg:None if ok else (_ for _ in ()).throw(ValueError(msg))
    require(label in ('default_build','current_normal','current_optimized','source_only'),'known final execution label')
    tmp=HERE/'private_tmp';(tmp/'replay_tmp').mkdir(exist_ok=True);(tmp/'build').mkdir(exist_ok=True)
    env=dict(os.environ);env['TMPDIR']=str(tmp/'replay_tmp')
    flags=['-I','-S','-B']+(['-O'] if label=='current_optimized' else [])
    wheels=A/'publication_tools_01/private_tmp/wheels'
    if label=='default_build':
        tool=C/'verification/portable.py';index=pin((C/'verification/package_index.json').read_bytes())['sha256']
        args=['build',index,str(tmp/'build/rank-two-fano-verification.zip'),'--dependency-dir',str(wheels)]
    elif label=='source_only':
        tool=C/'portable.py';repo=A.parents[2]
        args=['source-only','--catalog',str(repo/'unsolved_math_prioritization/catalog.json'),'--problems',str(repo/'unsolved_math_prioritization/cache/problems.json'),'--reports',str(repo/'unsolved_math_prioritization/cache/research_results.json'),'--primary-dir',str(A/'private_sources')]
    else:
        tool=C/'portable.py';index=pin((C/'CURRENT_PUBLICATION_MANIFEST.json').read_bytes())['sha256']
        args=['current',index,'--dependency-dir',str(wheels)]
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    proc=subprocess.run([sys.executable,*flags,str(tool),*args],cwd=tmp,env=env,capture_output=True,timeout=1200)
    end=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (tmp/(label+'_raw.stdout')).write_bytes(proc.stdout);(tmp/(label+'_raw.stderr')).write_bytes(proc.stderr)
    replacements=[(str(A).encode(),b'<AUDIT_ROOT>'),(str(A.resolve()).encode(),b'<AUDIT_ROOT>')]
    def sanitize(raw):
        for before,after in replacements:raw=raw.replace(before,after)
        return raw
    stdout=sanitize(proc.stdout);stderr=sanitize(proc.stderr)
    (HERE/(label.upper()+'_PUBLIC_STDOUT.json')).write_bytes(stdout)
    (HERE/(label.upper()+'_PUBLIC_STDERR.txt')).write_bytes(stderr)
    try:result=json.loads(stdout)
    except (ValueError,UnicodeError):result={'status':'NON_JSON_STDOUT'}
    receipt={'label':label,'started_utc':start,'ended_utc':end,'completion_estimate_percent':65 if label=='default_build' else 85,'scope':'Actual final candidate CLI run; auxiliary engineering only, no mathematical/priority/whole-package/publication verdict.','actual_outer_CLI_subprocesses':1,'requested_outer_flags':flags,'exit_code':proc.returncode,'raw_stdout':pin(proc.stdout),'raw_stderr':pin(proc.stderr),'public_stdout':pin(stdout),'public_stderr':pin(stderr),'sanitization':{'operation':'Byte replacement of private audit-root prefixes only; no fields or failure status changed.','stdout_changed':stdout!=proc.stdout,'stderr_changed':stderr!=proc.stderr,'replacement':'<AUDIT_ROOT>'},'raw_evidence_retained_privately':True,'result_status':result.get('status')}
    (HERE/(label.upper()+'_EXECUTION_RECEIPT.json')).write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'label':label,'exit':proc.returncode,'status':result.get('status'),'raw_stdout':pin(proc.stdout),'public_stdout':pin(stdout)},indent=2))
    sys.exit(0 if proc.returncode==0 and result.get('status')=='PASS' else 1)

if __name__=='__main__':main()
