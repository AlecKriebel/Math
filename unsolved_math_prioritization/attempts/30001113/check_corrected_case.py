#!/usr/bin/env python3
"""Run the accepted explicit-check checker, optionally applying one fixed mutant.

Caught intended RuntimeError messages are reported as deterministic JSON, rather
than environment-dependent tracebacks. This reporting adapter does not normalize
any subprocess stdout/stderr; the outer runner compares all bytes.
"""
import json,sys
from pathlib import Path
MUTATIONS={
 'missing_parameter_shift':('Mprime=[[one,e^e2],[one,one]]','Mprime=[[one,e],[one,one]]'),
 'wrong_involution_scalar':('if mm(M,M)!=[[one^e,0],[0,one^e]]:','if mm(M,M)!=[[one,0],[0,one]]:')}
def main():
 if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise ValueError('-I -S -B required')
 if len(sys.argv)!=2 or sys.argv[1] not in ['none',*MUTATIONS]:raise ValueError('exact intended case required')
 mutant=sys.argv[1];src=(Path(__file__).resolve().parent/'current/check_conjugacy.py').read_text()
 if mutant!='none':
  old,new=MUTATIONS[mutant]
  if src.count(old)!=1:raise ValueError('mutation target not unique')
  src=src.replace(old,new)
 try:exec(compile(src,'<accepted-corrected-checker>','exec'),{'__name__':'__main__'})
 except RuntimeError as e:
  print(json.dumps(dict(ok=False,mutant=mutant,failure=str(e)),sort_keys=True));return 1
 return 0
if __name__=='__main__':sys.exit(main())
