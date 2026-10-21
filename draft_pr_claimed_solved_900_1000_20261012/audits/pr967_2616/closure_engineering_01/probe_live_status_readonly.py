#!/usr/bin/env python3
"""Actual filename/status-only API shape validation. No service/Git mutations.
No source-catalog, private source body, mathematical or family report intake.
"""
import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('Use -I -S -B')
import argparse,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
OWN=Path(__file__).resolve().parent;P=OWN.parents[2]
p=argparse.ArgumentParser();p.add_argument('--core-sha256',required=True);args=p.parse_args()
raw=(P/'close_pr967.py').read_bytes()
if hashlib.sha256(raw).hexdigest()!=args.core_sha256:raise SystemExit('external actual source pin mismatch')
n={'__name__':'_actual_readonly_status_shape_','__file__':str(P/'close_pr967.py')};exec(compile(raw,str(P/'close_pr967.py'),'exec',dont_inherit=True,optimize=0),n)
methods=[];original_api=n['api']
def readonly(method,endpoint,payload=None):
 if method!='GET' and not(method=='POST' and endpoint=='graphql' and type(payload) is dict and not payload['query'].lstrip().startswith('mutation')):raise RuntimeError('Read-only probe rejected non-query service method')
 methods.append({'method':method,'endpoint':endpoint});return original_api(method,endpoint,payload)
n['api']=readonly
result=n['status_gate']()
print(json.dumps({'schema':'pr967-actual-readonly-status-shape-probe-v1','utc':datetime.now(timezone.utc).isoformat(),'core_sha256':args.core_sha256,'status':'PASS_ACTUAL_READONLY_GATE_SHAPE','gate':result,'actual_readonly_requests':methods,'service_mutations':0,'Git_fetch_or_mutation':False,'acceptance_or_priority_or_full_review_authority':False},sort_keys=True))
