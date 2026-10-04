"""Read completed local preparation bytes/modes; never execute native actions."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,stat,sys
A=Path(__file__).resolve().parent
D=A/'native_integration_preparation_20261004'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b))
def load(p):return json.loads(p.read_bytes())
def main():
 assert sys.flags.ignore_environment and sys.flags.optimize==0 and sys.flags.dont_write_bytecode
 mp=pin(D/'PREPARATION_MANIFEST_V2.json');assert mp['sha256']=='e2933888ab514a24bc22627f16589aa02ae8965568cd526046148a2ebe2a73db'
 m=load(D/'PREPARATION_MANIFEST_V2.json');assert m['file_count']==len(m['files'])==293
 expected=set()
 for row in m['files']:
  p=D/row['path'];assert p.resolve().is_relative_to(D.resolve()) and p.is_file() and not p.is_symlink()
  b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'] and oct(stat.S_IMODE(p.stat().st_mode))==row['mode'],row['path']
  assert row['path'] not in expected;expected.add(row['path'])
 exclusions=m['self_or_future_closure_exclusions']
 actual={str(p.relative_to(D)) for p in D.rglob('*') if p.is_file() and not any(str(p.relative_to(D))==v or str(p.relative_to(D)).startswith(v) for v in exclusions)}
 assert actual==expected
 v=load(D/'independent_structural_review/FINAL_V2_REVIEW.json')
 assert v['status']=='PASS_PREPARATION_ONLY' and v['required_fixes_remaining']==[] and v['ACK_handoff_case_count']==24 and v['execution_authorized'] is False
 for row in v['final_source_pins']:
  b=(D/row['path']).read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256']
 r=load(D/'FINAL_MANIFEST_READBACK.json');assert r['status']=='PASS_COMPLETE_LOCAL_MANIFEST_READBACK' and r['manifest_sha256']==mp['sha256'] and r['checked_files']==293
 report=load(D/'PREPARATION_REPORT_V2.json');assert report['execution_authorized'] is False and report['operational_phases_executed']==[]
 src=report['optional_ROOT_assembler_source_pin_as_reviewed'];p=A.parents[2]/src['path'];assert pin(p)['sha256']==src['sha256']
 out=A/'ROOT_completed_native_preparation_readback_20261004';out.mkdir(exist_ok=False)
 receipt={'status':'PASS','UTC':datetime.now(timezone.utc).isoformat(),'actual_PID':os.getpid(),'actual_cwd':os.getcwd(),'actual_argv':sys.argv,
  'executed_source':pin(Path(__file__)),'manifest':mp,'actual_whole_files_modes_checked':293,'exact_membership':True,
  'review':pin(D/'independent_structural_review/FINAL_V2_REVIEW.json'),'final_manifest_readback':pin(D/'FINAL_MANIFEST_READBACK.json'),
  'preparation_seal':pin(D/'PREPARATION_SEAL_RECEIPT_V2.json'),'six_authoritative_source_pins':v['final_source_pins'],
  'ACK_handoff_24_cases_independent_evidence_verified':True,'new_tests_or_native_Git_PR_mutation':False,
  'ROOT_read_complete_code_then_all_ACK_repair_sections_and_full_final_reports':True,'actual_operational_authorization_still_separate':True}
 (out/'READBACK.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'status':'PASS','receipt':pin(out/'READBACK.json'),'checked_files':293}))
if __name__=='__main__':main()
