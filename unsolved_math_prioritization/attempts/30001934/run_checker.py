#!/usr/bin/env python3
"""Explicit absolute-file loader for authenticated, read-only fixed checks.

No cwd/sys.path additions, PYTHONPATH imports, discovery generators or writes.
The independent reject wrapper only records the exception already raised by each
existing false-claim fixture; it leaves that fixture and rejection unchanged.
"""
import json,os,sys,types
from pathlib import Path
HERE=Path(__file__).resolve().parent
REASONS={'omit_subset_bounds':'alleged endpoint differs from independent rank endpoint','floor_fractional_endpoint':'alleged endpoint differs from independent rank endpoint','treat_any_fractional_tree_as_target_counterexample':'integer tree exists','require_globally_largest_endpoint_integral':'largest endpoint fractional','require_maximum_weight_tree_integral':'weighted star fractional','exclude_zero_maximum':'zero is a valid exact endpoint','omit_rank_zero_mass_bound':'alleged endpoint differs from independent rank endpoint','collapse_parallel_coordinate_bounds':'alleged endpoint differs from independent rank endpoint','accept_negative_remaining_mass':'negative mass'}
def need(ok,message):
 if not ok:raise ValueError(message)
def load(name,relative):
 path=HERE/relative;module=types.ModuleType(name);module.__file__=str(path);sys.modules[name]=module
 exec(compile(path.read_bytes(),str(path),'exec'),module.__dict__)
 return module
def main():
 need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000');need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B required')
 need(len(sys.argv)==2 and sys.argv[1] in ('author_core','author_saved_adversarial','independent','source_mutants'),'one exact suite identity required')
 case=sys.argv[1];load('exact_model','author/tests/exact_model.py')
 if case=='author_core':
  mod=load('accepted_author_core','author/tests/test_exact_model.py');print(json.dumps(mod.run(),sort_keys=True));return
 if case=='author_saved_adversarial':
  load('accepted_saved_point_checker','current/check_adversarial_records.py');return
 audit=load('independent_exact_audit','current/independent_exact_audit.py')
 if case=='source_mutants':
  mod=load('accepted_source_mutants','audit/tests/test_source_mutants.py');print(json.dumps(mod.run(),indent=2,sort_keys=True));return
 original=audit.reject;details=[]
 def trace(label,fn):
  before=len(details)
  def observed():
   try:fn()
   except RuntimeError as error:
    need(label in REASONS and str(error)==REASONS[label],'intended false-claim reason')
    details.append(dict(control=label,rejected=True,exception=type(error).__name__,reason=str(error)));raise
  result=original(label,observed)
  need(result==label and len(details)==before+1,'exactly one observed rejection')
  return result
 audit.reject=trace;result=audit.run();need([r['control'] for r in details]==list(REASONS),'complete fixed false-claim identities');result['rejection_details']=details
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
