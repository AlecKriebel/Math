#!/usr/bin/env python3
"""Portable read-only authored-member integrity and exact mathematical diagnostics."""
from pathlib import Path
import hashlib,json,subprocess,sys
HERE=Path(__file__).absolute().parent.parent
PREFIX='draft_pr_actual_claims_1100_1200_20261017/audits/pr1150_30003045'
AUDIT=HERE/PREFIX if (HERE/PREFIX).is_dir() else HERE.parent
def need(ok,msg):
 if not ok:raise ValueError(msg)
def safe(p):
 p=p.absolute()
 for root in (HERE,AUDIT):
  try:rel=p.relative_to(root)
  except ValueError:continue
  need('..' not in rel.parts,'unsafe path '+str(p))
  cursor=root;need(not cursor.is_symlink(),'symlink root '+str(cursor))
  for part in rel.parts:
   cursor=cursor/part;need(not cursor.is_symlink(),'symlink ancestor/member '+str(cursor))
  return p
 raise ValueError('path outside distribution roots '+str(p))
def pin(p):
 p=safe(p);need(p.is_file(),'missing file '+str(p));b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def main():
 pin(HERE/'verification/AUDIT_MEMBERS.json');pin(HERE/'verification/CONTROL_PLAN.json');allowed=json.loads((HERE/'verification/AUDIT_MEMBERS.json').read_text());plan=json.loads((HERE/'verification/CONTROL_PLAN.json').read_text())
 for n,want in allowed.items():
  rel=Path(n);need(not rel.is_absolute() and '..' not in rel.parts,'unsafe member');need(not any(x in rel.parts for x in ['private','tmp','rendered','__pycache__']),'private member');need(pin(AUDIT/rel)==want,'authored member pin mismatch '+n)
 current=AUDIT/plan['current_pr_root'];need(pin(current/'MANIFEST.json')==plan['current_pr_manifest'],'current PR manifest mismatch');need(pin(AUDIT/'FINAL_PROOF.md')==plan['operative_proof'],'operative proof mismatch');need((current/'COUNTEREXAMPLE.md').read_bytes()==(AUDIT/'FINAL_PROOF.md').read_bytes(),'current proof differs')
 r=subprocess.run([sys.executable,'-B',str(current/'verify_all.py')],capture_output=True);need(r.returncode==0 and not r.stderr,'current edition verification failed: '+r.stderr.decode())
 out=json.loads(r.stdout);need(out['status']=='PASS' and len(out['runs'])==plan['expected_positive_runs'] and len(out['actual_wrong_result_failures'])==plan['expected_actual_wrong_result_failures'],'incomplete exact verification')
 print(json.dumps({'status':'PASS','authored_audit_members':len(allowed),'current_pr_members':out['member_count'],'runs':out['runs'],'actual_wrong_result_failures':out['actual_wrong_result_failures'],'finite_diagnostics_only':True,'source_body_custody_checks':'Private source bodies intentionally excluded; only authored released members authenticated offline.'},sort_keys=True,indent=2))
if __name__=='__main__':main()
