#!/usr/bin/env python3
"""Finite JSON float controls on externally pinned actual helper source bytes.
No entrypoint/operation/API/Git call is made. Both helper strict() functions are
compiled at the actual outer optimization level. Legacy overflow evidence is
explicitly marked a known defect, never a clean outcome.
"""
import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('Use -I -S -B')
import argparse,hashlib,json,math
from pathlib import Path
OWN=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--core',required=True);p.add_argument('--core-sha256',required=True);p.add_argument('--wrapper',required=True);p.add_argument('--wrapper-sha256',required=True);p.add_argument('--test-sha256',required=True);p.add_argument('--expect-legacy-overflow',action='store_true');a=p.parse_args()
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,m):
 if not ok:raise RuntimeError(m)
need(sha(Path(__file__).read_bytes())==a.test_sha256,'external test source pin')
rows=[]
finite=[('zero','0.0',0.0),('negative_zero','-0.0',-0.0),('ordinary','1.25',1.25),('negative','-123.5',-123.5),('small_exponent','1e-12',1e-12),('large_finite_exponent','1e308',1e308),('largest_binary64','1.7976931348623157e308',sys.float_info.max),('negative_largest_binary64','-1.7976931348623157e308',-sys.float_info.max),('smallest_normal','2.2250738585072014e-308',sys.float_info.min),('smallest_subnormal','4.9406564584124654e-324',float.fromhex('0x0.0000000000001p-1022')),('underflow_finite_zero','1e-9999',0.0),('underflow_negative_finite_zero','-1e-9999',-0.0)]
overflow=[('positive_overflow','1e9999'),('negative_overflow','-1e9999'),('positive_boundary_overflow','1.7976931348623159e308'),('negative_boundary_overflow','-1.7976931348623159e308'),('nested_object_overflow','{"outer":[1.0,{"bad":1e9999}]}'),('nested_array_negative_overflow','[0.0,[-1e9999]]')]
constant=[('literal_NaN','NaN'),('literal_Infinity','Infinity'),('literal_negative_Infinity','-Infinity')]
for label,path,digest in [('close',Path(a.core),a.core_sha256),('finalizer',Path(a.wrapper),a.wrapper_sha256)]:
 raw=path.read_bytes();need(sha(raw)==digest,'external '+label+' source pin')
 n={'__name__':'_finite_json_offline_'+label,'__file__':str(path)};exec(compile(raw,str(path),'exec',dont_inherit=True,optimize=sys.flags.optimize),n)
 for name,text,want in finite:
  value=n['strict'](text);need(type(value) is float and math.isfinite(value) and value==want,'finite float rejected/changed '+label+' '+name)
  if want==0.0:need(math.copysign(1,value)==math.copysign(1,want),'negative zero sign lost')
  rows.append({'helper':label,'test':name,'status':'PASS_FINITE','decoded_type':'float'})
 # Ordinary JSON values, finite nested floats, strings resembling constants,
 # exact type preservation and arbitrary finite integers remain unchanged.
 text='{"array":[1,1.5,-0.0,true,false,null,"NaN","Infinity"],"integer":1234567890123456789012345678901234567890}'
 value=n['strict'](text);need(type(value['array'][0]) is int and type(value['array'][1]) is float and type(value['array'][3]) is bool and value['integer']==1234567890123456789012345678901234567890,'ordinary JSON type preservation')
 rows.append({'helper':label,'test':'nested_finite_mixed_values_and_large_finite_integer','status':'PASS_FINITE'})
 for name,text in overflow+constant+[('duplicate_keys','{"x":1.0,"x":2.0}')]:
  rejected=False
  try:value=n['strict'](text)
  except (RuntimeError,ValueError,OverflowError):rejected=True
  if a.expect_legacy_overflow and (name,text) in overflow:
   need(not rejected,'baseline no longer demonstrates overflow defect '+label+' '+name)
   def nonfinite(x):
    if type(x) is float:return not math.isfinite(x)
    if type(x) is list:return any(nonfinite(y) for y in x)
    if type(x) is dict:return any(nonfinite(y) for y in x.values())
    return False
   need(nonfinite(value),'baseline did not decode overflow into nonfinite float')
   rows.append({'helper':label,'test':name,'status':'KNOWN_LEGACY_DEFECT_ACCEPTED_NONFINITE'})
  else:
   need(rejected,'nonfinite/duplicate JSON accepted '+label+' '+name);rows.append({'helper':label,'test':name,'status':'REJECTED_EXPECTED'})
print(json.dumps({'schema':'pr967-finite-json-float-offline-controls-v1','status':'LEGACY_DEFECT_REPRODUCED_NO_CLEAN_CREDIT' if a.expect_legacy_overflow else 'PASS_FINITE_FLOAT_AND_OVERFLOW_CONTROLS','outer_optimization':sys.flags.optimize,'source_pins':{'test':a.test_sha256,'close':a.core_sha256,'finalizer':a.wrapper_sha256},'events':rows,'event_count':len(rows),'actual_service_or_Git_mutations':0,'entrypoints_or_operations_called':False,'legacy_underflow_policy':'finite signed-zero underflow remains accepted; no exact-real-arithmetic claim','clean_entire_package_review_or_execution_authority':False},sort_keys=True,allow_nan=False))
