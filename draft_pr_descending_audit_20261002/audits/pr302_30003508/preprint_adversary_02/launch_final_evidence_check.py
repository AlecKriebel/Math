"""Actual Popen launch and full prelaunch-source/stream capture of final check."""
import json,os,sys
from capture import HERE,capture
def main():
 sources=[HERE/n for n in ['authenticate_final_evidence.py','launch_final_evidence_check.py','REPORT.md','READ_LEDGER.md','DERIVATION.md','DERIVATION_checkpoint_50.md','DERIVATION_EDITORIAL_RECONCILIATION.json','VERDICT.json','SOURCE_ARCHIVE_INDEX.json','SOURCE_ARCHIVE_CATEGORY_CORRECTION.json','TOOL_CHECK_FAILURES.json','INDEPENDENT_RECONSTRUCTION_CHECKPOINT.json','AUTHENTICATION_AND_REPLAY.json','EVIDENCE_CROSSCHECK.json','prepare_review_outputs.py','correct_external_source_archive.py','authenticate_and_replay.py','check_package_evidence.py','check_package_evidence_v02.py']]
 result,out,err=capture('final_evidence_authentication',[sys.executable,'-E','-B',str(HERE/'authenticate_final_evidence.py')],HERE,sources)
 print(json.dumps(dict(actual_launcher_PID=os.getpid(),actual_checker_PID=result['actual_child_PID'],exit_code=result['exit_code'],stdout=out.decode(),stderr=err.decode())))
 if result['exit_code']or err:raise SystemExit(1)
if __name__=='__main__':main()
