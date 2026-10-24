"""Capture full stdout/stderr for both exact checks in normal and optimized modes."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).parent
SCRIPTS={'check_algorithms.py':'check_results.json','check_robust_rounding.py':'robust_check_results.json'}
def main():
 rows=[]
 for flags in [[],['-O']]:
  for script,result in SCRIPTS.items():
   c=subprocess.run([sys.executable,*flags,'-B',str(ROOT/script)],capture_output=True,text=True)
   row={'mode':'optimized' if flags else 'normal','script':script,'exit':c.returncode,'stdout':c.stdout,'stderr':c.stderr}
   if c.returncode:raise RuntimeError(row)
   row['full_output_matches']=json.loads(c.stdout)==json.loads((ROOT/result).read_text())
   if not row['full_output_matches']:raise RuntimeError(row)
   rows.append(row)
 print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
