#!/usr/bin/env python3
"""Unexecuted ROOT-only read-only SOURCE; creates no receipts or writes."""
from datetime import datetime
import json,stat
from closure_common import HERE,SELF,bind,inspect,load,require

def main():
    value=load(SELF)
    require(value['schema']=='pr52-divergence-shear-self-closure-v1','literal self schema')
    require(value['family']==str(HERE),'literal family identity')
    require(value['operator_pid']>0,'actual closer process ID')
    datetime.fromisoformat(value['utc'])
    require(value['self_hash_excluded'] is True,'noncircular self exclusion')
    require(stat.S_IMODE((HERE/SELF).stat().st_mode)==0o444,'full self mode')
    actual=[bind(p,True) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!=SELF]
    require(actual==value['files'],'entire closed family complete bytes and full modes')
    result=inspect(True)
    result['self_manifest']=bind(HERE/SELF,True)
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
