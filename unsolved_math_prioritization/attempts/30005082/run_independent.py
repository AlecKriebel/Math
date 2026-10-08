#!/usr/bin/env python3
"""Fresh independent algorithms, optionally comparing a disposable candidate mutant."""
import hashlib,json,os,runpy,sys
from pathlib import Path
def main():
 if os.getuid()!=1000 or os.geteuid()!=1000:raise ValueError('UID=EUID=1000 required')
 if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise ValueError('require -I -S -B')
 root=Path(__file__).absolute().parent;candidate=root/'check_math.py'
 if len(sys.argv)==3 and sys.argv[1]=='--candidate':candidate=Path(sys.argv[2])
 elif len(sys.argv)!=1:raise ValueError('invalid arguments')
 p=root/'independent_checks.py';raw=p.read_bytes();candidate_raw=candidate.read_bytes();ns=runpy.run_path(str(p),run_name='independent_mathematics')
 result=ns['check'](candidate)
 if p.read_bytes()!=raw or candidate.read_bytes()!=candidate_raw:raise ValueError('checker changed')
 return dict(schema=1,problem_id=30005082,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,script_sha256=hashlib.sha256(raw).hexdigest(),candidate_sha256=hashlib.sha256(candidate_raw).hexdigest(),mathematical_results=result,scope='Fresh independent finite exact controls; no global solution')
if __name__=='__main__':
 try:print(json.dumps(main(),indent=2,sort_keys=True))
 except Exception as e:print(json.dumps(dict(status='FAIL',error_type=type(e).__name__,reason=str(e)),sort_keys=True));sys.exit(1)
