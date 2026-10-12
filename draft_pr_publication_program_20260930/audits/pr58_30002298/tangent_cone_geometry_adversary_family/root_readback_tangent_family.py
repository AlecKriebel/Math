"""UNEXECUTED ROOT readback: python helper.py /absolute/close.json /absolute/readback.json"""
import json,os,sys
from datetime import datetime,timezone
from pathlib import Path
sys.dont_write_bytecode=True
from root_close_tangent_family import FAMILY,sha,validate
def main():
    assert len(sys.argv)==3
    prior=Path(sys.argv[1]).resolve();output=Path(sys.argv[2]).resolve()
    assert FAMILY not in prior.parents and FAMILY not in output.parents and not output.exists()
    b=prior.read_bytes();old=json.loads(b);fresh=validate()
    assert all(old[k]==v for k,v in fresh.items()) and old['validation_complete']
    result={'schema':'pr58-tangent-ROOT-readback/v1','executing_pid':os.getpid(),
        'utc':datetime.now(timezone.utc).isoformat(),'prior_receipt_sha256':sha(b),
        'current_bytes_modes_match_close':True,'validation':fresh,
        'scientific_operators_executed':False,'private_cache_read':False,
        'receipt_actual_only_if_ROOT_owns_and_captures_this_run':True}
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x') as f:f.write(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
