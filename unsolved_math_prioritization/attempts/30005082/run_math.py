#!/usr/bin/env python3
"""Fresh mode-specific envelope around the unchanged authored exact checker."""
import hashlib,json,os,runpy,sys
from pathlib import Path
def main():
 if len(sys.argv)!=1 or os.getuid()!=1000 or os.geteuid()!=1000:raise ValueError('no arguments; UID=EUID=1000 required')
 if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise ValueError('require -I -S -B')
 p=Path(__file__).absolute().parent/'check_math.py';raw=p.read_bytes();ns=runpy.run_path(str(p),run_name='authored_mathematics')
 result=ns['main']()
 if p.read_bytes()!=raw:raise ValueError('checker changed')
 return dict(schema=1,problem_id=30005082,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,script_sha256=hashlib.sha256(raw).hexdigest(),mathematical_results=result,scope='Fresh finite exact controls supporting five partial results; global target unfinished')
if __name__=='__main__':
 try:print(json.dumps(main(),indent=2,sort_keys=True))
 except Exception as e:print(json.dumps(dict(status='FAIL',error_type=type(e).__name__,reason=str(e)),sort_keys=True));sys.exit(1)
