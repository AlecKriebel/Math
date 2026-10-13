#!/usr/bin/env python3
"""Replay each audit mutation/counterexample separately with exact rejection reasons."""
import json,os,runpy,sys
from pathlib import Path
REASONS={'positive_only':'layer reconstruction','reverse_negative':'layer reconstruction','omit_base':'mutated ring','omit_chains':'mutated ring','reverse_implication_shift':'mutated ring','floor_instead_of_ceiling':'floor-rounded assignment infeasible','omit_bipartition_sign_change':'cover min fails','remove_subunit_layer':'subunit removal infeasible','replace_hull_with_relaxation':'LP point outside mixed hull','replace_hull_with_mixed_set':'hull point need not be mixed integral','explicit_exception_control':'explicit guard remains live'}
def need(ok,why):
 if not ok:raise ValueError(why)
def main():
 need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000')
 need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B required')
 need(len(sys.argv)==2 and sys.argv[1] in REASONS,'one exact rejection identity required')
 m=sys.argv[1];ns=runpy.run_path(str(Path(__file__).resolve().parent/'current/independent_checks.py'));Q=ns['Q'];check=ns['need'];ring=ns['ring_sets'];intended=ns['intended_ring']
 try:
  if m in ['positive_only','reverse_negative']:ns['verify_decomposition']((Q(-1),Q(2)),m)
  elif m in ['omit_base','omit_chains','reverse_implication_shift']:
   lo,hi,d={'omit_base':((0,0),(1,1),1),'omit_chains':((0,0),(2,2),-3),'reverse_implication_shift':((-1,-1),(2,2),1)}[m]
   check(set(ring(lo,hi,d,m)[1])==intended(lo,hi,d),'mutated ring')
  elif m=='floor_instead_of_ceiling':check(Q(0)>=Q(1,2),'floor-rounded assignment infeasible')
  elif m=='omit_bipartition_sign_change':check(min(1,0)+min(0,1)>=1,'cover min fails')
  elif m=='remove_subunit_layer':check(Q(1,2)-1>=0,'subunit removal infeasible')
  elif m=='replace_hull_with_relaxation':check(Q(1,4)+Q(1,4)>=1,'LP point outside mixed hull')
  elif m=='replace_hull_with_mixed_set':check(Q(1,2).denominator==1,'hull point need not be mixed integral')
  else:check(False,'explicit guard remains live')
 except ns['AuditFailure'] as error:
  need(str(error)==REASONS[m],'unintended rejection reason')
  print(json.dumps(dict(ok=False,python_optimize=sys.flags.optimize,mutation=m,failure=str(error)),sort_keys=True));return 1
 raise ValueError('rejection case survived')
if __name__=='__main__':
 try:sys.exit(main())
 except (ValueError,OSError,KeyError,TypeError) as error:
  print('REJECT: case adapter failed: '+str(error),file=sys.stderr);sys.exit(2)
