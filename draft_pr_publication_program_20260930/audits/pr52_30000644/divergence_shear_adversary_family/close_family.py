#!/usr/bin/env python3
"""Unexecuted ROOT-only SOURCE. Closes only this private audit family."""
from datetime import datetime,timezone
import json,os
from closure_common import HERE,SELF,bind,inspect,require

def main():
    require(not (HERE/SELF).exists(),'self manifest must be absent before actual ROOT closure')
    result=inspect(False)
    rows=[bind(p,True) for p in sorted(HERE.rglob('*')) if p.is_file()]
    value={'schema':'pr52-divergence-shear-self-closure-v1','status':'PASS',
           'family':str(HERE),'utc':datetime.now(timezone.utc).isoformat(),
           'operator_pid':os.getpid(),'files':rows,'inspection':result,
           'self_hash_excluded':True,'native_or_production_changes':False,
           'authority_limit':'Actual ROOT caller identity and invocation must be attested by ROOT outside this file; preparation alone is not execution.'}
    body=(json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
    os.chmod(HERE,0o755)
    try:
        fd=os.open(str(HERE/SELF),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
        with os.fdopen(fd,'wb') as stream:
            stream.write(body)
            stream.flush()
            os.fchmod(stream.fileno(),0o444)
            os.fsync(stream.fileno())
    finally:
        os.chmod(HERE,0o555)
    inspect(True)
    print(json.dumps({'status':'PASS','manifest':bind(HERE/SELF,True),
                      'payload_files':len(rows),'private_assertions':6681},sort_keys=True))
if __name__=='__main__':main()
