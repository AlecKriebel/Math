#!/usr/bin/env python3
"""Local regression: correct disposition must not bypass later acceptance gates."""
import argparse,hashlib,importlib.util,json,tempfile
from pathlib import Path
from datetime import datetime,timezone
P=Path(__file__).resolve().parent
GOOD='PREPARE_EXPLICITLY_ATTRIBUTED_APPLICATION_NOTE'
OLD='EVALUATE_AND_IF_ALL_FINAL_GATES_PASS_ACCEPT_EXPLICITLY_ATTRIBUTED_CLASSICAL_COROLLARY'
HEAD='704685791ec0053dc0a52590fdef49ed4aae61d9'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 path=P/'merge_pr919.py';spec=importlib.util.spec_from_file_location('pr919_merge_gate_regression',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 def forbidden(*a,**k):raise RuntimeError('UNEXPECTED_EXTERNAL_ACTION')
 m.run=m.rawblob=m.view=forbidden
 rows=[]
 with tempfile.TemporaryDirectory(dir=P/'audits/pr919_30002555/publication/tmp',prefix='disposition-gate-') as td:
  m.A=Path(td);(m.A/'publication').mkdir();(m.A/'publication/PREPUBLICATION_FREEZE.json').write_text('{}')
  cases=[('current_label_no_acceptance',GOOD,{'accepted':False},'Exact-source acceptance'),('obsolete_label_rejected',OLD,{'accepted':False},'Publication disposition changed'),('unsupported_label_rejected','UNSUPPORTED',{'accepted':False},'Publication disposition changed'),('wrong_head_rejected',GOOD,{'accepted':True,'original_pr_head':'0'*40,'full_package_reviews':[{},{}]},'Exact-source acceptance'),('one_review_rejected',GOOD,{'accepted':True,'original_pr_head':HEAD,'full_package_reviews':[{}]},'Exact-source acceptance'),('unbound_freeze_rejected',GOOD,{'accepted':True,'original_pr_head':HEAD,'full_package_reviews':[{},{}],'freeze_sha256':'0'*64},'Accepted freeze changed')]
  for name,decision,acceptance,expected in cases:
   (m.A/'PUBLICATION_DISPOSITION.json').write_text(json.dumps({'decision':decision}));(m.A/'ACCEPTANCE.json').write_text(json.dumps(acceptance));caught=''
   try:m.main()
   except RuntimeError as error:caught=str(error)
   rows.append(dict(case=name,expected_guard=expected,actual_guard=caught,passed=caught.startswith(expected)))
 result=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS' if all(r['passed'] for r in rows) else 'FAIL_EXPECTED_BEFORE_REPAIR',helper_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),cases=len(rows),passed=sum(r['passed'] for r in rows),no_external_action=True,rows=rows)
 if any(r['actual_guard']=='UNEXPECTED_EXTERNAL_ACTION' for r in rows):raise RuntimeError('Regression reached forbidden external action')
 args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if result['status']=='PASS' else 1)
if __name__=='__main__':main()
