#!/usr/bin/env python3
"""Pinned audit bytes plus independent finite replay, not theorem certification."""
import argparse,hashlib,json,os,re,stat,subprocess,sys
from pathlib import Path
EXPECTED={'AUDIT.md','ACCEPTANCE.json','SOURCE_REVIEW.json','README.md','INDEPENDENT_RESULTS.json','INTEGRITY_RESULTS.json','LEDGER_VALIDATION.patch','check_ledger_correction.py','extra_integrity_checks.py','independent_checks.py','verify_audit.py'}
def need(x,message):
    if not x:raise ValueError(message)
def pairs(items):
    result={}
    for key,value in items:
        need(key not in result,'duplicate JSON key');result[key]=value
    return result
def bad(value):raise ValueError('nonfinite JSON constant')
def parse(raw):return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)
def read(path,limit=2_000_000):
    info=path.lstat();need(stat.S_ISREG(info.st_mode) and not path.is_symlink() and 0<=info.st_size<=limit,'unsafe input');return path.read_bytes()
def digest(raw):return hashlib.sha256(raw).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--packet',required=True);ap.add_argument('--manifest',required=True);ap.add_argument('--manifest-sha256',required=True);args=ap.parse_args()
    need(sys.flags.isolated==1 and os.geteuid()!=0,'isolated nonroot process required')
    root=Path(args.packet);need(not root.is_symlink() and root.is_dir(),'unsafe packet root')
    need(re.fullmatch('[0-9a-f]{64}',args.manifest_sha256) is not None,'invalid manifest pin')
    raw=read(Path(args.manifest),100000);need(digest(raw)==args.manifest_sha256,'manifest pin mismatch');m=parse(raw)
    need(type(m) is dict and set(m)=={'schema','files'} and m['schema']=='erdos-cycle-sets-independent-audit-v1','manifest schema')
    need(type(m['files']) is dict and set(m['files'])==EXPECTED,'manifest file set');need({p.name for p in root.iterdir()}==EXPECTED,'packet file set')
    for name,rec in m['files'].items():
        need(type(rec) is dict and set(rec)=={'bytes','sha256'},'file record')
        need(type(rec['bytes']) is int and 0<=rec['bytes']<=2_000_000,'invalid byte count')
        need(type(rec['sha256']) is str and re.fullmatch('[0-9a-f]{64}',rec['sha256']) is not None,'invalid file hash')
        content=read(root/name);need(len(content)==rec['bytes'] and digest(content)==rec['sha256'],'file hash mismatch')
    acceptance=parse(read(root/'ACCEPTANCE.json'));need(acceptance['full_problem_resolved'] is False and acceptance['formal_certification'] is False and acceptance['status']=='unsolved','acceptance scope')
    need(type(acceptance['proof_turns']) is int and acceptance['proof_turns']==5,'approach count')
    flags=['-I','-B']+(['-OO'] if sys.flags.optimize==2 else ['-O'] if sys.flags.optimize else [])
    run=subprocess.run([sys.executable,*flags,str(root/'independent_checks.py')],capture_output=True,text=True,timeout=180)
    need(run.returncode==0,'independent finite checks failed');observed=parse(run.stdout);expected=parse(read(root/'INDEPENDENT_RESULTS.json'))['runs'][sys.flags.optimize]
    need({k:v for k,v in observed.items() if k!='uid'}=={k:v for k,v in expected.items() if k!='uid'},'independent result differs')
    print(json.dumps({'audit_integrity':'pass','independent_mathematics':'finite_controls_pass','optimize':sys.flags.optimize,'uid':os.geteuid(),'finite_check_count':observed['checks'],'formal_certification':False,'full_problem_resolved':False},sort_keys=True))
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,UnicodeError,KeyError,TypeError,subprocess.SubprocessError) as exc:
        print('REJECT: '+str(exc),file=sys.stderr);sys.exit(1)
