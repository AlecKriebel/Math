"""Bounded semantic comparator proposal; never authenticates a new packet or proves mathematics.
Only 12 explicitly identified floating fields in the author's four fixed samples use tolerances.
Every other field is recursively type-strict and exact except three declared version strings.
"""
import copy,json,math
from pathlib import Path
from datetime import datetime,timezone
BASE=Path(__file__).resolve().parent
ORIG=BASE.parents[1]/'original/unsolved_math_prioritization/attempts/6000001'
VERSION_FIELDS={'python','sympy','numpy'}
NUMERIC_FIELDS={'lambda','minimum_eigenvalue','H_df_minus_dphi_max_abs'}
def require(ok,msg):
 if not ok:raise ValueError(msg)
def compare(actual,expected,path=()):
 require(type(actual) is type(expected),'Type mismatch '+str(path))
 if isinstance(expected,dict):
  require(set(actual)==set(expected),'Key mismatch '+str(path))
  for k in expected:
   if not path and k in VERSION_FIELDS:
    require(type(actual[k]) is str and bool(actual[k]),'Malformed version')
   else:compare(actual[k],expected[k],path+(k,))
 elif isinstance(expected,list):
  require(len(actual)==len(expected),'Length mismatch '+str(path))
  for i,(a,e) in enumerate(zip(actual,expected)):compare(a,e,path+(i,))
 elif len(path)==3 and path[0]=='positive_hessian_completion_samples' and type(path[1]) is int and 0<=path[1]<4 and path[2] in NUMERIC_FIELDS:
  require(type(actual) is float and type(expected) is float and math.isfinite(actual) and math.isfinite(expected),'Nonfinite or nonfloat sample')
  field=path[2]
  if field=='lambda':
   require(actual>=1.0 and expected>=1.0 and math.isclose(actual,expected,rel_tol=1e-13,abs_tol=1e-13),'Lambda discrepancy')
  elif field=='minimum_eigenvalue':
   require(actual>0.0 and expected>0.0 and math.isclose(actual,expected,rel_tol=1e-10,abs_tol=1e-12),'Eigenvalue discrepancy')
  else:
   require(0.0<=actual<1e-6 and 0.0<=expected<1e-6 and math.isclose(actual,expected,rel_tol=0,abs_tol=1e-10),'Residual discrepancy')
 else:require(actual==expected,'Exact mismatch '+str(path))
def differences(actual,expected,path=()):
 if type(actual) is not type(expected):return [dict(path=list(path),actual=actual,expected=expected,kind='type')]
 if isinstance(expected,dict):
  return sum((differences(actual[k],expected[k],path+(k,)) for k in expected),[])
 if isinstance(expected,list):return sum((differences(a,e,path+(i,)) for i,(a,e) in enumerate(zip(actual,expected))),[])
 if actual!=expected:return [dict(path=list(path),actual=actual,expected=expected,kind=type(expected).__name__,absolute_difference=abs(actual-expected) if type(expected) is float else None)]
 return []
def main():
 actual=json.loads((BASE/'evidence/author_math.stdout').read_text());expected=json.loads((ORIG/'public/VERIFICATION.json').read_text())
 diff=differences(actual,expected);compare(actual,expected)
 tests=[]
 def negative(name,mutator):
  a=copy.deepcopy(actual);mutator(a)
  try:compare(a,expected)
  except ValueError:tests.append({'case':name,'rejected':True});return
  raise RuntimeError('Negative control accepted: '+name)
 negative('exact_integer_changed',lambda a:a.__setitem__('exact_residuals_checked',27))
 negative('bool_instead_of_integer',lambda a:a.__setitem__('exact_residuals_checked',True))
 negative('exact_symbolic_determinant',lambda a:a.__setitem__('two_dimensional_derivative_jet_determinant','575'))
 negative('missing_exact_key',lambda a:a.pop('symbolic_checks'))
 negative('extra_key_units_claim',lambda a:a.__setitem__('units','arbitrary_rescaled'))
 negative('sample_point_units_rescaled',lambda a:a['positive_hessian_completion_samples'][1]['point'].__setitem__(0,1000.0))
 for field in sorted(NUMERIC_FIELDS):
  for label,value in [('nan',float('nan')),('infinity',float('inf')),('boolean',True),('string','1.0'),('integer',1)]:
   negative(field+'_'+label,lambda a,field=field,value=value:a['positive_hessian_completion_samples'][1].__setitem__(field,value))
 negative('negative_eigenvalue',lambda a:a['positive_hessian_completion_samples'][1].__setitem__('minimum_eigenvalue',-1e-13))
 negative('zero_eigenvalue',lambda a:a['positive_hessian_completion_samples'][1].__setitem__('minimum_eigenvalue',0.0))
 negative('negative_residual',lambda a:a['positive_hessian_completion_samples'][1].__setitem__('H_df_minus_dphi_max_abs',-1e-13))
 negative('loosened_author_residual',lambda a:a['positive_hessian_completion_samples'][1].__setitem__('H_df_minus_dphi_max_abs',2e-6))
 negative('material_lambda_change',lambda a:a['positive_hessian_completion_samples'][1].__setitem__('lambda',actual['positive_hessian_completion_samples'][1]['lambda']+1e-6))
 negative('material_eigenvalue_change',lambda a:a['positive_hessian_completion_samples'][1].__setitem__('minimum_eigenvalue',actual['positive_hessian_completion_samples'][1]['minimum_eigenvalue']+1e-6))
 negative('material_residual_change',lambda a:a['positive_hessian_completion_samples'][1].__setitem__('H_df_minus_dphi_max_abs',2e-10))
 for i in range(4):
  negative('sample_'+str(i)+'_wrong_residual_type',lambda a,i=i:a['positive_hessian_completion_samples'][i].__setitem__('H_df_minus_dphi_max_abs',0))
 result=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',original_strict_comparison='FAIL',bounded_proposal='PASS',differences=diff,negative_controls=tests,tolerance_justification='The 12 explicit floats describe QR/eigensolver samples in the unchanged dimensionless source model. Lambda abs/rel1e-13, eigenvalue abs1e-12/rel1e-10, residual abs1e-10; all12 finite, positive/minimum and residual<1e-6 checks retained. Tolerances exceed the observed drift while retaining the original numerical semantics. This is a bounded consistency criterion, not a validated floating-point error proof. Points, ordering, units, exact counts, symbolic data, all other keys/types stay exact. No blanket numeric normalization.',limitation='Proposal alone; the original strict wrapper still rejects this runtime. No claim of byte-identical reproducibility, formal global theorem verification, or runtime-independent error certification.')
 (BASE/'evidence/COMPARISON.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
