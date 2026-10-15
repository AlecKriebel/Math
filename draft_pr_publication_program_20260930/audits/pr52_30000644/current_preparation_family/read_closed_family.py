#!/usr/bin/env python3
"""Unexecuted ROOT-only separate read-only SOURCE. No writes."""
import argparse,json
from closure_common import HERE,SELF,bind,inspect,load,require
from close_family import completed_private_readback

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--expected-index-sha256',required=True)
    parser.add_argument('--expected-ready-sha256',required=True)
    parser.add_argument('--expected-manifest-sha256',required=True)
    args=parser.parse_args()
    require(bind(HERE/'INDEX.json')['sha256']==args.expected_index_sha256,'actual full index pin')
    require(bind(HERE/'READY.json')['sha256']==args.expected_ready_sha256,'actual full READY pin')
    require(bind(HERE/SELF)['sha256']==args.expected_manifest_sha256,'actual full self-manifest pin')
    value=load(HERE/SELF)
    require(value['schema']=='pr52-current-lean-self-closure/v1','literal actual self schema')
    require(value['family']==str(HERE),'actual family identity')
    require(value['index_sha256']==args.expected_index_sha256 and value['ready_sha256']==args.expected_ready_sha256,'exact self index/READY pins')
    require(value['manifest_excludes_only_itself']==SELF and value['closure_operator_pid']>0,'self exclusion and actual closer PID')
    actual=[bind(p,True) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!=SELF]
    require(actual==value['files'],'all actual full frozen payload bodies and modes')
    for key in ('ROOT_personal_read_attestation','native_acceptance','new_independent_mathematical_verdict','production_or_publication_authority'):
        require(value[key] is False,'no forbidden current authority')
    completed_private_readback()
    result=inspect(True);result['manifest']=bind(HERE/SELF,True)
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
