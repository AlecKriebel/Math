import sys,os,json,hashlib,subprocess,datetime
from pathlib import Path
sys.dont_write_bytecode=True
A=Path(__file__).resolve().parents[1];R=A/'newreviews/package_04';O=A/'root_reproduction/whole04_20261016';O.mkdir(exist_ok=True)
def load(p):return json.loads(p.read_text())
def need(c,s):
 if not c:raise RuntimeError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
receipts=[]
def run(argv,ok=True):
 e=os.environ.copy();e['PYTHONDONTWRITEBYTECODE']='1';p=subprocess.run(argv,cwd=O,env=e,capture_output=True,text=True);receipts.append({'argv':argv,'cwd':str(O),'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'expected_success':ok});save(O/'ACTUAL_COMMANDS.json',receipts);need((p.returncode==0)==ok,'command failed');return p
py='/opt/homebrew/bin/python3.14'
run([py,'-B',str(R/'verify_seal.py')])
for s in load(R/'SOURCE_READ_LEDGER.json')['sources']:
 p=Path(s['path']);need(p.stat().st_size==s['bytes'] and sha(p)==s['sha256'],'primary identity')
src=(R/'fullmath.py').read_text().replace('HERE=Path(__file__).resolve().parent','HERE=Path('+repr(str(O))+')').replace("KIT=HERE.parents[1]/'preprint_v1_0/verification_kit'","KIT=Path("+repr(str(A/'preprint_v1_0/verification_kit'))+")")
(O/'fullmath_replay.py').write_text(src)
src=(R/'custody.py').read_text().replace("HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];D=BASE/'preprint_v1_0';K=D/'verification_kit';R=BASE/'repairs/archive_wording01'","HERE=Path("+repr(str(O))+");BASE=Path("+repr(str(A))+");D=BASE/'preprint_v1_0';K=D/'verification_kit';R=BASE/'repairs/archive_wording01'")
(O/'custody_replay.py').write_text(src)
for flags in [[],['-O']]:
 p=run([py,'-B',*flags,str(R/'independent_controls.py')]);need(json.loads(p.stdout)==load(R/'INDEPENDENT_RESULTS.json'),'complete controls JSON')
 for fault in ['insertion','parity','crossing']:run([py,'-B',*flags,str(R/'independent_controls.py'),'--fault',fault],False)
 run([py,'-B',*flags,str(O/'fullmath_replay.py')]);n='FULL_MATHEMATICAL_OUTPUT_COMPARISON_O.json' if flags else 'FULL_MATHEMATICAL_OUTPUT_COMPARISON.json';need(load(O/n)==load(R/n),'complete candidate math fields')
run([py,'-B',str(O/'custody_replay.py')])
run([py,'-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',str(A/'preprint_v1_0/deposit_metadata.json')])
run([py,'-B',str(R/'verify_seal.py')])
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_ADOPT_COMPLETE_WHOLE04_ZERO_ACTIONABLE_PENDING_CURRENT_TERMINAL_ADMIN','ROOT_full_report_independent_derivation_source_ledger_new_controls_fullmath_and_custody_code_read':True,'whole_reviews_completed':4,'minimum_whole_reviews':2,'finding_counts':{'P0':0,'P1':0,'P2':0,'P3':0},'frozen_inputs':801,'sealed_outputs':52,'output_pins_sha256':sha(R/'OUTPUT_PINS.json'),'actual_root_commands':receipts,'new_controls_full_JSON_equals_reviewer':True,'all_candidate_mathematical_fields_normal_optimized_equal_review':True,'root_custody':load(O/'CUSTODY_RESULTS.json'),'scope':'Finite simultaneous-conjugacy classes and attained finite maximum for one boundary twist under essential positive curves, fixed genus and pairwise geometric intersection<=1. Separate restricted arbitrary-length clause negative; higher-genus exact maximum/classification bundle PARTIAL. Priority/novelty/worldwide openness UNKNOWN.','review_PDF_scope':'Reviewer actual standalone compilation and all seven delivered pages individually viewed; ROOT did not repeat compilation/render during adoption.','historical_events':'Two explicit ENOSPC copytree interruptions and corrected local over-specific symlink diagnostic assertion preserved. Older erasing-fault cause remains UNESTABLISHED; ROOT older attempt02 cause UNCONFIRMED.','terminal_administration_and_external_ROOT_final_integrity_required':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,'candidate_and_old_reviews_unchanged':True}
save(A/'ROOT_WHOLE_PACKAGE_REVIEW_04.json',record)
print(json.dumps({'status':'PASS_ADOPTED_ZERO','commands':len(receipts),'inputs':801,'outputs':52}))
